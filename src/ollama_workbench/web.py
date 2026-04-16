from __future__ import annotations

"""
ollama_workbench/web.py

Explicit web access layer for fetching and storing web content.

Responsibilities:
- Fetch content from a single explicit URL
- Extract and normalize basic text content from HTML
- Persist fetched content as inspectable JSON artifacts
- Provide cleanup of old web artifacts

Design notes:
- Web access is opt-in and explicit (no automatic browsing)
- Each fetch produces a stored artifact under app data root
- Content extraction is simple and lossy (text-focused, no DOM structure)
- Artifacts are designed to be inspectable and reusable
- Logging traces fetch lifecycle and file operations, not content
"""

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timedelta, UTC
from html import unescape
from pathlib import Path
from typing import Any

from ollama_workbench.log import log_event
from ollama_workbench.paths import paths_get


def web_timestamp_now_get() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.now(UTC).isoformat()


def web_artifact_id_get(url: str) -> str:
    """Return a stable artifact identifier for the given URL."""
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def web_artifact_path_get(url: str) -> str:
    """Return the artifact file path for the given URL."""
    artifact_id = web_artifact_id_get(url)
    web_dir = paths_get().web_dir
    web_dir.mkdir(parents=True, exist_ok=True)
    return str(web_dir / f"{artifact_id}.json")


def _html_title_get(html_text: str) -> str | None:
    """Extract the HTML title from a page, if present."""
    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None

    title = unescape(match.group(1)).strip()
    title = re.sub(r"\s+", " ", title)
    return title or None


def _html_text_extract(html_text: str) -> str:
    """Extract normalized plain text content from HTML."""
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html_text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?is)<noscript[^>]*>.*?</noscript>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# WHY:
# Web fetch is explicit and artifact-based. Every fetch both returns content
# and writes an inspectable JSON snapshot so later commands can reason over
# the same stored input rather than hidden in-memory state.
def web_fetch(url: str) -> dict[str, Any]:
    """Fetch one URL, store its artifact, and return the artifact data."""
    log_event(
        "web.fetch.start",
        url=url,
    )

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ollama_workbench/0.1",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            final_url = resp.geturl()
            content_type = resp.headers.get("Content-Type", "")
            raw_bytes = resp.read()

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        log_event(
            "web.fetch.error",
            level="error",
            url=url,
            error=f"HTTP {exc.code}: {body}",
        )
        raise RuntimeError(f"Failed to fetch URL: {url}") from exc

    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        log_event(
            "web.fetch.error",
            level="error",
            url=url,
            error=f"Connection failed: {reason}",
        )
        raise RuntimeError(f"Failed to fetch URL: {url}") from exc

    html_text = raw_bytes.decode("utf-8", errors="replace")
    title = _html_title_get(html_text)
    content_text = _html_text_extract(html_text)

    artifact = {
        "url": final_url,
        "fetched_at": web_timestamp_now_get(),
        "content_type": content_type,
        "title": title,
        "content_text": content_text,
    }

    artifact_path = web_artifact_path_get(final_url)

    log_event(
        "web.artifact.save",
        path=artifact_path,
        url=final_url,
    )

    with open(artifact_path, "w", encoding="utf-8") as fh:
        json.dump(artifact, fh, indent=2)

    artifact["artifact_path"] = artifact_path

    log_event(
        "web.fetch.ready",
        path=artifact_path,
        url=final_url,
    )

    return artifact


def web_artifact_load(path: str) -> dict[str, Any]:
    """Load a saved web artifact from disk."""
    log_event(
        "web.artifact.load",
        path=path,
    )

    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def web_cleanup(days: int, delete: bool) -> list[Path]:
    """Find or remove web artifacts older than the given age."""
    paths = paths_get()
    web_dir = paths.web_dir

    log_event(
        "web.cleanup.start",
        path=str(web_dir),
    )

    if not web_dir.exists():
        log_event(
            "web.cleanup.skip_missing_dir",
            path=str(web_dir),
        )
        return []

    cutoff = datetime.now(UTC) - timedelta(days=days)

    removed: list[Path] = []

    for file_path in web_dir.glob("*.json"):
        try:
            stat = file_path.stat()
            modified = datetime.fromtimestamp(stat.st_mtime, UTC)
        except OSError:
            continue

        if modified < cutoff:
            removed.append(file_path)
            if delete:
                try:
                    file_path.unlink()
                    log_event(
                        "web.artifact.delete",
                        path=str(file_path),
                    )
                except OSError:
                    pass

    log_event(
        "web.cleanup.ready",
        path=str(web_dir),
    )

    return removed
