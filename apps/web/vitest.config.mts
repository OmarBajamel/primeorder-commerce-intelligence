import { defineConfig } from "vitest/config";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: { alias: { "@": path.resolve(here, "src") } },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    css: true,
    pool: "threads",
    maxWorkers: 1,
    coverage: { reporter: ["text", "html"], include: ["src/**/*.{ts,tsx}"] },
  },
});
