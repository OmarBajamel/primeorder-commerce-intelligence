import { expect, test } from "@playwright/test";

const routes = [
  ["/", /Executive overview/],
  ["/funnel/", /Commerce funnel/],
  ["/products/", /Products & categories/],
  ["/acquisition/", /Acquisition/],
  ["/seo/", /SEO & Merchant/],
  ["/customers/", /Customers/],
  ["/quality/", /Data quality/],
  ["/insights/", /Action backlog/],
  ["/methodology/", /Methodology/],
] as const;

test.describe("public-demo dashboard", () => {
  for (const [route, title] of routes) {
    test(`${route} loads without private calls or console errors`, async ({ page }) => {
      const errors: string[] = [];
      const privateCalls: string[] = [];
      page.on("console", (message) => {
        if (message.type() === "error") errors.push(message.text());
      });
      page.on("pageerror", (error) => errors.push(error.message));
      page.on("request", (request) => {
        if (/localhost:8000|127\.0\.0\.1:8000|\/api\/private/i.test(request.url())) privateCalls.push(request.url());
      });

      await page.goto(route);
      await expect(page.getByRole("heading", { level: 1, name: title })).toBeVisible();
      await expect(page.getByText("Synthetic portfolio demo data — no real customer or revenue information")).toBeVisible();
      await expect(page.getByText("Preparing trusted metrics...")).toBeHidden({ timeout: 15_000 });
      await expect(page.locator("main figure, main table, main article, main section").first()).toBeVisible();
      expect(privateCalls).toEqual([]);
      expect(errors).toEqual([]);
    });
  }

  test("filters, comparison, export, and language direction work", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Preparing trusted metrics...")).toBeHidden({ timeout: 15_000 });
    const revenue = page
      .locator("article")
      .filter({ has: page.getByText("Net revenue", { exact: true }) })
      .locator(".kpi-value")
      .first();
    const before = await revenue.textContent();
    await page.getByRole("combobox", { name: "Device", exact: true }).selectOption({ label: "Mobile" });
    await expect(revenue).not.toHaveText(before ?? "", { timeout: 10_000 });

    const comparison = page.getByLabel("Compare with previous period");
    await expect(comparison).toBeChecked();
    await comparison.uncheck();
    await expect(page.getByText(/vs previous period/).first()).toBeHidden();

    const downloadPromise = page.waitForEvent("download");
    await page.getByRole("button", { name: "Export CSV" }).click();
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/\.csv$/);

    await page.getByRole("button", { name: "ع" }).click();
    await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
    await expect(page.locator("html")).toHaveAttribute("lang", "ar");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("نظرة");
  });

  test("mobile layout has no document-level horizontal overflow", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/insights/");
    await expect(page.getByText("Preparing trusted metrics...")).toBeHidden({ timeout: 15_000 });
    const overflow = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth);
    await expect(page.getByText("Synthetic portfolio demo data — no real customer or revenue information")).toBeVisible();
  });
});
