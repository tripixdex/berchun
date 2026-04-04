# Report F02I — Study Pack Format Enrichment

## Scope ID and Name
- Scope ID: `F02I`
- Scope name: `Study Pack Format Enrichment`

## Objective
Добавить guide PDF как internal artifact внутрь `study_pack` без изменения top-level `output_format = bundle_dir`, без изменений `print_pack`, `docx` или delivery model.

## Trusted Inputs Used
- `reports/master_report.md`
- `reports/report_F02H_guide_pdf_runtime.md`
- `reports/report_F02G_output_formats.md`
- `docs/delivery/OUTPUT_FORMAT_PLAN.md`
- `docs/delivery/OUTPUT_FORMAT_CONTRACT.md`
- `README.md`
- `src/delivery_population.py`
- `src/delivery_guide_pdf.py`
- current `study_pack` behavior
- current guide PDF runtime path

## Files Created
- `src/delivery_guide_outputs.py`
- `reports/report_F02I_study_pack_enrichment.md`

## Files Updated
- `src/delivery_population.py`
- `tests/test_delivery_runtime.py`
- `tests/test_delivery_general_runtime.py`
- `README.md`
- `reports/master_report.md`

## What Was Implemented Now
- `study_pack + bundle_dir + variant_aware` теперь кладёт внутрь bundle не только `guide/methodical_guide__variant.md`, но и `guide/methodical_guide__variant.pdf`.
- `study_pack + bundle_dir + general` теперь кладёт внутрь bundle не только `guide/methodical_guide__general.md`, но и `guide/methodical_guide__general.pdf`.
- PDF строится через уже существующий exporter из `F02H`; новая truth-bearing authoring surface не открывалась.
- Для соблюдения size hygiene новый helper вынесен в маленький support module `src/delivery_guide_outputs.py`, а orchestration в `src/delivery_population.py` осталась узкой.
- Top-level request model не менялся: `study_pack` по-прежнему требует только `output_format = bundle_dir`.

## What Study_Pack Contains Now
- `delivery_manifest.json`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- guide Markdown:
  - `guide/methodical_guide__variant.md` или `guide/methodical_guide__general.md`
- guide PDF:
  - `guide/methodical_guide__variant.pdf` или `guide/methodical_guide__general.pdf`
- scope-aware guide schemes
- scope-aware guide plots только для `variant_aware`

Validation actually run:
- `python3 -m py_compile src/delivery_population.py src/delivery_guide_outputs.py tests/test_delivery_runtime.py tests/test_delivery_general_runtime.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_runtime tests.test_delivery_general_runtime tests.test_delivery_guide_pdf_runtime tests.test_delivery_validation -v`
- real smoke:
  - `python3 -B -m src.cli deliver --delivery-profile study_pack --output-format bundle_dir --report-scope full --guide-mode variant_aware --guide-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02i_smoke_variant`
  - `python3 -B -m src.cli deliver --delivery-profile study_pack --output-format bundle_dir --report-scope full --guide-mode general --guide-scope full --source-run-id 20260329T172832610175Z__3a359fd0383d --deliveries-dir /tmp/berchun_f02i_smoke_general`
- targeted validator confirmed:
  - both bundles contain guide Markdown + guide PDF;
  - guide PDFs are non-empty;
  - normalized `report/assets_manifest.json` still points only to delivery-local files;
  - `study_pack/general` still contains no guide plots.

## What Intentionally Remains Unsupported
- any change to top-level `study_pack` format (`bundle_dir` stays mandatory)
- any `print_pack` enrichment
- `docx`
- guide PDF copies outside `study_pack` and already implemented `guide_only`
- delivery-model redesign or new bundle prompts

## Remaining Risks
- Study-pack guide PDF still depends on local `pandoc + xelatex`; without toolchain export fails clearly.
- No guide-level asset manifest exists yet; only `delivery_manifest.json` and normalized report manifest are present inside the bundle.
- Repo-wide historical `tests/test_variant_integrity.py` drift remains outside this scope.

## Ready for F02J?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02J — Report DOCX Runtime`.
- Ограничить его только `report_only + docx` поверх уже frozen report baseline и narrow unified-session exposure для `report_only`, без `guide docx`, без bundle enrichment и без reopening solver/report/methodical truth.
