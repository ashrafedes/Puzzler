---
name: mystery-factory
description: >
  MYSTERY_FACTORY — produce mystery/logic-puzzle books with solver-verified
  answers. Invoke when the user message contains MYSTERY_FACTORY, asks to
  create logic-puzzle books/cases, or mentions mystery factory operations.
triggers:
  - user
  - model
---

# MYSTERY_FACTORY — Mystery Logic Puzzle Factory (v1.0.0)

If the user's message starts with or contains the keyword `MYSTERY_FACTORY`,
this factory owns the request. Deterministic invocation: `/mystery-factory`.

Factory home: `factories/mystery_logic_puzzle/` (see `FACTORY.yaml`,
`README.md`, `stages/`). Never load prompts, schemas, or state from another
factory — isolation is enforced by `platform/projects.py` (loading a project
under the wrong factory aborts with ISOLATION).

## Ops grammar → real commands

All ops run the platform CLI from the project root. `PID` = project id
(e.g. `MLP-0001`); factory is inferred from the PID prefix.

| User writes | You run |
|---|---|
| `MYSTERY_FACTORY factory list` | `python -m bookplatform.cli factory list` |
| `MYSTERY_FACTORY factory show` | `python -m bookplatform.cli factory show MYSTERY_FACTORY` |
| `MYSTERY_FACTORY Create <brief>` | `python -m bookplatform.cli book new --factory MYSTERY_FACTORY --title "<title>"` then intake: ask for missing spec essentials (stages/01_brief.md) — never invent them |
| `... STATUS <PID>` | `python -m bookplatform.cli book status <PID>` |
| `... RESUME <PID>` | `python -m bookplatform.cli book resume <PID>` then continue from `next_action` |
| `... VALIDATE <PID>` | `python -m bookplatform.cli book validate <PID>` |
| `... REVIEW <PID>` | `python -m bookplatform.cli book review <PID>`; after performing the rubric in `stages/06_editorial.md`, record with `--set editorial_review=pass --evidence "<what was actually reviewed>"` |
| `... REVISE <PID> <artifact>` | `python -m bookplatform.cli book revise <PID> <artifact>` then redo and re-validate |
| `... ASSEMBLE <PID>` | `python -m bookplatform.cli book assemble <PID>` |
| `... EXPORT <PID>` | `python -m bookplatform.cli book export <PID>` (blocks until all gates pass + `book approve --gate ship_approval`) |

## Production rules

- Follow `factories/mystery_logic_puzzle/stages/` in order; checkpoint via
  the CLI after each stage.
- Puzzles are written by you under `prompts/*_v1.md`; **proven by
  `checks/check_puzzles.py` (independent solver)** — never by your own say-so.
- A puzzle that fails validation stays failed: fix it within the retry budget
  (`spec.quality.max_case_retries`) or park it under `cases/_failed/` and
  report it. Never force-accept.
- Gate classes: CODE = machine-checked and blocking; EDITORIAL = your
  judgment, labeled as such; HUMAN = user approval required. Export has no
  override.
- On resume: run `book resume` first; trust `qc/` reports only if newer than
  the artifacts they cover (`check_book` enforces freshness).
