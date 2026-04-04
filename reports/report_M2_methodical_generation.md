# Report M2 — Variant-Aware Core Explanation Generation

## Scope ID and Name
- Scope ID: `M2`
- Scope name: `Variant-Aware Core Explanation Generation`

## Objective
Собрать первый реальный draft methodical guide для `1.1`, `1.2`, `1.3`, `1.4`, `2.1` простым русским языком, строго по frozen skeleton/contract из `M0/M1` и только на artifact-supported данных текущего варианта.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_PLAN.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_SKELETON.md`
- `docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`
- `docs/methodical/architecture/METHODICAL_DEFENSE_TEMPLATE.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`
- `out/artifacts/figure_manifest.json`
- `report/assets_manifest.json`

## Files Created
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/report_M2_methodical_generation.md`

## Files Updated
- `reports/master_report.md`

## Commands Run
- `sed -n '1,220p' reports/master_report.md`
- `sed -n '1,220p' docs/methodical/architecture/METHODICAL_GUIDE_PLAN.md`
- `sed -n '1,260p' docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `sed -n '1,260p' docs/methodical/architecture/METHODICAL_GUIDE_SKELETON.md`
- `sed -n '1,320p' docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`
- `sed -n '1,240p' docs/methodical/architecture/METHODICAL_DEFENSE_TEMPLATE.md`
- `sed -n '1,240p' inputs/variant_me.yaml`
- `jq '.' inputs/derived_parameters.json`
- `pdftotext report/final_report.pdf - | sed -n '1,260p'`
- `pdftotext report/final_report.pdf - | sed -n '260,520p'`
- `pdftotext report/final_report.pdf - | sed -n '520,760p'`
- `sed -n '1,260p' out/artifacts/figure_manifest.json`
- `jq '.' report/assets_manifest.json`
- `jq ... out/data/task_1_1.json`
- `jq ... out/data/task_1_2.json`
- `jq ... out/data/task_1_3.json`
- `jq ... out/data/task_1_4.json`
- `jq ... out/data/task_2_1.json`
- `rg -n '^## |^### |^#### ' docs/methodical/content/METHODICAL_GUIDE.md`
- `rg -n '=' docs/methodical/content/METHODICAL_GUIDE.md`
- `python3 - <<'PY' ... PY` validation for subsection coverage, block order, numeric allowlist and formula-line scan

## What Was Generated Now
- Создан `docs/methodical/content/METHODICAL_GUIDE.md` как первый variant-aware draft methodical guide.
- Внутри guide собраны short guide-level sections и реальные explanatory blocks для `1.1`, `1.2`, `1.3`, `1.4`, `2.1`.
- Для каждого подпункта сохранён frozen order из `M1`, включая обязательные финальные блоки:
  - `Что это значит простыми словами`
  - `Что сказать на защите`
- Во все подпункты добавлены только краткие safe defense hints; полный defense layer intentionally не открывался.

## How Artifact-Supported Numbers Were Enforced
- Все variant inputs и derived parameters брались только из `inputs/variant_me.yaml` и `inputs/derived_parameters.json`.
- Все checkpoint values брались только по frozen selector rules из `docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`.
- Для `1.1` использован first threshold point с `refusal_probability < 0.01`.
- Для `1.2` использованы только две замороженные family surfaces:
  - fixed `n = 5`, varying `m = 1/5/15`
  - fixed `m = 5`, varying `n = 5/8/11`
- Для `1.3` не выводились стационарные метрики для `n = 1..4`; текст начинается с first stationary point `n = 5`.
- Для `1.4` вместе с метриками использованы `epsilon_probability`, `epsilon_queue`, `max_state` и worst-case tail bounds.
- Для `2.1` отдельно сохранено различие между `waiting_probability` и `queue_exists_probability_state`.
- Дополнительно прогнан validator, который проверил:
  - покрытие `1.1`, `1.2`, `1.3`, `1.4`, `2.1`
  - порядок блоков по frozen skeleton
  - поддержку всех numeric tokens artifact-derived allowlist
  - отсутствие неожиданных formula-like lines вне frozen report surface

## What Was Intentionally Left For M3
- Полный defense layer по `docs/methodical/architecture/METHODICAL_DEFENSE_TEMPLATE.md` не интегрирован.
- Не создавались отдельные defense cards по каждому подпункту.
- Не открывались export/render/publication tasks.
- Не выполнялась интеграция guide в отдельный operator path.

## Remaining Risks
- Guide пока существует как markdown draft, а не как финальный delivery surface.
- Defense-help слой пока минимален и ограничен только short safe hints в конце подпунктов.
- Guide собран по текущему committed variant artifact set; future run-specific assembly path ещё не открыт.
- В guide местами остаются repo-facing термины вроде путей к данным, потому что M2 фиксировал content truth, а не final packaging polish.

## Ready for M3?
- `YES`

## Exact Recommendation For Next Step
- Открыть `M3 — Defense Layer Integration`.
- В `M3` ограничиться только заполнением repeatable defense-note cards для `1.1`, `1.2`, `1.3`, `1.4`, `2.1` поверх уже сгенерированного guide, не меняя solver/report truth и не открывая ещё export surface.
