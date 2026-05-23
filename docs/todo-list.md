todo

v2 phase 1 - cleanup + repo setup

done
[x] create proper package layout under src/local_ai
[x] move current python files into package directory
[x] update imports to package-safe imports
[x] add/update .gitignore
[x] fill in pyproject.toml
[x] rename any remaining hermes references to local_ai
[x] verify current commands still work after package cleanup

completed work not yet reflected in checklist
[x] add paths.py
[x] split config-owned roots from derived filesystem paths
[x] centralize session path resolution
[x] set runtime session path to ~/ai/data/local_ai/sessions
[x] verify sessions are being written to shared ai data path

next up - easy / structural
[x] add __init__.py
[x] update cli help text / app naming
[x] remove __pycache__ from repo
[x] add README.md

next up - cleanup pass
[x] add blank lines between top-level functions
[x] tighten obvious type hints
[x] remove unused Path import (commented for now)
[x] ai_status_show kept for later wiring
[ ] optional: CLI cleanup (skipped)

next up - project docs
[x] add initial architecture / roadmap notes
[x] add decisions.md

finish phase 1
[x] initialize git cleanly
[x] create first commit for local_ai v2 phase 1
[x] push to github

v2 phase 2 - session format baseline

done earlier
[x] centralize path handling
[x] set repo root separate from runtime data root
[x] set default runtime data root to ~/ai/data/local_ai

current phase
[x] define session file object format
[x] change session storage from raw message list to session object
[x] preserve backward compatibility for current session files if practical
[x] smoke test load/save/clear/sessions/stats

summaries
[x] add manual summarize action
[x] define summarize policy for long-running chats
[x] define when summaries run automatically vs only by request
[ ] add overnight summarize mode
[ ] define when summaries run automatically vs only by request

v2 cleanup
[x] detect malformed session JSON and fail with explicit error
[x] clean up runtime.py / runtime main flow
[x] decide whether missing models should auto-pull or fail with guidance
[x] pass model name into ollama_generate so summarize can use summary_model_name correctly

v2 phase 3 - summaries
[x] define simple summary format
[x] add manual summarize command
[x] store summary inside session file
[x] keep recent raw messages plus summary
[ ] define simple thresholds for later auto-summary
[x] verify inspectable and bounded memory behavior

v2 phase 5 - explicit runtime tooling
[x] make status command useful and explicit
[x] add doctor / smoke command
[x] show ollama status
[x] show configured model
[x] show session/data path
[x] bring AI helper scripts under repo control
[x] verify helper script integration stays explicit

v2 phase 6 - explicit web access
[x] define web access as separate commands/tools
[x] keep web use opt-in and visible
[x] define saved artifact shape for fetched web content
[x] define storage location for fetched web artifacts
[x] implement web-fetch for a single explicit URL
[x] implement minimal web-chat over one explicit fetched artifact
[x] avoid hidden web behavior in normal chat flow
[x] add cleanup path for old web artifacts

v2 cleanup final
[x] remove obvious dead/commented code after active phase work
[x] do final docs + todo consistency pass
[x] do final smoke pass across active commands

v3 - readability / traceability

v3 phase 1 - logs
[x] define logging policy and event shape
[x] define which event fields may be null in first pass
[x] add small shared logging helper
[x] add command start/end logging in cli.py
[x] add runtime request/startup logging in runtime.py
[x] add session/web file-operation logging in memory.py and web.py
[x] keep logs stdout-friendly and ELK-compatible JSON-per-line
[x] comment out old ndjson shape/examples where replaced and add new shape inline

v3 phase 2 - comments
[x] add module-level intent comments where behavior is non-obvious
[x] add short docstrings for public entry points
[x] add targeted comments for session compatibility/normalization flow
[x] add targeted comments for runtime startup/model checks
[x] decide whether log.py should have a header comment
[x] decide whether log.py should include a sample path comment
[x] update comments to match actual behavior
[x] remove comments that restate obvious code

v3 phase 3 - error handling
[x] add top-level CLI error boundary in main()
[x] show clean user-facing errors by default
[x] preserve traceback only for later debug mode
[x] handle urllib/network failures explicitly in runtime.py and web.py
[x] isolate malformed session files during aggregate commands
[x] keep failure messages explicit and inspectable

v3 phase 4 - doctor enhancement
[x] add structured doctor check logging
[x] add doctor summary output (checks run / failures)
[x] verify helper scripts exist and are runnable
[x] verify app data root and web dir are writable
[x] add doctor checks for malformed session files
[x] report bad session files without aborting full doctor run
[x] keep doctor output human-readable and logs machine-readable
[x] do not auto-repair; provide explicit guidance only

v4 - quick wins

v4 phase 1 - summary policy cleanup
[x] add overnight summarize mode
[x] define simple thresholds for later auto-summary
[x] define when summaries run automatically vs only by request

v4 phase 2 - small codebase polish
[x] add encoding="utf-8" where missing and useful
[x] decide whether external/sample config is needed before adding config file support

v5 - operator and developer UX

v5 phase 1 - debug mode
[x] preserve detailed exception context for debug/developer mode
[x] add --debug flag for full traceback output

v5 phase 2 - packaging / local install
[x] add console script entry point
[x] install in local venv with pip
[x] versioning approach

v5 phase 3 - runtime helper cleanup
[x] decide which active helper scripts should remain repo-owned
[x] replace active shell helpers with Python only where it improves clarity or portability
[x] keep legacy_ai_stack scripts isolated and clearly out of active workflow
[x] align helper behavior with manual ollama serve runtime

v6 - quality and safety hardening

v6 phase 1 - tests
[x] add basic tests
[x] add session test fixtures under test_data

v6 phase 1.1 - GitHub Actions
[x] add minimal GitHub Actions workflow for portable test checks

v6 phase 2 - session robustness
[x] add explicit repair/migrate command for session files

v6 phase 3 - archive strategy review
[ ] revisit separate storage only if chat JSONs need archiving or cold storage
[ ] revisit separate storage only if old web artifacts need archiving or cold storage
[ ] revisit storage/archive strategy for old chats and old web artifacts

v7 - web search capability expansion

v7 phase 1 - richer fetch behavior
[x] add richer extraction/cleaning strategies for fetched pages

v7 phase 2 - explicit search workflows

phase 2a
[x] add web-search by query

phase 2b - multi-source web-chat
[x] extend web-chat to accept --query as an alternative to --url
[x] run web-search when --query is used
[x] combine fetched artifacts into one bounded prompt
[x] print which sources/artifacts were used

v8 - observability / ELK

v8 phase 1 - local_ai ELK integration
[x] add explicit app log path under ~/ai/data/local_ai/logs/run.log
[x] extend log_event to write the same NDJSON payload to stdout and run.log
[x] keep logging behavior explicit and inspectable (no background logger setup)
[x] verify log directory/file creation behavior is simple and local

v8 phase 2 - filebeat wiring
[x] add docker volume mount for local_ai run.log into filebeat container
[x] add filebeat filestream input for local_ai run.log
[x] assign service.name=local-ai
[x] assign event.dataset=local-ai.runlog
[x] keep existing openvpn/python-lab ingestion unchanged

v8 phase 3 - field mapping / Kibana shape
[x] map local_ai fields into Kibana-friendly columns
[x] keep/service mirror columns where useful: service.name, event.dataset, log.level, log.logger, log.origin.function, log.origin.file.name, labels.run_id, event.action, message
[ ] decide which existing local_ai fields stay first-class: command, session, model, path, url, error
[x] verify fields are searchable and aggregatable in Discover

v8 phase 4 - verification
[x] run explicit CLI smoke commands and verify ingestion in Elasticsearch
[x] verify Discover filters for event.dataset:"local-ai.runlog"
[x] define initial Discover column layout for local_ai
[ ] refine saved Discover views per service / use case
[ ] add sample KQL queries for common operator views

v8 phase 5 - follow-up design review
[ ] decide whether run_id should become a first-class required field
[ ] decide whether command/session should map to labels.* or stay top-level
[ ] decide whether stdout+file dual-write remains the long-term logging policy
[ ] evaluate duplicate /api/version calls
    - collapse redundant health checks OR tag separately
    - preserve traceability

v8.6 - logging polish

phase 1 - raw app log contract
[x] keep current fields unchanged
[x] add event_outcome
[x] add elapsed_ms
[x] add error_message
[x] add error_type

phase 2 - filebeat mapping
[x] map owb.event_outcome -> event.outcome
[ ] decide whether to keep owb.elapsed_ms raw or also map to a standard field
[x] map owb.error_message -> error.message
[x] map owb.error_type -> error.type

phase 3 - kibana verification
[x] verify fields appear in Discover
[x] verify fields are searchable
[x] verify fields are aggregatable where expected
[x] verify success/failure filters work
[x] verify elapsed_ms is useful and not noisy

v9 - integration and platform decisions

v9 phase 1 - integration boundary
[ ] decide later how local_ai may integrate with manumental-effort
[ ] keep integration at boundary, not shared mess

v9 phase 2 - containers
[ ] containerize local_ai
[ ] make helper script handling container-friendly

v10 - output modes and CLI readability

v10 phase 1 - output boundary
[x] separate user-facing command output from structured log output
[x] keep NDJSON run.log always written for ELK/Filebeat
[x] add --verbose to show structured log events in terminal
[x] keep --debug focused on traceback/developer error detail
[x] create small output helper for human-facing CLI output
[x] move doctor color/checkmark helpers out of cli.py

v10 phase 2 - status command cleanup
[x] make status the pilot command for clean one-shot CLI output
[x] keep status readable without embedded NDJSON noise
[x] preserve detailed inspection through run.log / --verbose

v10 phase 3 - command result shape
[ ] identify a simple internal result/output shape that can later support Browser UI, One-shot CLI, and Workbench shell

v10 phase 4 - output code readability
[x] standardize comments/docstrings around log.py, output.py, and CLI output boundaries
[x] route existing success/failure CLI markers through output.py helpers
[x] standardize info/warning/failure helpers across CLI output
[x] enforce stderr for failure paths via fail()

v10 phase 5 - CLI output consistency review
[x] classify commands as action, report, content, or artifact commands
[x] standardize action result wording across commands
[x] standardize section, key/value, and list formatting rules
[x] standardize error, warning, dry-run, and no-op messages
[x] decide whether stats remains JSON-only or later gains human/json output modes

v11 - gui exploration

v11 phase 1 - starting a GUI
[ ] start a GUI for local_ai
[ ] decide whether the first GUI should be web-based
[ ] keep GUI optional and separate from core CLI flow

v11 phase 2 - interface exploration
[ ] gui exploration
[ ] web ui only if still wanted

v12 quick wins 2

Debug
[x] add tests for normal vs --debug error behavior

CLI cleanup
[x] make summarize output distinguish "summarized" vs "no summary needed"
[x] review summarize/user-facing CLI messages so skipped work is reported accurately
[x] malformed json should be a warning in docs  

Web.py
[x] add content truncation / windowing per source

v13 important 2

phase 1 - decisions

Debug
[x] decide whether debug mode should log exception type separately from error text
[x] decide whether --debug should surface contained/structured errors differently

CLI cleanup
[x] decide whether summarize --all should continue on per-session failure or fail fast
[x] review duplicate Ollama health/model calls only if logs become noisy

Web.py
[x] decide how search engines should be configured before adding config support
[x] decide what "--query is slow" means before optimizing


phase 2 - cli cleanup

Doctor
[x] create and move doctor logic in cli.py to doctor.py
[x] refactor cli.doctor_command_run

CLI cleanup
[x] keep cli.py focused on orchestration only as complexity justifies
[x] standardize command handler/docstring shape where helpful


phase 3 - web follow-up

Web.py
[ ] add search engine(s) to config
[x] add simple question-aware source windows for web-chat
[x] split each artifact content_text into bounded text windows
[x] score windows using question terms
[x] include top matching windows per source in the model prompt
[x] keep artifacts unchanged and inspectable
[x] keep fallback to first-N chars when no useful match is found

v14 misc tasks

Doctor
[ ] revisit doctor output grouping only if it improves readability
[ ] revisit doctor check taxonomy only if ELK/log review justifies it

Debug
[x] decide whether --debug should affect argparse parse errors

CLI cleanup
[ ] refactor repeated doctor writable-check pattern only if it improves readability without hiding behavior
[x] decide whether summary_inactive_minutes should remain reserved or be removed until used
[ ] tighten session naming around "load ok" vs deeper validation if needed later

Other
[ ] decide whether formats besides utf-8 should be allowed.
[ ] decide whether pipx install is needed for operator workflow
[ ] add chat config
[ ] parser arguments in chat
[ ] optionally turn logs off in cli

v15 prep for outside interfaces

File system
[x] add fs_read(path, max_chars) in fs.py
[x] validate path exists
[x] validate path is a file, not a directory
[x] enforce max_chars with a bounded default
[x] return structured result with path, size, content, included_chars, truncated

[x] add read-file <path> [--max-chars N] CLI command
[x] print path, size, included_chars of total, and bounded content

[x] default file access is one-time read only
[x] treat explicit read-file <path> invocation as operator approval for that file read

[x] log fs.read.start, fs.read.ready, fs.read.error

[x] add tests for happy path with small file
[x] add tests for truncation path with larger file
[x] add tests for missing file
[x] add tests for directory instead of file

[x] ensure file read behavior is read-only and has no side effects

File AI
[x] add file-chat <path> <question>
[x] read explicit file once
[x] shape content with content_window_get
[x] send bounded content to Ollama
[x] print path, included_chars of total, answer
[x] log command.start/end and fs.read lifecycle
[x] add tests/smoke for file-chat prompt construction if practical

v15.5 - logging consistency + interface-surface decision

Logging consistency
[x] verify every CLI command emits command.start and command.end OR command.error
[x] ensure command.start/end/error always include command=<name>
[x] add event_outcome="success" to web.fetch.ready
[x] add event_outcome="success" to web.cleanup.ready
[x] add elapsed_ms to web.fetch.ready
[x] add elapsed_ms to fs.read.ready

Deferred
[ ] consider content.window.ready later only if Kibana review says it helps

Decisions
[x] document: CLI output, structured logs, and module returns are separate surfaces
[x] document: logs are observability trace, not result API

v15.6 - interface readiness polish

Command inventory
[x] list commands by category: content / report / artifact / action
[x] identify which commands are likely UI/shell entrypoints first
[x] mark commands that are operator-only and should stay CLI-first

Access/source model
[x] document current source types:
    - web artifact
    - explicit file read
    - session memory
[x] decide whether “source” is just a concept for now, not a module yet

Output safety
[x] verify content commands avoid decorative output
[x] verify failure output stays stderr-only
[x] verify logs stay out of stdout unless --verbose

Smoke coverage
[x] ensure smoke test covers every major access path:
    - runtime
    - sessions
    - web
    - file
    - file AI
    - cleanup

v15.7 - multi-source (file + web)

Source handling
[ ] allow one question to use multiple explicit sources
[ ] support local file sources
[ ] support web URL sources
[ ] keep source access explicit and one-time
[ ] keep web artifacts unchanged
[ ] keep file reads read-only

CLI
[ ] add multi-source command shape
[ ] decide command name: source-chat vs multi-chat
[ ] accept repeated --file PATH
[ ] accept repeated --url URL
[ ] require one question
[ ] print sources used
[ ] print included_chars per source
[ ] print final answer

Context shaping
[ ] use content_window_get per source
[ ] combine bounded source windows into one prompt
[ ] preserve source labels in prompt
[ ] enforce per-source content bounds
[ ] avoid hidden source discovery

Logging / tests
[ ] verify command.start/end/error logs
[ ] verify fs.read lifecycle logs for file sources
[ ] verify web.fetch lifecycle logs for URL sources
[ ] add mocked prompt-construction test
[ ] smoke test with one file + one URL

v16 outside interfaces

v16.1 - shell MVP

[x] add shell command to CLI
[x] implement REPL loop
[x] add help command
[x] add exit/quit handling
[x] add default-to-chat fallback
[x] use shlex for parsing
[x] dispatch to existing handlers without duplicating command logic
[x] smoke test basic flow
[x] add pytest for default-to-chat routing

v16.2 - make shell usable

Help / discoverability
[x] improve shell help formatting
[x] add examples to shell help
[ ] add help by topic if useful: help file, help web, help session
[x] show default-to-chat behavior clearly

Shell UX
[x] add command history
[x] add Ctrl+D clean exit behavior
[x] keep Ctrl+C from killing shell
[x] improve parse-error messages
[ ] add clear screen command if useful
[x] add shell banner with current model and session
[x] add banner command to reprint shell context

Session behavior
[x] decide whether shell should have a default session
[x] support changing session inside shell if needed
[x] make chat default use selected session if shell session exists

Usability guardrails
[x] keep shell commands identical to CLI commands where practical
[x] avoid shell-only business logic
[x] keep shell as orchestration layer
[x] preserve command.start/end/error logging

Tests / smoke
[x] test explicit command routing
[x] test help command does not call CLI handlers
[x] manual smoke test interactive flow

v16.2.1
[x] warmup (done)
[x] streaming responses
[ ] consider shorter system prompt for shell
[ ] consider lightweight shell model

v16.3 - workspace container

Concept
[x] define workspace container purpose (reference point grouping)
[x] decide naming: workspace
[x] decide workspace is grouping metadata, not hidden behavior
[x] decide sessions, files, web artifacts, notes are supported references
[x] decide sessions can belong to multiple workspaces
[x] decide workspace owns relationships (no reverse pointer in session)
[x] decide CLI-visible first, shell integration second

Storage
[x] define workspace storage location under app data root
[x] define workspace file shape (schema locked in decisions.md)
[x] store workspace name (used as identifier)
[x] store linked session names
[x] store linked file paths
[x] store linked web artifact paths
[x] store notes/summary field
[x] add created_at / updated_at timestamps
[x] ensure add operations are idempotent (no duplicate references)
[x] ignore unknown fields on load (forward compatibility)

Commands (CLI-first)
[x] add workspace-create <name>
[x] add workspace-list
[x] add workspace-show <name>
[x] add workspace-add-session <workspace> <session>
[x] add workspace-add-file <workspace> <path>
[x] add workspace-add-web-artifact <workspace> <artifact_path>
[x] do NOT add remove commands until add/show is stable

Shell integration
[x] decide shell can select active workspace
[x] implement workspace NAME (create/select active workspace)
[x] link active session to workspace when workspace is active
[x] link active workspace to session when session is set
[x] show active workspace in shell banner
[x] keep workspace selection explicit
[x] avoid automatic source loading from workspace in v1

Guardrails
[x] do not create persistent file access silently
[x] do not auto-read workspace files
[x] do not auto-fetch workspace web sources
[x] do not auto-inject workspace into normal chat
[x] keep workspace as inspectable container

Workspace chat (future but defined)
[x] define workspace-chat as explicit command
[x] define use of existing bag-of-words / windowing for files
[x] define output should show which sources were used
[x] implement workspace-chat (after core commands stabilize)
[x] implement workspace-chat <workspace> <question>
[x] load workspace metadata
[x] use linked files with content_window_get
[x] use linked web artifacts with existing web artifact windowing
[x] print sources used with included chars
[x] do not auto-fetch web sources
[x] do not auto-read anything outside workspace references
[x] use linked sessions as needed context for workspace-chat
[x] include bounded linked session history / summaries
[x] print linked sessions used

Tests / smoke
[x] add tests for workspace create/list/show
[x] add tests for idempotent add operations
[x] add tests for session linking behavior
[x] add tests for file/artifact linking
[x] manual smoke test CLI workflow
[x] manual smoke test shell workspace selection
[x] smoke test workspace flow

v16.4 - user profile

Concept
[x] define user profile purpose
[x] decide what belongs in profile vs config
[x] keep profile explicit and inspectable
[x] avoid hidden personalization behavior
[x] profile persistence starts disabled by default
[x] profile can be enabled explicitly
[x] profile can be disabled easily
[x] profile can be deleted easily

Storage
[x] define profile storage location under app data root
[x] define profile file shape
[x] include enabled flag in profile state
[x] store display name only if useful
[x] store preferred default model only if needed
[ ] store preferred default session/workspace only if needed
[ ] store shell preferences only if needed

Commands
[x] add profile-show
[x] add profile-enable
[x] add profile-disable
[x] add profile-set <human-readable-key> <value>
[x] add profile-clear <human-readable-key>
[x] add profile-delete
[ ] add profile-reset only if needed

Shell integration
[x] auto-load default profile when default profile is enabled
[x] allow shell --profile <profile-key> to load a named profile
[ ] allow shell --user <profile-key> as human-friendly alias only if useful
[x] load selected profile before model warm-up
[x] show active profile in shell banner when useful
[x] keep shell startup behavior unchanged when no enabled profile exists
[x] apply preferred model from enabled profile only when present
[x] apply preferred workspace/session only when explicitly defined

Guardrails
[x] no sensitive personal data by default
[x] no hidden behavior based on profile
[x] no automatic memory injection from profile
[x] keep profile separate from chat/session memory
[x] profile-delete removes stored profile data, not just disables it

Tests / smoke
[x] add tests for profile read/write
[x] add tests for disabled profile behavior
[x] add tests for profile enable/disable
[x] add tests for profile delete
[ ] add tests for CLI override behavior if defaults are added
[x] smoke test profile commands
[x] smoke test shell profile loading

## post-v16.5 stabilization before integration

### Pre-rename safety check

[ ] confirm rename will not silently migrate data
[ ] confirm old data root remains untouched unless explicit migration is added
[ ] confirm old command compatibility behavior is intentional
[ ] confirm logging changes are documented before app/log path changes
[ ] confirm no profile/workspace/session behavior changes are bundled into rename

### Security

[ ] review all persistence surfaces
    - profiles
    - sessions
    - workspace paths
    - file reads
    - web artifacts
    - logs

[ ] verify profile values are explicit and non-executing
    - model is data only
    - session is data only
    - workspace is data only
    - no shell/profile command execution

[ ] validate workspace/profile path handling
    - reject unsafe paths where appropriate
    - normalize paths before use
    - preserve bounded reads only
    - avoid following persistence into implicit context injection

[ ] review logging for sensitive data exposure
    - profile names
    - file paths
    - prompts
    - URLs
    - errors/tracebacks

[ ] confirm no hidden automation was introduced
    - shell startup
    - profile auto-load
    - workspace loading
    - future retrieval hooks

[ ] document security boundaries in decisions.md
    - profiles are preferences, not memory
    - profile loading does not imply file/search/context loading
    - local_search integration must remain explicit


### Cleanup

[ ] review docs/todo-list.md for completed v16.4 items
[ ] move completed items out of active phase or mark done
[ ] add a new stabilization section before integration
[ ] review docs/decisions.md for profile decisions
[ ] ensure CLI command help is consistent
[ ] ensure shell command help is consistent
[ ] check naming consistency across:
    - cli.py
    - shell.py
    - profile module
    - docs
    - tests
    - README if applicable

[ ] remove dead code from profile implementation
[ ] remove unused imports
[ ] remove stale comments from previous shell/profile drafts
[ ] verify tests still describe intended behavior
[ ] add/adjust tests only where behavior is already agreed


### Rename project to local_ai

[ ] define rename end state
    - user-facing command: local-ai
    - Python package: local_ai
    - project identity: local_ai
    - old name: local_ai legacy/compatibility only

[ ] perform rename in two phases

[ ] phase 1: compatibility bridge
    - add local-ai console script
    - keep local-ai console script as alias
    - keep existing package path temporarily
    - update docs to prefer local-ai
    - add deprecation note for local-ai
    - do not move data root yet
    - do not rename log path yet
    - do not break ELK dashboards yet

[ ] phase 2: internal project rename
    - rename src/local_ai to src/local_ai
    - update all imports
    - update tests
    - update pyproject package discovery
    - update scripts/tests
    - update README/docs/cheatsheet
    - update shell banner/help text
    - update User-Agent strings
    - remove generated egg-info/cache artifacts from repo if tracked

[ ] decide data migration strategy
    - old data root: ~/ai/data/local_ai
    - new data root: ~/ai/data/local_ai
    - prefer explicit migration command, not silent move
    - support reading old location during transition if needed
    - document rollback behavior

[ ] decide logging compatibility strategy
    - app_name eventually becomes local_ai
    - run.log path eventually becomes ~/ai/data/local_ai/logs/run.log
    - preserve event names unless behavior changes
    - document ELK dashboard/filter impact
    - avoid surprise event.dataset breakage

[ ] add compatibility tests
    - local-ai status works
    - local-ai status still works during phase 1
    - python -m local_ai.cli works after phase 2
    - old command emits optional deprecation message only if acceptable
    - existing data remains readable

[ ] document rename decision in decisions.md
    - local_ai is the long-term project name
    - local-ai is the CLI command
    - local_ai is legacy naming
    - migration must be explicit and inspectable

17 - Website 
[ ] TBD

to be prioritized (tbp)
[ ] create a search engine like degoogle and load in local ai
[ ] AI should tell user where data lives.
[ ] CLI conversations should default to web searches.

File system
[ ] add parser/extraction layer for non-plain-text files, similar to web extraction
[ ] add persistent file access mode only with explicit opt-in
[ ] add persistent-read checkbox/setting for future UI
[ ] decide how persistent file permissions are stored and revoked

Shell
[ ] add shell command history
[ ] add shell autocomplete
[ ] add multiline input
[ ] add shell session/context awareness
[ ] add shell-specific formatting/presentation only if needed

Workspace chat polish
[ ] improve workspace-chat prompt/source separation so stale session context cannot dominate unrelated questions
[ ] workspace-chat should skip missing files/artifacts with warning
[x] add tests for workspace-chat source construction
[ ] verify workspace-chat does not fetch web sources
[ ] consider source weighting/order for sessions vs files vs web artifacts
[ ] consider workspace remove/unlink commands after add/show remains stable

Tests / smoke
[ ] test default-to-chat routing
[ ] test explicit command routing
[ ] test help command does not call CLI handlers
[ ] manual smoke test interactive flow

Refactor
[ ] make sure .pys are grouped in a way that makes sense
[ ] make sure paths are being used
[ ] docs strings are used
