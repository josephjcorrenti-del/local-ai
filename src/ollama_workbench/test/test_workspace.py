from pathlib import Path


def test_workspace_create_list_show(monkeypatch, tmp_path):
    from ollama_workbench import workspace

    class FakePaths:
        app_data_root = tmp_path

    monkeypatch.setattr(workspace, "paths_get", lambda: FakePaths())

    created = workspace.workspace_create("test-ws")

    assert created["name"] == "test-ws"
    assert created["sessions"] == []
    assert created["files"] == []
    assert created["web_artifacts"] == []
    assert created["notes"] == ""

    assert workspace.workspace_names_get() == ["test-ws"]

    loaded = workspace.workspace_load("test-ws")
    assert loaded["name"] == "test-ws"


def test_workspace_adds_are_idempotent(monkeypatch, tmp_path):
    from ollama_workbench import workspace

    class FakePaths:
        app_data_root = tmp_path

    monkeypatch.setattr(workspace, "paths_get", lambda: FakePaths())

    workspace.workspace_create("test-ws")

    first = workspace.workspace_session_add("test-ws", "default")
    second = workspace.workspace_session_add("test-ws", "default")

    assert first["changed"] is True
    assert second["changed"] is False

    first = workspace.workspace_file_add("test-ws", "README.md")
    second = workspace.workspace_file_add("test-ws", "README.md")

    assert first["changed"] is True
    assert second["changed"] is False

    first = workspace.workspace_web_artifact_add("test-ws", "/tmp/artifact.json")
    second = workspace.workspace_web_artifact_add("test-ws", "/tmp/artifact.json")

    assert first["changed"] is True
    assert second["changed"] is False

    loaded = workspace.workspace_load("test-ws")

    assert loaded["sessions"] == ["default"]
    assert loaded["files"] == ["README.md"]
    assert loaded["web_artifacts"] == ["/tmp/artifact.json"]
