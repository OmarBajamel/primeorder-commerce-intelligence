import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

const requested = process.env.PYTHON_EXECUTABLE;
const bundled = join(homedir(), ".cache", "codex-runtimes", "codex-primary-runtime", "dependencies", "python", "python.exe");
const candidates = [
  ...(requested ? [[requested]] : []),
  ...(process.platform === "win32" && existsSync(bundled) ? [[bundled]] : []),
  ...(process.platform === "win32" ? [["py", "-3"]] : []),
  ["python3"],
  ["python"],
];

let command;
for (const candidate of candidates) {
  const probe = spawnSync(candidate[0], [...candidate.slice(1), "--version"], { stdio: "ignore" });
  if (probe.status === 0) {
    command = candidate;
    break;
  }
}

if (!command) {
  console.error("Python 3 was not found. Install Python 3.11+ or set PYTHON_EXECUTABLE to its executable path.");
  process.exit(1);
}

const result = spawnSync(command[0], [...command.slice(1), ...process.argv.slice(2)], { stdio: "inherit" });
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);
