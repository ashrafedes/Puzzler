# Stage 2 — Writer

**Input:** current `plan/spec.md`, chapter contract, author materials, research,
claim register, shared example data and preceding accepted dependencies.
**Output:** complete `manuscript/` chapter, supporting evidence/assets, and updated
production state. Apply `SKILL.md`; DRAFTED never means APPROVED.

## Work one chapter at a time

1. Read the full chapter contract and relevant earlier chapters. Resolve essential
   missing inputs before presenting unsupported material as fact. Research primary
   sources, save source notes and locators, and update `research/claim_register.md`.
   Open and check sources; a search snippet or remembered standard is not verification.
2. Write developed prose following `anti_ai_style.md`. Explain why a method works,
   when it does not, and how the reader uses it. Headings, punchy lines and lists
   are not substitutes for explanation. Do not write a chapter synopsis as a chapter.
3. For nonfiction, execute each contract item: explanation, procedure, worked
   example, completed artifact, exceptions, and application check, or its planned
   justified alternative. Include real input/output fields, ownership and decisions.
   For novels, render scenes with action, conflict and consequences rather than
   narrating the beat sheet; check character bible, timeline and setups/payoffs.
4. Build examples from canonical data. Show units, denominators, formulas,
   intermediate results and rounding. Distinguish assumptions from observations.
   A failed-package fraction does not establish a labor-loss fraction; demonstrate
   the actual inference and account for unequal package sizes/rework effort.
5. Give every quantitative, technical, historical or personal-experience claim an
   appropriate register entry. Do not invent interviews, quotations, credentials,
   standards clauses or first-person experiences. Label constructed scenarios at
   their first use and label their tables/charts; a generic disclaimer is not enough.
   Unresolved `[verify]` markers are drafting blockers, never acceptable final text.
6. Produce planned assets using the agreed method. Save files and update
   `images/manifest.md` with actual path, ID, source/rights, caption, chapter,
   intended uses and status. Resolve image paths relative to each manuscript file
   and verify they also work in the chosen renderer. Do not insert fictional paths
   or claim an image exists before generating and checking it.
7. Measure and record chapter body words, total visible words and estimated pages.
   Body words are whitespace-separated tokens in narrative paragraphs, including
   narrative blockquotes; exclude headings, lists, table rows, captions, fenced
   code, raw URLs and image markup. Total visible words includes textual lists and
   tables, but not markup or raw URLs. Run `BOOKQC count <chapter.md>` (`BOOKQC` as defined in `SKILL.md`) and record
   its output as the method (it is approximate; keep using the same one for all chapters); report counts separately so tables cannot mask thin prose.
   Default body-word acceptance is 85–115% of the planned body-word target. Flag
   both shortfall and excess for planning review. Never pad or stretch typography.
8. Write a chapter handoff in `qc/production_state.md` and take a chapter-scope snapshot
   with `BOOKQC snapshot --scope`: chapter ID, draft revision,
   counts/method, contract-item locations, claim IDs, asset paths, dependencies,
   open issues and attempt count. Mark DRAFTED, then run Stage 3 on the chapter.
   Do not claim an inspection was performed merely because this handoff exists.

## Rich nonfiction, from foundations to professional application

Follow the chapter's assigned level in the learning-depth map. Build foundations
clearly, then increase complexity without repeating introductory explanations.
Give experienced readers substantive analysis rather than elementary reminders.
For major methods, develop why/how reasoning, complete examples, alternative
approaches, selection criteria, limitations and diagnostic evidence. Use verified
sources and transparent illustrative data, not unsupported confident detail.

In advanced chapters, require decisions under realistic constraints: incomplete
data, resource conflicts, uncertain forecasts, quality failures or competing
objectives as relevant. Show the rejected alternatives, chosen action, consequences
and verification. Include exercises with worked answers or explicit evaluation
criteria; complete the integrated capstone rather than substituting a success
summary. Do not imply reading alone guarantees professional mastery or certification.

Information-rich does not mean jargon-heavy, repetitive, or artificially long.
Every added explanation should resolve a reader question or enable a decision.
If a planned level cannot be taught adequately in its budget, flag a planning
conflict; do not silently downgrade it to a beginner overview.

## Example of the required depth

For a capacity-planning chapter, do not stop at `crews × days × factors`.
Provide a completed per-crew sheet; define each factor and avoid double-counting
losses already embedded in measured productivity; convert capacity into feasible
packages by work type and dependency; show what is excluded and why; then show a
weather/access disruption, a revised pull and Friday's reconciliation. Explain
how the PM changes next week's assumptions from that evidence. Use illustrative
labels unless supplied data establishes an actual project record.

## Revision discipline

Address findings by ID and record fix locations and supporting evidence. Do not
silently delete failed requirements, rewrite target budgets to match the draft,
or describe a rewritten chapter as independently approved. Revisions invalidate
affected snapshot approvals. Respect the retry budget in `SKILL.md`; unresolved
BLOCKER/MAJOR findings leave the chapter BLOCKED, not accepted with exceptions.

## Never deliver

- Unsupported statistics, fake precision, fabricated sources or author history.
- A collection of slogans, headings, blank templates or repeated summaries.
- Unresolved placeholders, missing assets or unverifiable success claims.
- Copied source phrasing without appropriate quotation, permission and attribution.
- Cosmetic paragraph expansion intended only to meet a word/page target.
