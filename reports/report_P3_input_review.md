# Scope ID and name
P3 — Input Review / Confirm-Before-Build UX

## Objective
Добавить узкий post-closeout UX-слой поверх существующего canonical intake/build flow: дать оператору возможность увидеть нормализованный raw input перед сборкой, в интерактивном режиме подтвердить или исправить поля, а в файловом режиме по запросу выполнить preview и явное подтверждение без изменения solver/report/archive semantics.

## Trusted inputs used
- `README.md`
- `reports/master_report.md`
- `reports/report_P2_run_archive.md`
- `src/cli.py`
- `src/input_schema.py`
- `src/intake.py`
- `src/build_pipeline.py`
- `inputs/examples/student_example.yaml`

## Files created
- `reports/report_P3_input_review.md`

## Files updated
- `src/cli.py`
- `src/intake.py`
- `src/build_pipeline.py`
- `README.md`
- `tests/test_input_validation.py`
- `tests/test_build_pipeline.py`
- `reports/master_report.md`

## What was implemented now
- В `src/intake.py` добавлен единый `canonical_input_summary(...)` для отображения уже нормализованного canonical raw input без введения второй input model.
- Интерактивный путь `build --interactive` теперь после ввода всегда проходит через review-loop:
  - показать summary;
  - принять `confirm`, `edit` или `cancel`;
  - при `edit` изменить одно выбранное поле и повторно провалидировать весь canonical raw input.
- Файловый путь получил опциональный `--review`:
  - `build --input ... --review` показывает тот же normalized summary;
  - далее принимает только `confirm` или `cancel`;
  - inline edit для file input не добавлялся.
- В `src/cli.py` review/prompts выведены в `stderr`, чтобы оператор видел UX-подсказки, а итоговый JSON summary `build` оставался чистым на `stdout`.
- Core `run_build(...)`, per-run archive `runs/<run_id>/...`, safe reuse policy по полному raw-input hash и solver/report pipeline не менялись по смыслу.

## UX flow summary
- Interactive:
  - пользователь вводит поля;
  - видит нормализованный canonical raw input;
  - выбирает `confirm`, `edit` или `cancel`;
  - после `confirm` запускается обычный `build`.
- File-based:
  - `build --input ...` ведёт себя как раньше и сразу запускает build после валидации;
  - `build --input ... --review` сначала показывает нормализованный canonical raw input;
  - затем пользователь выбирает `confirm` или `cancel`.

## What remained intentionally unchanged
- Solver mathematics, figure generation, report family и title-page logic не менялись.
- Run archive semantics из `P2` не менялись.
- Канонический raw-input schema и его валидация остались единственным источником истины.
- Для file-based review не добавлялось редактирование файла на месте или какая-либо альтернативная input model.

## Validation actually run
- `python3 -m unittest tests.test_input_validation tests.test_build_pipeline -v`
  - прошли новые узкие тесты на interactive review/edit/cancel и file-based review/build.
- `python3 -m src.cli --help`
  - подтверждено наличие `--review` и обновлённых operator examples.
- `mktemp -d /tmp/berchun_p3.XXXXXX`
  - создан isolated workspace: `/tmp/berchun_p3.IiBE3e`
- `python3 -m src.cli build --input inputs/examples/student_example.yaml --review --runs-dir /tmp/berchun_p3.IiBE3e/runs --variant-path /tmp/berchun_p3.IiBE3e/workspace/inputs/variant_me.yaml --derived-path /tmp/berchun_p3.IiBE3e/workspace/inputs/derived_parameters.json --out-dir /tmp/berchun_p3.IiBE3e/workspace/out/data --figures-dir /tmp/berchun_p3.IiBE3e/workspace/figures --manifest-path /tmp/berchun_p3.IiBE3e/workspace/out/artifacts/figure_manifest.json --report-source-path /tmp/berchun_p3.IiBE3e/workspace/report/final_report.tex --report-pdf-path /tmp/berchun_p3.IiBE3e/workspace/report/final_report.pdf --report-assets-manifest-path /tmp/berchun_p3.IiBE3e/workspace/report/assets_manifest.json`
  - вручную подтверждён `confirm`;
  - build завершился успешно и создал fresh run bundle.
- `python3 - <<'PY' ... PY`
  - подтверждено соответствие README новому `--review` пути;
  - подтверждено наличие `runs/index.json` и ненулевого `report/final_report.pdf` в temp run bundle.
- `python3 -m unittest discover -s tests -v`
  - итоговый полный suite прошёл: `21/21`, `OK`.

## Remaining risks
- File-based review intentionally ограничен preview + `confirm/cancel`; inline correction файла не реализована и требует либо редактирования input file вручную, либо `--interactive`.
- Review UX остаётся текстовым и командным (`confirm/edit/cancel`), без более сложного TUI/selector layer.
- Stage 07 loader по-прежнему intentionally поддерживает только flat scalar YAML / JSON-subset YAML для canonical schema.

## Ready to keep as canonical input UX? YES/NO
YES

## Exact recommendation for next scope
Обязательного следующего scope нет; сохранить текущий review/confirm слой как canonical operator UX поверх `build` и открывать новый post-closeout scope только по отдельному explicit request, не смешивая его с solver/report/archive redesign.
