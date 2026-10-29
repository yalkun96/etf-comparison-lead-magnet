"""PostgreSQL persistence for submitted leads."""

from collections.abc import Generator
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, func, inspect, text
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    marketing_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    marketing_consent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    utm_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    utm_medium: Mapped[str | None] = mapped_column(String(100), nullable=True)
    utm_campaign: Mapped[str | None] = mapped_column(String(100), nullable=True)
    utm_content: Mapped[str | None] = mapped_column(String(100), nullable=True)
    utm_term: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


UTM_FIELDS = ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term")


def ensure_lead_attribution_columns(engine) -> None:
    """Add UTM columns to an existing leads table without altering stored leads."""
    inspector = inspect(engine)
    if not inspector.has_table("leads"):
        return
    existing = {column["name"] for column in inspector.get_columns("leads")}
    missing = [field for field in UTM_FIELDS if field not in existing]
    if not missing:
        return
    if engine.dialect.name not in {"postgresql", "sqlite"}:
        raise RuntimeError("Lead attribution migration supports PostgreSQL and SQLite only.")

    with engine.begin() as connection:
        for field in missing:
            if engine.dialect.name == "postgresql":
                connection.execute(text(f'ALTER TABLE leads ADD COLUMN IF NOT EXISTS "{field}" VARCHAR(100)'))
            else:
                connection.execute(text(f'ALTER TABLE leads ADD COLUMN "{field}" VARCHAR(100)'))


def make_engine(database_url: str):
    options = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
        if database_url in {"sqlite://", "sqlite:///:memory:"}:
            options["poolclass"] = StaticPool
    return create_engine(database_url, **options)


def make_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session(session_factory) -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def record_lead(
    session: Session,
    *,
    first_name: str,
    email: str,
    marketing_consent: bool,
    attribution: dict[str, str | None] | None = None,
) -> None:
    """Insert or update a lead under its normalized, unique email address."""
    now = datetime.now(timezone.utc)
    consent_at = now if marketing_consent else None
    values = {
        "first_name": first_name,
        "email": email,
        "marketing_consent": marketing_consent,
        "marketing_consent_at": consent_at,
        **{field: (attribution or {}).get(field) for field in UTM_FIELDS},
        "created_at": now,
        "updated_at": now,
    }

    dialect = session.get_bind().dialect.name
    if dialect == "postgresql":
        insert = postgresql_insert(Lead)
    elif dialect == "sqlite":
        insert = sqlite_insert(Lead)
    else:
        raise RuntimeError(f"Unsupported database dialect: {dialect}")

    statement = insert.values(**values).on_conflict_do_update(
        index_elements=[Lead.email],
        set_={
            "first_name": insert.excluded.first_name,
            "marketing_consent": insert.excluded.marketing_consent,
            "marketing_consent_at": insert.excluded.marketing_consent_at,
            **{field: func.coalesce(getattr(insert.excluded, field), getattr(Lead, field)) for field in UTM_FIELDS},
            "updated_at": insert.excluded.updated_at,
        },
    )
    session.execute(statement)
    session.commit()
