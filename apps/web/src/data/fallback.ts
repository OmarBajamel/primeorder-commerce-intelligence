import type { DashboardData, PerformanceRecord } from "@/lib/types";

const products = [
  { id: "office-pro", name: { en: "Office Pro License", ar: "ترخيص أوفيس برو" }, category: "software", categoryName: { en: "Software", ar: "البرامج" }, price: 319 },
  { id: "design-suite", name: { en: "Design Suite Annual", ar: "حزمة التصميم السنوية" }, category: "subscriptions", categoryName: { en: "Subscriptions", ar: "الاشتراكات" }, price: 259 },
  { id: "security-plus", name: { en: "Security Plus", ar: "الحماية بلس" }, category: "security", categoryName: { en: "Security", ar: "الأمان" }, price: 189 },
  { id: "cloud-storage", name: { en: "Cloud Storage 1 TB", ar: "تخزين سحابي 1 تيرابايت" }, category: "subscriptions", categoryName: { en: "Subscriptions", ar: "الاشتراكات" }, price: 149 },
  { id: "windows-key", name: { en: "Windows Digital Key", ar: "مفتاح ويندوز رقمي" }, category: "software", categoryName: { en: "Software", ar: "البرامج" }, price: 229 },
  { id: "gaming-pass", name: { en: "Gaming Pass 12M", ar: "بطاقة ألعاب 12 شهرًا" }, category: "gaming", categoryName: { en: "Gaming", ar: "الألعاب" }, price: 219 },
  { id: "vpn-premium", name: { en: "VPN Premium", ar: "في بي إن بريميوم" }, category: "security", categoryName: { en: "Security", ar: "الأمان" }, price: 129 },
  { id: "learning-pack", name: { en: "Learning Platform Pack", ar: "حزمة منصة تعليمية" }, category: "subscriptions", categoryName: { en: "Subscriptions", ar: "الاشتراكات" }, price: 179 },
] as const;

const channels = ["Organic Search", "Paid Search", "Direct", "Email", "Social", "Referral"];
const devices = ["Mobile", "Desktop", "Tablet"];
const dates = ["2025-07-06", "2025-07-13", "2025-07-20", "2025-07-27", "2025-08-03", "2025-08-10", "2025-08-17", "2025-08-24", "2025-08-31", "2025-09-07", "2025-09-14", "2025-09-21", "2025-09-28", "2025-10-05", "2025-10-12", "2025-10-19", "2025-10-26", "2025-11-02", "2025-11-09", "2025-11-16", "2025-11-23", "2025-11-30", "2025-12-07", "2025-12-14", "2025-12-21", "2025-12-28"];

const records: PerformanceRecord[] = dates.flatMap((date, week) =>
  products.map((product, index) => {
    const seasonality = 0.88 + week * 0.025 + (week > 7 ? 0.08 : 0);
    const sessions = Math.round((150 + index * 24 + ((week * 19 + index * 7) % 61)) * seasonality);
    const viewItem = Math.round(sessions * (0.57 + (index % 3) * 0.035));
    const addToCart = Math.round(viewItem * (0.24 - (index % 2) * 0.025));
    const beginCheckout = Math.round(addToCart * (0.63 - (index % 3) * 0.025));
    const orders = Math.max(1, Math.round(beginCheckout * (0.68 - (index % 4) * 0.028)));
    return {
      date, product: product.id, category: product.category,
      channel: channels[(week + index * 2) % channels.length],
      device: devices[(week * 2 + index) % devices.length],
      sessions, activeUserDays: Math.round(sessions * 0.81), viewItem, addToCart, beginCheckout, trackedPurchases: orders, orders,
      units: orders + ((week + index) % 5 === 0 ? Math.ceil(orders * 0.12) : 0),
      revenue: orders * product.price,
      refunds: (week + index) % 7 === 0 ? Math.round(orders * product.price * 0.08) : 0,
    };
  }),
);

export const fallbackData: DashboardData = {
  schemaVersion: "1.0",
  meta: { dataMode: "public-demo", generatedAt: "2026-01-05T08:00:00Z", periodStart: dates[13], periodEnd: dates.at(-1)!, currency: "SAR", locale: "en-SA", seed: 20250301 },
  catalog: { products: products.map((product) => ({ id: product.id, name: product.name, category: product.category, categoryName: product.categoryName })), channels, devices },
  records,
  seo: {
    queries: [
      { query: { en: "office license saudi", ar: "ترخيص أوفيس السعودية" }, type: "Non-branded", clicks: 1284, impressions: 21350, ctr: 6.01, position: 7.2 },
      { query: { en: "primeorder", ar: "برايم أوردر" }, type: "Branded", clicks: 932, impressions: 3020, ctr: 30.86, position: 1.6 },
      { query: { en: "digital software key", ar: "مفتاح برنامج رقمي" }, type: "Non-branded", clicks: 684, impressions: 15980, ctr: 4.28, position: 10.4 },
      { query: { en: "vpn subscription ksa", ar: "اشتراك في بي إن السعودية" }, type: "Non-branded", clicks: 512, impressions: 9820, ctr: 5.21, position: 8.7 },
      { query: { en: "cloud storage offer", ar: "عرض تخزين سحابي" }, type: "Non-branded", clicks: 391, impressions: 11380, ctr: 3.44, position: 12.1 },
      { query: { en: "gaming pass 12 months", ar: "بطاقة ألعاب 12 شهر" }, type: "Non-branded", clicks: 348, impressions: 7720, ctr: 4.51, position: 9.8 },
    ],
    landingPages: [
      { page: "/products/office-pro", clicks: 1450, impressions: 24170, ctr: 6.0 },
      { page: "/collections/subscriptions", clicks: 1022, impressions: 18720, ctr: 5.46 },
      { page: "/products/security-plus", clicks: 734, impressions: 15430, ctr: 4.76 },
      { page: "/collections/gaming", clicks: 612, impressions: 12840, ctr: 4.77 },
    ],
    merchantDiagnostics: [
      { issue: { en: "Missing optional product identifier", ar: "معرّف منتج اختياري مفقود" }, affectedItemSnapshots: 3, severity: "Medium", status: "Open" },
      { issue: { en: "Image crawl pending", ar: "انتظار زحف الصور" }, affectedItemSnapshots: 2, severity: "Low", status: "Monitoring" },
      { issue: { en: "Price mismatch", ar: "عدم تطابق السعر" }, affectedItemSnapshots: 0, severity: "High", status: "Clear" },
    ],
  },
  customers: {
    segments: [
      { segment: { en: "New customers", ar: "عملاء جدد" }, customers: 1138, orders: 1184, revenue: 266120, share: 66.2 },
      { segment: { en: "Returning customers", ar: "عملاء عائدون" }, customers: 438, orders: 606, revenue: 135940, share: 33.8 },
    ],
    cohorts: [
      { cohort: "Sep 2025", month0: 100, month1: 24.8, month2: 16.2, month3: 11.4 },
      { cohort: "Oct 2025", month0: 100, month1: 22.1, month2: 14.7, month3: 0 },
      { cohort: "Nov 2025", month0: 100, month1: 20.6, month2: 0, month3: 0 },
      { cohort: "Dec 2025", month0: 100, month1: 0, month2: 0, month3: 0 },
    ],
    valueDistribution: [
      { band: "< 150 SAR", customers: 486 }, { band: "150–299 SAR", customers: 672 }, { band: "300–599 SAR", customers: 321 }, { band: "600+ SAR", customers: 97 },
    ],
  },
  quality: {
    healthScore: 84,
    consentStateCoverage: 91.4,
    connectors: [
      { id: "salla", name: "PrimeOrder / Salla", status: "FIXTURE_MODE", freshness: "2026-01-05T07:45:00Z", records: 9075 },
      { id: "ga4", name: "Google Analytics 4", status: "FIXTURE_MODE", freshness: "2026-01-05T06:30:00Z", records: 43720 },
      { id: "gsc", name: "Search Console", status: "FIXTURE_MODE", freshness: "2026-01-03T12:00:00Z", records: 1260 },
      { id: "merchant", name: "Merchant Center", status: "FIXTURE_MODE", freshness: "2026-01-05T05:00:00Z", records: 48 },
      { id: "clarity", name: "Microsoft Clarity", status: "FIXTURE_MODE", freshness: "2026-01-04T23:00:00Z", records: 9340 },
      { id: "ads", name: "Google Ads", status: "READY_NOT_AUTHENTICATED", freshness: "N/A", records: 0 },
    ],
    rules: [
      { id: "unique-transactions", name: { en: "Unique transaction IDs", ar: "معرّفات معاملات فريدة" }, status: "warning", severity: "high", evidence: { en: "One duplicate tracking transaction ID across 9,075 synthetic orders.", ar: "معرّف معاملة تتبع مكرر واحد ضمن 9,075 طلبًا اصطناعيًا." }, remediation: { en: "Deduplicate on transaction_id before reporting and inspect tag firing.", ar: "إزالة التكرار حسب transaction_id وفحص تشغيل الوسم." } },
      { id: "item-params", name: { en: "Item parameter completeness", ar: "اكتمال معلمات المنتج" }, status: "warning", severity: "medium", evidence: { en: "item_category is absent on 3.2% of add_to_cart events.", ar: "فئة المنتج مفقودة في 3.2٪ من أحداث الإضافة للسلة." }, remediation: { en: "Map the catalog category into the GA4 items array.", ar: "ربط فئة الكتالوج بمصفوفة المنتجات في GA4." } },
      { id: "unknown-products", name: { en: "Known product references", ar: "مراجع المنتجات المعروفة" }, status: "fail", severity: "high", evidence: { en: "7 synthetic events reference an unmapped item_id.", ar: "7 أحداث اصطناعية تشير إلى item_id غير مربوط." }, remediation: { en: "Quarantine unknown IDs and add catalog relationship tests.", ar: "عزل المعرّفات غير المعروفة وإضافة اختبارات علاقات الكتالوج." } },
      { id: "consent", name: { en: "Consent-state coverage", ar: "تغطية حالة الموافقة" }, status: "warning", severity: "medium", evidence: { en: "Consent state is observable for 91.4% of measured sessions.", ar: "حالة الموافقة قابلة للرصد في 91.4٪ من الجلسات المقاسة." }, remediation: { en: "Validate default and update commands in EEA test journeys.", ar: "التحقق من أوامر الموافقة الافتراضية والتحديث في مسارات المنطقة الاقتصادية الأوروبية." } },
      { id: "search-freshness", name: { en: "Search Console freshness", ar: "حداثة بيانات Search Console" }, status: "warning", severity: "medium", evidence: { en: "The fixture intentionally stops 11 days before commerce data.", ar: "تتوقف البيانات التجريبية عمدًا قبل بيانات التجارة بـ11 يومًا." }, remediation: { en: "Block stale SEO comparisons and surface the source watermark.", ar: "حظر مقارنات البحث القديمة وإظهار علامة حداثة المصدر." } },
      { id: "tracking-variance", name: { en: "Purchase-source reconciliation", ar: "مطابقة مصادر الشراء" }, status: "warning", severity: "medium", evidence: { en: "GA4 is intentionally under-reported during a five-day window.", ar: "تم خفض تقارير GA4 عمدًا خلال نافذة خمسة أيام." }, remediation: { en: "Compare server orders with analytics transaction IDs by date.", ar: "مقارنة طلبات الخادم بمعرّفات معاملات التحليلات حسب التاريخ." } },
      { id: "non-negative", name: { en: "Non-negative commerce measures", ar: "مقاييس تجارية غير سالبة" }, status: "pass", severity: "low", evidence: { en: "All published aggregate measures pass.", ar: "كل المقاييس التجميعية المنشورة اجتازت الاختبار." }, remediation: { en: "Continue enforcing warehouse constraints.", ar: "الاستمرار في فرض قيود مستودع البيانات." } },
    ],
    reconciliation: { sallaOrders: 9075, ga4Orders: 8914, orderVariance: -1.77, sallaRevenue: 2066686, ga4Revenue: 2025418, revenueVariance: -2.0 },
  },
  insights: [
    { id: "mobile-checkout", category: "Mobile UX", finding: { en: "Mobile checkout loses more intent", ar: "تسرب نية الشراء أعلى في الهاتف" }, evidence: { en: "Mobile begin_checkout → purchase trails desktop by 8.4 points.", ar: "تحويل بدء الدفع إلى الشراء على الهاتف أقل من سطح المكتب بـ 8.4 نقاط." }, kpi: { en: "Checkout completion", ar: "إكمال الدفع" }, action: { en: "Audit mobile payment and form friction.", ar: "تدقيق احتكاك الدفع والنموذج على الهاتف." }, direction: { en: "Reduce checkout abandonment", ar: "خفض تسرب الدفع" }, confidence: "High", effort: "M", priority: 92, owner: { en: "CRO lead", ar: "مسؤول تحسين التحويل" }, experiment: { en: "Run a device-split checkout usability study before A/B testing.", ar: "إجراء دراسة استخدام للدفع حسب الجهاز قبل اختبار A/B." }, status: "Ready" },
    { id: "transaction-dedupe", category: "Measurement repair", finding: { en: "Duplicate purchase events distort reporting", ar: "أحداث شراء مكررة تشوه التقارير" }, evidence: { en: "4 duplicate transaction IDs are present in the audit fixture.", ar: "يوجد 4 معرّفات معاملات مكررة في بيانات التدقيق." }, kpi: { en: "Orders and revenue", ar: "الطلبات والإيرادات" }, action: { en: "Add tag-fire guard and warehouse deduplication.", ar: "إضافة حماية تشغيل الوسم وإزالة التكرار في المستودع." }, direction: { en: "Improve measurement accuracy", ar: "رفع دقة القياس" }, confidence: "High", effort: "S", priority: 89, owner: { en: "Analytics engineer", ar: "مهندس التحليلات" }, experiment: { en: "Replay the purchase flow in debug mode and compare transaction IDs.", ar: "إعادة مسار الشراء في وضع التصحيح ومقارنة المعرّفات." }, status: "Ready" },
    { id: "nonbrand-content", category: "SEO", finding: { en: "Non-branded demand has page-one potential", ar: "فرصة للطلبات غير المرتبطة بالعلامة في الصفحة الأولى" }, evidence: { en: "Two high-impression queries rank between positions 8 and 13.", ar: "عبارتان عاليتا الظهور ترتبان بين المركزين 8 و13." }, kpi: { en: "Organic clicks", ar: "النقرات العضوية" }, action: { en: "Strengthen category copy and internal links around license intent.", ar: "تعزيز محتوى الفئة والروابط الداخلية حول نية الترخيص." }, direction: { en: "Increase qualified organic visibility", ar: "زيادة الظهور العضوي المؤهل" }, confidence: "Medium", effort: "M", priority: 81, owner: { en: "SEO manager", ar: "مدير تحسين البحث" }, experiment: { en: "Publish the update and compare 28-day query cohorts.", ar: "نشر التحديث ومقارنة مجموعات البحث خلال 28 يومًا." }, status: "Planned" },
    { id: "category-param", category: "Reporting governance", finding: { en: "Category analysis has a small tracking gap", ar: "فجوة تتبع صغيرة في تحليل الفئات" }, evidence: { en: "3.2% of add_to_cart events lack item_category.", ar: "3.2٪ من أحداث الإضافة للسلة تفتقد فئة المنتج." }, kpi: { en: "Category funnel", ar: "مسار الفئة" }, action: { en: "Standardize items-array mapping in GTM.", ar: "توحيد ربط مصفوفة المنتجات في GTM." }, direction: { en: "Improve category attribution", ar: "تحسين إسناد الفئة" }, confidence: "High", effort: "S", priority: 78, owner: { en: "Analytics specialist", ar: "أخصائي التحليلات" }, experiment: { en: "Validate 20 test events across product templates.", ar: "التحقق من 20 حدثًا تجريبيًا عبر قوالب المنتجات." }, status: "Ready" },
    { id: "portfolio", category: "Product merchandising", finding: { en: "Revenue is concentrated in two offers", ar: "الإيرادات مركزة في عرضين" }, evidence: { en: "The leading two products represent more than one third of filtered revenue.", ar: "يمثل المنتجان الرائدان أكثر من ثلث الإيرادات المصفاة." }, kpi: { en: "Revenue concentration", ar: "تركيز الإيرادات" }, action: { en: "Test contextual cross-sells for long-tail offers.", ar: "اختبار البيع المتقاطع السياقي للعروض طويلة الذيل." }, direction: { en: "Diversify product contribution", ar: "تنويع مساهمة المنتجات" }, confidence: "Medium", effort: "M", priority: 70, owner: { en: "E-commerce manager", ar: "مدير التجارة الإلكترونية" }, experiment: { en: "Compare attach rate for one eligible product pair.", ar: "مقارنة معدل الإرفاق لزوج منتجات مؤهل." }, status: "Planned" },
  ],
};
