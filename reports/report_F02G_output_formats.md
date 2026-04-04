# Report F02G — Output Format Expansion Freeze

## Scope ID and Name
- Scope ID: `F02G`
- Scope name: `Output Format Expansion Freeze`

## Objective
Заморозить output-format contract и implementation order для formal report, methodical guide и delivery bundles до открытия новых exporters/runtime paths.

## Trusted Inputs Used
- `reports/master_report.md`
- `README.md`
- `reports/report_F02F_manifest_normalization.md`
- `reports/report_F02E_unified_entrypoint.md`
- `reports/report_F02C3_regime_safety.md`
- `docs/delivery/DELIVERY_SURFACE_PLAN.md`
- `docs/delivery/DELIVERY_SURFACE_CONTRACT.md`
- `docs/delivery/DELIVERY_OUTPUT_MATRIX.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `docs/governance/GLOBAL_ROADMAP.md`
- `src/delivery_request.py`
- `src/delivery_session.py`

## Files Created
- `docs/delivery/OUTPUT_FORMAT_PLAN.md`
- `docs/delivery/OUTPUT_FORMAT_CONTRACT.md`
- `reports/report_F02G_output_formats.md`

## Files Updated
- `reports/master_report.md`

## What Was Defined Now
- Зафиксирована отдельная output-format branch поверх уже working delivery surface.
- Разведены:
  - single-surface formats;
  - bundle container format;
  - current baseline vs deferred formats.
- Зафиксировано, что current request field `output_format` сохраняется без redesign.
- Зафиксировано, что multi-artifact profiles остаются `bundle_dir` на top-level, а будущие дополнительные copies живут внутри bundle как internal artifacts.
- Заморожен safe implementation order для format expansion.

## Output-Format Support Summary
- Formal report format family: `pdf`, `docx`.
  - current runtime support: `pdf`
  - deferred: `docx`
- Methodical guide format family: `md`, `pdf`, `docx`.
  - current runtime support: `md`
  - next target: `pdf`
  - deferred: `docx`
- Multi-artifact delivery family:
  - `study_pack -> bundle_dir`
  - `print_pack -> bundle_dir`
  - future extra report/guide copies do not replace `bundle_dir` as top-level format.

## Implementation-Order Recommendation
1. `F02H — Guide PDF Runtime`
2. `F02I — Study Pack Format Enrichment`
3. `F02J — Report DOCX Runtime`
4. `F02K — Guide DOCX Runtime`

Причина такого порядка:
- guide already has Markdown baseline and therefore gives the smallest safe export slice;
- bundle enrichment should reuse that guide PDF result without changing the request model;
- report DOCX is more toolchain-sensitive and should not open first;
- guide DOCX stays last to avoid opening two new conversion families at once.

## Remaining Open Questions
- Конкретный exporter/toolchain intentionally не выбран в F02G.
- Bundle-level inclusion policy for future DOCX copies intentionally не раскрыт beyond the rule “top-level stays `bundle_dir`”.
- `print_pack` remains report-centric; any future guide presence there requires отдельный explicit scope, not implicit format drift.

## Ready for Implementation Pass?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02H — Guide PDF Runtime`.
- Ограничить его только runtime support для `guide_only + variant_aware + pdf` и `guide_only + general + pdf`, плюс narrow unified-session exposure of `pdf` only for `guide_only`, без `docx`, без redesign delivery model и без reopening solver/report/methodical truth.
