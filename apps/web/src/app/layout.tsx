import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/app-shell";

export const metadata: Metadata = {
  title: { default: "PrimeOrder Commerce Intelligence", template: "%s · PrimeOrder Intelligence" },
  description: "A privacy-safe bilingual commerce measurement portfolio for PrimeOrder.sa, powered entirely by deterministic synthetic data.",
  applicationName: "PrimeOrder Commerce Intelligence",
  authors: [{ name: "Omar Ba Jamel" }],
  keywords: ["e-commerce analytics", "GA4", "data quality", "CRO", "Saudi e-commerce", "portfolio"],
  robots: { index: true, follow: true },
  openGraph: { title: "PrimeOrder Commerce Intelligence", description: "Bilingual commerce analytics with transparent synthetic data and measurement-quality evidence.", type: "website", locale: "en_SA", alternateLocale: "ar_SA" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" dir="ltr" suppressHydrationWarning>
      <body><AppShell>{children}</AppShell></body>
    </html>
  );
}
