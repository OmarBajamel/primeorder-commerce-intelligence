"use client";

import { ArrowRight, CheckCircle2, CircleAlert, Gauge, Info, Sparkles, Target } from "lucide-react";
import { useMemo, useState } from "react";
import { filterRecords, groupRecords, sum } from "@/lib/data";
import { localize } from "@/lib/i18n";
import type { PerformanceRecord } from "@/lib/types";
import { useDashboard } from "./dashboard-provider";
import { ComparisonChart, FunnelBars, TrendChart } from "./charts";
import { EmptyState, ErrorState, formatCurrency, formatNumber, formatPercent, KpiCard, LoadingState, Notice, SectionCard, StatusChip } from "./ui";

export type DashboardRoute = "overview" | "funnel" | "products" | "acquisition" | "seo" | "customers" | "quality" | "insights" | "methodology";

const formula = {
  revenue: "SUM(completed order revenue) − SUM(refunded value)", orders: "COUNT(DISTINCT completed transaction_id)",
  conversion: "Completed orders ÷ sessions", aov: "Net revenue ÷ completed orders", refund: "Refunded value ÷ gross revenue",
};

function useMetrics() {
  const { data, filteredRecords: records, filters } = useDashboard();
  return useMemo(() => {
    const gross = sum(records, "revenue"), refunds = sum(records, "refunds"), orders = sum(records, "orders"), sessions = sum(records, "sessions");
    let previous: PerformanceRecord[] = [];
    if (data && filters.compare) {
      const start = new Date(`${filters.startDate}T00:00:00Z`), end = new Date(`${filters.endDate}T00:00:00Z`);
      const duration = end.getTime() - start.getTime() + 86_400_000;
      const previousEnd = new Date(start.getTime() - 86_400_000), previousStart = new Date(previousEnd.getTime() - duration + 86_400_000);
      previous = filterRecords(data.records, { ...filters, startDate: previousStart.toISOString().slice(0, 10), endDate: previousEnd.toISOString().slice(0, 10) });
    }
    const previousGross = sum(previous, "revenue") - sum(previous, "refunds"), previousOrders = sum(previous, "orders"), previousSessions = sum(previous, "sessions");
    const pct = (current: number, prior: number) => prior ? ((current - prior) / prior) * 100 : null;
    const net = gross - refunds, conversion = sessions ? orders / sessions * 100 : 0, aov = orders ? net / orders : 0;
    return { records, gross, net, refunds, orders, sessions, users: sum(records, "users"), units: sum(records, "units"), conversion, aov,
      refundRate: gross ? refunds / gross * 100 : 0,
      changes: { revenue: pct(net, previousGross), orders: pct(orders, previousOrders), conversion: pct(conversion, previousSessions ? previousOrders / previousSessions * 100 : 0) } };
  }, [data, filters, records]);
}

function changeLabel(value: number | null, locale: "en" | "ar", suffix: string) {
  if (value === null) return locale === "ar" ? "لا توجد فترة سابقة" : "No prior-period baseline";
  return `${value >= 0 ? "+" : ""}${value.toFixed(1)}% ${suffix}`;
}

function PageIntro({ title, description, eyebrow }: { title: string; description: string; eyebrow: string }) {
  return <header className="page-intro"><div><span className="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{description}</p></div><span className="trust-pill"><CheckCircle2 size={15} />Public-demo evidence</span></header>;
}

function Overview() {
  const { data, locale, t } = useDashboard(); const m = useMetrics(); if (!data) return null;
  const productNames = new Map(data.catalog.products.map((p) => [p.id, localize(p.name, locale)]));
  const categoryNames = new Map(data.catalog.products.map((p) => [p.category, localize(p.categoryName, locale)]));
  const trends = groupRecords(m.records, "date").map((row) => ({ name: row.name.slice(5), revenue: row.revenue - row.refunds, orders: row.orders }));
  const channels = groupRecords(m.records, "channel").sort((a, b) => b.revenue - a.revenue).map((row) => ({ name: row.name, revenue: row.revenue - row.refunds }));
  const devices = groupRecords(m.records, "device").sort((a, b) => b.revenue - a.revenue).map((row) => ({ name: row.name, revenue: row.revenue - row.refunds }));
  const products = groupRecords(m.records, "product").sort((a, b) => b.revenue - a.revenue);
  const categories = groupRecords(m.records, "category").sort((a, b) => b.revenue - a.revenue);
  return <><PageIntro eyebrow="DECISION SNAPSHOT" title={t("overview")} description={locale === "ar" ? "قراءة موحدة للأداء التجاري وموثوقية القياس والفرص التالية." : "A unified view of commercial performance, measurement trust and the next best actions."} />
    <div className="kpi-grid"><KpiCard label={t("revenue")} value={formatCurrency(m.net, locale)} change={changeLabel(m.changes.revenue, locale, t("vsPrevious"))} formula={formula.revenue} tone="teal" /><KpiCard label={t("orders")} value={formatNumber(m.orders, locale)} change={changeLabel(m.changes.orders, locale, t("vsPrevious"))} formula={formula.orders} /><KpiCard label={t("conversion")} value={formatPercent(m.conversion, locale)} change={changeLabel(m.changes.conversion, locale, t("vsPrevious"))} formula={formula.conversion} tone="sand" /><KpiCard label={t("aov")} value={formatCurrency(m.aov, locale)} formula={formula.aov} /><KpiCard label={t("refundRate")} value={formatPercent(m.refundRate, locale)} formula={formula.refund} /></div>
    <div className="grid wide-left"><SectionCard title={t("revenueTrend")}><TrendChart data={trends} label="Weekly net revenue and completed orders" /></SectionCard><SectionCard title={t("health")}><div className="score-wrap"><div className="score-ring" style={{ "--score": `${data.quality.healthScore * 3.6}deg` } as React.CSSProperties}><strong>{data.quality.healthScore}</strong><span>/ 100</span></div><div><StatusChip status="MONITOR" /><p>{locale === "ar" ? "قاعدتان تحتاجان إلى الإصلاح قبل اتخاذ قرارات دقيقة." : "Two rules need remediation before precision decisions."}</p><a href="quality/">{t("viewDetails")} <ArrowRight size={14} /></a></div></div></SectionCard></div>
    <div className="grid thirds"><SectionCard title={t("channelMix")}><ComparisonChart data={channels} label="Revenue by acquisition channel" /></SectionCard><SectionCard title={t("deviceMix")}><ComparisonChart data={devices} label="Revenue by device" /></SectionCard><SectionCard title={t("connectors")}><div className="status-list">{data.quality.connectors.slice(0, 5).map((item) => <div key={item.id}><span><b>{item.name}</b><small>{item.freshness === "N/A" ? "N/A" : new Date(item.freshness).toLocaleDateString()}</small></span><StatusChip status={item.status} /></div>)}</div></SectionCard></div>
    <div className="grid halves"><SectionCard title={t("topProducts")}><RankedList rows={products.slice(0, 5).map((row) => ({ name: productNames.get(row.name) ?? row.name, value: row.revenue - row.refunds }))} total={m.net} locale={locale} /></SectionCard><SectionCard title={t("topCategories")}><RankedList rows={categories.map((row) => ({ name: categoryNames.get(row.name) ?? row.name, value: row.revenue - row.refunds }))} total={m.net} locale={locale} /></SectionCard></div>
    <SectionCard title={t("opportunities")}><div className="insight-strip">{data.insights.slice(0, 3).map((item) => <article key={item.id}><span className="priority">P{item.priority}</span><div><small>{item.category}</small><h3>{localize(item.finding, locale)}</h3><p>{localize(item.evidence, locale)}</p></div><ArrowRight size={18} /></article>)}</div></SectionCard></>;
}

function RankedList({ rows, total, locale }: { rows: Array<{ name: string; value: number }>; total: number; locale: "en" | "ar" }) {
  return <ol className="rank-list">{rows.map((row, index) => <li key={row.name}><span className="rank">{index + 1}</span><div><span><b>{row.name}</b><strong>{formatCurrency(row.value, locale)}</strong></span><span className="mini-track"><i style={{ width: `${total ? row.value / total * 100 : 0}%` }} /></span></div></li>)}</ol>;
}

function Funnel() {
  const { locale, t } = useDashboard(); const m = useMetrics();
  const values = [m.sessions, sum(m.records, "viewItem"), sum(m.records, "addToCart"), sum(m.records, "beginCheckout"), m.orders];
  const names = [t("sessions"), "view_item", "add_to_cart", "begin_checkout", "purchase"];
  const stages = names.map((name, index) => ({ name, value: values[index], rate: index === 0 ? 100 : values[index - 1] ? values[index] / values[index - 1] * 100 : 0 }));
  const devices = groupRecords(m.records, "device").map((row) => ({ name: row.name, value: row.sessions ? row.orders / row.sessions * 100 : 0 }));
  const channels = groupRecords(m.records, "channel").map((row) => ({ name: row.name, value: row.sessions ? row.orders / row.sessions * 100 : 0 })).sort((a, b) => b.value - a.value);
  return <><PageIntro eyebrow="BEHAVIOR FLOW" title={t("funnelTitle")} description={t("funnelDesc")} /><div className="kpi-grid compact-kpis"><KpiCard label={t("sessions")} value={formatNumber(m.sessions, locale)} formula="COUNT(DISTINCT session_id)" /><KpiCard label="view_item" value={formatNumber(values[1], locale)} formula="Sessions containing ≥1 view_item event" /><KpiCard label="purchase" value={formatNumber(m.orders, locale)} formula={formula.orders} tone="teal" /><KpiCard label={t("conversion")} value={formatPercent(m.conversion, locale)} formula={formula.conversion} /></div>
    <div className="grid wide-left"><SectionCard title={t("funnelTitle")}><FunnelBars stages={stages} /></SectionCard><SectionCard title={t("comparison")}><ComparisonChart data={devices} dataKey="value" label="Conversion rate by device" /><div className="divider" /><ComparisonChart data={channels.slice(0, 4)} dataKey="value" label="Conversion rate by channel" /></SectionCard></div>
    <SectionCard title="Accessible funnel data"><div className="table-wrap"><table><thead><tr><th scope="col">{t("stage")}</th><th scope="col">{t("reached")}</th><th scope="col">{t("stepRate")}</th><th scope="col">{t("abandonment")}</th></tr></thead><tbody>{stages.map((stage, i) => <tr key={stage.name}><th scope="row"><code>{stage.name}</code></th><td>{formatNumber(stage.value, locale)}</td><td>{formatPercent(stage.rate, locale)}</td><td>{i ? formatPercent(100 - stage.rate, locale) : "—"}</td></tr>)}</tbody></table></div></SectionCard>
    <Notice>{locale === "ar" ? "المقام قائم على الجلسة: كل مرحلة تحسب الجلسات التي بلغت الحدث مرة واحدة على الأقل. لذلك لا يؤدي تكرار الأحداث إلى تضخيم التحويل." : "Session-based denominator: every stage counts sessions reaching the event at least once, so repeated events do not inflate conversion."}</Notice></>;
}

function Products() {
  const { data, locale, t } = useDashboard(); const m = useMetrics(); const [search, setSearch] = useState(""); const [sort, setSort] = useState("revenue"); if (!data) return null;
  const lookup = new Map(data.catalog.products.map((p) => [p.id, p]));
  const rows = groupRecords(m.records, "product").map((row) => ({ ...row, net: row.revenue - row.refunds, refundRate: row.revenue ? row.refunds / row.revenue * 100 : 0, conversion: row.sessions ? row.orders / row.sessions * 100 : 0 }))
    .filter((row) => localize(lookup.get(row.name)?.name ?? { en: row.name, ar: row.name }, locale).toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => sort === "orders" ? b.orders - a.orders : sort === "conversion" ? b.conversion - a.conversion : b.net - a.net);
  const categories = groupRecords(m.records, "category").map((row) => ({ name: localize(lookup.get(rows.find((p) => lookup.get(p.name)?.category === row.name)?.name ?? "")?.categoryName ?? { en: row.name, ar: row.name }, locale), revenue: row.revenue - row.refunds }));
  return <><PageIntro eyebrow="MERCHANDISING" title={t("productsTitle")} description={locale === "ar" ? "حدد المنتجات التي تدفع الطلب وأين يتركز الاعتماد التجاري." : "Identify the offers driving demand and where commercial reliance is concentrated."} />
    <div className="kpi-grid compact-kpis"><KpiCard label={t("revenue")} value={formatCurrency(m.net, locale)} formula={formula.revenue} tone="teal" /><KpiCard label={t("units")} value={formatNumber(m.units, locale)} formula="SUM(item_quantity) on completed orders" /><KpiCard label={t("orders")} value={formatNumber(m.orders, locale)} formula={formula.orders} /><KpiCard label={t("refundRate")} value={formatPercent(m.refundRate, locale)} formula={formula.refund} /></div>
    <SectionCard title={t("productsTitle")} action={<div className="table-tools"><label><span className="sr-only">{t("searchProducts")}</span><input type="search" placeholder={t("searchProducts")} value={search} onChange={(e) => setSearch(e.target.value)} /></label><label><span className="sr-only">{t("sortBy")}</span><select aria-label={t("sortBy")} value={sort} onChange={(e) => setSort(e.target.value)}><option value="revenue">{t("revenue")}</option><option value="orders">{t("orders")}</option><option value="conversion">{t("conversion")}</option></select></label></div>}><div className="table-wrap"><table><thead><tr><th scope="col">{t("productName")}</th><th scope="col">{t("revenue")}</th><th scope="col">{t("share")}</th><th scope="col">{t("units")}</th><th scope="col">{t("orders")}</th><th scope="col">{t("conversion")}</th><th scope="col">{t("refund")}</th></tr></thead><tbody>{rows.map((row) => <tr key={row.name}><th scope="row"><b>{localize(lookup.get(row.name)?.name ?? { en: row.name, ar: row.name }, locale)}</b><small>{localize(lookup.get(row.name)?.categoryName ?? { en: row.name, ar: row.name }, locale)}</small></th><td>{formatCurrency(row.net, locale)}</td><td>{formatPercent(m.net ? row.net / m.net * 100 : 0, locale)}</td><td>{formatNumber(row.units, locale)}</td><td>{formatNumber(row.orders, locale)}</td><td>{formatPercent(row.conversion, locale)}</td><td>{formatPercent(row.refundRate, locale)}</td></tr>)}</tbody></table>{!rows.length && <div className="table-empty">{t("noData")}</div>}</div></SectionCard>
    <div className="grid halves"><SectionCard title={t("concentration")}><ComparisonChart data={rows.slice(0, 6).map((r) => ({ name: localize(lookup.get(r.name)?.name ?? { en: r.name, ar: r.name }, locale), revenue: r.net }))} label="Net revenue by product" /></SectionCard><SectionCard title={t("topCategories")}><ComparisonChart data={categories} label="Net revenue by category" /></SectionCard></div><Notice>{t("marginUnavailable")}</Notice></>;
}

function Acquisition() {
  const { data, locale, t } = useDashboard(); const m = useMetrics(); if (!data) return null;
  const channels = groupRecords(m.records, "channel").map((row) => ({ ...row, net: row.revenue - row.refunds, conversion: row.sessions ? row.orders / row.sessions * 100 : 0 })).sort((a, b) => b.net - a.net);
  return <><PageIntro eyebrow="DEMAND SOURCES" title={t("acquisitionTitle")} description={locale === "ar" ? "قارن جودة الجلسات والقيمة التجارية عبر القنوات دون مبالغة في الإسناد." : "Compare session quality and commercial value across channels without overstating attribution."} />
    <SectionCard title={t("sourceMedium")}><div className="table-wrap"><table><thead><tr><th scope="col">{t("channel")}</th><th scope="col">{t("sessions")}</th><th scope="col">{t("users")}</th><th scope="col">{t("orders")}</th><th scope="col">{t("revenue")}</th><th scope="col">{t("conversion")}</th></tr></thead><tbody>{channels.map((row) => <tr key={row.name}><th scope="row"><b>{row.name}</b><small>{row.name.toLowerCase().replace(" ", "_")} / attributed</small></th><td>{formatNumber(row.sessions, locale)}</td><td>{formatNumber(row.users, locale)}</td><td>{formatNumber(row.orders, locale)}</td><td>{formatCurrency(row.net, locale)}</td><td>{formatPercent(row.conversion, locale)}</td></tr>)}</tbody></table></div></SectionCard>
    <div className="grid halves"><SectionCard title="Channel revenue"><ComparisonChart data={channels.map((r) => ({ name: r.name, revenue: r.net }))} label="Net revenue by acquisition channel" /></SectionCard><SectionCard title={t("landingPages")}><div className="compact-list">{data.seo.landingPages.map((row) => <div key={row.page}><code>{row.page}</code><span><b>{formatNumber(row.orders, locale)} {t("orders")}</b><small>{formatCurrency(row.revenue, locale)}</small></span></div>)}</div></SectionCard></div><Notice>{t("spendUnavailable")}</Notice><Notice>{t("attributionCaveat")}</Notice></>;
}

function Seo() {
  const { data, locale, t } = useDashboard(); if (!data) return null; const totals = data.seo.queries.reduce((a, r) => ({ clicks: a.clicks + r.clicks, impressions: a.impressions + r.impressions }), { clicks: 0, impressions: 0 });
  return <><PageIntro eyebrow="ORGANIC DISCOVERY" title={t("seoTitle")} description={locale === "ar" ? "اجمع طلب البحث مع جودة الكتالوج لتحديد فرص قابلة للتحقق." : "Connect search demand with catalog health to surface verifiable opportunities."} /><div className="kpi-grid compact-kpis"><KpiCard label={t("clicks")} value={formatNumber(totals.clicks, locale)} formula="SUM(Search Console clicks)" tone="teal" /><KpiCard label={t("impressions")} value={formatNumber(totals.impressions, locale)} formula="SUM(Search Console impressions)" /><KpiCard label={t("ctr")} value={formatPercent(totals.impressions ? totals.clicks / totals.impressions * 100 : 0, locale)} formula="Clicks ÷ impressions" /><KpiCard label={t("position")} value={(data.seo.queries.reduce((n, q) => n + q.position * q.impressions, 0) / totals.impressions).toFixed(1)} formula="Impression-weighted average position" /></div>
    <SectionCard title={t("query")}><div className="table-wrap"><table><thead><tr><th scope="col">{t("query")}</th><th scope="col">{t("queryType")}</th><th scope="col">{t("clicks")}</th><th scope="col">{t("impressions")}</th><th scope="col">{t("ctr")}</th><th scope="col">{t("position")}</th></tr></thead><tbody>{data.seo.queries.map((row) => <tr key={row.query.en}><th scope="row">{localize(row.query, locale)}</th><td><StatusChip status={row.type} /></td><td>{formatNumber(row.clicks, locale)}</td><td>{formatNumber(row.impressions, locale)}</td><td>{formatPercent(row.ctr, locale)}</td><td>{row.position.toFixed(1)}</td></tr>)}</tbody></table></div></SectionCard>
    <div className="grid halves"><SectionCard title={t("landingPages")}><div className="compact-list">{data.seo.landingPages.map((row) => <div key={row.page}><code>{row.page}</code><span><b>{formatNumber(row.clicks, locale)} {t("clicks")}</b><small>{formatNumber(row.orders, locale)} {t("orders")}</small></span></div>)}</div></SectionCard><SectionCard title={t("merchant")}><div className="status-list diagnostics">{data.seo.merchantDiagnostics.map((item) => <div key={item.issue.en}><span><b>{localize(item.issue, locale)}</b><small>{item.affected} {t("affected")}</small></span><StatusChip status={item.status} /></div>)}</div></SectionCard></div></>;
}

function Customers() {
  const { data, locale, t } = useDashboard(); if (!data) return null; const returning = data.customers.segments[1];
  return <><PageIntro eyebrow="PRIVACY-SAFE SEGMENTS" title={t("customersTitle")} description={t("privacyCaveat")} /><div className="kpi-grid compact-kpis">{data.customers.segments.map((row) => <KpiCard key={row.segment.en} label={localize(row.segment, locale)} value={formatNumber(row.customers, locale)} change={`${formatPercent(row.share, locale)} revenue share`} formula="Anonymous customers grouped by first completed order date" />)}<KpiCard label="Repeat-purchase indicator" value={formatPercent(returning.orders ? (returning.orders - returning.customers) / returning.customers * 100 : 0, locale)} formula="Orders after the first order ÷ returning customers" tone="teal" /></div>
    <div className="grid halves"><SectionCard title={t("retention")}><div className="table-wrap"><table><thead><tr><th scope="col">Cohort</th><th scope="col">M0</th><th scope="col">M1</th><th scope="col">M2</th><th scope="col">M3</th></tr></thead><tbody>{data.customers.cohorts.map((row) => <tr key={row.cohort}><th scope="row">{row.cohort}</th>{[row.month0, row.month1, row.month2, row.month3].map((v, i) => <td key={i}><span className="heat-cell" style={{ opacity: v ? Math.max(.2, v / 100) : .08 }}>{v ? formatPercent(v, locale) : "—"}</span></td>)}</tr>)}</tbody></table></div></SectionCard><SectionCard title={t("valueDistribution")}><ComparisonChart data={data.customers.valueDistribution.map((row) => ({ name: row.band, value: row.customers }))} dataKey="value" label="Anonymous customer count by lifetime value band" /></SectionCard></div><Notice>{t("privacyCaveat")}</Notice></>;
}

function Quality() {
  const { data, locale, filters, t } = useDashboard(); if (!data) return null; const connectors = data.quality.connectors.filter((item) => filters.connector === "all" || item.id === filters.connector); const r = data.quality.reconciliation;
  return <><PageIntro eyebrow="TRUST BEFORE ACTION" title={t("qualityTitle")} description={t("qualityDesc")} /><div className="kpi-grid compact-kpis"><KpiCard label={t("health")} value={`${data.quality.healthScore}/100`} formula="Weighted share of passing quality rules after severity adjustment" tone="teal" /><KpiCard label="Order variance" value={formatPercent(r.orderVariance, locale)} formula="(GA4 orders − Salla orders) ÷ Salla orders" /><KpiCard label="Revenue variance" value={formatPercent(r.revenueVariance, locale)} formula="(GA4 revenue − Salla revenue) ÷ Salla revenue" /><KpiCard label="Consent-state coverage" value="91.4%" formula="Sessions with observable analytics_storage consent state ÷ measured sessions" tone="sand" /></div>
    <div className="grid halves"><SectionCard title={t("connectors")}><div className="connector-grid">{connectors.map((item) => <article key={item.id}><div><span className="connector-icon">{item.name.slice(0, 2).toUpperCase()}</span><span><b>{item.name}</b><small>{item.records.toLocaleString()} records</small></span></div><StatusChip status={item.status} /><small>Freshness · {item.freshness === "N/A" ? "N/A" : new Date(item.freshness).toLocaleString()}</small></article>)}</div></SectionCard><SectionCard title={t("reconciliation")}><div className="reconcile"><div><span>Salla</span><strong>{formatNumber(r.sallaOrders, locale)}</strong><small>{formatCurrency(r.sallaRevenue, locale)}</small></div><div className="reconcile-gap"><ArrowRight /><b>{formatPercent(Math.abs(r.orderVariance), locale)}</b><small>order gap</small></div><div><span>GA4</span><strong>{formatNumber(r.ga4Orders, locale)}</strong><small>{formatCurrency(r.ga4Revenue, locale)}</small></div></div><Notice tone="warning">A variance is evidence to investigate, not proof that either source is wrong.</Notice></SectionCard></div>
    <SectionCard title="Validation rules"><div className="table-wrap"><table><thead><tr><th scope="col">{t("rule")}</th><th scope="col">{t("status")}</th><th scope="col">{t("severity")}</th><th scope="col">{t("evidence")}</th><th scope="col">{t("remediation")}</th></tr></thead><tbody>{data.quality.rules.map((rule) => <tr key={rule.id}><th scope="row">{localize(rule.name, locale)}</th><td><StatusChip status={rule.status} /></td><td>{rule.severity}</td><td>{localize(rule.evidence, locale)}</td><td>{localize(rule.remediation, locale)}</td></tr>)}</tbody></table></div></SectionCard></>;
}

function Insights() {
  const { data, locale, t } = useDashboard(); if (!data) return null;
  return <><PageIntro eyebrow="FROM SIGNAL TO EXPERIMENT" title={t("insightsTitle")} description={locale === "ar" ? "فرص مرتبة بقواعد واضحة وأدلة وخطوة تحقق قابلة للتنفيذ." : "Rule-ranked opportunities with explicit evidence and a testable next step."} /><div className="insight-grid">{data.insights.sort((a, b) => b.priority - a.priority).map((item) => <article className="insight-card" key={item.id}><header><span className="insight-category">{item.category}</span><span className="priority-score"><small>{t("priority")}</small>{item.priority}</span></header><h2>{localize(item.finding, locale)}</h2><p>{localize(item.evidence, locale)}</p><dl><div><dt>{t("action")}</dt><dd>{localize(item.action, locale)}</dd></div><div><dt>{t("direction")}</dt><dd>{localize(item.direction, locale)}</dd></div><div><dt>{t("experiment")}</dt><dd>{localize(item.experiment, locale)}</dd></div></dl><footer><span><b>{t("confidence")}</b> {item.confidence}</span><span><b>{t("effort")}</b> {item.effort}</span><span><b>{t("owner")}</b> {localize(item.owner, locale)}</span><StatusChip status={item.status} /></footer></article>)}</div><Notice>{locale === "ar" ? "تصف هذه البطاقات اتجاه الأثر المتوقع، ولا تدعي أي زيادة رقمية غير مقاسة." : "These cards state an expected direction of impact; they do not claim an unmeasured numerical uplift."}</Notice></>;
}

function Methodology() {
  const { data, locale, t } = useDashboard(); if (!data) return null;
  const cards = locale === "ar" ? [
    [t("sources"), "تعتمد الواجهة العامة على ملف JSON ثابت مُسبق الحساب. تمثل موصلات سلة وGA4 وSearch Console وMerchant وClarity بيانات تجريبية فقط."],
    [t("kpiMethod"), "تُحسب الإيرادات من الطلبات المكتملة بعد الاستردادات. التحويل هو الطلبات المكتملة مقسومة على الجلسات. لكل مؤشر تعريف ظاهر."],
    [t("generation"), `تُنشأ البيانات بصورة حتمية باستخدام البذرة ${data.meta.seed}. ولا تُشتق من أي مقاييس حقيقية لبرايم أوردر.`],
    [t("privacy"), "لا توجد أسماء أو بريد إلكتروني أو هواتف أو مراجع طلبات. طبقة العرض العام لا تتصل بواجهة خاصة أو مصدر تاجر."],
    [t("limitations"), "التكلفة والإنفاق الإعلامي والتدفقات المساعدة غير مكتملة، لذلك لا تُعرض هوامش أو ROAS أو استنتاجات سببية."],
    [t("claims"), "تحدد الفرص ما يجب اختباره. لا يدعي المشروع نمو الإيرادات أو التحويل ما لم تقسه تجربة صحيحة."],
  ] : [
    [t("sources"), "The public UI reads one precomputed static JSON file. Salla, GA4, Search Console, Merchant and Clarity connectors are represented in fixture mode only."],
    [t("kpiMethod"), "Revenue is completed-order value net of refunds. Conversion is completed orders divided by sessions. Every KPI exposes its formula at point of use."],
    [t("generation"), `Data is deterministic with fixed seed ${data.meta.seed}, realistic seasonality and documented quality defects. It is not derived from PrimeOrder metrics.`],
    [t("privacy"), "No names, emails, phone numbers or order references exist. The public presentation layer never calls a private API or merchant connector."],
    [t("limitations"), "Reliable cost, complete media spend and assisted journeys are absent, so margin, ROAS and causal conclusions are intentionally withheld."],
    [t("claims"), "Opportunities say what to test and the expected direction. This project never claims revenue or conversion growth without a valid measured experiment."],
  ];
  const icons = [<Info size={22} key="source" />, <Gauge size={22} key="kpi" />, <Sparkles size={22} key="generation" />, <CheckCircle2 size={22} key="privacy" />, <CircleAlert size={22} key="limits" />, <Target size={22} key="claims" />];
  return <><PageIntro eyebrow="EVIDENCE & LIMITS" title={t("methodologyTitle")} description={locale === "ar" ? "تعريفات وحدود ومصادر واضحة حتى يتمكن القارئ من الحكم على الأدلة." : "Clear definitions, boundaries and provenance so every reader can judge the evidence."} /><div className="method-hero"><div><span className="eyebrow">{t("transparent")}</span><h2>public-demo <span>≠</span> live-private</h2><p>{t("synthetic")}</p></div><div className="lineage"><span>Deterministic fixtures</span><ArrowRight /><span>Analytics marts</span><ArrowRight /><span>Static JSON</span><ArrowRight /><span>Dashboard</span></div></div><div className="method-grid">{cards.map(([title, body], index) => <article key={title}><span>{icons[index]}</span><h2>{title}</h2><p>{body}</p></article>)}</div><SectionCard title="Dashboard contract v1.0"><div className="contract"><code>public/data/dashboard.json</code><p>Required: <code>meta.dataMode = &quot;public-demo&quot;</code>. Typed records use date, device, channel, category, product, sessions, users, funnel events, orders, units, revenue and refunds. Invalid or absent optional sections are replaced by the deterministic safe fallback.</p></div></SectionCard></>;
}

export function DashboardView({ route }: { route: DashboardRoute }) {
  const { data, state, filteredRecords } = useDashboard();
  if (state === "loading") return <LoadingState />;
  if (state === "error" || !data) return <ErrorState />;
  if (!filteredRecords.length && !["seo", "customers", "quality", "insights", "methodology"].includes(route)) return <EmptyState />;
  const views = { overview: <Overview />, funnel: <Funnel />, products: <Products />, acquisition: <Acquisition />, seo: <Seo />, customers: <Customers />, quality: <Quality />, insights: <Insights />, methodology: <Methodology /> };
  return <div className="page-view">{views[route]}</div>;
}
