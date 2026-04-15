#!/usr/bin/env bash
set -e

if systemctl is-active --quiet docker; then
  echo "[=] docker already running"
else
  echo "[+] starting docker"
  sudo systemctl start docker
fi
