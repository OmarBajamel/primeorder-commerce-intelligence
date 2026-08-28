import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, resolve, sep } from "node:path";
import { pipeline } from "node:stream";
import { fileURLToPath } from "node:url";
import { createGzip } from "node:zlib";

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
  const extension = extname(target);
  const compressible = [".css", ".html", ".js", ".json", ".svg", ".txt"].includes(extension);
  const acceptsGzip = /\bgzip\b/.test(request.headers["accept-encoding"] || "");
  const headers = {
    "content-type": `${types[extension] || "application/octet-stream"}; charset=utf-8`,
    "cache-control": extension === ".html" ? "no-store" : "public, max-age=3600",
    ...(compressible && acceptsGzip ? { "content-encoding": "gzip", vary: "Accept-Encoding" } : {}),
  };
  response.writeHead(200, headers);
  if (compressible && acceptsGzip) pipeline(createReadStream(target), createGzip({ level: 9 }), response, () => {});
  else createReadStream(target).pipe(response);
});

server.listen(port, "127.0.0.1", () => console.log(`Static export mounted at http://127.0.0.1:${port}${basePath}/`));
for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => server.close(() => process.exit(0)));
