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

## Versioning approach

- Keep version in pyproject.toml
- Update manually at meaningful milestones
- Use 0.x.y while command shape and workflow are still evolving
- Bump patch for fixes/polish
- Bump minor for meaningful new capabilities or workflow changes
- Reserve 1.0.0 for a more stable, intentional CLI contract

## Observability / ELK

- `ollama_workbench` logs should remain explicit, local, and inspectable.
- Structured app logs should be emitted as NDJSON.
- `log.py` remains the single logging entrypoint.
- Logging should stay stdout-visible for CLI traceability.
- The same structured event payload may also be written to a local run log for Filebeat ingestion.
- The initial runtime log path is:
  `~/ai/data/ollama_workbench/logs/run.log`
- ELK ingestion should mirror the existing local pattern:
  app -> NDJSON file -> Filebeat -> Elasticsearch -> Kibana
- Initial ELK identity fields for this app should be:
  - `service.name = ollama-workbench`
  - `event.dataset = ollama-workbench.runlog`
- Prefer simple field mirroring and explicit mappings over introducing a fuller logging framework.
- Do not break or redesign existing OpenVPN or python-lab ingestion to add `ollama_workbench`.
