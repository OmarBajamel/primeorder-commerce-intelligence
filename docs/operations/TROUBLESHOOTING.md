# Troubleshooting

Start with the narrow symptom below. Preserve privacy: do not paste environment contents, tokens, headers, raw connector payloads, private database rows or exact live metrics into logs/issues/chat.

## Setup and dependencies

| Symptom | Likely cause | Safe checks | Resolution |
|---|---|---|---|
| `pnpm` is missing or wrong version | Corepack disabled or package manager mismatch | `node --version`; `corepack --version`; inspect root `packageManager` | Enable Corepack and activate/install pnpm `11.15.1`; rerun bootstrap |
| Next.js reports unsupported Node | Node below supported range | `node --version` | Use Node 20.9+; project baseline is Node 22 |
| Python is not found | No usable Python 3 executable was detected | Set `PYTHON_EXECUTABLE` to an approved Python 3.11+ path or install Python | Rerun the cross-platform `node scripts/run_python.mjs --version` probe, then bootstrap |
| Python module import fails | Requirements not installed into the interpreter selected by the wrapper | `node scripts/run_python.mjs -m pip --version`; `node scripts/run_python.mjs -m pip check` | `node scripts/run_python.mjs -m pip install --require-hashes -r requirements.lock` |
| `pnpm install --frozen-lockfile` fails | Lockfile missing/stale or wrong pnpm | Inspect Git status and package manager version | Use project pnpm; regenerate lockfile only as an intentional reviewed dependency change |

## Data generation and analytics

| Symptom | Diagnosis | Resolution |
|---|---|---|
| API readiness is 503 / “Generate fixtures” | Required `data/public-demo/api/*.json` absent | Run `pnpm data:generate`; confirm `metadata.json` says `public-demo` and expected seed/date range |
| Regeneration changes logical data/hash unexpectedly | Generator/dependency/version drift or nondeterministic timestamp/order | Compare seed, schema/generator code and manifest; remove runtime timestamps from dataset; fix the generator, do not update expected hashes blindly |
| dbt cannot find profile/project | Wrong working directory/arguments | Run root `pnpm analytics:build`, which supplies both directories |
| dbt DuckDB file is locked | API/dbt/inspection process holds the DB | Stop the owning project process after identifying it; rerun. Do not delete an unknown open DB |
| dbt quality mart contains warnings | Six synthetic anomalies are intentional | Confirm warning IDs match `metadata.json`; structural tests must still pass. A new/unexpected warning is a defect |
| Reconciliation test fails | Source scopes or generator logic drifted beyond global tolerance | Check timezone/date/status/currency/value/refund definitions and duplicate logic; do not widen tolerance to hide a defect |
| Product relationship test fails on `UNMAPPED-001` | Intentional anomaly is designed for left mapping, not a strict relationship | Verify test design expects the unmapped record in quality output. Do not silently drop it |

## API

| Symptom | Diagnosis | Resolution |
|---|---|---|
| Port 8000 already in use | Prior project API or unrelated process | `Get-NetTCPConnection -LocalPort 8000 -State Listen`; inspect owning process | Stop only the identified intended project process or select a documented alternate local port and update the client |
| `/summary` returns 400 | `date_from` is after `date_to` | Inspect URL dates only—no private payload | Correct inclusive ISO dates |
| `/summary` returns 404 | No fixture rows in selected range | Compare to metadata period | Choose `2025-01-01` through `2025-12-31` for demo or regenerate |
| 422 validation response | Unsupported filter/value/limit | Use `/docs` and contracts | Send accepted enums and limits; do not relax validation casually |
| Response appears stale after regenerating data | Repository uses process-local caching | Restart the API after regeneration | Stop/start Uvicorn; confirm readiness/mode |
| Unexpected API error | Sanitized `request_failed` log contains request ID and route only | Use the request ID; keep logs private | Fix the cause without interpolating upstream exception text or payloads |

## Web and static export

| Symptom | Diagnosis | Resolution |
|---|---|---|
| JS/CSS/images 404 on GitHub Pages | Repository base path mismatch | Inspect built URLs and `GITHUB_REPOSITORY`/`NEXT_PUBLIC_BASE_PATH` names, not secrets | Rebuild with the exact repository base path; verify trailing-slash routes |
| Direct navigation fails | Static route/trailing-slash or missing export | Inspect `apps/web/out` and Pages URL | Ensure route is statically generated and links respect base path/trailing slash |
| Public page requests localhost/private API | Public data-source boundary violated | Browser network inspection and bundle search | Stop release; remove runtime API path and rebuild from precomputed public JSON |
| Synthetic disclosure missing | UI regression or cropped responsive view | Inspect all routes/viewports/languages | Restore visible disclosure and recapture screenshots |
| Arabic layout reads LTR | Missing `dir="rtl"`, logical CSS or component override | Inspect `<html lang/dir>`, layout and charts/tables at mobile/desktop | Use document direction and CSS logical properties; test each route. Do not mirror data/charts blindly |
| Hydration/build differs by time/locale | Nondeterministic render or browser-only API | Search for current time/random/locale assumptions | Pass deterministic values and isolate browser behavior; rebuild cleanly |

## Connectors

| Status/symptom | Meaning | Action |
|---|---|---|
| `FIXTURE_MODE` | Deterministic public file selected | Expected for public builds; do not call it live-connected |
| `READY_NOT_AUTHENTICATED` | Live interface path exists but no usable credentials/executor | Configure through official secure local flow only if authorized; credentials never block public demo |
| `UNAVAILABLE` | Live transport/tool absent | Use fixture/import visibly; record limitation; do not build an unauthorized substitute |
| `FAILED_WITH_EVIDENCE` | Validation/import/read failed safely | Follow safe error code/evidence; never reveal raw response or credential detail |
| File import fails | Missing required fields, wrong JSON shape or unsupported suffix | Use `.csv` or record-array/`{records:[...]}` `.json`; validate header and schema version |
| Salla operation rejected | Operation is not on aggregate read allowlist | Do not bypass. Request design/security review for a genuinely required read capability |
| Live result status is connected but public page shows fixtures | Intended separation | Public site must remain fixtures; live aggregate analysis is local-only |
| Quota/rate limit | Vendor throttled a read | Honor retry hints and bounded backoff; do not add accounts/scopes or hammer endpoint |

Current application evidence intentionally reports all six public connectors as `FIXTURE_MODE` and live fresh-clone paths as `READY_NOT_AUTHENTICATED`. Active Codex tool reachability may differ; it is not inherited by a cloned application.

## Tests, screenshots and release gate

| Symptom | Diagnosis | Resolution |
|---|---|---|
| Playwright browser missing | Browser binaries not installed | Run project-appropriate Playwright browser installation; record dependency change only if needed |
| E2E server timeout | Web process failed, port conflict or wrong base URL | Inspect local process/build output and port owner | Fix the server/build; do not extend timeout first |
| Accessibility test fails | Semantic/contrast/focus/label/RTL regression | Open exact route/viewport and inspect axe finding | Fix component and rerun all relevant languages/viewports |
| Screenshot hash mismatch | File changed after manifest or wrong capture | Re-capture from final commit or regenerate manifest through screenshot workflow; rerun privacy review |
| Screenshot privacy check fails | Wrong mode, missing disclosure, metadata/content concern | Quarantine image from assets/releases | Correct app/capture, recapture and independently re-review |
| `release:check` says manifest missing | Screenshots have not been captured/evidenced | Run the finished app and `pnpm screenshots`; inspect manifest before rerun |
| Secret/PII scan flags documentation example | Real-looking example/pattern | Replace with clearly invalid placeholder or safe synthetic text; do not allowlist a real value |
| Release check flags private tracked path | Private file was staged/committed | Stop publication; remove from tracking without deleting the needed local source, assess history/exposure, rerun scan |
| Full test fails after narrow checks pass | Cross-track artifact/contract drift | Read first failing stage; fix root cause; rerun full suite | Do not skip later stages or weaken tests |

## Cleanup

`pnpm clean` intentionally removes only project build/report directories. If a server remains, stop its terminal process or identify the exact PID/command before ending it. After Docker use, run `docker compose down`. Confirm ports 3000/8000 are free before handoff.

## Escalation evidence

When a problem remains, record:

- command name (redacted arguments if necessary);
- OS/runtime/package versions;
- commit SHA and data mode;
- safe error code and concise message;
- expected/actual behavior;
- affected component and whether public/privacy boundary is at risk;
- paths to sanitized logs/evidence.

Never include environment dumps, credentials, headers, customer/order identifiers, private values or raw connector payloads.
