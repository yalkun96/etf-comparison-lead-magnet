"""FastAPI application for the single-page ETF comparison."""

from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database import Base, get_session, make_engine, make_session_factory, record_lead
from app.email_service import EmailResult, send_confirmation
from app.funds import (
    CHECKED_ON,
    COMMON_ISSUER_NOTE,
    EXCHANGE_SOURCE,
    FUNDS,
    STXF_HISTORY_URL,
    STXF_TICKER_URL,
    STXG_SUPPLEMENT_URL,
)

load_dotenv()

logger = logging.getLogger("etf_comparison")
ROOT = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(ROOT / "templates"))


class LeadSubmission(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    marketing_consent: bool = False

    @field_validator("first_name", mode="before")
    @classmethod
    def trim_first_name(cls, value):
        if not isinstance(value, str):
            raise ValueError("Zadejte prosím své jméno.")
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("Zadejte prosím své jméno.")
        return normalized


def create_app(
    database_url: str | None = None,
    email_sender=send_confirmation,
) -> FastAPI:
    selected_database_url = database_url or os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/etf_comparison",
    )
    engine = make_engine(selected_database_url)
    session_factory = make_session_factory(engine)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield
        engine.dispose()

    application = FastAPI(
        title="Srovnání amerických ETF",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    application.state.engine = engine
    application.state.session_factory = session_factory
    application.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

    def session_dependency():
        yield from get_session(session_factory)

    @application.get("/", response_class=HTMLResponse)
    def landing_page(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "funds": FUNDS,
                "checked_on": CHECKED_ON,
                "exchange_source": EXCHANGE_SOURCE,
                "common_issuer_note": COMMON_ISSUER_NOTE,
                "stxf_history_url": STXF_HISTORY_URL,
                "stxf_ticker_url": STXF_TICKER_URL,
                "stxg_supplement_url": STXG_SUPPLEMENT_URL,
            },
        )

    @application.post("/api/leads")
    def submit_lead(
        submission: LeadSubmission,
        session: Session = Depends(session_dependency),
    ):
        normalized_email = str(submission.email).strip().casefold()
        try:
            record_lead(
                session,
                first_name=submission.first_name,
                email=normalized_email,
                marketing_consent=submission.marketing_consent,
            )
        except (SQLAlchemyError, RuntimeError):
            session.rollback()
            logger.error("Lead recording failed; comparison remains locked.")
            raise HTTPException(
                status_code=503,
                detail="Údaje se nepodařilo uložit. Zkuste to prosím znovu.",
            ) from None

        try:
            email_result: EmailResult = email_sender(submission.first_name, normalized_email)
            email_status = email_result.status
        except Exception:
            # The lead is already committed; email failure must not relock the page.
            logger.error("Confirmation email attempt failed after lead recording.")
            email_status = "failed"

        if email_status not in {"accepted", "failed", "not_configured"}:
            email_status = "failed"

        return {
            "recorded": True,
            "email_status": email_status,
            "message": "Děkujeme, vaše srovnání je nyní odemčeno.",
        }

    return application


app = create_app()
