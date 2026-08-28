"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { fallbackData } from "@/data/fallback";
import { assetUrl, filterRecords, initialFilters, normalizeDashboardData } from "@/lib/data";
import { getMessage, type MessageKey } from "@/lib/i18n";
import type { DashboardData, Filters, Locale } from "@/lib/types";

type LoadState = "loading" | "ready" | "fallback" | "error";
interface DashboardContextValue {
  data: DashboardData | null; filteredRecords: DashboardData["records"]; state: LoadState; locale: Locale;
  filters: Filters; setFilters: React.Dispatch<React.SetStateAction<Filters>>; setLocale: (locale: Locale) => void;
  t: (key: MessageKey) => string; reload: () => void;
}

const DashboardContext = createContext<DashboardContextValue | null>(null);

export function DashboardProvider({ children }: { children: React.ReactNode }) {
  const [data, setData] = useState<DashboardData | null>(null);
  const [state, setState] = useState<LoadState>("loading");
  const [locale, setLocaleState] = useState<Locale>("en");
  const [filters, setFilters] = useState<Filters>(() => initialFilters());

  const load = useCallback(async () => {
    setState("loading");
    try {
      const response = await fetch(assetUrl("/data/dashboard.json"), { cache: "force-cache" });
      if (!response.ok) throw new Error(`Public dataset returned ${response.status}`);
      const normalized = normalizeDashboardData(await response.json());
      setData(normalized);
      setFilters(initialFilters(normalized));
      setState("ready");
    } catch {
      setData(fallbackData);
      setFilters(initialFilters(fallbackData));
      setState("fallback");
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);
  useEffect(() => {
    const timer = window.setTimeout(() => {
      const saved = window.localStorage.getItem("primeorder-locale");
      if (saved === "ar" || saved === "en") setLocaleState(saved);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);
  useEffect(() => {
    document.documentElement.lang = locale;
    document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
  }, [locale]);

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next);
    window.localStorage.setItem("primeorder-locale", next);
  }, []);
  const filteredRecords = useMemo(() => data ? filterRecords(data.records, filters) : [], [data, filters]);
  const t = useCallback((key: MessageKey) => getMessage(locale, key), [locale]);
  const value = useMemo(() => ({ data, filteredRecords, state, locale, filters, setFilters, setLocale, t, reload: load }), [data, filteredRecords, state, locale, filters, setLocale, t, load]);

  return <DashboardContext.Provider value={value}>{children}</DashboardContext.Provider>;
}

export function useDashboard() {
  const context = useContext(DashboardContext);
  if (!context) throw new Error("useDashboard must be used inside DashboardProvider");
  return context;
}
