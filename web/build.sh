#!/bin/bash

# ------------------------
# Configurable Defaults
# ------------------------

DOCKER_IMAGE=${DOCKER_IMAGE:-rhobotsai/documentlm-web:latest}
DOCKERFILE=${DOCKERFILE:-web/Dockerfile}

NUXT_PUBLIC_AUTH_BASE_URL=${NUXT_PUBLIC_AUTH_BASE_URL:-http://localhost:10000}
NUXT_PUBLIC_APP_BASE_URL=${NUXT_PUBLIC_APP_BASE_URL:-http://localhost:3000}
NUXT_PUBLIC_API_SCHEME=${NUXT_PUBLIC_API_SCHEME:-http}
NUXT_PUBLIC_API_BASE_URL=${NUXT_PUBLIC_API_BASE_URL:-localhost:8000}
NUXT_PUBLIC_GOOGLE_ANALYTICS_ID=${NUXT_PUBLIC_GOOGLE_ANALYTICS_ID:-G-XXXXXXX}
NUXT_PUBLIC_S3_URL=${NUXT_PUBLIC_S3_URL:-http://localhost:9090/documentlm/}

# ------------------------
# Docker Build Command
# ------------------------

echo "🛠  Building Docker image: $DOCKER_IMAGE"
docker build \
  -f "$DOCKERFILE" \
  --build-arg NUXT_PUBLIC_AUTH_BASE_URL="$NUXT_PUBLIC_AUTH_BASE_URL" \
  --build-arg NUXT_PUBLIC_APP_BASE_URL="$NUXT_PUBLIC_APP_BASE_URL" \
  --build-arg NUXT_PUBLIC_API_SCHEME="$NUXT_PUBLIC_API_SCHEME" \
  --build-arg NUXT_PUBLIC_API_BASE_URL="$NUXT_PUBLIC_API_BASE_URL" \
  --build-arg NUXT_PUBLIC_GOOGLE_ANALYTICS_ID="$NUXT_PUBLIC_GOOGLE_ANALYTICS_ID" \
  --build-arg NUXT_PUBLIC_S3_URL="$NUXT_PUBLIC_S3_URL" \
  -t "$DOCKER_IMAGE" .

echo "✅ Build complete"
