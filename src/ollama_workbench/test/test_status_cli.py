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


def test_status_runs_and_prints_core_sections():
    result = run_cli("status")

    assert result.returncode == 0
    assert "app: ollama_workbench" in result.stdout
    assert "runtime:" in result.stdout
    assert "paths:" in result.stdout
    assert "app_data_root:" in result.stdout
    assert "sessions_dir:" in result.stdout
    assert "system:" in result.stdout


def test_status_uses_test_data_dir_when_requested():
    result = run_cli("--data-dir", "test_data", "status")

    expected_app_data_root = Path.home() / "ai" / "test_data" / "ollama_workbench"
    expected_sessions_dir = expected_app_data_root / "sessions"

    assert result.returncode == 0
    assert "app: ollama_workbench" in result.stdout
    assert f"app_data_root: {expected_app_data_root}" in result.stdout
    assert f"sessions_dir: {expected_sessions_dir}" in result.stdout
