# Report F02C2 — General Guide Surface Runtime

## Scope ID and Name
- Scope ID: `F02C2`
- Scope name: `General Guide Surface Runtime`

## Objective
Добавить explicit runtime support для `guide_mode = general` в `guide_only` и `study_pack` без открытия `docx`, regime-aware guide safety logic и without solver/report/methodical redesign.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/DELIVERY_SURFACE_PLAN.md`
- `docs/DELIVERY_SURFACE_CONTRACT.md`
- `docs/DELIVERY_OUTPUT_MATRIX.md`
- `reports/report_F02B_delivery_runtime.md`
- `reports/report_F02C1_bundle_population.md`
- `docs/METHODICAL_GUIDE_PLAN.md`
- `docs/METHODICAL_GUIDE_CONTRACT.md`
- `docs/METHODICAL_GUIDE_SKELETON.md`
- `docs/METHODICAL_ARTIFACT_MAP.md`
- `docs/METHODICAL_GUIDE.md`
- current delivery runtime files
- current frozen report/methodical baselines

## Files Created
- `docs/METHODICAL_GUIDE_GENERAL_SOURCE.md`
- `tests/test_delivery_general_runtime.py`
- `reports/report_F02C2_general_guide.md`

## Files Updated
- `src/delivery_request.py`
- `src/delivery_population.py`
- `src/delivery_runtime.py`
- `src/cli.py`
- `tests/_delivery_support.py`
- `tests/test_delivery_validation.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- `guide_only + general + md` теперь поддерживается как отдельный runtime path.
- `study_pack + general + bundle_dir` теперь поддерживается как отдельный runtime path.
- `DeliveryRequest` больше не отвергает `guide_mode = general` по умолчанию; validation теперь различает run-backed и general-baseline cases.
- В `delivery_manifest.json` добавлен `guide_source_kind`, чтобы явно различать guide source context в combined deliveries.
- Existing F02B/F02C1 guards сохранены: `docx` запрещён, `guide_scope = report_scope` для `study_pack` сохранён, report-bearing bundles по-прежнему требуют compatible `source_run_id`.

## How General-guide Runtime Was Sourced
- General guide берётся не из blind redaction variant-aware guide.
- Для него введён отдельный explicit source file: `docs/METHODICAL_GUIDE_GENERAL_SOURCE.md`.
- Этот source:
  - не содержит student-specific чисел;
  - не содержит run-specific checkpoints;
  - повторяет frozen methodical skeleton;
  - фильтруется по `guide_scope` тем же deterministic path, что и variant-aware guide.
- Scheme assets для general guide берутся из текущего frozen `report/assets_manifest.json`.
- Plot assets для general guide не копируются вообще.

## What General-guide Deliveries Contain Now
- `guide_only + general + md`:
  - `delivery_manifest.json`
  - `guide/methodical_guide__general.md`
  - `guide/assets/schemes/...`
- `study_pack + general + bundle_dir`:
  - `delivery_manifest.json`
  - `report/final_report.pdf`
  - `report/assets_manifest.json`
  - `guide/methodical_guide__general.md`
  - `guide/assets/schemes/...`

## What Intentionally Remains Unsupported
- `docx`
- regime-aware guide safety logic
- run-specific plots inside `guide_mode = general`
- run-specific checkpoints inside `guide_mode = general`
- guide surface inside `print_pack`
- blind redaction of `docs/METHODICAL_GUIDE.md` into general guide

## Remaining Risks
- `docs/METHODICAL_GUIDE_GENERAL_SOURCE.md` является explicit baseline и может требовать отдельного content-polish pass, но это уже не runtime issue.
- Скопированный `report/assets_manifest.json` внутри report-bearing deliveries сохраняет исходные run-backed paths; F02C2 не открывал scope на manifest rewriting.
- Repo-wide `tests/test_variant_integrity.py` всё ещё содержит historical hardcoded expectations против текущего committed working set; F02C2 их не трогал.

## Ready for F02C3?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02C3 — Regime-Aware General Guide Safety Logic`.
- Ограничить его только safety rules для general guide around stationary/non-stationary interpretation и around which verbal claims are allowed without variant-specific checkpoints.
- Не открывать `docx`, export redesign и не переоткрывать solver/report/methodical truth.
