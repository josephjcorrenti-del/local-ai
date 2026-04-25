from __future__ import annotations

"""
ollama_workbench/output.py

Small helpers for human-facing CLI output.

This module owns terminal presentation details such as color and status markers.
Structured logging stays in log.py.
"""

import sys
import os

USE_COLOR = sys.stdout.isatty() or os.environ.get("OWB_FORCE_COLOR") == "1"


def color_green(text: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[32m{text}\033[0m"


def color_red(text: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[31m{text}\033[0m"


def color_yellow(text: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[33m{text}\033[0m"


def ok(message: str) -> None:
    print(f"{color_green('[✓]')} {message}")


def fail(message: str) -> None:
    print(f"{color_red('[✗]')} {message}", file=sys.stderr)


def warn(message: str) -> None:
    print(f"{color_yellow('[!]')} {message}")


def info(message: str) -> None:
    print(f"[*] {message}")
