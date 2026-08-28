import { describe, expect, it } from "vitest";
import { fallbackData } from "@/data/fallback";
import generatedDashboard from "../../public/data/dashboard.json";
import { filterRecords, initialFilters, normalizeDashboardData, recordsToCsv, sum } from "./data";

describe("public dashboard data", () => {
  it("accepts the generated v1 contract and reconciles canonical order totals", () => {
    const result = normalizeDashboardData(generatedDashboard);
    expect(result.meta.seed).toBe(20250301);
    expect(result.records.length).toBeGreaterThanOrEqual(365 * 3 * 12);
    expect(sum(result.records, "orders")).toBe(9075);
    expect(sum(result.records, "sessions")).toBeGreaterThan(sum(result.records, "trackedPurchases"));
    expect(new Set(result.records.map((row) => [row.date, row.device, row.channel, row.product].join("|"))).size).toBe(result.records.length);
  });

  it("rejects a live-private payload and retains the safe public fallback", () => {
    const result = normalizeDashboardData({ meta: { dataMode: "live-private" }, records: [{ revenue: 999_999 }] });
    expect(result.meta.dataMode).toBe("public-demo");
    expect(result.meta.seed).toBe(20250301);
    expect(result.records).toEqual(fallbackData.records);
  });

  it("applies date, device, channel, category, and product filters together", () => {
    const target = fallbackData.records.find((row) => row.date >= fallbackData.meta.periodStart)!;
    const filters = { ...initialFilters(fallbackData), startDate: target.date, endDate: target.date, device: target.device, channel: target.channel, category: target.category, product: target.product };
    const rows = filterRecords(fallbackData.records, filters);
    expect(rows.length).toBeGreaterThan(0);
    expect(rows.every((row) => row.date === target.date && row.device === target.device && row.product === target.product)).toBe(true);
    expect(sum(rows, "revenue")).toBeGreaterThan(0);
  });

  it("exports only the filtered public fields to CSV", () => {
    const csv = recordsToCsv(fallbackData.records.slice(0, 1));
    expect(csv.split("\n")).toHaveLength(2);
    expect(csv).toContain("date,device,channel,category,product");
    expect(csv).not.toMatch(/email|phone|customer_id/i);
  });
});
