"""Fail-closed public release checks for tracked files and generated evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonl", ".csv", ".ts", ".tsx", ".js", ".mjs",
    ".py", ".sql", ".yml", ".yaml", ".toml", ".html", ".css", ".env", ".sh", ".ps1",
}
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    "google_api_key": re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    "generic_secret_assignment": re.compile(
        r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\s*[:=]\s*['\"](?!\s*$|example|placeholder)[^'\"\s]{12,}"
    ),
}
PII_PATTERNS = {
    "email": re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I),
    # Require an explicit KSA country prefix or local 05 prefix. Treating any
    # nine-digit substring beginning with 5 as a phone number creates false
    # positives inside SHA-256 hashes and deterministic numeric evidence.
    "saudi_phone": re.compile(r"(?<![\dA-F])(?:\+?966[\s-]?5\d{8}|05\d{8})(?![\dA-F])", re.I),
}
ALLOWED_EMAILS = {
    "omar-ba-jamel@users.noreply.github.com",
    "security@example.invalid",
    "conduct@example.invalid",
}


def tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    )
    return [ROOT / item.decode("utf-8") for item in proc.stdout.split(b"\0") if item]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    mode = os.getenv("DATA_MODE", "public-demo")
    if mode != "public-demo":
        failures.append(f"DATA_MODE must be public-demo, got {mode!r}")

    files = tracked_files()
    relative = [path.relative_to(ROOT).as_posix() for path in files]
    private_tracked = [name for name in relative if name.startswith(("data/private/", ".private/")) and not name.endswith(".gitkeep")]
    if private_tracked:
        failures.append(f"Private paths are tracked: {private_tracked}")

    scan_findings: list[dict[str, str]] = []
    for path, rel in zip(files, relative):
        if path.suffix.lower() not in TEXT_EXTENSIONS or not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                scan_findings.append({"file": rel, "rule": name})
        for name, pattern in PII_PATTERNS.items():
            for match in pattern.finditer(text):
                value = match.group(0).lower()
                if name == "email" and (value in ALLOWED_EMAILS or value.endswith("@example.com")):
                    continue
                if rel.startswith("data/public-demo/") and name == "email":
                    scan_findings.append({"file": rel, "rule": "synthetic_email_not_allowed"})
                elif name != "email" or "@" in value:
                    scan_findings.append({"file": rel, "rule": name})
    if scan_findings:
        failures.append(f"Secret/PII scan findings: {scan_findings[:20]}")

    for bundle_dir in (ROOT / "apps/web/out", ROOT / "apps/web/.next/static"):
        if not bundle_dir.exists():
            continue
        for path in bundle_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".js", ".html", ".json", ".css"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(?:localhost|127\.0\.0\.1):(?:8000|3001)", text):
                failures.append(f"Private/local endpoint embedded in public bundle: {path.relative_to(ROOT)}")

    screenshot_manifest = ROOT / "artifacts/evidence/screenshot-manifest.json"
    if screenshot_manifest.exists():
        entries = json.loads(screenshot_manifest.read_text(encoding="utf-8"))
        for entry in entries:
            asset = ROOT / entry["file_path"]
            if entry.get("data_mode") != "public-demo" or entry.get("privacy_review") != "PASS":
                failures.append(f"Screenshot privacy metadata failed: {entry.get('file_path')}")
            if not asset.exists() or sha256(asset) != entry.get("sha256"):
                failures.append(f"Screenshot hash mismatch: {entry.get('file_path')}")
    else:
        failures.append("Screenshot manifest is missing")

    placeholder_roots = [ROOT / "README.md", ROOT / "README.de.md", ROOT / "docs/career", ROOT / "docs/social"]
    placeholder = re.compile(r"(?i)(REPLACE_ME|EXAMPLE_URL|YOUR_GITHUB|TODO_URL|TBD_URL)")
    for target in placeholder_roots:
        paths = [target] if target.is_file() else list(target.rglob("*")) if target.exists() else []
        for path in paths:
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
                if placeholder.search(path.read_text(encoding="utf-8", errors="ignore")):
                    failures.append(f"Placeholder URL marker in {path.relative_to(ROOT)}")

    evidence = {
        "mode": mode,
        "tracked_file_count": len(files),
        "secret_pii_findings": scan_findings,
        "private_paths_tracked": private_tracked,
        "screenshot_manifest_present": screenshot_manifest.exists(),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }
    out = ROOT / "artifacts/evidence/release-check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
