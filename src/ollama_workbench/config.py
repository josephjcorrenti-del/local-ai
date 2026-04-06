from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    app_name: str = "ollama_workbench"

    ollama_base_url: str = "http://127.0.0.1:11434"
    model_name: str = "qwen2.5-coder:3b"
    request_timeout_s: int = 120

    scripts_dir: Path = Path.home() / "scripts"
    ai_start_script: Path = scripts_dir / "ai_start.sh"
    ai_status_script: Path = scripts_dir / "ai_status.sh"

    ai_root: Path = Path.home() / "ai"
    data_root: Path = ai_root / "data"

    default_session_name: str = "default"
    memory_turn_limit: int = 8


CONFIG = AppConfig()
