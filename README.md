# local_ai

Local Ollama-first CLI workbench.

## Overview

A small, explicit, CLI-first tool for working with local LLMs via Ollama.

Design goals:
- explicit behavior (no hidden magic)
- inspectable session memory
- simple, understandable code
- model-swappable runtime

## Features (current)

- local prompt/chat via Ollama
- structured JSON output
- tool calling
- file-backed session memory
- named sessions (`--session`)
- session stats and listing

## Run from source

From repo root:

```bash
PYTHONPATH=src python3 -m local_ai.cli sessions
PYTHONPATH=src python3 -m local_ai.cli stats
PYTHONPATH=src python3 -m local_ai.cli chat "hello" --session scratch
