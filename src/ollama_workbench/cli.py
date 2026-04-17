from __future__ import annotations

"""
ollama_workbench/cli.py

Primary CLI entrypoint and command router.

Responsibilities:
- Define CLI commands and argument parsing (argparse)
- Route commands to small handler functions
- Keep handlers thin and explicit (no hidden behavior)
- Coordinate between runtime, memory, tools, and web modules
- Emit command-level logging (start / end / error)

Design notes:
- CLI is intentionally "flat": each command maps to one handler
- Business logic lives in other modules (runtime, memory, web)
- Output is a mix of:
  - human-readable CLI output (print)
  - machine-readable logs (log_event)
- No background behavior: all actions are explicit per command
"""

import argparse
import json
import os
from typing import Callable
import sys

from ollama_workbench.config import CONFIG
from ollama_workbench.log import log_event
from ollama_workbench.memory import (
    session_append,
    session_clear,
    session_load,
    session_names_get,
    session_stats_get,
    session_summarize,
    session_turns_get,
    sessions_stats_get,
)
from ollama_workbench.paths import paths_get
from ollama_workbench.runtime import (
    ai_status_show,
    ollama_chat,
    ollama_ensure_running,
    ollama_is_healthy,
    ollama_model_ensure_available,
)
from ollama_workbench.schemas import PING_SCHEMA
from ollama_workbench.tools import TOOL_DEFS, TOOL_REGISTRY
from ollama_workbench.web import web_fetch, web_artifact_load, web_cleanup


def prompt_run(user_prompt: str) -> None:
    """Run a one-off prompt against the local model."""
    ollama_ensure_running()

    payload = {
        "model": CONFIG.chat_model_name,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a concise local assistant. "
                    "Answer clearly and directly."
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
    }

    result = ollama_chat(payload)
    print(result["message"]["content"])


def json_run() -> None:
    """Run a structured JSON response test using the local model."""
    ollama_ensure_running()

    payload = {
        "model": CONFIG.chat_model_name,
        "stream": False,
        "format": PING_SCHEMA,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Return valid JSON only. "
                    "Do not include markdown fences."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Return a short health summary for this local stack. "
                    "Set status=ok, model to the active model name, "
                    "and summary to one sentence."
                ),
            },
        ],
    }

    result = ollama_chat(payload)
    content = result["message"]["content"]
    parsed = json.loads(content)
    print(json.dumps(parsed, indent=2))


# WHY:
# Tool-calling is kept as an explicit demo/test flow. The CLI shows the tool
# request, executes the selected local tool, and feeds the result back to the
# model so the full interaction stays visible and inspectable.
def tool_run(path: str) -> None:
    """Demonstrate tool-calling by listing and summarizing a directory."""
    ollama_ensure_running()

    messages = [
        {
            "role": "system",
            "content": (
                "You may use tools when helpful. "
                "If the user asks about local files, call the directory_list tool. "
                "Do not describe the tool call in prose. "
                "Prefer returning an actual tool call."
            ),
        },
        {
            "role": "user",
            "content": f"List the contents of this directory and summarize it: {path}",
        },
    ]

    first = ollama_chat(
        {
            "model": CONFIG.chat_model_name,
            "stream": False,
            "messages": messages,
            "tools": TOOL_DEFS,
        }
    )

    assistant_message = first["message"]
    messages.append(assistant_message)

    tool_calls = assistant_message.get("tool_calls", [])

    if not tool_calls:
        content = assistant_message.get("content", "").strip()

        try:
            parsed_tool = json.loads(content)
        except json.JSONDecodeError:
            parsed_tool = None

        if (
            isinstance(parsed_tool, dict)
            and "name" in parsed_tool
            and "arguments" in parsed_tool
            and isinstance(parsed_tool["arguments"], dict)
        ):
            tool_calls = [
                {
                    "function": {
                        "name": parsed_tool["name"],
                        "arguments": parsed_tool["arguments"],
                    }
                }
            ]
        else:
            print("[!] Model did not call a tool")
            print(content)
            return

    for tool_call in tool_calls:
        fn = tool_call["function"]["name"]
        args = tool_call["function"]["arguments"]

        print(f"[*] Executing tool: {fn}({args})")

        tool_fn = TOOL_REGISTRY[fn]
        tool_result = tool_fn(**args)

        print("[*] Tool result:")
        print(json.dumps(tool_result, indent=2))

        messages.append(
            {
                "role": "tool",
                "name": fn,
                "content": json.dumps(tool_result),
            }
        )

    messages.append(
        {
            "role": "system",
            "content": (
                "You have already received the tool result. "
                "Do not call any more tools. "
                "Summarize the directory contents for the user."
            ),
        }
    )

    final = ollama_chat(
        {
            "model": CONFIG.chat_model_name,
            "stream": False,
            "messages": messages,
        }
    )

    print("\n[*] Final answer:")
    print(final["message"]["content"])


def chat_run(user_prompt: str, session_name: str | None = None) -> None:
    """Run chat with optional session memory persistence."""
    ollama_ensure_running()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise local assistant. "
                "Help with general questions, coding, debugging, and technical reasoning. "
                "Be practical and direct."
            ),
        }
    ]

    messages.extend(session_turns_get(session_name))
    messages.append({"role": "user", "content": user_prompt})

    payload = {
        "model": CONFIG.chat_model_name,
        "stream": False,
        "messages": messages,
    }

    result = ollama_chat(payload)
    answer = result["message"]["content"]

    print(answer)

    session_append("user", user_prompt, session_name)
    session_append("assistant", answer, session_name)


def clear_run(session_name: str | None = None) -> None:
    """Clear stored messages for a session."""
    session_clear(session_name)
    print("[✓] Session cleared")


def prompt_command_run(args: argparse.Namespace) -> None:
    prompt_run(args.text)


def json_command_run(args: argparse.Namespace) -> None:
    json_run()


def tool_command_run(args: argparse.Namespace) -> None:
    tool_run(args.path)


def chat_command_run(args: argparse.Namespace) -> None:
    chat_run(args.text, args.session)


def clear_command_run(args: argparse.Namespace) -> None:
    clear_run(args.session)


def sessions_command_run(args: argparse.Namespace) -> None:
    del args
    for name in session_names_get():
        print(name)


def stats_command_run(args: argparse.Namespace) -> None:
    if args.session:
        print(json.dumps(session_stats_get(args.session), indent=2))
        return

    print(json.dumps(sessions_stats_get(), indent=2))


def summarize_command_run(args: argparse.Namespace) -> None:
    session_name = args.session or CONFIG.default_session_name
    session_summarize(session_name)
    print("[✓] Session summarized")


def status_command_run(args: argparse.Namespace) -> None:
    """Display runtime configuration and system status."""
    del args

    paths = paths_get()

    print(f"app: {CONFIG.app_name}")
    print()

    print("runtime:")
    print(f"  ollama_base_url: {CONFIG.ollama_base_url}")
    print(f"  ollama_healthy: {'yes' if ollama_is_healthy() else 'no'}")
    print(f"  chat_model: {CONFIG.chat_model_name}")
    print(f"  summary_model: {CONFIG.summary_model_name}")
    print()

    print("paths:")
    print(f"  repo_root: {paths.repo_root}")
    print(f"  app_data_root: {paths.app_data_root}")
    print(f"  sessions_dir: {paths.sessions_dir}")
    print()

    print("system:")
    ai_status_show()


USE_COLOR = sys.stdout.isatty()


def _green(text: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[32m{text}\033[0m"


def _red(text: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[31m{text}\033[0m"


def _doctor_ok(message: str) -> None:
    print(f"{_green('[✓]')} {message}")


def _doctor_fail(message: str) -> None:
    print(f"{_red('[✗]')} {message}")


def doctor_command_run(args: argparse.Namespace) -> None:
    """Run local runtime checks and report failures."""
    del args

    paths = paths_get()
    failures = 0
    checks_run = 0

    if ollama_is_healthy():
        log_event("doctor.check.ok", command="doctor")
        _doctor_ok("ollama reachable")
        checks_run += 1
    else:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            error="ollama not reachable",
        )
        _doctor_fail("ollama not reachable")
        failures += 1

    try:
        ollama_model_ensure_available(CONFIG.chat_model_name)
        log_event(
            "doctor.check.ok",
            command="doctor",
            model=CONFIG.chat_model_name,
        )
        _doctor_ok(f"chat model available ({CONFIG.chat_model_name})")
        checks_run += 1
    except RuntimeError:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            model=CONFIG.chat_model_name,
            error=f"chat model missing ({CONFIG.chat_model_name})",
        )
        _doctor_fail(f"chat model missing ({CONFIG.chat_model_name})")
        print(f"    run: ollama pull {CONFIG.chat_model_name}")
        failures += 1

    try:
        ollama_model_ensure_available(CONFIG.summary_model_name)
        log_event(
            "doctor.check.ok",
            command="doctor",
            model=CONFIG.summary_model_name,
        )
        _doctor_ok(f"summary model available ({CONFIG.summary_model_name})")
        checks_run += 1
    except RuntimeError:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            model=CONFIG.summary_model_name,
            error=f"summary model missing ({CONFIG.summary_model_name})",
        )
        _doctor_fail(f"summary model missing ({CONFIG.summary_model_name})")
        print(f"    run: ollama pull {CONFIG.summary_model_name}")
        failures += 1

    try:
        paths.sessions_dir.mkdir(parents=True, exist_ok=True)
        test_path = paths.sessions_dir / ".doctor_write_test"
        test_path.write_text("ok\n", encoding="utf-8")
        test_path.unlink()
        log_event(
            "doctor.check.ok",
            command="doctor",
            path=str(paths.sessions_dir),
        )
        _doctor_ok(f"sessions dir writable ({paths.sessions_dir})")
        checks_run += 1
    except OSError as exc:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            path=str(paths.sessions_dir),
            error=str(exc),
        )
        _doctor_fail(f"sessions dir not writable ({paths.sessions_dir})")
        print(f"    reason: {exc}")
        failures += 1

    for session_name in session_names_get():
        checks_run += 1
        try:
            session_load(session_name)
            log_event(
                "doctor.check.ok",
                command="doctor",
                session=session_name,
            )
            _doctor_ok(f"session load ok ({session_name})")
        except RuntimeError as exc:
            log_event(
                "doctor.check.fail",
                level="error",
                command="doctor",
                session=session_name,
                error=str(exc),
            )
            _doctor_fail(f"session file malformed ({session_name})")
            print("    guidance: fix or delete the session file")
            failures += 1

    checks_run += 1
    try:
        paths.app_data_root.mkdir(parents=True, exist_ok=True)
        test_path = paths.app_data_root / ".doctor_write_test"
        test_path.write_text("ok\n", encoding="utf-8")
        test_path.unlink()
        log_event(
            "doctor.check.ok",
            command="doctor",
            path=str(paths.app_data_root),
        )
        _doctor_ok(f"app data root writable ({paths.app_data_root})")
    except OSError as exc:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            path=str(paths.app_data_root),
            error=str(exc),
        )
        _doctor_fail(f"app data root not writable ({paths.app_data_root})")
        print(f"    reason: {exc}")
        failures += 1

    checks_run += 1
    try:
        paths.web_dir.mkdir(parents=True, exist_ok=True)
        test_path = paths.web_dir / ".doctor_write_test"
        test_path.write_text("ok\n", encoding="utf-8")
        test_path.unlink()
        log_event(
            "doctor.check.ok",
            command="doctor",
            path=str(paths.web_dir),
        )
        _doctor_ok(f"web dir writable ({paths.web_dir})")
    except OSError as exc:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            path=str(paths.web_dir),
            error=str(exc),
        )
        _doctor_fail(f"web dir not writable ({paths.web_dir})")
        print(f"    reason: {exc}")
        failures += 1

    checks_run += 1
    script = paths.ai_start_script

    if script.exists() and script.is_file() and os.access(script, os.X_OK):
        log_event("doctor.check.ok", command="doctor", path=str(script))
        _doctor_ok(f"helper script ok ({script.name})")
    else:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            path=str(script),
            error="missing or not executable",
        )
        _doctor_fail(f"helper script not runnable ({script.name})")
        print(f"    expected: executable file at {script}")
        failures += 1

    checks_run += 1
    script = paths.ai_status_script

    if script.exists() and script.is_file() and os.access(script, os.X_OK):
        log_event("doctor.check.ok", command="doctor", path=str(script))
        _doctor_ok(f"helper script ok ({script.name})")
    else:
        log_event(
            "doctor.check.fail",
            level="error",
            command="doctor",
            path=str(script),
            error="missing or not executable",
        )
        _doctor_fail(f"helper script not runnable ({script.name})")
        print(f"    expected: executable file at {script}")
        failures += 1

    print()
    print(f"checks run: {checks_run}")
    print(f"failures: {failures}")

    log_event(
        "doctor.summary",
        command="doctor",
        error=None if failures == 0 else f"{failures} failing check(s)",
    )

    if failures:
        raise RuntimeError(f"doctor found {failures} failing check(s)")


def web_fetch_command_run(args: argparse.Namespace) -> None:
    """Fetch a URL and display a preview of the stored artifact."""
    artifact = web_fetch(args.url)

    print(f"url: {artifact['url']}")
    print(f"fetched_at: {artifact['fetched_at']}")
    print(f"title: {artifact.get('title') or '(none)'}")
    print(f"artifact_path: {artifact['artifact_path']}")
    print()

    content_text = artifact.get("content_text", "")
    preview = content_text[:500]
    if len(content_text) > 500:
        preview += "..."

    print(preview)


def web_chat_command_run(args: argparse.Namespace) -> None:
    """Answer a question using content from a single fetched URL."""
    artifact = web_fetch(args.url)
    content_text = artifact.get("content_text", "")

    prompt = (
        f"Question: {args.question}\n\n"
        f"URL: {artifact['url']}\n"
        f"Title: {artifact.get('title') or '(none)'}\n\n"
        f"Page content:\n{content_text}"
    )

    ollama_ensure_running()

    payload = {
        "model": CONFIG.chat_model_name,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the provided web page content. "
                    "Be concise and say when the page does not contain enough information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    result = ollama_chat(payload)
    answer = result["message"]["content"]

    print(f"url: {artifact['url']}")
    print(f"artifact_path: {artifact['artifact_path']}")
    print()
    print(answer)


def web_cleanup_command_run(args: argparse.Namespace) -> None:
    """List or delete old web artifacts."""
    removed = web_cleanup(args.days, args.delete)

    if not removed:
        print("No old web artifacts found.")
        return

    action = "Deleting" if args.delete else "Would delete"
    print(f"{action} {len(removed)} artifact(s):")

    for path in removed:
        print(f"  {path}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "prompt": prompt_command_run,
    "json": json_command_run,
    "tool": tool_command_run,
    "chat": chat_command_run,
    "clear": clear_command_run,
    "sessions": sessions_command_run,
    "stats": stats_command_run,
    "status": status_command_run,
    "summarize": summarize_command_run,
    "doctor": doctor_command_run,
    "web-fetch": web_fetch_command_run,
    "web-chat": web_chat_command_run,
    "web-cleanup": web_cleanup_command_run,
}


def parser_build() -> argparse.ArgumentParser:
    """Construct and return the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Ollama Workbench local CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_prompt = subparsers.add_parser("prompt", help="Run a plain prompt")
    p_prompt.add_argument("text", help="Prompt text")

    subparsers.add_parser("json", help="Run structured JSON test")

    p_tool = subparsers.add_parser("tool", help="Run tool-calling test")
    p_tool.add_argument("path", help="Path for directory_list tool")


    p_chat = subparsers.add_parser("chat", help="Run chat with session memory")
    p_chat.add_argument("text", help="Chat prompt text")
    p_chat.add_argument("--session", default=None, help="Session name")

    p_clear = subparsers.add_parser("clear", help="Clear session memory")
    p_clear.add_argument("--session", default=None, help="Session name")

    subparsers.add_parser("sessions", help="List sessions")

    p_stats = subparsers.add_parser("stats", help="Show session stats")
    p_stats.add_argument("--session", default=None, help="Session name")

    subparsers.add_parser("status", help="Show AI runtime status")

    p_summarize = subparsers.add_parser("summarize", help="Summarize a session")
    p_summarize.add_argument("--session", default=None, help="Session name")

    subparsers.add_parser("doctor", help="Run local runtime checks")

    p_web_fetch = subparsers.add_parser(
        "web-fetch",
        help="Fetch one explicit URL and save a web artifact",
    )
    p_web_fetch.add_argument("url", help="URL to fetch")

    p_web_chat = subparsers.add_parser(
        "web-chat",
        help="Answer a question using one explicit fetched URL",
    )
    p_web_chat.add_argument("question", help="Question to answer")
    p_web_chat.add_argument("--url", required=True, help="URL to fetch and use")

    p_web_cleanup = subparsers.add_parser(
        "web-cleanup",
        help="Clean up old web artifacts",
    )
    p_web_cleanup.add_argument(
        "--days",
        type=int,
        default=7,
        help="Remove artifacts older than N days (default: 7)",
    )
    p_web_cleanup.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete files (default: dry run)",
    )

    return parser


# WHY:
# main() is the CLI boundary for argument parsing, command dispatch, and
# command-level logging. This keeps one clear entrypoint where cross-cutting
# concerns like logging and later top-level error handling can live.
def main() -> None:
    """Parse arguments, dispatch the command, and handle top-level logging."""
    parser = parser_build()
    args = parser.parse_args()

    command = args.command
    handler = COMMAND_HANDLERS.get(command)

    if handler is None:
        raise RuntimeError(f"Unknown command: {command}")

    log_event(
        "command.start",
        command=command,
    )

    try:
        handler(args)
    except Exception as exc:
        log_event(
            "command.error",
            level="error",
            command=command,
            error=str(exc),
        )

        print(f"[!] error: {exc}", file=sys.stderr)
        sys.exit(1)

    log_event(
        "command.end",
        command=command,
    )


if __name__ == "__main__":
    main()
