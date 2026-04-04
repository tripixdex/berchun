# Report F02B — Delivery Request Model + Bundle Skeleton

## Scope ID and Name
- Scope ID: `F02B`
- Scope name: `Delivery Request Model + Bundle Skeleton`

## Objective
Реализовать первый working delivery layer поверх frozen F02A architecture: отдельную delivery request model, `deliveries/<delivery_id>/...`, `delivery_manifest.json`, working runtime для `report_only/pdf` и `guide_only/variant_aware/md`, а также profile-aware skeleton layout для `study_pack` и `print_pack`.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/delivery/DELIVERY_SURFACE_PLAN.md`
- `docs/delivery/DELIVERY_SURFACE_CONTRACT.md`
- `docs/delivery/DELIVERY_OUTPUT_MATRIX.md`
- `README.md`
- `src/cli.py`
- `src/build_pipeline.py`
- `src/run_archive.py`
- `src/report_scope.py`
- current `runs/<run_id>/...` bundle layout
- current `docs/methodical/content/METHODICAL_GUIDE.md`
- current `inputs/derived_parameters.json`
- current `out/data/*.json`
- current `report/assets_manifest.json`
- current `out/artifacts/figure_manifest.json`

## Files Created
- `src/delivery_request.py`
- `src/delivery_assets.py`
- `src/delivery_runtime.py`
- `tests/_delivery_support.py`
- `tests/test_delivery_runtime.py`
- `tests/test_delivery_validation.py`
- `reports/report_F02B_delivery_runtime.md`

## Files Updated
- `src/cli.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- Введена отдельная `DeliveryRequest` model с явной validation логикой по frozen F02A matrix.
- Добавлен новый CLI path `python3 -m src.cli deliver ...` без смешения с truth-producing `build`.
- Введён отдельный delivery root `deliveries/<delivery_id>/...`.
- Добавлен `delivery_manifest.json` с полями:
  - `delivery_id`
  - `delivery_profile`
  - `output_format`
  - `report_scope` when present
  - `guide_scope` when present
  - `guide_mode` when present
  - `source_kind`
  - `source_run_id`
  - delivered `artifacts`
- Реализован populated runtime для:
  - `report_only` + `pdf`
  - `guide_only` + `variant_aware` + `md`
- Реализован skeleton-only layout для:
  - `study_pack` + `bundle_dir`
  - `print_pack` + `bundle_dir`
- Для `guide_only/variant_aware` добавлены:
  - filtering frozen guide baseline по `guide_scope`;
  - selection/copy правил для guide schemes и plots из selected successful run;
  - narrow guard against variant drift: selected run must match the frozen guide baseline artifacts.

## Supported Combinations Actually Working
- `report_only` + `pdf` + `report_scope = full|task1|task2`, если source run имеет тот же `report_scope`.
- `guide_only` + `variant_aware` + `md` + `guide_scope = full|task1|task2`, если source run compatible по scheme coverage и совпадает с текущим frozen guide baseline по `derived_parameters.json` и `out/data/*.json`.
- `study_pack` + `bundle_dir` + `guide_mode = variant_aware` как profile-aware skeleton bundle.
- `print_pack` + `bundle_dir` как profile-aware skeleton bundle.

## Unsupported Combinations Intentionally Rejected
- `output_format = docx`
- `guide_mode = general`
- variant-aware delivery без `source_run_id`
- `study_pack` с `guide_scope != report_scope`
- report-bearing delivery, если `source_run.report_scope` не совпадает с requested `report_scope`
- `guide_only/full` от partial run, где нет полного набора scheme assets

## What Intentionally Remained Unchanged
- Solver mathematics и solver outputs не менялись.
- Formal report build surface не менялась.
- Frozen methodical guide content не переписывался; delivery layer только фильтрует уже существующий markdown по scope.
- `study_pack` и `print_pack` не были расширены до full rich population.
- `docx` и runtime `guide_mode = general` не открывались.

## Remaining Risks
- `guide_only/variant_aware` в F02B узко привязан к frozen guide baseline и поэтому пока не является general per-run guide generator.
- `study_pack` и `print_pack` пока skeleton-only; rich bundle population остаётся на `F02C`.
- Repo-wide `python3 -m unittest discover -s tests -v` по-прежнему падает на двух historical `tests/test_variant_integrity.py` ожиданиях (`journal_number = 10`, `Tc = 20`), которые не совпадают с текущим committed working set (`journal_number = 4`, `Tc = 14`). F02B их не менял.
- `src/delivery_runtime.py` после inspection оставлен на `156` строках: файл выше soft target, но ниже hard limit и покрывает одну узкую cohesive responsibility без необходимости искусственного дальнейшего split в этом pass.

## Ready for F02C?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02C — Bundle Profiles + General Guide Surface`.
- В `F02C` ограничиться:
  - rich population rules для `study_pack` и `print_pack`;
  - explicit runtime path для `guide_mode = general`;
  - include/copy policy для report assets, guide schemes и guide plots внутри bundle profiles;
  - без `docx` и без reopening solver/report/methodical truth.
