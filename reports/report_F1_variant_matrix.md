# F1 — Variant Matrix Verification

## Objective
Проверить, что канонический путь `build -> solve -> figures -> report` устойчиво отрабатывает не только на текущем working set, но и на компактной репрезентативной матрице других вариантов без изменения solver truth и report semantics.

## Trusted inputs used
- `README.md`
- `reports/master_report.md`
- `src/cli.py`
- `src/input_schema.py`
- `src/build_pipeline.py`
- `src/intake.py`
- `src/variant.py`
- `inputs/examples/student_example.yaml`
- текущий reference-compatible report path через `python3 -m src.cli build`

## Files created
- `reports/report_F1_variant_matrix.md`

## Files updated
- `out/audit/variant_matrix_checks.json`
- `reports/master_report.md`

## Variant matrix used
- `V01`: `journal=1`, `day=1`, `month=1` — лёгкий базовый случай.
- `V02`: `journal=1`, `day=28`, `month=12` — тяжёлый call-центр, крупный участок.
- `V03`: `journal=5`, `day=29`, `month=2` — тяжёлый `1.4` с коротким ожиданием.
- `V04`: `journal=8`, `day=31`, `month=12` — тяжёлый `1.4` и выраженный профиль `2.1`.
- `V05`: `journal=15`, `day=15`, `month=6` — средний профиль.
- `V06`: `journal=25`, `day=10`, `month=9` — более лёгкий `1.3`, крупный участок.
- `V07`: `journal=30`, `day=31`, `month=1` — контрастный `2.1`, `first_stationary = 2`.
- `V08`: `journal=30`, `day=1`, `month=12` — лёгкий `2.1`, большой пул станков.
- `V09`: `journal=20`, `day=20`, `month=6` — точная граница `1.3` с `offered_load = 2.0`.

Матрица покрыла:
- низкие / средние / высокие значения `journal_number`;
- разные сочетания `birth_day` / `birth_month`;
- границы `1.3` от `2` до `7`;
- более тяжёлые варианты `1.4`;
- разные профили `2.1` при `max_repairers` от `31` до `42`.

## Commands actually run
- инспекция через `sed -n` и `rg -n` по `README.md`, `reports/master_report.md`, `src/cli.py`, `src/input_schema.py`, `src/build_pipeline.py`, `src/intake.py`, `src/variant.py`;
- локальные `python3 - <<'PY' ... PY` probes для структуры `out/data/*.json`, `out/artifacts/figure_manifest.json` и `report/assets_manifest.json`;
- основной audit harness `python3 - <<'PY' ... PY`, который:
  - создал evidence artifact `out/audit/variant_matrix_checks.json`;
  - запустил `9` изолированных команд вида `python3 -m src.cli build --input <temp>/<case>/input.yaml --runs-dir <temp>/<case>/runs --variant-path <temp>/<case>/workspace/inputs/variant_me.yaml --derived-path <temp>/<case>/workspace/inputs/derived_parameters.json --out-dir <temp>/<case>/workspace/out/data --figures-dir <temp>/<case>/workspace/figures --manifest-path <temp>/<case>/workspace/out/artifacts/figure_manifest.json --report-source-path <temp>/<case>/workspace/report/final_report.tex --report-pdf-path <temp>/<case>/workspace/report/final_report.pdf --report-assets-manifest-path <temp>/<case>/workspace/report/assets_manifest.json`;
  - использовал temp root `/var/folders/8y/2hybtl_s3j9d02mwk4n6xhj40000gn/T/berchun_f1_final_9o51fav4`;
- `python3 -m json.tool out/audit/variant_matrix_checks.json >/dev/null`;
- локальные `python3 - <<'PY' ... PY` summary checks по итоговому evidence artifact.

Точные per-case build commands сохранены в `out/audit/variant_matrix_checks.json` в `results[].commands`.

## Invariants checked
- `report_artifacts_exist`: PDF/TeX/run metadata/registry существуют и не пустые.
- `manifest_structure`: figure/report manifests валидны и сохраняют структурные counts `27 plot / 5 overview / 5 scheme`.
- `task_1_1_monotone_and_threshold`: вероятность отказа не возрастает по числу операторов, summary threshold совпадает с первой точкой ниже целевого уровня.
- `task_1_2_finite_and_monotone_refusal`: во всех family sweeps значения конечны, допустимы и вероятность отказа не возрастает при росте capacity.
- `task_1_3_boundary_consistency`: non-stationary зона отделена явно, `first_stationary_operators` совпадает с ожидаемым `floor(offered_load) + 1`.
- `task_1_4_truncation_sanity`: все точки конечны и неотрицательны, `stationary_truncated` используется согласованно, хвостовые upper bounds не превышают `epsilon = 1e-12`.
- `task_2_1_plausible_curves`: нет отрицательных/NaN значений, `waiting_probability` и `waiting_machines_expected` не возрастают, на максимальном числе наладчиков ожидание исчезает, arrival-weighted interpretation сохранена.
- `report_structure_smoke`: rebuilt PDF содержит обе задачи и имеет ненулевую длину.

## Successful cases
- Все `9/9` случаев завершились статусом `success`; build failures, suspicious cases и manifest/report regressions не зафиксированы.
- Диапазон подтверждённых `1.1` threshold points: от `n = 5` до `n = 13`.
- Диапазон подтверждённых `1.3` first stationary points: от `n = 2` до `n = 7`.
- Во всех `9` случаях `2.1` на правом конце sweep дал `waiting_probability = 0.0` и `waiting_machines_expected = 0.0`.
- Во всех `9` случаях `1.4` сохранил sane truncation bounds; максимальный `first_tail_probability_upper_bound` в матрице составил `4.1823839983783565e-14`, что существенно ниже `1e-12`.

## Failed or suspicious cases
- Не обнаружены.

## Residual uncertainty
- Это компактная матрица из `9` representative cases, а не исчерпывающий перебор всего variant space.
- Проверялись structural и invariant-style свойства; эта проверка не является формальным доказательством всех математических тождеств на каждом возможном варианте.
- Визуальная ручная ревизия каждого PDF отдельно не проводилась; выполнялся structural smoke через успешную сборку, manifests и извлечение текста.

## Ready to proceed to F2? YES

## Exact recommendation for next scope
Открыть `F2` только как финальный freeze-review / verdict pass поверх уже накопленного evidence trail: `Stage 09A`, `Stage 09B`, `R6` и текущего `F1`. Solver, report family и build/archive semantics не пересматривать без нового конкретного mismatch.
