import { rmSync } from "node:fs";
import { resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const targets = [
  "apps/web/.next",
  "apps/web/out",
  "analytics/target",
  "analytics/logs",
  "playwright-report",
  "test-results",
];

for (const relative of targets) {
  const target = resolve(root, relative);
  if (target === root || !target.startsWith(`${root}${sep}`)) {
    throw new Error(`Refusing to remove path outside project: ${target}`);
  }
  rmSync(target, { recursive: true, force: true });
}

console.log("Removed project build and test outputs.");
