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


def test_doctor_fails_on_test_data_malformed_session():
    result = run_cli("--data-dir", "test_data", "doctor")

    assert result.returncode != 0
    assert "session file malformed (malformed_bad_session)" in result.stdout
    assert "session load ok (valid_default)" in result.stdout
    assert "failures: 1" in result.stdout
    assert "[!] error: doctor found 1 failing check(s)" in result.stderr
