export type Locale = "en" | "ar";
export type LocalizedText = { en: string; ar: string };

export interface PerformanceRecord {
  date: string; device: string; channel: string; category: string; product: string;
  sessions: number; activeUserDays: number; viewItem: number; addToCart: number; beginCheckout: number;
  trackedPurchases: number; orders: number; units: number; revenue: number; refunds: number;
}

export interface ConnectorStatus {
  id: string; name: string;
  status: "FIXTURE_MODE" | "FILE_MODE" | "CONNECTED" | "READY_NOT_AUTHENTICATED" | "UNAVAILABLE" | "FAILED_WITH_EVIDENCE";
  freshness: string; records: number;
}

export interface QualityRule {
  id: string; name: LocalizedText; status: "pass" | "warning" | "fail"; severity: "low" | "medium" | "high";
  evidence: LocalizedText; remediation: LocalizedText;
}

export interface Insight {
  id: string; category: string; finding: LocalizedText; evidence: LocalizedText; kpi: LocalizedText; action: LocalizedText;
  direction: LocalizedText; confidence: "High" | "Medium" | "Low"; effort: "S" | "M" | "L"; priority: number;
  owner: LocalizedText; experiment: LocalizedText; status: "Ready" | "Planned" | "Monitoring";
}

export interface DashboardData {
  schemaVersion: "1.0";
  meta: { dataMode: "public-demo"; generatedAt: string; periodStart: string; periodEnd: string; currency: "SAR"; locale: "en-SA"; seed: number };
  catalog: {
    products: Array<{ id: string; name: LocalizedText; category: string; categoryName: LocalizedText }>;
    channels: string[]; devices: string[];
  };
  records: PerformanceRecord[];
  seo: {
    queries: Array<{ query: LocalizedText; type: "Branded" | "Non-branded"; clicks: number; impressions: number; ctr: number; position: number }>;
    landingPages: Array<{ page: string; clicks: number; impressions: number; ctr: number }>;
    merchantDiagnostics: Array<{ issue: LocalizedText; affectedItemSnapshots: number; severity: "Low" | "Medium" | "High"; status: string }>;
  };
  customers: {
    segments: Array<{ segment: LocalizedText; customers: number; orders: number; revenue: number; share: number }>;
    cohorts: Array<{ cohort: string; month0: number; month1: number; month2: number; month3: number }>;
    valueDistribution: Array<{ band: string; customers: number }>;
  };
  quality: {
    healthScore: number; consentStateCoverage: number; connectors: ConnectorStatus[]; rules: QualityRule[];
    reconciliation: { sallaOrders: number; ga4Orders: number; orderVariance: number; sallaRevenue: number; ga4Revenue: number; revenueVariance: number };
  };
  insights: Insight[];
}

export interface Filters {
  startDate: string; endDate: string; device: string; channel: string; category: string; product: string; connector: string; compare: boolean;
}
