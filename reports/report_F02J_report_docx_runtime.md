# Report F02J — Report DOCX Runtime

## Scope ID and Name
- Scope ID: `F02J`
- Scope name: `Report DOCX Runtime`

## Objective
Добавить narrow runtime support только для `report_only + docx` поверх frozen formal report baseline без открытия guide DOCX, bundle enrichment или redesign delivery model.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_F02G_output_formats.md`
- `reports/report_F02H_guide_pdf_runtime.md`
- `reports/report_F02I_study_pack_enrichment.md`
- `docs/delivery/OUTPUT_FORMAT_PLAN.md`
- `docs/delivery/OUTPUT_FORMAT_CONTRACT.md`
- `README.md`
- `src/delivery_request.py`
- `src/delivery_population.py`
- `src/delivery_manifest_normalization.py`
- `src/delivery_session.py`
- current formal report delivery/runtime baseline
- current unified entrypoint behavior

## Files Created
- `src/delivery_report_docx.py`
- `src/delivery_report_outputs.py`
- `tests/test_delivery_report_docx_runtime.py`
- `tests/test_unified_entrypoint_docx.py`
- `reports/report_F02J_report_docx_runtime.md`

## Files Updated
- `src/delivery_population.py`
- `src/delivery_manifest_normalization.py`
- `src/delivery_request.py`
- `src/delivery_session.py`
- `src/cli.py`
- `tests/test_delivery_manifest_normalization.py`
- `tests/test_delivery_validation.py`
- `tests/test_unified_entrypoint.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- `report_only + docx` теперь реально поддерживается в delivery runtime.
- Report DOCX строится из frozen `final_report.tex` через local `pandoc`.
- Для safe conversion добавлен только narrow deterministic preprocessing layer: перед export снимается `\detokenize{...}` у image paths, чтобы `pandoc` корректно встроил assets и figures.
- Новый delivery-local `report/assets_manifest.json` теперь умеет truthfully описывать DOCX-only bundle через `report_docx_path`, без утечки `runs/...` references.
- Unified session теперь показывает `docx` только для `report_only`; остальные profiles не получили новых format choices.

## What Report DOCX Combinations Work Now
- `report_only + docx`

Validation actually run:
- `python3 -m py_compile src/delivery_population.py src/delivery_manifest_normalization.py src/delivery_report_docx.py src/delivery_report_outputs.py src/delivery_session.py src/delivery_request.py tests/test_delivery_report_docx_runtime.py tests/test_unified_entrypoint.py tests/test_unified_entrypoint_docx.py tests/test_delivery_manifest_normalization.py tests/test_delivery_validation.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_runtime tests.test_delivery_report_docx_runtime tests.test_delivery_manifest_normalization tests.test_delivery_validation tests.test_unified_entrypoint tests.test_unified_entrypoint_docx -v`
- real smoke:
  - `python3 -B -m src.cli deliver --delivery-profile report_only --output-format docx --report-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02j_smoke_report_docx`
- targeted validator confirmed:
  - DOCX exists and is non-empty;
  - delivery manifest lists `report/final_report.docx`;
  - normalized report manifest uses `report_docx_path` and keeps no `runs/...` references;
  - generated DOCX embeds report media (`33` entries under `word/media/`).

## What Intentionally Remains Unsupported
- `guide_only + docx`
- any DOCX copies inside `study_pack` or `print_pack`
- any top-level bundle-format redesign
- guide DOCX or bundle DOCX prompts in unified session

## Remaining Risks
- Report DOCX runtime depends on local `pandoc`; without it export fails clearly.
- The preprocessing layer is intentionally narrow: it only normalizes `\detokenize{...}` around image paths and does not open broad TeX-to-DOCX rewrite logic.
- Repo-wide historical `tests/test_variant_integrity.py` drift remains outside this scope.

## Ready for F02K?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02K — Guide DOCX Runtime`.
- Ограничить его только `guide_only + variant_aware + docx` и `guide_only + general + docx`, плюс narrow unified-session exposure of `docx` only for `guide_only`, без bundle enrichment и без reopening solver/report/methodical truth.
