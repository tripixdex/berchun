# Output Format Contract

## Статус и назначение
Этот документ замораживает canonical output-format model поверх уже существующего delivery surface.

Он не меняет текущую delivery model, а фиксирует:
- какие formats вообще считаются допустимыми для report, guide и bundles;
- что считается current baseline;
- что идёт следующим implementation slice;
- что остаётся явно deferred.

## Canonical Concepts

| Concept | Allowed values | Meaning |
| --- | --- | --- |
| `output_format` | `pdf`, `md`, `bundle_dir`, `docx` | Top-level requested delivery format. Для single-surface deliveries это format самого surface artifact. Для multi-artifact profiles это container format. |
| `single_surface_format` | `pdf`, `md`, `docx` | Render/export format для одного operator-facing surface: report или guide. |
| `bundle_container_format` | `bundle_dir` | Top-level container format для multi-artifact delivery profiles. |
| `report_surface` | formal report baseline | Teacher-facing surface, который уже frozen и не меняется по содержанию в output-format scope. |
| `guide_surface` | methodical guide baseline | Student-facing surface, который уже frozen и не меняется по содержанию в output-format scope. |

## Core Rules
- `output_format` как request field сохраняется и не переопределяется заново.
- `bundle_dir` остаётся единственным top-level format для multi-artifact profiles.
- Для bundles дополнительные `pdf`/`docx` copies, если они позже появятся, считаются internal artifacts bundle, а не новым top-level `output_format`.
- Новый format не имеет права менять truth-bearing semantics исходного report или guide.

## Formal Report Format Family

| Format | Status | Meaning | Notes |
| --- | --- | --- | --- |
| `pdf` | current mandatory | canonical operator-facing report copy | Уже реализован и остаётся главным stable report format. |
| `docx` | frozen deferred | editable/exportable report copy | Допустим conceptually, но не открыт в runtime до отдельного implementation pass. |
| `md` | forbidden | not a supported report target | Formal report branch не переводится в Markdown target. |

## Methodical Guide Format Family

| Format | Status | Meaning | Notes |
| --- | --- | --- | --- |
| `md` | current mandatory | canonical authored and delivered guide baseline | Уже реализован для `variant_aware` и `general`. |
| `pdf` | next implementation target | readable non-editable guide copy | Следующий smallest safe runtime slice. |
| `docx` | frozen deferred | editable/exportable guide copy | Допустим conceptually, но only after stable guide PDF runtime. |

## Bundle Container Family

| Profile | Top-level format | Current status | Notes |
| --- | --- | --- | --- |
| `study_pack` | `bundle_dir` | current mandatory | Bundle may later include more internal guide/report format copies, but top-level request stays `bundle_dir`. |
| `print_pack` | `bundle_dir` | current mandatory | Print-oriented container remains report-centric in current model. |

## Minimum Supported Target Set
- `report_only -> pdf`
- `guide_only -> md`
- `study_pack -> bundle_dir`
- `print_pack -> bundle_dir`

Это frozen current runtime baseline и не должно маскироваться под более широкий format support.

## Explicit Frozen Decisions

### Report
- Report support family is `pdf + docx`.
- Current runtime support is only `pdf`.
- `docx` is allowed conceptually, but deferred.
- `md` is not a valid future report target in this branch.

### Guide
- Guide support family is `md + pdf + docx`.
- Current runtime support is only `md`.
- `pdf` is the next required expansion target.
- `docx` stays deferred until after guide PDF is stable.

### Bundles
- `bundle_dir` remains supported and mandatory for multi-artifact delivery.
- `study_pack` and `print_pack` do not switch their top-level `output_format` to `pdf` or `docx`.
- If bundles later include extra report/guide formats, these are copied artifacts inside the bundle.

## Delivery Profile × Format Contract

| Delivery profile | Current supported formats | Frozen future-eligible formats | Contract notes |
| --- | --- | --- | --- |
| `report_only` | `pdf` | `docx` | `md` and `bundle_dir` are not report-only targets. |
| `guide_only` | `md` | `pdf`, `docx` | `pdf` comes before `docx`; both must preserve `guide_mode` split. |
| `study_pack` | `bundle_dir` | `bundle_dir` only | Future extra format copies live inside the bundle; top-level format does not change. |
| `print_pack` | `bundle_dir` | `bundle_dir` only | Remains report-centric; no guide format expansion is implied here. |

## Artifact-Level Naming Policy
- Report artifacts:
  - `report/final_report.pdf`
  - `report/final_report.docx` when DOCX is eventually implemented
- Guide artifacts:
  - `guide/methodical_guide__variant.md`
  - `guide/methodical_guide__general.md`
  - `guide/methodical_guide__variant.pdf` when guide PDF is implemented
  - `guide/methodical_guide__general.pdf` when guide PDF is implemented
  - `guide/methodical_guide__variant.docx` when guide DOCX is implemented
  - `guide/methodical_guide__general.docx` when guide DOCX is implemented

## v1 Mandatory vs Deferred

### Mandatory current baseline
- report PDF
- guide Markdown
- `bundle_dir` for multi-artifact deliveries

### Mandatory next implementation slice
- guide PDF for:
  - `guide_only + variant_aware`
  - `guide_only + general`

### Explicitly deferred
- report DOCX
- guide DOCX
- bundle-local optional format toggles exposed in operator UX
- replacing `bundle_dir` with single-file bundle formats

## Constraints For Report vs Guide
- Report export must stay consistent with the frozen teacher-facing report branch and not introduce a new editable truth source.
- Guide export must preserve the already frozen split:
  - `variant_aware`
  - `general`
- General guide exports must keep existing restrictions:
  - no run-specific plots;
  - no variant-specific checkpoints presented as universal facts.
- Variant-aware guide exports must preserve existing safety guards and source-run requirements.

## Unified Session Exposure Rule
- Unified session continues to offer only formats that are actually implemented for the chosen profile.
- Format choice stays after profile/scope/mode selection and before final confirm.
- No extra sub-prompts like “also include PDF copy?” are allowed in the first expansion slice.
- For bundles, unified session should continue to show only `bundle_dir` unless a later explicit scope changes that rule.

## Safe Implementation Path
- First open `guide_only + pdf`.
- Then, if needed, allow `study_pack` to include guide PDF as internal artifact while keeping `output_format = bundle_dir`.
- Only after that open `report_only + docx`.
- Open `guide_only + docx` last.

## Explicitly Forbidden Shortcuts
- Нельзя подменять output-format expansion скрытым redesign delivery profiles.
- Нельзя считать `docx` обязательным только потому, что concept уже frozen.
- Нельзя открывать bundle top-level `pdf`/`docx` как shortcut вместо `bundle_dir`.
- Нельзя открывать guide DOCX раньше guide PDF только из соображений “одним махом поддержать всё”.
