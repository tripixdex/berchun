# Report P1

## Scope ID and Name
- `P1 — Numeric Display + Local Notation Hygiene`

## Objective
- Внести первый teacher-facing polish pass только в render-layer: нормализовать отображение чисел в тексте отчёта, сделать единым primitive блока `Исходные данные`, добавить обязательные локальные блоки `Обозначения:` после всех схем и не допустить drift по solver/data truth.

## Trusted Inputs Used
- `docs/MVP_POLISH_PLAN.md`
- `docs/REPORT_PRESENTATION_CONTRACT.md`
- `docs/GLOBAL_ROADMAP.md`
- `docs/WORK_PROTOCOL.md`
- `reports/master_report.md`
- `reports/report_P0_polish_plan.md`
- `reports/report_P0A_roadmap_consolidation.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- текущий rendering layer под `src/render/`

## Files Created
- `src/render/presentation.py`
- `src/render/notation.py`
- `reports/report_P1_numeric_notation.md`

## Files Updated
- `src/render/content.py`
- `src/render/section_flow.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What Changed Now
- Введён отдельный teacher-facing formatter, который показывает обычные числа максимум с `3` знаками после запятой, убирает хвостовые нули и использует форму `< 0.001` для ненулевых слишком малых значений вместо ложного `0.000`.
- Диагностические величины `1.4` сохранены в scientific form там, где это разрешено контрактом: `epsilon = 1e-12` и residual bounds.
- Блок `Исходные данные:` переведён на единый line-block primitive с одинаковым bold heading и отдельными строками для всех `1.1`, `1.2`, `1.3`, `1.4`, `2.1`.
- Сразу после каждой из `5` расчётных схем добавлен обязательный блок `Обозначения:` с локальным объяснением состояний, параметров и ближайших символов (`a`, `ρ_n`, `P_wait`, `P_ож` и др.).
- Локальные teacher-facing numeric phrases в `1.1`, `1.2`, `1.4`, `2.1` переведены на ту же numeric policy без изменения underlying JSON/artifact truth.

## What Intentionally Remained Unchanged
- Solver mathematics и `out/data` truth.
- Figure data и plot skin.
- Scheme semantics.
- Run archive / build / input behavior.
- Структурный skeleton и derivation flow из предыдущих passes, кроме минимально необходимой local notation hygiene.

## Validation Actually Run
- Инспекция planning/render surface:
  - `sed -n '1,220p' docs/MVP_POLISH_PLAN.md`
  - `sed -n '1,260p' docs/REPORT_PRESENTATION_CONTRACT.md`
  - `sed -n '1,260p' reports/master_report.md`
  - `rg --files src/render report | sort`
  - `sed -n '1,260p' src/render/common.py`
  - `sed -n '1,260p' src/render/content.py`
  - `sed -n '1,260p' src/render/report_builder.py`
  - `sed -n '1,260p' src/render/section_flow.py`
  - `sed -n '1,260p' src/render/specs.py`
  - `sed -n '1,260p' report/final_report.tex`
  - `rg -n "format_float\\(|scheme_note\\(|plain_lines_block\\(|Исходные данные|Обозначения" src/render src/plots report/final_report.tex`
- Синтаксическая проверка render-layer:
  - `python3 -m compileall src/render`
- Каноническая пересборка отчёта:
  - `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
- Проверка manifest:
  - `python3 -m json.tool report/assets_manifest.json >/dev/null`
- Локальные validation probes через `python3 - <<'PY' ... PY` с `pypdf` и regex:
  - подтверждены `5` блоков `Исходные данные:`
  - подтверждены `5` блоков `Обозначения:`
  - подтверждены `33` display-formula blocks, `27` plot includes и `5` scheme assets
  - подтверждено отсутствие old precision strings `0.016949` и `0.007471`
  - подтверждено присутствие `< 0.001`, `epsilon = 1e-12`, текущего threshold truth `n = 8` и current stationarity truth `n = 3`
  - подтверждено отсутствие teacher-facing decimal literals длиннее `3` знаков после запятой в rebuilt `final_report.tex`

## What Is Now Cleaner for Teacher-Facing Reading
- Числа в prose и notation blocks перестали выглядеть машинно-сырыми.
- После каждой схемы читатель сразу получает локальную карту обозначений, а не восстанавливает символы по памяти.
- Блоки `Исходные данные:` больше не дрейфуют между item’ами по виду и spacing primitive.
- В `1.2` малые ненулевые вероятности теперь показываются честно как `< 0.001`, а не как ложный ноль.

## What Still Remains for P2
- Plot-internal readability и `no legend overlap` policy ещё не трогались.
- Финальная visual convention для non-stationary shading в `1.3` остаётся задачей `P2`.
- Plot titles/legend placement/grid hierarchy остаются в текущем состоянии до отдельного plot pass.

## Ready for P2?
- `YES`

## Exact Recommendation for Next Scope
- Открыть `P2 — Plot Readability + Non-Stationary Visual Policy` и ограничить его только plot-local presentation: legend placement, non-stationary shading convention, title/label quieting и графическую читаемость без изменения figure data, solver truth или report structure.
