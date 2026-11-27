# Stage 1 — Planner

**Input:** recorded intake, user materials and initial verified research.
**Output:** `plan/spec.md`, initial `research/claim_register.md`, and updated
`qc/production_state.md`. Apply the gates in `SKILL.md`; do not draft chapters here.

## Required plan contents

1. **Book promise and boundaries:** audience, prior knowledge, intended use,
   reading level, language, binding, trim, paper, ink, and requested deliverables.
   Preserve user requirements. Check current platform support for the combination;
   an unsupported format is a blocker, not permission to substitute another one.
2. **Ordered file manifest:** every front-matter, chapter, appendix and back-matter
   path in build order, also written as a fenced block in `plan/spec.md` that
   `BOOKQC snapshot --whole-book` reads (one relative path per line, e.g. `manuscript/01_intro.md`;
   open with ```manifest and close with ```). The tool checks listed files exist, are
   non-empty, and that no manuscript file is unlisted; it cannot judge whether the
   plan itself is complete, so the inspector must. Identify dependencies and ownership of overlapping topics.
   A directory listing is not a build-order contract.
3. **Reconciled budget:** target pages and body words per chapter, allocations for
   tables/images/front/back matter, and totals. Show the actual sums. Final print
   pages must be within ±5% of intake. Estimate density using representative layout;
   do not multiply a convenient words-per-page guess into a delivery guarantee. Mark the
   density as PROVISIONAL and schedule the calibration build in `SKILL.md` (after the
   first two inspected chapters) to replace it with a measured words-per-page figure.
   For template- or table-heavy chapters, set separate body-word and total-visible-word
   targets so tables cannot hide thin prose.
4. **Chapter contracts:** use the fields below. Give each required item an ID so
   inspections can map it to evidence. Topic headings alone are insufficient.
5. **Voice sheet:** clear style rules and two representative prose samples. Direct
   writing may use short paragraphs, but sustained explanation must still exist.
6. **Asset plan:** image/table IDs, teaching purpose, chapter/use locations, style,
   captions, required inputs and production method. Permit intentional repeated
   use only when explicitly listed. Use code-rendered charts where appropriate;
   do not incur image-generation costs for charts the intake requested as diagrams.
7. **Front/back matter and metadata plan:** list the standard matter in order (half-title,
   title page, copyright page with ISBN/edition/disclaimers, dedication, contents,
   introduction/how-to-use, chapters, appendices/templates, glossary, references, about
   the author) with a page allowance for each. Include the KDP metadata plan (description
   angle, keyword and category candidates) so claims in it can be checked later.
8. **Research and risk plan:** primary sources, claims requiring verification,
   edition/date/jurisdiction limits, professional review needs, rights, privacy,
   safety and contractual cautions. Disclaimers do not replace factual verification.

## Nonfiction learning-depth map

Apply the beginner-to-advanced requirement in `SKILL.md`. Add a matrix to the plan:
learning stage → chapter IDs → prerequisites → observable capability → worked
case/artifact → exercise and evaluation criteria. Cover foundations, guided
practice, independent execution and advanced professional judgment within the
book's subject. Explain entry points for beginners and experienced practitioners.
Allocate meaningful space and research to advanced material; a final section
merely titled "advanced tips" is not coverage.

Advanced contracts must include non-routine decisions, competing approaches,
constraints, diagnostic evidence, failure recovery and justified trade-offs.
Plan progressively harder examples and an integrated capstone with consistent
data, decisions, results and a solution/rubric. Professional capability must be
demonstrated through tasks, not asserted in marketing. If the required depth
cannot fit the page budget, escalate the conflict instead of thinning chapters.

## Nonfiction chapter contract

For each chapter specify:

- Reader problem and observable outcome: what the reader can decide or do afterward.
- Prerequisites, scope exclusions, and boundaries with adjacent chapters.
- Required explanations: mechanisms, reasoning, assumptions and trade-offs.
- Procedure: inputs, roles, ordered actions, outputs and acceptance criteria.
- Worked example: starting data, intermediate reasoning/calculations, decisions,
  result and interpretation. Specify the scenario and expected artifacts now.
- Usable artifact: completed worksheet/card/board/sample record and, if useful,
  its blank reusable version. A blank form alone does not teach application.
- Exceptions and failure modes: how to detect them, respond, and verify recovery.
- Application exercise or checklist with a way to evaluate the result.
- Facts and stories requiring claim IDs; planned sources or missing author input.
- Body-word target, default acceptance range 85–115%, estimated pages, and assets.

Adapt this contract to chapter purpose. An introductory chapter may use a worked
diagnostic rather than an operating procedure. Mark genuinely inapplicable fields
N/A with a reason before writing; do not force identical boxes into every chapter.
A whole-book case study must demonstrate the integrated workflow with underlying
data and decisions, not merely summarize successes from preceding chapters.

## Novel chapter contract

Use scene/beat IDs, POV/tense, setting, character goal, conflict, choice,
consequence, emotional turn and setup/payoff obligations instead of nonfiction
procedures. Maintain character bible, chronology and world rules; specify scene
and word budgets. Do not impose worksheets or fabricated research on fiction.

## Shared examples and provenance

Create one canonical dataset for recurring scenarios: units, quantities, dates,
crews/resources, costs, baseline, forecast and actual/illustrative results. Reconcile
arithmetic and timeline before reuse. Label constructed data as illustrative;
never transform it into a reported field result. Trace external benchmarks to
sources and author anecdotes to supplied/confirmed accounts.

Initialize claim-register rows with: ID, chapter/location, claim or story,
classification (SOURCED / AUTHOR_CONFIRMED / ILLUSTRATIVE / UNRESOLVED), source path
or URL and locator, verification status, limitations, and required action.
User confirmation supports a personal account, not an unrelated technical claim.

## Planning gate

Check manifest completeness, budget sums, contract testability and provenance.
If an essential input is missing, record BLOCKED and ask the focused question;
otherwise record PLANNED. Do not relax a target after seeing a short draft just
to make it pass. Any justified reallocation must preserve scope and page budget,
record reasons, and invalidate affected approvals; user requirements need user
approval to change. On resume, add missing contracts before accepting old drafts.
