# R0 — Recovery Stabilization Roadmap Freeze

## Scope and Objective
Заморозить короткий stabilization roadmap после emergency audit, `A1` и `C1R`, не открывая implementation. Цель этого scope: честно зафиксировать, какие recovery/hardening шаги ещё обязательны до возврата к feature work, какие костыли и долги надо встроить в roadmap как отдельные corrective scopes, и по каким критериям репозиторий снова можно считать controlled, trustworthy и operator-safe.

## Files Inspected
- `README.md`
- `reports/master_report.md`
- `reports/report_AUDIT_emergency_repo_recovery.md`
- `reports/report_A1_cli_entrypoint_recovery.md`
- `reports/report_C1R_run_bound_reconcile.md`
- `reports/report_V3C_reconciliation.md`
- `tests/test_variant_integrity.py`
- repo-level claim/runtime references via search in `reports/`, `docs/`, `src/`, `tests/`

## Commands Run
- `git status --short`
- `sed -n '1,260p' README.md`
- `sed -n '1,320p' reports/master_report.md`
- `find reports -maxdepth 1 -type f | sort | rg 'AUDIT|A1|C1R|U5E|R0|C1'`
- `sed -n '1,260p' reports/report_AUDIT_emergency_repo_recovery.md`
- `rg -n "A1|C1R|U5E|variant-aware|CLI entrypoint|stale|hardcoded|baseline|debt|blocker" reports docs README.md src tests`
- `sed -n '1,260p' reports/report_A1_cli_entrypoint_recovery.md`
- `sed -n '1,320p' reports/report_C1R_run_bound_reconcile.md`
- `sed -n '1,220p' tests/test_variant_integrity.py`
- `sed -n '1,220p' reports/master_report.md`
- `sed -n '220,360p' reports/master_report.md`
- `sed -n '1,260p' reports/report_V3C_reconciliation.md`

## Current Recovery State Summary
- `A1` закрыл реальный shell-entrypoint blocker: `python3 -m src.cli ...` снова обязан проходить через реальные argv, а не падать в operator loop.
- `C1R` снял hidden baseline coupling из `variant_aware` guide delivery и вернул run-bound behavior для non-example runs.
- На этом recovery не завершён:
  - repo-level docs и текущий `master_report` частично противоречат уже исправленному runtime;
  - broad regression signal по-прежнему нельзя считать trustworthy из-за stale historical assertions;
  - working tree и handoff surface остаются смешанными: source, generated truth, deliveries, junk и incidental clutter лежат без явного engineering boundary.
- Вывод: после `A1` и `C1R` репозиторий уже не в emergency-blocked state, но ещё не в controlled engineering state.

## Remaining Blockers Before Safe Feature Work
- `HIGH`: `README.md` всё ещё содержит stale claim, что `guide_only/variant_aware` и `study_pack/variant_aware` требуют совпадения с frozen baseline artifacts. После `C1R` это уже неправда.
- `HIGH`: `reports/master_report.md` одновременно фиксирует `C1R` как completed corrective pass и всё ещё держит stale residual-risk bullet про baseline-bound `variant_aware` delivery, а также преждевременно указывает на возврат к `U5E`.
- `HIGH`: broad `python3 -m unittest discover -s tests -v` нельзя считать green gate, пока `tests/test_variant_integrity.py` содержит hardcoded historical expectations (`journal_number = 10`, `Tc = 20`) против текущего working set.
- `MEDIUM`: working tree/handoff surface смешивает контролируемые runtime/doc changes с generated artifacts, `deliveries/`, `.DS_Store`, `__pycache__` и accidental leftovers; это мешает понимать, что является intended source of truth.
- `MEDIUM`: feature branch нельзя безопасно продолжать, пока не зафиксирован честный supported operator surface после `A1/C1R` и не отделены recovery scopes от новых delivery/UX features.

## Explicit Recovery Roadmap
### R1 — Runtime Claim Reconciliation
- Цель: привести `README.md`, `reports/master_report.md` и текущие repo-level claims в соответствие с фактическим runtime после `A1` и `C1R`.
- В scope:
  - убрать stale baseline-bound wording для `variant_aware`;
  - привести `next recommended stage` к recovery reality, а не к преждевременному `U5E`;
  - зафиксировать supported operator/delivery surface без overclaim.
- Вне scope:
  - runtime/code changes;
  - новые delivery features;
  - массовая rewrite docs.
- Exit gate:
  - repo-level docs больше не противоречат `A1/C1R`;
  - supported behavior описан один раз и без конфликтующих формулировок.

### R2 — Test Baseline Integrity Recovery
- Цель: вернуть честный, engineering-usable regression signal.
- В scope:
  - исправить или перевести в явный historical status stale tests, прежде всего `tests/test_variant_integrity.py`;
  - проверить brittle text-needle assertions, если они привязаны к obsolete surface;
  - отделить truly supported behavior tests от historical snapshot checks.
- Вне scope:
  - новые runtime features;
  - semantic redesign tests;
  - массовое переписывание test strategy.
- Exit gate:
  - broad suite либо зелёная на поддерживаемом поведении, либо все intentionally historical checks явно выведены из broad gate с письменным justification;
  - test failures больше не объясняются stale baseline literals.

### R3 — Working Tree / Artifact Surface Stabilization
- Цель: вернуть handoff-поверхность в контролируемое инженерное состояние.
- В scope:
  - отделить intended committed sources от generated artifacts и incidental clutter;
  - классифицировать, что должно оставаться в repo как canonical truth, а что является runtime byproduct;
  - убрать accidental leftovers, которые мешают auditability.
- Вне scope:
  - feature redesign;
  - broad repo cleanup "на всякий случай";
  - изменение solver/report/delivery semantics.
- Exit gate:
  - working tree и handoff surface больше не смешивают runtime byproducts, junk и source-of-truth;
  - оператор и ревьюер могут понять, какие файлы являются canonical, а какие generated/runtime.

### R4 — Recovery Freeze Review Before Feature Resume
- Цель: после `R1–R3` провести короткий re-audit и решить, можно ли безопасно возвращаться к `U5E` и остальному feature work.
- В scope:
  - проверка, что CLI entrypoint, run-bound guide delivery, docs, tests и repo surface больше не конфликтуют;
  - подтверждение, что unified CLI direction остаётся достижимой без mixed-state debt underneath.
- Вне scope:
  - реализация `U5E`;
  - новые output formats;
  - platform/bot/payment work.
- Exit gate:
  - recovery scope formally closed;
  - repo снова trustworthy enough для возобновления feature work.

## Engineering Debt to Embed Into the Roadmap
- Stale README contract для `variant_aware` delivery после `C1R`.
- Stale `master_report` residual-risk wording и преждевременный pointer на `U5E`.
- `tests/test_variant_integrity.py` как hardcoded historical test, который продолжает ломать broad suite.
- Вероятная группа brittle tests, завязанных на obsolete formatting/surface assumptions, если они ещё живут рядом с current supported runtime.
- Mixed working tree surface:
  - generated `out/data`, `figures`, `report`, `runs/index.json`;
  - `deliveries/` как runtime byproduct на repo surface;
  - `.DS_Store`;
  - `__pycache__`;
  - accidental deleted leftovers.
- Residual trust problem: repo claims, tests и actual runtime всё ещё не сведены в одну честную engineering story.

## Exit Criteria for “Repo Back in Controlled State”
- `A1` и `C1R` остаются подтверждёнными, и ни один repo-level doc больше не спорит с этими фактами.
- Broad regression signal снова пригоден как engineering gate, а не ломается на stale baseline expectations.
- Supported operator surface описан честно и без внутренне противоречивых оговорок.
- Working tree/handoff surface больше не захламлена runtime byproducts и accidental junk настолько, чтобы мешать пониманию canonical truth.
- Recovery roadmap закрыт formal review verdict-ом, после которого feature work можно открывать без наложения на mixed repo state.

## What Intentionally Remains Outside Recovery and Belongs to Later Feature Work
- `U5E — Bundle DOCX UX`
- любые новые delivery features и output-format expansions
- DOCX/general bundle enrichment beyond current supported surface
- новые report/guide style passes
- platform/bot/payment/admin направления
- solver/report mathematics changes

## Exact Next Recommendation
- Открыть `R1 — Runtime Claim Reconciliation` как следующий narrow corrective scope.
- Не возвращаться к `U5E` и остальному feature work до закрытия как минимум `R1`, `R2`, `R3` и затем короткого `R4` freeze review.
