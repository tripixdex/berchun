# UX Scenario Matrix

## Status and Purpose
Этот документ замораживает operator-visible scenario layer поверх already implemented delivery runtime.

Он определяет не внутренние fields, а human-language scenarios, которые future one-button session должен показывать оператору.

## Shared Operator Rules
- Scope of work выбирается на input/build layer и дальше переиспользуется автоматически.
- `Ничего дополнительно не выдавать` остаётся valid skip path после build, но не считается отдельной delivery scenario family.
- Internal mapping остаётся deterministic and hidden.
- Standard one-button session показывает только operator-meaningful formats.
- Markdown остаётся техническим direct-CLI surface и скрывается из default session.

## Scenario Matrix

| Operator-visible scenario | What the operator sees | Internal runtime mapping | Formats offered in one-button flow | What stays hidden |
| --- | --- | --- | --- | --- |
| `Только итоговый отчёт` | “Собрать только итоговый отчёт по выбранному объёму работы” | `delivery_profile=report_only`, `report_scope=build.report_scope` | `PDF`, `DOCX` | `delivery_profile`, повторный `report_scope`, `source_run_id`, manifest detail |
| `Отчёт + материалы для подготовки` -> `персональные` | “Собрать отчёт и персональные материалы по этому варианту” | `delivery_profile=study_pack`, `report_scope=build.report_scope`, `guide_mode=variant_aware`, `guide_scope=report_scope`, `output_format=bundle_dir` | `папка-комплект` | `study_pack`, `guide_scope=report_scope`, `bundle_dir`, run-backed guide asset rules |
| `Отчёт + материалы для подготовки` -> `общие` | “Собрать отчёт и общие материалы без привязки к варианту” | `delivery_profile=study_pack`, `report_scope=build.report_scope`, `guide_mode=general`, `guide_scope=report_scope`, `output_format=bundle_dir` | `папка-комплект` | `guide_mode`, `bundle_dir`, scheme-only asset policy wording |
| `Только материалы для подготовки` -> `персональные` | “Собрать только персональную методичку по этому варианту” | `delivery_profile=guide_only`, `guide_mode=variant_aware`, `guide_scope=<human scope choice>`, `output_format in {pdf, docx}` | `PDF`, `DOCX` | `guide_only`, `variant_aware`, `source_run_id`, asset-policy detail |
| `Только материалы для подготовки` -> `общие` | “Собрать только общую методичку без привязки к варианту” | `delivery_profile=guide_only`, `guide_mode=general`, `guide_scope=<human scope choice>`, `output_format in {pdf, docx}` | `PDF`, `DOCX` | `guide_only`, `general`, source-context vocabulary, regime-note machinery |
| `Печатный комплект` | “Собрать папку для печати и ручной раздачи отчёта” | `delivery_profile=print_pack`, `report_scope=build.report_scope`, `output_format=bundle_dir` | `папка для печати` | `print_pack`, `bundle_dir`, manifest/asset normalization detail |

## Scope Selection Rules In Human Language
- Для report-bearing scenarios объём работы не спрашивается повторно: система использует already confirmed build scope.
- Для `только материалы для подготовки` объём методички спрашивается human labels:
  - `только задача 1`
  - `только задача 2`
  - `вся работа`
- Если current build physically limits variant-aware guide scope, session должна показать только реально допустимые human choices, а не internal explanation of why options disappeared.

## Output Presentation Rules By Scenario
- `Только итоговый отчёт`: show one primary file.
- `Отчёт + материалы для подготовки`: show one bundle root and short list of what is inside.
- `Только материалы для подготовки`: show one primary file and, if relevant, note that supporting schemes are included.
- `Печатный комплект`: show one bundle root and short note that it includes print-oriented report neighbors.

## Hidden Internal Concepts
- `delivery_profile`
- `guide_mode`
- `guide_scope`
- `output_format`
- `source_run_id`
- `bundle_dir`
- delivery-local manifest normalization
- regime-safety note machinery
