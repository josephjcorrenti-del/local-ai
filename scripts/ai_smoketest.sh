#!/usr/bin/env bash
set -e

echo "[*] Ollama version:"
curl -fsS http://127.0.0.1:11434/api/version
echo

echo "[*] Ollama models:"
curl -fsS http://127.0.0.1:11434/api/tags | head -c 300
echo
echo

echo "[*] Open WebUI listening on 8080?"
ss -ltn | grep -q ':8080' && echo "[✓] webui port open" || (echo "[!] webui port not open" && exit 1)

curl -fsS http://127.0.0.1:8080/ >/dev/null && echo "[✓] webui http ok"

echo "[✓] smoke test passed"
