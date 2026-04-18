#!/usr/bin/env bash
set -euo pipefail

FIXTURE_ROOT="$HOME/ai/test_data/ollama_workbench"
SESSIONS_DIR="$FIXTURE_ROOT/sessions"

echo "=== fixture directory ==="
if [[ -d "$SESSIONS_DIR" ]]; then
  echo "[✓] sessions fixture dir exists: $SESSIONS_DIR"
else
  echo "[✗] sessions fixture dir missing: $SESSIONS_DIR"
  exit 1
fi

required_files=(
  "valid_default.json"
  "malformed_bad_session.json"
  "legacy_list_session.json"
  "summarized_session.json"
  "empty_messages_session.json"
)

echo
echo "=== required fixture files ==="
for file in "${required_files[@]}"; do
  if [[ -f "$SESSIONS_DIR/$file" ]]; then
    echo "[✓] found $file"
  else
    echo "[✗] missing $file"
    exit 1
  fi
done

echo
echo "=== malformed fixture check ==="
if python3 - << 'PY'
import json
from pathlib import Path

path = Path.home() / "ai" / "test_data" / "ollama_workbench" / "sessions" / "malformed_bad_session.json"

try:
    json.loads(path.read_text(encoding="utf-8"))
except json.JSONDecodeError:
    raise SystemExit(0)

raise SystemExit(1)
PY
then
  echo "[✓] malformed_bad_session.json is still malformed"
else
  echo "[✗] malformed_bad_session.json is no longer malformed"
  exit 1
fi

echo
echo "[✓] fixture check passed"
