# Report U1 — Operator UX Audit + One-Button Contract Freeze

## Scope ID and Name
- Scope ID: `U1`
- Scope name: `Operator UX Audit + One-Button Contract Freeze`

## Objective
Честно проверить текущий operator-facing UX и заморозить новый one-button contract, который уменьшает cognitive load без изменения already implemented runtime semantics.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_Z1_delivery_freeze_review.md`
- `README.md`
- current CLI/operator-facing flows
- current unified `build --offer-delivery` behavior
- `docs/DELIVERY_SURFACE_CONTRACT.md`
- `docs/DELIVERY_OUTPUT_MATRIX.md`
- `docs/OUTPUT_FORMAT_CONTRACT.md`
- `src/cli.py`
- `src/delivery_session.py`
- `src/delivery_request.py`

## Files Created
- `docs/UX_ONE_BUTTON_PLAN.md`
- `docs/UX_ONE_BUTTON_CONTRACT.md`
- `docs/UX_SCENARIO_MATRIX.md`
- `reports/report_U1_ux_audit.md`

## Files Updated
- `reports/master_report.md`

## Main UX Problems Found
- Current operator path leaks internal runtime vocabulary directly into prompts: `delivery_profile`, `guide_mode`, `guide_scope`, `output_format`.
- Unified session is correct semantically, but the operator still has to translate a human goal into an internal delivery matrix.
- Current operator help is accurate but too dense; a confused operator does not get a short scenario-first path.
- Scope logic is technically valid, but externally it feels like repeated technical selection rather than one obvious business decision.
- Final success surface is still too technical: IDs and manifests compete with the simple answer to “what was produced?”.

## New One-Button Contract Summary
- Freeze one recommended operator session instead of teaching the operator separate `build` and `deliver` mental models.
- Keep `build` and `deliver` separate internally, but translate them externally into a single scenario-driven flow.
- Hide raw internal enums and show only human scenarios, human material types and human format labels.
- Keep Markdown available for technical/direct CLI use, but remove it from the standard one-button operator flow.
- Show final outputs as human-labeled results first, with technical IDs only as secondary detail.

## Scenario-Matrix Summary
- `Только итоговый отчёт`
- `Отчёт + материалы для подготовки` with two visible variants:
  - `персональные`
  - `общие`
- `Только материалы для подготовки` with two visible variants:
  - `персональные`
  - `общие`
- `Печатный комплект`

Each visible scenario now has a frozen deterministic mapping to the already implemented delivery runtime, while internal constraints like `guide_scope = report_scope` remain hidden from the operator.

## Remaining Open Questions
- Whether the future one-button session should become the new default recommended command name or remain a guided layer over `build --offer-delivery`.
- Whether Markdown should stay fully hidden in the default session or appear only behind an explicit advanced toggle.
- How compact the final result summary should be before technical IDs move into a separate detail block.

## Ready for U2?
- `YES`

## Exact Recommendation for Next Step
- Open `U2 — Scenario-Driven One-Button Session Runtime`.
- Keep it narrow: replace technical delivery prompts with scenario-first selection, human material labels, human format labels and result-first closeout summary, without changing internal build/deliver semantics or opening new delivery features.
