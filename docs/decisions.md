# ollama_workbench decisions

## Naming

- Project name is `ollama_workbench`.
- The old `hermes_lab` / `hermes` naming has been retired.
- Package imports should use `from ollama_workbench...`.

## Project shape

- Keep code under `src/ollama_workbench/`.
- Keep the repo standalone, separate from `manumental-effort`.
- Keep the project CLI-first for now.
- Do not add web UI / TUI / service layers unless there is a concrete reason.

## Runtime and data

- Ollama is the local runtime.
- Model must remain swappable.
- Runtime/session data lives outside the repo under:
  `~/ai/data/ollama_workbench/`
- Current session path:
  `~/ai/data/ollama_workbench/sessions/`

## Config and paths

- `config.py` owns settings and root paths.
- `paths.py` owns derived filesystem paths.
- Keep behavior explicit and inspectable.

## Memory

- Memory should stay small and inspectable.
- Prefer summaries over uncontrolled memory growth.
- Do not introduce hidden or complex memory systems.

## Coding standards

- Prefer clear, boring, understandable Python.
- Prefer descriptive names over short clever names.
- Use package imports: `from ollama_workbench...`
- Keep cleanup incremental; avoid large refactors.
- Tighten typing where easy and useful.
- Do not overengineer type hints.

## CLI behavior

- Explicit commands are preferred over hidden behavior.
- Web access, if added, should be explicit and opt-in.
- Tooling should remain inspectable.

## Current practical run mode

- From `src/`, this works:
  `python3 -m ollama_workbench.cli ...`
- From repo root, use:
  `PYTHONPATH=src python3 -m ollama_workbench.cli ...`
- A cleaner installed entry point can be added later.

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

## Summaries

- Summary shape should be:

  ```json
  {
    "text": "...",
    "updated_at": "...",
    "source_message_count": 0
  }
