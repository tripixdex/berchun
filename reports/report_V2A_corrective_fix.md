# Scope Report

## Scope ID and Name
- `V2A — Task 2 Variant Safety Fix + Prose Softening`

## Objective
- Убрать variant-fragility в teacher-facing render path задачи `2.1` и смягчить только те qualitative phrases, которые V2 классифицировал как `prose-risky`, не меняя solver truth, formulas, figure data и report structure.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_V2_variant_safety.md`
- `out/audit/variant_safety_checks.json`
- `src/render/task2_reflow.py`
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `report/final_report.tex`
- `report/final_report.pdf`

## Files Created
- `reports/report_V2A_corrective_fix.md`

## Files Updated
- `src/render/task2_reflow.py`
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What Was Fixed Now
- В `2.1` убрана жёсткая зависимость от `r = 33`: checkpoint теперь берётся через безопасный artifact-derived selection по реальным `x_value` из текущего sweep. Если точка `33` существует, она сохраняется; если нет, выбирается ближайшая реально рассчитанная точка, поэтому low-month variants больше не падают на `StopIteration`.
- Teacher-facing checkpoint block в `2.1` по-прежнему сохраняет педагогический смысл: остаются опорные точки около `r = 1`, `5`, `10`, `20` и high-end checkpoint, но без предположения, что `max_repairers >= 33`.
- Смягчены только V2-risky qualitative phrases в `1.2`, `1.3` и `2.1`; safe-фразы из V2 оставлены без изменений.

## Which Prose Phrases Were Softened
- `расширение очереди почти не создаёт новый ресурс обслуживания`
  стало:
  `расширение очереди не добавляет новый обслуживающий ресурс напрямую`
- `очередь становится длиннее, но каждое отдельное место используется менее интенсивно`
  стало:
  `занятость одного места изменяется ...; по этому показателю важно смотреть на конкретные численные значения`
- `почти каждая новая заявка попадает в ожидание`
  стало:
  `уже первая стационарная точка соответствует высокой вероятности ожидания`
- `стремится к нулю уже без заметной очереди`
  стало:
  `продолжает снижаться по мере уменьшения очереди`

## What Intentionally Remained Unchanged
- Все формулы.
- Все числовые значения solver outputs.
- Все figure ids, порядок рисунков и figure data.
- Все scheme semantics.
- Вся task hierarchy и title page.
- Build/archive/input behavior вне узко необходимого Task 2 render fix.
- Prose patterns, которые V2 already classified as `prose-safe`.

## Validation Actually Run
- `python3 -m compileall src/render`
- `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
- `python3 -m json.tool report/assets_manifest.json >/dev/null`
- local `python3 - <<'PY' ... PY` surface checks over `report/final_report.tex`:
  - `33` display-formula blocks,
  - `27` used plots,
  - `5` schemes,
  - risky phrases absent,
  - safe phrases still present
- local `python3 - <<'PY' ... PY` rerun of the six V2 failing cases:
  - `F01 full` `01.01.2000`
  - `F03 full` `01.01.2000`
  - `F06 full` `29.02.2000`
  - `F08 full` `28.02.2001`
  - `T14 task2` `01.01.2000`
  - `T16 task2` `29.02.2000`
- Result: all `6/6` cases now build successfully; task2 high checkpoint adapts safely to `r = 31` or `r = 32` where `33` is absent.

## Ready to Proceed to Feature-02?
- `YES`

## Exact Recommendation for Next Scope
- Открыть `Feature-02 — DOCX/exportable editable version` как следующий отдельный feature pass.
- Не смешивать `Feature-02` ни с solver/report redesign, ни с параллельной methodical planning branch.
