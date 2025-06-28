# ---------------- Base Image Setup ----------------
FROM --platform=${TARGETPLATFORM:-linux/amd64} node:24-alpine AS base

RUN apk update && apk upgrade --no-cache libc6-compat libcrypto3 libssl3
RUN corepack enable
RUN corepack prepare pnpm@10.12.3 --activate

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

# ---------------- Prune Dependencies ----------------
FROM base AS pruner

WORKDIR /mono
COPY . .

RUN pnpm install --frozen-lockfile
RUN npx turbo prune --scope=auth --docker

# ---------------- Builder Stage ----------------
FROM base AS builder

WORKDIR /mono

# Copy pruned files
COPY --from=pruner /mono/out/json/ ./
COPY --from=pruner /mono/out/pnpm-lock.yaml ./pnpm-lock.yaml
COPY --from=pruner /mono/out/pnpm-workspace.yaml ./pnpm-workspace.yaml
RUN pnpm install --frozen-lockfile

COPY --from=pruner /mono/out/full/ ./
# ---------------- Runtime Image ----------------
FROM node:24-alpine AS runner

RUN apk add --no-cache dumb-init curl

WORKDIR /app

# Use non-root user
ARG UID=1001
ARG GID=1001
RUN addgroup --system --gid ${GID} express \
  && adduser --system --uid ${UID} --ingroup express express
USER express

COPY --from=builder --chown=express:express /mono .

EXPOSE 10000

WORKDIR /app/auth

RUN chmod +x entrypoint.sh

#CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["dumb-init", "--", "sh", "./entrypoint.sh"]
