# Report U2 — Scenario-Driven One-Button Session Runtime

## Scope ID and Name
- Scope ID: `U2`
- Scope name: `Scenario-Driven One-Button Session Runtime`

## Objective
Заменить technical delivery prompt flow внутри unified `build --offer-delivery` session на frozen scenario-first operator layer, не меняя internal build/deliver semantics и не открывая новых delivery features.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_U1_ux_audit.md`
- `docs/UX_ONE_BUTTON_PLAN.md`
- `docs/UX_ONE_BUTTON_CONTRACT.md`
- `docs/UX_SCENARIO_MATRIX.md`
- `README.md`
- current unified `build --offer-delivery` flow
- current delivery runtime and validation files

## Files Created
- `src/delivery_session_labels.py`
- `reports/report_U2_one_button_runtime.md`

## Files Updated
- `src/delivery_session.py`
- `src/delivery_report_docx.py`
- `src/delivery_guide_docx.py`
- `tests/test_unified_entrypoint.py`
- `tests/test_unified_entrypoint_docx.py`
- `tests/test_unified_entrypoint_guide_docx.py`
- `tests/test_delivery_report_docx_runtime.py`
- `tests/test_delivery_guide_docx_runtime.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- Unified post-build session now asks human scenarios instead of raw technical delivery fields.
- Visible scenarios are now:
  - `Ничего дополнительно`
  - `Только итоговый отчёт`
  - `Отчёт + материалы для подготовки`
  - `Только материалы для подготовки`
  - `Печатный комплект`
- Human follow-up questions now ask only:
  - personal vs general study materials;
  - human scope labels for guide-only;
  - `PDF` / `DOCX` / `Папка-комплект` / `Папка для печати`.
- Markdown is intentionally hidden from the default one-button session and remains available only through direct technical `deliver`.
- Unified session review summary is now human-readable and result-oriented.
- Success closeout now starts with `Что создано`, then local paths, then optional technical IDs.
- During U2 validation a genuine inconsistency was found and fixed narrowly: report/guide DOCX exporters now resolve output paths absolutely, so default repo-root deliveries no longer fail on relative DOCX targets.

## What The New One-Button Session Supports Now
- One operator-facing session after canonical build.
- Scenario-driven mapping to already existing runtime slices:
  - `Только итоговый отчёт` -> `report_only`
  - `Отчёт + материалы для подготовки` -> `study_pack`
  - `Только материалы для подготовки` -> `guide_only`
  - `Печатный комплект` -> `print_pack`
- Hidden internal mapping still preserves:
  - current delivery request model;
  - current source-run rules;
  - current supported format/profile matrix;
  - current truth-bearing boundaries.

## What Intentionally Remains Unchanged
- Internal `build` and `deliver` runtime layers were not redesigned.
- Direct technical `deliver` CLI still exposes advanced paths such as guide Markdown.
- No new delivery slice, no new format and no new bundle behavior were opened.
- JSON summary on stdout remains the existing machine-oriented CLI contract.

## Remaining Risks
- One-button session is now much simpler, but stdout still ends with the technical JSON summary because that CLI contract was not reopened in U2.
- `study_pack` and `print_pack` remain bundle-only operator results.
- DOCX and PDF exports still depend on local toolchains exactly as before:
  - guide PDF -> `pandoc + xelatex`
  - report DOCX / guide DOCX -> `pandoc`

## Ready for U3?
- `YES`

## Exact Recommendation for Next Step
- Open `U3 — Result Summary + Operator Help Closeout`.
- Keep it narrow: polish the final operator-facing closeout/help surface around the already implemented one-button session, without changing internal delivery semantics or opening new runtime features.
