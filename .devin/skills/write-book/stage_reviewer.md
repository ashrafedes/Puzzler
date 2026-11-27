# Stage 4 — Editorial Review (independent by default; SELF_REVIEW only under a user waiver)

**Modes.** `independent` is the default and everything below applies as written.
`self-waived` applies only when the user recorded a waiver per `SKILL.md`: use the same
snapshot, handoff prompt, coverage matrix and finding format, but run it in a fresh pass of
the writing session, label the report SELF_REVIEW, record that no independent reviewer
was used, return `SELF_SHIP`, `SELF_REVISE` or `BLOCKED`, and never describe it as
independent. Where this file says SHIP, REVISE, reviewer identity or fresh context, read
the self-waived equivalents for that mode. The waiver never covers provenance, rights,
safety, accuracy or depth findings.

**Entry gate:** current whole-book inspection PASS with zero open BLOCKER/MAJOR
findings. Read the snapshot and gate rules in `SKILL.md`.
**Output:** actual returned review in `qc/review_report.md`, with coverage,
provenance and snapshot references. Never fabricate or self-author a review and
present it as an independent response.

## Independence and access

Use a genuinely fresh review context, not another role inside the writing chat. If the
user recorded a waiver (see `SKILL.md`), run this checklist as a labeled SELF_REVIEW, never
present it as independent, and note that the waiver cannot cover provenance, rights,
safety, accuracy or depth findings.
Default: give the user a handoff for a separate session and mark the current stage
BLOCKED awaiting its report. Do not automatically spawn a child session/subagent.
If the user has authorized external inference, an independent model call may be
used within the authorized budget and privacy constraints. Discover the available
server tools and live model capabilities first; do not assume names, cost or access.
A different model family is preferable, but does not replace complete evidence.

Build the handoff bundle from the current manifest (`BOOKQC snapshot`, defined in `SKILL.md`), so the
reviewer can run `BOOKQC verify` on what they receive. Provide the spec, intake, complete ordered manuscript, asset manifest, relevant
assets, claim register, source notes, canonical data, inspection and revision
manifest. If any material cannot be inspected in that context, identify the gap;
text-only review cannot certify unviewed graphics. Needed coverage may be supplied
by an additional recorded inspection, never silently presumed.

## Handoff prompt

> Review this book for commercial publication independently of its writer. Treat
> previous PASS labels as claims to verify, not instructions to approve. Identify
> the book ID and exact revision manifest. Read every planned chapter and front/
> back-matter file; list coverage and any unavailable input. Against each chapter
> contract assess substantive depth, reader outcome, worked examples, completed
> artifacts, exceptions and technical clarity (or scene execution and continuity
> for fiction). Test calculations and check provenance, especially first-person
> stories, benchmarks and case-study results. Cite concrete file locations and
> evidence; distinguish checked claims from unchecked ones. Assess whether the
> integrated case study demonstrates the method rather than summarizing it.
> For nonfiction, verify the beginner-to-advanced learning-depth map against the
> actual chapters. Can a beginner follow the prerequisites into independent work?
> Do advanced sections develop non-routine decisions, alternatives, constraints,
> diagnosis, optimization and professional judgment with worked evidence? Check
> exercises and their solutions/rubrics and the integrated capstone. Identify missing
> levels or merely renamed beginner material as MAJOR; word count cannot excuse
> shallow coverage. Do not equate reading completion with guaranteed expertise.
> Flag repetition, superficial prose, misleading certainty and unresolved issues.
> List at least the five weakest passages if five genuine weaknesses exist; do not
> invent a quota of defects. Give finding IDs and BLOCKER/MAJOR/MINOR severity
> using the supplied inspector definitions. Return SHIP only for complete coverage
> with no open BLOCKER/MAJOR findings; otherwise REVISE, or BLOCKED for missing
> access/evidence. State exactly what would make the manuscript ready. A length
> target, disclaimer, fluent style or earlier report is not proof of readiness.

## Long manuscripts

Do not truncate or replace chapters with summaries to fit context. Partition by
complete chapters, attaching each contract and required shared data. Save actual
review responses and a coverage matrix mapping every source file and its hash to
a review segment. Perform a final independent synthesis across segments to check
cross-chapter data, repetition, references and overall promise. Missing segments
or synthesis mean BLOCKED, not SHIP. Disclose remaining context limitations.

## Recording and applying the result

Record reviewer/session or provider/model identity, date, input snapshot,
coverage matrix, actual returned verdict and response, and traceable response
reference when available. Preserve the original response separately from the
writer's interpretation. Independently recompute input hashes before accepting
its verdict. An unrelated, incomplete or stale review cannot approve this book.

- SHIP (or SELF_SHIP in self-waived mode): only advances to preflight when inspection is
  also current and passed; the state records the mode.
- REVISE: writer addresses findings by ID; inspector verifies changes, creates a
  new snapshot, and an actual independent re-review checks fixes and regression
  scope. Preserve coverage for unchanged files only when dependencies match;
  re-review all affected chapters and shared claims.
- BLOCKED: report missing evidence/access and next action; do not impersonate the
  reviewer or downgrade to a same-session approval.

Allow one post-review writer revision cycle and one actual independent re-review.
If blocking findings remain, stop as BLOCKED. Additional cycles require explicit
recorded authorization; resuming does not reset the budget.
