# PrimeOrder Commerce Intelligence – Management Summary

## Ausgangslage

PrimeOrder Commerce Intelligence ist ein eigenständiges Portfolio-Projekt für einen saudischen Online-Shop mit digitalen Produkten. Ziel war nicht, einen geschäftlichen Erfolg zu behaupten, sondern eine belastbare Entscheidungsgrundlage zu entwickeln: Handelsdaten, Verhaltenssignale, Akquisitionsdaten, SEO-Informationen und Datenqualitätsbefunde werden mit klarer Quellenverantwortung zusammengeführt.

Alle öffentlich sichtbaren Kennzahlen sind vollständig synthetisch. Sie wurden mit einem festen Seed für 365 Tage erzeugt und stammen nicht aus realen Kunden-, Bestell- oder Umsatzdaten von PrimeOrder. Eine gemessene Umsatz-, Conversion- oder SEO-Steigerung wird ausdrücklich nicht behauptet.

## Gelieferte Lösung

Die Lösung verbindet Business Intelligence und Software Engineering in einem reproduzierbaren System:

- neun recruiter-taugliche Dashboard-Bereiche für Managementübersicht, Funnel, Produkte, Akquisition, SEO und Merchant Center, Kundensegmente, Datenqualität, priorisierte Maßnahmen und Methodik;
- sechs typisierte, ausschließlich lesende Connector-Pfade für PrimeOrder/Salla MCP, GA4, Google Search Console, Google Merchant Center, Microsoft Clarity und Google Ads;
- ein portables Analytics-Warehouse mit DuckDB und dbt;
- eine gefilterte FastAPI-Schnittstelle mit strikten Pydantic-Verträgen;
- ein statisch exportierbares Next.js-Dashboard in Englisch und Arabisch einschließlich RTL-Darstellung;
- dokumentierte GA4-E-Commerce-Ereignisse, GTM-Implementierungsregeln sowie Consent- und Datenschutzhinweise für den EWR-/Deutschland-Kontext;
- ein festes `public-demo`-/`live-private`-Trennungsmodell, das private Händlerdaten vom öffentlichen Build ausschließt.

Der öffentliche Modus zeigt alle sechs Connectoren ehrlich als `FIXTURE_MODE`. Der Status beweist weder eine Live-Authentifizierung noch einen produktiven Abruf. Live-private Daten würden nur über autorisierte, lesende und lokal kontrollierte Pfade verarbeitet.

## Daten- und KPI-Governance

Die Kennzahlen folgen einer eindeutigen Quellenlogik: Commerce ist führend für abgeschlossene Bestellungen, Umsatz, Rabatte und Erstattungen; GA4 ist führend für Sessions, Funnel und getrackte Käufe; Google Ads liefert Werbekosten; Search Console liefert organische Suchsignale. Abweichungen zwischen Commerce und GA4 werden nicht gemittelt, sondern als Reconciliation-Befund ausgewiesen.

Die aktuelle dbt-Struktur umfasst 28 Modelle und 78 Datentests. Zusammen mit elf Seeds wurden 117 dbt-Knoten erfolgreich ausgeführt. Die Tests prüfen unter anderem Umsatzdefinitionen, Modellgrains, Beziehungen, Quellenabgleich, Event-Abdeckung, stabile Kundensegmentierung und sechs bewusst eingebaute Qualitätsanomalien.

## Verifikation

Für den aktuellen Stand liegen folgende lokale Ergebnisse vor:

| Prüfbereich | Ergebnis |
|---|---:|
| Python: Generator, Connectoren und API | 26 bestanden |
| dbt | 117/117 Knoten bestanden |
| Frontend-Unit-Tests | 10 bestanden |
| Browser-End-to-End | 11 bestanden |
| Accessibility | 6 bestanden |
| Statischer Export unter Repository-Basispfad | 1 bestanden |
| Privacy-geprüfte Screenshots | 8 |

Lighthouse erreichte im Desktop-Profil 85/100/100/100 und im Mobile-Profil 46/100/100/100 für Performance, Accessibility, Best Practices und SEO. Die mobile Performance ist damit eine offen dokumentierte Einschränkung, kein Erfolgssignal: Der Audit meldet rund 428 KiB Gesamttransfer, hohe Main-Thread-Arbeit, 4,46 Sekunden Total Blocking Time und Layout Shift. Die kompakte Dashboard-JSON-Datei ist weiterhin ein relevanter Payload-Anteil und ein konkreter Optimierungsansatz.

`docker compose config --quiet` ist erfolgreich. Ein lokaler Container-Build und Runtime-Smoke-Test konnten nicht ausgeführt werden, weil die Docker-Desktop-Linux-Engine nicht verfügbar war. Der CI-Workflow enthält dafür Compose-Build, Start, Health-/Web-Smoke-Test und Cleanup; dessen tatsächliche Ausführung darf erst nach einem erfolgreichen CI-Lauf behauptet werden.

## Nutzen für Arbeitgeber

Das Projekt zeigt die Verbindung aus E-Commerce-Verständnis, Analytics Engineering und sicherer Produktumsetzung. Es macht nicht nur Kennzahlen sichtbar, sondern dokumentiert Definitionen, Quellen, Datenqualität, Grenzen und nächste Experimente. Das ist besonders relevant für Rollen wie E-Commerce Manager, Digital Analytics Specialist, Technical E-Commerce Specialist, CRO/Growth Specialist und Product Data Analyst.

Die wichtigste Aussage lautet: Entscheidungen werden nachvollziehbar und überprüfbar gemacht. Geschäftlicher Impact bleibt eine Hypothese, bis ein sauber geplantes Experiment oder eine belastbare Vorher-Nachher-Messung ihn bestätigt.

## Grenzen

- Keine öffentliche Kennzahl stammt aus realen PrimeOrder-Daten.
- Kein Live-Connector ist im öffentlichen Artefakt authentifiziert.
- Die Consent-Dokumentation ist eine technische Portfolio-Implementierung, keine Rechtsberatung.
- Docker-Compose-Runtime und CI-Container-Smoke sind lokal nicht verifiziert.
- Die mobile Lighthouse-Performance muss vor einer belastbaren Performance-Aussage verbessert und erneut gemessen werden.

