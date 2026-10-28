from fastapi.testclient import TestClient
from sqlalchemy import select

import app.main as main_module
from app.database import Lead
from app.email_service import EmailResult, send_confirmation
from app.main import create_app


def make_client(email_sender=None):
    application = create_app("sqlite://", email_sender=email_sender or (lambda *_: EmailResult("not_configured")))
    return application, TestClient(application)


def test_landing_page_shows_useful_preview_and_keeps_full_comparison_locked():
    _, client = make_client()
    with client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Tři různé přístupy k americkým akciím" in response.text
    assert "0,0545 %" in response.text
    assert "0,18 %" in response.text
    assert 'id="full-comparison"' in response.text
    assert 'id="full-comparison" aria-labelledby="full-title" hidden' in response.text


def test_new_lead_is_saved_before_unlock_and_email_is_personalized():
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
        assert response.json() == {"recorded": True, "email_status": "accepted", "message": "Děkujeme, vaše srovnání je nyní odemčeno."}
        with application.state.session_factory() as session:
            lead = session.scalar(select(Lead))
            assert lead is not None
            assert lead.first_name == "Anna"
            assert lead.email == "anna.example@example.com"
            assert lead.marketing_consent is True
            assert lead.marketing_consent_at is not None
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
        assert response.json()["email_status"] == "failed"
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
        response = client.post(
            "/api/leads",
            json={"first_name": "Eva", "email": "eva@example.com", "marketing_consent": False},
        )

    assert response.status_code == 200
    assert response.json()["email_status"] == "not_configured"


def test_real_email_adapter_does_not_fake_sending_without_credentials(monkeypatch):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    monkeypatch.delenv("RESEND_FROM_EMAIL", raising=False)

    result = send_confirmation("Eva", "eva@example.com")

    assert result.status == "not_configured"
