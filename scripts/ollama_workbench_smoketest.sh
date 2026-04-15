set -e

echo "=== sessions ==="
PYTHONPATH=src python3 -m ollama_workbench.cli sessions
echo

echo "=== stats ==="
PYTHONPATH=src python3 -m ollama_workbench.cli stats
echo

echo "=== chat ==="
PYTHONPATH=src python3 -m ollama_workbench.cli chat "test"
echo

echo "=== summarize ==="
PYTHONPATH=src python3 -m ollama_workbench.cli summarize --session scratch
echo

echo "=== status ==="
PYTHONPATH=src python3 -m ollama_workbench.cli status
echo

echo "=== doctor ==="
PYTHONPATH=src python3 -m ollama_workbench.cli doctor
echo

echo "=== web-fetch ==="
PYTHONPATH=src python3 -m ollama_workbench.cli web-fetch https://example.com
echo

echo "=== web-chat ==="
PYTHONPATH=src python3 -m ollama_workbench.cli web-chat "test" --url https://example.com
echo

echo "=== web-cleanup (dry run) ==="
PYTHONPATH=src python3 -m ollama_workbench.cli web-cleanup --days 0
echo
