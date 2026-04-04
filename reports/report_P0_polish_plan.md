# Scope Report

## Scope ID and name
- `P0 — MVP Polish Roadmap Freeze`

## Objective
- Заморозить детальный polishing roadmap и presentation contract для текущего berchun MVP report system перед любыми следующими teacher-facing implementation passes.

## Trusted inputs used
- `report/final_report.pdf`
- `references/DZ1.pdf`
- `src/render/common.py`
- `src/render/content.py`
- `src/render/section_flow.py`
- `src/render/title_page.py`
- `src/render/report_builder.py`
- `src/render/specs.py`
- `src/plots/common.py`
- `src/plots/style.py`
- `src/plots/task1_simple.py`
- `src/plots/task1_family.py`
- `src/plots/task2.py`
- `docs/report/REFERENCE_COMPAT_CONTRACT.md`
- `reports/master_report.md`

## Files created
- `docs/report/MVP_POLISH_PLAN.md`
- `docs/report/REPORT_PRESENTATION_CONTRACT.md`
- `reports/report_P0_polish_plan.md`

## Files updated
- none

## What was defined now
- Зафиксирован новый MVP-polish roadmap из последовательных implementation passes `P1`–`P4`.
- Зафиксирован teacher-facing presentation contract для чисел, графиков, non-stationary presentation, variable explanations, captions и derivation rhythm.
- Зафиксированы жёсткие scope boundaries: будущие passes должны оставаться rendering-local и не имеют права переоткрывать solver truth, `out/data`, figure data, scheme semantics или build/archive behavior.

## Highest-priority issues
- Teacher-facing числа в текущем PDF и render helpers всё ещё часто показываются с избыточной точностью; это противоречит требованию owner о `max 3 decimal places`.
- Блок `Исходные данные` уже существует, но ещё не выглядит как полностью замороженный и одинаковый visual primitive во всех item-блоках.
- После схем остаётся неполная и неравномерная подача обозначений, из-за чего часть переменных читается «по памяти», а не локально.
- Family plots остаются визуально тяжелее reference-family, а policy `no legend overlap` пока не зафиксирована как обязательное правило исполнения.
- `1.3` честно отделяет non-stationary region, но визуальная convention для shading/note ещё не заморожена.
- Dense spots в `1.1`, `1.4` и `2.1` всё ещё более систематизированы, чем human-readable, и недостаточно похожи на reference-family sequential exposition.

## Staged polish plan
1. `P1 — Numeric Display + Local Notation Hygiene`
Результат: заморозить и применить numeric display policy, единый блок `Исходные данные` и обязательные `Обозначения:` после схем.

2. `P2 — Plot Readability + Non-Stationary Visual Policy`
Результат: сделать plots визуально спокойнее и cleaner, убрать риск legend overlap, внедрить frozen policy для `1.3` non-stationary marking.

3. `P3 — Task 1 Sequential Derivation Reflow`
Результат: sections `1.1`–`1.4` становятся более пошаговыми, human-readable и reference-compatible по ритму изложения.

4. `P4 — Task 2 Readability + Final Teacher-Facing Microfit`
Результат: `2.1` доводится до того же teacher-facing уровня, после чего выполняется финальная проверка отчёта на соответствие presentation contract без переоткрытия math/core scope.

## What must remain unchanged
- Solver mathematics.
- `out/data` truth.
- Figure data and series content.
- Scheme semantics.
- Run archive, intake and build behavior.
- `1.1` threshold truth;
- `1.3` explicit non-stationary handling;
- `1.4` `epsilon = 1e-12` and residual-bound truth;
- `2.1` arrival-weighted meaning of `waiting_probability`.

## Ready for P1?
- YES

## Exact recommendation for next pass
- Открыть `P1 — Numeric Display + Local Notation Hygiene` и ограничить его только teacher-facing numeric formatting, uniform `Исходные данные` blocks, обязательными локальными `Обозначения:` после схем и минимально необходимыми render-local helper changes без изменения solver/data truth.
