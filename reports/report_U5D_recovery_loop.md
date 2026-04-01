# Report: U5D — Guided Input Recovery Loop

## Objective
Improve the operator recovery path after YAML/input validation failures so the user can continue more naturally inside the same calm CLI flow, without changing build or delivery semantics.

## Files Created
- `reports/report_U5D_recovery_loop.md`

## Files Updated
- `src/cli.py`
- `src/input_surface.py`
- `tests/test_cli_operator_surface.py`
- `README.md`
- `reports/master_report.md`

## What Recovery Wording Changed
- Validation failures now end with a short next-step line that explicitly says the operator can retry, choose another YAML, create a starter YAML, or cancel.
- The CLI help text now explains that validation failures offer retry / other YAML / starter YAML recovery.
- The README recovery note now matches the CLI surface instead of stopping at error explanation only.

## What Guided Shortcut Was Added
- Added a small recovery menu after validation failures.
- In file-based flows, `e` returns to the YAML chooser so the operator can pick a different input file without restarting the CLI.
- In both file-based and interactive flows, `s` opens the starter YAML creation path from the same session.
- `Enter` retries the current flow, and `x` cancels cleanly.

## How the Failure-Recovery Flow Was Demonstrated
- Ran a realistic invalid YAML with `journal_number: -1`.
- The CLI printed a human-readable error block, then offered recovery actions.
- Choosing `e` returned to the YAML chooser, selecting the example YAML and confirming review completed the build successfully in the same session.

## How the Full Happy-Path Pack Was Regenerated
- Ran a fresh happy-path `build --input inputs/examples/student_example.yaml --review --offer-delivery` flow.
- Kept the run workspace in a temporary directory and wrote the delivery output to the repo-local `deliveries/` tree.
- The resulting bundle is [deliveries/20260331T192043428342Z__study_pack__full](/Users/vladgurov/Desktop/study/8sem/berchun/deliveries/20260331T192043428342Z__study_pack__full).
- The main artifact to open first is [report/final_report.pdf](/Users/vladgurov/Desktop/study/8sem/berchun/deliveries/20260331T192043428342Z__study_pack__full/report/final_report.pdf).

## What Intentionally Remained Unchanged
- build semantics
- delivery semantics
- solver truth
- report truth
- methodical guide truth
- quiet default operator style from U5A
- YAML discoverability assist from U5B
- starter YAML creation path from U5C

## Remaining Risks
- Recovery is still narrow and terminal-native; it is not a full YAML editor.
- `e` recovery depends on the operator having a sensible alternative YAML candidate or manual correction path.
- The helper keeps the default flow calm, but it still assumes the operator is comfortable editing files outside the CLI when needed.

## Ready for U5E? YES/NO
- `YES`

## Exact Recommendation for Next Step
- Open `U5E — Bundle DOCX UX`.
- Keep it narrow: improve the bundle-oriented operator path only where it is still unnecessarily technical, without changing build/delivery semantics or the new validation recovery behavior.
