# Read-only connector adapters

All six adapters implement the same typed result contract, deterministic fixture
mode, CSV/JSON import, required-field validation, freshness metadata, retry policy
metadata, and explicit statuses. Public builds use only `FIXTURE_MODE`.

Live credentials are detected only by presence and never logged. The Salla bridge
requires an injected environment-owned MCP executor, accepts only allow-listed
read operations, projects only privacy-safe aggregate fields, and never writes raw
MCP results. Live transports intentionally remain outside this public repository.
