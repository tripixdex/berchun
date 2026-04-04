# Delivery Surface Contract

## Статус и назначение
Этот документ замораживает operator contract и canonical concepts для future delivery/export surface.

Он вводит нормализованную delivery model поверх уже существующих baselines и запрещает превращать delivery selection в набор несвязанных флагов.

## Canonical Concepts

| Concept | Allowed values | Meaning |
| --- | --- | --- |
| `report_scope` | `task1`, `task2`, `full` | Какая часть formal report surface должна войти в delivery. Используется только если profile включает report surface. |
| `delivery_profile` | `report_only`, `study_pack`, `guide_only`, `print_pack` | Что именно выдаёт delivery surface: только report, report вместе с study materials, только guide, либо print-oriented bundle. |
| `guide_scope` | `task1`, `task2`, `full` | Какая часть methodical surface должна войти в delivery. Используется только если profile включает guide surface. |
| `guide_mode` | `variant_aware`, `general` | Variant-aware guide опирается на конкретный run и его числа. General guide не привязан к student identity и не содержит variant-specific checkpoints. |
| `output_format` | `pdf`, `md`, `bundle_dir`, `docx` | Формат primary delivery result. В runtime v1 поддерживаются только `pdf`, `md`, `bundle_dir`; `docx` зарезервирован как follow-up extension. |

## Meaning Rules
- `report_scope` и `guide_scope` — разные concepts и не должны сливаться в одно поле.
- Когда profile не включает соответствующую surface, поле не передаётся и не сериализуется как `none`.
- `guide_mode = variant_aware` всегда означает artifact-backed methodical material.
- `guide_mode = general` всегда означает non-variant study material без student identity и без run-specific чисел.

## Frozen v1 Support Decision
- `pdf` — `YES`, mandatory in v1 for report-bearing single-surface deliveries.
- `md` — `YES`, mandatory in v1 for guide-bearing single-surface deliveries.
- `bundle_dir` — `YES`, mandatory in v1 for multi-artifact deliveries and print-oriented bundles.
- `docx` — `NO` for the first runtime slice; concept frozen now, implementation deferred to a later pass.

## Delivery Root And Layout
Каждая delivery assembly должна собираться в отдельный каталог:

```text
deliveries/<delivery_id>/
  delivery_manifest.json
  report/
    final_report.pdf
    final_report.tex
    assets_manifest.json
    assets/...
  figures/...
  guide/
    methodical_guide__variant.md
    methodical_guide__general.md
    assets/
      schemes/...
      plots/...
```

Правила layout:
- `delivery_manifest.json` обязателен всегда.
- Каталоги `report/`, `figures/`, `guide/` появляются только если нужны выбранному profile.
- `figures/` хранит copied plot PNG files только для self-contained bundle profiles.
- Внутреннее физическое dedupe файлов не является обязательным в v1.

## Naming Policy
- Все operator-facing filenames и directory names остаются на английском.
- Delivery root называется `deliveries/<delivery_id>/`.
- `delivery_id` должен быть детерминированно читаемым и включать как минимум:
  - UTC timestamp;
  - `delivery_profile`;
  - основной scope tag.
- Имена report artifacts остаются совместимыми с уже frozen report surface:
  - `final_report.pdf`
  - `final_report.tex`
  - `assets_manifest.json`
- Имена guide artifacts обязаны явно различать mode:
  - `methodical_guide__variant.md`
  - `methodical_guide__general.md`

## Minimal `delivery_manifest.json`
В future implementation manifest обязан содержать минимум:
- `delivery_id`
- `delivery_profile`
- `output_format`
- `report_scope` when present
- `guide_scope` when present
- `guide_mode` when present
- `source_kind`: `run_bundle` or `general_baseline`
- `source_run_id` when `guide_mode = variant_aware` or report surface comes from a run
- список реально выданных artifact paths

## Operator-Facing Selection Rules
- Operator truth path и delivery path должны быть разведены:
  - `build` создаёт truth-bearing run bundle;
  - `deliver` пакует уже существующие baselines.
- Для `variant_aware` delivery operator должен выбрать успешный run source.
- Для `general` guide delivery run source не требуется.
- Если profile включает report surface, operator обязан выбрать `report_scope`.
- Если profile включает guide surface, operator обязан выбрать `guide_scope` и `guide_mode`.
- В combined profile `study_pack` v1 требует `guide_scope = report_scope`.
- `print_pack` в v1 не включает guide surface.
- Selection UX должен идти в таком порядке:
  1. `delivery_profile`
  2. source context (`run_bundle` or `general_baseline`)
  3. `report_scope` if needed
  4. `guide_mode` if needed
  5. `guide_scope` if needed
  6. `output_format`
  7. confirmation summary

## Rules For Images, Figures And Schemes
- Report-bearing deliveries используют тот же plot/scheme truth, что и formal report baseline.
- Variant-aware guide deliveries могут включать:
  - расчётные схемы выбранного guide scope;
  - реальные plot PNG files текущего run для выбранного guide scope.
- General guide deliveries в v1 могут включать только расчётные схемы.
- General guide deliveries не имеют права включать run-specific plots, потому что они несут variant-specific numeric truth.

## Mandatory vs Optional In v1

### Mandatory in v1
- Normalized delivery request model.
- Profiles:
  - `report_only`
  - `study_pack`
  - `guide_only`
  - `print_pack`
- Formats:
  - `pdf`
  - `md`
  - `bundle_dir`
- Separate delivery root `deliveries/<delivery_id>/...`
- `delivery_manifest.json`

### Explicitly Deferred Beyond The First Runtime Slice
- `docx`
- zipped delivery outputs
- guide PDF / guide DOCX
- combined bundles where `guide_scope` differs from `report_scope`
- blind redaction of variant-aware guide into `general`

## Explicitly Forbidden Shortcuts
- Нельзя сводить delivery selection к одному флагу вида “attach study materials”.
- Нельзя смешивать truth generation и delivery packaging в одном неявном path.
- Нельзя строить `general` guide удалением student-specific строк из variant-aware guide.
- Нельзя брать variant-aware figures для general guide.
