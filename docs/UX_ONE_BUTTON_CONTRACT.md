# UX One-Button Contract

## Status and Purpose
Этот документ замораживает operator-facing contract для future one-button session.

Он определяет, что должен видеть обычный оператор, что должно остаться внутренним, и каким должен быть нормальный session flow поверх уже существующих `build` и `deliver`.

## Frozen Operator-Facing Principles
- Operator должен думать сценариями результата, а не delivery-profile vocabulary.
- Operator должен проходить одну непрерывную session, а не собирать mental model из двух CLI commands.
- Каждый prompt должен отвечать на понятный человеческий вопрос.
- Каждое дополнительное уточнение должно появляться только если оно действительно влияет на результат.
- Final screen должен объяснять output раньше, чем показывать technical IDs.

## What The Operator Should See
- Свою raw-input анкету и нормализованный review перед build.
- Понятный выбор объёма работы: `только задача 1`, `только задача 2`, `вся работа`.
- Понятный выбор desired result:
  - `только итоговый отчёт`
  - `отчёт + материалы для подготовки`
  - `только материалы для подготовки`
  - `печатный комплект`
- Если нужны study materials: понятный выбор between:
  - `персональные материалы по этому варианту`
  - `общие материалы без привязки к варианту`
- Если format choice действительно поддерживается: human labels `PDF`, `DOCX`, `папка-комплект`.
- Финальный human summary produced outputs with local paths.

## What The Operator Should Not See
- literal field names `delivery_profile`, `guide_mode`, `guide_scope`, `output_format`
- `source_run_id`
- `variant_aware` / `general` as raw internal tokens
- `bundle_dir`
- `guide_scope = report_scope` as a manual rule to enforce
- baseline/source path switches like `guide_source_path`, `guide_general_source_path`
- manifest filenames as primary result explanation

## Required Simplifications
- После build operator не должен видеть вопрос “какой delivery_profile нужен?”.
- Для `study_pack` нельзя спрашивать отдельный `guide_scope`, если он обязан совпадать с already chosen work scope.
- Для report-bearing result нельзя повторно спрашивать `report_scope`, если он уже определён raw input.
- В standard one-button flow Markdown не должен быть primary format choice.
- `md` остаётся available through direct technical CLI path, но не через default operator session.

## Required End-State Of The One-Session Flow
1. Operator enters or reviews raw input.
2. Operator confirms canonical build input.
3. System runs canonical build.
4. System asks one human-language question: “Что вы хотите получить на выходе?”
5. System asks only the minimum extra clarifiers needed for the chosen scenario.
6. System shows a human-language review summary.
7. Operator chooses `confirm`, `edit` or `cancel`.
8. System produces result and shows a concise result summary with paths.

## Review / Confirm / Cancel Rules
- `confirm` must mean “produce exactly the summarized result”.
- `edit` must return to the nearest meaningful choice, not to raw internal fields.
- `cancel` must leave the already completed build intact and skip only the optional result packaging layer.

## Final Result Presentation Contract
- First block: “Что создано”.
- Second block: direct local paths to the produced operator-facing artifacts.
- Third block: optional technical detail such as `run_id` or `delivery_id`.
- Manifest paths may appear only as secondary technical detail, not as the main explanation of success.

## Explicitly Forbidden Shortcuts
- Нельзя просто переименовать current technical prompts without changing their wording logic.
- Нельзя показывать operator raw internal enums and считать это acceptable UX.
- Нельзя делать “one button” ценой смешивания build truth и delivery packaging into one opaque semantic blob.
- Нельзя открывать новые formats or new bundle semantics inside this UX scope.
