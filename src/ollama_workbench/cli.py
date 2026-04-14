from __future__ import annotations

import argparse
import json
from typing import Callable

from ollama_workbench.config import CONFIG
from ollama_workbench.memory import (
    session_append,
    session_clear,
    session_names_get,
    session_stats_get,
    session_summarize,
    session_turns_get,
    sessions_stats_get,
)
from ollama_workbench.runtime import (
    ai_status_show,
    ollama_chat,
    ollama_ensure_running,
)
from ollama_workbench.schemas import PING_SCHEMA
from ollama_workbench.tools import TOOL_DEFS, TOOL_REGISTRY


def prompt_run(user_prompt: str) -> None:
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


def tool_run(path: str) -> None:
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


def status_command_run(args: argparse.Namespace) -> None:
    del args
    ai_status_show()


def summarize_command_run(args: argparse.Namespace) -> None:
    session_name = args.session or CONFIG.default_session_name
    session_summarize(session_name)
    print("[✓] Session summarized")


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
}


def parser_build() -> argparse.ArgumentParser:
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

    return parser


def main() -> None:
    parser = parser_build()
    args = parser.parse_args()

    command = args.command
    handler = COMMAND_HANDLERS.get(command)

    if handler is None:
        raise RuntimeError(f"Unknown command: {command}")

    handler(args)


if __name__ == "__main__":
    main()
