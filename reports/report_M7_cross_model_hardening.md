# Report M7 — Cross-Model Contrast Defense Hardening

## Scope ID and name
- `M7 — Cross-Model Contrast Defense Hardening`

## Objective
- Узко усилить cross-model contrast layer в `docs/METHODICAL_GUIDE.md`.
- Локально заблокировать самые опасные переносы выводов между соседними моделями.
- Не менять числа, formulas, checkpoints, figures, solver truth, report truth и общую структуру guide.

## Files created
- `reports/report_M7_cross_model_hardening.md`

## Files updated
- `docs/METHODICAL_GUIDE.md`
- `reports/master_report.md`

## What was strengthened
- В guide добавлены короткие local contrast bridges формата:
  - `Частая опасная путаница здесь такая: ...`
  - `Безопасно говорить так: ...`
- Усиление сделано только там, где weak student чаще всего смешивает соседние модели и переносит метрики или выводы не в тот подпункт.
- Новые мостики не переписывают theory layer, а лишь локально фиксируют:
  - что именно изменилось в соседней модели;
  - что не осталось прежним;
  - какие похожие по названию метрики нельзя механически смешивать;
  - какой safe oral contrast надо уметь произнести.

## Which contrast areas changed
- `1.1` vs `1.2`:
  - явно зафиксировано, что в `1.1` очереди нет совсем;
  - запрещён перенос ожидания и queue-metrics из `1.2` в модель без очереди.
- `1.2` vs `1.1` / `1.3`:
  - явно разведены конечный буфер ожидания, мгновенный отказ и бесконечный хвост;
  - зафиксировано, что `1.2` нельзя читать ни как `1.1`, ни как "почти `1.3`".
- `1.3` vs `1.2` / `1.4`:
  - явно разведены конечная очередь против бесконечной очереди;
  - отдельно зафиксировано, что `1.3` не имеет второго канала разгрузки хвоста, который появляется в `1.4`.
- `1.4` vs `1.3`:
  - явно зафиксировано, что уход клиентов меняет сам механизм хвоста, а не только "смягчает числа".
- `2.1` vs queue metrics из задачи 1:
  - явно разведены объект очереди и смысл метрик;
  - зафиксировано, что `P_ож`, `M_ож` и queue-метрики из задачи 1 нельзя смешивать как одну и ту же сущность.

## What intentionally remained unchanged
- Весь section order guide.
- Все числа и artifact-derived checkpoints.
- Все formulas.
- Все figures.
- Все report/data/manifest files.
- Existing formula-defense, graph-defense и defense-card layers как отдельные структуры.
- Любые solver/report/delivery/runtime/UX files не менялись.

## Remaining risks
- Guide стал сильнее именно против cross-model confusion, но ещё не получил отдельный pass на сжатие безопасных oral answers до максимально коротких memory-safe форм.
- Weak student всё ещё может перегружать ответ лишними деталями, даже если теперь лучше различает соседние модели.
- Methodical branch по-прежнему остаётся compact guide, а не full oral exam script.

## Ready for M8? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `M8 — Checkpoint-to-Answer Compression Hardening`.
- Держать его таким же узким:
  - усиливать только места, где safe oral answer надо ужать до одной-двух фраз вокруг одного checkpoint;
  - не менять числа, formulas, figures, data/manifests и общую структуру guide.
