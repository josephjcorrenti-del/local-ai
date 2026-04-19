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


def test_doctor_runs_and_reports_summary():
    result = run_cli("doctor")

    assert "checks run:" in result.stdout
    assert "failures:" in result.stdout


def test_doctor_accepts_test_data_dir_flag():
    result = run_cli("--data-dir", "test_data", "doctor")

    assert "checks run:" in result.stdout
    assert "failures:" in result.stdout


def test_doctor_failure_is_reported_cleanly():
    result = run_cli("doctor")

    if result.returncode != 0:
        assert "[!] error:" in result.stderr
