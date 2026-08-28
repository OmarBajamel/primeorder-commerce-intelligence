# Interview STAR Stories

These are evidence-based first-person talking points for Omar Ba Jamel. Adapt the wording to the role; keep the limitations intact.

## 1. Building a public analytics product without exposing merchant data

**Situation:** I wanted to demonstrate real e-commerce analytics capability, but a public portfolio could not contain customer identifiers, merchant metrics, credentials or raw connector payloads.

**Task:** I needed an architecture that remained useful to recruiters while making public/private separation enforceable rather than relying on a disclaimer.

**Action:** I created a fixed-seed, 365-day synthetic dataset and made `public-demo` the only mode allowed in builds, tests, screenshots and release artifacts. I designed six read-only connector adapters with explicit statuses, schema validation and safe error envelopes. For Salla MCP, I used an injected executor, an operation allow-list and an aggregate-field projection; raw results are not serialized. I added release scanning for secrets, PII patterns, tracked private paths and archives.

**Result:** The repository now provides a reproducible public dashboard while all six public connectors report `FIXTURE_MODE`. The release checker reports `PASS` with no secret/PII or tracked-private-path finding, and eight captured screenshots have recorded privacy review `PASS`. This result proves the boundary controls and public artifact quality; it does not prove a live production integration.

**Likely follow-up:** Why not simply anonymize real data? Synthetic generation gives stronger public-release isolation and reproducibility. A live-private analysis could still use approved aggregates locally, but it would remain outside the public build.

## 2. Resolving KPI ambiguity across commerce and analytics sources

**Situation:** Commerce platforms and GA4 can report different purchase and revenue values because they use different status, attribution, consent and timing rules. Early review also found ambiguity around gross revenue, AOV, refunds and non-additive users.

**Task:** I needed one semantic layer that a manager could trust without pretending the sources were identical.

**Action:** I defined source precedence: Commerce owns completed orders and commercial revenue; GA4 owns sessions, funnel behavior and tracked purchases; Google Ads owns spend. Gross revenue is pre-discount and pre-refund, net revenue subtracts both, and AOV uses net revenue divided by completed orders. Refunds are allocated to items proportionally to after-discount value. GA4 users are labelled as additive active user-days when rolled up, not as distinct period users. I preserved Commerce-versus-GA4 values side by side with a 10% daily tolerance rather than averaging them.

**Result:** Executive, product, category, payment, acquisition and reconciliation outputs now follow the documented definitions. The final dbt run completed 117/117 nodes: 28 models, 78 tests and 11 seeds. Five deliberately injected reconciliation days are detected as warnings. The outcome is semantic consistency and observable disagreement, not a claim that either source improved.

**Likely follow-up:** Which number would you show management? I would use the commerce source for completed commercial orders/revenue, GA4 for behavioral conversion, and show the reconciliation gap with its scope and caveats.

## 3. Turning data-quality defects into demonstrable tests

**Situation:** A perfectly clean demo would show dashboard development, but not whether the analytics layer could detect realistic failures.

**Task:** I needed controlled defects that were visible, reproducible and prevented from being mistaken for real PrimeOrder findings.

**Action:** I injected six documented anomalies: one duplicate tracking transaction, one incomplete event-parameter group, an eleven-day Search Console freshness gap, one unmapped product, a five-day GA4 under-reporting window and one low-consent-coverage day. I modeled the checks in dbt and mirrored their evidence in the API/dashboard. Regression tests assert exact expected affected counts, event coverage and cross-runtime quality alignment.

**Result:** All six anomalies appear as warnings while structural tests remain green. The project therefore demonstrates detection and remediation thinking without fabricating a live business problem. The Python suite passed 26 tests and dbt passed all 117 nodes.

**Likely follow-up:** Why not make those tests fail? They are known fixture scenarios. Structural invariants must fail the build, while deliberately documented quality conditions remain visible warnings and are tested for exactness.

## 4. Shipping a recruiter-facing application with measurable quality

**Situation:** Technical work is hard to evaluate if it exists only as SQL or notebooks. Recruiters also need a fast, understandable and safe demonstration.

**Task:** I needed to make the analytics accessible across desktop/mobile and English/Arabic while preserving static-hosting and privacy constraints.

**Action:** I built nine Next.js routes, shared filters, CSV export, empty/error/loading states and Arabic RTL behavior. I generated compact static JSON for the public runtime, added direct-navigation testing under the repository base path, and captured a privacy-reviewed screenshot set. I tested routes, keyboard access and serious/critical axe violations.

**Result:** Ten frontend unit tests, eleven browser E2E checks, six accessibility checks and one static-export scenario passed. Eight screenshots cover desktop, mobile and RTL evidence. Lighthouse scored 85/100/100/100 on desktop and 46/100/100/100 on mobile. I present the mobile 46 as an open performance limitation: the audit reported about 428 KiB transfer, heavy main-thread work, 4.46 seconds blocking time and layout shift.

**Likely follow-up:** What would you optimize first? Reduce the client-side payload and JavaScript work, split route data, defer non-critical visualizations, stabilize layout dimensions, then rerun the same mobile profile before making a performance claim.

## 5. Designing container verification when the local engine is unavailable

**Situation:** The application includes Dockerfiles and Compose orchestration, but Docker Desktop’s Linux engine was unavailable in the local review environment.

**Task:** I had to distinguish what was actually verified from what was only designed.

**Action:** I validated the Compose model with `docker compose config --quiet`, documented the local engine failure, and kept the CI job that builds both services, starts the stack, polls API health and the web endpoint, captures logs on failure and tears down volumes.

**Result:** Compose configuration validation passed. Local image build/runtime remains unverified, and I do not describe the CI smoke as passed until a real workflow run provides that evidence. This demonstrates honest release reporting and a clear next verification step.

