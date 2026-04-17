#!/usr/bin/env bash
set -euo pipefail

echo "=== ollama_workbench init ==="

if [ ! -d ".venv" ]; then
  echo "[*] creating virtual environment"
  python3 -m venv .venv
else
  echo "[*] virtual environment already exists"
fi

echo "[*] activating virtual environment"
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[*] upgrading pip"
python -m pip install --upgrade pip

echo "[*] installing project (editable)"
python -m pip install -e .

echo "[✓] ready: use 'ollama-workbench'"

if command -v ollama-workbench >/dev/null 2>&1; then
  echo "[✓] CLI available"
else
  echo "[!] CLI not found"
fi
