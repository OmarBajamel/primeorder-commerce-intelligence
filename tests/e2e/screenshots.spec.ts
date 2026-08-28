import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { expect, test } from "@playwright/test";

const root = resolve(__dirname, "../..");
const screenshotDir = resolve(root, "assets/screenshots");
const manifestPath = resolve(root, "artifacts/evidence/screenshot-manifest.json");

type ManifestEntry = {
  file_path: string;
  route: string;
  viewport: string;
  language: "en" | "ar";
  data_mode: "public-demo";
  commit_sha: string;
  capture_time: string;
  sha256: string;
  privacy_review: "PENDING" | "PASS";
  privacy_reviewed_by: string | null;
  privacy_reviewed_at: string | null;
  intended_use: string;
  alt_text: string;
};

test.describe.configure({ mode: "serial" });

test("capture deterministic portfolio evidence", async ({ page }) => {
  await mkdir(screenshotDir, { recursive: true });
  const commit = execFileSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" }).trim();
  const entries: ManifestEntry[] = [];
  const cases = [
    ["01-executive-overview-desktop.png", "/", 1440, 1000, "en", "Recruiter hero", "PrimeOrder executive overview with synthetic commerce KPIs and trends"],
    ["02-funnel-analysis-desktop.png", "/funnel/", 1440, 1000, "en", "Portfolio evidence", "Synthetic commerce funnel with step conversion and abandonment"],
    ["03-product-performance-desktop.png", "/products/", 1440, 1000, "en", "Portfolio evidence", "Synthetic product and category performance analysis"],
    ["04-data-quality-reconciliation-desktop.png", "/quality/", 1440, 1000, "en", "Portfolio evidence", "Data quality rules, connector freshness, and source reconciliation"],
    ["05-seo-acquisition-desktop.png", "/seo/", 1440, 1000, "en", "Portfolio evidence", "Synthetic SEO and Merchant performance dashboard"],
    ["06-arabic-rtl-desktop.png", "/", 1440, 1000, "ar", "RTL evidence", "Arabic right-to-left executive commerce dashboard using synthetic data"],
    ["07-executive-overview-mobile.png", "/", 390, 844, "en", "Mobile evidence", "Mobile executive overview with synthetic KPIs"],
    ["08-insights-backlog-mobile.png", "/insights/", 390, 844, "en", "Mobile evidence", "Mobile evidence-linked commerce action backlog"],
  ] as const;

  for (const [name, route, width, height, language, intendedUse, altText] of cases) {
    await page.setViewportSize({ width, height });
    await page.goto(route);
    await expect(page.locator("footer").filter({ hasText: "Schema v1.0" })).toBeVisible({ timeout: 15_000 });
    await page.getByRole("button", { name: language === "ar" ? "ع" : "EN", exact: true }).click();
    await expect(page.locator("html")).toHaveAttribute("lang", language);
    await expect(page.locator("html")).toHaveAttribute("dir", language === "ar" ? "rtl" : "ltr");
    await expect(page.locator("main .page-view")).toBeVisible();
    await expect(page.getByText("Synthetic portfolio demo data — no real customer or revenue information").first()).toBeVisible();
    const renderedText = await page.locator("body").innerText();
    expect(renderedText).not.toMatch(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i);
    expect(renderedText).not.toMatch(/(?:\+?966[\s-]?5\d{8}|05\d{8})/);
    const target = resolve(screenshotDir, name);
    await page.screenshot({ path: target, fullPage: false, animations: "disabled" });
    const bytes = await readFile(target);
    entries.push({
      file_path: `assets/screenshots/${name}`,
      route,
      viewport: `${width}x${height}`,
      language,
      data_mode: "public-demo",
      commit_sha: commit,
      capture_time: new Date().toISOString(),
      sha256: createHash("sha256").update(bytes).digest("hex"),
      privacy_review: "PENDING",
      privacy_reviewed_by: null,
      privacy_reviewed_at: null,
      intended_use: intendedUse,
      alt_text: altText,
    });
  }
  await mkdir(resolve(root, "artifacts/evidence"), { recursive: true });
  await writeFile(manifestPath, `${JSON.stringify(entries, null, 2)}\n`, "utf8");
});
