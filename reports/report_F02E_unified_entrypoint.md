# Report F02E — Unified Delivery Entrypoint

## Scope ID and Name
- Scope ID: `F02E`
- Scope name: `Unified Delivery Entrypoint`

## Objective
Дать оператору один session-layer поверх уже существующих `build` и `deliver`, чтобы после подтверждения raw input и успешного `build` можно было в той же сессии выбрать optional delivery outputs без reopening solver/report/methodical truth.

## Trusted Inputs Used
- `reports/master_report.md`
- `README.md`
- current build interactive flow
- current deliver runtime flow
- `reports/report_Feature_01_scope_input.md`
- `reports/report_F02B_delivery_runtime.md`
- `reports/report_F02C1_bundle_population.md`
- `reports/report_F02C2_general_guide.md`
- `reports/report_F02C3_regime_safety.md`
- current CLI files
- current input/build/delivery models

## Files Created
- `src/delivery_session.py`
- `tests/test_unified_entrypoint.py`
- `reports/report_F02E_unified_entrypoint.md`

## Files Updated
- `src/cli.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- В `build` добавлен opt-in flag `--offer-delivery`.
- После успешного `run_build` unified session может открыть отдельный post-build delivery prompt в той же operator session.
- Prompt reuse-ит существующие `build_delivery_request` и `run_delivery`; новый truth-producing path не вводился.
- Unified session поддерживает review step для delivery request с обязательными `confirm / edit / cancel`.
- Output `build` без `--offer-delivery` оставлен прежним; combined session summary включается только при явном opt-in.

## What Unified Interactive Flow Supports Now
- `build -> none`: оператор завершает build без дополнительного delivery.
- `build -> report_only`.
- `build -> study_pack`.
- `build -> guide_only`.
- `build -> print_pack`.
- Для guide-bearing profiles session позволяет выбирать:
  - `guide_mode = variant_aware | general`
  - `guide_scope` только из реально допустимых значений текущего runtime slice.
- Для report-bearing profiles session показывает только `report_scope`, совместимый с только что собранным run.
- `output_format` в session выбирается только из реально поддерживаемых значений текущего v1 slice: `pdf`, `md`, `bundle_dir`.

## What Intentionally Remains Unsupported
- `docx`
- redesign внутренней delivery model
- новый truth-producing path поверх `build`
- unified flow, который скрыто меняет solver/report/methodical semantics
- delivery-local manifest rewriting

## Validation Actually Run
- `python3 -m py_compile src/cli.py src/delivery_session.py tests/test_unified_entrypoint.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_input_validation tests.test_build_pipeline tests.test_unified_entrypoint tests.test_delivery_runtime tests.test_delivery_general_runtime tests.test_delivery_validation tests.test_delivery_safety -v`
- real smoke: `build --input ... --review --offer-delivery` with `none`
- real smoke: `build --input ... --review --offer-delivery` with `guide_only + general + task1`

Validation facts from executed checks:
- existing build input/review tests остались зелёными;
- unified session покрыта на `skip`, `report_only`, `guide_only`, `edit`, `cancel`, invalid interactive choice blocking;
- delivery-focused suites `F02B/F02C1/F02C2/F02C3` остались зелёными поверх нового session-layer;
- real CLI smoke подтвердил combined summary для `build -> none` и `build -> guide_only/general`.

## Remaining Risks
- `src/cli.py` после `F02E` остаётся выше soft size target (`173` lines), но ниже hard limit; delivery prompt вынесен в отдельный `src/delivery_session.py`, так что дополнительный split в этом narrow pass не понадобился.
- Unified session пока intentionally CLI-only и не открывает новый multi-step UI contract beyond terminal prompts.
- Copied `report/assets_manifest.json` внутри delivery bundles всё ещё сохраняет run-backed paths; `F02E` это не открывал.

## Ready for Next Scope?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02F — Delivery-local Manifest Normalization`.
- Ограничить его только переписыванием copied manifest paths внутри delivery bundles на delivery-local self-contained references без `docx`, без solver/report/methodical redesign и без нового export architecture pass.
