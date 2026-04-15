#!/usr/bin/env bash
set -e

echo "[*] restarting AI stack"
~/scripts/ai_stop.sh
~/scripts/ai_start.sh
~/scripts/ai_status.sh
