#!/usr/bin/env bash

echo "[*] Stopping Open WebUI..."
docker stop open-webui 2>/dev/null || true

echo "[*] Stopping Ollama..."
sudo systemctl stop ollama

echo "[✓] AI stack stopped."

