# Report G1 — Guide PDF Render Integrity Fix

## Scope ID and name
- `G1 — Guide PDF Render Integrity Fix`

## Objective
- Найти точную причину пропажи Greek symbols и notation fragments в guide PDF.
- Внести минимальный локальный fix только в guide PDF export path.
- Пересобрать и проверить guide PDF без изменения methodical truth-bearing content.

## Files created
- `reports/report_G1_guide_pdf_render_fix.md`

## Files updated
- `src/delivery_guide_pdf.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `deliveries/20260330T220422020897Z__study_pack__full/guide/methodical_guide__variant.pdf`
- `reports/master_report.md`

## Root cause found
- Потеря символов происходила не в source markdown и не в guide logic.
- Проблема была в `pandoc + xelatex` export surface: Greek/Cyrillic notation в guide в основном живёт внутри inline code spans, а exporter задавал только `mainfont`.
- Для inline code spans Pandoc/XeLaTeX использовал monospaced font family по умолчанию, у которой в текущем render path не было надёжного glyph coverage для `λ`, `μ`, `ν`, `ρ`, `δ` и идентификаторов вида `P_отк`, `M_зан`, `K_загр`.
- Минимальная render probe подтвердила это напрямую: без `monofont` `pdftotext` отдавал replacement characters, а с явным `monofont=Courier New` те же notation lines извлекались корректно.

## What was fixed
- В `src/delivery_guide_pdf.py` guide PDF exporter теперь задаёт не только `mainfont`, но и explicit `monofont`.
- Добавлен narrow mono-font fallback chain: `Courier New`, `Menlo`, `DejaVu Sans Mono`, `Liberation Mono`.
- Поведение для main text, guide content, delivery model и other formats не менялось.
- Тест `tests/test_delivery_guide_pdf_runtime.py` усилен: он теперь проверяет не только non-empty PDF, но и реальную текстовую сохранность notation через `pdftotext`.
- Текущий broken repo-local artifact `deliveries/20260330T220422020897Z__study_pack__full/guide/methodical_guide__variant.pdf` пересобран тем же exporter'ом без изменения markdown source.

## How it was validated
- `python3 -m py_compile src/delivery_guide_pdf.py tests/test_delivery_guide_pdf_runtime.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_guide_pdf_runtime tests.test_delivery_validation -v`
- Real runtime smoke:
  - `guide_only + variant_aware + pdf` -> `/tmp/berchun_g1_variant/.../methodical_guide__variant.pdf`
  - `guide_only + general + pdf` -> `/tmp/berchun_g1_general/.../methodical_guide__general.pdf`
- Old-vs-new extraction check показал:
  - до fix строки `λ = 1 / Tc = 0.0714`, `μ = 1 / Ts = 0.0154`, `ν = 1 / Tw = 0.00943`, `P_отк = p_n`, `M_зан`, `K_загр`, `ρ_n < 1`, `δ_k = min(k, n) μ + max(k - n, 0) ν` в old PDF не извлекались;
  - после fix все эти notation examples извлекаются корректно в regenerated PDF;
  - regenerated repo-local delivery PDF теперь тоже проходит тот же needle check.
- `git diff -- docs/methodical/content/METHODICAL_GUIDE.md` пуст: guide source content в G1 не менялся.

## What intentionally remained unchanged
- `docs/methodical/content/METHODICAL_GUIDE.md`
- Все числа, formulas, checkpoints, section order и defense logic.
- Все figures, manifests и solver/report truth.
- README, delivery request model, unified UX, DOCX paths и bundle semantics.

## Remaining risks
- Guide PDF runtime по-прежнему зависит от локального `pandoc + xelatex`.
- Успех fix также зависит от наличия хотя бы одного mono font из narrow fallback chain.
- Проверка integrity сделана честно на живом PDF extraction, но не открывала broader export redesign и не трогала другие output surfaces.

## Ready for G2? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `G2 — Guide PDF Embedded Figure Surface Pass`.
- Держать его столь же узким: добавить в guide PDF только controlled embedding of already existing guide schemes/plots where it improves usability, без изменения guide content truth, без новых formulas/checkpoints и без общего redesign delivery/runtime.
