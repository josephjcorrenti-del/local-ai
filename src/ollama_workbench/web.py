from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timedelta, UTC
from html import unescape
from pathlib import Path
from typing import Any

from ollama_workbench.paths import paths_get


def web_timestamp_now_get() -> str:
    return datetime.now(UTC).isoformat()


def web_artifact_id_get(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def web_artifact_path_get(url: str) -> str:
    artifact_id = web_artifact_id_get(url)
    web_dir = paths_get().web_dir
    web_dir.mkdir(parents=True, exist_ok=True)
    return str(web_dir / f"{artifact_id}.json")


def _html_title_get(html_text: str) -> str | None:
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
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html_text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?is)<noscript[^>]*>.*?</noscript>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def web_fetch(url: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ollama_workbench/0.1",
        },
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        final_url = resp.geturl()
        content_type = resp.headers.get("Content-Type", "")
        raw_bytes = resp.read()

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
    with open(artifact_path, "w", encoding="utf-8") as fh:
        json.dump(artifact, fh, indent=2)

    artifact["artifact_path"] = artifact_path
    return artifact


def web_artifact_load(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def web_cleanup(days: int, delete: bool) -> list[Path]:
    paths = paths_get()
    web_dir = paths.web_dir

    if not web_dir.exists():
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
                except OSError:
                    pass

    return removed
