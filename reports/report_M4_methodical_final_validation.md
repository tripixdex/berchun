# Report M4 — Methodical Final Validation

## Scope ID and Name
- Scope ID: `M4`
- Scope name: `End-to-End Assembly + Consistency Validation`

## Objective
Провести полную сквозную проверку `docs/methodical/content/METHODICAL_GUIDE.md` против frozen skeleton, frozen artifact map, current machine-readable outputs, current formal report surface и уже встроенных defense cards, а при необходимости внести только узкие consistency-corrections.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_PLAN.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_SKELETON.md`
- `docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`
- `docs/methodical/architecture/METHODICAL_DEFENSE_TEMPLATE.md`
- `docs/methodical/content/METHODICAL_GUIDE.md`
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
- `reports/report_M4_methodical_final_validation.md`

## Files Updated
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/master_report.md`

## Commands Run
- `sed -n '1,240p' reports/master_report.md`
- `sed -n '1,260p' docs/methodical/architecture/METHODICAL_GUIDE_SKELETON.md`
- `sed -n '1,320p' docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`
- `rg -n '^(## |### |#### |##### )' docs/methodical/content/METHODICAL_GUIDE.md`
- `rg -n '^\\section|^\\subsection|^\\subsubsection|Задача №|Вероятность|средн|коэффициент|очеред' report/final_report.tex`
- `sed -n '1,220p' docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `sed -n '1,220p' docs/methodical/architecture/METHODICAL_DEFENSE_TEMPLATE.md`
- `sed -n '1,240p' inputs/variant_me.yaml`
- `jq '{derived: .derived, sweep_policies: .derived.sweep_policies, truncation_policy: .derived.truncation_policy}' inputs/derived_parameters.json`
- `pdftotext report/final_report.pdf - | sed -n '1,260p'`
- `jq ... out/data/task_1_1.json out/data/task_1_3.json out/data/task_1_4.json`
- `sed -n '1,320p' docs/methodical/content/METHODICAL_GUIDE.md`
- `sed -n '321,700p' docs/methodical/content/METHODICAL_GUIDE.md`
- `sed -n '701,1120p' docs/methodical/content/METHODICAL_GUIDE.md`
- `jq ... out/data/task_1_2.json`
- `jq ... out/data/task_2_1.json`
- `sed -n '1,120p' out/artifacts/figure_manifest.json`
- `sed -n '1,220p' report/assets_manifest.json`
- `sed -n '1,240p' reports/report_M3_defense_layer.md`
- `rg -n 'В характерной точке r = 10|0\\.891|0\\.876|P_отк < 0\\.01|При n = 5 переход от m = 1 к m = 15|Оставшийся вклад не превышает 4\\.791e-14|При r = 20 среднее число ожидающих станков становится 0\\.002' report/final_report.tex`
- `rg -n 'первый черновик|stable baseline|черновик' docs/methodical/content/METHODICAL_GUIDE.md docs/methodical/architecture/METHODICAL_GUIDE_PLAN.md reports/report_M2_methodical_generation.md reports/report_M3_defense_layer.md`
- `python3 - <<'PY' ... PY` end-to-end validator for subsection order, defense-card coverage, graph-reading blocks, manifest coverage, numeric allowlist, selector checkpoints and formal-report anchors

## What Was Validated
- Подпункты `1.1`, `1.2`, `1.3`, `1.4`, `2.1` реально присутствуют в guide.
- В каждом required subsection сохранён frozen order обязательных блоков из `docs/methodical/architecture/METHODICAL_GUIDE_SKELETON.md`.
- Во всех пяти required subsections сохранён полноценный defense layer с повторяемыми карточками и всеми обязательными полями.
- Graph-reading blocks остаются согласованными с frozen contract:
  - явно называют ось `X`;
  - явно называют ось `Y`;
  - явно говорят, что остаётся фиксированным;
  - дают простой смысл формы кривой.
- Все числовые токены в `docs/methodical/content/METHODICAL_GUIDE.md` повторно проверены против current artifacts и их допустимых rounded renderings.
- Selector-backed checkpoints повторно подтверждены:
  - `1.1`: first `P_отк < 0.01` действительно достигается при `n = 11`;
  - `1.3`: first stationary point действительно `n = 5`;
  - `1.4`: maximum controlled-truncation upper bounds действительно `4.791e-14` и `8.497e-13`;
  - `2.1`: `waiting_probability` по-прежнему интерпретируется как `arrival_weighted_probability_for_new_breakdown`.
- Manifest cross-check подтвердил наличие всех нужных plot ids и scheme ids, на которые опирается frozen artifact map.
- Guide повторно сверён с current formal report surface по ключевым checkpoint claims и не даёт противоречащих выводов.

## What Was Corrected, If Anything
- В `docs/methodical/content/METHODICAL_GUIDE.md` исправлена одна узкая wording inconsistency в шапке:
  - было: guide назван `первым черновиком`;
  - стало: guide назван `текущим базовым вариантом`.
- Других содержательных inconsistencies между guide, artifacts, frozen skeleton и formal report surface не обнаружено.

## What Intentionally Remained Unchanged
- Основной explanatory layer из `M2` не переписывался.
- Defense cards из `M3` не перерабатывались по содержанию.
- Frozen guide skeleton, artifact map и defense template не менялись.
- Solver mathematics, formal report branch, figure generation и export/render surface не открывались.

## Remaining Risks
- Methodical branch теперь стабилен как markdown baseline, но не как отдельная publication/export surface.
- Если позже понадобится delivery-format beyond markdown, это должен быть новый явный scope, а не продолжение `M4`.

## Can the Methodical Branch Now Be Frozen?
- `YES`

## Exact Recommendation for Next Step
- Зафиксировать methodical branch как stable baseline на уровне текущего `docs/methodical/content/METHODICAL_GUIDE.md`.
- Новый внутренний corrective scope для methodical branch не открывать.
- Если owner позже захочет продолжение, открывать уже отдельный explicit scope только на delivery/export surface, не переоткрывая solver truth, formal report branch или frozen guide structure.
