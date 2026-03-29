# Report H1A

## Scope ID and Name
- `H1A — Terminology Russification + De-Anglicization`

## Objective
- Выполнить только узкий текстовый pass поверх optional ветки `H1`: убрать оставшиеся английские и внутренние технические формулировки из teacher-facing PDF без изменения математики, чисел, формул, структуры, рисунков и acceptance-critical пояснений.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_H1_humanization.md`
- `report/final_report.tex`
- `report/final_report.pdf`

## Files Created
- `reports/report_H1A_russification.md`

## Files Updated
- `src/render/notation.py`
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `src/render/task2_reflow.py`
- `src/render/content.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## Which Phrases Were Replaced
- `offered load` -> `приведённая нагрузка`
- `arrival-weighted вероятность` / `arrival-weighted probability` -> `вероятность того, что новый отказ будет ожидать обслуживания` или эквивалентная русская формулировка в ближайшем контексте
- `sweep` / `sweep-режимы` -> `серия графиков` / `серии графиков`
- `stationary_truncated` -> естественное русское пояснение про стационарные метрики, полученные после контролируемого численного усечения хвоста
- `epsilon` в прозе -> `порог усечения ε`

## What Intentionally Remained Unchanged
- Все формулы.
- Все числовые значения и checkpoint values.
- Все figure ids, порядок рисунков и figure data.
- Все scheme semantics.
- Вся task hierarchy.
- Все acceptance-critical пояснения про `P_ож` и усечение в `1.4`.
- Все build / archive / input semantics.

## Validation Actually Run
- Инспекция текущего surface:
  - `sed -n '1,240p' reports/master_report.md`
  - `sed -n '1,220p' reports/report_H1_humanization.md`
  - `rg -n "offered load|arrival-weighted|sweep|stationary_truncated|epsilon|ε" report/final_report.tex src/render -g '*.py'`
  - `sed -n '1,220p' src/render/notation.py`
  - `sed -n '1,220p' src/render/task1_reflow_11_12.py`
  - `sed -n '1,220p' src/render/task1_reflow_13_14.py`
  - `sed -n '1,220p' src/render/task2_reflow.py`
  - `sed -n '1,220p' src/render/content.py`
- Подготовка и syntax check:
  - `cp report/final_report.tex /tmp/berchun_h1a_before_final_report.tex`
  - `cp report/assets_manifest.json /tmp/berchun_h1a_before_assets_manifest.json`
  - `python3 -m compileall src/render`
- Каноническая пересборка:
  - `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
  - `python3 -m json.tool report/assets_manifest.json >/dev/null`
- Post-rebuild checks:
  - `rg -n "offered load|arrival-weighted|sweep|stationary_truncated|epsilon|приведённая нагрузка|вероятность того, что новый отказ будет ожидать обслуживания|серии графиков|порог усечения ε" report/final_report.tex`
  - `python3 - <<'PY' ... PY` для проверки `display_formula_count = 33`, `display_formulas_equal = true`, `number_token_multiset_equal = true`
  - `python3 - <<'PY' ... PY` по `pypdf` для подтверждения отсутствия в PDF слов `offered load`, `arrival-weighted`, `sweep`, `stationary_truncated`, `epsilon`
- Подтверждено:
  - `display_formula_count = 33`
  - `display_formulas_equal = true`
  - `number_token_multiset_equal = true`
  - `plot_include_count = 27`
  - `scheme_count = 5`
  - `title_asset_count = 1`
  - targeted English/internal phrases отсутствуют в teacher-facing PDF

## Ready to Keep H1/H1A Branch as the Current Text Surface?
- `YES`
- После `H1A` optional ветка перестала тянуть в PDF английские и внутренние технические ярлыки, при этом осталась строго surface-only и не затронула math/build/report truth.

## Exact Recommendation for Next Step
- Новый implementation scope не требуется. Если owner устраивает более живой и уже де-англизированный surface, ветку `H1/H1A` можно оставить как текущий teacher-facing текстовый слой; если нужен максимально консервативный baseline, можно по-прежнему откатиться только к `P4`, не открывая никакой новой переработки.
