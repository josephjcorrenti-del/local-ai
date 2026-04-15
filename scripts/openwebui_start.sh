#!/usr/bin/env bash
set -e

NAME="open-webui"
IMAGE="ghcr.io/open-webui/open-webui:main"
VOL="open-webui"

if docker ps --format '{{.Names}}' | grep -qx "$NAME"; then
  echo "[=] open-webui already running"
  exit 0
fi

if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
  echo "[+] starting existing open-webui container"
  docker start "$NAME"
  exit 0
fi

echo "[+] creating open-webui container"
docker run -d \
  --name "$NAME" \
  --restart always \
  --network=host \
  -e OLLAMA_BASE_URL="http://127.0.0.1:11434" \
  -v "$VOL":/app/backend/data \
  "$IMAGE"
