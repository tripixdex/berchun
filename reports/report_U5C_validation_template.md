# Report: U5C — Validation Error Assist + Starter YAML Template

## Objective
Improve the default operator flow when YAML validation fails and add a simple starter YAML template path inside the same CLI experience, without changing build/delivery semantics.

## Files Created
- `reports/report_U5C_validation_template.md`

## Files Updated
- `src/cli.py`
- `src/cli_surface.py`
- `src/input_surface.py`
- `tests/test_cli_operator_surface.py`
- `README.md`
- `reports/master_report.md`

## What Validation-Error Help Was Improved
- Build-input validation failures now report the wrong field in human terms instead of raw schema wording.
- The error surface now explains the expected format briefly and suggests the next action.
- Common input issues such as bad `journal_number`, malformed `birth_date`, and missing required text fields now map to short operator-friendly guidance.

## What Starter-Template Path Was Added
- Added a starter YAML creation path inside the same CLI using `build --starter-yaml`.
- The path can save directly to a chosen file or accept the default `inputs/starter.yaml`.
- The generated template includes the fields a new operator needs to start safely:
  - student full name
  - student group
  - teacher full name
  - journal number
  - birth date
  - report scope
  - report year

## How the Validation-Failure Path Was Demonstrated
- A realistic invalid YAML was run with a bad `journal_number` value.
- The CLI returned a human-readable error block that named the field, explained the expected format, and pointed to the starter YAML path.
- The failure stayed in the normal operator flow: no raw schema dump was required.

## How the Full Happy-Path Pack Was Regenerated
- A fresh happy-path run was executed from a newly created starter YAML file.
- The operator then ran the normal build flow and selected the standard study-pack delivery path.
- The resulting visible pack was saved in the repo-local deliveries tree at:
  - `deliveries/20260331T185448527145Z__study_pack__full`
- The main artifact to open first is the final report PDF inside that bundle.

## What Intentionally Remained Unchanged
- build semantics
- delivery semantics
- solver truth
- report truth
- methodical guide truth
- delivery matrix and supported outputs
- quiet default operator style from U5A
- YAML discoverability assist from U5B

## Remaining Risks
- The starter YAML path is intentionally narrow and still expects the operator to edit values manually in the file.
- Validation help is now clearer, but it is still a guided CLI workflow rather than a full interactive YAML editor.
- The new starter flow does not change the underlying canonical schema or the delivery model.

## Ready for U5D? YES/NO
- `YES`

## Exact Recommendation for Next Step
- Open `U5D — Guided Input Recovery Loop`.
- Keep it narrow: improve retry and recovery wording after validation failures and add only a tiny guided re-edit shortcut if it is truly needed, without changing build/delivery semantics or opening a broad CLI redesign.
