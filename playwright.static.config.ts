import { defineConfig, devices } from "@playwright/test";

const basePath = (process.env.STATIC_BASE_PATH || "/primeorder-commerce-intelligence").replace(/\/$/, "");

export default defineConfig({
  testDir: ".",
  testMatch: ["tests/e2e/static-export.spec.ts"],
  workers: 1,
  reporter: [["line"]],
  use: {
    baseURL: `http://127.0.0.1:4173${basePath}/`,
    trace: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 1000 } } }],
  webServer: {
    command: "node scripts/serve_static_export.mjs",
    url: `http://127.0.0.1:4173${basePath}/`,
    reuseExistingServer: false,
    timeout: 30_000,
  },
});
