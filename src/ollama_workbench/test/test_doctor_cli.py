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


def test_doctor_passes_on_normal_data():
    result = run_cli("doctor")

    assert result.returncode == 0
    assert "checks run:" in result.stdout
    assert "failures: 0" in result.stdout
    assert "[✓] helper script ok (ai_status.sh)" in result.stdout


def test_doctor_uses_test_data_sessions_dir():
    result = run_cli("--data-dir", "test_data", "doctor")

    expected_sessions_dir = Path.home() / "ai" / "test_data" / "ollama_workbench" / "sessions"

    assert f"sessions dir writable ({expected_sessions_dir})" in result.stdout


def test_doctor_reports_aggregate_failure_cleanly_when_test_data_fails():
    result = run_cli("--data-dir", "test_data", "doctor")

    assert result.returncode != 0
    assert "checks run:" in result.stdout
    assert "failures:" in result.stdout
    assert "[!] error:" in result.stderr
