# UX One-Button Plan

## Status and Purpose
Этот документ замораживает отдельный UX scope для operator-facing simplification.

Его задача не в том, чтобы менять solver truth, report truth или delivery semantics. Его задача — поверх уже работающего runtime зафиксировать более простой внешний путь: один понятный session flow, один человеческий выбор результата, один очевидный итог.

## Why The Current UX Is Insufficient
- Текущий runtime technically correct, но operator-facing слой всё ещё заставляет человека думать внутренними сущностями `delivery_profile`, `guide_mode`, `guide_scope`, `output_format`.
- Unified session скрывает build/deliver orchestration только частично: operator всё ещё переводит свою задачу в internal matrix вручную.
- README честный, но перегруженный technical detail; confused operator не получает короткого ответа на вопрос “что мне нажать, чтобы получить нужный комплект”.
- Current prompts спрашивают не сценарий пользователя, а параметры системы.
- Финальный результат описывается слишком технически: operator видит IDs, manifests и internal names раньше, чем понятный human summary produced outputs.

## What “One Button” Means In This Repository
- Один рекомендуемый operator-facing entrypoint для нормальной работы.
- Одна непрерывная session: intake -> review -> build -> choice of result -> final summary.
- Один human-language вопрос о desired outcome вместо direct exposure of delivery matrix.
- Один final result screen, где сначала показано “что собрано”, а уже потом при необходимости technical detail.

Это не означает слияние build и deliver semantics в один truth path.

## External UX vs Internal Runtime
- Internal build truth path остаётся прежним: canonical raw input -> `run_build`.
- Internal delivery packaging path остаётся прежним: `run_delivery`.
- One-button UX — это только operator-facing translation layer над уже frozen runtime.
- Scenario labels снаружи могут быть human-friendly, even if inside they map to `report_only`, `study_pack`, `guide_only`, `print_pack`.
- Internal constraints вроде `guide_scope = report_scope` для `study_pack` должны применяться автоматически, а не превращаться в отдельную operator puzzle.

## Staged Roadmap
- `U1 — Operator UX Audit + One-Button Contract Freeze`
- `U2 — Scenario-Driven One-Button Session Runtime`
- `U3 — Result Summary + Operator Help Closeout`

## Recommended Implementation Order
1. Сначала заменить technical delivery selection на scenario-first prompt layer.
2. Затем спрятать internal field names и показывать только human labels for scope, material type and final format.
3. Затем привести final closeout summary к виду “что создано и где лежит”.
4. После этого синхронизировать README/help text с новой operator contract.

## Separation From Truth-Bearing Branches
- Этот UX scope не открывает новый solver behavior.
- Этот UX scope не меняет formal report content.
- Этот UX scope не меняет frozen methodical guide content.
- Этот UX scope не меняет delivery request model как internal contract.
- Этот UX scope меняет только то, как already implemented behavior объясняется и выбирается оператором.

## Why This Must Be A Separate Explicit Scope
- Runtime уже работает; проблема теперь не вычислительная, а operator-facing.
- Если пытаться править UX без frozen contract, легко случайно сломать explicit delivery rules.
- Separate UX freeze нужен, чтобы дальнейший implementation pass был narrow: только session wording, scenario mapping и result presentation.
