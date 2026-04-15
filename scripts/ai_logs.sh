#!/usr/bin/env bash
echo "[*] ollama logs (ctrl+c to stop):"
sudo journalctl -u ollama -f
