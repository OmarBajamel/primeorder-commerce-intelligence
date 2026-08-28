import { fallbackData } from "@/data/fallback";
import type { DashboardData, Filters, PerformanceRecord } from "./types";

export const assetUrl = (path: string) => `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}${path}`;

const isObject = (value: unknown): value is Record<string, unknown> => typeof value === "object" && value !== null;
const hasValidRecords = (value: unknown): value is PerformanceRecord[] => Array.isArray(value) && value.length > 0 && value.every((item) =>
  isObject(item) && typeof item.date === "string" && typeof item.product === "string" && typeof item.revenue === "number" && typeof item.orders === "number",
);

/**
 * Public dashboard contract v1.0. A generator may replace public/data/dashboard.json.
 * Invalid or missing optional sections are filled from the deterministic seed-20250301
 * fallback; live/private shapes are deliberately rejected by dataMode.
 */
export function normalizeDashboardData(value: unknown): DashboardData {
  if (!isObject(value) || !isObject(value.meta) || value.meta.dataMode !== "public-demo") return fallbackData;
  const candidate = value as Partial<DashboardData>;
  return {
    ...fallbackData,
    ...candidate,
    schemaVersion: "1.0",
    meta: { ...fallbackData.meta, ...(candidate.meta ?? {}), dataMode: "public-demo" },
    catalog: { ...fallbackData.catalog, ...(candidate.catalog ?? {}) },
    records: hasValidRecords(candidate.records) ? candidate.records : fallbackData.records,
    seo: { ...fallbackData.seo, ...(candidate.seo ?? {}) },
    customers: { ...fallbackData.customers, ...(candidate.customers ?? {}) },
    quality: { ...fallbackData.quality, ...(candidate.quality ?? {}) },
    insights: Array.isArray(candidate.insights) && candidate.insights.length ? candidate.insights : fallbackData.insights,
  };
}

export const initialFilters = (data: DashboardData = fallbackData): Filters => {
  const end = new Date(`${data.meta.periodEnd}T00:00:00Z`);
  const rollingStart = new Date(end.getTime() - 89 * 86_400_000).toISOString().slice(0, 10);
  return { startDate: rollingStart > data.meta.periodStart ? rollingStart : data.meta.periodStart, endDate: data.meta.periodEnd, device: "all", channel: "all", category: "all", product: "all", connector: "all", compare: true };
};

export function filterRecords(records: PerformanceRecord[], filters: Filters) {
  return records.filter((row) => row.date >= filters.startDate && row.date <= filters.endDate &&
    (filters.device === "all" || row.device === filters.device) &&
    (filters.channel === "all" || row.channel === filters.channel) &&
    (filters.category === "all" || row.category === filters.category) &&
    (filters.product === "all" || row.product === filters.product));
}

export const sum = (records: PerformanceRecord[], key: keyof Pick<PerformanceRecord, "sessions" | "users" | "viewItem" | "addToCart" | "beginCheckout" | "orders" | "units" | "revenue" | "refunds">) =>
  records.reduce((total, row) => total + row[key], 0);

export function groupRecords(records: PerformanceRecord[], key: keyof Pick<PerformanceRecord, "date" | "device" | "channel" | "category" | "product">) {
  const grouped = new Map<string, PerformanceRecord[]>();
  records.forEach((row) => grouped.set(row[key], [...(grouped.get(row[key]) ?? []), row]));
  return [...grouped].map(([name, rows]) => ({ name, rows, sessions: sum(rows, "sessions"), users: sum(rows, "users"), orders: sum(rows, "orders"), units: sum(rows, "units"), revenue: sum(rows, "revenue"), refunds: sum(rows, "refunds") }));
}

export function recordsToCsv(records: PerformanceRecord[]) {
  const keys: Array<keyof PerformanceRecord> = ["date", "device", "channel", "category", "product", "sessions", "users", "viewItem", "addToCart", "beginCheckout", "orders", "units", "revenue", "refunds"];
  return [keys.join(","), ...records.map((row) => keys.map((key) => JSON.stringify(row[key])).join(","))].join("\n");
}
