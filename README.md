# ETF comparison lead magnet

A Czech-language educational landing page comparing ten NYSE-listed ETFs. The project uses FastAPI, Jinja2, plain HTML/CSS/JavaScript, SQLAlchemy, and PostgreSQL. The comparison is educational, not personalized investment advice. See [docs/etf-research.md](docs/etf-research.md) for source records and limitations and [docs/local-development.md](docs/local-development.md) for local setup.

## Funnel measurement

The existing `POST /api/events` endpoint validates event names and logs allowlisted events to the application log. There is no third-party analytics service or separate analytics database. Events do not contain names or email addresses. The five supported campaign query parameters are read on page load and sent with event requests and the lead submission. Contact-like values (including email-shaped values and URLs) are discarded; values are limited to 100 characters.

| Event | Recorded when | Storage |
|---|---|---|
| `landing_page_view` | The landing page finishes loading and its deferred script initializes. | Application log |
| `comparison_interaction` | The visitor first uses the comparison with a pointer, keyboard, or scroll interaction. | Application log |
| `lead_offer_view` | The in-page offer reaches at least 20% viewport visibility, or the lead modal opens. | Application log |
| `form_start` | The visitor first interacts with a form field or consent checkbox. | Application log |
| `lead_submission_success` | FastAPI emits this server-side event only after the lead write commits successfully; clients cannot submit this event through `/api/events`. | Application log |

The application continues to log CTA and confirmation-email status events. Campaign attribution (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`) is stored on the existing lead record in the `leads` table. On repeated submissions, a new non-empty UTM value replaces the prior value; missing values preserve the existing value. The application performs an additive startup migration for existing PostgreSQL and SQLite `leads` tables.

To inspect events locally, run the application as described in [docs/local-development.md](docs/local-development.md), then open a URL such as `http://127.0.0.1:8000/?utm_source=example&utm_medium=social&utm_campaign=concept_a`. Watch the server terminal for `funnel_event=... attribution={...}` lines. Inspect the corresponding lead row in PostgreSQL to confirm its UTM columns.

## Verification

Run focused tests with `pytest -q tests/test_funnel_measurement.py tests/test_lead_flow.py`. Tests use isolated SQLite and stub email senders; they do not send real email.

## Limitations

Application-log events are not durable analytics records and have no dashboard, user-level journey stitching, retention policy, or built-in aggregation. Counts may be lost when hosting logs expire. Lead attribution is last non-empty touch on the lead record, not a full multi-touch attribution model. Campaign parameters are campaign identifiers only; do not place personal information in UTM values.
