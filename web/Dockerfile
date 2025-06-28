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
RUN npx turbo prune --scope=web --docker

# ---------------- Build Nuxt App ----------------
FROM base AS builder

WORKDIR /mono

COPY --from=pruner /mono/out/json ./
COPY --from=pruner /mono/out/pnpm-workspace.yaml ./pnpm-workspace.yaml
COPY --from=pruner /mono/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN pnpm install --frozen-lockfile

COPY --from=pruner /mono/out/full ./
WORKDIR /mono/web

# Pass build-time environment variables
ARG NUXT_PUBLIC_AUTH_BASE_URL
ARG NUXT_PUBLIC_APP_BASE_URL
ARG NUXT_PUBLIC_API_SCHEME
ARG NUXT_PUBLIC_API_BASE_URL
ARG NUXT_PUBLIC_GOOGLE_ANALYTICS_ID
ARG NUXT_PUBLIC_S3_URL

ENV NUXT_PUBLIC_AUTH_BASE_URL=$NUXT_PUBLIC_AUTH_BASE_URL
ENV NUXT_PUBLIC_APP_BASE_URL=$NUXT_PUBLIC_APP_BASE_URL
ENV NUXT_PUBLIC_API_SCHEME=$NUXT_PUBLIC_API_SCHEME
ENV NUXT_PUBLIC_API_BASE_URL=$NUXT_PUBLIC_API_BASE_URL
ENV NUXT_PUBLIC_GOOGLE_ANALYTICS_ID=$NUXT_PUBLIC_GOOGLE_ANALYTICS_ID
ENV NUXT_PUBLIC_S3_URL=$NUXT_PUBLIC_S3_URL

RUN pnpm generate

# ---------------- Runtime Image ----------------
FROM node:24-alpine AS runner

RUN apk add --no-cache dumb-init

ENV NODE_ENV=production
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Use non-root user
ARG UID=1001
ARG GID=1001
RUN addgroup --system --gid ${GID} webuser \
  && adduser --system --uid ${UID} --ingroup webuser webuser
USER webuser

WORKDIR /app

COPY --from=builder --chown=webuser:webuser /mono/web/.output ./.output
COPY --from=builder --chown=webuser:webuser /mono/web/entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["dumb-init", "--", "sh", "./entrypoint.sh"]