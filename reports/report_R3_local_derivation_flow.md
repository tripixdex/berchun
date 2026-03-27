# Scope ID and name
R3 — Reference-Compatible Local Derivation Flow

## Objective
Перестроить только локальный ритм чтения generated report в сторону accepted reference: сделать exposition formulas более дробной, приблизить plots к поддерживающим их формулам и пояснениям, сократить caption family и убрать отдельную страницу `Краткие выводы`, не меняя solver truth, `out/data` artifacts, plot data, title-page family, scheme family и build/archive semantics.

## Trusted inputs used
- `reports/report_R1_reference_diff.md`
- `reports/report_R2_structural_skeleton.md`
- `docs/REFERENCE_COMPAT_CONTRACT.md`
- `reports/master_report.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `references/DZ1.pdf`
- `src/render/content.py`
- `src/render/report_builder.py`
- `src/render/specs.py`
- `src/render/title_page.py`

## Files created
- `src/render/section_flow.py`
- `reports/report_R3_local_derivation_flow.md`

## Files updated
- `src/render/content.py`
- `src/render/report_builder.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/master_report.md`

## What changed now
- Локальный flow секций вынесен в отдельный render-helper `src/render/section_flow.py`, чтобы формулы, краткие пояснения и plots чередовались более reference-like и при этом `report_builder.py` не выходил за hard limit.
- Большие блоки `Вероятности состояний -> Основные метрики -> Результаты -> batch of figures` заменены на меньшие тематические сегменты:
  - `1.1`: сначала `M_зан` и загрузка, затем `P_отк` с threshold-paragraphs;
  - `1.2`: два sweep-family блока (`по m`, затем `по n`) с локальными metric-subblocks вместо общего figure dump;
  - `1.3`, `1.4`, `2.1`: отдельные локальные блоки для занятости, ожидания и queue-related метрик.
- Caption family сокращена и переведена в более учебный reference-like вид:
  - без synthetic `Семейство графиков ... от числа ...`;
  - с короткими формами вида `Вероятность отказа в зависимости от m при различных n`.
- Отдельная страница `Краткие выводы` удалена в соответствии с `docs/REFERENCE_COMPAT_CONTRACT.md`; существенные факты остались внутри локальных section-level paragraphs.
- В `1.2` локальные формулы во втором sweep-family не дублируются display-блоками повторно: сохранён тот же набор формул, но figures и пояснения теперь стоят ближе к соответствующим метрикам.

## What intentionally remained unchanged
- Solver mathematics, `out/data/*.json` truth, figure data, build/archive semantics и canonical raw-input binding не менялись.
- Scheme family из R2 не переделывалась повторно.
- Title-page family из R2 не открывалась повторно.
- Все семантические safeguards сохранены:
  - `1.1` threshold остаётся из текущих validated outputs;
  - `1.3` non-stationary handling остаётся явным;
  - `1.4` сохраняет `epsilon = 1e-12` и текущие residual-bound facts;
  - `2.1` сохраняет arrival-weighted meaning of `waiting_probability`.

## Validation actually run
- `python3 -m compileall src/render`
- `python3 -m src.cli report --variant-path inputs/variant_me.yaml --derived-path inputs/derived_parameters.json --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json --report-year 2026`
- `python3 -m json.tool report/assets_manifest.json >/dev/null`
- локальные `python3 - <<'PY' ... PY` проверки:
  - display-formula blocks сохранились точно: `33` before/after, `formula_sets_equal = True`;
  - plot basename set сохранился `27/27`, scheme asset count остался `5`;
  - `Краткие выводы` отсутствует и в `final_report.tex`, и в rebuilt `final_report.pdf`;
  - page count rebuilt PDF теперь `20`, то есть отдельная final closeout page действительно убрана;
  - в PDF подтверждены новые локальные headings `Семейства по числу мест в очереди.`, `Семейства по числу операторов.`, `Занятые операторы.`, `Вероятность ожидания обслуживания.`.
- визуальная сверка через `fitz` + `view_image`:
  - page 2: distribution block и первая metric group после схемы;
  - page 5: refusal formula и figure идут локально, затем сразу `M_зан` figure;
  - page 19: waiting-probability figure в `2.1` стоит непосредственно перед поясняющим arrival-weighted paragraph.

## What is now closer to the reference
- Ритм чтения стал локальнее: formulas, short explanation text и figures теперь чаще идут как единый учебный блок.
- `1.2` перестал выглядеть как длинный batch dump из 12 figures после общего текста.
- Caption wording стал короче и ближе к reference family.
- Политика conclusion page теперь соответствует frozen contract: отдельной страницы выводов нет.

## What still remains different
- Formula typography и плотность page-level composition всё ещё менее textbook-like, чем в accepted reference.
- Left institutional mark на титуле остаётся typographic, а не official emblem asset.
- Plot visuals остаются current generated family; R3 менял только placement/caption flow, а не сами figure assets.
- Некоторые explanatory paragraphs всё ещё более систематичны и технически аккуратны, чем в accepted reference, а не столь же рукописно-учебны по тону.

## Ready to proceed to R4? YES/NO
YES.

## Exact recommendation for next scope
Открыть `R4 — Reference-Compatible Visual Polish` и ограничить его только оставшимися page-level presentation gaps: formula typography/spacing, final caption polish, pagination density и вопрос official emblem asset на cover page, не трогая solver truth, plot data, scheme semantics и build/archive behavior.
