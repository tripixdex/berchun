# Scope ID and name
R4 — Reference-Compatible Visual Polish

## Objective
Закрыть только оставшиеся page-level presentation gaps между generated report и accepted reference: улучшить formula typography/spacing, polish captions, сделать page rhythm менее template-like и, где это возможно без хаков, заменить титульную заглушку на более официальный emblem treatment, не меняя solver truth, `out/data` truth, plot data, scheme semantics и pipeline behavior.

## Trusted inputs used
- `reports/report_R1_reference_diff.md`
- `reports/report_R2_structural_skeleton.md`
- `reports/report_R3_local_derivation_flow.md`
- `docs/report/REFERENCE_COMPAT_CONTRACT.md`
- `reports/master_report.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `references/DZ1.pdf`
- `references/DZ1.docx`
- `src/render/common.py`
- `src/render/content.py`
- `src/render/title_page.py`
- `src/render/section_flow.py`
- `src/render/report_builder.py`

## Files created
- `src/render/assets/bmstu_emblem.jpeg`
- `reports/report_R4_visual_polish.md`

## Files updated
- `src/render/content.py`
- `src/render/title_page.py`
- `src/render/section_flow.py`
- `src/render/report_builder.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What changed now
- На титульном листе типографическая boxed-заглушка заменена на реальный emblem asset, извлечённый из `references/DZ1.docx` и детерминированно подключаемый в report build как `assets/title_emblem.jpeg`.
- В TeX preamble добавлена узкая типографическая полировка:
  - `\\raggedbottom`;
  - более плотные и устойчивые `\\abovedisplayskip`, `\\belowdisplayskip`, `\\textfloatsep`, `\\floatsep`, `\\intextsep`;
  - меньший `\\parskip`;
  - более аккуратный `\\captionsetup` для centred educational captions.
- Visual rhythm внутри секций сглажен без изменения R3 flow:
  - тематические lead-in headings теперь подаются inline bold line, а не как более тяжёлые paragraph-block headings;
  - `PLOT_WIDTH` уменьшен до `0.8\\textwidth`, чтобы страницы выглядели ближе к reference family и не казались чрезмерно заполненными.
- Caption family дополнительно сокращена:
  - `в зависимости от ...` заменено на более короткое `при изменении ...`;
  - семейства `1.2` теперь подписаны как `... при изменении m и разных n` / `... при изменении n и разных m`.
- В `report/assets_manifest.json` добавлен отдельный `title_assets_used` entry для title emblem; scheme count и plot count при этом не изменились.

## What intentionally remained unchanged
- Все validated formulas и вся solver mathematics остались прежними.
- `out/data/*.json`, plot PNG data и scheme semantics не менялись.
- R2 skeleton changes и R3 local-flow changes сохранены: numbered task items, state-based schemes, local figure placement и отсутствие отдельной страницы `Краткие выводы`.
- Никаких изменений в build/intake/archive behavior не вносилось.

## Validation actually run
- `python3 -m compileall src/render`
- `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
- `python3 -m json.tool report/assets_manifest.json >/dev/null`
- локальные `python3 - <<'PY' ... PY` проверки:
  - display-formula blocks сохранены точно: `33` before/after, `formula_sets_equal = True`;
  - plot basename set сохранён `27/27`;
  - scheme count остался `5`;
  - `title_assets_used` теперь содержит ровно `1` asset;
  - typographic placeholder `\\fbox` исчез из rebuilt TeX;
  - `title_emblem.jpeg` реально используется в rebuilt TeX;
  - separate conclusion page по-прежнему отсутствует;
  - R3 local-family headings по-прежнему присутствуют.
- визуальная сверка через `fitz` + `view_image`:
  - page 1: actual emblem on cover, closer to accepted reference;
  - page 2: formula blocks выглядят менее template-like за счёт inline bold lead-ins;
  - page 5 и page 19: captions и figure rhythm стали компактнее и естественнее без drift of content.

## What is now closer to the reference
- Cover page теперь использует реальный institutional emblem вместо typographic placeholder.
- Формульные блоки читаются более textbook-like за счёт мягкой spacing-tuning и менее тяжёлых block headings.
- Captions стали короче, естественнее и меньше напоминают machine-generated wording.
- Page-level visual rhythm стал спокойнее: больше воздуха вокруг plots и меньше ощущения жёсткого templated layout.

## What still remains different
- Plot visuals как family по-прежнему остаются generated, а не reference-like по стилю линий, легенд и overall chart skin.
- Page count всё ещё короче reference PDF; R4 улучшал rhythm, но не пытался искусственно растянуть документ.
- Derivation prose остаётся более систематизированной и технически аккуратной, чем в accepted reference.
- Title emblem теперь официальный-looking, но это всё равно raster asset из reference docx, а не отдельный institutional vector package.

## Ready to proceed to R5? YES/NO
YES.

## Exact recommendation for next scope
Открыть `R5 — Reference-Compatible Plot Skin + Final Microfit` и ограничить его только visual style of existing data-driven plots и остаточной prose/caption micro-polish, не меняя plot data, solver truth, schemes, structure или pipeline behavior.
