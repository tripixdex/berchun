# Report M6 — Graph-to-Conclusion Defense Hardening

## Scope ID and name
- `M6 — Graph-to-Conclusion Defense Hardening`

## Objective
- Узко усилить graph-to-conclusion oral-defense слой в `docs/methodical/content/METHODICAL_GUIDE.md`.
- Работать только внутри уже существующих graph-reading blocks.
- Не менять числа, formulas, checkpoints, figures, solver truth, report truth и общую структуру guide.

## Files created
- `reports/report_M6_graph_conclusion_hardening.md`

## Files updated
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/master_report.md`

## What was strengthened
- В graph-reading blocks добавлены короткие tactical bridges, которые помогают студенту устно ответить:
  - что меняется по `X`;
  - что читается по `Y`;
  - с какого checkpoint безопаснее начинать объяснение;
  - почему кривая идёт именно так;
  - какой локальный вывод разрешён без overclaim.
- Добавлены короткие oral-safety guards против типичных ошибок:
  - объявить threshold глобальным optimum;
  - перепутать saturation с линейным ростом;
  - смешать probability-curve и average-value curve;
  - перенести вывод одного family на все режимы сразу.

## Which graph-related areas changed
- `1.1`:
  - усилены оба graph blocks;
  - добавлен guard против фразы про "лучшее число операторов вообще".
- `1.2`:
  - усилены family blocks по `m` и по `n`;
  - добавлены guards против смешения "буфер ожидания" и "новый обслуживающий ресурс";
  - добавлен guard против объявления одной пары `(n, m)` универсально лучшей.
- `1.3`:
  - усилены blocks `P_wait`, `M_зан/K_загр`, `P_оч/L_оч`;
  - добавлены cues, что первый безопасный graph checkpoint начинается только в стационарной зоне.
- `1.4`:
  - усилены blocks `M_зан/K_загр` и `P_оч/L_оч`;
  - добавлен guard, что уход клиентов ускоряет спад хвоста, но не делает малое `n` автоматически приемлемым.
- `2.1`:
  - усилены blocks `M_пр/M_ож`, `P_ож`, `M_зан/K_загр`;
  - добавлены cues про first safe checkpoint, saturation и различие между судьбой нового отказа и текущим состоянием очереди.

## What intentionally remained unchanged
- Весь section order guide.
- Все числа и artifact-derived checkpoints.
- Все formulas.
- Все figures.
- Все report/data/manifest files.
- Existing defense-card set как отдельная структура.
- Любые solver/report/delivery/runtime/UX files не менялись.

## Remaining risks
- Guide стал сильнее именно на graph-defense layer, но ещё не закрывает отдельно cross-model confusion между соседними подпунктами.
- Student still needs short rehearsal, потому что локальные oral-safety bridges не заменяют живую устную практику.
- Methodical branch по-прежнему остаётся compact guide, а не full exam-prep encyclopedia.

## Ready for M7? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `M7 — Cross-Model Contrast Defense Hardening`.
- Держать его таким же узким:
  - усиливать только места, где weak student путает соседние модели и режимы;
  - не менять числа, formulas, figures, data/manifests и общую структуру guide.
