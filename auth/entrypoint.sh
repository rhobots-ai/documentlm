#!/bin/bash
set -e

echo "🔄 Running Auth migrations..."
npx @better-auth/cli migrate --y

echo "🚀 Starting Auth server..."

if [ "$1" = "dev" ]; then
  exec pnpm run dev
elif [ "$1" = "start" ]; then
  exec pnpm run start
else
  echo "❓ Unknown command: $1"
  exec "$@"
fi
