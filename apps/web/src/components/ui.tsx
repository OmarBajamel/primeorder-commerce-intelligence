"use client";

import { AlertTriangle, CircleHelp, DatabaseZap, RefreshCw } from "lucide-react";
import type { ReactNode } from "react";
import { initialFilters } from "@/lib/data";
import { useDashboard } from "./dashboard-provider";

export const formatNumber = (value: number, locale = "en") => new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-GB", { maximumFractionDigits: 0 }).format(value);
export const formatCurrency = (value: number, locale = "en") => new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-SA", { style: "currency", currency: "SAR", maximumFractionDigits: 0 }).format(value);
export const formatPercent = (value: number, locale = "en") => new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-GB", { style: "percent", maximumFractionDigits: 1 }).format(value / 100);

export function Tooltip({ text }: { text: string }) {
  return (
    <span className="tooltip-wrap">
      <button className="tooltip-trigger" type="button" aria-label={text}><CircleHelp size={14} aria-hidden="true" /></button>
      <span className="tooltip-content" role="tooltip">{text}</span>
    </span>
  );
}

export function KpiCard({ label, value, change, formula, tone = "default" }: { label: string; value: string; change?: string; formula: string; tone?: "default" | "teal" | "sand" }) {
  return (
    <article className={`kpi-card kpi-${tone}`}>
      <div className="kpi-label"><span>{label}</span><Tooltip text={formula} /></div>
      <strong className="kpi-value">{value}</strong>
      {change && <span className="kpi-change">{change}</span>}
    </article>
  );
}

export function SectionCard({ title, action, children, className = "" }: { title: string; action?: ReactNode; children: ReactNode; className?: string }) {
  return <section className={`panel ${className}`}><header className="panel-header"><h2>{title}</h2>{action}</header>{children}</section>;
}

export function StatusChip({ status }: { status: string }) {
  const normalized = status.toLowerCase();
  const tone = normalized.includes("pass") || normalized.includes("connected") || normalized.includes("clear") ? "success" :
    normalized.includes("fail") || normalized.includes("unavailable") ? "danger" : "warning";
  return <span className={`status-chip status-${tone}`}>{status.replaceAll("_", " ")}</span>;
}

export function LoadingState() {
  const { t } = useDashboard();
  return <div className="state-card" role="status"><span className="loader" aria-hidden="true" /><strong>{t("loading")}</strong><div className="skeleton-row" /><div className="skeleton-row short" /></div>;
}

export function EmptyState() {
  const { t, data, setFilters } = useDashboard();
  return <div className="state-card"><DatabaseZap size={32} aria-hidden="true" /><strong>{t("noData")}</strong><p>{t("noDataHint")}</p><button className="button secondary" onClick={() => data && setFilters(initialFilters(data))}>{t("reset")}</button></div>;
}

export function ErrorState() {
  const { t, reload } = useDashboard();
  return <div className="state-card" role="alert"><AlertTriangle size={32} aria-hidden="true" /><strong>Dashboard data is unavailable</strong><p>The static data file is invalid and no safe fallback could be initialized.</p><button className="button secondary" onClick={reload}><RefreshCw size={15} />{t("retry")}</button></div>;
}

export function Notice({ children, tone = "info" }: { children: ReactNode; tone?: "info" | "warning" }) {
  return <div className={`notice notice-${tone}`}><AlertTriangle size={17} aria-hidden="true" /><span>{children}</span></div>;
}
