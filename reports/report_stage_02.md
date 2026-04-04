# Stage ID and name
STAGE 02: Confirm Variant + Implement Analytical Solver
Corrective Pass A

## Objective
Исправить неверно записанный raw-вход `journal_number`, пересчитать все зависящие derived-параметры и аналитические выходы, минимально улучшить структуру oversized кода и честно переоформить отчёт Stage 02 без расширения scope.

## Trusted inputs used
- `docs/project/SPEC.md`
- `docs/project/INPUT_MAP.json`
- `docs/report/REPORT_CONTRACT.md`
- `reports/report_stage_01.md`
- `reports/report_stage_02.md` предыдущей редакции
- `reports/master_report.md`
- `inputs/variant_me.yaml` предыдущей редакции
- `inputs/derived_parameters.json` предыдущей редакции
- Подтверждённые raw-входы corrective pass:
  - `journal_number = 4`
  - `birth_day = 25`
  - `birth_month = 6`

## What was wrong before
- В предыдущей редакции Stage 02 был зафиксирован неверный `journal_number = 5`.
- Из-за этого были неверны все производные величины, зависящие от номера по журналу:
  - `task1.tc_seconds`
  - `task2.tc_minutes`
  - связанные интенсивности поступления и offered load.
- Следовательно, все `out/data/*.json` содержали численные результаты не для подтверждённого варианта пользователя.

## Files created
- `src/variant.py`
- `src/pipeline.py`
- `src/compute/task1_common.py`
- `src/compute/task1_finite.py`
- `src/compute/task1_infinite.py`

## Files updated
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `docs/project/INPUT_MAP.json`
- `src/cli.py`
- `src/compute/task1.py`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`
- `tests/test_task1.py`
- `tests/test_task2.py`
- `tests/test_variant_integrity.py`
- `reports/report_stage_02.md`
- `reports/master_report.md`

## Implementation summary
- Raw-вход исправлен на подтверждённый:
  - `journal_number: 5 -> 4`
  - `birth_day: 25` без изменений
  - `birth_month: 6` без изменений
- Derived-параметры пересчитаны:
  - задача 1: `Tc = 14 c`, `Ts = 65 c`, `Tw = 106 c`
  - задача 2: `N = 36`, `Tc = 104 мин`, `Ts = 50 мин`
- Все аналитические JSON-выходы пересобраны заново через `python3 -m src.cli`.
- Oversized модули прошлой редакции разрезаны:
  - `src/cli.py: 244 -> 31` строка через вынос variant/pipeline-логики;
  - `src/compute/task1.py: 398 -> 9` строк через вынос finite/infinite расчётов в отдельные модули.
- Часть лишнего hardcoding убрана:
  - derivation/document builder вынесен в `src/variant.py`;
  - output writing и orchestration вынесены в `src/pipeline.py`;
  - диапазоны sweep-ов в `derived_parameters.json` теперь формируются из значений dataclass, а не только из голых литералов внутри CLI.

## Which outputs changed because of journal_number changed from 5 to 4
- `out/data/task_1_1.json`
  - изменился `input_snapshot`: `tc_seconds 15 -> 14`, `offered_load_erlangs 4.333333333333333 -> 4.642857142857143`;
  - изменился главный дискретный вывод: `minimal_operators_for_refusal_below_target 10 -> 11`.
- `out/data/task_1_2.json`
  - изменился `input_snapshot`;
  - все семейства кривых пересчитаны для большей входной нагрузки; диапазоны sweep-ов не изменились.
- `out/data/task_1_3.json`
  - изменился `input_snapshot`;
  - `first_stationary_operators` не изменился и остался `5`;
  - стационарные значения изменились численно, например при `5` операторах `queue_length_expected` выросло `4.482690761038142 -> 10.75769968683608`.
- `out/data/task_1_4.json`
  - изменился `input_snapshot`;
  - все метрики в стационарно-усечённом режиме пересчитаны, например при `5` операторах `queue_length_expected` выросло `0.7530404752971156 -> 0.9705722342925645`.
- `out/data/task_2_1.json`
  - изменился `input_snapshot`: `tc_minutes 105 -> 104`, `offered_load_per_machine_erlangs 0.47619047619047616 -> 0.4807692307692308`;
  - все кривые по числу наладчиков пересчитаны, например при `10` наладчиках `waiting_probability` выросла `0.8834940555321936 -> 0.8907358907061694`.

## Whether final analytical conclusions changed
- Да, для `1.1` изменился итоговый порог: условие `P_refusal < 0.01` теперь впервые достигается при `11`, а не при `10` операторах.
- Нет, для `1.3` граница стационарности не изменилась: стационарный режим по-прежнему начинается с `5` операторов.
- Для `1.2`, `1.4`, `2.1` изменились численные кривые, но в предыдущем отчёте не было зафиксировано отдельных дискретных one-line выводов сверх диапазонов sweep-а и modelling notes.

## Which code files were structurally improved
- `src/cli.py`
  - теперь содержит только CLI parsing и вызов pipeline.
- `src/pipeline.py`
  - выделен для orchestration, записи JSON и полного прогона стадии.
- `src/variant.py`
  - выделен для загрузки raw-входов, derivation и сборки machine-readable документа derived-параметров.
- `src/compute/task1.py`
  - превращён в тонкий экспортный модуль.
- `src/compute/task1_common.py`
  - выделены общие helpers для задачи 1.
- `src/compute/task1_finite.py`
  - вынесена finite-state логика для `1.1` и `1.2`.
- `src/compute/task1_infinite.py`
  - вынесена infinite-state логика для `1.3` и `1.4`.

## Validation actually re-run
- Выполнен `python3 -m src.cli`.
- Выполнен `python3 -m unittest discover -s tests -v`.
- Выполнен `python3 -m json.tool docs/project/INPUT_MAP.json`.
- Выполнен `python3 -m json.tool inputs/derived_parameters.json`.
- Выполнена проверка чтения всех `out/data/*.json` через `json.loads`.

## Corrected now
- Исправлен raw input `journal_number`.
- Пересчитаны derived-величины `task1.tc_seconds` и `task2.tc_minutes` и зависящие от них интенсивности.
- Пересобраны все machine-readable outputs.
- Исправлены тестовые ожидания на новый вариант.
- Обновлён `docs/project/INPUT_MAP.json` как trusted machine-readable summary.

## Revalidated now
- Парсинг `inputs/variant_me.yaml`.
- Согласованность `inputs/derived_parameters.json`.
- Генерация и запись всех `out/data/*.json`.
- Структурированность solver outputs.
- Обработка `non_stationary` в `1.3`.
- Наличие truncation metadata в `1.4`.
- Диапазон `waiting_probability` для `2.1`.

## Unchanged
- Постановка задачи и границы Stage 02.
- `birth_day = 25`, `birth_month = 6`.
- Derived-параметры, не зависящие от номера по журналу:
  - `task1.ts_seconds = 65`
  - `task1.tw_seconds = 106`
  - `task2.machine_count = 36`
  - `task2.ts_minutes = 50`
- Модельная трактовка `waiting_probability` в `2.1`.
- Truncation policy для `1.4`.

## Inferred
- `waiting_probability` в `2.1` по-прежнему трактуется как arrival-weighted вероятность ожидания для новой заявки.
- Верхняя граница sweep-а `task2.repairers = 1..N` по-прежнему основана на frozen inference из Stage 01.

## Deferred
- Генерация графиков.
- Формульные артефакты для итогового отчёта.
- Сборка финального отчёта.
- Внешний cross-check против независимого численного эталона или симуляции.

## What remains unknown or risky
- Независимое внешнее численное сравнение с формулами из образца по-прежнему не выполнено.
- Трактовка `waiting_probability` в `2.1` остаётся явным modelling choice, а не формулой, напрямую извлечённой из образца.
- `src/variant.py` и `src/compute/task1_finite.py` остаются выше soft limit по длине (`163` и `157` строк), но не превышают hard limit и не смешивают разные ответственности.

## File length review result
- Hard limit `180` строк после corrective pass не превышает ни один program file.
- Исправлены два прежних hard-limit нарушения:
  - `src/cli.py`
  - `src/compute/task1.py`
- Soft-limit исключения оставлены только там, где модуль уже обладает одной чёткой ответственностью:
  - `src/variant.py` загружает raw-вход, производит derivation и собирает один machine-readable document;
  - `src/compute/task1_finite.py` содержит только finite-state модели задачи 1.

## Hardcode review result
- Сокращено дублирование путей, derivation-формул и sweep-описаний внутри CLI.
- Убраны скрытые behavioral switches: orchestration и derivation вынесены в явные модули.
- Сохранены только предметно-естественные inline-константы:
  - формулы варианта из `my_var.md`;
  - canonical output filenames;
  - математически естественные пороги и диапазоны, уже зафиксированные в спецификации и dataclass defaults.

## Sanitation check
- Scope corrective pass не расширялся в сторону Stage 03+.
- Git не трогался.
- Дополнительная документация сверх минимально необходимой не создавалась.
- После `compileall` и тестов служебные `__pycache__` были удалены.

## Prompt re-check
- Сначала inspected Stage 02 artifacts: выполнено.
- Исправлен raw input: выполнено.
- Пересчитаны derived параметры: выполнено.
- Пересобраны аналитические outputs: выполнено.
- Проведён structural quality pass: выполнено.
- Повторная narrow validation реально запущена: выполнено.
- Отчёты обновляются в конце: выполнено.

## READY TO CLOSE STAGE 02? YES/NO
YES

## Recommendation for exact next stage
`STAGE 03 — Generate Figures + Package Artifacts`.

Точный следующий шаг:
- строить все обязательные графики строго из обновлённых `out/data/*.json`;
- сохранить figure-артефакты по контракту `docs/report/REPORT_CONTRACT.md`;
- подготовить machine-readable manifest соответствия `данные -> график`;
- не переходить к сборке финального отчёта раньше Stage 04.
