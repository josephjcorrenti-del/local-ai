# ollama_workbench decisions

## Naming

- Project name is `ollama_workbench`.
- The old `hermes_lab` / `hermes` naming has been retired.
- Package imports should use `from ollama_workbench...`.
- Prefer model naming that separates size/capability from usage role.
- Current baseline model tiers are:
  - `lightweight_model_name`
  - `large_model_name`
- Role-specific names like `chat_model_name` and `summary_model_name` may point to those tiers when useful.

## Project shape

- Keep code under `src/ollama_workbench/`.
- Keep the repo standalone, separate from `manumental-effort`.
- Keep the project CLI-first for now.
- Do not add web UI / TUI / service layers unless there is a concrete reason.

## Runtime and data

- Ollama is the local runtime.
- Models must remain swappable.
- Runtime/session data lives outside the repo under:
  `~/ai/data/ollama_workbench/`
- Current session path:
  `~/ai/data/ollama_workbench/sessions/`

### Model behavior

- If Ollama is not running, the CLI may attempt to start the local AI stack.
- If a configured model is missing, the CLI should fail with clear guidance.
- The CLI must not implicitly pull models.
- Pulling models remains an explicit user action (e.g. `ollama pull <model>`).

## Config and paths

- `config.py` owns settings and root paths.
- `paths.py` owns derived filesystem paths.
- Keep behavior explicit and inspectable.

## Memory

- Memory should stay small and inspectable.
- Prefer summaries over uncontrolled memory growth.
- Do not introduce hidden or complex memory systems.
- Session files should use a stable object shape with:
  - `session`
  - `created_at`
  - `updated_at`
  - `summary`
  - `messages`
- Backward compatibility with older list-based session files should be preserved when practical.

## Web access

- Web access should remain explicit and opt-in.
- Normal chat flow must not browse the web implicitly.
- Web operations should use separate commands/tools.
- Fetched web content should be saved as inspectable artifacts under the app data root.
- AI reasoning over web content should operate on explicit fetched artifacts.
