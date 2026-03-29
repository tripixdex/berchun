# Report M1 — Methodical Section Skeleton + Artifact Mapping

## Scope ID and Name
- Scope ID: `M1`
- Scope name: `Methodical Section Skeleton + Artifact Mapping`

## Objective
Заморозить канонический skeleton будущего methodical guide, generation-ready artifact map для `1.1`, `1.2`, `1.3`, `1.4`, `2.1` и repeatable defense-note template, не начиная ещё реальную prose generation.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/METHODICAL_GUIDE_PLAN.md`
- `docs/METHODICAL_GUIDE_CONTRACT.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`
- `out/artifacts/figure_manifest.json`
- `report/assets_manifest.json`

## Files Created
- `docs/METHODICAL_GUIDE_SKELETON.md`
- `docs/METHODICAL_ARTIFACT_MAP.md`
- `docs/METHODICAL_DEFENSE_TEMPLATE.md`
- `reports/report_M1_methodical_skeleton.md`

## Files Updated
- `reports/master_report.md`

## Commands Run
- `sed -n '1,240p' reports/master_report.md`
- `sed -n '1,240p' docs/METHODICAL_GUIDE_PLAN.md`
- `sed -n '1,260p' docs/METHODICAL_GUIDE_CONTRACT.md`
- `sed -n '1,260p' report/final_report.tex`
- `sed -n '261,520p' report/final_report.tex`
- `sed -n '520,760p' report/final_report.tex`
- `pdftotext report/final_report.pdf - | sed -n '1,220p'`
- `pdftotext report/final_report.pdf - | sed -n '220,420p'`
- `sed -n '1,220p' inputs/variant_me.yaml`
- `sed -n '1,260p' inputs/derived_parameters.json`
- `sed -n '1,220p' out/data/task_1_1.json`
- `sed -n '1,240p' out/data/task_1_2.json`
- `sed -n '1,220p' out/data/task_1_3.json`
- `sed -n '1,240p' out/data/task_1_4.json`
- `sed -n '1,240p' out/data/task_2_1.json`
- `sed -n '1,260p' out/artifacts/figure_manifest.json`
- `sed -n '1,220p' report/assets_manifest.json`
- `rg -n '"sweep_kind"|"fixed_parameters"|"queue_places"|"operators"' out/data/task_1_2.json`
- `rg -n 'task1_4__|task2_1__' out/artifacts/figure_manifest.json`
- `rg -n 'waiting_probability|busy_repairers_expected|repairers_utilization|idle_machines_expected|waiting_machines_expected|queue_exists_probability_state|x_value' out/data/task_2_1.json`
- `rg -n 'busy_operators_expected|operators_utilization|queue_exists_probability|queue_length_expected|queue_occupancy|refusal_probability|x_value|wait_probability|traffic_intensity' out/data/task_1_3.json out/data/task_1_4.json`

## What Was Defined Now
- Зафиксирована каноническая структура будущего guide на уровне guide-level sections и точного subsection order.
- Заморожены mandatory blocks, которые обязаны повторяться в каждом подпункте.
- Заморожен generation-ready artifact map с selector rules и точными data/figure dependencies.
- Заморожен repeatable defense-note template с обязательными полями и минимальным набором карточек на подпункт.

## Skeleton Summary
- Будущий guide имеет короткий guide-level header, затем проходит по `1.1`, `1.2`, `1.3`, `1.4`, `2.1` в порядке formal report.
- Каждый подпункт заканчивается двумя обязательными блоками:
  - `Что это значит простыми словами`
  - `Что сказать на защите`
- Для каждого graph block заморожен micro-order `метрика -> checkpoint -> verbal bridge -> чтение графика -> локальный вывод`.
- `1.2` отдельно зафиксирован как подпункт с двумя family blocks, а не как один плоский массив графиков.

## Artifact Mapping Summary
- Guide-level header берёт student/raw identity из `inputs/variant_me.yaml`, derived/sweep policies из `inputs/derived_parameters.json`, а ordering/report surface — из `report/assets_manifest.json` и current report.
- `1.1` читает threshold logic из `out/data/task_1_1.json` через first `refusal_probability < 0.01`.
- `1.2` читает две family surfaces из `out/data/task_1_2.json` и использует selector-backed checkpoints по `n_load_anchor`, `m = 5`, `m = 15`, `n_relief_task1`.
- `1.3` опирается на first stationary point и никогда не invents stationary values for `non_stationary` points.
- `1.4` дополнительно читает truncation policy и worst-case tail bounds, а не только plot metrics.
- `2.1` читает both `waiting_probability` and `queue_exists_probability_state`, чтобы guide не путал arrival-weighted ожидание нового отказа с календарной вероятностью очереди.

## Remaining Open Questions
- Формат конечного generated output по-прежнему не заморожен глубже, чем skeleton/content/template layer.
- Точная плотность future prose внутри каждого блока остаётся задачей `M2`, а не `M1`.
- Количество дополнительных defense cards сверх минимального набора может быть уточнено в `M2`, но базовый шаблон уже frozen.

## Validation
- Scope является `documentation-only` / `skeleton-only`.
- Проверено, что current report surface доступна и в `TeX`, и в `PDF`.
- Проверено, что machine-readable outputs и manifests содержат достаточно данных для frozen selector rules.
- Реальная guide generation, export и runtime integration не запускались.

## Ready for M2?
- `YES`

## Exact Recommendation For Next Step
- Открыть `M2 — Variant-Aware Core Explanation Generation`.
- В `M2` ограничиться сборкой простых explanatory blocks из уже замороженных selectors и artifact dependencies для `1.1`, `1.2`, `1.3`, `1.4`, `2.1`, не открывая ещё export surface и не раздувая branch в platform/document flow.
