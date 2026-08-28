# LinkedIn-Post - Deutsch

Ich habe PrimeOrder Commerce Intelligence entwickelt, um eine einfache, aber schwer belastbar zu beantwortende Frage zu lösen: Was passiert tatsächlich über Commerce, Akquisition, Produkte, SEO, Kunden und Measurement hinweg?

Entstanden ist ein datenschutzorientiertes Portfolio-System für ein saudisches Digitalprodukte-Umfeld. Es verbindet reproduzierbare synthetische Daten, sechs typisierte Read-only-Connectoren - darunter ein ausschließlich lesender PrimeOrder/Salla-MCP-Adapter - mit DuckDB/dbt, FastAPI und einem responsiven Next.js-Dashboard mit neun Bereichen in Englisch und Arabisch/RTL.

Die wichtigste Architekturentscheidung: Nicht jede Kennzahl wird künstlich in eine einzige „Source of Truth“ gezwungen. Commerce verantwortet abgeschlossene Bestellungen und Umsatz. GA4 verantwortet Sessions, Funnel-Verhalten und getrackte Käufe. Google Ads, Search Console, Merchant Center und Clarity behalten ihren jeweiligen Diagnosebereich. Abweichungen, Aktualität, Consent-Abdeckung und Event-Vollständigkeit bleiben sichtbar.

Die Evidenz: 28 dbt-Modelle, 78 Datentests, 117 erfolgreiche dbt-Knoten, 26 Python-Tests, 10 Frontend-Unit-Tests, 17 Browser-/Accessibility-Prüfungen, ein Static-Hosting-Test und acht datenschutzgeprüfte Screenshots. Lighthouse Desktop: 85/100/100/100. Die mobile Performance ist offen als Einschränkung dokumentiert.

Es werden keine echten Kunden- oder Umsatzdaten veröffentlicht und kein kommerzieller Uplift behauptet. Gezeigt wird die technische und analytische Grundlage, um Verbesserungen verantwortungsvoll zu messen.

Live-Demo und Quellcode stehen im ersten Kommentar.

#AnalyticsEngineering #EcommerceAnalytics #GA4 #dbt #Nextjs
