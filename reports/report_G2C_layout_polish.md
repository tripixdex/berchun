# Report G2C — Guide PDF Final Layout Polish

## Scope ID and name
- `G2C — Guide PDF Final Layout Polish`

## Objective
- Локально успокоить guide PDF around already embedded schemes/plots без изменения truth-bearing content.
- Исправить только spacing/page-flow/caption pacing/figure calmness issues, которые ещё мешали слабому студенту читать guide как цельную опорную surface.

## Files created
- `reports/report_G2C_layout_polish.md`

## Files updated
- `src/delivery_guide_pdf.py`
- `src/delivery_guide_pdf_surface.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `deliveries/20260331T113057027618Z__study_pack__full/guide/methodical_guide__variant.pdf`
- `reports/master_report.md`

## What layout problems were fixed
- Ключевые plots больше не плавают вверх страницы отдельно от своего local explanation block.
- Long plot captions больше не ломаются визуально как detached word fragment справа от графика.
- Width policy стала спокойнее:
  - schemes: `0.76\textwidth`
  - key plots: `0.86\textwidth`
- Figure/caption pair теперь держится как one local centered visual block, а не как markdown image routed through float-like PDF behavior.

## What local layout policy changed
- Guide PDF surface builder больше не опирается на pandoc image AST for embedded visuals.
- Embedded visuals теперь вставляются как narrow raw-LaTeX centered blocks with:
  - non-floating `\includegraphics`
  - centered `\parbox` caption under the same width envelope
  - absolute asset paths for reliable XeLaTeX resolution
- Existing placement logic preserved:
  - scheme after `Схема и состояния`
  - one key plot at the same section-local graph-reading anchor
- Clean page break before main methodical body (`## Задача 1...`) preserved from `G2B`.

## How it was validated
- `python3 -m py_compile src/delivery_guide_pdf.py src/delivery_guide_pdf_surface.py tests/test_delivery_guide_pdf_runtime.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_guide_pdf_runtime tests.test_delivery_validation -v`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_runtime tests.test_delivery_general_runtime tests.test_delivery_guide_pdf_runtime -v`
- Real smoke:
  - `guide_only + general + pdf`
  - `guide_only + variant_aware + pdf`
- Visual inspection via page PNGs for former rough pages (`5`, `10`, `14`, `23`) confirmed:
  - plots remain embedded,
  - captions sit directly under the plot,
  - the plot no longer detaches to page top as a separate floating object.
- `pdftotext` validation confirmed no literal `\includegraphics` / `\clearpage` leakage in the rendered PDF text.

## What intentionally remained unchanged
- `docs/methodical/content/METHODICAL_GUIDE.md`
- all numbers
- all formulas
- all checkpoints
- all defense / graph / contrast / compression / stop-line logic
- all section-local placement decisions for already embedded visuals
- delivery model and broader export architecture

## Remaining risks
- `G2C` deliberately fixed only the current local PDF imbalance; it did not open a full typography redesign.
- The current sync touched only the visible variant-aware study-pack PDF artifact, not every historical delivery copy.
- `tests/test_delivery_guide_pdf_runtime.py` is now `172` lines: above soft limit, below hard limit; no test split was opened in this narrow pass.

## Ready for G3? YES/NO
- `YES`

## Exact recommendation for next step
- Open `G3 — Guide Surface Freeze Review`.
- Keep it narrow: review the now teacher-first, visually supported and locally polished guide PDF surface as one operator/student-facing artifact, fix only tiny real inconsistencies if any remain, and do not reopen numbers, formulas, checkpoints, guide logic or delivery semantics.
