from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ollama_workbench.config import CONFIG


@dataclass(frozen=True)
class AppPaths:
    repo_root: Path
    src_root: Path
    package_root: Path
    ai_root: Path
    data_root: Path
    app_data_root: Path
    sessions_dir: Path


def paths_get() -> AppPaths:
    package_root = Path(__file__).resolve().parent
    src_root = package_root.parent
    repo_root = src_root.parent

    ai_root = CONFIG.ai_root
    data_root = CONFIG.data_root
    app_data_root = data_root / CONFIG.app_name
    sessions_dir = app_data_root / "sessions"

    return AppPaths(
        repo_root=repo_root,
        src_root=src_root,
        package_root=package_root,
        ai_root=ai_root,
        data_root=data_root,
        app_data_root=app_data_root,
        sessions_dir=sessions_dir,
    )
