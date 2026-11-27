# Stage 3 — Inspector

**Input:** current spec, full chapter/book source, research and claim register,
canonical data, assets, and SHA-256 revision manifest defined in `SKILL.md`.
**Output:** chapter inspections and `qc/inspector_report.md` with findings history.
The inspector reports; the writer fixes. Same-session inspection is not independent
review and cannot substitute for Stage 4.

## Severity and verdict

- **BLOCKER:** fabricated provenance/approval, serious safety/rights problem,
  missing essential evidence or dependency, or incomplete required input/coverage.
- **MAJOR:** substantive depth missing, unsupported consequential claim, incorrect
  calculation, contradictory data, missing required chapter/artifact/asset, broken
  required reference, or word/page budget outside its acceptance range.
- **MINOR:** local editorial defect that does not undermine correctness, usability,
  scope, rights, or acceptance requirements.

Verdict is PASS only with zero open BLOCKER/MAJOR findings and every applicable
check completed. MINOR findings may remain listed with owner/action; they cannot
hide failed acceptance criteria. Otherwise FAIL; use BLOCKED disposition when an
input/access limitation prevents completion. Missing reports never imply PASS.

## Required checks for each chapter

1. **Contract coverage:** map every contract ID to file and heading/line evidence.
   Read the material; a matching heading is not coverage. Mark PASS/FAIL or planned
   justified N/A. Missing procedures/examples cannot be waived after drafting.
2. **Depth and usability:** trace the reader outcome end to end. For nonfiction,
   walk the worked example using the provided inputs; check roles, steps, decisions,
   outputs, completed artifact and exception handling. Name any step the reader
   must invent. Distinguish sustained explanation from assertions and list-only
   treatment. For novels, assess rendered scenes, motivations and consequences.
3. **Counts:** independently measure body/visible words by running `BOOKQC count`
   (method in `stage_writer.md`) and save the output. Record target, actual, ratio, method and page estimate.
   Default body-word range is 85–115%; both shortfall and excess need resolution.
   Meeting word count cannot override a depth failure. Planning review must justify
   any revised allocation before reinspecting; padding is not a fix.
4. **Provenance:** trace claims to the register and checked sources/author records.
   All consequential claims must be verified or clearly constructed and labeled;
   UNRESOLVED entries and `[verify]` flags block passage. Check edition, context,
   denominator and applicability, not just source-link existence. Check first-person
   stories in the preface and captions as well as chapter text.
5. **Arithmetic and technical consistency:** recompute worked examples and claimed
   changes; check units, crew-days versus person-days, percent versus percentage
   points, baseline/forecast/actual, losses and timelines. Check shared datasets
   across chapters. Flag unqualified universal rules and unsupported causal claims.
6. **Assets and references:** actual files exist, relative paths resolve from the
   manuscript and renderer, captions/labels match, rights are recorded, planned
   usage counts match the asset manifest, and cross-references have valid targets.
7. **Style:** apply `anti_ai_style.md` with contextual reading. Flag repetitive
   rhetoric, compressed summary prose and poor definitions; do not require long
   paragraphs or introduce deliberate errors to look less formulaic.
8. **Novel continuity where applicable:** bible, names/ages, chronology, POV/tense,
   world rules and setup/payoff continuity. Record N/A for nonfiction-only checks.

## Whole-book inspection

- Run `BOOKQC verify` against the whole-book manifest first (`BOOKQC` as defined in `SKILL.md`); any difference makes
  the inspection STALE before it starts.
- Reconcile all files against the ordered manifest, including front/back matter.
- Check that the KDP metadata plan and description claims match the manuscript.
- Verify all chapter inspections cover the current snapshot and dependencies.
- Check chapter boundaries, duplication, progressive teaching and cross-references.
- Confirm integrated case studies actually demonstrate the promised workflow.
- Reconcile total word/page budgets and assets. The page target is ±5%, never ±10%.
  Estimated compliance permits review handoff only; measured final pages belong
  to preflight and are required before COMPLETE.
- Verify no missing sources/assets, placeholders, unsupported author claims, or
  contradictory disclaimers. Apply current platform requirements, not a claim
  that a style disclaimer guarantees compliance.

## Nonfiction progression and information-richness gate

Inspect the learning-depth map, not merely its labels. For each stage record the
chapters read, capabilities taught, worked-example locations and assessment
criteria checked. Verify beginners have explained prerequisites and can progress
to independent application without hidden steps. Verify advanced readers receive
non-routine analysis, meaningful alternatives, diagnostic reasoning, constraints,
trade-offs and recovery methods, not renamed elementary advice.

Walk a foundational example, an independent-application task, an advanced case
and the integrated capstone end to end; add further checks wherever contracts
require them. Recompute relevant calculations and test the exercise solutions or
rubrics. Confirm complexity genuinely increases and each assigned chapter has
sufficient explanation for its level without repetitive padding.

A missing learning stage, superficial advanced coverage, unsolved capstone or
unusable assessment of a required capability is MAJOR and prevents PASS even
when the book meets all word/page counts. This is a reading-and-reasoning gate;
`BOOKQC count` and `verify` cannot certify instructional depth.

## Report contract

Record book ID, date, role, scope, snapshot manifest, counts/method, per-contract
results, source/calculation checks actually performed, coverage limitations,
findings and verdict. Each finding needs ID, severity, path/location, evidence,
reader impact, required fix, owner and OPEN/FIXED/VERIFIED status. A writer's
FIXED claim is not VERIFIED until inspected. Preserve previous findings/verdicts;
record supersession and invalidated snapshots rather than erasing history.

Follow the initial inspection plus two revision-cycle budget in `SKILL.md`.
If blocking findings remain after the budget, record BLOCKED and notify the user.
Never proceed on the third pass merely because the retry budget has expired.
