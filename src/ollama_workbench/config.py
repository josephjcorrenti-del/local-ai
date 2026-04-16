from __future__ import annotations

"""
ollama_workbench/config.py

Central configuration for the application.

Responsibilities:
- Define all runtime configuration values in one place
- Provide a single immutable config object (CONFIG)
- Keep configuration explicit and inspectable (no env-driven overrides yet)

Design notes:
- Uses a frozen dataclass to prevent mutation at runtime
- Separates "roles" of models:
  - lightweight_model_name: cheaper / smaller tasks (summarization)
  - large_model_name: primary chat / reasoning model
- Paths are defined relative to a single ai_root to keep runtime data separate from repo code
- Defaults favor local, explicit behavior over flexibility
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration values used across modules."""
    app_name: str = "ollama_workbench"

    ollama_base_url: str = "http://127.0.0.1:11434"
    request_timeout_s: int = 120

    lightweight_model_name: str = "phi3:mini"
    large_model_name: str = "qwen2.5-coder:3b"

    ai_start_script_name: str = "ai_start.sh"
    ai_status_script_name: str = "ai_status.sh"

    ai_root: Path = Path.home() / "ai"
    data_root: Path = ai_root / "data"

    default_session_name: str = "default"
    memory_turn_limit: int = 8

    chat_model_name: str = large_model_name
    summary_model_name: str = lightweight_model_name

    summary_keep_recent_messages: int = 8
    summary_max_input_messages: int = 12
    summary_inactive_minutes: int = 30
    summary_max_input_chars: int = 600


CONFIG = AppConfig()
