"""FastAPI application for the single-page ETF comparison."""

from contextlib import asynccontextmanager
import json
import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database import Base, Lead, UTM_FIELDS, ensure_lead_attribution_columns, get_session, make_engine, make_session_factory, record_lead
from app.email_service import EmailResult, send_confirmation
from app.funds import (
    COMMON_ISSUER_NOTE,
    EXCHANGE_SOURCE,
    FUNDS,
    PREVIEW_FUNDS,
    STXF_HISTORY_URL,
    STXF_TICKER_URL,
    STXG_SUPPLEMENT_URL,
)

load_dotenv()

logger = logging.getLogger("etf_comparison")
ROOT = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(ROOT / "templates"))


class CampaignAttribution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    utm_source: str | None = Field(default=None, max_length=100)
    utm_medium: str | None = Field(default=None, max_length=100)
    utm_campaign: str | None = Field(default=None, max_length=100)
    utm_content: str | None = Field(default=None, max_length=100)
    utm_term: str | None = Field(default=None, max_length=100)

    @field_validator(*UTM_FIELDS, mode="before")
    @classmethod
    def normalize_campaign_value(cls, value):
        if value is None or not isinstance(value, str):
            return None
        normalized = " ".join(value.split()).strip()
        if not normalized or len(normalized) > 100:
            return None
        # Campaign tags must be identifiers, never contact details or URLs.
        if "@" in normalized or re.search(r"https?://", normalized, re.IGNORECASE):
            return None
        return normalized


def campaign_values(model: CampaignAttribution) -> dict[str, str | None]:
    return {field: getattr(model, field) for field in UTM_FIELDS}


def log_funnel_event(event: str, placement: str, attribution: dict[str, str | None] | None = None) -> None:
    campaign = {key: value for key, value in (attribution or {}).items() if value}
    logger.info(
        "funnel_event=%s placement=%s attribution=%s",
        event,
        placement,
        json.dumps(campaign, ensure_ascii=True, sort_keys=True, separators=(",", ":")),
    )


class LeadSubmission(CampaignAttribution):
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


class FunnelEvent(CampaignAttribution):
    event: str = Field(pattern=r"^(landing_page_view|comparison_interaction|lead_offer_view|form_start|cta_interaction|email_accepted|email_failed|email_not_configured|email_status_unknown)$")
    placement: str | None = Field(default=None, pattern=r"^(landing_page|comparison|lead_offer|lead_modal|form|email|hero|preview|table_unlock|lead_flow)$")

class ConfirmationRequest(BaseModel):
    email: EmailStr


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
        ensure_lead_attribution_columns(engine)
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
                "preview_funds": PREVIEW_FUNDS,
                "exchange_source": EXCHANGE_SOURCE,
                "common_issuer_note": COMMON_ISSUER_NOTE,
                "stxf_history_url": STXF_HISTORY_URL,
                "stxf_ticker_url": STXF_TICKER_URL,
                "stxg_supplement_url": STXG_SUPPLEMENT_URL,
            },
        )

    @application.post("/api/events", status_code=204)
    def record_funnel_event(event: FunnelEvent):
        # Only allowlisted campaign identifiers accompany event names; no contact data is accepted.
        log_funnel_event(event.event, event.placement or "none", campaign_values(event))
        return Response(status_code=204)

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
                attribution=campaign_values(submission),
            )
        except (SQLAlchemyError, RuntimeError):
            session.rollback()
            logger.error("Lead recording failed; comparison remains locked.")
            raise HTTPException(
                status_code=503,
                detail="Údaje se nepodařilo uložit. Zkuste to prosím znovu.",
            ) from None

        # This event is emitted only after record_lead has committed successfully.
        log_funnel_event("lead_submission_success", "form", campaign_values(submission))
        return {
            "recorded": True,
            "message": "Děkujeme, vaše srovnání je nyní odemčeno.",
        }

    @application.post("/api/confirmation-email")
    def send_confirmation_email(
        submission: ConfirmationRequest,
        session: Session = Depends(session_dependency),
    ):
        normalized_email = str(submission.email).strip().casefold()
        lead = session.scalar(select(Lead).where(Lead.email == normalized_email))
        if lead is None:
            raise HTTPException(status_code=404, detail="Uloženou žádost se nepodařilo najít.")

        try:
            result: EmailResult = email_sender(lead.first_name, normalized_email)
            email_status = result.status
        except Exception:
            logger.error("Confirmation email attempt failed after lead recording.")
            email_status = "failed"

        if email_status not in {"accepted", "failed", "not_configured"}:
            email_status = "failed"
        return {"email_status": email_status}

    return application


app = create_app()
