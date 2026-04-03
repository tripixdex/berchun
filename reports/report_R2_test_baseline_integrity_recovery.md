# R2 — Test Baseline Integrity Recovery

## Scope and Objective
Вернуть честный broad regression signal без изменения runtime semantics и без feature work: найти stale historical tests, минимально их отремонтировать или перевести в non-gating historical status, затем доказать, что broad suite снова пригодна как engineering gate.

## Files Inspected
- `tests/test_variant_integrity.py`
- `inputs/variant_me.yaml`
- `src/variant.py`
- `reports/master_report.md`
- repo-wide test references через search по `tests/`

## Commands Run
- `sed -n '1,240p' tests/test_variant_integrity.py`
- `rg -n "variant_me.yaml|journal_number\\)|task1\\.tc_seconds|machine_count|hardcoded|historical|baseline" tests`
- `python3 -m unittest tests.test_variant_integrity -v`
- `sed -n '1,220p' inputs/variant_me.yaml`
- `sed -n '1,260p' src/variant.py`
- `python3 - <<'PY' ... PY` для проверки текущих `load_variant(...)` и `derive_inputs(...)` значений
- `python3 -m unittest discover -s tests -v`
- `sed -n '145,320p' reports/master_report.md`
- `git status --short tests/test_variant_integrity.py reports/master_report.md README.md`

## What Stale/Brittle Tests Were Found
- `tests/test_variant_integrity.py::test_variant_file_is_parsed_correctly`
  - stale historical snapshot test;
  - жёстко ожидал `journal_number = 10`, `birth_day = 19`, `birth_month = 3`, хотя текущий committed `inputs/variant_me.yaml` уже давно `4 / 25 / 6`.
- `tests/test_variant_integrity.py::test_derived_parameters_match_confirmed_variant`
  - stale historical snapshot test;
  - жёстко ожидал `Tc = 20`, `Ts = 59`, `Tw = 103`, `machine_count = 33`, `Tc = 110`, `Ts = 44`, `repairers = 1..33`;
  - при этом сам runtime честно выводит текущие значения из текущего canonical input.
- Других broad-suite failures не найдено: полный `python3 -m unittest discover -s tests -v` до patch падал только на эти два assertion'а.

## What Was Changed
- В `tests/test_variant_integrity.py` удалены две stale snapshot-привязки к старому working set.
- `test_variant_file_is_parsed_correctly` переведён на truthful invariant:
  - читает текущий `inputs/variant_me.yaml`,
  - проверяет, что `load_variant(...)` корректно извлекает `journal_number`, `birth_day`, `birth_month` из текущего canonical payload,
  - проверяет canonical source tags.
- `test_derived_parameters_match_confirmed_variant` переведён на formula/invariant checks вместо historical literals:
  - `task1.tc_seconds = 10 + raw.journal_number`
  - `task1.ts_seconds = 40 + raw.birth_day`
  - `task1.tw_seconds = 100 + raw.birth_month`
  - `task2.machine_count = 30 + raw.birth_month`
  - `task2.tc_minutes = 100 + raw.journal_number`
  - `task2.ts_minutes = 25 + raw.birth_day`
  - `task_2_1.repairers = 1..max_repairers`
- Историзация в отдельный non-gating bucket не понадобилась: минимальный repair вернул тесту honest runtime alignment.

## What Was Validated
- `python3 -m unittest tests.test_variant_integrity -v` после patch: `3/3 OK`.
- `python3 -m unittest discover -s tests -v` после patch: `72 tests, OK`.
- Отдельно подтверждено через direct probe, что текущий committed working set действительно сейчас `journal_number = 4`, `birth_date = 25.06.2000`, а derived values `14 / 65 / 106 / 36 / 104 / 50`.
- Broad suite теперь снова является usable engineering gate на текущем supported runtime.

## What Intentionally Remained Unchanged
- runtime/code behavior
- solver/report/guide truth
- delivery semantics
- broader test architecture redesign
- repo surface / artifact hygiene
- docs, кроме `reports/master_report.md`

## Remaining Risks
- Handoff surface всё ещё смешивает intended sources и generated/runtime artifacts; это следующий stabilization blocker, но не test-baseline issue.
- Этот scope не перепроверял every possible hidden brittle assertion вручную; он доказал, что текущий broad gate снова зелёный на фактическом supported runtime.
- `inputs/variant_me.yaml` остаётся mutable working-set mirror, поэтому future tests снова не должны превращаться в snapshot literals без явного justification.

## Ready for R3? YES/NO
- `YES`

## Exact Next Recommendation
- Открыть `R3 — Working Tree / Artifact Surface Stabilization` и ограничить его только восстановлением controlled handoff surface без новых features и без runtime redesign.
