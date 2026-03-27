# Scope ID and name
P1 — Human Title Page aligned to accepted reference

## Objective
Улучшить только титульный лист итогового отчёта: сделать его более формальным и ближе к accepted reference family, не меняя solver truth, figure package, структуру остальных разделов и детерминированный autofill из canonical raw inputs.

## Trusted inputs used
- `README.md`
- `reports/master_report.md`
- `report/final_report.tex`
- `report/final_report.pdf`
- `src/render/content.py`
- `src/render/report_builder.py`
- `inputs/variant_me.yaml`
- `report/assets_manifest.json`
- `references/DZ1.pdf`

## Files created
- `reports/report_P1_title_page.md`

## Files updated
- `src/render/content.py`
- `report/final_report.tex`
- `report/final_report.pdf`
- `reports/master_report.md`

## What changed on the title page
- Вместо рабочего минимального титульного листа введена более формальная academic hierarchy, выровненная по accepted reference:
  - institutional heading уровня министерства и университета;
  - отдельные строки факультета и кафедры;
  - центрированный блок названия работы и курса;
  - более аккуратный правый блок со студентом, группой и преподавателем через выровненную таблицу;
  - variant-specific raw data перенесены вниз страницы как вторичный служебный блок, чтобы не ломать главную иерархию;
  - сохранён нижний блок `Москва, 2026 г.`.
- Autofill не возвращён к ручному хардкоду:
  - `student_full_name`, `student_group`, `teacher_full_name` и variant values продолжают подтягиваться из текущего canonical raw input;
  - title-page dynamic values теперь проходят через `latex_escape`, чтобы не ломать TeX при символах со спец-смыслом.

## What intentionally remained unchanged
- Не менялись solver mathematics, figures, manifests contract, body sections отчёта и общий report family вне `titlepage`.
- Не добавлялись новые raw-input fields и не менялся canonical intake/build flow.
- `report/assets_manifest.json` не менялся содержательно; rebuild подтвердил это.
- Не предпринималась попытка сделать пиксельно-официальный institutional template: цель была narrow alignment to the accepted reference family, а не полный визуальный редизайн.

## Validation actually run
- Inspection reads via `rg -n`, `sed -n`, `find`, `wc -l` for:
  - `src/render/content.py`
  - `src/render/report_builder.py`
  - `report/final_report.tex`
  - `inputs/variant_me.yaml`
  - `reports/master_report.md`
- `python3 - <<'PY' ... PY`
  - extracted first-page text from `references/DZ1.pdf` to identify the accepted reference title-page structure.
- `python3 - <<'PY' ... PY`
  - extracted first-page text from the pre-change `report/final_report.pdf` to establish the current baseline.
- `cp report/final_report.tex /tmp/berchun_p1_before_final_report.tex`
- `cp report/assets_manifest.json /tmp/berchun_p1_before_assets_manifest.json`
  - saved pre-change report artifacts for narrow regression comparison.
- `python3 -m src.cli report --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json`
  - succeeded; rebuilt the canonical final report package.
- `python3 -m json.tool report/assets_manifest.json >/dev/null`
  - succeeded.
- `python3 - <<'PY' ... PY`
  - compared `report/final_report.tex` before/after with the `titlepage` block stripped out; result: `BODY_UNCHANGED = True`.
- `python3 - <<'PY' ... PY`
  - compared `report/assets_manifest.json` before/after; result: `MANIFEST_CHANGED = False`.
- `python3 - <<'PY' ... PY`
  - extracted first-page text from the rebuilt `report/final_report.pdf` and verified presence of:
    - ministry heading;
    - `МГТУ им. Н.Э. Баумана`;
    - faculty line;
    - `КАФЕДРА РК-9`;
    - `Гуров Владислав Александрович`;
    - `РК9-84Б`;
    - `Берчун Юрий Валерьевич`;
    - `Москва, 2026 г.`

## Remaining risks
- Similarity to the accepted reference was checked structurally through the reference PDF text and the rebuilt TeX/PDF output, but not through a pixel-perfect visual overlay against the source PDF.
- The title page is still implemented inside the current generic `article`-based report template, so it remains somewhat simpler than a full official university cover template.
- `src/render/content.py` is now exactly at the hard line limit (`180` lines); splitting it further was intentionally avoided here to keep the scope strictly title-page-local.

## Ready to keep as current default title page? YES/NO
YES

## Exact recommendation for next scope
Нового обязательного scope нет; сохранить этот title page как текущий default и открывать следующий post-closeout pass только по отдельному explicit request, если потребуется ещё более точное visual alignment to the institutional reference without изменения solver/report body.
