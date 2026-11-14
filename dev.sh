#!/usr/bin/env bash
# Restart the docker stack and start the frontend dev server if it isn't already running.
cd "$(dirname "$0")"

docker compose down
docker compose up -d --build

# Vite's default port is 5173
if curl -s -o /dev/null http://localhost:5173; then
  echo "Frontend already running on :5173"
else
  cd frontend && npm run dev
fi
