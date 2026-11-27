# Stage 5 — Rendered Preflight and Delivery

**Entry gate:** current snapshot inspection PASS, and either a genuine independent
SHIP or (with a recorded user waiver, see `SKILL.md`) a SELF_SHIP that is reported as
self-review, with zero open BLOCKER/MAJOR findings. Run `BOOKQC verify` on the
whole-book manifest (`BOOKQC` as defined in `SKILL.md`); state labels alone do not authorize release.
**Output:** requested approved deliverables plus `qc/preflight_report.md`.

## Build without implying approval

Preview and calibration builds live in `build/`, marked unapproved. Before writing
or replacing anything in `final/`, satisfy the entry gate. Preserve user files and
reports; never delete working sources as part of packaging.

Use the ordered plan manifest, not filename sorting. Choose and record one render
path in `build/README.md` before the calibration build, and reuse it for the final:
- Default: Markdown → Pandoc → XeLaTeX (or HTML+CSS → Chromium/WeasyPrint) with an
  explicit page-size, margin and font configuration committed to `build/`.
- DOCX for print is a fallback only; Word reflow makes page counts unstable.
- Inspect the installed tools first (`pandoc --version`, `xelatex --version`, etc.);
  an artwork assembler is not automatically a prose-book renderer.
Render every required chapter, table, reference and image from the reviewed snapshot.

## KDP technical reference (provisional: verify against KDP help at build time)

Record the source URL and date checked in the preflight report. Where KDP's current
pages disagree with this table, KDP wins and this table gets updated.

| Item | Reference value |
|---|---|
| Paperback pages | 24 minimum, 828 maximum |
| Hardcover pages | 75 minimum, 550 maximum (confirm) |
| Bleed | 0.125 in on top, bottom, outside; page size grows 0.125 in wide, 0.25 in tall |
| Outside/top/bottom margin | 0.25 in minimum without bleed; 0.375 in with bleed |
| Inside (gutter) margin | 24–150 pp 0.375 in; 151–300 0.5; 301–500 0.625; 501–700 0.75; 701–828 0.875 |
| Image resolution | 300 dpi effective at print size recommended |
| Fonts | All embedded; no missing glyphs |
| Spine text | Paperback needs more than 79 pages; hardcover threshold differs |
| Price | Subject to KDP minimum (from printing cost) and maximum list price; check calculator |

Use margins at or above these minimums; for a book over 150 pages prefer a
comfortable inside margin (0.75 in or more) for readability, noting the trade-off
against page count.

## Interior checks

- Requested trim, binding, paper/ink and bleed combination currently supported.
- Rendered print pages within ±5% of intake, including front/back matter. Record
  actual count and bounds. Estimated pages do not pass.
- Scope complete and substantive; no whitespace inflation, oversized fonts,
  repeated text or unrequested blank pages.
- Required matter and chapters in manifest order. TOC, running heads, folios and
  cross-references resolve to rendered content. Verso/recto pagination is correct.
- Fonts embedded, glyphs correct, tables legible, no clipping, overflow, orphan
  headings or broken images. Inspect every rendered page visually, in batches if
  necessary (for example `pdftoppm -r 60 -png` contact sheets, then zoom on
  doubtful pages); record page coverage. Automated checks supplement, never replace.
- Run and save output of: `pdfinfo` (pages, page size), `pdffonts` (all embedded:
  yes), `pdfimages -list` (effective ppi), plus a text extract spot-check.
- Margins/gutter and image resolution measured against the table above for this
  exact page count; record required, source, and measured values.
- Companion links/QRs resolve to the approved resource; decode QR codes from the
  rendered output; promised files exist. Missing resources block the claim.

If fixing a layout defect changes wording, captions, numbers or meaning, create a
new snapshot and re-run affected inspection/review. Layout-only changes need
repeated preflight; prior content approval stays valid only when reviewed content
and dependencies are unchanged.

## Cover checks

Use KDP's current cover calculator/template for the exact final page count, binding,
trim, paper and ink: https://kdp.amazon.com/cover-calculator
Record inputs, retrieved dimensions/template and date. The template wins. If the
calculator cannot be reached from this environment, ask the user to run it with the
recorded inputs and paste the dimensions; until then the cover is BLOCKED. A
provisional spine estimate (pages × per-page paper thickness) may be used only for
layout drafts, labeled unapproved.

Never apply a paperback formula to hardcover. Check bleed, wrap, hinge/fold, spine
and safe zones against the actual template. Verify barcode clearance (KDP places
it on the back cover if you do not), readable spine/front/back text, embedded
fonts, resolution and consistent title/author/edition. A changed page count
invalidates cover sizing and requires another cover preflight.

## KDP metadata file (when requested; default on)

Create `final/<slug>_KDP_Metadata.md` containing: title, subtitle, series, edition,
author, contributors, description (plain text plus a basic HTML version using only
tags KDP supports), seven keywords, up to three category paths, language, age/grade
if relevant, ISBN plan, list price check, territories, AI-content disclosure notes
(what was AI-generated in text, images, cover), and a pre-publish checklist. Claims
in the description must match the manuscript and the claim register; no unverifiable
income or result promises. Mark price and category availability as "verify in KDP".

## Ebook (only if requested)

Treat as a separate deliverable with its own checks: reflowable EPUB (or KDP's
current accepted format), navigable TOC, no fixed page-number references, alt text
for images, tables that reflow or become images with alt text, tested in an
available reader/previewer. Record tool versions and results. Do not derive ebook
approval from print approval.

## Preflight evidence and delivery

Record book ID, source revision manifest, inspection/review (or waiver) references,
build tool/version and the exact command used, final file paths and SHA-256 hashes,
measured pages/dimensions, visual coverage, check results and unresolved findings.
A failed or unperformed required check means FAIL/BLOCKED. Mark COMPLETE only when
all required deliverables pass and hashes match the checked files. Preserve failed
results as history.

Deliver only the formats requested in intake, normally:
- `final/<slug>_Interior.pdf`
- `final/<slug>_Cover_Wrap.pdf` when a cover was requested
- `final/<slug>_Manuscript.docx` when requested, checked against the same content
- `final/<slug>_KDP_Metadata.md`
- Other requested ebook files, separately verified

Report actual paths, final page count, binding-specific cover dimensions, checks run
and honest limitations. Do not guarantee platform acceptance or claim human/proof
review that did not happen. Recommend a printed proof copy. Do not publish or upload
without a separate user request; the author submits KDP's disclosures.
