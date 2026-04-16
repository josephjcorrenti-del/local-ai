from __future__ import annotations

"""
ollama_workbench/runtime.py

Runtime integration layer for local AI stack (Ollama + helper scripts).

Responsibilities:
- Provide thin wrappers around Ollama HTTP API (GET/POST)
- Ensure Ollama is running before requests (startup + health checks)
- Validate model availability before use
- Execute external helper scripts for AI stack control
- Emit runtime-level logging for traceability (requests, startup, model checks)

Design notes:
- HTTP calls are intentionally simple (urllib, no external client)
- Health checks are performed via /api/version and may be repeated for clarity
- Startup is explicit:
  - if Ollama is not healthy, attempt to start local AI stack
  - retry for a short bounded window before failing
- Model availability is enforced explicitly (no auto-pull)
- Logging captures:
  - request intent (chat/generate)
  - HTTP calls
  - startup and health transitions
  - model validation outcomes
- Prompt/response content is never logged
"""

import json
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any

from ollama_workbench.config import CONFIG
from ollama_workbench.log import log_event
from ollama_workbench.paths import paths_get


def _ollama_get(path: str) -> dict[str, Any]:
    """Perform a GET request to the Ollama API and return parsed JSON."""
    url = f"{CONFIG.ollama_base_url}{path}"
    req = urllib.request.Request(url, method="GET")

    log_event(
        "ollama.http.get",
        path=path,
        url=url,
    )

    try:
        with urllib.request.urlopen(req, timeout=CONFIG.request_timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        log_event(
            "ollama.http.get.error",
            level="error",
            path=path,
            url=url,
            error=f"HTTP {exc.code}: {body}",
        )
        raise RuntimeError(f"Ollama HTTP error {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        log_event(
            "ollama.http.get.error",
            level="error",
            path=path,
            url=url,
            error=f"Connection failed: {reason}",
        )
        raise RuntimeError(
            f"Failed to connect to Ollama at {CONFIG.ollama_base_url}"
        ) from exc


def _ollama_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        """Perform a POST request to the Ollama API and return parsed JSON."""
        url = f"{CONFIG.ollama_base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        log_event(
            "ollama.http.post.error",
            level="error",
            path=path,
            url=url,
            model=model,
            error=f"Connection failed: {reason}",
        )
        raise RuntimeError(
            f"Failed to connect to Ollama at {CONFIG.ollama_base_url}"
        ) from exc

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    model_name = payload.get("model")
    model = model_name if isinstance(model_name, str) else None

    log_event(
        "ollama.http.post",
        path=path,
        url=url,
        model=model,
    )

    try:
        with urllib.request.urlopen(req, timeout=CONFIG.request_timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        log_event(
            "ollama.http.post.error",
            level="error",
            path=path,
            url=url,
            model=model,
            error=f"HTTP {exc.code}: {body}",
        )
        raise RuntimeError(f"Ollama HTTP error {exc.code}: {body}") from exc


def ollama_version_get() -> dict[str, Any]:
    """Return Ollama version information."""
    return _ollama_get("/api/version")


def ollama_models_get() -> list[str]:
    """Return a list of available model names from Ollama."""
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


# WHY:
# Health is treated as a simple boolean check: any failure to reach Ollama
# is considered "not healthy". This intentionally hides specific errors at
# this layer so callers can make a simple go/no-go decision.
def ollama_is_healthy() -> bool:
    """Return True if Ollama responds to a basic health check."""
    try:
        ollama_version_get()
        return True
    except Exception:
        return False


def ai_stack_start() -> None:
    """Start the local AI stack using the configured helper script."""
    script_path = paths_get().ai_start_script

    log_event(
        "ai.stack.start",
        path=str(script_path),
    )

    subprocess.run(
        [str(script_path)],
        check=True,
        text=True,
    )


def ai_status_show() -> None:
    """Display the current status of the local AI stack."""
    script_path = paths_get().ai_status_script

    log_event(
        "ai.stack.status",
        path=str(script_path),
    )

    subprocess.run(
        [str(script_path)],
        check=True,
        text=True,
    )


# WHY:
# Commands assume a working local AI runtime. Instead of failing immediately,
# attempt to start the local stack and retry for a short, bounded window.
# This keeps CLI usage smooth while still failing fast if startup does not succeed.
def ollama_ensure_running() -> None:
    """Ensure Ollama is running, starting it if necessary."""
    log_event("ollama.ensure_running.check")

    if ollama_is_healthy():
        log_event("ollama.ensure_running.ready")
        return

    log_event("ollama.ensure_running.start")
    print("[*] Ollama not healthy. Starting AI stack...")
    ai_stack_start()

    for _ in range(20):
        if ollama_is_healthy():
            log_event("ollama.ensure_running.ready")
            print("[✓] Ollama is healthy")
            return
        time.sleep(1)

    log_event(
        "ollama.ensure_running.timeout",
        level="error",
        error="Ollama did not become healthy after startup",
    )
    raise RuntimeError("Ollama did not become healthy after startup")


def ollama_model_ensure_available(model_name: str) -> None:
    """Ensure the given model is available locally, raising if not."""
    log_event(
        "ollama.model.ensure_available.check",
        model=model_name,
    )

    available_models = ollama_models_get()

    if model_name in available_models:
        log_event(
            "ollama.model.ensure_available.ready",
            model=model_name,
        )
        return

    log_event(
        "ollama.model.ensure_available.missing",
        level="error",
        model=model_name,
        error=(
            f"Configured model '{model_name}' is not available in local Ollama. "
            f"Pull it explicitly with: ollama pull {model_name}"
        ),
    )

    raise RuntimeError(
        f"Configured model '{model_name}' is not available in local Ollama. "
        f"Pull it explicitly with: ollama pull {model_name}"
    )


# WHY:
# Chat requests validate model availability before issuing the HTTP call.
# This ensures failures are explicit and local (model missing) rather than
# surfacing later as API errors.
def ollama_chat(payload: dict[str, Any]) -> dict[str, Any]:
    """Send a chat request to Ollama and return the response JSON."""
    model_name = payload.get("model")
    model = model_name if isinstance(model_name, str) else None

    log_event(
        "ollama.chat.request",
        model=model,
        path="/api/chat",
    )

    if isinstance(model_name, str):
        ollama_model_ensure_available(model_name)

    return _ollama_post("/api/chat", payload)


# WHY:
# Generate is a simpler prompt-based path that defaults to the configured
# chat model unless explicitly overridden. This keeps summarize and other
# flows flexible without duplicating request logic.
def ollama_generate(prompt: str, model_name: str | None = None) -> str:
    """Generate a completion from Ollama using the given prompt."""
    model = model_name or CONFIG.chat_model_name

    log_event(
        "ollama.generate.request",
        model=model,
        path="/api/generate",
    )

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
