# AI Work Log

This is a factual summary of how AI assistance was used for the ETF comparison assignment. It is not a raw conversation export. Exact historical prompts are not reproduced here; consult separate native exports if available.

## Division of responsibilities

- **Developer:** Set the assignment goal, audience, approved product direction, conversion flow, and preferred technology constraints; reviewed proposed decisions and supplied build/runtime error messages for diagnosis. The developer reported checking local email configuration during troubleshooting. The project history assigns final diff review, manual browser checks, and deployment decisions to the developer, but does not establish that every final live/manual check has been completed.
- **ChatGPT:** Helped interpret the assignment and plan product decisions, ETF research criteria, the visitor journey, and advertising/copy concepts; compared alternatives and helped frame technical decisions and troubleshooting requests. The assistant's recommendations were subject to developer approval and source/document review.
- **Codex:** Inspected the repository and implemented or updated scoped application and documentation work recorded in the project history, including the landing-page and funnel work, local/deployment configuration, and dependency declarations. Codex reported its diffs and checks; those reports and automated tests do not substitute for developer review or live production verification.

The available history supports that responsibilities were shared. It does not support attributing every individual line, fund-selection judgment, or manual review to a specific person/tool beyond the decisions and actions described above.

## Instructions and workflow

The recurring workflow was to inspect relevant existing files before editing; keep each task narrowly scoped; preserve working behavior; avoid unnecessary context scans, unrelated features, and broad refactoring; use existing project sources and avoid invented facts; and report changed files, checks, and remaining limitations. The developer remained responsible for reviewing diffs and performing manual checks. Prompts are summarized here rather than reconstructed as verbatim transcripts.

## Concrete errors and corrections

- An initial Vercel configuration used `entrypoint = "app.main"`. Vercel's build error required a `module:object` value; the entrypoint was corrected to `app.main:app`, matching the exported FastAPI application.
- An earlier deployment attempt reported `ModuleNotFoundError: No module named 'dotenv'`.
- A later deployment attempt reported `ModuleNotFoundError: No module named 'resend'`.
- The later dependency audit found `python-dotenv` already present in the checked `requirements.txt` and `pyproject.toml`, while `resend` was missing. The audit aligned runtime dependencies across both manifests and classified `pytest` and `httpx` as development/test dependencies. The earlier `dotenv` error does not prove that `python-dotenv` was absent from those later manifests; its precise cause in that earlier deployment was not established.

## Review and verification

### Automated checks reported

The dependency-audit work reported these checks:

- Runtime dependency entries in `requirements.txt` and `pyproject.toml` were compared; TOML parsing succeeded, and installed local package versions were checked against the declared ranges.
- `uv pip check` reported the installed environment's packages compatible.
- `pytest -q tests/test_funnel_measurement.py tests/test_lead_flow.py` reported **19 passed**. These focused tests use isolated SQLite and injected/stub email senders.
- The focused test run emitted a Starlette deprecation warning for the current `httpx` TestClient integration and a pytest cache write warning caused by filesystem permissions.

`tests/test_resend.py` was inspected but not run because it can send a real email. The focused tests do not verify real Resend delivery, every production database behavior, all deployment scenarios, or the entire application.

### Manual inspection and outstanding verification

The project history includes review of Vercel build-error logs supplied during troubleshooting and inspection of code/configuration changes. Those logs documented failed build attempts, not a successful deployment. No successful final Vercel deployment or live request test is established by the available evidence. A local environment-value check was reported during troubleshooting, but no secret value is recorded here.

Developer manual review of the final diff, browser behavior, production email, production PostgreSQL, and deployed site remains necessary where applicable. Do not infer these checks from the automated test result.

## Remaining limitations

AI did not independently verify live email delivery, durable analytics, unique-visitor measurement, or controlled A/B assignment. It did not establish whether Czech retail investors can access each fund through a particular broker, whether a suitable PRIIPs KID is available, or whether the privacy notice, lawful basis, retention/deletion process, provider terms, and sender-domain/DNS setup have passed legal or operational review. Fund facts retain the source dates and caveats in [the research record](../docs/etf-research.md) and require rechecking before publication. Application behavior and test reports should be independently reviewed by the developer.
