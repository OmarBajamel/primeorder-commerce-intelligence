import sharp from "sharp";
import { mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = resolve(root, "assets/architecture");
await mkdir(outDir, { recursive: true });

const escape = (value) => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const colors = { ink: "#14282f", muted: "#5f747a", teal: "#0b7f78", mint: "#dff4ee", sand: "#f3e7d3", navy: "#102b3f", line: "#b8c9ca", white: "#ffffff", bg: "#f7faf8" };
const box = (x, y, w, h, title, lines, tone = "white") => {
  const fill = tone === "mint" ? colors.mint : tone === "sand" ? colors.sand : tone === "navy" ? colors.navy : colors.white;
  const titleColor = tone === "navy" ? colors.white : colors.ink;
  const lineColor = tone === "navy" ? "#d6ebe6" : colors.muted;
  return `<g><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="${fill}" stroke="${colors.line}" stroke-width="2"/><text x="${x + 24}" y="${y + 38}" font-size="22" font-weight="700" fill="${titleColor}">${escape(title)}</text>${lines.map((line, i) => `<text x="${x + 24}" y="${y + 70 + i * 26}" font-size="16" fill="${lineColor}">${escape(line)}</text>`).join("")}</g>`;
};
const arrow = (x1, y1, x2, y2, label = "") => `<g><path d="M${x1} ${y1} L${x2} ${y2}" stroke="${colors.teal}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>${label ? `<text x="${(x1 + x2) / 2}" y="${(y1 + y2) / 2 - 10}" text-anchor="middle" font-size="14" font-weight="600" fill="${colors.teal}">${escape(label)}</text>` : ""}</g>`;
const shell = (title, subtitle, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${colors.teal}"/></marker><filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#102b3f" flood-opacity="0.08"/></filter></defs><rect width="1600" height="900" fill="${colors.bg}"/><rect x="0" y="0" width="1600" height="12" fill="${colors.teal}"/><text x="80" y="86" font-family="Arial, sans-serif" font-size="42" font-weight="700" fill="${colors.ink}">${escape(title)}</text><text x="80" y="124" font-family="Arial, sans-serif" font-size="19" fill="${colors.muted}">${escape(subtitle)}</text><g font-family="Arial, sans-serif" filter="url(#shadow)">${body}</g><text x="80" y="858" font-family="Arial, sans-serif" font-size="15" fill="${colors.muted}">PrimeOrder Commerce Intelligence · Public-demo architecture · Omar Ba Jamel</text></svg>`;

const architecture = shell(
  "Privacy-first commerce intelligence architecture",
  "Static recruiter demo and local private analysis share contracts without sharing private data.",
  [
    box(80, 190, 300, 180, "Read-only sources", ["PrimeOrder / Salla MCP", "GA4 · GSC · Merchant", "Clarity · optional Ads"], "sand"),
    box(80, 500, 300, 170, "Public fixtures", ["Fixed seed: 20250301", "365 synthetic days", "Six documented anomalies"], "mint"),
    box(505, 270, 330, 230, "Ingestion & contracts", ["Typed connector interface", "Schema validation", "Freshness + status", "CSV / JSON fallback", "Private path isolation"], "white"),
    box(960, 190, 330, 210, "DuckDB + dbt", ["Staging → intermediate", "12 decision marts", "KPI definitions", "Quality + reconciliation"], "navy"),
    box(960, 505, 250, 150, "Public contracts", ["Validated static JSON", "Local FastAPI reads same", "No dbt runtime coupling"], "white"),
    box(1305, 380, 230, 210, "Next.js", ["Static JSON mode", "EN + AR / RTL", "9 dashboard areas", "GitHub Pages", "No private endpoint"], "mint"),
    arrow(380, 280, 505, 330, "live-private"), arrow(380, 585, 505, 445, "public-demo"), arrow(835, 350, 960, 300, "validation branch"), arrow(835, 445, 960, 570, "public export"), arrow(1210, 580, 1305, 520, "static JSON"),
    `<g><rect x="470" y="720" width="660" height="76" rx="18" fill="#fff3e8" stroke="#df9a43" stroke-width="2"/><text x="500" y="750" font-size="18" font-weight="700" fill="#854d13">Release privacy gate</text><text x="500" y="778" font-size="15" fill="#755c42">Public mode · secret/PII scan · ignored private paths · screenshot hashes · bundle endpoint scan</text></g>`,
  ].join("")
);

const lineage = shell(
  "Analytics lineage and decision layer",
  "Public contracts and tested SQL are parallel consumers of the same deterministic, source-labelled fixtures.",
  [
    box(70, 200, 250, 170, "Seeded source facts", ["sessions · events", "orders · items · refunds", "search · ads · UX"], "sand"),
    box(390, 200, 250, 170, "Staging models", ["typed columns", "source timestamps", "normalized keys"], "white"),
    box(710, 200, 250, 170, "Intermediate", ["daily source spine", "funnel rollup", "reconciliation"], "white"),
    box(1030, 175, 300, 230, "Decision marts", ["executive · funnel", "products · acquisition", "SEO · customers", "quality · insights"], "navy"),
    box(1380, 200, 160, 170, "Evidence", ["dbt tests", "lineage", "KPI checks"], "mint"),
    arrow(320, 285, 390, 285), arrow(640, 285, 710, 285), arrow(960, 285, 1030, 285), arrow(1330, 285, 1380, 285),
    box(390, 520, 250, 150, "KPI contract export", ["typed Python rules", "API-shaped JSON", "semantic regression"], "mint"),
    box(710, 520, 250, 150, "Public surfaces", ["FastAPI", "static JSON", "Next.js dashboard"], "mint"),
    box(1030, 520, 300, 150, "Evidence-linked actions", ["priority = impact × confidence", "direction, effort, owner", "validation experiment"], "sand"),
    arrow(195, 370, 515, 520, "same fixtures"), arrow(640, 595, 710, 595), arrow(960, 595, 1030, 595),
    `<text x="80" y="760" font-size="17" font-weight="700" fill="${colors.ink}">Source precedence</text><text x="80" y="790" font-size="16" fill="${colors.muted}">Commerce value: Salla aggregate → validated import → fixture · Behavior: GA4 → fixture · Search: GSC → fixture</text>`,
  ].join("")
);

await sharp(Buffer.from(architecture)).png().toFile(resolve(outDir, "system-architecture.png"));
await sharp(Buffer.from(lineage)).png().toFile(resolve(outDir, "data-lineage.png"));
console.log("Rendered architecture PNGs.");
