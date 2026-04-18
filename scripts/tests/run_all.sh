#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$SCRIPT_DIR/fixtures_check.sh"
bash "$SCRIPT_DIR/status_test.sh"
bash "$SCRIPT_DIR/doctor_test.sh"
bash "$SCRIPT_DIR/python_tests.sh"
