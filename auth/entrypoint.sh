#!/bin/bash
set -e

echo "🔄 Running Auth migrations..."
npx @better-auth/cli migrate --y

echo "🚀 Starting Auth server..."
exec node server.ts