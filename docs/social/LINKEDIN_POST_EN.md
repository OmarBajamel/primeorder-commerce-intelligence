# LinkedIn post - English

I built PrimeOrder Commerce Intelligence to answer a question that is easy to ask and surprisingly hard to defend: what is actually happening across commerce, acquisition, product, SEO, customer, and measurement data?

The result is a privacy-separated portfolio system for a Saudi digital-products context. It combines deterministic synthetic data, six typed read-only connector paths - including a read-only PrimeOrder/Salla MCP adapter - with DuckDB/dbt, FastAPI, and a responsive Next.js dashboard with nine routes in English and Arabic/RTL.

The key design choice was not to force every number into one “source of truth.” Commerce owns completed orders and revenue. GA4 owns sessions, funnel behavior, and tracked purchases. Google Ads, Search Console, Merchant Center, and Clarity retain their own diagnostic scopes. The dashboard exposes source variance, freshness, consent coverage, and event completeness so that uncertainty remains visible.

Verified evidence includes 28 dbt models, 78 data tests, 117 successful dbt nodes, 26 Python tests, 10 frontend unit tests, 17 browser/accessibility checks, a static-hosting check, and eight privacy-reviewed screenshots. The desktop Lighthouse result is 85/100/100/100; mobile performance remains an openly documented limitation.

No real PrimeOrder customer or revenue data is published, and I am not claiming commercial uplift. What this demonstrates is the engineering and analytical foundation needed to measure improvement responsibly.

Live demo and source are in the first comment.

#AnalyticsEngineering #EcommerceAnalytics #GA4 #dbt #Nextjs
