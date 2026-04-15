#!/usr/bin/env bash

echo "=== AI Stack Status ==="

echo -n "Ollama: "
systemctl is-active ollama || true

echo -n "Docker: "
systemctl is-active docker || true

echo -n "Open WebUI: "
docker ps --format '{{.Names}}' | grep -q open-webui && echo running || echo stopped

