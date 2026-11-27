#!/usr/bin/env python3
"""
puzzle_qc.py — logic-grid-puzzle validator for this workspace.

For each puzzle JSON (schema: tools/puzzle_qc/SCHEMA.md) it proves or fails:
  solvable, uniquely solvable, published-answer correctness, clue sanity.
Separately it reports EDITORIAL warnings (near-duplicates, name reuse,
redundant clues) that need a human decision — never treated as proof.

Usage:
  python tools/puzzle_qc/puzzle_qc.py [files/dirs/globs ...]
      default scan: puzzles/**/*.json under the project root
  python tools/puzzle_qc/puzzle_qc.py --selftest   (validates the bundled samples)

Exit 0 = no PROVEN failures, 1 = at least one PROVEN failure.
"""
from __future__ import annotations
import itertools, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NODE_CAP = 2_000_000          # max solver states before declaring UNPROVEN
NEAR_DUP_JACCARD = 0.75


# ---------- schema ----------

def schema_errors(p: dict) -> list[str]:
    errs = []
    if not isinstance(p, dict):
        return ["file is not a JSON object"]
    for k in ("id", "title", "type", "categories", "clues", "solution"):
        if k not in p:
            errs.append(f"missing key '{k}'")
    if errs:
        return errs
    if p["type"] != "grid_logic":
        errs.append(f"unknown type '{p['type']}'")
    cats = p["categories"]
    if not isinstance(cats, list) or len(cats) < 2:
        errs.append("need >=2 categories")
        return errs
    sizes = {len(c.get("options", [])) for c in cats}
    if len(sizes) != 1:
        errs.append(f"category sizes differ: {sizes}")
    n = sizes.pop() if sizes else 0
    if not 2 <= n <= 8:
        errs.append(f"category size {n} outside 2..8")
    opts = [o for c in cats for o in c.get("options", [])]
    if len(opts) != len(set(opts)):
        errs.append("option labels must be unique across all categories")
    catname = {o: c["name"] for c in cats for o in c["options"]}

    def check_pair(pair, where):
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            errs.append(f"{where}: pair must be [opt, opt]")
            return
        a, b = pair
        for o in (a, b):
            if o not in catname:
                errs.append(f"{where}: unknown option '{o}'")
        if a in catname and b in catname and catname[a] == catname[b]:
            errs.append(f"{where}: '{a}' and '{b}' are in the same category "
                        f"'{catname[a]}'")

    for i, cl in enumerate(p["clues"]):
        t, where = cl.get("type"), f"clue[{i}]"
        if t in ("same", "not"):
            check_pair([cl.get("a"), cl.get("b")], where)
        elif t in ("or", "xor"):
            if not isinstance(cl.get("pairs"), list) or len(cl["pairs"]) < 2:
                errs.append(f"{where}: '{t}' needs >=2 pairs")
            else:
                for j, pr in enumerate(cl["pairs"]):
                    check_pair(pr, f"{where}.pairs[{j}]")
        else:
            errs.append(f"{where}: unknown type '{t}'")

    sol = p["solution"]
    base = cats[0]["options"]
    if isinstance(sol, dict):
        if set(sol.keys()) != set(base):
            errs.append(f"solution keys != first-category options "
                        f"(missing {set(base) - set(sol.keys()) or 'none'})")
        used = {c["name"]: [] for c in cats[1:]}
        for row, cells in sol.items():
            if not isinstance(cells, dict):
                errs.append(f"solution['{row}'] must be an object")
                continue
            if set(cells.keys()) != set(used.keys()):
                errs.append(f"solution['{row}'] must assign each of {sorted(used)}")
            for cn, o in cells.items():
                if o in catname and catname[o] == cn:
                    used[cn].append(o)
                else:
                    errs.append(f"solution['{row}']['{cn}'] = '{o}' "
                                f"is not an option of '{cn}'")
        for cn, lst in used.items():
            if sorted(lst) != sorted(next(c["options"] for c in cats if c["name"] == cn)):
                errs.append(f"solution does not use each '{cn}' option exactly once")
    else:
        errs.append("solution must be an object")
    return errs


# ---------- model & solver ----------

def build_model(p):
    cats = p["categories"]
    base = cats[0]["options"]
    others = [c["options"] for c in cats[1:]]
    row_of = {o: i for i, o in enumerate(base)}     # base opts fixed to their row
    return {"cats": cats, "base": base, "others": others,
            "n": len(base), "row_of": dict(row_of),
            "catname": {o: c["name"] for c in cats for o in c["options"]}}


def _pairs_of(clue):
    if clue["type"] in ("same", "not"):
        return [(clue["a"], clue["b"])]
    return [tuple(pr) for pr in clue["pairs"]]


def clue_status(clue, row_of) -> str:
    """'satisfied' | 'violated' | 'pending' under a partial opt->row map."""
    t = clue["type"]
    if t in ("same", "not"):
        a, b = clue["a"], clue["b"]
        if a not in row_of or b not in row_of:
            return "pending"
        same = row_of[a] == row_of[b]
        if (same and t == "not") or (not same and t == "same"):
            return "violated"
        return "satisfied"
    decided_true = undecided = 0
    for a, b in _pairs_of(clue):
        if a not in row_of or b not in row_of:
            undecided += 1
        elif row_of[a] == row_of[b]:
            decided_true += 1
    if t == "or":
        if decided_true >= 1:
            return "satisfied"
        return "pending" if undecided else "violated"
    # xor
    if decided_true > 1 or (undecided == 0 and decided_true == 0):
        return "violated"
    if undecided == 0 and decided_true == 1:
        return "satisfied"
    return "pending"


def solve(p, max_solutions=2, node_cap=NODE_CAP):
    """Return (solutions, nodes, capped). Stops early at max_solutions."""
    m = build_model(p)
    clues, others, n = p["clues"], m["others"], m["n"]
    row0 = dict(m["row_of"])
    sols, nodes = [], [0]

    def rec(k, row_of):
        if nodes[0] > node_cap or len(sols) >= max_solutions:
            return
        nodes[0] += 1
        if any(clue_status(c, row_of) == "violated" for c in clues):
            return
        if k == len(others):
            if all(clue_status(c, row_of) == "satisfied" for c in clues):
                sols.append(dict(row_of))
            return
        for perm in itertools.permutations(others[k]):
            ext = dict(row_of)
            ext.update({o: i for i, o in enumerate(perm)})
            rec(k + 1, ext)
            if len(sols) >= max_solutions or nodes[0] > node_cap:
                return
    rec(0, row0)
    return sols, nodes[0], nodes[0] > node_cap


def search_space(p):
    m = build_model(p)
    import math
    return math.factorial(m["n"]) ** max(0, len(m["others"]))


def solution_assignment(p):
    """Published solution -> opt->row map (or None if malformed)."""
    m = build_model(p)
    row_of = dict(m["row_of"])
    try:
        for base_opt, cells in p["solution"].items():
            r = m["row_of"][base_opt]
            for _, o in cells.items():
                row_of[o] = r
        return row_of
    except Exception:
        return None


def static_contradictions(p):
    bad = set()
    sames = {tuple(sorted(_pairs_of(c)[0])) for c in p["clues"] if c["type"] == "same"}
    for c in p["clues"]:
        if c["type"] == "not" and tuple(sorted(_pairs_of(c)[0])) in sames:
            bad.add(f"'{_pairs_of(c)[0]}' declared both same and not")
    return sorted(bad)


# ---------- per-puzzle analysis ----------

def analyze(p: dict) -> dict:
    pid = p.get("id", "?") if isinstance(p, dict) else "?"
    rep = {"id": pid, "proven_failures": [], "editorial": [],
           "solutions": None, "unique": None, "metrics": None}
    errs = schema_errors(p)
    if errs:
        rep["proven_failures"] += [f"schema: {e}" for e in errs]
        return rep
    for c in static_contradictions(p):
        rep["proven_failures"].append(f"contradictory clues: {c}")

    space = search_space(p)
    if space > NODE_CAP:
        rep["proven_failures"].append(
            f"UNPROVEN: search space ~{space:,} exceeds cap {NODE_CAP:,}; "
            f"cannot certify solvability/uniqueness")
        return rep

    sols, nodes, capped = solve(p, max_solutions=2)
    rep["solutions"] = len(sols)
    if capped and len(sols) < 2:
        rep["proven_failures"].append("UNPROVEN: solver hit node cap before "
                                      "proving uniqueness")
        return rep
    if len(sols) == 0:
        rep["proven_failures"].append("no solution exists")
    elif len(sols) > 1:
        rep["proven_failures"].append(f"not unique: >=2 solutions "
                                      f"(found {len(sols)} before early stop)")
        rep["unique"] = False
    else:
        rep["unique"] = True

    if rep["unique"]:
        rep["metrics"] = deduction_metrics(p)

    pub = solution_assignment(p)
    if pub is None:
        rep["proven_failures"].append("published solution is malformed")
    else:
        bad = [i for i, c in enumerate(p["clues"])
               if clue_status(c, pub) != "satisfied"]
        if bad:
            rep["proven_failures"].append(
                f"published solution violates clue(s) {bad}")
        if rep["unique"] and pub != sols[0]:
            rep["proven_failures"].append(
                "published solution != the unique computed solution")

    # redundancy is informational only — never a failure
    if rep["unique"] and len(p["clues"]) > 1:
        for i in range(len(p["clues"])):
            sub = dict(p)
            sub["clues"] = [c for j, c in enumerate(p["clues"]) if j != i]
            if search_space(sub) <= NODE_CAP:
                s2, _, _ = solve(sub, max_solutions=2)
                if len(s2) == 1:
                    rep["editorial"].append(f"clue[{i}] is redundant "
                                            "(removing it keeps the solution unique)")
    return rep


# ---------- human-style propagation solver & deduction metrics ----------

def _propagate(p, givens=None, used=None, clues=None):
    """Deterministic propagation over possible[opt] = set(rows).
    Returns (solved_row_of or None, rounds, stall_possible).
    used (set): clue indices that produced a derivation (path-contributing).
    clues: optional subset (default all) — used to verify cited-clue support."""
    m = build_model(p)
    clues = p["clues"] if clues is None else clues
    base, others, n = m["base"], m["others"], m["n"]
    catof = m["catname"]
    possible = {o: set(range(n)) for cat in others for o in cat}
    for i, o in enumerate(base):
        possible[o] = {i}   # base opts are fixed to their own row
    # pre-place: each option of a category excludes its rivals per row implicitly
    def assign(o, r, why):
        if len(possible[o]) == 1 and r in possible[o]:
            return True
        possible[o] = {r}
        for o2 in (x for c in m["cats"] if c["name"] == catof[o]
                   for x in c["options"] if x != o):
            possible[o2].discard(r)
        return True
    def collapse():
        changed = False
        for c in m["cats"][1:]:
            for r in range(n):
                cand = [o for o in c["options"] if r in possible[o]]
                if len(cand) == 0:
                    return "contradiction", False
                if len(cand) == 1 and len(possible[cand[0]]) > 1:
                    assign(cand[0], r, "hidden"); changed = True
        return None, changed
    # givens = list of facts treated as derived knowledge:
    #   (option, row)            -> forced placement
    #   (option, row, False)     -> proven exclusion (case-split elimination)
    for g in (givens or []):
        o, r = g[0], g[1]
        if len(g) > 2 and g[2] is False:
            possible[o].discard(r)
            if not possible[o]:
                return None, 0, None
            continue
        if r not in possible[o]:
            return None, 0, None
        assign(o, r, "given")
    row_of = dict(m["row_of"])  # base opts fixed
    rounds = 0
    def rows(o): return possible[o]
    def certain_same(a, b):
        return rows(a) & rows(b)
    while True:
        rounds += 1
        before = {o: frozenset(s) for o, s in possible.items()}
        for i, cl in enumerate(clues):
            t = cl["type"]
            def note(): used is not None and used.add(i)
            if t in ("same", "not"):
                a, b = cl["a"], cl["b"]
                if t == "same":
                    inter = rows(a) & rows(b)
                    if not inter: return None, rounds, None
                    if rows(a) - inter or rows(b) - inter:
                        possible[a] &= inter; possible[b] &= inter; note()
                else:
                    for x, y in ((a, b), (b, a)):
                        if len(rows(x)) == 1:
                            r = next(iter(rows(x)))
                            if r in rows(y):
                                possible[y].discard(r); note()
                                if not rows(y): return None, rounds, None
                        elif rows(y) == rows(x) and rows(x):
                            # x,y must occupy different rows; if y's rows ⊆ x's single-row case handled above
                            pass
                continue
            pairs = [tuple(pr) for pr in cl["pairs"]]
            live = [pr for pr in pairs if rows(pr[0]) & rows(pr[1])]
            true = [pr for pr in live
                    if len(rows(pr[0])) == 1 and rows(pr[0]) == rows(pr[1])]
            if t == "or":
                if true: continue
                if not live: return None, rounds, None
                if len(live) == 1:
                    a, b = live[0]
                    inter = rows(a) & rows(b)
                    possible[a] &= inter; possible[b] &= inter; note()
            else:  # xor
                if len(true) > 1:
                    return None, rounds, None   # two true pairs — violated
                if true:
                    dead = [pr for pr in live if pr != true[0]]
                    for a, b in dead:
                        if len(rows(a)) == 1:
                            r = next(iter(rows(a)))
                            possible[b].discard(r); note()
                            if not rows(b): return None, rounds, None
                        elif len(rows(b)) == 1:
                            r = next(iter(rows(b)))
                            possible[a].discard(r); note()
                            if not rows(a): return None, rounds, None
                    continue
                if not live or len(live) > 1 and len(live) == len(pairs):
                    pass
                if len(live) == 1:
                    a, b = live[0]
                    inter = rows(a) & rows(b)
                    possible[a] &= inter; possible[b] &= inter; note()
        res, changed = collapse()
        if res == "contradiction":
            return None, rounds, None
        if all(len(s) == 1 for s in possible.values()):
            ro = dict(row_of)
            for o, s in possible.items():
                ro[o] = next(iter(s))
            # a completed grid must satisfy every clue — a clause may have been
            # processed before the placements that violate it became final
            if all(clue_status(cl, ro) == "satisfied" for cl in clues):
                return ro, rounds, possible
            return None, rounds, None  # completed grid violates a clue
        if {o: frozenset(s) for o, s in possible.items()} == before:
            return None, rounds, possible  # stalled


def _case_split(p, depth, cap, stats, givens=None, clues=None):
    """Depth-limited branching on top of propagation.
    Returns (solution_row_of_or_None, min_branch_depth_or_None, status)
    status: 'solved' | 'dead' (all branches contradicted) | 'unknown' (cap)."""
    m = build_model(p)
    sol, rounds, poss = _propagate(p, givens=givens, clues=clues)
    stats["rounds"] += rounds
    if sol is not None:
        return sol, 0, "solved"
    if poss is None:
        return None, None, "dead"
    if depth >= cap:
        return None, None, "unknown"
    undecided = [o for o, s in poss.items() if len(s) > 1]
    if not undecided:
        return None, None, "unknown"
    o = min(undecided, key=lambda x: len(poss[x]))
    any_unknown = False
    for r in sorted(poss[o]):
        sub, dd, st = _case_split(p, depth + 1, cap, stats,
                                  givens=(givens or []) + [(o, r)],
                                  clues=clues)
        if st == "solved":
            stats["post_branch"] += len(sub) - len(m["base"])
            return sub, (dd + 1) if dd is not None else 1, "solved"
        if st == "unknown":
            any_unknown = True
    return None, None, "unknown" if any_unknown else "dead"


def deduction_metrics(p, cap=5):
    """Provisional metrics — calibrated heuristics, not proofs of difficulty.
    Reports: solver_method, propagation_rounds, case_split_depth,
    post_branch_derivations, direct_pins, direct_ratio, clue classes."""
    m = build_model(p)
    n = m["n"]
    used = set()
    stats = {"rounds": 0, "post_branch": 0}
    sol, rounds, poss = _propagate(p, used=used)
    stats["rounds"] = rounds
    method, cs_depth = "propagation_only", None
    if sol is None:
        sub, dd, st = _case_split(p, 0, cap, stats)
        if st == "solved":
            method, cs_depth = "case_split", max(dd or 1, 1)
            sol = sub
        else:
            method = "unproven"  # cannot measure depth reliably
    cells = n * max(0, len(m["others"]))
    direct = 0
    base_set = set(m["base"])
    for cl in p["clues"]:
        if cl["type"] == "same":
            a, b = cl["a"], cl["b"]
            if a in base_set or b in base_set:
                direct += 1  # a base<->other same-clue directly states a cell
    # clue classification
    cls = {"essential_for_uniqueness": [], "direct_assignment": [],
           "path_contributing": [], "decorative": []}
    for i, cl in enumerate(p["clues"]):
        if i in used:
            cls["path_contributing"].append(i)
        if cl["type"] == "same" and (cl["a"] in base_set or cl["b"] in base_set):
            cls["direct_assignment"].append(i)
        sub = dict(p); sub["clues"] = [c for j, c in enumerate(p["clues"]) if j != i]
        if search_space(sub) <= NODE_CAP:
            s2, _, _ = solve(sub, max_solutions=2)
            if len(s2) != 1:
                cls["essential_for_uniqueness"].append(i)
        if i not in used and i not in cls["direct_assignment"]:
            cls["decorative"].append(i)
    return {"solver_method": method, "propagation_rounds": rounds,
            "case_split_depth": cs_depth,
            "post_branch_derivations": stats["post_branch"],
            "direct_pins": direct, "total_cells": cells,
            "direct_ratio": round(direct / cells, 3) if cells else 0,
            "clue_classes": cls,
            "redundant_frac": round(
                sum(1 for i in range(len(p["clues"]))
                    if i not in cls["essential_for_uniqueness"])
                / max(1, len(p["clues"])), 3),
            "provisional": True}


def derived_facts(p, givens=None, clues=None):
    """(solved_row_of|None, {opt: row} forced placements, stall_possible|None).
    Forced = every option whose possible rows collapsed to a singleton under
    deterministic propagation. Used by hint/explanation replay checks."""
    sol, _rounds, poss = _propagate(p, givens=givens, clues=clues)
    if sol is not None:
        return sol, dict(sol), None
    forced = {o: next(iter(s)) for o, s in (poss or {}).items() if len(s) == 1}
    return None, forced, poss


# ---------- corpus / duplicate checks ----------

def _norm_text(s):
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).split()


def _clue_key(c):
    if c["type"] in ("same", "not"):
        return (c["type"], tuple(sorted((str(c["a"]), str(c["b"])))))
    return (c["type"], tuple(sorted(tuple(sorted(map(str, pr))) for pr in c["pairs"])))


def structure_signature(p):
    cats = tuple(sorted((c["name"], tuple(sorted(c["options"]))) for c in p["categories"]))
    clues = tuple(sorted(_clue_key(c) for c in p["clues"]))
    return (cats, clues)


def corpus_warnings(puzzles: list[dict]) -> dict:
    """Return {id: [editorial warnings...]} comparing puzzles against each other."""
    out = {}
    sigs, clue_sets, names, stories = {}, {}, {}, {}
    for p in puzzles:
        pid = p.get("id", "?")
        sigs[pid] = structure_signature(p)
        clue_sets[pid] = set(_clue_key(c) for c in p["clues"])
        names[pid] = {o for c in p["categories"] for o in c["options"]}
        stories[pid] = _norm_text(p.get("story", ""))
    ids = [p.get("id", "?") for p in puzzles]
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if sigs[a] == sigs[b]:
                out.setdefault(a, []).append(f"exact structural duplicate of {b}")
                out.setdefault(b, []).append(f"exact structural duplicate of {a}")
                continue
            ca, cb = clue_sets[a], clue_sets[b]
            if ca and cb:
                j = len(ca & cb) / len(ca | cb)
                if j >= NEAR_DUP_JACCARD:
                    msg = f"clue set {j:.0%} identical to {b} (>= {NEAR_DUP_JACCARD:.0%})"
                    out.setdefault(a, []).append(msg)
                    out.setdefault(b, []).append(msg.replace(str(b), str(a)))
            na, nb = names[a] & names[b], names[a] | names[b]
            if nb and len(na) / len(nb) >= 0.5:
                msg = f"option/name overlap with {b}: {sorted(na)[:6]}"
                out.setdefault(a, []).append(msg)
                out.setdefault(b, []).append(msg.replace(str(b), str(a)))
            sa, sb = stories[a], stories[b]
            if sa and sb and sa == sb:
                out.setdefault(a, []).append(f"identical story text to {b}")
                out.setdefault(b, []).append(f"identical story text to {a}")
    return out


# ---------- CLI ----------

def iter_puzzle_files(args):
    files = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            files += sorted(p.rglob("*.json"))
        elif p.is_file():
            files.append(p)
        else:
            files += sorted(ROOT.glob(a))
    seen, out = set(), []
    for f in files:
        if f not in seen:
            seen.add(f); out.append(f)
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    if "--selftest" in sys.argv or not args:
        args = args or [str(ROOT / "puzzles")]
        if "--selftest" in sys.argv:
            args = [str(Path(__file__).parent / "sample_puzzles")]
    files = iter_puzzle_files(args)
    if not files:
        print(f"no puzzle files found under: {args}")
        sys.exit(0)

    puzzles, reps, parse_fail = [], [], 0
    for f in files:
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            reps.append({"id": f.name, "proven_failures": [f"unparseable JSON: {e}"],
                         "editorial": [], "solutions": None, "unique": None})
            parse_fail += 1
            continue
        p.setdefault("id", f.stem)
        r = analyze(p)
        r["_file"] = str(f)
        reps.append(r)
        if not r["proven_failures"]:
            puzzles.append(p)

    for pid, warns in corpus_warnings(puzzles).items():
        for r in reps:
            if r["id"] == pid:
                r["editorial"] += warns

    nfail = 0
    for r in reps:
        status = "FAIL" if r["proven_failures"] else \
                 "WARN" if r["editorial"] else "PASS"
        if r["proven_failures"]:
            nfail += 1
        print(f"[{status}] {r['id']}  solutions={r['solutions']} unique={r['unique']}")
        for e in r["proven_failures"]:
            print(f"       PROVEN-FAIL: {e}")
        for w in r["editorial"]:
            print(f"       EDITORIAL:   {w}")
    print(f"== {len(reps)} puzzle(s): {nfail} proven failure(s), "
          f"{sum(bool(r['editorial']) for r in reps)} with editorial flags ==")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
