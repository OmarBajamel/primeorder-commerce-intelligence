# Dashboard application

This package contains the static Next.js recruiter dashboard for PrimeOrder Commerce Intelligence. It reads only the committed deterministic `public-demo` contract at `public/data/dashboard.json`; it never calls FastAPI, MCP, localhost, or a vendor API in the public build.

Run package commands from the repository root so the single workspace lockfile remains authoritative:

```bash
pnpm install --frozen-lockfile
pnpm data:generate
pnpm dev:web
pnpm --filter web build
```

GitHub Pages builds set `NEXT_PUBLIC_BASE_PATH` to the repository name. The independent static-export browser test mounts `apps/web/out` at that path and checks all nine routes by direct navigation.
