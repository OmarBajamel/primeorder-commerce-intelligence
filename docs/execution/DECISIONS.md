# Decisions

## ADR-001 - Public static data and private local integration

GitHub Pages receives precomputed JSON from deterministic fixtures only. The local FastAPI service exposes the same contracts and may consume ignored, privacy-safe aggregate exports. This prevents public browser code from reaching private systems.

## ADR-002 - Next.js static export

Next.js App Router with static export supplies URL-addressable pages while retaining typed React components. Repository-aware base paths are applied in CI for GitHub Pages.

## ADR-003 - DuckDB and dbt

DuckDB keeps the analytics warehouse portable for reviewers; dbt provides tested staging, intermediate, and mart contracts with documented lineage.

## ADR-004 - Synthetic data is independent

The public generator uses a fixed seed and invented product/channel parameters. It never derives scale, distribution, or performance from PrimeOrder private metrics.

## ADR-005 - Honest unavailable metrics

Gross margin, CPA, and ROAS are shown only where synthetic fixtures contain explicitly reliable cost/spend fields. Live connectors report authentication or availability status rather than simulating connectivity.
