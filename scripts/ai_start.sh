#!/usr/bin/env bash
set -e

echo "=== AI Stack Startup ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Docker
"$SCRIPT_DIR/docker_start.sh"

# 2. Ollama
echo "[*] Checking Ollama service..."
if ! systemctl is-active --quiet ollama; then
  echo "[+] Starting Ollama..."
  sudo systemctl start ollama
else
  echo "[=] Ollama already running."
fi

# 3. Open WebUI
"$SCRIPT_DIR/openwebui_start.sh"

echo
echo "[✓] AI stack is up"
echo "    Ollama:    http://127.0.0.1:11434"
echo "    Open WebUI: http://localhost:8080"

