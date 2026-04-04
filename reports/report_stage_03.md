# Stage ID and name
STAGE 03: Generate Figures + Package Artifacts

## Objective
Сгенерировать все data-driven figure artifacts строго из текущих `out/data/*.json`, упаковать их в чистую структуру для следующей стадии, выпустить machine-readable manifest и не затрагивать solver layer.

## Trusted inputs used
- `docs/project/SPEC.md`
- `docs/report/REPORT_CONTRACT.md`
- `reports/report_stage_02.md`
- `reports/master_report.md`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`

## Files created
- `src/plots/__init__.py`
- `src/plots/common.py`
- `src/plots/task1.py`
- `src/plots/task1_simple.py`
- `src/plots/task1_family.py`
- `src/plots/task2.py`
- `tests/test_plots.py`
- `figures/*.png` (`32` deterministic PNG-файла, полный перечень зафиксирован в `out/artifacts/figure_manifest.json`)
- `out/artifacts/figure_manifest.json`
- `reports/report_stage_03.md`

## Files updated
- `src/cli.py`
- `reports/master_report.md`

## Implemented now
- Добавлен отдельный plotting-layer в `src/plots/` без изменения solver logic.
- Реализован figure generation path `python3 -m src.cli figures`.
- Сгенерированы `27` индивидуальных data-driven plot PNG:
  - `1.1`: `2`
  - `1.2`: `12`
  - `1.3`: `4`
  - `1.4`: `4`
  - `2.1`: `5`
- Дополнительно сгенерированы `5` обзорных PNG:
  - `figures/task_1_1.png`
  - `figures/task_1_2.png`
  - `figures/task_1_3.png`
  - `figures/task_1_4.png`
  - `figures/task_2_1.png`
- Выпущен `out/artifacts/figure_manifest.json` с `32` generated entries и `5` deferred entries для scheme-артефактов.
- Сокращено дублирование plotting-конфигурации, подписей осей, manifest entry-формата и figure naming logic через `src/plots/common.py`.
- File-length discipline соблюдена:
  - hard limit `180` не превышен;
  - наибольший файл `src/plots/common.py` имеет ровно `180` строк.

## Validated now
- Выполнен `python3 -m src.cli figures`.
- Выполнен `python3 -m unittest discover -s tests -v` (`9/9`, `OK`).
- Выполнен `python3 -m json.tool out/artifacts/figure_manifest.json`.
- Подтверждено, что все обязательные overview-файлы существуют и имеют ненулевой размер.
- Подтверждено, что generated entries в manifest ссылаются только на:
  - `out/data/task_1_1.json`
  - `out/data/task_1_2.json`
  - `out/data/task_1_3.json`
  - `out/data/task_1_4.json`
  - `out/data/task_2_1.json`

## Inferred only
- Контракт Stage 03 интерпретирован так: генерируются все data-driven plots, доступные из существующих JSON, а расчётные схемы не генерируются автоматически, потому что их источник не содержится в `out/data/*.json`.
- Фигура `task2_1__waiting_probability_vs_repairers.png` наследует modelling choice Stage 02: `waiting_probability` трактуется как arrival-weighted вероятность ожидания для новой заявки.
- Обзорные `figures/task_*.png` интерпретированы как packaging-friendly sheets для reviewer-path и следующей сборочной стадии, а не как замена индивидуальных plot-файлов в финальном отчёте.

## Deferred
- Автоматическая генерация расчётных схем.
- Формульные/OMML-совместимые артефакты.
- Финальная сборка отчёта.
- Любая визуальная полировка сверх базовой report-readable plot readability.

## Remaining risks
- `docs/report/REPORT_CONTRACT.md` в минимальном наборе рисунков учитывает и расчётные схемы; они не построены на Stage 03, потому что текущая стадия ограничена JSON-driven figures.
- Семейства графиков `1.2` содержат по `15` кривых на панель; это честно отражает данные, но визуально плотнее остальных figure artifacts.
- Семантика `waiting_probability` для `2.1` остаётся зависимой от ранее выбранной трактовки и должна быть сохранена неизменной в Stage 04.

## Figure inventory
- Generated plot figures:
  - `1.1`: `task1_1__busy_operators_vs_operators.png`, `task1_1__refusal_and_utilization_vs_operators.png`
  - `1.2`: `12` family-plot PNG с суффиксами `vs_queue__family_by_operators` и `vs_operators__family_by_queue`
  - `1.3`: `task1_3__busy_operators_vs_operators.png`, `task1_3__operators_utilization_vs_operators.png`, `task1_3__queue_exists_vs_operators.png`, `task1_3__queue_length_vs_operators.png`
  - `1.4`: `task1_4__busy_operators_vs_operators.png`, `task1_4__operators_utilization_vs_operators.png`, `task1_4__queue_exists_vs_operators.png`, `task1_4__queue_length_vs_operators.png`
  - `2.1`: `task2_1__idle_machines_vs_repairers.png`, `task2_1__waiting_machines_vs_repairers.png`, `task2_1__waiting_probability_vs_repairers.png`, `task2_1__busy_repairers_vs_repairers.png`, `task2_1__repairers_utilization_vs_repairers.png`
- Generated overview figures:
  - `task_1_1.png`
  - `task_1_2.png`
  - `task_1_3.png`
  - `task_1_4.png`
  - `task_2_1.png`
- Deferred manifest-only entries:
  - `task1_1__scheme`
  - `task1_2__scheme`
  - `task1_3__scheme`
  - `task1_4__scheme`
  - `task2_1__scheme`

## Artifact packaging summary
- Все generated images лежат в `figures/`.
- Все связи `figure id -> source json -> output path -> semantic description -> status` зафиксированы в `out/artifacts/figure_manifest.json`.
- Manifest содержит:
  - `32` generated artifact entries;
  - `5` deferred scheme entries;
  - детерминированный generator marker `matplotlib_agg`.
- Для следующей стадии `figure_manifest.json` уже даёт reviewer-safe индекс того, какие plot-файлы готовы к вставке в отчёт, а какие scheme-файлы ещё отсутствуют.

## Sanitation check
- Solver logic не пересчитывалась и не менялась.
- Подтверждённые raw inputs не менялись.
- Дополнительная документация сверх обязательного stage-report не создавалась.
- Временные `__pycache__` после прогонов удалены.
- Git не трогался.

## Prompt re-check
- Сначала inspected Stage 02 outputs и report contract: выполнено.
- Определён точный figure set: выполнено.
- Реализованы узкие plotting modules: выполнено.
- Фигуры построены только из существующих JSON outputs: выполнено.
- Manifest создан: выполнено.
- Narrow validation реально запущена: выполнено.
- Отчёты обновляются в конце: выполнено.

## READY TO CLOSE? YES/NO
YES

## Exact recommendation for the next stage
`STAGE 04 — Assemble Final Report`

Точный следующий шаг:
- использовать `out/artifacts/figure_manifest.json` как индекс figure artifacts;
- собрать недостающие scheme/formula artifacts из не-JSON источников;
- вставить индивидуальные plot PNG и scheme/formula artifacts в структуру отчёта по `docs/report/REPORT_CONTRACT.md`;
- не начинать финальный closeout раньше завершения полной сборки отчёта.
