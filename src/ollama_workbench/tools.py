from __future__ import annotations

from pathlib import Path


def directory_list(path: str) -> dict[str, object]:
    base = Path(path).expanduser().resolve()

    if not base.exists():
        return {"ok": False, "error": f"path does not exist: {base}"}

    if not base.is_dir():
        return {"ok": False, "error": f"path is not a directory: {base}"}

    entries = []
    for child in sorted(base.iterdir(), key=lambda p: p.name.lower()):
        entries.append(
            {
                "name": child.name,
                "type": "dir" if child.is_dir() else "file",
            }
        )

    return {
        "ok": True,
        "path": str(base),
        "entries": entries[:50],
    }


TOOL_REGISTRY = {
    "directory_list": directory_list,
}


TOOL_DEFS = [
    {
        "type": "function",
        "function": {
            "name": "directory_list",
            "description": "List files and directories at a local path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute or home-relative directory path",
                    }
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
    }
]
