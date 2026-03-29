# Report F02F — Delivery-local Manifest Normalization

## Scope ID and Name
- Scope ID: `F02F`
- Scope name: `Delivery-local Manifest Normalization`

## Objective
Сделать copied manifests внутри delivery bundles self-contained: убрать run-backed path leakage для реально упакованных report artifacts и переписать ссылки на delivery-local paths без изменения solver/report/methodical truth.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_F02B_delivery_runtime.md`
- `reports/report_F02C1_bundle_population.md`
- `reports/report_F02C2_general_guide.md`
- `reports/report_F02C3_regime_safety.md`
- `reports/report_F02E_unified_entrypoint.md`
- `README.md`
- `src/delivery_population.py`
- `src/delivery_runtime.py`
- `src/delivery_assets.py`
- current `deliveries/<delivery_id>/...` layout
- current copied `report/assets_manifest.json` inside delivery bundles

## Files Created
- `src/delivery_manifest_normalization.py`
- `tests/test_delivery_manifest_normalization.py`
- `reports/report_F02F_manifest_normalization.md`

## Files Updated
- `src/delivery_population.py`
- `tests/test_delivery_runtime.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- Добавлен узкий helper `normalize_report_assets_manifest(...)` для copied `report/assets_manifest.json` внутри delivery bundles.
- Normalizer не пересчитывает report truth и не создаёт новые artifacts; он только приводит manifest к delivery-local subset.
- Для report-bearing bundles normalizer теперь:
  - переписывает `report_pdf_path` на `report/final_report.pdf`;
  - переписывает `report_source_file` на `report/final_report.tex`, если этот файл реально входит в bundle;
  - фильтрует `figure_inputs_used` до реально включённых `figures/...`;
  - фильтрует `additional_artifacts_used` и `title_assets_used` до реально включённых `report/assets/...`;
  - очищает неупакованные external references: `variant_source_file`, `derived_source_file`, `data_inputs_used`;
  - помечает normalized copy через `meta.delivery_local_paths = true`.
- `delivery_population.py` теперь вызывает normalizer после сборки `report_only`, `study_pack` и `print_pack`.

## Which Manifests Are Normalized Now
- `report/assets_manifest.json` внутри:
  - `report_only`
  - `study_pack`
  - `print_pack`
- `delivery_manifest.json` intentionally не менялся: он уже использует delivery-local relative artifact list.
- Для `guide_only` отдельный copied report manifest отсутствует, поэтому F02F туда ничего не добавлял.

## Validation Actually Run
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_runtime tests.test_delivery_general_runtime tests.test_delivery_manifest_normalization tests.test_delivery_validation tests.test_delivery_safety -v`
- real smoke:
  - `python3 -B -m src.cli deliver --delivery-profile report_only --output-format pdf --report-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02f_smoke_report`
  - `python3 -B -m src.cli deliver --delivery-profile study_pack --output-format bundle_dir --report-scope full --guide-mode general --guide-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02f_smoke_study`
  - `python3 -B -m src.cli deliver --delivery-profile print_pack --output-format bundle_dir --report-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02f_smoke_print`
- targeted validator confirmed for all three smoke bundles:
  - normalized report manifests no longer contain `runs/...` artifact paths;
  - all normalized manifest references are relative, delivery-local, and exist inside the delivery root.

## What Intentionally Remained Unchanged
- Solver mathematics и source solver outputs не менялись.
- Formal report build semantics не менялись.
- Frozen methodical guide content и guide delivery logic не менялись.
- Новый guide-level manifest не вводился.
- `docx` и иные output-format expansions не открывались.
- Unified session/UX не менялся.

## Remaining Risks
- F02F нормализует только copied `report/assets_manifest.json`; отдельного guide-assets manifest в v1 по-прежнему нет.
- `guide_only` bundles остаются без дополнительного secondary manifest beyond `delivery_manifest.json`; это сознательно оставлено вне F02F.
- Repo-wide `tests/test_variant_integrity.py` всё ещё содержит historical hardcoded expectations против текущего committed working set; F02F их не трогал.

## Ready for F02G?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02G — Output Format Expansion Freeze`.
- Ограничить его только freeze/contract pass для следующего output-format slice поверх уже self-contained bundles: решить, какие дополнительные delivery formats действительно нужны после `pdf/md/bundle_dir`, без reopening solver/report/methodical truth и без UX redesign.
