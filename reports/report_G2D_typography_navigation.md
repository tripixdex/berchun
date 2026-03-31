# Report G2D — Text Block Typographic Integrity + PDF Navigation Pass

## Scope ID and name
- `G2D — Text Block Typographic Integrity + PDF Navigation Pass`

## Objective
- Локально исправить reader-facing typography defects в guide PDF, где support-block headings схлопывались с соседним текстом.
- Добавить практическую PDF navigation для guide/report surfaces без изменения truth-bearing content.
- Перевыпустить текущий полный user-facing pack через system path, чтобы visible report+guide artifacts уже отражали исправление.

## Files created
- `reports/report_G2D_typography_navigation.md`
- `tests/test_pdf_surface_integrity.py`

## Files updated
- `src/delivery_guide_pdf.py`
- `src/render/report_builder.py`
- `src/render/section_flow.py`
- `reports/master_report.md`
- regenerated full pack:
  - `deliveries/20260331T122052864762Z__study_pack__full/report/final_report.pdf`
  - `deliveries/20260331T122052864762Z__study_pack__full/guide/methodical_guide__variant.pdf`
  - `deliveries/20260331T122052864762Z__study_pack__full/delivery_manifest.json`

## What typography problems were fixed
- Root cause in guide PDF: markdown heading depth reached LaTeX run-in levels (`\paragraph` / `\subparagraph`), so support blocks like `Числовой checkpoint`, `Локальный вывод`, `Что это значит простыми словами` visually collapsed into adjacent prose.
- Fixed only that local rendering behavior:
  - `\paragraph` and `\subparagraph` are now emitted as block-style headings in guide PDF export;
  - vertical rhythm around those local teaching blocks is now separated instead of run-in.
- End-user effect:
  - `Числовой checkpoint` no longer renders as `Числовой checkpoint По итоговым...`
  - `Локальный вывод` no longer merges into the first sentence of the block
  - `Что это значит простыми словами` again reads as a distinct guide aid, not as inline prose.

## What PDF navigation was added
- Guide PDF:
  - kept the existing outline/bookmark structure produced from the guide headings;
  - explicitly enabled `PageMode = UseOutlines`, so the guide opens with practical outline navigation behavior where the viewer supports it.
- Report PDF:
  - added explicit PDF bookmarks for:
    - title page
    - task 1
    - sections `1.1`, `1.2`, `1.3`, `1.4`
    - task 2
    - section `2.1`
  - enabled `PageMode = UseOutlines` in the report PDF as well.
- A visible TOC was intentionally not added in this narrow pass, because that would change visible document flow more than necessary.

## How the full pack was regenerated
- Built a fresh canonical run through the system with the current input and a fresh dedicated runs-dir:
  - `build --input inputs/variant_me.yaml --runs-dir /tmp/berchun_g2d_runs.5v07B1`
- Then issued the current full user-facing pack through the delivery system:
  - `deliver --runs-dir /tmp/berchun_g2d_runs.5v07B1 --source-run-id 20260331T122041760945Z__2aaa6e434b2c --delivery-profile study_pack --output-format bundle_dir --report-scope full --guide-mode variant_aware --guide-scope full`
- Resulting visible pack:
  - `deliveries/20260331T122052864762Z__study_pack__full`

## How it was validated
- Syntax:
  - `python3 -m py_compile src/delivery_guide_pdf.py src/render/report_builder.py src/render/section_flow.py tests/test_pdf_surface_integrity.py`
- Automated tests:
  - `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_pdf_surface_integrity tests.test_delivery_guide_pdf_runtime tests.test_build_pipeline -v`
- End-state PDF checks on the regenerated pack:
  - guide PDF: `PageMode = /UseOutlines`, outline count `14`
  - report PDF: `PageMode = /UseOutlines`, outline count `8`
  - extracted guide text no longer contains the collapsed patterns:
    - `Числовой checkpoint По итоговым`
    - `Локальный вывод Для моего варианта`
    - `Что это значит простыми словами Поток звонков`

## What intentionally remained unchanged
- `docs/METHODICAL_GUIDE.md`
- all numbers
- all formulas
- all checkpoints
- all guide/report logic
- all figure choices and placements
- delivery model and broader export architecture

## Remaining risks
- `G2D` intentionally fixed only local support-block typography plus PDF navigation; it did not open a full typography redesign for either surface.
- Guide PDF still depends on local `pandoc + xelatex`, and report PDF still depends on local XeLaTeX toolchain.
- Guide outline depth remains the current pandoc-driven structure; this pass did not open a new visible TOC or guide navigation redesign.

## Ready for G3? YES/NO
- `YES`

## Exact recommendation for next step
- Open `G3 — Guide Surface Freeze Review`.
- Keep it narrow: review the current teacher-first, visually supported, typographically repaired and navigation-enabled guide/report surface as a user-facing artifact set; fix only tiny real inconsistencies if found, without reopening numbers, formulas, checkpoints, guide logic or delivery semantics.
