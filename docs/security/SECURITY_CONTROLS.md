# Security Controls

## Control status model

- `DESIGNED`: control requirement and mechanism are documented.
- `IMPLEMENTED_UNVERIFIED`: repository mechanism exists but passing evidence is not yet recorded.
- `VERIFIED`: identified evidence shows the control passed for a specific commit/artifact.
- `NOT_IMPLEMENTED`: required mechanism is absent.
- `NOT_APPLICABLE`: justified for the named scope.

This initial register is conservative. A document cannot promote its own control to `VERIFIED`; test/release evidence must identify the command, commit and artifact.

## Control register

| ID | Control | Mechanism/requirement | Initial status | Verification evidence required |
|---|---|---|---|---|
| `SEC-01` | Default public mode | `public-demo` is default and mandatory in builds/tests/screenshots/releases; release script rejects another mode | `IMPLEMENTED_UNVERIFIED` | Release check output and built artifact mode disclosure |
| `SEC-02` | Private-path exclusion | Ignore private/local paths; release script rejects tracked private files | `IMPLEMENTED_UNVERIFIED` | `git ls-files`/release gate result and separate history scan |
| `SEC-03` | Secret detection | Scan tracked files, history, build output and release archives for credentials/auth metadata | `DESIGNED` | Tool/version/pattern set, pass log, false-positive disposition |
| `SEC-04` | PII/private-metric detection | Pattern scan plus human review of text/binaries/screenshots | `DESIGNED` | Privacy report bound to commit/artifact hashes |
| `SEC-05` | Read-only connectors | Six adapters declare read-only; Salla bridge has an aggregate-operation and field allowlist | `IMPLEMENTED_UNVERIFIED` | Final code review/tests and source/tool scope record |
| `SEC-06` | Explicit connector mode/status | Typed five-state vocabulary, fixture/file/live modes, no silent fixture fallback, status artifact | `IMPLEMENTED_UNVERIFIED` | Connector tests and final `connector-status.json` |
| `SEC-07` | Input validation | Typed result/error envelope, connector-specific Pydantic field types/enums/bounds and allow-listed normalized projection | `VERIFIED` | Connector malformed metric/unknown-field tests; `CO-002` resolution |
| `SEC-08` | Injection prevention | Parameterized SQL, React escaping, controlled paths, formula neutralization for tabular export | `DESIGNED` | SAST/tests and manual import/export review |
| `SEC-09` | Local API isolation | Root script binds Uvicorn to loopback; structured errors; no CORS middleware is configured | `IMPLEMENTED_UNVERIFIED` | Listening-address/CORS/error-response tests |
| `SEC-10` | Safe logging | Request ID/route/status/duration only; unexpected exception payload and traceback are deliberately omitted | `VERIFIED` | API log-capture privacy test and `SEC-001` resolution |
| `SEC-11` | Dependency governance | Lockfiles/pins, maintained packages, automated vulnerability review, constrained update policy | `DESIGNED` | Lockfile, scan report and unresolved advisory review |
| `SEC-12` | CI least privilege | Minimal `GITHUB_TOKEN` permissions, trusted/pinned actions, no private credentials in public build | `DESIGNED` | Workflow review and successful CI run |
| `SEC-13` | Static public boundary | Next.js static export consumes precomputed synthetic shapes; release script scans built output for local endpoints | `IMPLEMENTED_UNVERIFIED` | Bundle/network scan and deployed-site browser evidence |
| `SEC-14` | Analytics integrity | dbt constraints, invariants, deduplication, item allocation, source reconciliation and semantic tests | `IMPLEMENTED_UNVERIFIED` | Final dbt manifest/run results and targeted formula tests |
| `SEC-15` | Consent-aware measurement | Defaults/updates before tags, granular purposes, scenario validation | `DESIGNED` | Privacy-approved expected states and Tag Assistant/network evidence |
| `SEC-16` | Screenshot provenance | Release script requires manifest mode/privacy state and verifies file hashes | `IMPLEMENTED_UNVERIFIED` | Final screenshot manifest plus visual/OCR review |
| `SEC-17` | Artifact provenance | Hash reviewed release contents; exact commit/tag; licensed/owned assets | `DESIGNED` | Evidence manifest, license inventory, release inspection |
| `SEC-18` | Incident response | Stop publication, contain, rotate, assess, notify privately, purge, learn | `DESIGNED` | Tabletop or real incident record (sanitized) |
| `SEC-19` | Retention/deletion | Documented expiry for live extracts, DBs, caches, logs and pseudonyms | `DESIGNED` | Local inventory and deletion procedure evidence |
| `SEC-20` | Branch/release review | Critical/high review findings resolved before publication; checklist sign-off | `DESIGNED` | `REVIEW_FINDINGS.md`, release checklist, final commit |

## Credential handling

- Prefer official tool-managed OAuth/device flows and OS credential storage.
- `.env.example` lists variable names only. Real `.env`/credential files are local and ignored.
- Never print, echo, inspect broadly, copy to chat, commit, screenshot or archive secret values.
- Do not accept passwords, PATs, OAuth tokens, cookies, service-account JSON, one-time/recovery codes, or payment credentials in project files.
- On suspected exposure, stop use and rotate/revoke through the provider before treating deletion as remediation.
- CI public-demo jobs should require no connector credential.

## Application/API controls

- FastAPI binds to `127.0.0.1` by default; Docker/explicit network exposure requires separate review.
- Validate filters against typed allowlists and bounds. Parameterize database queries.
- Use generic structured client errors and internal safe codes; do not return stack traces/upstream bodies.
- Set request size, timeout, pagination and row limits appropriate to a local analytics API.
- Health reports process state; readiness reports safe dependency state without credentials or private totals.
- CORS is disabled unless a specific local origin is required; never use credentialed wildcard origins.
- Public Next.js output does not call FastAPI or vendors.

## Dependency and vulnerability policy

1. Commit lockfiles and pinned Python dependencies; pin GitHub Actions to trusted versions/SHAs where practical.
2. Use maintained, necessary packages and remove unused dependencies.
3. Run ecosystem audits and review advisories in context; scan failures are not automatically dismissed.
4. Critical/high exploitable vulnerabilities in shipped/runtime scope block release. A documented non-exploitable/transitive finding requires owner, rationale, compensating control and review date.
5. Avoid install scripts or new registries without review; public CI gets minimal permissions and no live secrets.
6. Apply security updates promptly and rerun functional, accessibility, analytics and release gates.

## Logging and evidence

Evidence should answer what ran, when, against which commit/mode/artifact, with what result. It should not contain data payloads. Sanitize commands if arguments could contain sensitive paths/values. Store evidence hashes and safe summaries; keep live/private logs ignored and expire them according to policy.

## Release blocking conditions

Block the public release for any unresolved critical/high finding involving secrets, private data, live-mode artifact, mutation capability, public private endpoint, input/code execution, dependency exploitability, consent/privacy control in shipped tracking, inaccurate evidence, or unlicensed asset. See [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md).

## Incident response summary

1. Contain: stop deploy/release and restrict affected artifact/service.
2. Preserve safe evidence: do not copy the sensitive payload into tickets/logs.
3. Eradicate: revoke credentials, remove artifacts/caches, coordinate history purge when necessary.
4. Assess/notify: owner plus qualified security/privacy advisers determine contractual/legal duties.
5. Recover: rebuild from reviewed clean inputs and rerun every gate.
6. Learn: record root cause and durable control improvement without disclosing protected facts.
