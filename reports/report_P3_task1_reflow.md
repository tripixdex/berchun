# Report P3

## Scope ID and Name
- `P3 — Task 1 Sequential Derivation Reflow`

## Objective
- Выполнить третий teacher-facing polish pass только внутри `1.1`–`1.4`: сделать Task 1 более последовательной и объяснительной за счёт локального restaging formulas/prose, числовых checkpoint-фраз и более явной цепочки `состояния -> вероятности -> метрики -> график -> интерпретация`, не изменяя solver truth, figure data, scheme semantics или `2.1`.

## Trusted Inputs Used
- `docs/MVP_POLISH_PLAN.md`
- `docs/REPORT_PRESENTATION_CONTRACT.md`
- `docs/GLOBAL_ROADMAP.md`
- `docs/WORK_PROTOCOL.md`
- `reports/master_report.md`
- `reports/report_P1_numeric_notation.md`
- `reports/report_P2_plot_readability.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- текущий rendering layer под `src/render/`

## Files Created
- `src/render/task1_reflow_core.py`
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `reports/report_P3_task1_reflow.md`

## Files Updated
- `src/render/task1_reflow.py`
- `src/render/section_flow.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What Changed Now
- Для `1.1`–`1.4` введён отдельный render-local reflow helper, чтобы Task 1 собиралась не из слишком общих compressed blocks, а из более коротких смысловых шагов.
- В `1.1` добавлена более явная последовательность: переход от `Tc/Ts` к `a, p_k`, затем отдельно занятость операторов и затем вероятность отказа, с локальными числовыми checkpoint-фразами перед графиками.
- В `1.2` state formulas разбиты на два последовательных шага, а оба sweep-семейства теперь сопровождаются локальными checkpoint-примерами до графиков и краткой интерпретацией после них.
- В `1.3` усилен человеческий ритм вокруг границы стационарности: сначала отдельно проверяется `ρ_n < 1`, затем объясняется `P_wait`, затем только после этого показываются стационарные метрики занятости и очереди.
- В `1.4` dense block с Erlang-A restaged на два последовательных шага: сначала интенсивности переходов, затем рекуррентное построение и controlled truncation, после чего отдельно читаются занятость операторов и показатели очереди.
- Для соблюдения архитектурного hard-limit новый Task 1 reflow split выполнен на маленькие support-модули `task1_reflow_core.py`, `task1_reflow_11_12.py`, `task1_reflow_13_14.py`; `src/render/section_flow.py` при этом стал компактнее и остался ниже hard limit.

## What Intentionally Remained Unchanged
- Solver mathematics и `out/data` truth.
- Figure data, plot styling и figure ordering.
- Scheme semantics.
- Task hierarchy.
- Build / archive / input behavior.
- Весь текстовый и формульный flow `2.1`.

## Validation Actually Run
- Инспекция scope и render surface:
  - `sed -n '1,240p' docs/MVP_POLISH_PLAN.md`
  - `sed -n '1,260p' docs/REPORT_PRESENTATION_CONTRACT.md`
  - `sed -n '1,260p' reports/master_report.md`
  - `sed -n '1,240p' reports/report_P1_numeric_notation.md`
  - `sed -n '1,240p' reports/report_P2_plot_readability.md`
  - `wc -l src/render/*.py`
  - `sed -n '1,240p' src/render/content.py`
  - `sed -n '1,260p' src/render/section_flow.py`
  - `sed -n '1,240p' src/render/presentation.py`
  - `sed -n '1,240p' src/render/notation.py`
  - `sed -n '1,240p' src/render/specs.py`
- Архитектурный и синтаксический контроль:
  - `python3 -m compileall src/render`
  - проверка line counts после split: `src/render/task1_reflow.py = 15`, `src/render/task1_reflow_core.py = 30`, `src/render/task1_reflow_11_12.py = 128`, `src/render/task1_reflow_13_14.py = 100`, `src/render/section_flow.py = 142`
- Перед rebuild сохранены pre-P3 артефакты:
  - `cp report/final_report.tex /tmp/berchun_p3_before_final_report.tex`
  - `cp report/assets_manifest.json /tmp/berchun_p3_before_assets_manifest.json`
- Каноническая пересборка отчёта:
  - `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
  - `python3 -m json.tool report/assets_manifest.json >/dev/null`
- Локальные validation probes через `python3 - <<'PY' ... PY`:
  - подтверждено, что `Task 2` substring в `final_report.tex` идентичен pre-P3 версии;
  - подтверждено, что `Task 1` действительно изменилась;
  - подтверждены `27` plot includes, `5` input blocks, `5` notation blocks, `5` schemes и `1` title asset;
  - подтверждено наличие `8` фраз `Числовой checkpoint:` и новых bridge headings `Переход от исходных данных к вероятностям состояний.`, `Нормировка распределения.`, `Проверка стационарности.`, `Рекуррентное построение и усечение хвоста.`;
  - подтверждено сохранение truth markers `n = 8`, `n = 3`, `epsilon = 1e-12`;
  - подтверждено, что `Вероятность ожидания в задаче 2.1...` осталась на месте;
  - по корректному regex-check подтверждено, что display-formula sequence сохранилась `33/33`, а set формульных блоков в rebuilt Task 1 остаётся подмножеством pre-P3 формул без новых математических выражений;
  - через `pypdf.PdfReader` подтверждено, что rebuilt PDF содержит новые checkpoint-фразы и reflow headings уже в конечном артефакте.

## What Is Now Clearer for Teacher-Facing Reading
- `1.1` больше не прыгает от распределения сразу к графику: сначала появляется state model, затем локальный числовой checkpoint для занятости, затем отдельный checkpoint для порога отказов.
- `1.2` теперь читается как два осмысленных sweep-сценария с локальными примерами до графиков, а не как большой пакет figure dumps с минимальной связкой.
- `1.3` явно ведёт читателя через стационарность, `P_wait`, затем через устойчивые метрики; причина резкой очереди у границы устойчивости теперь проговаривается до просмотра графика.
- `1.4` перестала выглядеть как плотный technical dump: сначала объясняется механизм ухода клиентов и controlled truncation, затем отдельно читаются метрики занятости и очереди.

## What Still Remains for P4
- `2.1` ещё не доведена до такого же sequential/human-readable уровня.
- Финальная teacher-facing microfit по всему PDF ещё не выполнена.
- Локальные captions/prose вне Task 1 ещё не проходили завершающую унификацию по итогам `P3`.

## Ready for P4?
- `YES`

## Exact Recommendation for Next Scope
- Открыть `P4 — Task 2 Readability + Final Teacher-Facing Microfit` и ограничить его только `2.1` reflow плюс финальной локальной prose/caption доводкой по всему PDF, не трогая solver truth, figure data, scheme semantics, build/archive behavior или broader `Feature Branch`.
