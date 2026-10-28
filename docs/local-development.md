# Local Development

This project is a FastAPI and Jinja2 landing page with PostgreSQL lead storage. It does not deploy or create cloud resources. The form sends email only when Resend credentials and a verified sender are configured; otherwise it reports that no email was sent.

## Requirements

- Python 3.11 or later.
- PostgreSQL 14 or later, with `initdb`, `pg_ctl`, `createdb`, and `psql` available in the shell. On macOS, install PostgreSQL with Homebrew if needed.

## Create a local PostgreSQL database

From the project root, initialize a local-only database cluster. These example commands use port `55432` so an existing PostgreSQL service on port `5432` is not disturbed. The `trust` authentication options are for this disposable local development cluster only.

```sh
mkdir -p .local/postgres
initdb -D .local/postgres/data -U postgres --auth-local=trust --auth-host=trust
pg_ctl -D .local/postgres/data -l .local/postgres/server.log -o "-h 127.0.0.1 -p 55432" start
createdb -h 127.0.0.1 -p 55432 -U postgres etf_comparison
```

If you already have a database, skip this section and set its connection URL in `.env`.

## Install and run

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

The example database URL matches the local cluster above. Start the application:

```sh
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser. The first run creates the `leads` table automatically. Stop the local PostgreSQL cluster when finished:

```sh
pg_ctl -D .local/postgres/data stop
```

## Email configuration

Leave `RESEND_API_KEY` and `RESEND_FROM_EMAIL` blank to verify the lead-saving and comparison-unlocking flow without sending email. The page will state that confirmation email was not configured. To test real sending, configure a Resend key and verified sender in your private `.env`; never commit that file. `SITE_URL` is used as the return link. No email delivery was verified as part of local setup.

## Automated checks

```sh
source .venv/bin/activate
pytest -q
```

The critical form and persistence tests use an isolated in-memory SQLite database to avoid requiring the local PostgreSQL service. They do not replace manually checking the application against PostgreSQL.

When the same normalized email is submitted again, the row is updated with the latest name and checkbox state. An unchecked box clears the stored marketing-consent flag and timestamp; marketing sending is not implemented.

## Manual browser review

1. At a narrow mobile width, confirm the heading, benefit, and preview CTA are visible without scrolling.
2. Check the three preview cards on mobile and the compact comparison table on desktop.
3. Expand each glossary item with mouse, touch, and keyboard; confirm the focus indicator is visible and reduced-motion preference is respected.
4. Submit an empty form and an invalid email; confirm the browser and server reject them with clear messages.
5. With a working local PostgreSQL connection and email variables blank, submit a valid lead. Confirm the full comparison unlocks only after the response, the email-not-configured message is truthful, and the lead appears once in PostgreSQL.
6. Submit the same email again with different casing and surrounding spaces. Confirm there is still only one lead record and the comparison unlocks again.
7. Temporarily stop PostgreSQL and submit a lead. Confirm the page stays locked, provides a retry message, and does not claim a lead was recorded.
8. Review the full comparison's source links, STXF naming caveat, expense assumptions, data date, privacy placeholders, and educational disclaimer.

## Before public launch

Supply and review the actual data controller's identity and contact information, lawful basis and consent wording, data retention and deletion process, provider/data-transfer disclosures, sender domain and email configuration, and final privacy information. Verify the current limitations and terms of any free hosting or database services before configuring them. None are configured by this local-only step.
