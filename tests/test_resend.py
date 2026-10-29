import resend
from dotenv import dotenv_values

config = dotenv_values(".env")

api_key = (config.get("RESEND_API_KEY") or "").strip()
sender = (config.get("RESEND_FROM_EMAIL") or "").strip()

if not api_key or not api_key.strip():
    raise RuntimeError("RESEND_API_KEY is missing in .env")

if not sender:
    raise RuntimeError("RESEND_FROM_EMAIL is missing in .env")

resend.api_key = api_key

try:
    result = resend.Emails.send({
        "from": sender,
        "to": ["yalkun9669@gmail.com"],
        "subject": "ETF project — email test",
        "html": "<p>Resend integration test successful.</p>",
    })

    print("Resend accepted the request.")
    print("Response type:", type(result).__name__)

except Exception as exc:
    print("Sending failed:", type(exc).__name__)
    print("Details:", str(exc))