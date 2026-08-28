import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const out = resolve(root, "apps", "web", "out");
const basePath = (process.env.STATIC_BASE_PATH || "/primeorder-commerce-intelligence").replace(/\/$/, "");
const port = Number(process.env.STATIC_PORT || 4173);
const types = { ".css": "text/css", ".html": "text/html", ".ico": "image/x-icon", ".js": "text/javascript", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".txt": "text/plain" };

if (!existsSync(out)) throw new Error("apps/web/out is missing; build the Pages export first");

const server = createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url || "/", "http://127.0.0.1").pathname);
  if (pathname === basePath) {
    response.writeHead(308, { location: `${basePath}/` });
    response.end();
    return;
  }
  if (!pathname.startsWith(`${basePath}/`)) {
    response.writeHead(404).end("Not found");
    return;
  }
  const relative = pathname.slice(basePath.length + 1);
  let target = resolve(out, relative);
  if (target !== out && !target.startsWith(`${out}${sep}`)) {
    response.writeHead(400).end("Invalid path");
    return;
  }
  if (existsSync(target) && statSync(target).isDirectory()) target = resolve(target, "index.html");
  if (!existsSync(target) && !extname(target)) target = resolve(target, "index.html");
  if (!existsSync(target) || !statSync(target).isFile()) {
    response.writeHead(404).end("Not found");
    return;
  }
  response.writeHead(200, { "content-type": `${types[extname(target)] || "application/octet-stream"}; charset=utf-8`, "cache-control": "no-store" });
  createReadStream(target).pipe(response);
});

server.listen(port, "127.0.0.1", () => console.log(`Static export mounted at http://127.0.0.1:${port}${basePath}/`));
for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => server.close(() => process.exit(0)));
