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


def test_migrate_dry_run_runs():
    result = run_cli(
        "--data-dir", "test_data",
        "migrate",
        "--session", "valid_default",
        "--dry-run",
    )

    assert result.returncode == 0
    assert "Would migrate" in result.stdout
