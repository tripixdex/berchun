# Report M9 — Answer Stop-Line Hardening

## Scope ID and name
- `M9 — Answer Stop-Line Hardening`

## Objective
- Узко усилить stop-line layer в `docs/methodical/content/METHODICAL_GUIDE.md`.
- Помочь weak student понять, после какого safe checkpoint-answer уже лучше остановиться и не добавлять рискованный explanatory tail.
- Не менять числа, formulas, checkpoints, figures, solver truth, report truth и общую структуру guide.

## Files created
- `reports/report_M9_stop_line_hardening.md`

## Files updated
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/master_report.md`

## What was strengthened
- В targeted подпунктах добавлены короткие local stop-line bridges формата:
  - `После этого лучше остановиться и не добавлять ...`
  - `Безопасная финальная точка такая: ...`
- Каждый новый мостик объясняет:
  - после какого safe compressed answer уже можно остановиться;
  - какой опасный хвост не надо продолжать;
  - какой короткой фразой безопасно закрыть ответ.
- Усиление осталось коротким и student-facing; existing defense cards и prior hardening layers не дублировались.

## Which areas gained stop-line hardening
- `1.1`:
  - добавлен stop-line после порога по отказу, чтобы student не превращал local threshold в "лучшее число операторов вообще".
- `1.2`:
  - добавлен stop-line после локального сравнения очереди и операторов, чтобы student не скатывался в универсальные советы "всегда увеличивать только `m`" или только `n`.
- `1.3`:
  - добавлен stop-line после первой стационарной точки, чтобы student не начинал приписывать стационарные числа неустойчивым режимам.
- `1.4`:
  - добавлен stop-line после safe вывода про облегчение хвоста, чтобы student не выдавал уход клиентов за полное решение перегрузки.
- `2.1`:
  - добавлен stop-line после checkpoint `r = 20`, чтобы student не объявлял эту точку универсально лучшим числом наладчиков.

## What intentionally remained unchanged
- Весь section order guide.
- Все числа и artifact-derived checkpoints.
- Все formulas.
- Все figures.
- Все report/data/manifest files.
- Existing formula-defense, graph-defense, contrast-defense, compression layer и defense-card layers как отдельные структуры.
- Любые solver/report/delivery/runtime/UX files не менялись.

## Remaining risks
- Guide стал сильнее именно на stop-line layer, но weak student всё ещё может потеряться в длинном неподготовленном cross-questioning после базового safe ответа.
- Текущий guide лучше защищает точку остановки после локального ответа, чем длинную импровизацию при цепочке новых follow-up вопросов.
- Methodical branch по-прежнему остаётся compact defense guide, а не полным устным сценарием с rehearsal tree.

## Ready for M10? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `M10 — Final Methodical Freeze Review`.
- Держать его таким же узким:
  - проверить уже накопленный `M5`-`M9` hardening layer как единый weak-student defense surface;
  - исправлять только tiny consistency issues, если они реально найдутся;
  - не менять числа, formulas, figures, data/manifests и общую структуру guide.
