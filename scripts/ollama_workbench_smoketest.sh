#!/usr/bin/env bash
set -euo pipefail

run_owb() {
  if command -v ollama-workbench >/dev/null 2>&1; then
    ollama-workbench "$@"
  else
    PYTHONPATH=src python3 -m ollama_workbench.cli "$@"
  fi
}

echo "=== ai_status.sh ==="
./scripts/ai_status.sh
echo

echo "=== ai_health.sh ==="
./scripts/ai_health.sh
echo

echo "=== sessions ==="
run_owb sessions
echo

echo "=== stats ==="
run_owb stats
echo

echo "=== summarize ==="
run_owb summarize --session scratch
echo

echo "=== status ==="
run_owb status
echo

echo "=== doctor ==="
run_owb doctor
echo

echo "=== web-fetch ==="
run_owb web-fetch https://example.com
echo

echo "=== web-chat ==="
run_owb web-chat "test" --url https://example.com
echo

echo "=== web-cleanup (dry run) ==="
run_owb web-cleanup --days 0
echo
