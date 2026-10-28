# Conversion Journey

## Approved visitor journey

1. The visitor arrives from an advertisement. The first screen immediately reflects the advertisement's promise and previews the comparison of STXF, STXG, and STXV.
2. The visitor can expand short explanations of broad U.S. large-cap, growth, value, and expense-ratio terminology.
3. The page explains what additional verified information and caveats are included in the full comparison.
4. The visitor enters a required first name and email address. A separate, optional marketing-consent checkbox is initially unchecked. Access to the comparison does not depend on marketing consent.
5. The backend records the lead before the full comparison unlocks on the same page. Repeated submissions with the same normalized email must not create duplicate lead records.
6. After successful recording, the full comparison unlocks. If recording fails, it remains locked and the visitor can retry.
7. The service attempts to send a personalized transactional confirmation email using the visitor's first name. It links to the landing page, where the visitor can enter the same email to unlock the comparison again.
8. If email sending fails after the lead is recorded, the comparison remains unlocked and the page shows a truthful, non-blocking message. The page must not claim that an email was sent unless the sending attempt succeeded.

The full comparison is on the landing page. PDF generation, accounts, and one-time access tokens are outside the MVP.

## Lead capture and privacy

The name and email are collected to record the request for the comparison and, for the email address, to send the requested transactional confirmation. The marketing checkbox records a separate choice; it is not required to access the comparison. Marketing emails must not be sent without the required consent or another verified legal basis.

Before launch, confirm the privacy notice, lawful basis and consent wording, data retention and deletion process, and provider terms and data-handling arrangements. Also confirm any email-sender domain and DNS requirements. These items are not treated as resolved by this plan.

## Product boundaries

- This is a single-page educational landing site, not a full web application.
- STXF, STXG, and STXV represent different investment approaches; the comparison is educational, not a ranking or personalized investment advice.
- The comparison uses public financial information. The email gate is a lead-generation mechanism, not security or confidential access control.
- Do not promise permanent access or any feature that has not been implemented and tested.

## Implementation details to confirm

The preferred implementation technologies are Python, FastAPI, Jinja2, plain HTML/CSS/Vanilla JavaScript, SQLAlchemy, and PostgreSQL. The final service setup remains to be confirmed before implementation. Check current Render Free and Supabase Free limitations and terms, and use Resend only if transactional sending can be configured and tested without spending. Confirm provider configuration, production environment variables, email delivery behavior, and duplicate-email handling before launch.
