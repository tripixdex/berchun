# Report P2

## Scope ID and Name
- `P2 — Plot Readability + Non-Stationary Visual Policy`

## Objective
- Выполнить второй teacher-facing polish pass только в plotting layer: убрать наложение legends на данные, приглушить внутренние plot titles/notes и зафиксировать финальную visual policy для `1.3` без изменения solver truth, figure data или build semantics.

## Trusted Inputs Used
- `docs/report/MVP_POLISH_PLAN.md`
- `docs/report/REPORT_PRESENTATION_CONTRACT.md`
- `docs/governance/GLOBAL_ROADMAP.md`
- `docs/governance/WORK_PROTOCOL.md`
- `reports/master_report.md`
- `reports/report_P1_numeric_notation.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- текущий plotting layer под `src/plots/`
- текущий rendering layer под `src/render/`

## Files Created
- `reports/report_P2_plot_readability.md`

## Files Updated
- `src/plots/common.py`
- `src/plots/style.py`
- `src/plots/task1_family.py`
- `src/plots/task1_simple.py`
- `src/plots/task2.py`
- PNG в `figures/`
- `out/artifacts/figure_manifest.json`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What Changed Now
- Для multi-series plots введена единая внешняя legend-policy: legend теперь выводится в отдельную верхнюю safe zone вне plotting field.
- Для single-series plots legends убраны полностью, если caption и оси уже однозначно объясняют смысл графика.
- Внутренние plot titles подавлены для data-driven charts, чтобы не дублировать report caption и не создавать synthetic clutter.
- Plot-local note на `2.1 waiting_probability` убрана как избыточная по отношению к caption и nearby prose.
- Для `1.3` удалена visual shaded region policy: нестационарность теперь остаётся только в локальном prose отчёта, без shaded/fill marker на графиках и без выдуманных stationary values.
- Для family plots `1.2` увеличено число legend columns до `5`, чтобы legend оставалась компактной и не заходила на данные.

## What Intentionally Remained Unchanged
- Solver mathematics и `out/data` truth.
- Figure data / series content.
- Scheme semantics.
- Run archive / build / input behavior.
- Локальный derivation flow и prose reflow, которые оставлены на `P3`.

## Validation Actually Run
- Инспекция scope и plotting surface:
  - `sed -n '1,220p' docs/report/MVP_POLISH_PLAN.md`
  - `sed -n '1,260p' docs/report/REPORT_PRESENTATION_CONTRACT.md`
  - `sed -n '1,220p' reports/report_P1_numeric_notation.md`
  - `rg --files src/plots src/render | sort`
  - `wc -l src/plots/*.py src/render/*.py`
  - `sed -n '1,260p' src/plots/common.py`
  - `sed -n '1,220p' src/plots/style.py`
  - `sed -n '1,260p' src/plots/task1_simple.py`
  - `sed -n '1,240p' src/plots/task1_family.py`
  - `sed -n '1,220p' src/plots/task2.py`
- Синтаксическая проверка plotting layer:
  - `python3 -m compileall src/plots`
- Пересборка figures:
  - `python3 -m src.cli figures --data-dir out/data --figures-dir figures --manifest-path out/artifacts/figure_manifest.json`
- Пересборка отчёта:
  - `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
- Проверка manifests:
  - `python3 -m json.tool out/artifacts/figure_manifest.json >/dev/null`
  - `python3 -m json.tool report/assets_manifest.json >/dev/null`
- Локальные validation probes через `python3 - <<'PY' ... PY`:
  - подтверждены `27` plot artifacts, `5` overview artifacts и `5` deferred schemes;
  - подтверждено совпадение plot id set с expected report figure set;
  - подтверждены `27` plot includes, `33` display-formula blocks, `5` input blocks и `5` notation blocks в rebuilt `final_report.tex`;
  - подтверждено сохранение truth markers `n = 8`, `n = 3`, `epsilon = 1e-12` и явного non-stationary prose;
  - для `figures/task1_3__queue_length_vs_operators.png` получено `shade_like_pixels = 0` по бывшему shade-color target.
- Визуальная проверка через `view_image`:
  - `figures/task1_1__refusal_and_utilization_vs_operators.png`
  - `figures/task1_2__refusal_vs_queue__family_by_operators.png`
  - `figures/task1_2__queue_exists_vs_operators__family_by_queue.png`
  - `figures/task1_3__queue_length_vs_operators.png`
  - `figures/task2_1__waiting_probability_vs_repairers.png`

## What Is Now Cleaner for Teacher-Facing Reading
- Family legends перестали спорить с кривыми и осевыми подписями.
- Single-series charts перестали тратить место на самоповторяющиеся legends.
- Внутренние chart titles больше не дублируют figure captions.
- `1.3` читаетcя спокойнее: нестационарность честно остаётся в prose, но больше не шумит shaded background на графике.

## What Still Remains for P3
- Плотные derivation blocks в `1.1`, `1.4` и частично `2.1` ещё не перестроены в более последовательный учебный ритм.
- Локальные numerical checkpoints и prose bridges вокруг формул остаются задачей `P3`.
- Task 1 всё ещё более систематизирована, чем accepted reference, на уровне формульного повествования.

## Ready for P3?
- `YES`

## Exact Recommendation for Next Scope
- Открыть `P3 — Task 1 Sequential Derivation Reflow` и ограничить его только local derivation/prose restaging внутри `1.1`–`1.4`, не трогая plot data, solver truth, scheme semantics, build/archive behavior или feature branch.
