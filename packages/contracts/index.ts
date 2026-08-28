export type ConnectorStatus =
  | "CONNECTED"
  | "READY_NOT_AUTHENTICATED"
  | "FIXTURE_MODE"
  | "FILE_MODE"
  | "UNAVAILABLE"
  | "FAILED_WITH_EVIDENCE";

export interface Period { start: string; end: string; days: number }
export interface TimeSeriesPoint { date: string; sessions: number; tracked_purchases: number; completed_orders: number; net_revenue_sar: number }
export interface SummaryTotals {
  sessions: number; active_user_days: number; product_views: number; add_to_carts: number;
  begin_checkouts: number; tracked_purchases: number; completed_orders: number; units_sold: number;
  gross_revenue_sar: number; discount_sar: number; refund_sar: number;
  net_revenue_sar: number; cost_sar: number; ad_spend_sar: number;
  average_order_value_sar: number; purchase_conversion_rate: number;
  refund_rate: number; gross_margin_sar: number;
}
export interface SummaryResponse {
  disclosure: string; currency: "SAR"; period: Period;
  totals: SummaryTotals; timeseries: TimeSeriesPoint[];
}
export interface FunnelStep {
  step: string; count: number; step_conversion_rate: number;
  overall_conversion_rate: number; abandonment_rate: number;
}
export interface FunnelResponse { disclosure: string; steps: FunnelStep[] }
export interface ProductPerformance {
  product_id: string; product_name_en: string; product_name_ar: string;
  category: string; brand: string; units_sold: number; revenue_sar: number;
  gross_margin_sar: number;
}
export interface AcquisitionPerformance {
  channel: string; source: string; medium: string; campaign: string;
  sessions: number; active_user_days: number; tracked_purchases: number; purchase_revenue_sar: number;
  ad_spend_sar: number; conversion_rate: number; roas: number | null;
}
export interface SearchPerformance {
  query: string; page: string; is_branded: boolean; clicks: number;
  impressions: number; ctr: number; average_position: number;
}
export interface CustomerSegment {
  customer_type: "new" | "returning"; customers: number; completed_orders: number;
  net_revenue_sar: number; revenue_share: number;
}
export interface QualityCheck {
  check_id: string; status: "pass" | "warning" | "fail"; severity: string;
  metric_value: number; threshold: number; affected_rows: number;
}
export interface Insight {
  insight_id: string; priority: number; area: string; title: string;
  evidence: string; confidence: string; recommended_action: string;
}
export interface ConnectorSummary {
  id: string; display_name: string; status: ConnectorStatus;
  live_status: ConnectorStatus; read_only: true; fallback_formats: string[];
  fixture_fresh_through: string; schema_validation: "enabled";
  source_timezone: "Asia/Riyadh"; report_range: { start: string; end: string };
  currency: "SAR"; evidence_ref: string; max_retries: number;
  retry_policy: { on: string[]; backoff_seconds: number[] }; payloads_persisted: false;
}
