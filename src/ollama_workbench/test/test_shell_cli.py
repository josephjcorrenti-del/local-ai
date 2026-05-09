def test_shell_line_defaults_to_chat(monkeypatch):
    from ollama_workbench import cli

    called = {}

    def fake_chat_run(text, session_name=None, model_name=None, stream=False):
        called["command"] = "chat"
        called["text"] = text
        called["session"] = session_name
        called["model"] = model_name
        called["stream"] = stream

    monkeypatch.setattr(cli, "chat_run", fake_chat_run)

    cli.shell_line_run(
        "hello world",
        {"session": "default", "model": "test-model"},
    )

    assert called["command"] == "chat"
    assert called["text"] == "hello world"
    assert called["session"] == "default"
    assert called["model"] == "test-model"
    assert called["stream"] is True
