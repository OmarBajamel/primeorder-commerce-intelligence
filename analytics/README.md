# PrimeOrder analytics warehouse

The DuckDB/dbt project loads fixed-seed public fixtures and builds 9 staging
views, 4 intermediate views, and 12 decision-oriented marts. Commerce revenue
uses Salla-like synthetic orders as source priority; GA4-like data is used for
behavioral funnel comparison and reconciliation. Documented anomalies are
expected rows in `mart_data_quality`, while structural, date, relationship,
non-negative, tolerance, reconciliation, and business-invariant tests must pass.

Event parameter coverage uses `1` for a parameter that is present and valid when
applicable, or explicitly not applicable to that event (for example,
`transaction_id` on `view_item`). Values below `1` only represent incomplete
applicable records. Consent coverage is evaluated separately at daily/event grain.

Run `python scripts/generate_demo_data.py`, then
`python -m dbt build --project-dir analytics --profiles-dir analytics`.
