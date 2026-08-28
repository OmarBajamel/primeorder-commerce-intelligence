FROM node:22-alpine

ENV DATA_MODE=public-demo
WORKDIR /workspace

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json ./apps/web/package.json
RUN corepack enable && pnpm install --frozen-lockfile

COPY apps/web ./apps/web
RUN chown -R node:node /workspace

USER node
EXPOSE 3000
CMD ["pnpm", "dev:web", "--hostname", "0.0.0.0"]
