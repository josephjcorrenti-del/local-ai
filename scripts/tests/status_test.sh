#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

run_owb() {
  PYTHONPATH="$REPO_ROOT/src" python3 -m local_ai.cli "$@"
}

echo "=== status (normal data) ==="
run_owb status > /tmp/status_normal.out 2>&1

if grep -q "/home/joe/ai/data/local_ai/sessions" /tmp/status_normal.out; then
  echo "[✓] normal status points to data sessions dir"
else
  echo "[✗] normal status did not point to expected data sessions dir"
  cat /tmp/status_normal.out
  exit 1
fi

echo
echo "=== status (test_data) ==="
run_owb --data-dir test_data status > /tmp/status_test.out 2>&1

if grep -q "/home/joe/ai/test_data/local_ai/sessions" /tmp/status_test.out; then
  echo "[✓] test_data status points to test_data sessions dir"
else
  echo "[✗] test_data status did not point to expected test_data sessions dir"
  cat /tmp/status_test.out
  exit 1
fi

echo
echo "[✓] status test passed"
