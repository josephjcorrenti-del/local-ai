#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

run_owb() {
  PYTHONPATH="$REPO_ROOT/src" python3 -m ollama_workbench.cli "$@"
}

echo "=== doctor (normal data) ==="
if run_owb doctor > /tmp/doctor_normal.out 2>&1; then
  echo "[✓] normal doctor passed"
else
  echo "[✗] normal doctor failed unexpectedly"
  cat /tmp/doctor_normal.out
  exit 1
fi

echo
echo "=== doctor (test_data) ==="
if run_owb --data-dir test_data doctor > /tmp/doctor_test.out 2>&1; then
  echo "[✗] test_data doctor unexpectedly passed"
  cat /tmp/doctor_test.out
  exit 1
else
  echo "[✓] test_data doctor failed as expected"
fi

echo
echo "=== verifying output ==="

if grep -q '"message": "doctor.check.fail"' /tmp/doctor_test.out \
  && grep -q '"session": "malformed_bad_session"' /tmp/doctor_test.out; then
  echo "[✓] malformed session detected"
else
  echo "[✗] malformed session NOT detected"
  cat /tmp/doctor_test.out
  exit 1
fi

if grep -q '"message": "doctor.check.ok"' /tmp/doctor_test.out \
  && grep -q '"session": "valid_default"' /tmp/doctor_test.out; then
  echo "[✓] valid sessions still processed"
else
  echo "[✗] valid sessions NOT processed"
  cat /tmp/doctor_test.out
  exit 1
fi

echo
echo "[✓] doctor test passed"
