# Scope ID and name
R2 — Reference-Compatible Structural Skeleton

## Objective
Сдвинуть generated report к accepted reference family только на уровне structural shell: изменить family титульного листа, видимую иерархию задач/пунктов, формат condition blocks и семейство расчётных схем, не меняя solver truth, `out/data` artifacts, figure data и archive semantics.

## Trusted inputs used
- `reports/report_R1_reference_diff.md`
- `docs/report/REFERENCE_COMPAT_CONTRACT.md`
- `reports/master_report.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `references/DZ1.pdf`
- `src/render/content.py`
- `src/render/report_builder.py`
- `src/render/specs.py`
- `src/render/schemes.py`

## Files created
- `src/render/title_page.py`
- `reports/report_R2_structural_skeleton.md`

## Files updated
- `src/render/common.py`
- `src/render/content.py`
- `src/render/report_builder.py`
- `src/render/specs.py`
- `src/render/schemes.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What changed now
- Титульный лист переведён в более reference-like family: добавлен левый institutional mark, горизонтальный separator rule, year-only footer и убрана строка variant-data с cover page.
- Видимая иерархия задачи 1 перестроена из template-like `1.1/1.2/1.3/1.4` в numbered assignment items `1.`, `2.`, `3.`, `4.`; задача 2 теперь начинается сразу с task statement после заголовка `Задача №2. ...`.
- Condition formatting переведён на assignment-style wording и plain-line `Исходные данные:` block вместо bullet-list input blocks.
- Расчётные схемы полностью перерисованы в state-transition / Markov-chain family и теперь показывают состояния и интенсивности переходов вместо process/block diagram family.
- Подписи plot figures и сами data-driven figures не менялись; changed only scheme PNG assets and local TeX structure around them.

## What intentionally remained unchanged
- Solver mathematics, `out/data/*.json` truth и derived parameter chain не менялись.
- Displayed formula blocks оставлены теми же по составу и порядку; R2 не открывал derivation rewrite.
- Plot PNG data и их набор не менялись; R2 не открывал figure-placement/caption redesign beyond the structural shell.
- Семантические safeguards из frozen contract сохранены: `1.1` threshold остаётся из current outputs, `1.3` non-stationary handling сохранён, `1.4` truncation truth не ослаблена, `2.1` waiting-probability interpretation не ослаблена.
- Extra final conclusion page пока сохранена, потому что её removal отложен в следующий pass по frozen contract.

## Validation actually run
- `python3 -m compileall src/render`
- `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
- локальные `python3 - <<'PY' ... PY` проверки:
  - `includegraphics` count сохранился `32`, plot basename set сохранился `27/27`;
  - display-math blocks сохранились без изменения: `33` before/after, `formula_blocks_exact_match = True`;
  - в новом TeX подтверждены `\section*{Задача №1. ...}`, `\section*{Задача №2. ...}`, visible labels `1./2./3./4.` и plain-line `Исходные данные:`;
  - из rebuilt PDF подтверждены year-only footer, отсутствие `Индивидуальные данные варианта` и отсутствие `Москва, ...` на cover page;
  - `report/assets_manifest.json` остался валидным и указывает на `27` plot inputs и `5` rebuilt scheme assets.
- визуальная сверка page render через `fitz` + `view_image`:
  - page 1: new title-page family with left mark and separator rule;
  - page 2: task 1 intro + item `1.` + state-based scheme;
  - task 2 opening page: task-level heading without visible `2.1` subsection header and state-based finite-source scheme.

## What is now closer to the reference
- cover page hierarchy and footer policy;
- task-level visible structure;
- assignment-style condition wording;
- plain-line raw-data presentation;
- state-based scheme family directly under the condition block.

## What still remains for future passes
- formula exposition is still denser and more block-based than in the accepted reference;
- plot figures are still batched more systematically than in the reference and captions remain current-family rather than fully reference-local;
- the extra `Краткие выводы` page still exists;
- the left cover mark is a deterministic typographic institutional mark, not an official raster emblem from the accepted reference.

## Ready to proceed to R3? YES/NO
YES.

## Exact recommendation for next scope
Открыть `R3 — Reference-Compatible Local Derivation Flow`, ограничив его только restaging formulas/results flow toward the accepted reference: более локальная interleaving of derivation text and figures, figure/caption family refit и решение по final conclusion page. Solver truth, figure data and archive/build semantics по-прежнему не трогать.
