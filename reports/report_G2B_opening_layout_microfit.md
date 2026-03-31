# Report G2B — Guide Opening Compression + Navigation + Layout Microfit

## Scope ID and name
- `G2B — Guide Opening Compression + Navigation + Layout Microfit`

## Objective
- Сделать opening/front matter guide короче и спокойнее для слабого студента.
- Добавить только минимальную navigation help перед основным methodical body.
- Локально отполировать guide PDF surface вокруг уже встроенных schemes/plots без изменения truth-bearing content.

## Files created
- `reports/report_G2B_opening_layout_microfit.md`

## Files updated
- `docs/METHODICAL_GUIDE.md`
- `src/delivery_guide_pdf.py`
- `src/delivery_guide_pdf_surface.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `deliveries/20260330T235413154621Z__study_pack__full/guide/methodical_guide__variant.md`
- `deliveries/20260330T235413154621Z__study_pack__full/guide/methodical_guide__variant.pdf`
- `reports/master_report.md`

## What opening text was compressed
- Верхний intro block сокращён до трёх коротких мыслей:
  - сначала восстановить teacher framing,
  - затем перейти к объяснениям и опорным графикам,
  - помнить, что guide нужен для понимания и защиты, а formal report — для сдачи.
- В teacher-first blocks для задач `1` и `2` укорочены только service phrases:
  - `Из этих исходных данных получаются` -> `Для расчёта сразу используем`
  - `Здесь полезно сразу держать в голове смысл обозначений` / `Здесь обозначения такие` -> `Коротко про обозначения`
  - task framing sentences сделаны короче, но teacher-origin logic и все current-variant values сохранены.

## What navigation help was changed
- Блок `Как этим руководством пользоваться дальше` сжат до одного short route:
  - сначала посмотреть постановку и свои числа,
  - потом открыть нужный подпункт,
  - на защите идти по цепочке `checkpoint -> схема/график -> короткий локальный вывод`.
- Navigation help осталась минимальной и не превратилась в новый navigation subsystem.

## What layout microfit was applied
- PDF body теперь начинает main methodical section `## Задача 1...` с explicit clean page break.
- Already embedded schemes/plots оставлены на тех же section-local positions, но теперь вставляются через pandoc-native image sizing instead of full-width default placement.
- Applied local sizing policy:
  - schemes: `80%`
  - key plots: `90%`
- Caption rhythm оставлен прежним по смыслу, но visual placement стал спокойнее за счёт меньшей ширины и более предсказуемого page flow.
- PDF surface builder дополнительно покрыт узким test на page break + scaled figure markup.

## What intentionally remained unchanged
- Все numbers.
- Все formulas.
- Все checkpoints.
- Весь downstream guide body после `## Как читать схемы, обозначения, формулы и графики`.
- Все figure files и их data.
- Все defense / graph / contrast / compression / stop-line layers.
- Delivery model, bundle semantics и broader export architecture.

## Remaining risks
- `general` guide opening intentionally не переводился на teacher-first frame в этом pass; `G2B` работал только с current variant-aware baseline opening and shared PDF presentation layer.
- Layout microfit остаётся local and conservative: он не открывает full typography/layout redesign и не решает every page-balance nuance.
- Visible artifact sync выполнен только для current variant-aware study-pack guide, а не для historical deliveries sweep.
- `tests/test_delivery_guide_pdf_runtime.py` после narrow additions остаётся чуть выше soft size target (`157` lines), но below hard limit; отдельный test split ради `G2B` intentionally не открывался.

## Ready for G3? YES/NO
- `YES`

## Exact recommendation for next step
- Open `G3 — Guide PDF Layout Microfit`.
- Keep it narrow: polish only spacing, page breaks, local visual balance and caption pacing around the already embedded schemes/plots across the guide PDF, without changing numbers, formulas, checkpoints, guide logic or delivery semantics.
