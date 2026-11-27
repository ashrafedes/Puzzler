#!/usr/bin/env python3
"""bookqc.py - evidence helpers for the /write-book pipeline.

  bookqc.py snapshot <book-dir> <rev-id> [--scope P ...] [--na PATH=REASON ...] [--whole-book]
  bookqc.py verify   <book-dir> <manifest.md>
  bookqc.py count    <file.md> [<file.md> ...]

IMPORTANT: a CURRENT result means only that file bytes match a manifest, and a word
count is only a diagnostic. Neither is approval of book quality; approval comes from
the inspection and review reports (see SKILL.md).

snapshot  Writes qc/snapshots/<rev-id>.md (SHA-256 + relative path). Default scope:
          intake_answers.md, plan, research, manuscript, images. FAILS (no manifest
          written, exit 2) if any scope entry is missing, unless declared with
          --na PATH=REASON. With --whole-book it also requires plan/spec.md to hold a
          ```manifest fenced block (one relative path per line, build order) and fails
          if a listed file is missing or empty, if a manuscript/*.md file is not
          listed, or if manuscript files contain [verify], TODO, TBD or [placeholder].
verify    Recomputes hashes. Exit 1 on CHANGED/ADDED/REMOVED files, on a manifest that
          recorded missing scope entries without --na, and (for whole-book manifests)
          when the plan-completeness checks fail now.
count     Body words and visible words (approximate, same method for every chapter):
          body = narrative paragraphs and blockquotes; excludes headings, list items,
          table rows, captions (Figure/Table/Source), fenced code, image markup, URLs.
          visible = body + list items + table cells + captions.
"""
import argparse, datetime, hashlib, os, re, sys

DEFAULT_SCOPE = ["intake_answers.md", "plan", "research", "manuscript", "images"]
PLACEHOLDER = re.compile(r"\[verify\]|\bTODO\b|\bTBD\b|\[placeholder", re.I)

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def collect(book, scope):
    files = []
    for s in scope:
        p = os.path.join(book, s)
        if os.path.isfile(p):
            files.append(s)
        elif os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.relpath(os.path.join(root, n), book) for n in names]
    return sorted(set(files))

def plan_manifest(book):
    spec = os.path.join(book, "plan", "spec.md")
    if not os.path.isfile(spec):
        return None
    m = re.search(r"```manifest\s*\n(.*?)```", open(spec, encoding="utf-8").read(), re.S)
    if not m:
        return None
    return [l.strip() for l in m.group(1).splitlines() if l.strip() and not l.startswith("#")]

def whole_book_problems(book):
    problems = []
    listed = plan_manifest(book)
    if listed is None:
        return ["plan/spec.md has no ```manifest block (ordered file list); cannot prove completeness"]
    for rel in listed:
        p = os.path.join(book, rel)
        if not os.path.isfile(p):
            problems.append(f"planned file missing: {rel}")
        elif os.path.getsize(p) == 0:
            problems.append(f"planned file empty: {rel}")
    for rel in collect(book, ["manuscript"]):
        if rel.endswith(".md") and rel not in listed:
            problems.append(f"manuscript file not in plan manifest: {rel}")
    for rel in listed:
        p = os.path.join(book, rel)
        if os.path.isfile(p) and rel.endswith(".md"):
            for i, line in enumerate(open(p, encoding="utf-8"), 1):
                if PLACEHOLDER.search(line):
                    problems.append(f"placeholder marker at {rel}:{i}")
    return problems

def snapshot(book, rev, scope, na, whole):
    scope = scope or DEFAULT_SCOPE
    na_map = dict(x.split("=", 1) for x in na) if na else {}
    bad_na = [k for k, v in na_map.items() if not v.strip()]
    if bad_na:
        sys.exit(f"--na needs a reason: {bad_na}")
    missing = [s for s in scope if not os.path.exists(os.path.join(book, s)) and s not in na_map]
    problems = [f"required scope entry missing: {m}" for m in missing]
    if whole:
        problems += whole_book_problems(book)
    if problems:
        print("FAIL: snapshot not written")
        for p in problems:
            print("  -", p)
        sys.exit(2)
    dest = os.path.join(book, "qc", "snapshots", f"{rev}.md")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        sys.exit(f"refusing to overwrite {dest}; use a new revision id")
    files = collect(book, scope)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(dest, "w") as f:
        f.write(f"# Revision manifest\nbook: {os.path.basename(os.path.abspath(book))}\n"
                f"revision: {rev}\ncreated: {now}\nmode: {'whole-book' if whole else 'scoped'}\n"
                f"scope: {', '.join(scope)}\n"
                f"na: {'; '.join(f'{k}={v}' for k, v in na_map.items()) or 'none'}\n\n```\n")
        for rel in files:
            f.write(f"{sha(os.path.join(book, rel))}  {rel}\n")
        f.write("```\n")
    print(f"wrote {dest} ({len(files)} files, mode={'whole-book' if whole else 'scoped'})")

def parse_manifest(path):
    entries, meta, inblock = {}, {}, False
    for line in open(path):
        if line.startswith("```"):
            inblock = not inblock
        elif inblock and "  " in line:
            h, rel = line.rstrip("\n").split("  ", 1)
            entries[rel] = h
        elif ":" in line and not inblock:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    scope = [s.strip() for s in meta.get("scope", "").split(",") if s.strip()]
    return entries, scope, meta

def verify(book, manifest):
    old, scope, meta = parse_manifest(manifest)
    problems = []
    if "missing_scope_entries" in meta and meta["missing_scope_entries"] != "none":
        problems.append(f"manifest was created with missing entries: {meta['missing_scope_entries']}")
    na = meta.get("na", "none")
    na_paths = {x.split("=", 1)[0].strip() for x in na.split(";")} if na != "none" else set()
    for s in scope:
        if not os.path.exists(os.path.join(book, s)) and s not in na_paths:
            problems.append(f"required scope entry missing now: {s}")
    now = {r: sha(os.path.join(book, r)) for r in collect(book, scope)}
    for r in old:
        if r in now and old[r] != now[r]:
            problems.append(f"CHANGED: {r}")
        elif r not in now:
            problems.append(f"REMOVED: {r}")
    problems += [f"ADDED: {r}" for r in now if r not in old]
    if meta.get("mode") == "whole-book":
        problems += whole_book_problems(book)
    if problems:
        print("STALE/FAIL: evidence tied to this manifest must be re-checked")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"CURRENT: {len(old)} files match this manifest (hash match only; not a quality approval)")

URL = re.compile(r"https?://\S+")
def count(path):
    body = vis = 0
    fence = False
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s or s.startswith("![") or s.startswith("#"):
            continue
        s = URL.sub("", s)
        words = len(s.lstrip("> ").split()) if s.startswith(">") else len(re.sub(r"[*_`|]", " ", s).split())
        vis += words
        if not (re.match(r"([-*+]|\d+[.)])\s", s) or s.startswith("|") or re.match(r"\*?(Figure|Table|Source)\b", s)):
            body += words
    return body, vis

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("snapshot"); s.add_argument("book"); s.add_argument("rev")
    s.add_argument("--scope", nargs="+"); s.add_argument("--na", nargs="+"); s.add_argument("--whole-book", action="store_true")
    v = sub.add_parser("verify"); v.add_argument("book"); v.add_argument("manifest")
    c = sub.add_parser("count"); c.add_argument("files", nargs="+")
    a = ap.parse_args()
    if a.cmd == "snapshot":
        snapshot(a.book, a.rev, a.scope, a.na, a.whole_book)
    elif a.cmd == "verify":
        verify(a.book, a.manifest)
    else:
        for p in a.files:
            b, vv = count(p)
            print(f"{p}: body={b} visible={vv}")
