from __future__ import annotations


PING_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "model": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": ["status", "model", "summary"],
    "additionalProperties": False,
}
