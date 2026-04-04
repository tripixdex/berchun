# Stage ID and name
STAGE 04: Assemble Final Report

## Objective
Собрать итоговый отчёт по варианту пользователя на русском языке из уже подтверждённых входов, аналитических JSON-результатов и figure artifacts, довести пакет до канонического `TeX -> PDF` вида и не менять solver truth.

## Trusted inputs used
- `docs/project/SPEC.md`
- `docs/report/REPORT_CONTRACT.md`
- `reports/report_stage_03.md`
- `reports/master_report.md`
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `out/artifacts/figure_manifest.json`
- `out/data/task_1_1.json`
- `out/data/task_1_2.json`
- `out/data/task_1_3.json`
- `out/data/task_1_4.json`
- `out/data/task_2_1.json`
- `figures/*.png`
- `references/DZ1.docx`

## Files created
- `src/render/__init__.py`
- `src/render/common.py`
- `src/render/schemes.py`
- `src/render/specs.py`
- `src/render/content.py`
- `src/render/report_builder.py`
- `report/assets/task1_1__scheme.png`
- `report/assets/task1_2__scheme.png`
- `report/assets/task1_3__scheme.png`
- `report/assets/task1_4__scheme.png`
- `report/assets/task2_1__scheme.png`
- `report/final_report.tex`
- `report/final_report.pdf`
- `report/assets_manifest.json`
- `reports/report_stage_04.md`

## Files updated
- `src/cli.py`
- `reports/master_report.md`

## Implemented now
- Добавлен отдельный `render`-слой для Stage 04 без изменения вычислительного контура.
- Реализован CLI-путь `python3 -m src.cli report`.
- Авторитетным исходником отчёта сделан `report/final_report.tex`.
- Сгенерированы `5` недостающих расчётных схем в `report/assets/`.
- Собран финальный `report/final_report.pdf` через `xelatex`.
- Выпущен `report/assets_manifest.json` с явной фиксацией:
  - входных JSON-данных;
  - reused plot PNG;
  - дополнительных scheme assets;
  - build-команд.
- Все новые программные файлы Stage 04 уложены в hard limit `180` строк; самый длинный файл `src/render/report_builder.py` имеет `159` строк.
- В итоговом `TeX` зафиксированы `32` включения рисунков:
  - `27` reused plot PNG из Stage 03;
  - `5` новых scheme PNG из Stage 04.
- Внутренняя структура каждого раздела приведена к контракту:
  - формулировка;
  - исходные данные;
  - расчётная схема;
  - формулы вероятностей состояний;
  - формулы метрик;
  - рисунки и краткие пояснения.

## Reused from earlier stages
- Подтверждённые raw inputs из `inputs/variant_me.yaml`.
- Производные параметры из `inputs/derived_parameters.json`.
- Все `5` аналитических JSON-выходов из `out/data/`.
- Все `27` индивидуальных plot PNG из `figures/`.
- Замороженные modelling choices Stage 02/03:
  - нестационарные точки `1.3` не маскируются фиктивными значениями;
  - `1.4` использует deterministic truncation policy;
  - `2.1` сохраняет arrival-weighted трактовку `waiting_probability`.

## Validated now
- Выполнен `python3 -m src.cli report`.
- Выполнен `python3 -m json.tool report/assets_manifest.json`.
- Выполнен `python3 -m unittest discover -s tests -v` (`9/9`, `OK`).
- Подтверждено наличие и ненулевой размер:
  - `report/final_report.tex`
  - `report/final_report.pdf`
  - `report/assets_manifest.json`
- Подтверждено, что `report/final_report.tex`:
  - содержит `32` вызова `\includegraphics`;
  - ссылается на plot artifacts из `figures/`;
  - ссылается на scheme artifacts из `report/assets/`;
  - фиксирует подтверждённый вариант (`journal_number = 4`).
- Подтверждено, что `report/` после сборки очищается от `aux/fls/fdb/log/xdv` через `latexmk -c`.

## Inferred only
- Расчётные схемы Stage 04 построены детерминированно по уже замороженной структуре моделей, а не экспортированы из внешнего инструмента или из teacher-source.
- На титульном листе оставлены пустые поля для студента/группы/преподавателя, потому что этих персональных данных в репозитории нет.
- Формульные артефакты не вынесены в отдельные файлы; единственным источником формульного оформления выбран `report/final_report.tex`.

## Deferred
- `STAGE 05 — Final Validation + Closeout`.
- Заполнение персональных полей титульного листа при появлении подтверждённых данных.

## Remaining risks
- В текущем репозитории не подтверждены ФИО студента, группа и имя преподавателя для титульного листа; в PDF стоят пустые линии вместо догадок.
- Базовая установка `BasicTeX` ранее показывала отсутствие загруженных русских переносов; PDF собирается успешно, но качество переноса строк может слегка отличаться от полной TeX-установки.

## Final report package summary
- Канонический источник: `report/final_report.tex`.
- Сгенерированный PDF: `report/final_report.pdf`.
- Пакетный manifest: `report/assets_manifest.json`.
- Использованные figure inputs:
  - `27` plot PNG из `figures/`;
  - `5` scheme PNG из `report/assets/`.
- Использованные data inputs:
  - `out/data/task_1_1.json`
  - `out/data/task_1_2.json`
  - `out/data/task_1_3.json`
  - `out/data/task_1_4.json`
  - `out/data/task_2_1.json`
- Всего в финальном отчёте задействовано `32` рисунка, что совпадает с минимальным контрактом.

## Reference-alignment summary
- Сохранён академический контур титульного листа.
- Порядок разделов повторяет reference-family:
  - задача 1;
  - подпункты `1.1`–`1.4`;
  - задача 2;
  - подпункт `2.1`.
- Внутренний порядок подпунктов приведён к контракту и reference-style: схема и формулы идут до графиков.
- Графики встроены как отдельные рисунки, а не как обзорные sheets.

## What was improved versus the reference
- Нумерация рисунков сделана последовательной и без дубликатов.
- В `1.3` отдельно и явно зафиксированы нестационарные режимы.
- В `1.4` отдельно и явно описана политика усечения бесконечного хвоста.
- В `2.1` явно зафиксирована трактовка `waiting_probability`.
- Появился machine-readable `assets_manifest.json`, которого у reference-образца нет.
- Исключено смешение figure-overview sheets с обязательными рисунками финального отчёта.

## Sanitation check
- Solver layer и raw variant не менялись.
- Build-path финального отчёта очищает служебные `latexmk`-артефакты после успешной сборки.
- `__pycache__` после локальных прогонов удалены.
- Дополнительная документация сверх обязательного stage-report не создавалась.
- Git не трогался.

## Prompt re-check
- Сначала inspected Stage 03 outputs и report contract: выполнено.
- Принята reference-aligned структура и mapped current artifacts: выполнено.
- Реализован минимальный render/build path: выполнено.
- Добавлены только действительно недостающие scheme assets: выполнено.
- Собраны `final_report.tex` и `final_report.pdf`: выполнено.
- Narrow validation реально запущена: выполнено.
- Отчёты обновлены в конце: выполнено.

## READY TO CLOSE? YES/NO
YES

## Exact recommendation for the next stage
`STAGE 05 — Final Validation + Closeout`

Точный следующий шаг:
- выполнить финальную сверку `SPEC / REPORT_CONTRACT / final_report.tex / final_report.pdf / assets_manifest.json`;
- проверить, что в master-report и stage-reports нет противоречий по статусам;
- при необходимости вручную заполнить персональные поля титульного листа подтверждёнными данными;
- выполнить закрывающий sanitation sweep и выпустить финальный closeout-report.
