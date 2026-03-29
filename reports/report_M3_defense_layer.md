# Report M3 — Defense Layer Integration

## Scope ID and Name
- Scope ID: `M3`
- Scope name: `Defense Layer Integration`

## Objective
Встроить в `docs/METHODICAL_GUIDE.md` полноценный повторяемый defense layer для `1.1`, `1.2`, `1.3`, `1.4`, `2.1`, не меняя solver truth, formal report behavior, frozen guide skeleton и уже сгенерированный explanatory layer из `M2`.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/METHODICAL_GUIDE_PLAN.md`
- `docs/METHODICAL_GUIDE_CONTRACT.md`
- `docs/METHODICAL_GUIDE_SKELETON.md`
- `docs/METHODICAL_ARTIFACT_MAP.md`
- `docs/METHODICAL_DEFENSE_TEMPLATE.md`
- `docs/METHODICAL_GUIDE.md`
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
- `reports/report_M3_defense_layer.md`

## Files Updated
- `docs/METHODICAL_GUIDE.md`
- `reports/master_report.md`

## Commands Run
- `sed -n '1,220p' reports/master_report.md`
- `sed -n '1,240p' docs/METHODICAL_GUIDE_CONTRACT.md`
- `sed -n '1,260p' docs/METHODICAL_ARTIFACT_MAP.md`
- `sed -n '1,220p' docs/METHODICAL_DEFENSE_TEMPLATE.md`
- `sed -n '1,260p' docs/METHODICAL_GUIDE.md`
- `sed -n '260,940p' docs/METHODICAL_GUIDE.md`
- `jq ... out/data/task_1_1.json`
- `jq ... out/data/task_1_2.json`
- `jq ... out/data/task_1_3.json`
- `jq ... out/data/task_1_4.json`
- `jq ... out/data/task_2_1.json`
- `rg -n '#### Что сказать на защите|##### Карточка|Что могут спросить|Короткий безопасный ответ|Где чаще всего путаются|Каких слов лучше не говорить|Один практический смысл' docs/METHODICAL_GUIDE.md`
- `python3 - <<'PY' ... PY` validation for defense-card coverage, skeleton alignment, numeric allowlist and formula-line scan

## What Was Added Now
- Во все пять подпунктов `1.1`, `1.2`, `1.3`, `1.4`, `2.1` встроены полноценные defense blocks внутри уже существующих секций `Что сказать на защите`.
- Для каждого подпункта добавлены `4` короткие карточки:
  - смысл модели
  - смысл метрики
  - как читать график
  - итоговый вывод
- Каждая карточка использует один и тот же краткий формат:
  - `Что могут спросить`
  - `Короткий безопасный ответ`
  - `Где чаще всего путаются`
  - `Каких слов лучше не говорить`
  - `Один практический смысл`

## How Defense Cards Were Grounded In Artifact-Supported Truth
- Все variant-specific числа в карточках уже присутствуют в frozen M2 guide и повторно проверены по `out/data/task_*.json`.
- `1.1` опирается только на threshold pair `n = 10/11` и condition `P_отк < 0.01`.
- `1.2` использует только frozen selector-backed families:
  - fixed `n = 5`, varying `m = 1/5/15`
  - fixed `m = 5`, varying `n = 5/8/11`
- `1.3` сохраняет ключевую защитную границу: first stationary point `n = 5`; до неё стационарные числа не invent.
- `1.4` опирается на controlled truncation block и реальные upper bounds `4.791e-14` и `8.497e-13`.
- `2.1` отдельно удерживает distinction between `waiting_probability` and `queue_exists_probability_state`.
- Дополнительно прогнан validator, который подтвердил:
  - каждый required subsection теперь содержит defense layer с минимум `4` карточками
  - карточки стоят внутри текущего guide skeleton и не ломают subsection order
  - все numeric tokens остаются artifact-supported
  - неожиданных formula-like claims не добавлено

## What Intentionally Remained Unchanged
- Explanatory blocks из `M2` сохранены и не переписаны.
- Guide skeleton и order section blocks не менялись.
- Solver mathematics, formal report branch, figures, manifests и export surface не трогались.
- Separate publication/render/operator flow для guide по-прежнему не открывался.

## Remaining Risks
- Guide всё ещё остаётся markdown-draft, а не final delivery surface.
- Defense cards короткие и запоминаемые, но пока не прошли отдельную end-to-end consistency pass against a future assembled guide package.
- В guide сохранены некоторые repo-facing слова из предыдущего M2 layer; M3 сознательно не открывал общий language polish beyond the defense cards.

## Ready for M4?
- `YES`

## Exact Recommendation For Next Step
- Открыть `M4 — End-to-End Assembly + Consistency Validation`.
- В `M4` ограничиться только полной сквозной проверкой согласованности guide: числа, обозначения, graph references, defense cards и local conclusions должны быть сверены между `docs/METHODICAL_GUIDE.md`, current machine-readable artifacts и formal report surface, без открытия export/pipeline redesign.
