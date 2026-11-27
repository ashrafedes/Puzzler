# Puzzle QC — logic-grid-puzzle validation

Proves (in code, not by model opinion) that each published puzzle is solvable,
uniquely solvable, and that the printed answer matches the computed one.
Editorial flags (near-duplicates, reused names/stories, redundant clues) are
reported separately for human review and never counted as proof.

## Commands

```bash
# validate every puzzle under puzzles/**/*.json
python tools/puzzle_qc/puzzle_qc.py

# validate specific files / dirs / globs
python tools/puzzle_qc/puzzle_qc.py puzzles/book1 puzzles/book2/LGP-*.json

# run on the bundled sample fixtures (self-test of the validator)
python tools/puzzle_qc/puzzle_qc.py --selftest

# pytest suite (fixtures + corpus discovery)
python -m pytest tools/puzzle_qc/tests -v
```

## Output format

```
[PASS] LGP-0001  solutions=1 unique=True
[WARN] LGP-0002  solutions=1 unique=True
       EDITORIAL:   clue[3] is redundant (removing it keeps the solution unique)
[FAIL] LGP-0003  solutions=2 unique=False
       PROVEN-FAIL: not unique: >=2 solutions (found 2 before early stop)
== 3 puzzle(s): 1 proven failure(s), 1 with editorial flags ==
```

- **PROVEN-FAIL** = a defect the code verified. The puzzle must not ship.
- **EDITORIAL** = heuristic flag for human judgement (possible duplication,
  name reuse, redundant clue). Not a defect by itself.
- **UNPROVEN** = the search space exceeded the safety cap, so uniqueness could
  not be certified. Never treated as valid.

Puzzle format: see `SCHEMA.md`. Puzzle files live in `puzzles/**/*.json`
(anywhere in the project). None exist yet — the bundled `sample_puzzles/`
fixtures demonstrate one valid puzzle and three kinds of detected defects.
