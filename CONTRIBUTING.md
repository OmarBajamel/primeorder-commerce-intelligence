# Contributing

Thank you for helping improve PrimeOrder Commerce Intelligence. Contributions must preserve its central promise: a reproducible public portfolio demo with no real customer, revenue, credential or merchant-confidential data.

## Before opening a change

- Read [`AGENTS.md`](AGENTS.md), the [architecture](docs/architecture/ARCHITECTURE.md), [KPI catalog](docs/analytics/KPI_CATALOG.md), and [privacy design](docs/privacy/PRIVACY_DESIGN.md).
- Discuss material changes to KPI semantics, connector scopes, data mode, public hosting, consent, authentication or repository structure before implementation.
- Report security/privacy vulnerabilities privately under [`SECURITY.md`](SECURITY.md), not in a public issue.
- Never use live customer/admin actions, cart/checkout/order activity, mutation tools or wider vendor scopes as test setup.

## Development setup

From the repository root:

```powershell
pnpm bootstrap
pnpm data:generate
pnpm test:api
pnpm test:analytics
pnpm dev:web
```

See the [runbook](docs/operations/RUNBOOK.md) for Windows, Bash, Docker, API and cleanup details.

## Branch and commit practice

- Branch from the latest `main` and keep one coherent purpose per change.
- Use descriptive commits that explain the behavioral/data-contract change.
- Do not commit caches, local databases, generated dependency directories, credentials, `.env`, raw vendor output, live extracts or private evidence.
- Preserve unrelated work and generated artifact provenance.
- Do not rewrite shared history without coordinated maintainer approval.

## Data and privacy rules

- `public-demo` is the default and only allowed mode for tests, screenshots, CI, Pages and release assets.
- New fixtures must be independently synthetic, deterministic and documented. Do not perturb, rescale or imitate private values.
- Test anomalies must be intentionally synthetic and listed in dataset metadata.
- Store approved live aggregate exports only in ignored `data/private/` or `.private/` locations; never include them in issues, reviews or screenshots.
- Do not log headers, tokens, payloads, customer/order IDs, exact live metrics or raw connector errors.
- A connector remains read-only and reports its exact mode/capability/status; no silent fixture fallback.

## Code and model standards

- TypeScript/React: accessible semantic components, EN/AR support, RTL and responsive behavior, no public private-API request.
- Python: type/Pydantic validation, structured safe errors/logging, bounded inputs/retries and parameterized queries.
- SQL/dbt: one declared grain per model, explicit source precedence, null-safe ratios, relationship/business tests, no many-to-many fact joins.
- Measurement: follow the versioned GA4 event/value contract; do not deploy tracking changes as part of a documentation/demo change.
- Documentation: separate implemented/verified capability from recommendations and do not claim unmeasured commercial impact.

## Verification

Run the narrowest relevant checks while editing and the complete repository gate before proposing release:

```powershell
pnpm lint
pnpm typecheck
pnpm test:unit
pnpm test:api
pnpm test:analytics
pnpm build
pnpm test:e2e
pnpm test:a11y
pnpm release:check
```

The full `pnpm test` also regenerates data. Release checks can legitimately fail before the final screenshot manifest/artifacts exist. Fix defects; do not reduce thresholds, skip checks or rewrite expected outputs simply to obtain green status.

For a KPI or schema change, update together:

- source/generator and normalized contract;
- dbt staging/intermediate/mart logic and tests;
- Python/TypeScript response contracts;
- static API fixtures and UI labels/tooltips;
- data dictionary, KPI catalog and machine-readable definition;
- case study/evidence where claims changed.

## Pull request checklist

- [ ] Scope and business/technical rationale are explained.
- [ ] Public/private boundary is unchanged or the approved design change is documented.
- [ ] No secret, PII, private metric, raw response or unauthorized binary is included.
- [ ] Fixture changes are deterministic, independently synthetic and documented.
- [ ] Model grains/formulas/source precedence and migrations are clear.
- [ ] EN/AR, RTL, responsive and accessibility impact is tested when relevant.
- [ ] Relevant tests/builds passed with exact command evidence.
- [ ] Documentation and screenshots match the final behavior.
- [ ] No unsupported revenue, conversion, SEO, saving or uplift claim was added.

## Review and release

Maintainers may request a focused architecture, analytics, security/privacy, UX/accessibility or documentation review. Critical/high release findings must be resolved before publication. See the [public release checklist](docs/security/PUBLIC_RELEASE_CHECKLIST.md).

By contributing, you agree that your contribution is licensed under this repository's [MIT License](LICENSE) and that you will follow the [Code of Conduct](CODE_OF_CONDUCT.md).

