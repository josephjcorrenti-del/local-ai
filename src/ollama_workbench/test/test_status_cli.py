from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")

    return subprocess.run(
        [sys.executable, "-m", "ollama_workbench.cli", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def test_status_uses_default_data_dir():
    result = run_cli("status")

    assert result.returncode == 0
    assert "app: ollama_workbench" in result.stdout
    assert "app_data_root: /home/joe/ai/data/ollama_workbench" in result.stdout
    assert "sessions_dir: /home/joe/ai/data/ollama_workbench/sessions" in result.stdout


def test_status_uses_test_data_dir():
    result = run_cli("--data-dir", "test_data", "status")

    assert result.returncode == 0
    assert "app: ollama_workbench" in result.stdout
    assert "app_data_root: /home/joe/ai/test_data/ollama_workbench" in result.stdout
    assert "sessions_dir: /home/joe/ai/test_data/ollama_workbench/sessions" in result.stdout
