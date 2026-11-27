# Puzzle JSON Schema (v1) — `type: "grid_logic"`

One file per puzzle. Store puzzles under `puzzles/**/*.json` anywhere in the
project (the test suite discovers them automatically).

```json
{
  "id": "LGP-0001",
  "title": "The Garden Club",
  "type": "grid_logic",
  "story": "Optional free text shown to the solver. Used in duplicate checks.",
  "categories": [
    {"name": "name",  "options": ["Ada", "Boris", "Cleo", "Dan"]},
    {"name": "pet",   "options": ["cat", "dog", "fox", "owl"]},
    {"name": "color", "options": ["red", "blue", "green", "gold"]}
  ],
  "clues": [
    {"type": "same", "a": "Ada", "b": "cat"},
    {"type": "not",  "a": "Boris", "b": "red"},
    {"type": "or",   "pairs": [["Ada", "cat"], ["Boris", "cat"]]},
    {"type": "xor",  "pairs": [["Dan", "owl"], ["Dan", "dog"]]}
  ],
  "solution": {
    "Ada":   {"pet": "cat", "color": "red"},
    "Boris": {"pet": "dog", "color": "blue"},
    "Cleo":  {"pet": "fox", "color": "green"},
    "Dan":   {"pet": "owl", "color": "gold"}
  }
}
```

## Rules

- **Categories:** the first category defines the "rows" of the grid (its options
  are the keys of `solution`). Every category must have the same number of
  options (2–6 recommended for solvability proof).
- **Option labels** must be unique across ALL categories — clues reference
  options by label alone.
- **Clue types:**
  - `same`: option `a` is in the same row as option `b`
  - `not`: option `a` is NOT in the same row as `b`
  - `or`: at least one listed `[a, b]` pair shares a row
  - `xor`: exactly one listed `[a, b]` pair shares a row
  - Both members of a pair must come from different categories.
- **solution:** keyed by first-category options; each row maps every other
  category name to the option placed in that row. Every option must be used
  exactly once.

## What the validator proves vs. flags

| Check | Kind |
|---|---|
| Schema/shape valid, clue refs exist | PROVEN (fail = defect) |
| ≥1 solution exists | PROVEN |
| Exactly 1 solution (uniqueness) | PROVEN |
| Published `solution` satisfies all clues | PROVEN |
| Published `solution` equals the computed solution | PROVEN |
| Directly contradictory clues (`same`+`not` on same pair) | PROVEN |
| Redundant clue (removing it keeps solution unique) | EDITORIAL |
| Exact/near-duplicate puzzles or clue sets in corpus | EDITORIAL |
| Reused names/options/story passages across puzzles | EDITORIAL |

EDITORIAL flags mean "a human should look" — they are heuristics, not proofs.
If the search space exceeds the safety cap, uniqueness is reported as
UNPROVEN rather than guessed.
