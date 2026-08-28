import { spawnSync } from "node:child_process";

const basePath = (process.env.STATIC_BASE_PATH || "/primeorder-commerce-intelligence").replace(/\/$/, "");
const windows = process.platform === "win32";
const command = windows ? (process.env.ComSpec || "cmd.exe") : "pnpm";
const args = windows ? ["/d", "/s", "/c", "pnpm --filter web build"] : ["--filter", "web", "build"];
const result = spawnSync(command, args, {
  stdio: "inherit",
  env: {
    ...process.env,
    DATA_MODE: "public-demo",
    NEXT_PUBLIC_BASE_PATH: basePath,
    STATIC_BASE_PATH: basePath,
  },
});

if (result.error) throw result.error;
process.exit(result.status ?? 1);
