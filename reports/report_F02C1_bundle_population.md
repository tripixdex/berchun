# Report F02C1 — Bundle Profiles Rich Population

## Scope ID and Name
- Scope ID: `F02C1`
- Scope name: `Bundle Profiles Rich Population`

## Objective
Расширить frozen delivery runtime так, чтобы `study_pack` и `print_pack` перестали быть skeleton-only roots и начали реально упаковывать уже существующие frozen report/methodical surfaces из successful run bundles.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/delivery/DELIVERY_SURFACE_PLAN.md`
- `docs/delivery/DELIVERY_SURFACE_CONTRACT.md`
- `docs/delivery/DELIVERY_OUTPUT_MATRIX.md`
- `reports/report_F02B_delivery_runtime.md`
- `README.md`
- `src/delivery_request.py`
- `src/delivery_assets.py`
- `src/delivery_runtime.py`
- `src/cli.py`
- current `runs/<run_id>/...` bundle layout
- current `docs/methodical/content/METHODICAL_GUIDE.md`
- current `report/assets_manifest.json`
- current `out/artifacts/figure_manifest.json`

## Files Created
- `src/delivery_population.py`
- `reports/report_F02C1_bundle_population.md`

## Files Updated
- `src/delivery_request.py`
- `src/delivery_assets.py`
- `src/delivery_runtime.py`
- `tests/_delivery_support.py`
- `tests/test_delivery_runtime.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- `study_pack` переведён из skeleton-only в populated bundle для `guide_mode = variant_aware`.
- `print_pack` переведён из skeleton-only в populated report-centric bundle.
- Assembly logic вынесена из `src/delivery_runtime.py` в отдельный `src/delivery_population.py`, чтобы runtime orchestration остался компактным.
- Добавлены явные selectors для:
  - guide schemes;
  - guide plots;
  - report assets;
  - report figures по выбранному `report_scope`.
- Существующие F02B guards сохранены:
  - `source_run_id` обязателен;
  - `docx` запрещён;
  - `guide_mode = general` запрещён;
  - `study_pack` требует `guide_scope = report_scope`;
  - delivery не пересчитывает solver truth.

## What `study_pack` Contains Now
- `delivery_manifest.json`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `guide/methodical_guide__variant.md`
- `guide/assets/schemes/...` для выбранного `guide_scope`
- `guide/assets/plots/...` для выбранного `guide_scope`

## What `print_pack` Contains Now
- `delivery_manifest.json`
- `report/final_report.pdf`
- `report/final_report.tex`
- `report/assets_manifest.json`
- `report/assets/...`:
  - title asset;
  - scheme assets для выбранного `report_scope`
- `figures/...`:
  - только plot PNG files, реально используемые report surface выбранного `report_scope`

## What Intentionally Remains Unsupported
- `guide_mode = general`
- regime-aware guide safety logic
- `docx`
- guide surface внутри `print_pack`
- manifest remapping from source-run paths to delivery-local paths

## Remaining Risks
- Variant-aware guide packaging по-прежнему intentionally привязан к frozen guide baseline artifacts и не является arbitrary per-run guide generator.
- Скопированный `report/assets_manifest.json` сохраняет исходные run-backed paths; F02C1 не переоткрывал отдельный scope на local-path rewriting.
- Repo-wide `tests/test_variant_integrity.py` всё ещё содержит historical hardcoded expectations против текущего committed working set; F02C1 их не трогал.

## Ready for F02C2?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02C2 — General Guide Surface Runtime`.
- Ограничить его только runtime support для `guide_mode = general` в `guide_only` и `study_pack` с scheme-only asset policy.
- Не открывать `docx`, regime-aware guide safety logic и не переоткрывать solver/report/methodical truth.
