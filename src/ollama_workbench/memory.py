from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ollama_workbench.config import CONFIG
from ollama_workbench.paths import paths_get
from ollama_workbench.runtime import ollama_generate, ollama_ensure_running


def timestamp_now_get() -> str:
    return datetime.now(UTC).isoformat()


def session_path_get(session_name: str | None = None) -> Path:
    name = session_name or CONFIG.default_session_name
    sessions_dir = paths_get().sessions_dir
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir / f"{name}.json"


def session_empty_get(session_name: str | None = None) -> dict[str, Any]:
    name = session_name or CONFIG.default_session_name
    now = timestamp_now_get()

    return {
        "session": name,
        "created_at": now,
        "updated_at": now,
        "summary": None,
        "messages": [],
    }


def session_normalize(
    data: Any,
    session_name: str | None = None,
) -> dict[str, Any]:
    name = session_name or CONFIG.default_session_name

    if isinstance(data, dict):
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            messages = []

        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        summary = data.get("summary")

        if created_at is None:
            created_at = _messages_first_timestamp_get(messages)
        if updated_at is None:
            updated_at = _messages_last_timestamp_get(messages)

        return {
            "session": data.get("session", name),
            "created_at": created_at,
            "updated_at": updated_at,
            "summary": summary,
            "messages": messages,
        }

    if isinstance(data, list):
        return {
            "session": name,
            "created_at": _messages_first_timestamp_get(data),
            "updated_at": _messages_last_timestamp_get(data),
            "summary": None,
            "messages": data,
        }

    return session_empty_get(name)


def session_load(session_name: str | None = None) -> dict[str, Any]:
    path = session_path_get(session_name)
    if not path.exists():
        return session_empty_get(session_name)

    with path.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)

    return session_normalize(raw, session_name)


def session_save(
    session_data: dict[str, Any],
    session_name: str | None = None,
) -> None:
    normalized = session_normalize(session_data, session_name)

    if normalized["created_at"] is None:
        normalized["created_at"] = timestamp_now_get()

    normalized["updated_at"] = timestamp_now_get()

    path = session_path_get(session_name)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(normalized, fh, indent=2)


def session_turns_get(session_name: str | None = None) -> list[dict[str, str]]:
    session_data = session_load(session_name)
    raw_messages = session_data["messages"]
    turns: list[dict[str, str]] = []

    for item in raw_messages[-CONFIG.memory_turn_limit:]:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant", "system"} and isinstance(content, str):
            turns.append({"role": role, "content": content})

    return turns


def session_append(role: str, content: str, session_name: str | None = None) -> None:
    session_data = session_load(session_name)
    session_data["messages"].append(
        {
            "role": role,
            "content": content,
            "timestamp_utc": timestamp_now_get(),
        }
    )
    session_save(session_data, session_name)


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


def session_stats_get(session_name: str) -> dict[str, object]:
    path = session_path_get(session_name)

    if not path.exists():
        return {"session": session_name, "exists": False}

    session_data = session_load(session_name)
    messages = session_data["messages"]
    file_size = path.stat().st_size

    total_messages = len(messages)
    total_chars = sum(len(m.get("content", "")) for m in messages)

    user_count = sum(1 for m in messages if m.get("role") == "user")
    assistant_count = sum(1 for m in messages if m.get("role") == "assistant")

    avg_len = total_chars // total_messages if total_messages else 0

    return {
        "session": session_data["session"],
        "exists": True,
        "file_size_bytes": file_size,
        "messages": total_messages,
        "turns_est": min(user_count, assistant_count),
        "user_messages": user_count,
        "assistant_messages": assistant_count,
        "total_chars": total_chars,
        "avg_message_len": avg_len,
        "created_at": session_data["created_at"],
        "last_updated": session_data["updated_at"],
        "has_summary": session_data["summary"] is not None,
    }


def sessions_stats_get() -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    for name in session_names_get():
        summaries.append(session_stats_get(name))
    return summaries


def _messages_first_timestamp_get(messages: list[dict[str, Any]]) -> str | None:
    for message in messages:
        timestamp = message.get("timestamp_utc")
        if isinstance(timestamp, str):
            return timestamp
    return None


def _messages_last_timestamp_get(messages: list[dict[str, Any]]) -> str | None:
    for message in reversed(messages):
        timestamp = message.get("timestamp_utc")
        if isinstance(timestamp, str):
            return timestamp
    return None

def session_summarize(session_name: str) -> None:
    session_data = session_load(session_name)
    messages = session_data["messages"]

    if not messages:
        return

    keep_n = CONFIG.summary_keep_recent_messages
    recent_messages = messages[-keep_n:]
    older_messages = messages[:-keep_n]
    max_input = CONFIG.summary_max_input_messages
    older_messages = older_messages[-max_input:]


    if not older_messages:
        return  # nothing to summarize

    # Build simple text for summarization input
    lines: list[str] = []
    for m in older_messages:
        role = m.get("role", "unknown")
        content = m.get("content", "")
        if isinstance(content, str):
            #lines.append(f"{role}: {content}")
            lines.append(content)

    #summary_input = "\n".join(lines)
    summary_input = "\n\n".join(lines[-6:])

    max_chars = CONFIG.summary_max_input_chars
    if len(summary_input) > max_chars:
        summary_input = summary_input[-max_chars:]

    # Use ollama to generate summary
    ollama_ensure_running()

    payload: dict[str, object] = {
        "model": CONFIG.summary_model_name,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Summarize the following text briefly."
    ),
            },
            {
                "role": "user",
                "content": summary_input,
            },
        ],
    }

    prompt = f"Summarize the following text briefly:\n\n{summary_input}"

    try:
        summary_text = ollama_generate(prompt)
    except RuntimeError as exc:
        raise RuntimeError(
            f"Session summarize failed for '{session_name}'. "
            "The summarization request may be too large for the current local model/runtime."
        ) from exc

    # Write summary object
    session_data["summary"] = {
        "text": summary_text,
        "updated_at": timestamp_now_get(),
        "source_message_count": len(messages),
    }

    # Keep only recent messages
    session_data["messages"] = recent_messages

    session_save(session_data, session_name)
