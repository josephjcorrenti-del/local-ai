from __future__ import annotations

import json
import subprocess
import time
import urllib.error
import urllib.request

from ollama_workbench.config import CONFIG


def ollama_version_get() -> dict[str, object]:
    url = f"{CONFIG.ollama_base_url}/api/version"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ollama_is_healthy() -> bool:
    try:
        _ = ollama_version_get()
        return True
    except Exception:
        return False


def ai_stack_start() -> None:
    subprocess.run(
        [str(CONFIG.ai_start_script)],
        check=True,
        text=True,
    )


def ai_status_show() -> None:
    subprocess.run(
        [str(CONFIG.ai_status_script)],
        check=False,
        text=True,
    )


def ollama_ensure_running() -> None:
    if ollama_is_healthy():
        return

    print("[*] Ollama not healthy. Starting AI stack...")
    ai_stack_start()

    for _ in range(20):
        if ollama_is_healthy():
            print("[✓] Ollama is healthy")
            return
        time.sleep(1)

    raise RuntimeError("Ollama did not become healthy after startup")


def ollama_chat(payload: dict[str, object]) -> dict[str, object]:
    url = f"{CONFIG.ollama_base_url}/api/chat"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=CONFIG.request_timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP error {exc.code}: {body}") from exc


def ollama_generate(prompt: str) -> str:
    url = f"{CONFIG.ollama_base_url}/api/generate"

    payload = {
        "model": CONFIG.chat_model_name,
        "prompt": prompt,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=CONFIG.request_timeout_s) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP error {exc.code}: {body}") from exc
