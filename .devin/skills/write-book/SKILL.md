---
name: write-book
description: >
  Produces and audits nonfiction books or novels through evidence-gated intake,
  planning, chapter writing, inspection, independent review, and KDP packaging.
  Use when writing, producing, resuming, or checking a book production pipeline.
argument-hint: "start a new book, resume <book-dir>, or audit <book-dir>"
---

# /write-book — Evidence-gated Book Production (v2)

## Scope and precedence

This file coordinates the stages. It is an instruction-based orchestrator, not an
installed executable gate. Never describe these instructions as automated
validation unless real checks were run and their output saved. The helper
`bookqc.py` (snapshot, verify, count), located inside this skill folder, makes the hash and word-count
evidence real; use it instead of estimating.

Read the relevant stage file before executing that stage. These rules apply even
when an older plan is less strict. User-approved scope changes must be recorded;
never lower a requirement merely to pass a failing draft. For prose books, do not
use the coloring-book `kdp-book` workflow. Follow higher-priority permissions and
billing rules; do not spawn subagents without explicit user permission. A
separate user-opened review session is valid.

## Non-negotiable acceptance rules

1. Gather intake in one consolidated round using `intake.md`. Reuse recorded
   answers on resume. If an essential fact, permission, or author source later
   proves missing, ask only the focused blocking question and pause that work.
   Never invent an answer to keep work moving.
2. Final print page count must be within ±5% of intake. Estimated pages are
   provisional; only the rendered interior establishes the final count.
3. Each chapter must satisfy its content contract. Word count is a diagnostic,
   not proof of quality. Default body-word range is 85–115% of target unless the
   plan sets a different, justified range for that chapter; outside it, return to
   planning before acceptance. No padding or layout tricks.
4. BLOCKER and MAJOR findings prevent approval and final packaging. A retry limit
   stops work; it never converts failure into permission to ship.
5. A draft, a folder, an estimate, or an old report is not evidence of approval.
   Reports must identify the exact files reviewed and their SHA-256 snapshot.
6. Do not fabricate author experience, statistics, sources, reviewer responses,
   tool runs, or approvals. Label constructed scenarios as illustrative at use.
   Author biography alone does not substantiate a specific first-person story.
7. Preserve sources, intermediate files, reports, and earlier findings. Do not
   delete or overwrite user work destructively. Keep truthful provenance and
   comply with current platform disclosure requirements (see `kdp_output.md`);
   style rules never authorize concealing required disclosures.
8. Continue automatically only while evidence and permissions allow. At a
   blocker, record the reason and next action, notify the user, and stop the
   affected transition. Never report completion of unfinished stages.

## Nonfiction depth and learning progression

For this project's nonfiction books, produce a substantial information-rich
reference, not a simple introductory guide or an expanded outline. Build a
beginner-to-advanced learning path within the stated subject: foundations and
terminology → guided application → independent execution → complex cases,
diagnosis, optimization and professional judgment. Professional competence is a
learning objective, not a promised credential or guaranteed outcome from reading.

The plan must map each stage to chapters, prerequisites, observable capabilities,
worked examples and assessment evidence. Introduce essentials without assuming
unexplained jargon; do not let introductory explanations displace advanced depth.
Experienced readers need navigation to advanced material without repeated basics.

Explain mechanisms and trade-offs, compare viable approaches, show complete
calculations and decisions, and address uncertainty, constraints, failure recovery
and limits. Use progressively harder cases, completed artifacts and exercises
with answers or evaluation criteria. End with an integrated case that requires
choosing and defending an approach, not merely recalling definitions.

Depth is evaluated across the book and each chapter's assigned level, not by
forcing every chapter to repeat the whole progression. Superficial coverage of a
required level is a MAJOR finding even when word/page targets are met. If this
scope cannot fit the agreed page budget, report the conflict and seek an explicit
scope/page decision; never silently compress the book into a beginner summary,
add filler, or expand user requirements. Apply scene/character contracts instead
of this instructional progression to fiction.

## Working files

Use the selected `books/<slug>/` directory; do not mix evidence between books.
Create these artifacts when running production, not during a configuration-only edit:

- `intake_answers.md`: user answers, ACCEPTED_DEFAULT items, assumptions, open issues (separate sections).
- `plan/spec.md`: ordered file manifest, chapter contracts, budgets, research plan, metadata plan.
- `research/claim_register.md`: claim/story provenance and verification status.
- `research/`: source notes and underlying calculation/example data.
- `manuscript/`: chapter and front/back matter source files.
- `images/manifest.md`: planned assets, actual paths, captions, uses; record NONE if no images.
- `build/`: render scripts/config, preview builds (always unapproved).
- `qc/production_state.md`: current stage, chapter states, attempts, blockers, evidence paths, snapshots, next action.
- `qc/snapshots/`: revision manifests (produced by `BOOKQC snapshot`).
- `qc/chapters/<chapter-id>_inspection.md`: chapter evidence and findings history.
- `qc/inspector_report.md`: whole-book inspection and historical verdicts.
- `qc/review_report.md`: actual independent review, identity/method and coverage.
- `qc/preflight_report.md`: rendered-output checks and deliverable hashes.
- `final/`: approved requested deliverables only.

## Snapshot and status contract

**Tool path:** below, `BOOKQC` means `python "<skill-dir>/bookqc.py"`, where
`<skill-dir>` is the folder holding this SKILL.md; it is not relative to the book or
project root. If the file is not there, record BLOCKED for hash evidence and ask the
user to restore it; never substitute estimated hashes.

At every review handoff, run `BOOKQC snapshot <book-dir> <rev-id>` (use `--scope` for a
single chapter plus its dependencies, `--na PATH=REASON` for a genuinely inapplicable
input, and `--whole-book` for whole-book inspection, review and preflight). Snapshot
fails and writes nothing when a required entry is missing, when a file listed in the
```manifest block of `plan/spec.md` is missing or empty, when a manuscript file is not
listed, or when `[verify]`/TODO/TBD/placeholder markers remain. Manifests include
intake, spec, manuscript, claim register, source notes, image manifest and assets.
A missing required entry fails; record N/A with a reason only for genuinely
inapplicable inputs. Whole-book inspection and final review require the complete
planned source set. Reports cite their manifest and list every file covered.
Run `BOOKQC verify <book-dir> <manifest>` at every gate transition. CURRENT means only
that bytes match the manifest and it is not approval; completeness against contracts,
sources and depth still comes from inspection and review reports.

On any changed, added or removed input, mark affected approval evidence STALE.
A manuscript or shared-data change invalidates whole-book inspection, independent
SHIP and output preflight until rechecked. Preserve old reports as history. A
revision may reuse unchanged chapter evidence only when hashes and dependencies
match. Never reuse an unrelated book's report.

Chapter states: PLANNED → DRAFTED → INSPECTED → REVIEWED → APPROVED.
A revised chapter returns to DRAFTED. REVIEWED carries a mode and is recorded as
`REVIEWED(independent)` (covered by a genuine independent whole-book review) or
`REVIEWED(self, waived)` (covered by a SELF_REVIEW under a recorded user waiver).
APPROVED requires current inspection PASS, a current review verdict matching that mode
(`SHIP` for independent, `SELF_SHIP` for self, waived) and no blocking findings. The mode
is kept in every later state label and report; `REVIEWED(self, waived)` is never
reported as independent.
Book stages: INTAKE → PLANNING → WRITING → INSPECTION → REVIEW → PREFLIGHT → COMPLETE.
REVIEW has mode `independent` (default) or `self-waived`. BLOCKED is a disposition alongside the current stage.
Reports, not the state label, establish passage.

## Stage transitions

0. **Intake:** `intake.md`. Gate: essentials, format, source/story policy,
   permissions and unresolved items explicitly recorded.
1. **Plan:** `stage_planner.md`. Gate: complete ordered manifest; chapter contracts;
   reconciled word/page budgets; case-study data and provenance rules; metadata plan.
2. **Write:** `stage_writer.md` and `anti_ai_style.md`. One chapter at a time; inspect
   before drafting the next dependent chapter. **Calibration checkpoint:** after the
   first two inspected chapters (or first ~15% of words), build a preview from the
   real renderer, measure words per page, and update the page budget in the plan
   (recorded reallocation, not a quiet target change). Independent chapters may
   proceed while a blocker is isolated; the book cannot reach approval with any
   blocked chapter.
3. **Inspect:** `stage_inspector.md`, per chapter and whole book.
4. **Review:** `stage_reviewer.md`. Independent mode gate: genuine fresh context,
   complete coverage, traceable report, current SHIP. Missing reviewer access means
   BLOCKED unless the user records a waiver (next section); then self-waived mode gate:
   labeled SELF_REVIEW with the same coverage matrix and a current SELF_SHIP.
5. **Preflight and deliver:** `kdp_output.md`. COMPLETE only after requested
   deliverables pass rendered preflight.

## Independent-review waiver (user decision only)

If the user cannot or will not arrange independent review, they may record in
`qc/production_state.md` an explicit waiver in their own words. Then:
- Run the reviewer checklist as a clearly labeled SELF_REVIEW in a fresh pass, with
  the same snapshot, coverage matrix and finding format. Verdicts are `SELF_SHIP`,
  `SELF_REVISE` or `BLOCKED`; the word independent never appears in its report or state.
- Revision budget is unchanged: one revision cycle, one SELF_REVIEW re-review.
- The waiver never covers provenance, rights, safety, accuracy or substantive-depth
  findings; those still block.
- The final disposition is `COMPLETE (independent review waived by user)` and the
  completion response, preflight report and handoff say so. Do not call it reviewed.

## Bounded revision, fail closed

Per chapter: an initial inspection plus at most two writer revision cycles per
production run. After review (either mode): one revision cycle and one actual
re-review in the same mode; a second REVISE blocks completion. Counters do not reset on
resume; record explicit user authorization for any extra cycle. Never waive a
critical accuracy, provenance, safety, rights or depth failure as a minor note.

**Escalation when the budget ends:** record BLOCKED with finding IDs and a short
root-cause note classifying each open finding as PLAN_DEFECT (contract or budget
wrong), INPUT_MISSING (author story, data, source), CONTRACT_UNTESTABLE, or
WRITER_DEFECT. Then offer the user concrete options: supply the input, approve a
plan change (invalidates affected approvals), or authorize N extra cycles. Do not
continue until one is chosen.

## Resume and audit

Inspect disk evidence first. Existing manuscripts with missing or stale reports
remain DRAFTED/unverified; do not invent a past PASS. Run `BOOKQC verify` against
the latest manifest, compare manifest completeness, contracts and sources, then
resume at the earliest unmet gate. For old plans lacking contracts, extend the
plan before expanding prose; preserve user requirements. Do not silently rewrite
the manuscript during an audit-only request.

## Completion response

Report actual stage, checks run (with the commands), unresolved limitations, and
requested file paths. If blocked, give the precise blocker and next action instead
of claiming KDP readiness. This pipeline does not publish or upload on the user's
behalf; the author answers KDP's publishing questions (including AI disclosure).
