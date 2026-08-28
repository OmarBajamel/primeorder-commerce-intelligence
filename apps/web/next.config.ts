import type { NextConfig } from "next";

const explicitBasePath = process.env.NEXT_PUBLIC_BASE_PATH?.replace(/\/$/, "");
const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const basePath = explicitBasePath ??
  (process.env.GITHUB_ACTIONS === "true" && repositoryName ? `/${repositoryName}` : "");

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  basePath,
  assetPrefix: basePath || undefined,
  images: { unoptimized: true },
  env: { NEXT_PUBLIC_BASE_PATH: basePath },
  poweredByHeader: false,
};

export default nextConfig;
