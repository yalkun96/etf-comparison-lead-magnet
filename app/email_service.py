"""Optional Resend adapter. No credentials means no email is sent."""

from dataclasses import dataclass
from html import escape
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class EmailResult:
    status: str


def send_confirmation(first_name: str, recipient: str) -> EmailResult:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    from_email = os.getenv("RESEND_FROM_EMAIL", "").strip()
    site_url = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")

    if not api_key or not from_email:
        return EmailResult(status="not_configured")

    safe_name = escape(first_name)
    safe_url = escape(site_url, quote=True)
    plain_text = (
        f"Dobrý den, {first_name},\n\n"
        "děkujeme za zájem o srovnání ETF STXF, STXG a STXV. "
        f"Přehled najdete na této stránce: {site_url}\n\n"
        "Po návratu na stránku zadejte stejný e-mail a srovnání znovu otevřete.\n\n"
        "Tento e-mail potvrzuje vaši žádost o srovnání. Nejde o marketingový e-mail."
    )
    html = (
        f"<p>Dobrý den, {safe_name},</p>"
        "<p>Děkujeme za zájem o srovnání ETF STXF, STXG a STXV. "
        f'<a href="{safe_url}">Otevřít srovnání</a>.</p>'
        "<p>Po návratu na stránku zadejte stejný e-mail a srovnání znovu otevřete.</p>"
        "<p>Tento e-mail potvrzuje vaši žádost o srovnání. Nejde o marketingový e-mail.</p>"
    )
    payload = {
        "from": from_email,
        "to": [recipient],
        "subject": "Vaše srovnání ETF je připravené",
        "text": plain_text,
        "html": html,
    }
    request = Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=8) as response:
            if 200 <= response.status < 300:
                return EmailResult(status="accepted")
            return EmailResult(status="failed")
    except (HTTPError, URLError, TimeoutError, OSError):
        return EmailResult(status="failed")
