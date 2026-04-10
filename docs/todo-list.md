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
[x] add automatic summarize policy for long-running chats
[ ] add overnight summarize mode
[ ] define when summaries run automatically vs only by request

storage
[ ] prepare for later move to /mnt/data
[ ] add migration path for storage move if needed

v2 cleanup
[ ] clean malformed legacy session file content (for example `}[`)
[ ] decide whether to add explicit migrate/fix command for old session files
[ ] clean up runtime.py / runtime main flow
[ ] decide whether missing models should auto-pull or fail with guidance
[ ] pass model name into ollama_generate so summarize can use summary_model_name correctly

v2 phase 3 - summaries
[x] define simple summary format
[x] add manual summarize command
[x] store summary inside session file
[x] keep recent raw messages plus summary
[ ] define simple thresholds for later auto-summary
[x] verify inspectable and bounded memory behavior

v2 phase 4 - storage move
[ ] add config for data_root / sessions_dir
[ ] set target path to /mnt/data/ai/ollama_workbench
[ ] add migrate-sessions command
[ ] verify migrated sessions load correctly
[ ] keep move explicit and inspectable

v2 phase 5 - explicit runtime tooling
[ ] add status command
[ ] add doctor / smoke command
[ ] show ollama status
[ ] show configured model
[ ] show session/data path
[ ] verify helper script integration stays explicit

v2 phase 6 - explicit web access
[ ] define web access as separate command/tool
[ ] keep web use opt-in and visible
[ ] define output format for saved web results
[ ] avoid hidden web behavior in normal chat flow

to be prioritized (tbp)

session model
[ ] change session storage from raw message list to session object
[ ] preserve backward compatibility for current session files if practical
[ ] add session-level metadata
[ ] add summary field to session file shape

memory / summaries
[ ] define simple summary format
[ ] add manual summarize command
[ ] keep recent raw messages plus summary
[ ] define simple thresholds for later auto-summary

runtime / tooling
[ ] add status command
[ ] add doctor / smoke command
[ ] show ollama status
[ ] show configured model
[ ] show session/data path

storage
[ ] add config for data_root / sessions_dir overrides
[ ] prepare move to /mnt/data/ai/ollama_workbench
[ ] add migrate-sessions command

web access
[ ] define explicit web access as separate command/tool
[ ] keep web use opt-in and visible
[ ] define saved output format for web results

packaging / release
[ ] add console script entry point
[ ] install with pip/pipx locally
[ ] versioning approach

quality
[ ] add basic tests
[ ] add smoke test script
[ ] add sample config

future ui
[ ] richer cli output
[ ] tui exploration
[ ] web ui only if still wanted

integration
[ ] decide later how ollama_workbench may integrate with manumental-effort
[ ] keep integration at boundary, not shared mess
to be prioritized (tbp)

