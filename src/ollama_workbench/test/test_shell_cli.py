def test_shell_line_defaults_to_chat(monkeypatch):
    from ollama_workbench import cli

    called = {}

    def fake_chat_command_run(args):
        called["command"] = "chat"
        called["text"] = args.text
        called["session"] = args.session

    monkeypatch.setitem(cli.COMMAND_HANDLERS, "chat", fake_chat_command_run)

    cli.shell_line_run("hello world", {"session": "default"})

    assert called["command"] == "chat"
    assert called["text"] == "hello world"
    assert called["session"] == "default"
