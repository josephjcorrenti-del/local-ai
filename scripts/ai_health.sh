#!/usr/bin/env bash
echo "[*] Ollama API:"
curl -s http://127.0.0.1:11434/api/version || echo "ollama not reachable"

echo
echo "[*] Open WebUI:"
ss -ltnp | grep ':8080' || echo "webui not listening"
