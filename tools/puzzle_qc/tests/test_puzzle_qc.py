"""Tests for the logic-puzzle validator.

Runs against the bundled fixtures (proving the harness itself works) and
discovers real puzzles under <project>/puzzles/**/*.json when they exist.
"""
import json, sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import puzzle_qc as qc  # noqa: E402

SAMPLES = HERE.parent / "sample_puzzles"
ROOT = HERE.parents[2]


def load(name):
    return json.loads((SAMPLES / name).read_text(encoding="utf-8"))


# --- fixture-based checks: prove the validator works ---

def test_valid_fixture_unique_and_answered():
    rep = qc.analyze(load("valid_4x3.json"))
    assert rep["proven_failures"] == [], rep
    assert rep["unique"] is True
    assert rep["solutions"] == 1


def test_ambiguous_puzzle_is_flagged():
    rep = qc.analyze(load("multi_solution.json"))
    assert rep["unique"] is False
    assert any("not unique" in e for e in rep["proven_failures"])


def test_wrong_published_answer_is_flagged():
    rep = qc.analyze(load("wrong_answer.json"))
    assert rep["unique"] is True          # puzzle itself is fine
    assert any("published solution" in e for e in rep["proven_failures"])


def test_bad_option_reference_is_flagged():
    rep = qc.analyze(load("bad_reference.json"))
    assert any("unknown option" in e for e in rep["proven_failures"])


def test_contradictory_clues_detected():
    p = load("valid_4x3.json")
    p["clues"] = [
        {"type": "same", "a": "Ada", "b": "cat"},
        {"type": "not", "a": "Ada", "b": "cat"},
    ]
    rep = qc.analyze(p)
    assert any("contradictory" in e for e in rep["proven_failures"])


def test_unsolvable_puzzle_detected():
    p = load("valid_4x3.json")
    p["clues"] = [
        {"type": "same", "a": "Ada", "b": "cat"},
        {"type": "same", "a": "Ada", "b": "dog"},  # Ada can't have two pets
        {"type": "same", "a": "cat", "b": "red"},
    ]
    rep = qc.analyze(p)
    assert any("no solution" in e for e in rep["proven_failures"])


# --- duplicate / editorial checks ---

def test_exact_duplicate_detected():
    p1, p2 = load("valid_4x3.json"), load("valid_4x3.json")
    p2["id"] = "COPY-001"
    warns = qc.corpus_warnings([p1, p2])
    assert any("duplicate" in w for w in warns.get("SAMPLE-VALID-001", []))
    assert any("duplicate" in w for w in warns.get("COPY-001", []))


def test_distinct_puzzles_not_flagged_as_duplicates():
    p1 = load("valid_4x3.json")
    p2 = load("valid_4x3.json")
    p2["id"] = "OTHER"
    p2["clues"] = [{"type": "same", "a": "Ada", "b": "red"}]
    p2["story"] = "A completely different setup about racing pigeons."
    warns = qc.corpus_warnings([p1, p2])
    assert not any("duplicate" in w or "identical" in w
                   for w in warns.get("OTHER", []))


# --- corpus discovery: real puzzles when they exist ---

def corpus_files():
    d = ROOT / "puzzles"
    return sorted(d.rglob("*.json")) if d.is_dir() else []


@pytest.mark.parametrize("path", corpus_files() or [pytest.param(None, marks=pytest.mark.skip(reason="no puzzles/ corpus yet"))])
def test_corpus_puzzle(path):
    p = json.loads(Path(path).read_text(encoding="utf-8"))
    p.setdefault("id", Path(path).stem)
    rep = qc.analyze(p)
    assert rep["proven_failures"] == [], f"{path}: {rep['proven_failures']}"


def test_corpus_duplicates():
    files = corpus_files()
    if len(files) < 2:
        pytest.skip("need >=2 real puzzles for corpus checks")
    puzzles = [json.loads(Path(f).read_text(encoding="utf-8")) for f in files]
    for p, f in zip(puzzles, files):
        p.setdefault("id", Path(f).stem)
    warns = qc.corpus_warnings(puzzles)
    dups = {k: v for k, v in warns.items()
            if any("duplicate" in w for w in v)}
    assert not dups, f"duplicate puzzles found: {dups}"
