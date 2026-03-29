# Scope Report

## Scope ID and Name
- `V2 — Universal Variant Safety + Prose Condition Audit`

## Objective
- Проверить, остаются ли solver/report outputs математически согласованными на более широкой variant-матрице, и отделить universally safe teacher-facing фразы от тех, которые зависят от варианта и требуют смягчения.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_Feature_01_scope_input.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `src/render/task1_reflow_11_12.py`
- `src/render/task1_reflow_13_14.py`
- `src/render/task2_reflow.py`
- `src/render/section_flow.py`
- `src/cli.py`
- `src/build_pipeline.py`
- `src/input_schema.py`
- `src/variant.py`
- `tests/test_build_pipeline.py`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`

## Files Created
- `reports/report_V2_variant_safety.md`
- `out/audit/variant_safety_checks.json`

## Files Updated
- `reports/master_report.md`

## Variant Matrix Used
- `F01` `full`: `journal_number = 1`, `birth_date = 01.01.2000`
- `F02` `full`: `journal_number = 1`, `birth_date = 31.12.2000`
- `F03` `full`: `journal_number = 30`, `birth_date = 01.01.2000`
- `F04` `full`: `journal_number = 30`, `birth_date = 31.12.2000`
- `F05` `full`: `journal_number = 15`, `birth_date = 15.06.2000`
- `F06` `full`: `journal_number = 8`, `birth_date = 29.02.2000`
- `F07` `full`: `journal_number = 22`, `birth_date = 10.09.2000`
- `F08` `full`: `journal_number = 12`, `birth_date = 28.02.2001`
- `F09` `full`: `journal_number = 25`, `birth_date = 20.11.2000`
- `F10` `full`: `journal_number = 5`, `birth_date = 17.04.2000`
- `T11` `task1`: `journal_number = 30`, `birth_date = 01.01.2000`
- `T12` `task1`: `journal_number = 1`, `birth_date = 31.12.2000`
- `T13` `task1`: `journal_number = 18`, `birth_date = 07.03.2000`
- `T14` `task2`: `journal_number = 30`, `birth_date = 01.01.2000`
- `T15` `task2`: `journal_number = 1`, `birth_date = 31.12.2000`
- `T16` `task2`: `journal_number = 8`, `birth_date = 29.02.2000`
- `T17` `task2`: `journal_number = 18`, `birth_date = 07.03.2000`

Matrix coverage:
- `17` build cases total.
- `11` unique `(journal_number, birth_date)` variants.
- Low / mid / high `journal_number`.
- Months `1`, `2`, `3`, `4`, `6`, `9`, `11`, `12`.
- `1.3` first stationary point from `2` to `7`.
- Heavy-looking `1.4` and `2.1` cases explicitly included.
- `full`, `task1`, `task2` scopes all sampled.

## Commands Actually Run
- `rg -n "заметно влияет|раст[её]т уже слабо|наибольший выигрыш|новый ресурс|почти не созда[её]т|становится длиннее|..." src/render report/final_report.tex`
- `sed -n ...` over `reports/master_report.md`, `reports/report_Feature_01_scope_input.md`, `report/final_report.tex`, `src/render/*.py`, `src/cli.py`, `src/build_pipeline.py`, `src/input_schema.py`, `src/variant.py`, `tests/test_build_pipeline.py`
- `nl -ba src/render/task1_reflow_11_12.py | sed -n '1,180p'`
- `nl -ba src/render/task1_reflow_13_14.py | sed -n '1,180p'`
- `nl -ba src/render/task2_reflow.py | sed -n '1,180p'`
- local probe: `python3 - <<'PY' ... PY` for targeted `task2` month-1 traceback confirmation
- local audit harness: `python3 - <<'PY' ... PY` that executed the `17` isolated `build` cases and wrote `out/audit/variant_safety_checks.json`
- `python3 -m json.tool out/audit/variant_safety_checks.json >/dev/null`
- local `python3 - <<'PY' ... PY` summaries over the evidence artifact

## Variant-Dependent Prose Patterns Found
- `1.1`: `крайнее состояние S_n заметно влияет на итоговые метрики`
- `1.1`: `среднее число занятых операторов растёт уже слабо`
- `1.2`: `первые дополнительные места в очереди дают наибольший выигрыш по потерям`
- `1.2`: `расширение очереди почти не создаёт новый ресурс обслуживания`
- `1.2`: `очередь становится длиннее, но каждое отдельное место используется менее интенсивно`
- `1.3`: `почти каждая новая заявка попадает в ожидание`
- `1.4`: `заметно сокращает её хвост уже на умеренных значениях числа операторов`
- `2.1`: `дальнейший рост числа наладчиков влияет уже главным образом на резерв`
- `2.1`: `эта вероятность падает быстрее всего, а затем стремится к нулю уже без заметной очереди`

## Which Patterns Are Safe vs Risky
- `prose-safe`
- `1.1` `крайнее состояние S_n заметно влияет ...`: safe on the sampled region. На всех `11` уникальных вариантах точка `n = threshold - 1` сохраняла `P_отк >= 0.01`, а threshold-point уже переводила систему ниже целевого барьера.
- `1.1` `растёт уже слабо`: safe on the sampled region. При переходе от `n = threshold - 1` к `n = threshold + 1` прирост `M_зан` оставался в диапазоне `0.0135 .. 0.0572`.
- `1.2` `первые дополнительные места ...`: safe on the sampled region. Для всех sampled variants падение `P_отк` на переходе `m: 1 -> 5` было больше, чем на переходе `m: 5 -> 15`.
- `1.4` `заметно сокращает хвост ...`: safe on the sampled region. Для всех sampled variants `L_оч(n=8) < L_оч(n=5) < L_оч(n=1)`, а отношение `L_оч(8)/L_оч(5)` лежало в диапазоне `0.0018 .. 0.2103`.
- `2.1` `влияет главным образом на резерв`: numerically safe on the sampled region. На всех sampled variants `M_ож(r=20)` опускалось до `<= 0.0991`, а `M_зан(r=20)` уже почти совпадало с уровнем при `r = r_max`.
- `prose-risky`
- `1.2` `расширение очереди почти не создаёт новый ресурс обслуживания`: wording too strong for heavy variants. На sampled region прирост `M_зан` при `m: 1 -> 15` достигает `0.697`, так что без смягчения фраза выглядит чрезмерно категоричной.
- `1.2` `каждое отдельное место используется менее интенсивно`: not universal. На high-load variant `journal_number = 1`, `birth_date = 31.12.2000` занятость места очереди растёт с `0.335` до `0.783`, а не падает.
- `1.3` `почти каждая новая заявка попадает в ожидание`: not universal. По sampled variants `P_wait` в первой стационарной точке лежит в диапазоне `0.347 .. 0.909`; на `7` из `11` уникальных variants фраза уже слишком сильная.
- `2.1` `падает быстрее всего ... уже без заметной очереди`: not universal. На sampled max-load variant `journal_number = 1`, `birth_date = 31.12.2000` получено `P_ож(r=20) = 0.0629`, так что wording про “уже без заметной очереди” требует смягчения.

## Mathematical Safety Findings
- `solver-safe`
- На sampled region все boolean invariant-checks по `1.1`, `1.2`, `1.3`, `1.4`, `2.1` остались истинными.
- `1.1`: `P_отк(n)` не возрастает, threshold summary согласован с фактическими точками.
- `1.2`: семейства по `m` и по `n` сохраняют ожидаемую монотонность по ключевым метрикам.
- `1.3`: `first_stationary = floor(a) + 1`, нестационарный префикс отделён корректно, стационарные значения конечны и неотрицательны.
- `1.4`: метрики конечны и неотрицательны, truncation bounds не вышли за agreed precision policy.
- `2.1`: `waiting_probability` и `waiting_machines_expected` по sampled cases не возрастают при росте `r`; отрицательных или NaN-значений не обнаружено.
- `report / render risk, not solver risk`
- `6 / 17` build cases завершились падением teacher-facing report layer, хотя `figure_manifest.json` и solver JSON outputs были уже выпущены.
- Все `6` падений пришлись на cases с `birth_month in {1, 2}` и совпали с `max_repairers < 33`.
- Прямая причина: хардкод `r = 33` в [src/render/task2_reflow.py](/Users/vladgurov/Desktop/study/8sem/berchun/src/render/task2_reflow.py#L11) и [src/render/task2_reflow.py](/Users/vladgurov/Desktop/study/8sem/berchun/src/render/task2_reflow.py#L57), а не solver inconsistency.

## Remaining Uncertainty
- Это всё ещё representative audit, а не полный перебор пространства вариантов.
- `17` build cases cover more than F1, but not all `30 x 366` combinations.
- Prose classification опирается на sampled variants и на консервативные numerical checks для сильных qualitative statements; это достаточное evidence для risk triage, но не формальный proof over the full space.
- Because `task2` report rendering fails for `birth_month < 3`, the current audit cannot honestly claim universal report-layer safety until that hardcoded checkpoint is removed.

## Ready to Proceed to Feature-02?
- `NO`

## Exact Recommendation for Next Scope
- Открыть узкий corrective pass `V2A — Task 2 Variant Safety Fix + Prose Softening`.
- Scope `V2A` should do only two things:
- убрать variant-fragility в `2.1` reflow, заменив hardcoded `r = 33` на artifact-derived safe checkpoint selection;
- смягчить только те qualitative phrases, которые V2 classified as `prose-risky`, without changing solver truth, figure data, or report structure.
- `Feature-02 — DOCX/exportable editable version` не открывать до завершения этого corrective pass.
