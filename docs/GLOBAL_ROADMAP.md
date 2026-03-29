# Global Roadmap

## Статус и назначение
Этот документ замораживает верхнеуровневую дорожную карту проекта поверх уже закрытого berchun baseline. Его задача: явно развести две линии дальнейшей работы:
- polish branch для текущего teacher-facing MVP;
- post-freeze feature branch для последующего роста за пределы текущего отчётного ядра.

## Текущий frozen state
- Frozen baseline закрыт на `STAGE 09B` + `F2`.
- Текущий solver/report/build контур для berchun MVP считается закрытым и не нуждается в повторном redesign без отдельного нового доказанного основания.
- Ближайший приоритет проекта: довести teacher-facing polish текущего MVP report system.

## Структура roadmap
- Ветка `Polish Branch` описывает только доводку текущего MVP отчёта.
- Ветка `Feature Branch` описывает post-freeze расширения, согласованные заранее, но не входящие в немедленный polish scope.
- Эти две ветки не смешиваются в одном Codex-pass.
- Если owner сознательно меняет приоритет, это должно быть отражено отдельным новым scope, а не неявным drift внутри текущего.

## Ветка A — Polish Branch
Источник истины: `docs/MVP_POLISH_PLAN.md`

Состав ветки:
1. `P1 — Numeric Display + Local Notation Hygiene`
2. `P2 — Plot Readability + Non-Stationary Visual Policy`
3. `P3 — Task 1 Sequential Derivation Reflow`
4. `P4 — Task 2 Readability + Final Teacher-Facing Microfit`

Назначение ветки:
- сделать текущий отчёт более human-readable;
- довести teacher-facing presentation до стабильного reference-compatible качества;
- не менять solver truth, `out/data`, figure data и pipeline behavior.

## Ветка B — Post-freeze Feature Branch
Эта ветка intentionally не входит в текущий polish scope, но уже замораживается как согласованное направление дальнейшего роста.

### Phase B1 — MVP usability extensions
1. `Feature-01 — task1/task2/full selection in CLI/report generation`
2. `Feature-02 — DOCX/exportable editable version`
3. `Feature-03 — defense-prep layer`

### Phase B2 — Platform foundation over study/
4. `Feature-04 — higher-level platform foundation over study/`
5. `Feature-05 — subject adapterization for other subject boxes`

### Phase B3 — Channel and operations surface
6. `Feature-06 — channel bot MVP`
7. `Feature-07 — order pipeline/admin surface`
8. `Feature-08 — payments/tokens/ledger`

## Ordering rationale
- Сначала идёт `Polish Branch`, потому что это текущий owner priority и самая короткая дорога к более сильному teacher-facing MVP.
- `Feature-01`–`Feature-03` стоят первыми в feature-ветке, потому что они ближе всего к уже существующему report/product surface и требуют минимального conceptual jump.
- `Feature-04` идёт раньше bot/admin/payment scopes, потому что platform foundation должна быть зафиксирована до расширения в каналы и многопредметность.
- `Feature-05` идёт после foundation, потому что adapterization без общей платформенной рамки быстро создаст drift между subject boxes.
- `Feature-06`–`Feature-08` идут последними, потому что bot/operations/commercial layers должны опираться на уже стабилизированные foundation, subject contracts и operator workflows.

## Правило ветвления
- По умолчанию следующий scope после текущей planning freeze-ступени: `P1`.
- Переход в `Feature Branch` до завершения `P1`–`P4` возможен только как явное управленческое решение owner.
- Даже при таком переключении feature scope должен быть выделен как отдельный narrow pass и не смешиваться с незавершённым polish scope.

## Что этот roadmap не разрешает
- скрытно переоткрывать frozen baseline;
- смешивать teacher-facing polish с platform feature work в одном шаге;
- делать вид, что broader future direction «само собой понятно» без отдельной scope framing.
