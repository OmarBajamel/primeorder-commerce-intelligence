# PrimeOrder Commerce Intelligence — Project Summary

## Compact English version

**PrimeOrder Commerce Intelligence** is a privacy-separated e-commerce analytics portfolio system for a Saudi digital-products business. It combines deterministic synthetic commerce data, six typed read-only connector paths, DuckDB/dbt modeling, a filtered FastAPI service and a nine-route English/Arabic Next.js dashboard.

Commerce owns completed-order and revenue definitions; GA4 owns sessions, funnel behavior and tracked purchases; Google Ads, Search Console, Merchant Center and Clarity retain their own diagnostic scopes. The system makes source variance, freshness, event completeness and consent coverage visible instead of hiding uncertainty.

Verified scope: 28 dbt models, 78 data tests and 117 successful dbt nodes; 26 Python tests; 10 frontend unit tests; 11 browser E2E checks; 6 accessibility checks; one static-export check; and eight privacy-reviewed screenshots. Lighthouse scores are 85/100/100/100 desktop and 46/100/100/100 mobile. Mobile performance is an open limitation.

The public application uses synthetic data only. All six public connector statuses are `FIXTURE_MODE`; no live authentication, deployment URL or measured commercial uplift is claimed.

## Kurzfassung auf Deutsch

**PrimeOrder Commerce Intelligence** ist ein datenschutzorientiertes E-Commerce-Analytics-Portfolio für ein saudisches Digitalprodukte-Geschäft. Die Lösung verbindet reproduzierbare synthetische Handelsdaten, sechs typisierte Read-only-Connectoren, DuckDB/dbt, eine gefilterte FastAPI und ein responsives Next.js-Dashboard mit neun Bereichen in Englisch und Arabisch/RTL.

Die Quellenverantwortung ist klar getrennt: Commerce liefert Bestellungen und Umsatz, GA4 liefert Sessions, Funnel und getrackte Käufe. Abweichungen, Aktualität, Event-Vollständigkeit und Consent-Abdeckung werden als Qualitätsbefunde sichtbar gemacht.

Verifizierter Umfang: 28 dbt-Modelle, 78 Datentests und 117 erfolgreiche dbt-Knoten; 26 Python-Tests; 10 Frontend-Unit-Tests; 11 E2E- und 6 Accessibility-Prüfungen; ein Test des statischen Exports; acht datenschutzgeprüfte Screenshots. Lighthouse: Desktop 85/100/100/100, Mobile 46/100/100/100. Die mobile Performance bleibt eine offen dokumentierte Einschränkung.

## 30-second interview pitch

I built an end-to-end commerce intelligence system that shows how I approach both the business question and the engineering evidence behind it. It covers commerce KPIs, GA4 funnel measurement, acquisition, SEO, product performance, customer segments and data quality. The public demo is reproducible and synthetic, while the live-private architecture is read-only and isolated. The strongest evidence is not a claimed uplift; it is the tested semantic layer, transparent source reconciliation and deployable bilingual dashboard.

## Evidence snapshot

| Area | Delivered evidence |
|---|---|
| Product | 9 dashboard routes; English and Arabic/RTL; responsive views; CSV export |
| Sources | 6 typed read-only connector paths; all public statuses `FIXTURE_MODE` |
| Analytics | 28 dbt models; 78 data tests; 11 seeds; 117 successful nodes |
| API/automation | FastAPI contracts, filters and safe errors; deterministic Python generator |
| Measurement | 11 GA4 e-commerce events plus parameter and consent coverage |
| Quality | 6 deliberate anomaly classes and Commerce/GA4 reconciliation |
| Automated tests | 26 Python; 10 frontend unit; 11 E2E; 6 accessibility; 1 static export |
| Visual proof | 8 privacy-reviewed screenshots |
| Lighthouse | Desktop 85/100/100/100; mobile 46/100/100/100 |
| Containers | Compose config passes; local runtime unverified because Docker engine was unavailable |

## Technology line

Next.js, React, TypeScript, Python, FastAPI, Pydantic, DuckDB, dbt, GA4/GTM measurement design, Playwright, axe-core, Docker Compose and GitHub Actions.

## Claims boundary

- The data is synthetic and not derived from real PrimeOrder customers or revenue.
- Connector implementation and fixture behavior are demonstrated; public live connectivity is not.
- Recommendations are hypotheses to test, not measured business results.
- Consent/privacy material is a portfolio engineering implementation, not legal advice.
- No repository, demo or release URL is included until independently verified.

