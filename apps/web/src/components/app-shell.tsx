"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, BarChart3, Boxes, CircleGauge, Database, FileSearch, Languages, Lightbulb, Search, ShieldCheck, ShoppingCart, UsersRound } from "lucide-react";
import { type MessageKey } from "@/lib/i18n";
import { DashboardProvider, useDashboard } from "./dashboard-provider";
import { FilterBar } from "./filter-bar";

const navigation: Array<{ href: string; label: MessageKey; icon: typeof CircleGauge }> = [
  { href: "/", label: "overview", icon: CircleGauge }, { href: "/funnel", label: "funnel", icon: ShoppingCart },
  { href: "/products", label: "products", icon: Boxes }, { href: "/acquisition", label: "acquisition", icon: BarChart3 },
  { href: "/seo", label: "seo", icon: Search }, { href: "/customers", label: "customers", icon: UsersRound },
  { href: "/quality", label: "quality", icon: ShieldCheck }, { href: "/insights", label: "insights", icon: Lightbulb },
  { href: "/methodology", label: "methodology", icon: FileSearch },
];

function ShellContent({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { data, state, locale, setLocale, t } = useDashboard();
  const withoutBase = pathname.replace(process.env.NEXT_PUBLIC_BASE_PATH ?? "", "") || "/";
  const currentPath = withoutBase.length > 1 ? withoutBase.replace(/\/$/, "") : withoutBase;
  const current = navigation.find((item) => item.href === currentPath) ?? navigation[0];
  const filteredConnectors = data?.quality.connectors.filter((item) => item.status === "FIXTURE_MODE").length ?? 0;
  return <div className="app-shell">
    <aside className="sidebar">
      <Link href="/" className="brand" aria-label="PrimeOrder Intelligence home"><span className="brand-mark"><Activity size={20} aria-hidden="true" /></span><span><b>PRIMEORDER</b><small>COMMERCE INTELLIGENCE</small></span></Link>
      <nav className="nav-list" aria-label="Dashboard navigation">{navigation.map(({ href, label, icon: Icon }) => <Link href={href} key={href} aria-current={currentPath === href ? "page" : undefined} className={currentPath === href ? "active" : ""}><Icon size={17} aria-hidden="true" /><span>{t(label)}</span></Link>)}</nav>
      <div className="sidebar-status"><span className="pulse" aria-hidden="true" /><div><b>{t("dataStatus")}</b><small>{filteredConnectors} {t("fixture")}</small></div></div>
    </aside>
    <div className="workspace">
      <div className="disclosure" role="note"><span className="demo-badge"><Database size={13} aria-hidden="true" />{t("publicDemo")}</span><p>{t("synthetic")}</p></div>
      <header className="topbar"><div><span className="eyebrow">PRIMEORDER.SA · MEASUREMENT SYSTEM</span><h1>{t(current.label)}</h1></div><div className="topbar-actions">
        {data && <div className="freshness"><span className="pulse" /><div><small>{t("updated")}</small><b>{new Intl.DateTimeFormat(locale === "ar" ? "ar-SA" : "en-GB", { day: "numeric", month: "short", year: "numeric" }).format(new Date(data.meta.generatedAt))}</b></div></div>}
        <div className="language-toggle" aria-label="Language"><Languages size={15} aria-hidden="true" /><button type="button" aria-pressed={locale === "en"} onClick={() => setLocale("en")}>EN</button><span>/</span><button type="button" aria-pressed={locale === "ar"} onClick={() => setLocale("ar")}>ع</button></div>
      </div></header>
      <FilterBar />
      <main id="main-content" tabIndex={-1} className="content">{state === "fallback" && <div className="fallback-banner" role="status"><strong>{t("fallback")}</strong><span>{t("fallbackHint")}</span></div>}{children}</main>
      <footer><span>PrimeOrder Commerce Intelligence</span><span>Public-demo · Schema v{data?.schemaVersion ?? "1.0"} · Seed {data?.meta.seed ?? 20250301}</span></footer>
    </div>
  </div>;
}

export function AppShell({ children }: { children: React.ReactNode }) {
  return <DashboardProvider><a className="skip-link" href="#main-content">Skip to content</a><ShellContent>{children}</ShellContent></DashboardProvider>;
}
