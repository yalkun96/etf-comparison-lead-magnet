from fastapi.testclient import TestClient
from sqlalchemy import select

import app.main as main_module
from app.database import Lead
from app.email_service import EmailResult, send_confirmation
from app.main import create_app


def make_client(email_sender=None):
    application = create_app("sqlite://", email_sender=email_sender or (lambda *_: EmailResult("not_configured")))
    return application, TestClient(application)


def test_landing_page_has_one_early_ten_fund_table_with_locked_continuation():
    _, client = make_client()
    with client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Tři různé přístupy k americkým akciím" in response.text
    assert "0,0545 %" in response.text
    assert "0,18 %" in response.text
    assert 'id="full-comparison" aria-labelledby="full-title" hidden' in response.text
    assert "Úplné srovnání obsahuje 10 ETF." in response.text
    assert response.text.count("<table") == 1
    table = response.text.split('<table class="comparison-table"', 1)[1].split("</table>", 1)[0]
    assert table.count('class="comparison-fund-row') == 10
    assert table.count('locked-row"') == 7
    assert 'class="locked-preview" data-locked="true" aria-hidden="true"' in table
    assert 'class="locked-hidden" data-locked="true" aria-hidden="true"' in table
    assert "Odemknout úplné srovnání" in table
    assert response.text.count('id="lead-form"') == 1
    for ticker in ("STXF", "STXG", "STXV", "STXK", "STXD", "DRLL", "SHOC", "BROL", "RONB", "BCSM"):
        assert ticker in table


def test_new_lead_is_saved_and_unlock_response_precedes_personalized_email():
    sent = []

    def sender(first_name, recipient):
        sent.append((first_name, recipient))
        return EmailResult("accepted")

    application, client = make_client(sender)
    with client:
        response = client.post(
            "/api/leads",
            json={"first_name": " Anna ", "email": "Anna.Example@example.com", "marketing_consent": True},
        )
        assert response.status_code == 200
        assert response.json() == {"recorded": True, "message": "Děkujeme, vaše srovnání je nyní odemčeno."}
        with application.state.session_factory() as session:
            lead = session.scalar(select(Lead))
            assert lead is not None
            assert lead.first_name == "Anna"
            assert lead.email == "anna.example@example.com"
            assert lead.marketing_consent is True
            assert lead.marketing_consent_at is not None
        assert sent == []
        email_response = client.post("/api/confirmation-email", json={"email": "Anna.Example@example.com"})
        assert email_response.status_code == 200
        assert email_response.json() == {"email_status": "accepted"}
    assert sent == [("Anna", "anna.example@example.com")]


def test_repeat_normalized_email_updates_one_lead_and_choice():
    application, client = make_client()
    with client:
        first = client.post(
            "/api/leads",
            json={"first_name": "Petr", "email": "Petr@example.com", "marketing_consent": True},
        )
        repeat = client.post(
            "/api/leads",
            json={"first_name": "Petr Novák", "email": "  petr@EXAMPLE.com ", "marketing_consent": False},
        )
        assert first.status_code == repeat.status_code == 200
        with application.state.session_factory() as session:
            leads = session.scalars(select(Lead)).all()
            assert len(leads) == 1
            assert leads[0].email == "petr@example.com"
            assert leads[0].first_name == "Petr Novák"
            assert leads[0].marketing_consent is False
            assert leads[0].marketing_consent_at is None


def test_invalid_submission_is_rejected_server_side():
    application, client = make_client()
    with client:
        response = client.post("/api/leads", json={"first_name": "   ", "email": "not-an-email"})
        assert response.status_code == 422
        with application.state.session_factory() as session:
            assert session.scalar(select(Lead)) is None


def test_email_failure_does_not_undo_saved_lead_or_unlock_result():
    def failing_sender(*_):
        raise RuntimeError("provider unavailable")

    application, client = make_client(failing_sender)
    with client:
        response = client.post(
            "/api/leads",
            json={"first_name": "Jana", "email": "jana@example.com", "marketing_consent": False},
        )
        assert response.status_code == 200
        assert response.json()["recorded"] is True
        with application.state.session_factory() as session:
            assert session.scalar(select(Lead)) is not None
        email_response = client.post("/api/confirmation-email", json={"email": "jana@example.com"})
        assert email_response.status_code == 200
        assert email_response.json()["email_status"] == "failed"
        with application.state.session_factory() as session:
            assert session.scalar(select(Lead)) is not None


def test_database_failure_does_not_unlock_or_attempt_email(monkeypatch):
    called = []

    def sender(*args):
        called.append(args)
        return EmailResult("accepted")

    _, client = make_client(sender)
    monkeypatch.setattr(main_module, "record_lead", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError()))
    with client:
        response = client.post(
            "/api/leads",
            json={"first_name": "Jana", "email": "jana@example.com", "marketing_consent": False},
        )

    assert response.status_code == 503
    assert response.json()["detail"] == "Údaje se nepodařilo uložit. Zkuste to prosím znovu."
    assert called == []


def test_unconfigured_email_is_reported_without_claiming_delivery():
    _, client = make_client()
    with client:
        saved = client.post(
            "/api/leads",
            json={"first_name": "Eva", "email": "eva@example.com", "marketing_consent": False},
        )
        assert saved.status_code == 200
        response = client.post("/api/confirmation-email", json={"email": "eva@example.com"})

    assert response.status_code == 200
    assert response.json()["email_status"] == "not_configured"


def test_confirmation_email_requires_a_previously_saved_lead():
    called = []
    _, client = make_client(lambda *args: called.append(args) or EmailResult("accepted"))
    with client:
        response = client.post("/api/confirmation-email", json={"email": "missing@example.com"})

    assert response.status_code == 404
    assert called == []


def test_funnel_events_log_only_allowed_event_and_placement(caplog):
    _, client = make_client()
    with caplog.at_level("INFO", logger="etf_comparison"), client:
        response = client.post("/api/events", json={"event": "landing_page_view", "placement": "hero"})

    assert response.status_code == 204
    assert "funnel_event=landing_page_view placement=hero" in caplog.text
    assert "email=" not in caplog.text


def test_funnel_event_endpoint_rejects_contact_fields():
    _, client = make_client()
    with client:
        response = client.post(
            "/api/events",
            json={"event": "landing_page_view", "placement": "hero", "email": "person@example.com"},
        )

    assert response.status_code == 422


def test_real_email_adapter_does_not_fake_sending_without_credentials(monkeypatch):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    monkeypatch.delenv("RESEND_FROM_EMAIL", raising=False)

    result = send_confirmation("Eva", "eva@example.com")

    assert result.status == "not_configured"
