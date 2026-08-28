# PrimeOrder Commerce Intelligence v1.0.0

## Release summary

Version 1.0.0 is the first portfolio release of an evidence-first commerce measurement system for PrimeOrder’s Saudi digital-commerce context. It combines commercial KPIs, GA4 funnel behavior, product and acquisition analysis, SEO/Merchant reporting, privacy-safe customer segments, source reconciliation, and an evidence-linked action backlog.

**Live demo:** https://omarbajamel.github.io/primeorder-commerce-intelligence/  
**Repository:** https://github.com/OmarBajamel/primeorder-commerce-intelligence

## What ships

- Nine responsive Next.js routes with English and Arabic/RTL interfaces.
- Deterministic public-demo data covering 365 days, generated from seed `20250301` and independent of real merchant metrics.
- Six read-only connector contracts with fixture/file fallbacks and honest status reporting.
- FastAPI read-only analytics API and typed Pydantic contracts.
- DuckDB/dbt analytical reference warehouse: 11 staging, 5 intermediate, and 12 mart models.
- 11-event ecommerce measurement specification, consent-aware checks, six intentional anomaly detections, and daily source reconciliation.
- Public/private trust boundaries, secret/PII scans, screenshot provenance, CI, Pages deployment, and container smoke workflow.

## Verification snapshot

- Frontend unit: 10 passed.
- Python/API/connectors/generator: 26 passed.
- dbt: 117 PASS, 0 WARN, 0 ERROR.
- Browser/accessibility: 17 passed; static Pages direct navigation: 1 passed.
- Lighthouse desktop: performance 85, accessibility 100, best practices 100, SEO 100.
- Public release check: PASS after manual review of all eight screenshot assets.

## Privacy statement

All published values and visuals use synthetic portfolio data. No real customer data, private revenue, credentials, raw MCP responses, or merchant identifiers are included. Live-private paths are ignored and are not release inputs.

## Honest limitations

The release proves implemented measurement capability, not commercial uplift. All live connectors remain separately authenticated and read-only. Distinct period users, live margin, causal attribution, and measured CRO impact require governed source reports or experiments. Local Docker runtime verification was unavailable; the CI container build/smoke job is the release authority for that path.
