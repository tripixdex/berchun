# Delivery Output Matrix

## Статус и назначение
Этот документ замораживает concrete matrix для delivery/export surface.

Он отвечает на вопрос: какие profile combinations вообще существуют, что они обязаны выдавать и какие combinations в v1 запрещены.

## Shared Rules
- `report_scope` применяется только к report-bearing profiles.
- `guide_scope` применяется только к guide-bearing profiles.
- В `study_pack` для v1 действует правило `guide_scope = report_scope`.
- `print_pack` в v1 является report-centric bundle и не включает guide surface.
- `bundle_dir` означает directory delivery, а не zip archive.
- `docx` не входит в первый runtime slice, even though concept is frozen in the contract.

## Matrix

| Delivery profile | Supported scopes | Guide mode | Supported formats | Required artifacts | Disallowed combinations |
| --- | --- | --- | --- | --- | --- |
| `report_only` | `report_scope = task1 \| task2 \| full` | not used | `pdf` in v1 | `delivery_manifest.json`, `report/final_report.pdf`, `report/assets_manifest.json` | `guide_scope`, `guide_mode`, `md`, `bundle_dir`-only-with-guide semantics, `docx` in first runtime slice |
| `study_pack` | `report_scope = task1 \| task2 \| full`; `guide_scope = same as report_scope` | `variant_aware` | `bundle_dir` | `delivery_manifest.json`, `report/final_report.pdf`, `report/assets_manifest.json`, `guide/methodical_guide__variant.md`, `guide/assets/schemes/...`, `guide/assets/plots/...` | `guide_scope != report_scope`, `pdf` as single-file target, `docx` in first runtime slice |
| `study_pack` | `report_scope = task1 \| task2 \| full`; `guide_scope = same as report_scope` | `general` | `bundle_dir` | `delivery_manifest.json`, `report/final_report.pdf`, `report/assets_manifest.json`, `guide/methodical_guide__general.md`, `guide/assets/schemes/...` | run-specific plots inside guide, `guide_scope != report_scope`, `docx` in first runtime slice |
| `guide_only` | `guide_scope = task1 \| task2 \| full` | `variant_aware` | `md` | `delivery_manifest.json`, `guide/methodical_guide__variant.md`, `guide/assets/schemes/...`, `guide/assets/plots/...` | `report_scope`, report artifacts, `pdf`/`docx` in first runtime slice |
| `guide_only` | `guide_scope = task1 \| task2 \| full` | `general` | `md` | `delivery_manifest.json`, `guide/methodical_guide__general.md`, `guide/assets/schemes/...` | run-specific plots, report artifacts, `pdf`/`docx` in first runtime slice |
| `print_pack` | `report_scope = task1 \| task2 \| full` | not used in v1 | `bundle_dir` | `delivery_manifest.json`, `report/final_report.pdf`, `report/final_report.tex`, `report/assets_manifest.json`, `report/assets/...`, `figures/...` for the selected report scope | guide surface in v1, `md`, `docx` in first runtime slice |

## Interpretation Notes

### `report_only`
- Это самый узкий delivery profile.
- Он нужен, когда operator хочет только финальный formal report surface без study layer.

### `study_pack`
- Это нормализованный combined profile, а не checkbox “приложить guide”.
- Он всегда содержит formal report и ровно один guide surface.
- В v1 combined scope intentionally упрощён: `guide_scope` должен совпадать с `report_scope`.

### `guide_only`
- Этот profile не тащит formal report surface.
- Он нужен для самостоятельной раздачи методических материалов.

### `print_pack`
- Этот profile описывает print-oriented directory bundle.
- В v1 это report-centric bundle: formal PDF плюс self-contained print/archival neighbors.

## v1 Implementation Slice Recommendation
Для первого narrow implementation pass достаточно покрыть:
1. `report_only` with `pdf`
2. `guide_only` with `variant_aware + md`
3. skeleton assembly for `study_pack` and `print_pack` as `bundle_dir`

Rows `guide_only/general` и `study_pack/general` входят в frozen architecture, но не обязаны быть первыми в runtime implementation order.
