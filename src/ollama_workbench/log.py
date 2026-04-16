from __future__ import annotations

"""
ollama_workbench/log.py

Minimal structured logging helper.

Responsibilities:
- Emit one JSON object per line (NDJSON)
- Keep logs stdout-first and immediately inspectable
- Provide a stable, flat event shape for traceability

Design constraints:
- No file logging, batching, or async behavior
- No hidden configuration or environment-driven behavior
- Allow null fields in first pass where values are not yet defined
- Keep event structure simple and easy to extend later (ELK phase)

Old lab-style NDJSON reference (kept briefly during transition):
# {
#   "ts": "...",
#   "level": "INFO",
#   "module": "...",
#   "logger": "...",
#   "message": "...",
#   "run_id": "...",
#   "event": "...",
#   "fn": "...",
#   "elapsed_ms": 12,
#   "params": {...},
#   "detail": {...}
# }

Current ollama_workbench event shape:
# {
#   "ts": "2026-04-15T20:10:00Z",
#   "level": "info",
#   "event": "ollama.ensure_running.start",
#   "command": "chat",
#   "session": "scratch",
#   "model": null,
#   "path": null,
#   "url": null,
#   "error": null
# }
"""

from datetime import UTC, datetime
import json
from typing import Any


def log_timestamp_now_get() -> str:
    """Return current UTC timestamp in log format."""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_event(
    event: str,
    *,
    level: str = "info",
    command: str | None = None,
    session: str | None = None,
    model: str | None = None,
    path: str | None = None,
    url: str | None = None,
    error: str | None = None,
) -> None:
    """Emit one structured log event as a single JSON line to stdout."""
    payload: dict[str, Any] = {
        "ts": log_timestamp_now_get(),
        "level": level,
        "event": event,
        "command": command,
        "session": session,
        "model": model,
        "path": path,
        "url": url,
        "error": error,
    }

    print(json.dumps(payload, ensure_ascii=False))
