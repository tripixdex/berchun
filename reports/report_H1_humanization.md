# Report H1

## Scope ID and Name
- `H1 — Humanization-Only Surface Pass`

## Objective
- Выполнить только узкий stylistic pass поверх уже замороженного teacher-facing baseline: слегка уменьшить риторическую однотипность текста и части подписей без изменения математики, чисел, структуры, порядка рисунков, схем или build behavior.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_P4_task2_microfit.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- текущий rendering layer под `src/render/`
- пользовательское external expert summary о том, что дополнительный humanization-pass является опциональным и не нужен для acceptance

## Files Created
- `reports/report_H1_humanization.md`

## Files Updated
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `src/render/task2_reflow.py`
- `src/render/content.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What Changed Now
- В Task 1 и `2.1` слегка разведены повторяющиеся вводные формулы речи: часть одинаковых `Сначала`, `Затем`, `Следовательно`, `Для текущего варианта` заменена на более естественные, но равносильные по смыслу варианты.
- Ярлык `Числовой checkpoint:` больше не повторяется механически во всех местах подряд: теперь используются несколько близких по тону форм `В числах это даёт:`, `Для ориентира:`, `По расчёту:` и `На характерных точках:`.
- Ограниченный набор teacher-facing captions (`5` штук) сделан менее шаблонным: они остаются академичными и понятными, но уже не следуют везде одному и тому же обороту `в зависимости от ...`.
- Несколько мостиковых фраз сокращены так, чтобы объяснительная логика сохранилась, а текст звучал чуть менее редакторски выровненным.

## What Intentionally Remained Unchanged
- Все формулы.
- Все числовые значения и checkpoint values.
- Все figure ids, figure ordering и figure data.
- Все scheme semantics.
- Вся task hierarchy и title-page semantics.
- Все acceptance-critical пояснения про `P_ож` и про усечение хвоста в `1.4`.
- Все build / archive / input semantics.

## Validation Actually Run
- Инспекция исходного baseline:
  - `sed -n '1,260p' reports/master_report.md`
  - `sed -n '1,260p' reports/report_P4_task2_microfit.md`
  - `rg -n "Сначала|Затем|Следовательно|Для текущего варианта|Числовой checkpoint|в зависимости от" report/final_report.tex src/render -g '*.py'`
  - `sed -n '1,220p' src/render/task1_reflow_11_12.py`
  - `sed -n '1,220p' src/render/task1_reflow_13_14.py`
  - `sed -n '1,220p' src/render/task2_reflow.py`
  - `sed -n '1,220p' src/render/content.py`
- Узкая подготовка и syntax check:
  - `cp report/final_report.tex /tmp/berchun_h1_before_final_report.tex`
  - `cp report/assets_manifest.json /tmp/berchun_h1_before_assets_manifest.json`
  - `python3 -m compileall src/render`
- Каноническая пересборка:
  - `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
  - `python3 -m json.tool report/assets_manifest.json >/dev/null`
- Post-rebuild probes:
  - `rg -n "Числовой checkpoint|В числах это даёт|Для ориентира|По расчёту|На характерных точках|при увеличении|при изменении" report/final_report.tex`
  - `python3 - <<'PY' ... PY` для line-based сравнения pre/post формульных блоков, include basenames и всех числовых токенов
  - `python3 - <<'PY' ... PY` для unified diff по prose/caption drift
- Подтверждено:
  - `display_formula_count = 33`
  - `display_formulas_equal = true`
  - `number_token_multiset_equal = true`
  - `includegraphics_total = 33`
  - `plot_include_count = 27`
  - `scheme_count = 5`
  - `title_asset_count = 1`
  - sequence of include basenames preserved exactly
  - drift ограничен prose/caption surface lines; formulas и numeric tokens не изменились

## Whether the Report Now Feels Less Stylistically Uniform
- `YES, slightly`
- Изменение намеренно небольшое: текст стал менее ровно-шаблонным по связкам и ярлыкам, но не потерял прозрачности и teacher-facing объяснимости.

## Ready to Keep or Discard This Branch?
- `YES`
- Ветка остаётся опциональной и изолированной: её можно оставить как более живой surface-variant либо спокойно не принимать и вернуться к `P4`, не затрагивая никакой math/build truth.

## Exact Recommendation for Next Step
- Новый implementation scope не требуется. Провести только owner-side side-by-side review между текущим `H1` PDF и замороженным `P4` baseline и принять одно из двух решений: либо оставить `H1` как текущий teacher-facing default surface, либо отбросить его и сохранить `P4` как официальный frozen text surface.
