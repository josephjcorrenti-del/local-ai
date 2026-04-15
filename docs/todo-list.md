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

to be prioritized (tbp)

memory / summaries
[ ] define simple thresholds for later auto-summary

packaging / release
[ ] add console script entry point
[ ] install with pip/pipx locally
[ ] versioning approach

quality
[ ] add basic tests
[ ] add sample config

future ui
[ ] richer cli output
[ ] tui exploration
[ ] web ui only if still wanted

integration
[ ] decide later how ollama_workbench may integrate with manumental-effort
[ ] keep integration at boundary, not shared mess

storage / archive (future)
[ ] revisit separate storage only if chat JSONs need archiving or cold storage.  (removed storage from current flow)
[ ] revisit separate storage only if old web artifacts need archiving or cold storage.

more robust jsons
[ ] catch runtime errors in CLI and show clean user-facing error
[ ] preserve detailed exception context for debug/developer mode
[ ] add --debug flag for full traceback output
[ ] add doctor command checks for malformed session files
[ ] add explicit repair/migrate command for session files
[ ] isolate bad session files during aggregate commands (for example stats) and continue showing valid sessions

flexible code 
[ ] encoding="utf-8"

containers
[ ] containerize ollama_workbench
[ ] make helper script handling container-friendly

readability/traceability
[ ] logs (elk compatible)
[ ] comments
[ ] error handling

web search
[ ] add web-search by query
[ ] support multi-source web-chat
[ ] add richer extraction/cleaning strategies for fetched pages
[ ] revisit storage/archive strategy for old chats and old web artifacts
[ ] make helper script handling container-friendly
