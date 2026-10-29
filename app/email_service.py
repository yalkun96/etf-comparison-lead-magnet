from dataclasses import dataclass
from html import escape
import os

import resend


@dataclass(frozen=True)
class EmailResult:
    status: str


def send_confirmation(first_name: str, recipient: str) -> EmailResult:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    from_email = os.getenv("RESEND_FROM_EMAIL", "").strip()
    site_url = os.getenv(
        "SITE_URL",
        "http://127.0.0.1:8000",
    ).rstrip("/")

    if not api_key or not from_email:
        print("Resend is not configured: API key or sender is missing.")
        return EmailResult(status="not_configured")

    name = first_name.strip() or "investore"

    payload = {
        "from": from_email,
        "to": [recipient],
        "subject": "Vaše srovnání ETF je připravené",
        "text": (
            f"Dobrý den, {name},\n\n"
            "Vaše srovnání ETF je připravené.\n"
            f"Otevřete stránku: {site_url}\n"
        ),
        "html": (
            f"<p>Dobrý den, {escape(name)},</p>"
            "<p>Vaše srovnání ETF je připravené.</p>"
            f'<p><a href="{escape(site_url, quote=True)}">'
            "Otevřít srovnání ETF</a></p>"
        ),
    }

    try:
        resend.api_key = api_key
        result = resend.Emails.send(payload)

        email_id = (
            result.get("id")
            if hasattr(result, "get")
            else getattr(result, "id", None)
        )

        if email_id:
            print(f"Confirmation email accepted by Resend: id={email_id}")
            return EmailResult(status="accepted")

        print(
            "Resend returned a response without an email ID. "
            f"Response type: {type(result).__name__}"
        )
        return EmailResult(status="failed")

    except Exception as exc:
        print(
            "Resend send failed: "
            f"type={type(exc).__name__}, "
            f"message={str(exc)[:300]}"
        )
        return EmailResult(status="failed")