"use client";

import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip as ChartTooltip, XAxis, YAxis } from "recharts";
import { useDashboard } from "./dashboard-provider";
import { formatCurrency, formatNumber } from "./ui";

export interface ChartDatum { name: string; revenue?: number; orders?: number; value?: number; sessions?: number }

export function TrendChart({ data, label }: { data: ChartDatum[]; label: string }) {
  const { locale, t } = useDashboard();
  return <figure className="chart"><div className="chart-canvas" role="img" aria-label={label}>
    <ResponsiveContainer width="100%" height="100%"><LineChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
      <CartesianGrid stroke="#dfe6e5" vertical={false} /><XAxis dataKey="name" tick={{ fontSize: 11, fill: "#60706f" }} tickLine={false} axisLine={false} />
      <YAxis yAxisId="revenue" tick={{ fontSize: 11, fill: "#60706f" }} tickFormatter={(v) => `${Math.round(v / 1000)}k`} tickLine={false} axisLine={false} />
      <YAxis yAxisId="orders" orientation="right" tick={{ fontSize: 11, fill: "#60706f" }} tickLine={false} axisLine={false} />
      <ChartTooltip formatter={(value, name) => name === "revenue" ? formatCurrency(Number(value), locale) : formatNumber(Number(value), locale)} />
      <Legend /><Line yAxisId="revenue" type="monotone" dataKey="revenue" stroke="#087f76" strokeWidth={3} dot={false} />
      <Line yAxisId="orders" type="monotone" dataKey="orders" stroke="#d39a46" strokeWidth={2} dot={false} />
    </LineChart></ResponsiveContainer></div>
    <details className="chart-data"><summary>{t("accessibleData")}</summary><table><thead><tr><th scope="col">Date</th><th scope="col">{t("revenue")}</th><th scope="col">{t("orders")}</th></tr></thead><tbody>{data.map((row) => <tr key={row.name}><th scope="row">{row.name}</th><td>{formatCurrency(row.revenue ?? 0, locale)}</td><td>{formatNumber(row.orders ?? 0, locale)}</td></tr>)}</tbody></table></details>
  </figure>;
}

export function ComparisonChart({ data, label, dataKey = "revenue" }: { data: ChartDatum[]; label: string; dataKey?: "revenue" | "orders" | "sessions" | "value" }) {
  const { locale, t } = useDashboard();
  return <figure className="chart"><div className="chart-canvas compact" role="img" aria-label={label}>
    <ResponsiveContainer width="100%" height="100%"><BarChart data={data} layout="vertical" margin={{ top: 0, right: 16, left: 12, bottom: 0 }}>
      <CartesianGrid stroke="#e5e9e8" horizontal={false} /><XAxis type="number" hide /><YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 11, fill: "#344443" }} tickLine={false} axisLine={false} />
      <ChartTooltip formatter={(value) => dataKey === "revenue" ? formatCurrency(Number(value), locale) : formatNumber(Number(value), locale)} />
      <Bar dataKey={dataKey} fill="#087f76" radius={[0, 5, 5, 0]} />
    </BarChart></ResponsiveContainer></div>
    <details className="chart-data"><summary>{t("accessibleData")}</summary><table><thead><tr><th scope="col">Name</th><th scope="col">Value</th></tr></thead><tbody>{data.map((row) => <tr key={row.name}><th scope="row">{row.name}</th><td>{dataKey === "revenue" ? formatCurrency(row[dataKey] ?? 0, locale) : formatNumber(row[dataKey] ?? 0, locale)}</td></tr>)}</tbody></table></details>
  </figure>;
}

export function FunnelBars({ stages }: { stages: Array<{ name: string; value: number; rate: number }> }) {
  const { locale } = useDashboard();
  const max = stages[0]?.value || 1;
  return <div className="funnel-bars">{stages.map((stage, index) => <div className="funnel-stage" key={stage.name}>
    <div className="funnel-meta"><span><b>{String(index + 1).padStart(2, "0")}</b>{stage.name}</span><strong>{formatNumber(stage.value, locale)}</strong></div>
    <div className="funnel-track"><span style={{ width: `${Math.max(4, stage.value / max * 100)}%` }} /></div><small>{stage.rate.toFixed(1)}% step conversion</small>
  </div>)}</div>;
}
