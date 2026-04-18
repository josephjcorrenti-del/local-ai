from __future__ import annotations

from pathlib import Path

from ollama_workbench.paths import paths_get


def test_paths_default_data_root(monkeypatch):
    monkeypatch.delenv("OWB_DATA_DIR", raising=False)

    paths = paths_get()

    assert paths.data_root == Path.home() / "ai" / "data"
    assert paths.app_data_root == Path.home() / "ai" / "data" / "ollama_workbench"
    assert paths.sessions_dir == Path.home() / "ai" / "data" / "ollama_workbench" / "sessions"
    assert paths.web_dir == Path.home() / "ai" / "data" / "ollama_workbench" / "web"


def test_paths_test_data_root(monkeypatch):
    monkeypatch.setenv("OWB_DATA_DIR", "test_data")

    paths = paths_get()

    assert paths.data_root == Path.home() / "ai" / "test_data"
    assert paths.app_data_root == Path.home() / "ai" / "test_data" / "ollama_workbench"
    assert paths.sessions_dir == Path.home() / "ai" / "test_data" / "ollama_workbench" / "sessions"
    assert paths.web_dir == Path.home() / "ai" / "test_data" / "ollama_workbench" / "web"


def test_repo_paths_resolve_inside_repo():
    paths = paths_get()

    assert paths.repo_root.name == "ollama_workbench"
    assert paths.src_root == paths.repo_root / "src"
    assert paths.package_root == paths.repo_root / "src" / "ollama_workbench"
    assert paths.scripts_dir == paths.repo_root / "scripts"
