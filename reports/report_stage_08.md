# Stage ID and name
STAGE 08 — Packaging + Operating Playbook

## Objective
Сделать канонический usage path репозитория очевидным для нового оператора, не меняя solver/report core: добавить минимально достаточную operator-facing документацию, при необходимости уточнить CLI help и честно оценить, близок ли репозиторий к frozen state в рамках текущего учебного scope.

## Trusted inputs used
- `reports/master_report.md`
- `reports/report_stage_07.md`
- `docs/project/SPEC.md`
- `docs/report/REPORT_CONTRACT.md`
- `src/cli.py`
- `src/input_schema.py`
- `src/intake.py`
- `src/build_pipeline.py`
- `inputs/examples/student_example.yaml`
- `out/artifacts/figure_manifest.json`
- `report/assets_manifest.json`
- `report/final_report.tex`
- `report/final_report.pdf`

## Files created
- `README.md`
- `reports/report_stage_08.md`

## Files updated
- `src/cli.py`
- `reports/master_report.md`

## What was improved now
- Добавлен корневой `README.md`, который закрывает operator-facing вопросы без размазывания документации по нескольким каталогам:
  - purpose и high-level pipeline;
  - канонические команды `build --input` и `build --interactive`;
  - ожидаемые default outputs, включая `report/final_report.pdf`;
  - перечень raw fields;
  - что редактировать и что не редактировать вручную;
  - краткая карта репозитория;
  - разделение canonical vs internal/historical artifacts.
- Уточнён `python3 -m src.cli --help`:
  - `build` явно обозначен как canonical operator entrypoint;
  - lower-level команды `solve`, `figures`, `report` явно описаны как audit/debug path;
  - help теперь показывает пример команды и default output paths.
- В корневом README явно задокументированы два места, которые иначе легко перепутать:
  - `inputs/variant_me.yaml` в текущем snapshot остаётся historical artifact, но default `build` будет писать туда raw input текущего прогона;
  - `figures/task_*.png` являются overview PNG для inspection и не являются теми plot files, которые вставляются в финальный отчёт.

## What remained intentionally unchanged
- Не менялись solver mathematics, derived formulas, plotting logic и report family.
- Не добавлялись локальные README в `inputs/examples`, `report/` или `src/`:
  - после проверки оказалось, что сильный root `README.md` и улучшенный CLI help уже закрывают operator navigation;
  - дополнительные README здесь лишь дублировали бы одни и те же canonical commands.
- Не выполнялась broad repository cleanup:
  - `.DS_Store`, `__pycache__`, large reference binaries и другие incidental files не удалялись в этом stage, чтобы не расширять scope с documentation/handoff до cleanup pass.
- Не менялись committed canonical report artifacts в репозитории; validation снова выполнялась в изолированном temp workspace.

## Validation actually run
- `python3 -m src.cli --help`
  - confirmed that help text now exposes the canonical `build` path, examples, and default output locations.
- `python3 -m unittest discover -s tests -v`
  - passed: `14/14`, `OK`
- `mktemp -d /tmp/berchun_stage08.XXXXXX`
  - created: `/tmp/berchun_stage08.SwioGw`
- `python3 -m src.cli build --input inputs/examples/student_example.yaml --variant-path /tmp/berchun_stage08.SwioGw/inputs/variant_me.yaml --derived-path /tmp/berchun_stage08.SwioGw/inputs/derived_parameters.json --out-dir /tmp/berchun_stage08.SwioGw/out/data --figures-dir /tmp/berchun_stage08.SwioGw/figures --manifest-path /tmp/berchun_stage08.SwioGw/out/artifacts/figure_manifest.json --report-source-path /tmp/berchun_stage08.SwioGw/report/final_report.tex --report-pdf-path /tmp/berchun_stage08.SwioGw/report/final_report.pdf --report-assets-manifest-path /tmp/berchun_stage08.SwioGw/report/assets_manifest.json`
  - succeeded; produced canonical raw, derived, data, figures, TeX, PDF, and assets manifest in one high-level run.
- `python3 -m json.tool /tmp/berchun_stage08.SwioGw/out/artifacts/figure_manifest.json >/dev/null`
- `python3 -m json.tool /tmp/berchun_stage08.SwioGw/report/assets_manifest.json >/dev/null`
  - both succeeded.
- `python3 - <<'PY' ... PY`
  - checked that `README.md` contains the documented canonical command snippets and expected artifact path references;
  - checked that the repository paths named in the README actually exist;
  - checked that temp build outputs exist and are non-empty, including `/tmp/berchun_stage08.SwioGw/report/final_report.pdf`.

## Repository cleanliness findings
- Root and generated-artifact directories still contain incidental `.DS_Store` files:
  - `.DS_Store`
  - `out/.DS_Store`
  - `report/.DS_Store`
- Generated figure directory contains both:
  - canonical report-linked plot PNG;
  - overview PNG files `figures/task_1_1.png`, `figures/task_1_2.png`, `figures/task_1_3.png`, `figures/task_1_4.png`, `figures/task_2_1.png`.
  These overview files are real generated artifacts, but they are not referenced by `report/assets_manifest.json`.
- Historical/compatibility artifacts remain in place:
  - `inputs/variant_me.yaml` is still the legacy validated snapshot in the committed tree until a user runs `build` with default outputs;
  - `references/DZ2/.vs/` and related large reference binaries remain outside the Stage 08 cleanup boundary.
- Program files above the soft size target were inspected:
  - `src/cli.py`: `158` lines after the help-text pass;
  - `src/variant.py`: `171` lines;
  - `src/render/content.py`: `176` lines.
  They remain below the hard limit, and splitting them here would have widened Stage 08 into refactoring instead of operator handoff work.

## README coverage rationale
- Added only one README: the repository root.
- Did not add local README files because the main operator questions are all answered centrally:
  - what command to run;
  - what input file format to use;
  - where the final PDF appears;
  - what outputs are generated;
  - which paths are canonical vs internal/historical.
- Additional local README files would have repeated the same information and increased documentation drift risk.

## Operator handoff summary
- Normal operator entrypoint: `python3 -m src.cli build ...`
- Example input file: `inputs/examples/student_example.yaml`
- Interactive intake path: `python3 -m src.cli build --interactive`
- Canonical final PDF path with default outputs: `report/final_report.pdf`
- Generated/internal artifacts that should not be hand-edited for normal use:
  - `inputs/derived_parameters.json`
  - `out/data/*.json`
  - `out/artifacts/figure_manifest.json`
  - `report/final_report.tex`
  - `report/assets_manifest.json`
- Lower-level commands `solve`, `figures`, `report` remain available, but they are no longer the recommended human-facing path.

## Frozen-readiness assessment: YES/NO with explanation
YES

Для intended coursework/operator-handoff scope репозиторий теперь достаточно близок к frozen state:
- канонический usage path явно документирован и подтверждён реальным rerun;
- one-command build produces the expected final package without tribal knowledge;
- canonical vs internal/historical artifacts are explicitly separated in the root README and CLI help;
- текущие residual issues относятся к cleanliness and legacy clutter, а не к отсутствию рабочего operator path.

Это не означает polished distributable product beyond repo scope; это означает, что в рамках текущей учебной задачи и handoff-модели новых обязательных engineering passes не видно.

## Exact recommendation for the next step
Объявить repository closeout-ready for its intended scope and использовать `README.md` вместе с `python3 -m src.cli build` как канонический operator handoff; любые дальнейшие работы открывать только отдельным explicit scope, например cleanup pass или distribution-oriented packaging, не смешивая их с уже замороженным solver/report core.
