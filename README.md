# ETF comparison lead magnet

A Czech-language, single-page educational landing site comparing ten ETFs recorded as listed on the NYSE venue itself; NYSE Arca is excluded. The local application uses Python, FastAPI, Jinja2, HTML, CSS, Vanilla JavaScript, SQLAlchemy, and PostgreSQL. The comparison is not personalized investment advice. Product decisions and fund-level source records are documented in [docs/conversion-journey.md](docs/conversion-journey.md), [docs/ads.md](docs/ads.md), and [docs/etf-research.md](docs/etf-research.md).

## Audience and Offer

- **Audience:** Czech-language retail-investor prospects interested in understanding differences between U.S.-listed ETFs, particularly beginners who want to make sense of broad U.S. large-cap, growth, and value approaches.
- **Offer:** A free educational comparison of ten ETFs listed on the NYSE venue, unlocked on the page after the visitor submits a first name and email address.
- Marketing consent is separate, optional, and unchecked by default. It is not required to access the comparison.
- The content is educational and is not personalized investment advice. The funds are not presented as interchangeable choices or ranked from best to worst.
- A NYSE listing does not establish that a fund is available to a Czech retail investor. Broker-specific access and PRIIPs KID availability have not been verified.

The comparison and access flow are a lead-generation mechanism, not confidential content or a security boundary. The complete value exchange and limitations are described in the linked research and conversion documents.

## Section Order and Rationale

The page order follows the implemented template and the approved journey in [docs/conversion-journey.md](docs/conversion-journey.md):

1. **Ad-matched promise and initial fund preview.** The hero states “Srovnání 10 amerických ETF: přístup, cíle a roční náklady,” then names STXF, STXG, and STXV as the concrete preview. Its CTA moves to the first three funds. The table immediately shows those funds' approaches, objectives, benchmark methodology, stated annual fund expenses, illustrative costs, exchange venue, and links. Visitors can judge relevance before being asked for contact details.
2. **Terminology and the full-comparison offer.** A short callout directly below the single comparison table says the full comparison contains ten ETFs and explains what opens after a name and email are submitted. On screens up to 960px wide, the same `funds` data is presented as readable cards with expandable details; on wider screens it is shown as a table. Below it, expandable definitions explain large U.S. companies, growth, value, benchmark, and annual fund expenses. This puts the offer in context while helping beginners interpret the preview rather than asking them to decode jargon unaided.
3. **Contact choice through the existing form.** A native modal opens six seconds after page-script initialization unless it was dismissed or access was unlocked in the current browser session. The table CTA can reopen that same modal; closing it leaves the page usable. There is one form: first name and email are required; the separate marketing-consent checkbox is optional and initially unchecked. This offers a clear next step while preserving the visitor's choice and not making newsletter consent a condition of access. The six-second interruption may also create friction and is a testable hypothesis, not a proven improvement.
4. **Unlock after a saved lead.** The browser reveals the locked rows in the single desktop table or the matching mobile cards only after the lead endpoint confirms successful recording, and unhides the following comparison-details section. Both presentations are rendered from the same ten-fund data list and preserve the same order. If saving fails, the page keeps the comparison locked and allows a retry. Email sending happens afterward and does not control unlocking.
5. **Calculation, source notes, and caveats.** After unlock, the page displays the expense formula and exclusions, fund-level issuer and SEC links, source-check/document dates, benchmark-name caveats, exchange-scope explanation, Czech-access/KID limitations, and the educational disclaimer. This keeps the first view focused while making supporting evidence available with the complete comparison. The initial three rows already show their issuer and exchange links and the initial research-check date; the fuller source register and limitations are below the unlocked details.

The privacy information appears near the bottom of the page and in brief beside the form. It explains the implemented data flow and expressly warns that it is incomplete. The controller identity and contact details, legal bases, retention period, rights-request and withdrawal channel, production database/hosting provider and region, and Resend terms and data-transfer details remain to be supplied or verified. The page is not ready for public lead collection or a live advertising campaign until these facts are completed and reviewed.

## Data Sources and Research Dates

Research used primary issuer product pages and official fund documentation, together with relevant SEC records and filings: prospectuses, supplements, shareholder reports, and applicable fund records. Issuer exchange disclosures and official NYSE listing information were used where relevant to check the listing venue; NYSE Arca is outside the selection scope. The research record notes where a separate NYSE listing-page URL was not preserved and records alternate primary evidence and source caveats rather than treating every source trail as identical.

A **source-check date** is when a page or document was reviewed. It is distinct from a document date, reporting period, or financial value's own “as of” date. The original three candidates were checked on **October 28, 2026**; the seven additional candidates were checked on **October 29, 2026**. These are historical research-check dates; this README revision does not represent a new source check. This project contains ten funds from two issuers and is not a representative sample of the ETF market.

Known research limitations:

- **STXF and STXK benchmark names remain discrepant.** Current issuer pages and prospectus terminology differ. The issuer has not formally reconciled the naming; the source wording and caveats are preserved in the research file.
- Czech broker availability and PRIIPs KID status have not been verified. No claim is made that every fund can be bought by a Czech retail investor.
- Expense-ratio illustrations apply the stated annual fund operating expense ratio to a hypothetical investment. They are not forecasts or total ownership costs and exclude brokerage charges, bid-ask spreads, taxes, currency conversion, and other individual costs.
- Fund facts and documents may change and should be rechecked before publication.

See [docs/etf-research.md](docs/etf-research.md) for the complete source register, source-check dates, document/as-of dates, benchmark discrepancies, exclusions, calculation assumptions, and limitations.

## Expected Conversion Rate

The provisional planning target is **3–5% of unique landing-page visitors submitting a successfully recorded lead**.

This is an **unvalidated planning hypothesis** for prioritizing future optimization. It is not an industry benchmark, observed baseline, measured result, or claim of achieved performance. It assumes relevant Czech-language traffic, an ad promise that reasonably matches the landing page, a useful and credible comparison, a functioning lead form and email flow, and a clearly explained privacy and consent choice.

For this target:

- **Numerator:** unique visitors who submit a lead that is successfully committed to the database.
- **Denominator:** unique landing-page visitors over the same measurement period.
- The numerator and denominator must use a consistent time window and a defensible definition of a unique visitor.

Current funnel events are written to application logs. There is no durable analytics platform, reliable built-in unique-visitor aggregation, or analytics dashboard. Events have no stable visitor identifier, repeat successful submissions can produce another server-side success event for an existing lead, and logs may expire. Consequently, current logs cannot reliably establish this conversion rate. The target cannot be properly evaluated until reliable visitor-level measurement and adequate traffic are available.

## A/B Test Hypotheses (Ranked by Expected Impact)

These are hypotheses, not proven improvements. The current events (`landing_page_view`, `comparison_interaction`, `lead_offer_view`, `form_start`, and `lead_submission_success`) can describe some steps, but they do not provide reliable unique visitors, controlled variant assignment, or complete modal-dismissal measurement. Any test needs sufficient traffic, controlled assignment, consistent measurement, and an appropriate evaluation period before results are interpreted.

### Rank 1 — Hero headline and CTA clarity

- **Expected impact and rationale:** Highest of these hypotheses. A more specific promise may match the advertisement, clarify that the offer compares ten funds, and reduce ambiguity about what the visitor receives.
- **Control:** Current hero headline, “Srovnání 10 amerických ETF: přístup, cíle a roční náklady,” supporting text naming the three preview funds and describing the ten-fund comparison, and CTA “Prohlédnout první tři fondy”.
- **Variant:** Test a clearer, more specific headline and CTA that state the ten-fund NYSE comparison and its useful contents (approach, benchmark/methodology, and stated costs), while retaining the non-ranking educational caveat.
- **Possible mechanism:** Better ad-to-page message match could help relevant visitors understand the offer and take a next step; it could also attract less-qualified clicks if the copy overpromises.
- **Primary metric:** Successfully recorded leads per unique landing-page visitor, using the definitions above.
- **Guardrails:** `comparison_interaction`, `lead_offer_view`, and `form_start` progression; lead quality where it can be measured lawfully and consistently; email status (`email_accepted`, `email_failed`, `email_not_configured`, `email_status_unknown`). `email_accepted` means the provider accepted the request, not that it reached an inbox.

### Rank 2 — Lead form/modal timing and presentation

- **Expected impact and rationale:** Second. The current modal exposes the offer quickly but interrupts visitors who have not yet explored the comparison. Reducing interruption may help some visitors; delaying the form may mean fewer see it.
- **Control:** The existing modal opens six seconds after the deferred page script initializes, once per session unless dismissed or unlocked. The existing table CTA can reopen it.
- **Variant:** Show the same form only after a visitor activates the table's “Odemknout úplné srovnání” CTA; do not auto-open it.
- **Possible mechanism:** User-triggered presentation may respect visitor intent and reduce interruption/friction, but could reduce exposure and total form starts.
- **Primary metric:** Successfully recorded leads per unique landing-page visitor, plus offer-to-form-start and form-start-to-success rates if assignment and visitor measurement become reliable.
- **Guardrails:** `lead_offer_view`, `form_start`, `lead_submission_success`, form abandonment where measurable, email-status events, and modal dismissal. Modal dismissal is **not currently an event**, so that guardrail would require additional instrumentation before a test; it must not be inferred from the existing events.

### Rank 3 — Amount and usefulness of the pre-unlock comparison preview

- **Expected impact and rationale:** Third. The preview already demonstrates the format and names the full offer. Showing more may build trust, though it may also reduce the reason to submit a lead.
- **Control:** In the one existing table, rows 1–3 are readable, rows 4–6 are blurred, and rows 7–10 are concealed; the callout explains that the complete table has ten ETFs.
- **Variant:** Keep the same table and row order, but make rows 4–6 readable before unlock while leaving rows 7–10 concealed. No additional table is introduced.
- **Possible mechanism:** More visible examples may make the comparison's usefulness and breadth more credible, while giving away more information may reduce the incentive to unlock.
- **Primary metric:** Successfully recorded leads per unique landing-page visitor; `comparison_interaction` and `lead_offer_view` can help describe preview engagement but are not unique-user measures.
- **Guardrails:** `form_start` and `lead_submission_success` progression, modal dismissal if separately instrumented, email-status events, and lead quality where measurable. Watch whether additional preview exposure increases interaction but lowers lead submission.

No experiment has been run, and no result or statistical significance is claimed. Current logs cannot support reliable visitor-level A/B evaluation on their own.

## Funnel Measurement

The browser sends the page and interaction events to the existing `POST /api/events` endpoint. The backend validates an allowlist and writes the events to the application log; there is no third-party analytics service or separate analytics database. Event payloads do not include names or email addresses.

| Event | Recorded when | Storage |
|---|---|---|
| `landing_page_view` | The deferred browser script initializes on the landing page. | Application log |
| `comparison_interaction` | The visitor first uses the comparison table with a trusted pointer, keyboard, or scroll interaction. | Application log |
| `lead_offer_view` | The offer reaches at least 20% viewport visibility, or the modal opens; the page deduplicates this event. | Application log |
| `form_start` | The visitor first interacts with a name/email field or marketing checkbox. | Application log |
| `lead_submission_success` | FastAPI logs the event after the lead write commits; the public event endpoint does not accept this event. | Application log |

The app also records `cta_interaction` and confirmation-email status events: `email_accepted`, `email_failed`, `email_not_configured`, and `email_status_unknown`. UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, and `utm_term`) are read from the arrival URL and accompany event requests and lead submissions. Values are limited to 100 characters; email-shaped values and URLs are discarded, and campaign values should not contain personal information. The fields are stored on the existing lead record. Repeat submissions use a normalized email and update one lead: a supplied non-empty UTM value replaces the prior value, while a missing value preserves it. An additive startup migration adds missing UTM columns for existing PostgreSQL and SQLite lead tables. Attribution is last non-empty touch, not multi-touch attribution.

To inspect events locally, follow [docs/local-development.md](docs/local-development.md), open a URL such as `http://127.0.0.1:8000/?utm_source=example&utm_medium=social&utm_campaign=concept_a`, and inspect server output for `funnel_event=... attribution={...}`. Inspect the corresponding lead record to verify stored UTM fields. Application-log events are not durable analytics records, have no built-in retention policy, user-level journey stitching, or aggregation, and may be lost when hosting logs expire.

## Architecture and Local Setup

The application is a single-page FastAPI/Jinja2 site with plain HTML/CSS/Vanilla JavaScript, SQLAlchemy lead persistence, and PostgreSQL for local or managed storage. `app.main:app` is the Vercel entrypoint. Resend is used for the optional transactional email attempt after a lead is saved; email failure does not relock the comparison. For exact local database setup, environment variables, install/run commands, and manual browser checks, see [docs/local-development.md](docs/local-development.md).

The current `pyproject.toml` specifies Python `>=3.12,<3.15`; `docs/local-development.md` still says “Python 3.11 or later.” That setup requirement is stale and should be reconciled. The `Implementation details to confirm` paragraph at the end of [docs/conversion-journey.md](docs/conversion-journey.md) predates the local implementation: the stack and journey are now implemented locally, while public-service configuration and launch reviews remain outstanding.

## Verification

Focused automated checks use isolated SQLite databases and stub email senders, so they do not require the local PostgreSQL service or send real email:

```sh
pytest -q tests/test_funnel_measurement.py tests/test_lead_flow.py
```

The tests cover lead persistence and email-failure behavior, funnel event validation and attribution, and source-level browser hooks. They do not establish live email delivery, production PostgreSQL behavior, a successful Vercel deployment, or end-to-end behavior in every browser. Follow [docs/local-development.md](docs/local-development.md) for manual browser and local PostgreSQL checks. `tests/test_resend.py` can send a real email and should only be run deliberately with appropriate sender, recipient, and credentials.

## What Is Incomplete or Simplified

### Current gaps, unverified items, or outstanding reviews

- Funnel events are application-log entries rather than durable analytics records; there is no analytics dashboard or reliable built-in unique-visitor aggregation.
- UTM attribution stores the last non-empty touch on a lead, not a multi-touch journey.
- Czech broker availability and PRIIPs KID status remain unverified. No claim of Czech retail purchase availability is made.
- Privacy/legal review remains outstanding. The current notice is an interim explanation, not a complete public privacy notice. Before real advertising or contact collection, provide the controller's legal name, address and contact; verify the legal basis for storing the requested comparison access and sending the transactional confirmation, and the separate legal basis and wording for any future marketing; set and document lead-data retention and deletion arrangements; provide a working channel and process for rights requests and marketing-consent withdrawal; identify production hosting and database providers, processing locations, recipients and any international transfers; review provider terms/data-processing arrangements (including Resend if enabled); and confirm the email sender domain/DNS configuration. These details are not established by the repository and must not be invented.
- Fund data and issuer documents are historical research checks and need rechecking before publication. STXF and STXK benchmark-name discrepancies remain unresolved by the issuer.
- Python support documentation is inconsistent: `pyproject.toml` requires Python 3.12–3.14, while `docs/local-development.md` still mentions Python 3.11 or later.
- No durable visitor identity or experiment assignment is implemented, so unique-visitor conversion and controlled A/B tests cannot be evaluated from current funnel logs.

### Intentional MVP simplifications or exclusions

- The comparison contains ten funds from two issuers, not a representative sample of the ETF market.
- It is educational information, without personalized investment advice or a best-to-worst fund ranking.
- There is no PDF generation, user account, password, or one-time access token. A returning visitor can enter the same email again.
- The email gate is a lead-generation mechanism, not a security boundary; the underlying information is public.
- The page uses one comparison table, a compact pre-unlock preview, expandable glossary entries, and a single existing lead form. It has no advanced filtering, sorting, or search.
- Marketing consent is optional and does not control access to the comparison; marketing sending is not implemented in the current local MVP.
