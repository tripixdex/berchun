# Report G1A — User-Facing Surface De-internalization

## Scope ID and name
- `G1A — User-Facing Surface De-internalization`

## Objective
- Убрать из user-facing methodical guide ссылки на внутренние repository/runtime/artifact paths.
- Заменить их на black-box wording про текущий вариант, расчётные данные, текущий отчёт и построенные графики.
- Не менять numbers, formulas, checkpoints, defense logic или structure.

## Files created
- `reports/report_G1A_deinternalization.md`

## Files updated
- `docs/METHODICAL_GUIDE.md`
- `deliveries/20260330T223443431128Z__study_pack__full/guide/methodical_guide__variant.md`
- `deliveries/20260330T223443431128Z__study_pack__full/guide/methodical_guide__variant.pdf`
- `reports/master_report.md`

## What internal leaks were removed
- Удалена repository-style provenance line с `inputs/variant_me.yaml`, `inputs/derived_parameters.json`, `out/data/task_*.json`, `out/artifacts/figure_manifest.json`.
- Удалены локальные checkpoint references на `out/data/task_1_1.json`, `out/data/task_1_3.json`, `out/data/task_2_1.json`.
- Убрана внутренняя procedural ссылка на `M1` как на источник выбора опорных точек.

## What wording replaced them
- Вместо path-like provenance теперь используется black-box wording:
  - `из расчётов для текущего варианта`
  - `из итоговых расчётных данных`
  - `из построенных графиков`
  - `из текущего формального отчёта`
- Вместо file-based checkpoint references теперь используются wording-level references:
  - `по итоговым расчётным данным для текущего варианта`
  - `по итоговым расчётным данным`
  - `опорные точки, выбранные для короткого разбора по текущим расчётным данным`

## What intentionally remained unchanged
- Все числа.
- Все formulas.
- Все artifact-derived checkpoints.
- Вся defense logic, graph logic, contrast guards, compression cues и stop-line layer.
- Вся section/subsection structure и порядок guide.
- Runtime/design of delivery surface, exporter logic and README.

## Remaining risks
- General guide source уже был clean и отдельного вмешательства не потребовал; pass был намеренно сосредоточен на variant-aware user surface.
- В delivery bundle сейчас синхронизирован только текущий visible study-pack guide artifact; other future bundles будут получать clean wording уже из обновлённого source.
- Pass deliberately не открывал figure embedding, compression или broader UX work.

## Ready for G2? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `G2 — Guide PDF Embedded Figure Surface Pass`.
- Держать его narrow: работать только с controlled embedding/presentation of already existing guide schemes/plots inside guide PDF, без изменения numbers, formulas, checkpoints, guide structure или delivery semantics.
