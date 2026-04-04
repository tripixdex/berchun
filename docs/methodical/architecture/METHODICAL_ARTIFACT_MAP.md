# Methodical Artifact Map

## Статус и назначение
Этот документ замораживает generation-oriented artifact map для `M1`.

Его задача:
- показать, из каких именно репозиторных артефактов future guide должен брать числа и графики;
- зафиксировать selector rules для variant-aware checkpoints;
- запретить выдуманные числа и неподтверждённые выводы.

## Shared source priority
Будущий guide должен читать источники в таком порядке:
1. `inputs/variant_me.yaml` — student-facing raw identity и current raw input.
2. `inputs/derived_parameters.json` — derived parameters, sweep policies, truncation policy.
3. `out/data/task_*.json` — machine-readable metrics, regime flags, diagnostics.
4. `out/artifacts/figure_manifest.json` — `figure_id -> source_data_files -> output_image_path`.
5. `report/assets_manifest.json` — actual report inputs, scheme assets, current report build surface.
6. `report/final_report.tex` / `report/final_report.pdf` — section flow, teacher-facing checkpoint placement, existing wording anchors.

## Shared mapping rules
- Current `report/final_report.tex` contains run-specific figure paths. Future guide must resolve figures through manifests or active run bundle, not by hardcoding the current run ID.
- `input_snapshot` inside `out/data/task_1_1.json`, `task_1_2.json`, `task_1_3.json` contains shared task-1 fields, but guide must surface only subsection-relevant values.
- If two selector rules point to the same `x_value`, future generator deduplicates the checkpoint instead of inventing an extra one.
- If a target checkpoint is outside the available sweep, generator clamps to the nearest available artifact-backed point and states the real value.

## Shared selector rules
- `n_threshold_1_1`: first `x_value` in `out/data/task_1_1.json` with `metrics.refusal_probability < 0.01`.
- `n_threshold_prev_1_1`: previous available point before `n_threshold_1_1`.
- `n_load_anchor`: `ceil(task1.offered_load_erlangs)`, clamped to the relevant sweep range.
- `n_relief_task1`: `n_load_anchor + 3`, clamped to the relevant sweep range.
- `n_stationary_first_1_3`: first point in `out/data/task_1_3.json` with `regime.is_stationary = true`.
- `n_stationary_plus_2`: `n_stationary_first_1_3 + 2`, clamped.
- `n_stationary_plus_5`: `n_stationary_first_1_3 + 5`, clamped.
- `r_low_task2`: `1`.
- `r_mid_task2`: `min(10, max_repairers_in_sweep)`.
- `r_relief_task2`: `min(20, max_repairers_in_sweep)`.
- `r_high_safe_task2`: `min(33, max_repairers_in_sweep)`.

## Guide-level shared inputs
Для header-level blocks будущий guide может читать:
- из `inputs/variant_me.yaml`: `student_full_name`, `student_group`, `teacher_full_name`, `report_scope`, `report_year`, `journal_number`, `birth_date`;
- из `report/assets_manifest.json`: `meta.report_scope`, `meta.report_year`, `data_inputs_used`, `figure_inputs_used`;
- из `report/final_report.tex` / PDF: порядок задач и подпунктов.

## 1.1. Система без очереди

### Raw / derived fields
- Raw origin: `journal_number`, `birth_date` -> `birth_day`.
- Derived fields:
  - `derived.task1.tc_seconds`
  - `derived.task1.ts_seconds`
  - `derived.task1.arrival_rate_per_second`
  - `derived.task1.service_rate_per_second`
  - `derived.task1.offered_load_erlangs`
  - `derived.sweep_policies.task_1_1.operators`

### Machine-readable outputs
- Main data file: `out/data/task_1_1.json`.
- Required paths:
  - `input_snapshot`
  - `sweeps[0].points[*].x_value`
  - `sweeps[0].points[*].metrics.refusal_probability`
  - `sweeps[0].points[*].metrics.busy_operators_expected`
  - `sweeps[0].points[*].metrics.operators_utilization`

### Figures referenced
- Scheme: `task1_1__scheme`
- Plot: `task1_1__busy_operators_vs_operators`
- Plot: `task1_1__refusal_and_utilization_vs_operators`

### Checkpoint values to pull
- `a = offered_load_erlangs`
- `n_threshold_prev_1_1`
- `n_threshold_1_1`
- For both threshold points:
  - `refusal_probability`
  - `busy_operators_expected`
  - `operators_utilization`

### Conclusions allowed from artifacts
- При росте `n` вероятность отказа падает.
- Среднее число занятых операторов около порога меняется слабее, чем вероятность отказа.
- Минимально достаточное `n` для условия `P_отк < 0.01` определяется только по first artifact-backed threshold point.

### Facts that must NOT be invented
- Нельзя утверждать другое пороговое `n`, если его нет в данных.
- Нельзя объявлять `n` «оптимальным» без отдельного artifact-backed критерия.
- Нельзя выводить новые числа из устного пересказа report prose, если их нет в JSON.

## 1.2. Система с ограниченной очередью

### Raw / derived fields
- Raw origin: `journal_number`, `birth_date` -> `birth_day`.
- Derived fields:
  - `derived.task1.tc_seconds`
  - `derived.task1.ts_seconds`
  - `derived.task1.arrival_rate_per_second`
  - `derived.task1.service_rate_per_second`
  - `derived.task1.offered_load_erlangs`
  - `derived.sweep_policies.task_1_2.operators`
  - `derived.sweep_policies.task_1_2.queue_places`

### Machine-readable outputs
- Main data file: `out/data/task_1_2.json`.
- Required structures:
  - `sweeps[*].sweep_kind`
  - `sweeps[*].series[*].fixed_parameters`
  - `sweeps[*].series[*].points[*].metrics.refusal_probability`
  - `sweeps[*].series[*].points[*].metrics.busy_operators_expected`
  - `sweeps[*].series[*].points[*].metrics.operators_utilization`
  - `sweeps[*].series[*].points[*].metrics.queue_exists_probability`
  - `sweeps[*].series[*].points[*].metrics.queue_length_expected`
  - `sweeps[*].series[*].points[*].metrics.queue_occupancy`

### Figures referenced
- Scheme: `task1_2__scheme`
- Family A, fixed `n`, varying `m`:
  - `task1_2__refusal_vs_queue__family_by_operators`
  - `task1_2__busy_operators_vs_queue__family_by_operators`
  - `task1_2__operators_utilization_vs_queue__family_by_operators`
  - `task1_2__queue_exists_vs_queue__family_by_operators`
  - `task1_2__queue_length_vs_queue__family_by_operators`
  - `task1_2__queue_occupancy_vs_queue__family_by_operators`
- Family B, fixed `m`, varying `n`:
  - `task1_2__refusal_vs_operators__family_by_queue`
  - `task1_2__busy_operators_vs_operators__family_by_queue`
  - `task1_2__operators_utilization_vs_operators__family_by_queue`
  - `task1_2__queue_exists_vs_operators__family_by_queue`
  - `task1_2__queue_length_vs_operators__family_by_queue`
  - `task1_2__queue_occupancy_vs_operators__family_by_queue`

### Checkpoint values to pull
- Family A selector:
  - fix `n = n_load_anchor`
  - pull `m = 1`, `m = 5`, `m = 15`
- Family B selector:
  - fix `m = 5`
  - pull `n = n_load_anchor`, `n = n_relief_task1`, `n = min(15, n_threshold_1_1)`
- For each selected point pull:
  - `refusal_probability`
  - `busy_operators_expected`
  - `operators_utilization`
  - `queue_exists_probability`
  - `queue_length_expected`
  - `queue_occupancy`

### Conclusions allowed from artifacts
- Добавление мест в очереди уменьшает потери, но переносит часть нагрузки в ожидание.
- Добавление операторов уменьшает и потери, и очередь быстрее, чем одно расширение буфера ожидания.
- Абсолютное число занятых операторов меняется слабее, чем их относительная загрузка.

### Facts that must NOT be invented
- Нельзя объявлять глобально лучший pair `(n, m)` без отдельного selector policy и objective.
- Нельзя переносить числа из Family A в Family B без явного совпадения fixed parameters.
- Нельзя говорить о «полном исчезновении очереди», если метрика только мала, но не равна нулю.

## 1.3. Система с неограниченной очередью

### Raw / derived fields
- Raw origin: `journal_number`, `birth_date` -> `birth_day`.
- Derived fields:
  - `derived.task1.tc_seconds`
  - `derived.task1.ts_seconds`
  - `derived.task1.arrival_rate_per_second`
  - `derived.task1.service_rate_per_second`
  - `derived.task1.offered_load_erlangs`
  - `derived.sweep_policies.task_1_3.operators`

### Machine-readable outputs
- Main data file: `out/data/task_1_3.json`.
- Required paths:
  - `sweeps[0].points[*].regime.is_stationary`
  - `sweeps[0].points[*].diagnostics.traffic_intensity`
  - `sweeps[0].points[*].diagnostics.wait_probability`
  - `sweeps[0].points[*].metrics.busy_operators_expected`
  - `sweeps[0].points[*].metrics.operators_utilization`
  - `sweeps[0].points[*].metrics.queue_exists_probability`
  - `sweeps[0].points[*].metrics.queue_length_expected`

### Figures referenced
- Scheme: `task1_3__scheme`
- Plot: `task1_3__busy_operators_vs_operators`
- Plot: `task1_3__operators_utilization_vs_operators`
- Plot: `task1_3__queue_exists_vs_operators`
- Plot: `task1_3__queue_length_vs_operators`

### Checkpoint values to pull
- `a = offered_load_erlangs`
- pre-stationary evidence: all points before `n_stationary_first_1_3` only as regime-status evidence, without metric values
- stationary checkpoints:
  - `n_stationary_first_1_3`
  - `n_stationary_plus_2`
  - `n_stationary_plus_5`
- For stationary checkpoints pull:
  - `traffic_intensity`
  - `wait_probability`
  - `busy_operators_expected`
  - `operators_utilization`
  - `queue_exists_probability`
  - `queue_length_expected`

### Conclusions allowed from artifacts
- До первой стационарной точки стационарные метрики не должны объясняться как существующие значения.
- В стационарной зоне `busy_operators_expected` остаётся на уровне offered load, а загрузка падает при росте `n`.
- Очередь особенно тяжёлая около первой стационарной точки и быстро уменьшается при удалении от границы устойчивости.

### Facts that must NOT be invented
- Нельзя подставлять псевдо-стационарные числа для `non_stationary` points.
- Нельзя смешивать `wait_probability` и `queue_exists_probability`.
- Нельзя говорить, что очередь «исчезла», если метрики лишь малы.

## 1.4. Система с неограниченной очередью и уходом клиентов

### Raw / derived fields
- Raw origin: `journal_number`, `birth_date` -> `birth_day`, `birth_month`.
- Derived fields:
  - `derived.task1.tc_seconds`
  - `derived.task1.ts_seconds`
  - `derived.task1.tw_seconds`
  - `derived.task1.arrival_rate_per_second`
  - `derived.task1.service_rate_per_second`
  - `derived.task1.abandonment_rate_per_second`
  - `derived.task1.offered_load_erlangs`
  - `derived.truncation_policy.task_1_4.*`
  - `derived.sweep_policies.task_1_4.operators`

### Machine-readable outputs
- Main data file: `out/data/task_1_4.json`.
- Required paths:
  - `metadata.truncation_policy`
  - `sweeps[0].points[*].metrics.busy_operators_expected`
  - `sweeps[0].points[*].metrics.operators_utilization`
  - `sweeps[0].points[*].metrics.queue_exists_probability`
  - `sweeps[0].points[*].metrics.queue_length_expected`
  - `sweeps[0].points[*].truncation.tail_probability_upper_bound`
  - `sweeps[0].points[*].truncation.tail_queue_upper_bound`
  - `sweeps[0].points[*].diagnostics.traffic_intensity`

### Figures referenced
- Scheme: `task1_4__scheme`
- Plot: `task1_4__busy_operators_vs_operators`
- Plot: `task1_4__operators_utilization_vs_operators`
- Plot: `task1_4__queue_exists_vs_operators`
- Plot: `task1_4__queue_length_vs_operators`

### Checkpoint values to pull
- operator checkpoints:
  - `n = 1`
  - `n = n_load_anchor`
  - `n = n_relief_task1`
- truncation checkpoints:
  - `epsilon_probability`
  - `epsilon_queue`
  - `max_state`
  - maximum `tail_probability_upper_bound` across all points
  - maximum `tail_queue_upper_bound` across all points
- For operator checkpoints pull:
  - `busy_operators_expected`
  - `operators_utilization`
  - `queue_exists_probability`
  - `queue_length_expected`

### Conclusions allowed from artifacts
- В этой модели стационарные значения есть во всём sweep, но они получены через controlled truncation.
- Хвост очереди уменьшается при росте `n`.
- Среднее число занятых операторов выходит к offered load, а относительная загрузка падает.
- Truncation block может объясняться как контролируемое численное приближение, а не как случайная отсечка.

### Facts that must NOT be invented
- Нельзя говорить, что truncation error равен нулю.
- Нельзя использовать только один tail bound как глобальный максимум по всему sweep, если не выполнен actual max scan.
- Нельзя выдавать уход клиентов за полное устранение очереди на малых `n`.

## 2.1. Производственный участок

### Raw / derived fields
- Raw origin: `journal_number`, `birth_date` -> `birth_day`, `birth_month`.
- Derived fields:
  - `derived.task2.machine_count`
  - `derived.task2.tc_minutes`
  - `derived.task2.ts_minutes`
  - `derived.task2.arrival_rate_per_minute`
  - `derived.task2.service_rate_per_minute`
  - `derived.task2.offered_load_per_machine_erlangs`
  - `derived.sweep_policies.task_2_1.repairers`

### Machine-readable outputs
- Main data file: `out/data/task_2_1.json`.
- Required paths:
  - `input_snapshot`
  - `sweeps[0].points[*].metrics.idle_machines_expected`
  - `sweeps[0].points[*].metrics.waiting_machines_expected`
  - `sweeps[0].points[*].metrics.waiting_probability`
  - `sweeps[0].points[*].metrics.busy_repairers_expected`
  - `sweeps[0].points[*].metrics.repairers_utilization`
  - `sweeps[0].points[*].diagnostics.queue_exists_probability_state`
  - `sweeps[0].points[*].diagnostics.waiting_probability_interpretation`

### Figures referenced
- Scheme: `task2_1__scheme`
- Plot: `task2_1__idle_machines_vs_repairers`
- Plot: `task2_1__waiting_machines_vs_repairers`
- Plot: `task2_1__waiting_probability_vs_repairers`
- Plot: `task2_1__busy_repairers_vs_repairers`
- Plot: `task2_1__repairers_utilization_vs_repairers`

### Checkpoint values to pull
- `r_low_task2`
- `r_mid_task2`
- `r_relief_task2`
- `r_high_safe_task2`
- For each selected `r` pull:
  - `idle_machines_expected`
  - `waiting_machines_expected`
  - `waiting_probability`
  - `queue_exists_probability_state`
  - `busy_repairers_expected`
  - `repairers_utilization`
- Always pull `waiting_probability_interpretation` as wording guard for the guide.

### Conclusions allowed from artifacts
- При росте `r` уменьшаются и простаивающие, и ожидающие станки.
- `waiting_probability` — это вероятность ожидания нового отказа, а не календарная доля времени с очередью.
- Среднее число занятых наладчиков выходит к пределу быстрее, чем растёт общее число наладчиков.
- Относительная загрузка каждого наладчика падает по мере роста резерва.

### Facts that must NOT be invented
- Нельзя приравнивать `waiting_probability` к `queue_exists_probability_state`.
- Нельзя хардкодить `r = 33`; high-end checkpoint берётся только по `r_high_safe_task2`.
- Нельзя заявлять, что все наладчики нужны или что число наладчиков «оптимально», если это не подтверждено отдельным критерием.
