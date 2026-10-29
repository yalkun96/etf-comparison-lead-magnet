# Conversion Journey

## Approved visitor journey

1. The visitor arrives from an advertisement. The first screen immediately reflects the advertisement's promise: it previews STXF, STXG, and STXV and explains that the full comparison contains ten ETFs whose primary listing is NYSE.
2. The visitor can expand short explanations of broad U.S. large-cap, growth, value, benchmark, and expense-ratio terminology.
3. The page explains what additional verified information and caveats are included in the full comparison: ten fund rows with objectives, approaches, benchmarks or comparison indices, methodologies, stated annual expenses, illustrative costs for 100,000 Kč, sources, check dates, and limitations.
4. The visitor enters a required first name and email address. A separate, optional marketing-consent checkbox is initially unchecked. Access to the comparison does not depend on marketing consent.
5. The backend records the lead, then responds without waiting for the email provider. Repeated submissions with the same normalized email update the existing record rather than creating a duplicate.
6. After successful recording, the full comparison unlocks. If recording fails, it remains locked and the visitor can retry.
7. After the page unlocks, the browser requests a personalized transactional confirmation email using the first name already stored with the lead. The email links to the landing page, where the visitor can enter the same email to unlock the comparison again.
8. If email sending fails after the lead is recorded, the comparison remains unlocked and the page shows a truthful, non-blocking message. The page must not claim that an email was sent unless the sending attempt succeeded.

The full comparison is on the landing page. PDF generation, accounts, and one-time access tokens are outside the MVP.

## Comparison preview, modal, and funnel events

The landing page contains exactly one ETF comparison table in the early “Přehled” section. The first three funds are fully visible. Rows four to six are blurred, with a concise unlock explanation and CTA immediately after them in the same table; rows seven to ten stay concealed in that same table. After the lead-save endpoint confirms the database commit, all ten rows appear in their original order, the blur and lock message disappear, and the source and calculation notes below the table are revealed.

A native modal containing the single existing lead form opens six seconds after page load unless it was already dismissed or the comparison was unlocked in the current browser session. The visitor can close it with its close button or Escape; the page remains usable while it is closed. The table CTA opens the same modal again. The modal does not return automatically during that session after dismissal or successful unlock. The name and email fields, optional unchecked marketing consent, privacy wording, and existing endpoint are reused; no duplicate form is added.

The funnel stages are `landing_page_view`, `comparison_interaction`, `lead_offer_view`, `form_start`, and `lead_submission_success`. The browser logs page view, comparison interaction, lead-offer view, and form start through `POST /api/events`; lead-offer view fires when the in-page offer is visible or the modal opens. The backend emits `lead_submission_success` only after the lead transaction commits, and the public event endpoint does not accept that success event from clients. CTA and confirmation-email status events continue through the same endpoint. Events are written to application logs, not a separate analytics database. The five UTM values are attached to event records and submitted with the form, then stored on the existing lead row; no name or email is included in event payloads. There is no external analytics service or dashboard. Hosting-provider request/access logs are separate and remain subject to provider privacy review.

## Lead capture and privacy

The name and email are collected to record the request for the comparison and, for the email address, to send the requested transactional confirmation. The marketing checkbox records a separate choice; it is not required to access the comparison. Marketing emails must not be sent without the required consent or another verified legal basis.

Before launch, confirm the privacy notice, lawful basis and consent wording, data retention and deletion process, and provider terms and data-handling arrangements. Also confirm any email-sender domain and DNS requirements. These items are not treated as resolved by this plan.

## Product boundaries

- This is a single-page educational landing site, not a full web application.
- The ten provisional ETFs cover different U.S. equity approaches and include passive index funds, active strategies, small-cap, dividend-growth and sector exposure. They are not interchangeable or ranked; the comparison is educational, not personalized investment advice.
- The set contains seven Strive funds and three Baron funds. It is a small two-issuer selection, not a representative view of the ETF market. STXF and STXK have source naming caveats recorded in `docs/etf-research.md`.
- The 10-row comparison remains horizontally scrollable on narrow screens; the first column stays available as a ticker/name reference.
- The comparison uses public financial information. The email gate is a lead-generation mechanism, not security or confidential access control.
- Do not promise permanent access or any feature that has not been implemented and tested.

## Implementation details to confirm

The preferred implementation technologies are Python, FastAPI, Jinja2, plain HTML/CSS/Vanilla JavaScript, SQLAlchemy, and PostgreSQL. The final service setup remains to be confirmed before implementation. Check current Render Free and Supabase Free limitations and terms, and use Resend only if transactional sending can be configured and tested without spending. Confirm provider configuration, production environment variables, email delivery behavior, and duplicate-email handling before launch.
