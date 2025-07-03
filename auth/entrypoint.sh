#!/bin/bash
set -e

echo "🔄 Running Auth migrations..."
npx @better-auth/cli migrate --y

echo "🚀 Starting Auth server..."

if [ "$1" = "dev" ]; then
  exec npm run dev
elif [ "$1" = "start" ]; then
  exec npm run start
else
  echo "❓ Unknown command: $1"
  exec "$@"
fi
