todo

v2 phase 1 - cleanup + repo setup

done
[x] create proper package layout under src/ollama_workbench
[x] move current python files into package directory
[x] update imports to package-safe imports
[x] add/update .gitignore
[x] fill in pyproject.toml
[x] rename any remaining hermes references to ollama_workbench
[x] verify current commands still work after package cleanup

completed work not yet reflected in checklist
[x] add paths.py
[x] split config-owned roots from derived filesystem paths
[x] centralize session path resolution
[x] set runtime session path to ~/ai/data/ollama_workbench/sessions
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
[x] create first commit for ollama_workbench v2 phase 1
[x] push to github

v2 phase 2 - session format baseline

done earlier
[x] centralize path handling
[x] set repo root separate from runtime data root
[x] set default runtime data root to ~/ai/data/ollama_workbench

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
[~] add explicit repair/migrate command for session files

v6 phase 3 - archive strategy review
[ ] revisit separate storage only if chat JSONs need archiving or cold storage
[ ] revisit separate storage only if old web artifacts need archiving or cold storage
[ ] revisit storage/archive strategy for old chats and old web artifacts

v7 - web search capability expansion

v7 phase 1 - richer fetch behavior
[ ] add richer extraction/cleaning strategies for fetched pages

v7 phase 2 - explicit search workflows
[ ] add web-search by query
[ ] support multi-source web-chat

v8 - observability / ELK

v8 phase 1 - ELK standup
[ ] match current ELK files
[ ] make available in Kibana

v8 phase 2 - logging design follow-up
[ ] decide whether to keep logging stdout-only or also support file output
[ ] decide whether to keep logging helper minimal or adopt fuller logger/config setup
[ ] decide whether env-driven logging config is needed
[ ] decide whether rotating file handler is needed
[ ] decide whether run_id is needed in first real pass
[ ] decide whether decorator-based function tracing is needed
[ ] decide which additional fields should become required later instead of null
[ ] evaluate duplicate /api/version calls
    - collapse redundant health checks OR tag separately
    - preserve traceability

v9 - integration and platform decisions

v9 phase 1 - integration boundary
[ ] decide later how ollama_workbench may integrate with manumental-effort
[ ] keep integration at boundary, not shared mess

v9 phase 2 - containers
[ ] containerize ollama_workbench
[ ] make helper script handling container-friendly

v10 - richer CLI output

v10 phase 1 - output refinement
[ ] richer cli output

v11 - gui exploration

v11 phase 1 - starting a GUI
[ ] start a GUI for ollama_workbench
[ ] decide whether the first GUI should be web-based
[ ] keep GUI optional and separate from core CLI flow

v11 phase 2 - interface exploration
[ ] gui exploration
[ ] web ui only if still wanted

to be prioritized (tbp)

Doctor
[ ] create and move doctor logic in cli.py to doctor.py
[ ] refactor cli.doctor_command_run
[ ] revisit doctor output grouping only if it improves readability
[ ] revisit doctor check taxonomy only if ELK/log review justifies it

Debug
[ ] decide whether --debug should affect argparse parse errors
[ ] decide whether --debug should surface contained/structured errors differently
[ ] decide whether debug mode should log exception type separately from error text
[ ] decide whether a later --verbose flag is needed distinct from --debug
[ ] add tests for normal vs --debug error behavior

CLI cleanup
[ ] refactor repeated doctor writable-check pattern only if it improves readability without hiding behavior
[ ] make summarize output distinguish "summarized" vs "no summary needed"
[ ] decide whether summarize --all should continue on per-session failure or fail fast
[ ] decide whether summary_inactive_minutes should remain reserved or be removed until used
[ ] review duplicate Ollama health/model calls only if logs become noisy
[ ] tighten session naming around "load ok" vs deeper validation if needed later
[ ] create and move doctor logic in cli.py to doctor.py
[ ] keep cli.py focused on orchestration only as complexity justifies
[ ] review summarize/user-facing CLI messages so skipped work is reported accurately
[ ] standardize command handler/docstring shape where helpful

Web.py
[ ] rename web.py to web_search.py

File system
[ ] read file system with explicit approval

Other 
[ ] decide whether formats besides utf-8 should be allowed.
[ ] decide whether pipx install is needed for operator workflow
