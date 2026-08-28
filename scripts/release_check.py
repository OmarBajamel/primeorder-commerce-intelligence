"""Fail-closed public release checks for tracked files and generated evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
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
    "email": re.compile(r"(?<![\w.+-])[A-Z0-9][A-Z0-9._%+-]*@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I),
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
EXPECTED_SCREENSHOTS = {
    "assets/screenshots/01-executive-overview-desktop.png",
    "assets/screenshots/02-funnel-analysis-desktop.png",
    "assets/screenshots/03-product-performance-desktop.png",
    "assets/screenshots/04-data-quality-reconciliation-desktop.png",
    "assets/screenshots/05-seo-acquisition-desktop.png",
    "assets/screenshots/06-arabic-rtl-desktop.png",
    "assets/screenshots/07-executive-overview-mobile.png",
    "assets/screenshots/08-insights-backlog-mobile.png",
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
    required_files = {
        ".gitignore", "package.json", "scripts/generate_demo_data.py",
        "apps/web/public/data/dashboard.json", "data/private/.gitkeep",
    }
    required_missing = sorted(required_files.difference(relative))
    if not files:
        failures.append("Tracked-file inventory is empty; refusing a vacuous release scan")
    if required_missing:
        failures.append(f"Required release inventory is missing: {required_missing}")
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

    history_findings: list[dict[str, str]] = []
    history = subprocess.run(
        ["git", "log", "--all", "--format=", "--patch", "--no-ext-diff"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout.decode("utf-8", errors="ignore")
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(history):
            history_findings.append({"scope": "git_history", "rule": name})
    for name, pattern in PII_PATTERNS.items():
        for match in pattern.finditer(history):
            value = match.group(0).lower()
            if name == "email" and (value in ALLOWED_EMAILS or value.endswith("@example.com")):
                continue
            history_findings.append({"scope": "git_history", "rule": name})
            break
    if history_findings:
        failures.append(f"Git-history secret/PII findings: {history_findings[:20]}")

    archive_findings: list[dict[str, str]] = []
    archive_paths = list((ROOT / "artifacts" / "release").glob("*.zip")) + list((ROOT / "artifacts" / "linkedin").glob("*.zip"))
    for archive in archive_paths:
        with zipfile.ZipFile(archive) as handle:
            for member in handle.infolist():
                normalized = member.filename.replace("\\", "/")
                if normalized.startswith(("data/private/", ".private/")) or re.search(r"(^|/)\.env(?!\.example$)", normalized):
                    archive_findings.append({"archive": archive.name, "member": normalized, "rule": "private_path"})
                    continue
                suffix = Path(normalized).suffix.lower()
                if member.file_size > 5_000_000 or suffix not in TEXT_EXTENSIONS:
                    continue
                content = handle.read(member).decode("utf-8", errors="ignore")
                for name, pattern in SECRET_PATTERNS.items():
                    if pattern.search(content):
                        archive_findings.append({"archive": archive.name, "member": normalized, "rule": name})
                for name, pattern in PII_PATTERNS.items():
                    for match in pattern.finditer(content):
                        value = match.group(0).lower()
                        if name == "email" and (value in ALLOWED_EMAILS or value.endswith("@example.com")):
                            continue
                        archive_findings.append({"archive": archive.name, "member": normalized, "rule": name})
                        break
    if archive_findings:
        failures.append(f"Release-archive findings: {archive_findings[:20]}")

    public_bundle = ROOT / "apps/web/out"
    if not public_bundle.exists():
        failures.append("Public static bundle is missing; build the export before release:check")
    for bundle_dir in (public_bundle, ROOT / "apps/web/.next/static"):
        if not bundle_dir.exists():
            continue
        for path in bundle_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".js", ".html", ".json", ".css"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"https?://(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])(?::\d+)?", text, re.I):
                failures.append(f"Private/local endpoint embedded in public bundle: {path.relative_to(ROOT)}")

    screenshot_manifest = ROOT / "artifacts/evidence/screenshot-manifest.json"
    if screenshot_manifest.exists():
        entries = json.loads(screenshot_manifest.read_text(encoding="utf-8"))
        paths = [entry.get("file_path") for entry in entries]
        if len(entries) != len(EXPECTED_SCREENSHOTS) or set(paths) != EXPECTED_SCREENSHOTS or len(paths) != len(set(paths)):
            failures.append("Screenshot manifest must contain exactly the eight canonical unique evidence assets")
        capture_shas = {entry.get("commit_sha") for entry in entries}
        if len(capture_shas) != 1 or None in capture_shas:
            failures.append("Screenshot manifest must reference one capture commit SHA")
        for entry in entries:
            asset = ROOT / entry["file_path"]
            if (entry.get("data_mode") != "public-demo" or entry.get("privacy_review") != "PASS"
                    or not entry.get("privacy_reviewed_by") or not entry.get("privacy_reviewed_at")):
                failures.append(f"Screenshot privacy metadata failed: {entry.get('file_path')}")
            if not asset.exists() or sha256(asset) != entry.get("sha256"):
                failures.append(f"Screenshot hash mismatch: {entry.get('file_path')}")
        if len(capture_shas) == 1 and None not in capture_shas:
            capture_sha = next(iter(capture_shas))
            exists = subprocess.run(["git", "cat-file", "-e", f"{capture_sha}^{{commit}}"], cwd=ROOT, capture_output=True).returncode == 0
            if not exists:
                failures.append(f"Screenshot capture commit does not exist: {capture_sha}")
            else:
                invalidating = subprocess.run(
                    ["git", "diff", "--name-only", f"{capture_sha}..HEAD", "--", "apps/web", "data/public-demo", "scripts/generate_demo_data.py", "package.json", "pnpm-lock.yaml"],
                    cwd=ROOT, check=True, capture_output=True, text=True,
                ).stdout.splitlines()
                if invalidating:
                    failures.append(f"Screenshots are stale after presentation/data changes: {invalidating}")
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
        "required_files_missing": required_missing,
        "secret_pii_findings": scan_findings,
        "git_history_findings": history_findings,
        "release_archive_findings": archive_findings,
        "archive_scan_scope": "member names plus text-like members up to 5 MB; binary visual artifacts require separate render review",
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
