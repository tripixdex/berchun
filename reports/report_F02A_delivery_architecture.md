# Report F02A — Delivery Surface Architecture Freeze

## Scope ID and Name
- Scope ID: `F02A`
- Scope name: `Delivery / Export Surface Architecture Freeze`

## Objective
Заморозить architecture и operator contract для нового delivery/export surface поверх уже frozen formal report baseline, scope-aware build path и frozen methodical branch, не открывая реализацию export.

## Trusted Inputs Used
- `reports/master_report.md`
- `README.md`
- `docs/METHODICAL_GUIDE_PLAN.md`
- `docs/METHODICAL_GUIDE_CONTRACT.md`
- `docs/METHODICAL_GUIDE.md`
- `docs/REPORT_CONTRACT.md`
- `docs/WORK_PROTOCOL.md`
- `reports/report_Feature_01_scope_input.md`
- `src/cli.py`
- `src/build_pipeline.py`
- `src/report_scope.py`
- `src/run_archive.py`
- `src/render/report_builder.py`
- `src/render/specs.py`
- current `runs/<run_id>/...` bundle layout

## Files Created
- `docs/DELIVERY_SURFACE_PLAN.md`
- `docs/DELIVERY_SURFACE_CONTRACT.md`
- `docs/DELIVERY_OUTPUT_MATRIX.md`
- `reports/report_F02A_delivery_architecture.md`

## Files Updated
- `reports/master_report.md`

## Commands Run
- `sed -n '1,240p' reports/master_report.md`
- `sed -n '1,260p' README.md`
- `rg -n 'report_scope|scope|task1|task2|full|review|build --interactive|build --review|Feature-01|delivery|export|docx' docs src README.md reports -g '!reports/report_*'`
- `sed -n '1,260p' docs/METHODICAL_GUIDE_PLAN.md`
- `sed -n '1,260p' docs/METHODICAL_GUIDE_CONTRACT.md`
- `sed -n '1,220p' docs/METHODICAL_GUIDE.md`
- `sed -n '1,260p' src/cli.py`
- `sed -n '1,260p' src/build_pipeline.py`
- `sed -n '1,220p' src/report_scope.py`
- `sed -n '1,220p' src/run_archive.py`
- `sed -n '1,260p' src/render/report_builder.py`
- `sed -n '1,220p' src/render/specs.py`
- `sed -n '1,220p' docs/REPORT_CONTRACT.md`
- `sed -n '1,240p' reports/report_Feature_01_scope_input.md`
- `sed -n '1,220p' docs/WORK_PROTOCOL.md`
- `find runs -maxdepth 3 -type f | sort | sed -n '1,120p'`
- `ls -1 runs | tail -n 5`
- `sed -n '1,220p' runs/<latest_run>/run_metadata.json`
- `find runs/<latest_run> -maxdepth 3 -type f | sort`

## What Was Defined Now
- Delivery surface зафиксирован как отдельный packaging layer поверх frozen truth-bearing baselines.
- Введена нормализованная модель concepts:
  - `report_scope`
  - `delivery_profile`
  - `guide_scope`
  - `guide_mode`
  - `output_format`
- Зафиксирован отдельный delivery root `deliveries/<delivery_id>/...`, а не extension текущего `runs/<run_id>/...`.
- Зафиксировано разделение source contexts:
  - variant-aware delivery идёт от successful run bundle;
  - general guide delivery не должна получаться blind-redaction из student-specific guide.
- Заморожено решение по v1 formats:
  - `pdf` — yes
  - `md` — yes
  - `bundle_dir` — yes
  - `docx` — not in first runtime slice

## Delivery Profile Summary
- `report_only`: только formal report surface для выбранного `report_scope`.
- `study_pack`: formal report + ровно один guide surface для того же topical scope.
- `guide_only`: только methodical surface без formal report.
- `print_pack`: report-centric print/archival directory bundle.

## Output Matrix Summary
- В `report_only` v1 нормализован вокруг `pdf`.
- В `guide_only` v1 нормализован вокруг `md`.
- Multi-artifact deliveries (`study_pack`, `print_pack`) в v1 должны выдаваться как `bundle_dir`, а не как single file.
- Variant-aware guide может включать реальные run-specific plots и schemes.
- General guide в frozen architecture допускается, но не имеет права включать run-specific plots; в v1 он ограничивается schemes + general explanatory surface.

## Remaining Open Questions
- Должен ли future general guide иметь отдельный dedicated content source file set или отдельный generator layer поверх frozen guide skeleton.
- Нужен ли позже zip-wrapper поверх `bundle_dir`, если базовый directory delivery окажется недостаточным для handoff.
- Должен ли future `docx` layer обслуживать только report-bearing profiles или позднее распространяться и на guide surface.

## Ready for F02B?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02B — Delivery Request Model + Bundle Skeleton`.
- В `F02B` ограничиться:
  - отдельным delivery request validation;
  - `deliveries/<delivery_id>/delivery_manifest.json`;
  - profile-aware layout skeleton;
  - минимальными assemblies для `report_only/pdf` и `guide_only/variant_aware/md`;
  - bundle-directory skeleton for `study_pack` and `print_pack`;
  - без `docx` и без runtime implementation of `guide_mode = general`.
