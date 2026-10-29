from sqlalchemy import inspect, select
from fastapi.testclient import TestClient

import app.main as main_module
from app.database import Lead, ensure_lead_attribution_columns, make_engine
from app.email_service import EmailResult
from app.main import create_app


def make_client():
    application = create_app("sqlite://", email_sender=lambda *_: EmailResult("not_configured"))
    return application, TestClient(application)


def test_event_endpoint_accepts_funnel_stages_and_campaign_tags_without_contact_data(caplog):
    _, client = make_client()
    payload = {
        "event": "lead_offer_view",
        "placement": "lead_offer",
        "utm_source": "newsletter",
        "utm_medium": "paid_social",
        "utm_campaign": "concept_a",
        "utm_content": "creative_1",
        "utm_term": "new investor",
    }
    with caplog.at_level("INFO", logger="etf_comparison"), client:
        response = client.post("/api/events", json=payload)

    assert response.status_code == 204
    assert "funnel_event=lead_offer_view" in caplog.text
    assert '"utm_campaign":"concept_a"' in caplog.text
    assert '"utm_term":"new investor"' in caplog.text
    assert "email=" not in caplog.text
    assert "newsletter@example" not in caplog.text


def test_lead_attribution_is_persisted_and_success_event_is_logged_after_save(caplog):
    application, client = make_client()
    payload = {
        "first_name": "Jana",
        "email": "jana@example.com",
        "marketing_consent": False,
        "utm_source": "social",
        "utm_medium": "paid",
        "utm_campaign": "concept_b",
        "utm_content": "variant_2",
        "utm_term": "beginner ETF",
    }
    with caplog.at_level("INFO", logger="etf_comparison"), client:
        response = client.post("/api/leads", json=payload)
        assert response.status_code == 200
        with application.state.session_factory() as session:
            lead = session.scalar(select(Lead).where(Lead.email == "jana@example.com"))
            assert lead is not None
            assert (lead.utm_source, lead.utm_medium, lead.utm_campaign) == ("social", "paid", "concept_b")
            assert (lead.utm_content, lead.utm_term) == ("variant_2", "beginner ETF")

    assert "funnel_event=lead_submission_success placement=form" in caplog.text
    assert '"utm_campaign":"concept_b"' in caplog.text
    assert "jana@example.com" not in caplog.text
    assert "Jana" not in caplog.text


def test_missing_repeat_attribution_preserves_existing_campaign_values():
    application, client = make_client()
    with client:
        first = client.post(
            "/api/leads",
            json={"first_name": "Jana", "email": "jana@example.com", "utm_source": "social", "utm_campaign": "concept_a"},
        )
        second = client.post(
            "/api/leads",
            json={"first_name": "Jana", "email": "jana@example.com"},
        )
        assert first.status_code == second.status_code == 200
        with application.state.session_factory() as session:
            lead = session.scalar(select(Lead).where(Lead.email == "jana@example.com"))
            assert lead.utm_source == "social"
            assert lead.utm_campaign == "concept_a"


def test_failed_lead_save_does_not_log_success_event(monkeypatch, caplog):
    _, client = make_client()
    monkeypatch.setattr(
        main_module,
        "record_lead",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("database unavailable")),
    )
    with caplog.at_level("INFO", logger="etf_comparison"), client:
        response = client.post(
            "/api/leads",
            json={"first_name": "Jana", "email": "jana@example.com", "utm_campaign": "concept_a"},
        )
    assert response.status_code == 503
    assert "funnel_event=lead_submission_success" not in caplog.text


def test_contact_like_campaign_value_is_dropped_from_event_log(caplog):
    _, client = make_client()
    with caplog.at_level("INFO", logger="etf_comparison"), client:
        response = client.post(
            "/api/events",
            json={"event": "landing_page_view", "utm_campaign": "visitor@example.com"},
        )
    assert response.status_code == 204
    assert "visitor@example.com" not in caplog.text
    assert 'attribution={}' in caplog.text


def test_startup_migration_adds_attribution_columns_to_existing_lead_table():
    engine = make_engine("sqlite://")
    with engine.begin() as connection:
        connection.exec_driver_sql("CREATE TABLE leads (id INTEGER PRIMARY KEY)")
    ensure_lead_attribution_columns(engine)
    columns = {column["name"] for column in inspect(engine).get_columns("leads")}
    assert {"utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"} <= columns
    engine.dispose()


def test_browser_hooks_use_visibility_and_real_interaction_and_forward_campaign_tags():
    script = (main_module.ROOT / "static/js/site.js").read_text()
    assert 'track("landing_page_view", "landing_page")' in script
    assert 'new IntersectionObserver' in script
    assert 'trackOnce("lead_offer_view", "lead_offer")' in script
    assert 'trackOnce("lead_offer_view", "lead_modal")' in script
    assert 'trackOnce("comparison_interaction", "comparison")' in script
    assert 'if (!event.isTrusted' in script
    assert 'trackOnce("form_start", "form")' in script
    assert 'form.addEventListener("keydown", recordFormStart)' in script
    assert 'track("lead_submission_success"' not in script
    assert '...campaignAttribution' in script
    for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"):
        assert field in script


def test_success_event_cannot_be_forged_through_public_event_endpoint():
    _, client = make_client()
    with client:
        response = client.post("/api/events", json={"event": "lead_submission_success", "placement": "form"})
    assert response.status_code == 422
