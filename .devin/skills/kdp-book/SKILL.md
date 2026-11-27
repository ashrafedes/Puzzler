---
name: kdp-book
description: Produces and verifies artwork-based paperback coloring/activity books for Amazon KDP. Use for numbered page-art interiors and their wrap covers, not prose nonfiction, novels, or hardcover production; use write-book for those workflows.
---

# KDP Artwork Book Pipeline

Scope: artwork-based paperback coloring/activity books only. Do not use this
workflow's margins, page ordering, cover formulas or sampled checks to approve a
prose book or hardcover. For those, follow `.devin/skills/write-book/SKILL.md`.
Verify current KDP requirements for the exact selected format before release;
the presets below are not universal requirements. Discover current MCP tools
before invoking them. Uploading or publishing requires a separate user request.

Goal: deliver `<Book>_interior.pdf` and `<Book>_cover.pdf` after verification.
Preserve original artwork, working sources and QA evidence; do not delete user
files or intermediate artifacts as an automatic delivery step. Keep required
platform disclosures truthful.

## Hard KDP requirements (paperback)

- **Trim size:** 8.5 × 11 in is the standard for this project.
- **Interior (no bleed):** PDF page = trim size exactly. Margins: ≥ 0.375" inside (gutter) for 24–150 pages, ≥ 0.25" outside/top/bottom. This project uses **0.375" uniform on all sides**.
- **Interior (bleed):** only if art must reach the page edge. PDF page = trim + 0.125" on top, bottom, outside edge (8.625 × 11.25). Default here is **no bleed**.
- **Page order:** strictly by filename, 1 → N. Page 1 of the PDF is the first right-hand page.
- **Cover (full wrap):** one page, width = 0.125 + back + spine + front + 0.125 = 2×trimW + spine + 0.25; height = trimH + 0.25.
- **Spine width (B&W):** pages × 0.002252" white paper, × 0.0025" cream, × 0.002347" premium color. Recalculate whenever page count or paper changes — a wrong spine makes KDP reject or misalign the cover.
- **Cover safe zones:** keep text/logos ≥ 0.25" inside trim and ≥ 0.0625" from spine edges; leave a clear ~2×1.2" box bottom-right of back cover for the barcode.
- **Fonts:** every font in either PDF must be embedded. All-image PDFs (no text objects) avoid this entirely.
- **Resolution:** ≥300 DPI recommended for cover and line art.
- **Page count:** ≥24 pages, ≤828 B&W.

## Workflow per book

1. **Source art** — put numbered page images in `Books/<BookName>/` as `1.png … N.png` (sequential, no gaps; the script fails otherwise). Cover art as a full-wrap image/PDF or separate front+back images.
   - With the **Canva MCP server** (configured in `.devin/mcp_config.json`): generate pages with `create-design`/image tools at ≥3477×4500 px (≈400 DPI at 8.5×11), export PNG, save into the book folder. For the cover ask for a single full-wrap design sized `2*trimW + spine` × `trimH + 0.25` inches at 300 DPI, spine centered.
   - Kids 3–10 coloring pages: bold black line art, white background, no shading, age-appropriate subjects.
2. **Build** — `python tools/build_book.py "Books/<BookName>" --cover <wrap> [--paper white]`
   - Produces `<BookName>_interior.pdf` (8.5×11, 0.375" margins, grayscale JPEG q90, ~1 MB/page) and `<BookName>_cover.pdf`.
   - Intermediates go to a temp dir deleted automatically (`--keep-temp` to inspect).
3. **Verify** — open both PDFs: page count, size printed by script, spot-check first/middle/last page visually, confirm barcode box and spine position on the cover.
4. **Upload to KDP:** Paperback → Black & white interior, white paper → 8.5×11 → Bleed: **No** → upload interior, then cover → set price.

## Known pitfalls from past builds

- Baked-in page numbers inside artwork can contradict filename order — detect printed folios and erase before building (small connected components bottom-center), or renumber correctly.
- Source images exactly at trim size have no bleed margin — use the no-bleed margins build rather than faking bleed.
- Canva exports may carry unembedded fonts in PDFs — rebuild covers through `build_book.py` (image-only pages) to strip them.
- 30-page spine ≈ 0.068"; keep spine text off books under ~100 pages (KDP won't print it anyway below 79–100 pages depending on spec).
