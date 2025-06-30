#!/bin/bash

# ------------------------
# Configurable Defaults
# ------------------------

DOCKER_IMAGE=${DOCKER_IMAGE:-auth}
DOCKERFILE=${DOCKERFILE:-auth/Dockerfile}

# ------------------------
# Docker Build Command
# ------------------------

echo "🛠  Building Docker image: $DOCKER_IMAGE"
docker build \
  -f "$DOCKERFILE" \
  -t "$DOCKER_IMAGE" .

echo "✅ Build complete"
