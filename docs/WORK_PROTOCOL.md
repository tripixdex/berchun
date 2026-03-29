# Work Protocol

## Назначение
Этот документ замораживает рабочий протокол для будущих шагов проекта в цикле `assistant -> user -> Codex -> user/reviewer -> assistant`.

## Базовое правило scope
- Один шаг равен одному узкому scope.
- Один scope имеет одну главную цель.
- У каждого scope должны быть явно выписаны:
- objective;
- in-scope / out-of-scope;
- trusted inputs;
- required output files;
- validation requirements;
- done criteria.

## Рабочий цикл
1. Assistant формулирует следующий narrow scope и фиксирует границы.
2. User подтверждает scope, сужает его или переписывает ограничения.
3. Codex выполняет только этот scope и возвращает артефакты.
4. User и/или reviewer проверяют результат и либо принимают его, либо формулируют следующий narrow corrective pass.
5. Assistant закрывает текущий scope в документации и предлагает следующий шаг.

## Что должен вернуть Codex после каждого run
- список созданных файлов;
- список обновлённых файлов;
- список реально запущенных команд;
- что было сделано;
- что осталось риском, blocker'ом или сознательно не трогалось;
- результат validation либо явное указание, что scope был planning-only/documentation-only;
- verdict `готово / не готово` для следующего шага, если он требуется;
- exact next recommendation.

## Обязательные reporting artifacts
- Для каждого нетривиального scope создаётся отдельный отчёт в `reports/` с именем вида `report_<scope>.md`.
- Если scope меняет текущее planning state, latest report path или next step, обновляется `reports/master_report.md`.
- Если scope чисто локальный и не меняет верхнеуровневое состояние, `master_report.md` обновляется только по явному требованию scope.

## Acceptance criteria
- Scope считается закрытым только если все требуемые output files созданы или обновлены.
- В отчёте должны быть честно разделены: выполнено, не выполнено, не проверено, оставшиеся риски.
- Нельзя заявлять более широкую готовность, чем реально подтверждают артефакты и validation.
- Следующий шаг должен быть назван явно; закрывать scope фразой «дальше видно будет» запрещено.

## Git policy
- Git по умолчанию запрещён.
- Commit допустим только по явному запросу user.
- Commit не создаётся автоматически в конце scope.
- Если нужен commit, это либо отдельный narrow scope, либо явный add-on к уже закрытому scope после синхронизации отчётов.

## Anti-drift rules
- Не смешивать `Polish Branch` и `Feature Branch` в одном Codex-pass.
- Не переоткрывать solver mathematics в governance/documentation/polish scopes без отдельного доказанного основания.
- Не прятать cleanup, refactor или feature work под видом «маленькой правки рядом».
- Не использовать память или старые summary claims как источник истины, если текущие артефакты репозитория говорят иначе.
- Любые reviewer findings становятся trusted input только после явного включения их в следующий scope.
- Если scope planning-only, он не должен незаметно превращаться в implementation pass.

## Default branch rule
- Пока owner явно не сменил приоритет, immediate next scope берётся из `Polish Branch`.
- На момент заморозки этого протокола таким шагом является `P1 — Numeric Display + Local Notation Hygiene`.
