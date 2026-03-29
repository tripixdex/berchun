# Scope Report

## Scope ID and Name
- `Feature-01 — Report Scope Selection + Input UX Upgrade`

## Objective
- Добавить `report_scope = task1 | task2 | full`, ускорить canonical operator input path и сохранить корректный build/archive behavior без изменения solver truth и teacher-facing математики.

## Trusted Inputs Used
- `docs/GLOBAL_ROADMAP.md`
- `docs/WORK_PROTOCOL.md`
- `reports/master_report.md`
- `README.md`
- `src/input_schema.py`
- `src/intake.py`
- `src/build_pipeline.py`
- `src/cli.py`
- `src/render/report_builder.py`
- `src/render/section_flow.py`
- `tests/test_input_validation.py`
- `tests/test_build_pipeline.py`
- `tests/test_run_archive.py`
- `tests/test_variant_integrity.py`

## Files Created
- `src/report_scope.py`
- `reports/report_Feature_01_scope_input.md`

## Files Updated
- `src/input_schema.py`
- `src/intake.py`
- `src/build_pipeline.py`
- `src/cli.py`
- `src/run_archive.py`
- `src/variant.py`
- `src/render/report_builder.py`
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `inputs/examples/student_example.yaml`
- `README.md`
- `tests/test_input_validation.py`
- `tests/test_build_pipeline.py`
- `tests/test_run_archive.py`
- `tests/test_variant_integrity.py`
- `reports/master_report.md`

## What Was Implemented Now
- В canonical raw input добавлено поле `report_scope` с допустимыми значениями `task1`, `task2`, `full`.
- Operator-facing schema переведена на одно поле `birth_date` в формате `ДД.ММ.ГГГГ`; старые `birth_day/birth_month/birth_year` оставлены только для backward-compatible чтения.
- `teacher_full_name` теперь по умолчанию равен `Берчун Юрий Валерьевич`, если поле не задано явно.
- В интерактивном intake добавлены quick-choice группы `РК9-81Б`, `РК9-82Б`, `РК9-83Б`, `РК9-84Б`, `другая группа`, а `report_scope` по умолчанию равен `full`.
- `report_year` больше не спрашивается в normal interactive path и автоматически берётся из локального текущего года; file-based override сохранён как optional field.
- `build` теперь передаёт `report_scope` в report assembly, а low-level `report` получил `--report-scope` для audit/debug use.
- Report builder стал scope-aware: `task1` включает только разделы задачи 1, `task2` только задачу 2, `full` сохраняет исходный full report path; manifest теперь фиксирует `report_scope` и только реально использованные task data / schemes / plots.
- `report_scope` включён в canonical raw-input identity и участвует в `raw_input_hash`, поэтому разные scope не переиспользуют один и тот же run.
- Локально убрана variant-fragility в Task 1 reflow: характерные точки для `1.1` и `1.3` теперь берутся из текущих task outputs, а не из старых зашитых `n = 3/5/8`.

## What Was Intentionally Left Unchanged
- Solver truth и все `out/data` semantics.
- Figure data и series content.
- Scheme semantics и frozen teacher-facing report style.
- Run archive policy кроме обязательного включения `report_scope` в input identity.
- Solve/figures contour остаётся полным; partial modes фильтруют именно report assembly, а не solver outputs.

## Validation Actually Run
- `python3 -m compileall src`
- `python3 -m unittest tests.test_input_validation tests.test_build_pipeline tests.test_run_archive -v`
- `python3 -m unittest discover -s tests -v`
- `python3 -m src.cli --help`

Validation facts from executed checks:
- interactive path проверен на default teacher, group quick-select, custom group, single-field `birth_date`, auto `report_year`, review/edit/cancel;
- file-based review path проверен на normalized preview;
- real CLI builds внутри `tests.test_build_pipeline` прошли для `full`, `task1` и `task2`;
- `report_scope` verified as part of raw-input hash and run reuse decision;
- full test suite after the final code state: `25/25 OK`.

## Remaining Risks
- Частичные режимы `task1` и `task2` пока не сокращают solve/figures stage; они используют полный вычислительный контур и затем ограничивают только report assembly.
- Canonical input loader по-прежнему intentionally ограничен flat scalar YAML / JSON-subset YAML.
- `src/cli.py` остаётся выше soft size target, но после Feature-01 снова ниже hard limit.

## Ready for Next Feature Stage?
- `YES`

## Exact Recommendation for Next Scope
- Открыть `Feature-02 — DOCX/exportable editable version` как отдельный narrow pass поверх текущего scope-aware build path, не смешивая его с solver/report mathematics, bot/platform scopes или новой переработкой teacher-facing PDF.
