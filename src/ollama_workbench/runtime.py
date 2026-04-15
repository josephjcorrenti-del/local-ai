from __future__ import annotations

import json
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any

from ollama_workbench.config import CONFIG


def _ollama_get(path: str) -> dict[str, Any]:
    url = f"{CONFIG.ollama_base_url}{path}"
    req = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=CONFIG.request_timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP error {exc.code}: {body}") from exc


def _ollama_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{CONFIG.ollama_base_url}{path}"
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


def ollama_version_get() -> dict[str, Any]:
    return _ollama_get("/api/version")


def ollama_models_get() -> list[str]:
    result = _ollama_get("/api/tags")
    models = result.get("models", [])

    if not isinstance(models, list):
        return []

    names: list[str] = []
    for model in models:
        if not isinstance(model, dict):
            continue

        name = model.get("name")
        if isinstance(name, str):
            names.append(name)

    return names


def ollama_is_healthy() -> bool:
    try:
        ollama_version_get()
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


def ollama_model_ensure_available(model_name: str) -> None:
    available_models = ollama_models_get()

    if model_name in available_models:
        return

    raise RuntimeError(
        f"Configured model '{model_name}' is not available in local Ollama. "
        f"Pull it explicitly with: ollama pull {model_name}"
    )


def ollama_chat(payload: dict[str, Any]) -> dict[str, Any]:
    model_name = payload.get("model")

    if isinstance(model_name, str):
        ollama_model_ensure_available(model_name)

    return _ollama_post("/api/chat", payload)


def ollama_generate(prompt: str, model_name: str | None = None) -> str:
    model = model_name or CONFIG.chat_model_name
    ollama_model_ensure_available(model)
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    result = _ollama_post("/api/generate", payload)
    response = result.get("response", "")

    if not isinstance(response, str):
        return ""

    return response
