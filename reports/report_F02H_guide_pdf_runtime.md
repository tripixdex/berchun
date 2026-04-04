# Report F02H — Guide PDF Runtime

## Scope ID and Name
- Scope ID: `F02H`
- Scope name: `Guide PDF Runtime`

## Objective
Добавить narrow runtime support для `guide_only + pdf` поверх уже frozen guide baselines, без открытия bundle enrichment, DOCX или redesign delivery model.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_F02G_output_formats.md`
- `docs/delivery/OUTPUT_FORMAT_PLAN.md`
- `docs/delivery/OUTPUT_FORMAT_CONTRACT.md`
- `README.md`
- `src/delivery_population.py`
- `src/delivery_request.py`
- `src/delivery_session.py`
- current guide delivery baselines
- current unified entrypoint behavior

## Files Created
- `src/delivery_guide_pdf.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `reports/report_F02H_guide_pdf_runtime.md`

## Files Updated
- `src/delivery_population.py`
- `src/delivery_request.py`
- `src/delivery_session.py`
- `tests/test_delivery_validation.py`
- `tests/test_unified_entrypoint.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- Добавлен explicit exporter `pandoc + xelatex` для guide PDF поверх уже существующего Markdown guide surface.
- `guide_only + variant_aware + pdf` теперь использует тот же frozen variant-aware guide source, что и текущий `guide_only + md`.
- `guide_only + general + pdf` теперь использует тот же explicit general-guide baseline, что и текущий `guide_only + md`.
- Existing guide asset policy сохранена:
  - `variant_aware` PDF delivery продолжает класть scope-aware schemes и plots;
  - `general` PDF delivery продолжает класть scope-aware schemes и не кладёт guide plots.
- `build_delivery_request(...)` теперь разрешает `guide_only` с `output_format = pdf`.
- Unified session теперь показывает `pdf` только для `guide_only`; `report_only`, `study_pack` и `print_pack` не получили новых format choices.
- Bundle profiles intentionally не менялись.

## What Guide PDF Combinations Work Now
- `guide_only + variant_aware + pdf`
- `guide_only + general + pdf`

Validation actually run:
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_runtime tests.test_delivery_general_runtime tests.test_delivery_guide_pdf_runtime tests.test_delivery_validation tests.test_delivery_safety tests.test_unified_entrypoint -v`
- real smoke:
  - `python3 -B -m src.cli deliver --delivery-profile guide_only --output-format pdf --guide-mode general --guide-scope full --deliveries-dir /tmp/berchun_f02h_smoke_general`
  - `python3 -B -m src.cli deliver --delivery-profile guide_only --output-format pdf --guide-mode variant_aware --guide-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02h_smoke_variant`
- targeted validator confirmed both smoke PDFs exist and are non-empty.

## What Intentionally Remains Unsupported
- `report_only + docx`
- `guide_only + docx`
- any new PDF/DOCX copies inside `study_pack`
- any new guide surface inside `print_pack`
- any top-level format redesign for bundle profiles

## Remaining Risks
- Guide PDF runtime now depends on local availability of `pandoc` and `xelatex`; if either tool is missing, delivery fails clearly.
- Guide PDF remains a rendered copy of the existing Markdown baseline, not a new authoring surface.
- Repo-wide `tests/test_variant_integrity.py` historical expectation drift remains outside F02H.

## Ready for F02I?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02I — Study Pack Format Enrichment`.
- Ограничить его только добавлением guide PDF как internal artifact внутри `study_pack` при сохранении `output_format = bundle_dir`, без `docx`, без `print_pack` changes и без reopening solver/report/methodical truth.
