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

## CLI output model

The CLI distinguishes between different categories of commands. This ensures
consistent output behavior and allows future reuse across CLI, web UI, and
other interfaces.

### Command categories

Commands should fall into one of the following categories:

- action:
  - Performs an explicit, state-changing or operator-invoked task
  - Examples: clear, summarize, migrate, repair, web-cleanup --delete
  - Output:
    - Uses output helpers (ok / fail / info / warn)
    - Ends with a clear result message

- report:
  - Displays current system or data state
  - Examples: status, sessions, stats, web-cleanup (dry run)
  - Output:
    - Plain, structured, and scannable
    - Avoids output helpers unless highlighting exceptional conditions

- content:
  - Returns model-generated or user-facing content
  - Examples: prompt, chat, json, tool, web-chat
  - Output:
    - Minimal framing
    - Avoids extra markers or formatting that interfere with readability

- artifact:
  - Produces or lists inspectable files or fetched sources
  - Examples: web-fetch, web-search
  - Output:
    - Consistent source/path formatting
    - Clear association between content and artifact path

### Output rules

- stdout is reserved for usable command output.
- stderr is reserved for failure conditions.
- The `fail()` helper must always write to stderr.
- The `ok()`, `info()`, and `warn()` helpers write to stdout.

- Structured logs are:
  - Always written to the run log file
  - Only shown in terminal when `--verbose` is set

- Commands must not mix structured logs into normal CLI output.

### Design intent

- Keep CLI output predictable and script-friendly
- Preserve a clear separation between:
  - human-readable output
  - structured logs
  - failure signaling

- This model supports future expansion to:
  - browser-based UI
  - interactive workbench shell
  - SQL-like querying interface

### Formatting rules

- Prefer plain, readable output over decorative formatting.
- Use output helpers only when they clarify action status, progress, warning, or failure.
- Do not force markers onto report/data/content output.
- Use lowercase section headers ending with `:`.
- Separate major sections with one blank line.
- Use `key: value` for simple facts.
- Use two-space indentation for nested key/value lines.
- Use numbered blocks for source/artifact lists.
- Keep raw model/content output minimally framed.
- Keep JSON output valid and unwrapped when a command intentionally emits JSON.
- Dry-run output should clearly say what would happen, not imply that work was performed.

### Action message guidelines

- Prefer starting action-related messages with:
  "<Object> <action>"

- This applies primarily to:
  - ok() messages (successful actions)
  - fail() messages (failed actions)

- Additional detail may follow as needed, for example:
  - "Session migrated (default) changed=True"
  - "chat model lookup failed: qwen2.5-coder:3b"

- Do not enforce this pattern strictly where it harms readability.

- info() and warn() messages are intentionally flexible and may:
  - describe progress ("Executing tool...")
  - describe intent ("Would migrate...")
  - explain conditions ("Model did not call a tool")

- Clarity is preferred over strict formatting.

### Search provider direction

- Current web search uses DuckDuckGo as the only implemented provider.
- Do not add search-engine configuration while there is only one provider.
- The preferred long-term direction is a locally hosted search service/API that `ollama_workbench` can call explicitly.
- A provider abstraction should be introduced only after a second provider exists, preferably the local search provider.

### Summarize behavior

- `summarize --session` operates on a single session and reports:
  - summarized
  - skipped with reason

- `summarize --all` is currently fail-fast:
  - a single malformed or failing session stops execution
  - this is intentional for manual/operator use

- A future automated/batch mode may:
  - log per-session failures
  - continue processing remaining sessions
  - provide a final summary

### Debug mode behavior

- Default mode:
  - shows concise user-facing error messages
  - does not include traceback or exception type

- `--debug` mode:
  - shows full Python traceback
  - preserves full exception context

- Structured error details:
  - remain in NDJSON logs
  - are not surfaced in CLI output

- Do not introduce additional error formatting unless a second interface requires it.

### Web-chat prompt policy

- Web-chat uses bounded content per source to control prompt size.
- The limit is defined by:
  - `CONFIG.web_chat_max_source_chars`

- Bounding is:
  - explicit
  - deterministic
  - applied before model invocation

- This is a safety and performance boundary, not a quality optimization.
- Future improvements may replace simple truncation with question-aware selection.

### Web search performance

- Web search latency is primarily due to:
  - sequential network fetch of multiple sources

- Current behavior:
  - fetches results sequentially
  - prioritizes simplicity and inspectability over speed

- Optimization is deferred until needed.
- Likely future direction:
  - parallel fetch of sources

### Web artifact handling

- Fetched web content is stored as raw, inspectable artifacts.
- Artifacts must remain unchanged after fetch.

- Any transformation for model input (e.g. truncation, chunking):
  - occurs at read/use time
  - must not modify stored artifacts

- This preserves:
  - reproducibility
  - inspectability
  - debuggability
