import { expect, test } from "@playwright/test";

const routes = ["/", "/funnel/", "/products/", "/acquisition/", "/seo/", "/customers/", "/quality/", "/insights/", "/methodology/"];
const basePath = (process.env.STATIC_BASE_PATH || "/primeorder-commerce-intelligence").replace(/\/$/, "");

test("Pages export works under the repository base path with direct navigation", async ({ page }) => {
  const failures: string[] = [];
  page.on("response", (response) => {
    if (response.status() >= 400) failures.push(`${response.status()} ${response.url()}`);
  });
  page.on("pageerror", (error) => failures.push(error.message));

  for (const route of routes) {
    await page.goto(`.${route}`);
    await expect(page.locator("footer").filter({ hasText: "Schema v1.0" })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText("Synthetic portfolio demo data — no real customer or revenue information").first()).toBeVisible();
    await expect(page.locator("main .page-view")).toBeVisible();
    expect(new URL(page.url()).pathname).toBe(`${basePath}${route}`);
  }
  expect(failures).toEqual([]);
});
