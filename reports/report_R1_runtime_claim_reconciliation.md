# R1 — Runtime Claim Reconciliation

## Scope and Objective
Выполнить только docs/claim reconciliation после `A1` и `C1R`: синхронизировать `README.md` и `reports/master_report.md` с текущим runtime, не трогая code/runtime/tests и не возвращаясь преждевременно к feature work.

## Files Inspected
- `README.md`
- `reports/master_report.md`
- `reports/report_A1_cli_entrypoint_recovery.md`
- `reports/report_C1R_run_bound_reconcile.md`
- `reports/report_R0_recovery_stabilization_plan.md`

## Commands Run
- `rg -n "variant_aware|baseline|guide_only|study_pack|U5E|Current Post-closeout Scope|Latest Report Note|Next Recommended Stage|shell CLI|entrypoint" README.md reports/master_report.md reports/report_A1_cli_entrypoint_recovery.md reports/report_C1R_run_bound_reconcile.md reports/report_R0_recovery_stabilization_plan.md`
- `sed -n '1,320p' README.md`
- `sed -n '145,320p' reports/master_report.md`
- `sed -n '228,258p' README.md`
- `sed -n '330,392p' README.md`
- `sed -n '244,258p' reports/master_report.md`

## What Stale Claims Were Found
- В `README.md` оставалась ложная формулировка, что `guide_only/variant_aware` и `study_pack/variant_aware` работают только для run, совпадающего с текущим frozen baseline по `derived_parameters.json` и `out/data/*.json`. После `C1R` это уже неверно.
- В `README.md` phrasing для `guide_only/pdf` и `guide_only/docx` была слишком baseline-centered и не различала `variant_aware` и `general` источники.
- В `README.md` high-level scope line всё ещё говорила про delivery layer поверх `frozen guide baseline`, хотя текущий runtime уже разделяет run-bound `variant_aware` guide и explicit `general` source.
- В `master_report.md` post-closeout state всё ещё оставался на `R0`, а latest note всё ещё ссылалась на roadmap freeze вместо уже выполненного reconciliation.
- В `master_report.md` next recommended stage всё ещё не был сдвинут на `R2`.

## What Was Changed in README
- Заменён stale baseline-bound claim на truthful wording: `guide_only/variant_aware` и `study_pack/variant_aware` теперь описаны как run-bound через `source_run_id` и его successful run bundle.
- Уточнено, что `guide_only/pdf` и `guide_only/docx` строятся из того же guide source, что и соответствующий `guide_only/md`, без ложной привязки ко всему delivery surface как к frozen baseline.
- High-level scope line переведена с `frozen guide baseline` на более точное описание: delivery layer работает поверх already built runs, run-bound variant-aware guide и explicit general-guide source.

## What Was Changed in master_report
- Текущий post-closeout scope переведён с `R0` на `R1`, статус оставлен `Completed`.
- `Latest Report Path` обновлён на `reports/report_R1_runtime_claim_reconciliation.md`.
- `Latest Report Note` переписан narrowly: теперь он фиксирует docs-only reconciliation и explicitly отводит следующий шаг к `R2`, а не к feature work.
- В `Current Blockers` убран уже устаревший docs-drift bullet и заменён на всё ещё актуальный blocker про mixed handoff surface.
- `Next Recommended Stage` переведён с `R1` на `R2 — Test Baseline Integrity Recovery`.

## What Was Validated
- Проверено, что stale README phrase про baseline-bound `variant_aware` delivery удалена.
- Проверено, что `master_report.md` теперь указывает текущий scope как `R1`, latest report path как `report_R1_runtime_claim_reconciliation.md`, а next recommended stage как `R2`.
- Проверено, что этот pass ограничился только `README.md` и `reports/master_report.md` плюс новым scope report; code/runtime/tests не менялись.

## What Intentionally Remained Unchanged
- runtime/code/tests
- delivery semantics
- solver/report/guide truth
- historical reports, кроме текущего `master_report.md`
- mixed working tree / artifact hygiene
- stale broad-suite baseline assertions

## Remaining Risks
- Broad test suite всё ещё не является trustworthy gate: `tests/test_variant_integrity.py` остаётся stale.
- Handoff surface всё ещё смешивает intended sources с generated/runtime artifacts.
- Этот scope не проверял runtime заново; он только reconciled repo-level claims с уже зафиксированными фактами `A1` и `C1R`.

## Ready for R2? YES/NO
- `YES`

## Exact Next Recommendation
- Открыть `R2 — Test Baseline Integrity Recovery` и ограничить его только восстановлением честного broad regression signal без возврата к feature work.
