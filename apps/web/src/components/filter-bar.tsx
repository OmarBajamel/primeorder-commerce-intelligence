"use client";

import { Download, RotateCcw, SlidersHorizontal } from "lucide-react";
import { initialFilters, recordsToCsv } from "@/lib/data";
import { localize } from "@/lib/i18n";
import { useDashboard } from "./dashboard-provider";

export function FilterBar() {
  const { data, filteredRecords, filters, setFilters, locale, t } = useDashboard();
  if (!data) return null;
  const categories = [...new Map(data.catalog.products.map((p) => [p.category, p.categoryName])).entries()];
  const update = (key: keyof typeof filters, value: string | boolean) => setFilters((current) => ({ ...current, [key]: value }));
  const reset = () => setFilters(initialFilters(data));
  const exportCsv = () => {
    const url = URL.createObjectURL(new Blob([recordsToCsv(filteredRecords)], { type: "text/csv;charset=utf-8" }));
    const anchor = document.createElement("a"); anchor.href = url; anchor.download = "primeorder-public-demo-filtered.csv"; anchor.click(); URL.revokeObjectURL(url);
  };
  return <section className="filter-shell" aria-label={t("filters")}>
    <div className="filter-heading"><span><SlidersHorizontal size={16} aria-hidden="true" />{t("filters")}</span><button type="button" className="text-button" onClick={reset}><RotateCcw size={14} />{t("reset")}</button></div>
    <div className="filters-grid">
      <label><span>{t("startDate")}</span><input type="date" min={data.meta.periodStart} max={filters.endDate} value={filters.startDate} onChange={(e) => update("startDate", e.target.value)} /></label>
      <label><span>{t("endDate")}</span><input type="date" min={filters.startDate} max={data.meta.periodEnd} value={filters.endDate} onChange={(e) => update("endDate", e.target.value)} /></label>
      <label><span>{t("device")}</span><select value={filters.device} onChange={(e) => update("device", e.target.value)}><option value="all">{t("all")}</option>{data.catalog.devices.map((item) => <option key={item}>{item}</option>)}</select></label>
      <label><span>{t("channel")}</span><select value={filters.channel} onChange={(e) => update("channel", e.target.value)}><option value="all">{t("all")}</option>{data.catalog.channels.map((item) => <option key={item}>{item}</option>)}</select></label>
      <label><span>{t("category")}</span><select value={filters.category} onChange={(e) => update("category", e.target.value)}><option value="all">{t("all")}</option>{categories.map(([id, name]) => <option value={id} key={id}>{localize(name, locale)}</option>)}</select></label>
      <label><span>{t("product")}</span><select value={filters.product} onChange={(e) => update("product", e.target.value)}><option value="all">{t("all")}</option>{data.catalog.products.filter((item) => filters.category === "all" || item.category === filters.category).map((item) => <option value={item.id} key={item.id}>{localize(item.name, locale)}</option>)}</select></label>
      <label><span>{t("connector")}</span><select value={filters.connector} onChange={(e) => update("connector", e.target.value)}><option value="all">{t("all")}</option>{data.quality.connectors.map((item) => <option value={item.id} key={item.id}>{item.name}</option>)}</select></label>
      <div className="filter-actions"><label className="checkbox"><input type="checkbox" checked={filters.compare} onChange={(e) => update("compare", e.target.checked)} /><span>{t("compare")}</span></label><button type="button" className="button export-button" onClick={exportCsv} disabled={!filteredRecords.length}><Download size={15} />{t("exportCsv")}</button></div>
    </div>
  </section>;
}
