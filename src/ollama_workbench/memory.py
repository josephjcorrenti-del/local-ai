from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from ollama_workbench.config import CONFIG
from ollama_workbench.paths import paths_get


def session_path_get(session_name: str | None = None) -> Path:
    name = session_name or CONFIG.default_session_name
    sessions_dir = paths_get().sessions_dir
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir / f"{name}.json"


def session_load(session_name: str | None = None) -> list[dict[str, Any]]:
    path = session_path_get(session_name)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        return []

    return data


def session_save(
    messages: list[dict[str, Any]],
    session_name: str | None = None,
) -> None:
    path = session_path_get(session_name)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(messages, fh, indent=2)


def session_turns_get(session_name: str | None = None) -> list[dict[str, str]]:
    raw = session_load(session_name)
    turns: list[dict[str, str]] = []

    for item in raw[-CONFIG.memory_turn_limit:]:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant", "system"} and isinstance(content, str):
            turns.append({"role": role, "content": content})

    return turns


def session_append(role: str, content: str, session_name: str | None = None) -> None:
    messages = session_load(session_name)
    messages.append(
        {
            "role": role,
            "content": content,
            "timestamp_utc": datetime.now(UTC).isoformat(),
        }
    )
    session_save(messages, session_name)


def session_clear(session_name: str | None = None) -> None:
    path = session_path_get(session_name)
    if path.exists():
        path.unlink()


def session_names_get() -> list[str]:
    sessions_dir = paths_get().sessions_dir
    if not sessions_dir.exists():
        return []

    names: list[str] = []
    for path in sessions_dir.glob("*.json"):
        names.append(path.stem)

    return sorted(names)


def session_stats_get(session_name: str) -> dict[str, Any]:
    path = session_path_get(session_name)

    if not path.exists():
        return {"session": session_name, "exists": False}

    data = session_load(session_name)
    file_size = path.stat().st_size

    total_messages = len(data)
    total_chars = sum(len(m.get("content", "")) for m in data)

    user_count = sum(1 for m in data if m.get("role") == "user")
    assistant_count = sum(1 for m in data if m.get("role") == "assistant")

    last_ts = data[-1].get("timestamp_utc") if data else None
    avg_len = total_chars // total_messages if total_messages else 0

    return {
        "session": session_name,
        "exists": True,
        "file_size_bytes": file_size,
        "messages": total_messages,
        "turns_est": min(user_count, assistant_count),
        "user_messages": user_count,
        "assistant_messages": assistant_count,
        "total_chars": total_chars,
        "avg_message_len": avg_len,
        "last_updated": last_ts,
    }


def sessions_summary_get() -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for name in session_names_get():
        summaries.append(session_stats_get(name))
    return summaries
