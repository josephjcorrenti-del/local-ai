#!/usr/bin/env bash
set -euo pipefail

echo "=== local_ai init ==="

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

echo "[✓] ready: use 'local-ai'"

if command -v local-ai >/dev/null 2>&1; then
  echo "[✓] CLI available"
else
  echo "[!] CLI not found"
fi
