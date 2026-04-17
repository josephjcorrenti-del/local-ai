#!/usr/bin/env bash

echo "=== Ollama Health Check ==="

echo "[*] API /api/version:"
curl -s http://127.0.0.1:11434/api/version || echo "not reachable"

echo
echo "[*] API /api/tags (models):"
curl -s http://127.0.0.1:11434/api/tags || echo "not reachable"
