# Stage ID and name
STAGE 07 — Generalize to Any Variant

## Objective
Добавить минимальный канонический intake/build слой поверх уже подтверждённого аналитического контура, чтобы пользователь мог один раз ввести полный набор raw inputs и затем получить `derived -> out/data -> figures -> final report` одним high-level command.

## Trusted inputs used
- `reports/master_report.md`
- `reports/report_stage_06.md`
- `docs/SPEC.md`
- `docs/REPORT_CONTRACT.md`
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `src/cli.py`
- `src/pipeline.py`
- `src/variant.py`
- `src/plots/__init__.py`
- `src/render/report_builder.py`
- `report/final_report.tex`
- `report/assets_manifest.json`

## Files created
- `src/input_schema.py`
- `src/intake.py`
- `src/build_pipeline.py`
- `inputs/examples/student_example.yaml`
- `tests/test_input_validation.py`
- `tests/test_build_pipeline.py`
- `reports/report_stage_07.md`

## Files updated
- `src/cli.py`
- `src/variant.py`
- `src/render/content.py`
- `reports/master_report.md`

## What was implemented now
- Введён единый канонический raw-input schema для Stage 07 с обязательными полями:
  - `student_full_name`
  - `student_group`
  - `teacher_full_name`
  - `journal_number`
  - `birth_day`
  - `birth_month`
  - `birth_year`
  - `report_year`
- Добавлена строгая валидация:
  - непустые нормализованные строки для ФИО/группы/преподавателя;
  - положительный `journal_number`;
  - проверка валидной даты по `birth_day`, `birth_month`, `birth_year`;
  - разумный диапазон `report_year`.
- Добавлена поддержка двух intake-путей:
  - interactive prompt flow через `python3 -m src.cli build --interactive`;
  - file-based flow через `python3 -m src.cli build --input ...`.
- Добавлен high-level build orchestrator:
  - сохраняет канонический raw artifact;
  - детерминированно пересчитывает `inputs/derived_parameters.json`-совместимый derived artifact;
  - запускает существующие `solve -> figures -> report` шаги без изменения solver mathematics.
- Сохранена backward compatibility:
  - старые команды `solve`, `figures`, `report` не удалены;
  - `src.variant.load_variant` теперь понимает и прежний Stage 02 nested format, и новый канонический Stage 07 raw-input document.
- Удалено жёсткое связывание титульного листа с захардкоженными ФИО:
  - `src/render/content.py` теперь берёт title metadata из канонического raw-input document;
  - при старом формате остаётся fallback на существующие Stage 06 значения, чтобы не ломать прежний низкоуровневый report path.

## What remained unchanged intentionally
- Не менялись аналитические формулы, sweep-политики, figure family и report family.
- Не менялся текущий исторический `inputs/variant_me.yaml` в репозитории:
  - в доступных trusted sources отсутствует подтверждённый `birth_year` для текущего студента;
  - вместо выдумывания этого значения Stage 07 вводит schema + example + build flow, который сам записывает канонический raw artifact, когда пользователь даёт полный набор данных.
- Не пересобирались текущие canonical `report/final_report.tex` и `report/final_report.pdf` в самом репозитории:
  - Stage 07 валидировал general build flow в чистом temp workspace;
  - это не требовало переписывать reference-grade Stage 06 report package.
- Не открывался новый scope по packaging/distribution beyond Stage 07.

## Validation actually run
- `python3 -m unittest tests.test_input_validation tests.test_build_pipeline -v`
  - passed: `5/5`, `OK`
- `python3 -m unittest discover -s tests -v`
  - passed: `14/14`, `OK`
- `mktemp -d /tmp/berchun_stage07_final.XXXXXX`
- `python3 -m src.cli build --input inputs/examples/student_example.yaml --variant-path /tmp/berchun_stage07_final.mBwaDX/inputs/variant_me.yaml --derived-path /tmp/berchun_stage07_final.mBwaDX/inputs/derived_parameters.json --out-dir /tmp/berchun_stage07_final.mBwaDX/out/data --figures-dir /tmp/berchun_stage07_final.mBwaDX/figures --manifest-path /tmp/berchun_stage07_final.mBwaDX/out/artifacts/figure_manifest.json --report-source-path /tmp/berchun_stage07_final.mBwaDX/report/final_report.tex --report-pdf-path /tmp/berchun_stage07_final.mBwaDX/report/final_report.pdf --report-assets-manifest-path /tmp/berchun_stage07_final.mBwaDX/report/assets_manifest.json`
  - succeeded; high-level build wrote canonical raw, derived, data, figures, and report artifacts in one run
- `python3 -m json.tool` on:
  - `/tmp/berchun_stage07_final.mBwaDX/inputs/variant_me.yaml`
  - `/tmp/berchun_stage07_final.mBwaDX/inputs/derived_parameters.json`
  - `/tmp/berchun_stage07_final.mBwaDX/out/artifacts/figure_manifest.json`
  - `/tmp/berchun_stage07_final.mBwaDX/report/assets_manifest.json`
  - all succeeded
- `python3 - <<'PY' ... PY`
  - checked that temp raw/derived/report artifacts exist and are non-empty;
  - checked that temp `final_report.tex` contains the example title metadata;
  - extracted text from temp `final_report.pdf` via `pypdf.PdfReader` and confirmed the generated PDF contains the same student/group/teacher data and `Москва, 2026 г.`

## Remaining risks
- `src/input_schema.py` intentionally supports only:
  - JSON-subset YAML documents;
  - flat scalar YAML mappings for the Stage 07 canonical fields.
  This is sufficient for the current schema and example, but it is not a general-purpose YAML loader.
- The repository snapshot still keeps legacy `inputs/variant_me.yaml` as the historical confirmed variant artifact; the new full-schema raw artifact appears when the user runs Stage 07 build with actual full input.
- Existing files remain above the soft size target though below the hard limit:
  - `src/variant.py`: `171` lines;
  - `src/render/content.py`: `176` lines.
  They were not split further to avoid widening Stage 07 into a refactor pass.

## UX summary of the new intake/build flow
- Interactive path:
  - `python3 -m src.cli build --interactive --variant-path <raw_output.yaml> --derived-path <derived.json> --out-dir <out/data> --figures-dir <figures> --manifest-path <figure_manifest.json> --report-source-path <final_report.tex> --report-pdf-path <final_report.pdf> --report-assets-manifest-path <assets_manifest.json>`
- File-based path:
  - `python3 -m src.cli build --input inputs/examples/student_example.yaml ...`
- In both paths the user does not enter derived parameters manually.
- The high-level build command performs:
  - intake/load;
  - validation;
  - canonical raw artifact write;
  - deterministic derivation;
  - solve;
  - figure generation;
  - final report build.

## Ready to proceed to Stage 08? YES/NO
YES

## Exact recommendation for the next stage
Если нужен следующий этап, открывать Stage 08 только как packaging/distribution or operator-handoff pass поверх уже работающего Stage 07 intake/build flow; solver mathematics и report family на этом основании менять не требуется.
