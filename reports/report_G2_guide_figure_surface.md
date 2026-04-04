# Report G2 — Guide PDF Embedded Figure Surface Pass

## Scope ID and name
- `G2 — Guide PDF Embedded Figure Surface Pass`

## Objective
- Сделать guide PDF менее тексто-нагруженным и более удобным для слабого студента.
- Встроить только уже существующие схемы и ключевые plots в guide PDF.
- Не менять numbers, formulas, checkpoints, structure или delivery semantics.

## Files created
- `reports/report_G2_guide_figure_surface.md`

## Files updated
- `src/delivery_guide_pdf_surface.py`
- `src/delivery_guide_outputs.py`
- `src/delivery_population.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `deliveries/20260330T225118192318Z__study_pack__full/guide/methodical_guide__variant.pdf`
- `reports/master_report.md`

## What visuals were embedded
- Для всех guide PDF surfaces:
  - `task1_1__scheme.png`
  - `task1_2__scheme.png`
  - `task1_3__scheme.png`
  - `task1_4__scheme.png`
  - `task2_1__scheme.png`
- Для `variant_aware` guide PDF дополнительно встроены только опорные plots:
  - `task1_1__refusal_and_utilization_vs_operators.png`
  - `task1_2__refusal_vs_operators__family_by_queue.png`
  - `task1_3__queue_length_vs_operators.png`
  - `task1_4__queue_length_vs_operators.png`
  - `task2_1__waiting_probability_vs_repairers.png`

## Where they were embedded
- Каждая схема вставляется сразу после `#### Схема и состояния` в соответствующем подпункте.
- Опорные plots вставляются только в уже существующие graph-reading blocks:
  - `1.1` — после `#### Как читать совмещённый график отказа и загрузки`
  - `1.2` — после `#### Блок "Семейства по числу операторов при фиксированном m"`
  - `1.3` — после `#### Блок "Очередь"`
  - `1.4` — после `#### Блок "Очередь и уход клиентов"`
  - `2.1` — после `#### Блок "Вероятность ожидания нового отказа"`

## Why those placements were chosen
- Схема рядом с вводом модели помогает студенту быстро восстановить смысл состояний.
- Один опорный plot на подпункт помогает показать, на какой кривой безопасно строить устный ответ.
- Выбранные placements поддерживают существующий guide flow и не превращают guide в дубликат formal report.
- В `general` режиме встроены только схемы, потому что run-specific plots в этом surface intentionally не допускаются.

## What intentionally remained unchanged
- `docs/methodical/content/METHODICAL_GUIDE.md`
- Все numbers, formulas, checkpoints и defense logic.
- Вся section/subsection order.
- Все figure files и их data source.
- README, delivery request model, manifest model и bundle semantics.
- Markdown and DOCX guide surfaces остались без figure embedding в этом pass.

## Remaining risks
- PDF embedding сделан через narrow markdown-image surface без отдельного layout microfit; spacing и page-break behavior остаются acceptable, но не fine-polished.
- `general` guide PDF получает только schemes; visual support там intentionally легче, чем в `variant_aware`.
- Pass intentionally не трогал DOCX/MD guide surfaces и не открывал broader export redesign.

## Ready for G3? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `G3 — Guide PDF Layout Microfit`.
- Держать его narrow: локально отполировать только spacing, page breaks и visual balance вокруг уже встроенных схем/plots в guide PDF, без изменения numbers, formulas, checkpoints, guide structure или delivery semantics.
