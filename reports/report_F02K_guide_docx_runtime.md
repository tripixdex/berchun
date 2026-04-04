# Report F02K — Guide DOCX Runtime

## Scope ID and Name
- Scope ID: `F02K`
- Scope name: `Guide DOCX Runtime`

## Objective
Добавить narrow runtime support только для `guide_only + variant_aware + docx` и `guide_only + general + docx` поверх frozen guide baselines без открытия bundle DOCX copies, study_pack/print_pack enrichment или redesign delivery model.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_F02G_output_formats.md`
- `reports/report_F02H_guide_pdf_runtime.md`
- `reports/report_F02I_study_pack_enrichment.md`
- `reports/report_F02J_report_docx_runtime.md`
- `docs/delivery/OUTPUT_FORMAT_PLAN.md`
- `docs/delivery/OUTPUT_FORMAT_CONTRACT.md`
- `README.md`
- `src/delivery_guide_outputs.py`
- `src/delivery_request.py`
- `src/delivery_session.py`
- current guide delivery/runtime baselines
- current unified entrypoint behavior

## Files Created
- `src/delivery_guide_docx.py`
- `tests/test_delivery_guide_docx_runtime.py`
- `tests/test_unified_entrypoint_guide_docx.py`
- `reports/report_F02K_guide_docx_runtime.md`

## Files Updated
- `src/delivery_guide_outputs.py`
- `src/delivery_request.py`
- `src/delivery_session.py`
- `tests/test_delivery_validation.py`
- `tests/test_unified_entrypoint.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- `guide_only + docx` теперь реально поддерживается в delivery runtime.
- Guide DOCX строится из тех же frozen Markdown guide baselines, что уже использовались для `guide_only + md` и `guide_only + pdf`.
- Добавлен отдельный narrow exporter `src/delivery_guide_docx.py`, который использует local `pandoc` и не открывает новый truth-bearing authoring surface.
- Unified session теперь показывает `docx` только для `guide_only`; `report_only`, `study_pack` и `print_pack` не получили новых format choices.
- Bundle semantics не менялись: `study_pack` и `print_pack` по-прежнему остаются без DOCX copies.

## What Guide DOCX Combinations Work Now
- `guide_only + variant_aware + docx`
- `guide_only + general + docx`

Validation actually run:
- `python3 -m py_compile src/delivery_guide_docx.py src/delivery_guide_outputs.py src/delivery_request.py src/delivery_session.py tests/test_delivery_guide_docx_runtime.py tests/test_unified_entrypoint.py tests/test_unified_entrypoint_guide_docx.py tests/test_delivery_validation.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_runtime tests.test_delivery_general_runtime tests.test_delivery_guide_pdf_runtime tests.test_delivery_guide_docx_runtime tests.test_delivery_report_docx_runtime tests.test_delivery_validation tests.test_unified_entrypoint tests.test_unified_entrypoint_docx tests.test_unified_entrypoint_guide_docx tests.test_delivery_safety -v`
- real smoke:
  - `python3 -B -m src.cli deliver --delivery-profile guide_only --output-format docx --guide-mode variant_aware --guide-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02k_smoke_variant_docx`
  - `python3 -B -m src.cli deliver --delivery-profile guide_only --output-format docx --guide-mode general --guide-scope full --deliveries-dir /tmp/berchun_f02k_smoke_general_docx`
  - `printf 'confirm\nguide_only\ngeneral\nfull\ndocx\nconfirm\n' | PYTHONDONTWRITEBYTECODE=1 python3 -B -m src.cli build --input inputs/examples/student_example.yaml --review --offer-delivery --runs-dir /tmp/berchun_f02k_unified/runs --deliveries-dir /tmp/berchun_f02k_unified/deliveries --variant-path /tmp/berchun_f02k_unified/workspace/inputs/variant_me.yaml --derived-path /tmp/berchun_f02k_unified/workspace/inputs/derived_parameters.json --out-dir /tmp/berchun_f02k_unified/workspace/out/data --data-dir /tmp/berchun_f02k_unified/workspace/out/data --figures-dir /tmp/berchun_f02k_unified/workspace/figures --manifest-path /tmp/berchun_f02k_unified/workspace/out/artifacts/figure_manifest.json --report-source-path /tmp/berchun_f02k_unified/workspace/report/final_report.tex --report-pdf-path /tmp/berchun_f02k_unified/workspace/report/final_report.pdf --report-assets-manifest-path /tmp/berchun_f02k_unified/workspace/report/assets_manifest.json`
- targeted validator confirmed:
  - generated DOCX files exist and are non-empty;
  - delivery manifests list the expected guide DOCX artifacts;
  - unified session exposes `docx` for `guide_only` and keeps unsupported bundle DOCX combinations closed;
  - generated DOCX files contain `word/document.xml`, and the real unified smoke produced a non-empty `guide/methodical_guide__general.docx`.

## What Intentionally Remains Unsupported
- any DOCX copies inside `study_pack` or `print_pack`
- any top-level bundle-format redesign
- guide DOCX prompts outside `guide_only`
- any reopening of solver/report/methodical truth

## Remaining Risks
- Guide DOCX runtime depends on local `pandoc`; without it export fails clearly.
- Guide DOCX currently follows the frozen Markdown baselines; no separate guide-docx-specific authoring surface exists, by design.
- Repo-wide historical `tests/test_variant_integrity.py` drift remains outside this scope.

## Ready for Z1?
- `YES`

## Exact Recommendation for Next Step
- Repo-local predeclared `Z1` scope не найден.
- Если открывать следующий explicit scope, рекомендован `Z1 — Delivery Surface Freeze Review`.
- Ограничить его только closeout/freeze review для уже открытых delivery slices (`report_only`, `guide_only`, `study_pack`, `print_pack`) и output formats (`pdf`, `md`, `docx`, `bundle_dir`) без нового export redesign и без reopening solver/report/methodical truth.
