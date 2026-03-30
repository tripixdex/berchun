# Report Z1 — Delivery Surface Freeze Review

## Scope ID and Name
- Scope ID: `Z1`
- Scope name: `Delivery Surface Freeze Review`

## Objective
Провести узкий финальный freeze-review уже открытого delivery surface и вынести честный verdict: готов ли он сейчас к практическому operator use без открытия новых features.

## Trusted Inputs Used
- `reports/master_report.md`
- `README.md`
- `reports/report_F02F_manifest_normalization.md`
- `reports/report_F02G_output_formats.md`
- `reports/report_F02H_guide_pdf_runtime.md`
- `reports/report_F02I_study_pack_enrichment.md`
- `reports/report_F02J_report_docx_runtime.md`
- `reports/report_F02K_guide_docx_runtime.md`
- current delivery/runtime files
- current unified entrypoint behavior

## Files Created
- `reports/report_Z1_delivery_freeze_review.md`

## Files Updated
- `reports/master_report.md`

## What Was Validated
- README-supported delivery surface was checked against current runtime behavior.
- Fresh temp `build` was executed, then all currently supported delivery slices were exercised against that successful run when required:
  - `report_only + pdf`
  - `report_only + docx`
  - `guide_only + variant_aware + md`
  - `guide_only + variant_aware + pdf`
  - `guide_only + variant_aware + docx`
  - `guide_only + general + md`
  - `guide_only + general + pdf`
  - `guide_only + general + docx`
  - `study_pack + bundle_dir + variant_aware`
  - `study_pack + bundle_dir + general`
  - `print_pack + bundle_dir`
- For report-bearing bundles, copied `report/assets_manifest.json` was verified to stay delivery-local and not leak `runs/...` paths.
- For `general` guide deliveries, absence of `guide/assets/plots/...` was verified.
- Unified `build --offer-delivery` was checked on:
  - `none`
  - `guide_only + general + docx`
- Unsupported combinations were checked to fail clearly:
  - `study_pack + docx`
  - `print_pack + docx`
  - `guide_only + general` with `source_run_id`
- Focused delivery/unified/safety test suite was re-run end-to-end.

## What Was Corrected, If Anything
- No code or README correction was required.
- Freeze-review found no genuine inconsistency that needed a narrow runtime fix.

## Supported-surface Summary
- Single-surface report delivery:
  - `report_only + pdf`
  - `report_only + docx`
- Single-surface guide delivery:
  - `guide_only + variant_aware + md/pdf/docx`
  - `guide_only + general + md/pdf/docx`
- Bundle delivery:
  - `study_pack + bundle_dir + variant_aware`
  - `study_pack + bundle_dir + general`
  - `print_pack + bundle_dir`
- Unified operator flow:
  - `build --offer-delivery` keeps build and delivery semantics separate
  - supported choices stay explicit
  - false format/profile availability was not observed in review

## Remaining Risks
- Delivery surface is practically usable, but some explicit non-blocking limits remain:
  - bundle-local DOCX copies are still not implemented;
  - `print_pack` remains report-centric;
  - guide PDF depends on local `pandoc + xelatex`;
  - report DOCX and guide DOCX depend on local `pandoc`;
  - repo-wide `tests/test_variant_integrity.py` historical drift remains outside the delivery surface and outside this scope.

## Final Verdict: Ready for Practical Use?
- `YES`

## Exact Recommendation for Next Step
- No mandatory next scope is required for the currently opened delivery surface.
- Keep the delivery surface frozen at the current supported slice for practical use now.
- If later expansion is actually needed, open a new explicit narrow scope rather than reopening `Z1`; the most natural follow-up candidate would be bundle-local DOCX copies, but only on explicit demand.
