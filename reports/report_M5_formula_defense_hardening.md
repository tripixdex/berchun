# Report M5 — Formula-to-Defense Hardening

## Scope ID and name
- `M5 — Formula-to-Defense Hardening`

## Objective
- Узко усилить formula-to-defense слой в `docs/methodical/content/METHODICAL_GUIDE.md`.
- Работать только в `1.1`, `1.3`, `1.4`, `2.1`.
- Не менять числа, формулы, checkpoints, solver truth, report truth и общую структуру guide.

## Trusted inputs used
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_SKELETON.md`
- `docs/methodical/architecture/METHODICAL_DEFENSE_TEMPLATE.md`
- `report/final_report.pdf`
- `reports/master_report.md`
- user-provided independent audit conclusion for `M5`

## Files created
- `reports/report_M5_formula_defense_hardening.md`

## Files updated
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/master_report.md`

## What was strengthened
- После ключевых formula-origin points добавлены короткие локальные мостики:
  - что именно сейчас считается;
  - откуда берётся выражение;
  - почему метрика читается именно из этих состояний.
- В `1.1`, `1.3`, `1.4`, `2.1` добавлены compact danger-question cues вида:
  - `Опасный вопрос здесь такой: ...`
  - `Безопасный ответ: ...`
- Усиление осталось коротким и oral-defense oriented; guide не превращался в derivation note.

## Which targeted sections changed
- `1.1`:
  - усилено различие между `P_отк = p_n` и средним по всем состояниям;
  - добавлен follow-up bridge про один крайний state против всего распределения.
- `1.3`:
  - усилено объяснение, что сначала проверяется право на существование стационарных средних;
  - добавлен follow-up bridge про невозможность честно читать стационарные метрики в неустойчивом режиме.
- `1.4`:
  - усилено происхождение `δ_k` как суммы двух способов разгрузки хвоста;
  - усилено объяснение controlled truncation как bounded approximation, а не произвольной отсечки;
  - добавлены короткие follow-up bridges для обеих точек риска.
- `2.1`:
  - усилено происхождение `λ_i`, `μ_i` и рекуррентного чтения всех метрик из одного `p_i`;
  - усилено различие между `P_ож` и фактом наличия очереди;
  - добавлены короткие follow-up bridges по обеим темам.

## What intentionally remained unchanged
- Весь section order guide.
- Все числа и artifact-derived checkpoints.
- Все formulas и teacher-facing mathematical truth.
- Весь existing defense-card set.
- `1.2` не открывался.
- Любые solver/report/delivery/runtime/UX files не менялись.

## Remaining risks
- Guide стал сильнее именно на formula-origin layer, но ещё не доведён до отдельного graph-to-conclusion hardening pass.
- Current methodical branch по-прежнему остаётся markdown-first explanatory surface, а не full oral-defense encyclopedia.
- Внутри `1.3`/`1.4`/`2.1` student still depends on disciplined oral wording; M5 усилил это локально, но не заменяет rehearsal.

## Ready for M6? YES/NO
- `YES`

## Exact recommendation for next step
- Открыть `M6 — Graph-to-Conclusion Defense Hardening`.
- Держать его таким же узким:
  - усиливать только места, где студент должен устно объяснить форму графика и разрешённый локальный вывод;
  - не менять числа, formulas, figures, data/manifests и общую структуру guide.
