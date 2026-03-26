# Stage ID and name
STAGE 09A — Independent Math Lock Check

## Objective
Выполнить узкий независимый math-lock pass поверх уже committed solver outputs: выбрать компактный набор контрольных точек по всем пяти моделям, пересчитать их независимо от solver helpers и честно зафиксировать совпадения, расхождения и остаточную неопределённость.

## Trusted inputs used
- `reports/master_report.md`
- `reports/report_stage_08.md`
- `report/final_report.pdf` — прочитан только как финальный reference artifact по названиям разделов, а не как источник математической истины
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`
- `src/compute/task1.py`
- `src/compute/task1_finite.py`
- `src/compute/task1_infinite.py`
- `src/compute/task1_common.py`
- `src/compute/task2.py`
- `src/compute/common.py`

## Commands actually run
- Inspection reads via `sed -n` for:
  - `reports/master_report.md`
  - `reports/report_stage_08.md`
  - `inputs/variant_me.yaml`
  - `inputs/derived_parameters.json`
  - `src/compute/task1.py`
  - `src/compute/task1_finite.py`
  - `src/compute/task1_infinite.py`
  - `src/compute/task1_common.py`
  - `src/compute/common.py`
  - `src/compute/task2.py`
- `python3 - <<'PY' ... PY`
  - inspected the committed `out/data/*.json` structure and sampled current points before selecting control points
- `python3 - <<'PY' ... PY`
  - extracted text from `report/final_report.pdf` via `pypdf.PdfReader` to confirm the report still contains the expected numbered subsection naming
- `python3 - <<'PY' ... PY`
  - prototype independent recomputation for all five model families to establish workable tolerances and confirm the selected control points are meaningful
- `python3 - <<'PY' ... PY`
  - generated `out/audit/math_lock_checks.json` with the final independent control-point comparisons
- `python3 -m json.tool out/audit/math_lock_checks.json >/dev/null`
- `python3 - <<'PY' ... PY`
  - summarized maximum absolute differences per task from `out/audit/math_lock_checks.json`

## Control points selected
- `1.1` Erlang B / loss system:
  - `n = 1`
  - `n = 4`
  - `n = 10`
  - `n = 11`
  These points cover a low-capacity regime, a medium regime near the offered load, and the refusal-threshold crossing claimed in the summary.
- `1.2` finite queue system:
  - `(n, m) = (1, 1)`
  - `(n, m) = (4, 1)`
  - `(n, m) = (5, 5)`
  - `(n, m) = (10, 15)`
  These points cover low capacity, a boundary-like case near `a ≈ 4.64`, a characteristic internal point, and a high-capacity point. For every selected pair the audit compared the duplicated value stored in both sweep families.
- `1.3` infinite queue M/M/n:
  - `n = 4`
  - `n = 5`
  - `n = 6`
  - `n = 10`
  - `n = 15`
  These points cover the stationarity boundary, the first stationary point, an internal stationary point, and two larger-`n` checks.
- `1.4` Erlang-A / abandonment:
  - `n = 1`
  - `n = 4`
  - `n = 5`
  - `n = 10`
  - `n = 15`
  These points cover a strongly overloaded low-`n` regime, the `n = 4` point that is unstable in `1.3` but should be stabilized by abandonment here, and larger-`n` behavior.
- `2.1` finite-source repairman model:
  - `r = 1`
  - `r = 5`
  - `r = 10`
  - `r = 20`
  - `r = 36`
  These points cover saturation, a still-congested internal point, a midrange point, a light-waiting point, and the physical upper bound where waiting must vanish.

## Independently verified now
- Evidence artifact written: `out/audit/math_lock_checks.json`
- `1.1`:
  - independent method: Erlang-B recursion plus carried-traffic identities;
  - all `4` control points matched within absolute tolerance `1e-12`;
  - maximum absolute metric difference: `8.88e-16`;
  - summary check `minimal_operators_for_refusal_below_target = 11` matched exactly.
- `1.2`:
  - independent method: direct stationary birth-death recurrence, written outside solver helpers;
  - all `4` selected `(n, m)` points matched within `1e-12`;
  - maximum absolute metric difference: `8.88e-16`;
  - at all selected points the duplicated committed values in `families_by_queue_places` and `families_by_operators` matched exactly, with `dual_series_max_abs_diff = 0.0`.
- `1.3`:
  - independent method: closed-form Erlang-C evaluation plus explicit `rho < 1` stationarity check;
  - `n = 4` independently confirmed as non-stationary with `a / n = 1.160714... > 1`;
  - `n = 5` independently confirmed as the first stationary point;
  - stationary control points matched within `1e-12`;
  - maximum absolute metric difference on stationary points: `3.47e-18`;
  - summary checks `first_stationary_operators = 5` and `non_stationary_operators = [1, 2, 3, 4]` matched exactly.
- `1.4`:
  - independent method: separate Erlang-A birth-death recurrence with a stricter tail-controlled stopping rule and no call into solver helper functions;
  - all `5` selected points matched within absolute tolerance `1e-12`;
  - maximum absolute metric difference: `5.20e-13`;
  - both the committed truncation bounds and the independent truncation bounds were below the repository epsilon `1e-12` at all checked points.
- `2.1`:
  - independent method: direct finite-source birth-death recurrence plus independent recomputation of the arrival-weighted `waiting_probability`;
  - all `5` selected points matched within `1e-12`;
  - maximum absolute metric difference: `3.55e-15`;
  - the diagnostic `queue_exists_probability_state` also matched within tolerance, which independently supports the intentional distinction between arrival-weighted waiting probability and stationary queue-state share.

## Likely correct but not fully independently proven
- The committed solver outputs outside the selected control points remain only likely correct, not exhaustively proven by this stage.
- `1.4` is only semi-independent in method:
  - the audit recomputation was written separately and used a stricter stopping rule;
  - however, it still relies on the same stationary birth-death model class for Erlang-A rather than a wholly different closed-form or external implementation.
- No external CAS, textbook software, or Monte Carlo simulation was used in this pass.
- This stage did not symbolically prove monotonicity or correctness for every sweep point across all JSON artifacts.

## Mismatches found (if any)
- No mismatches found in the selected control points.
- `out/audit/math_lock_checks.json` records `mismatch_count = 0`.

## Residual mathematical uncertainty
- This is compact control-point evidence, not an exhaustive proof over every committed output point.
- `1.4` remains the least independently locked family because the alternative check still shares the same underlying birth-death stationary formulation, even though it was recomputed independently and matched tightly.
- The stage establishes absence of detected inconsistency at representative points; it does not prove the absence of all possible hidden implementation defects outside those points.

## Ready to proceed to 9B? YES/NO
YES

## Exact recommendation for next step
Use `reports/report_stage_09A_math_lock.md` and `out/audit/math_lock_checks.json` as solver-math lock evidence for a final `Stage 09B` closeout verdict pass; do not reopen solver redesign unless a new, concrete mismatch is found.
