# Analytical Queueing Coursework Repository

## Purpose
Репозиторий воспроизводимо строит аналитическое решение и итоговый отчёт по двум учебным задачам:
- задача 1: проектирование call-центра;
- задача 2: проектирование производственного участка.

Канонический пользовательский путь с `Stage 07` и далее: один raw-input intake, затем детерминированный проход `solve -> figures -> report`.
С `P2` канонический результат `build` сохраняется как отдельный run bundle в `runs/<run_id>/`; повторное вычисление допускается к reuse только при полностью идентичном canonical raw input.

## Canonical Workflow
Для обычной работы используйте только команду `build`.

Файловый режим:
```bash
python3 -m src.cli build --input inputs/examples/student_example.yaml
```

Файловый режим только для задачи 1:
```bash
python3 -m src.cli build --input my_student.yaml
```
В `my_student.yaml` задайте `report_scope: "task1"`.

Файловый режим только для задачи 2:
```bash
python3 -m src.cli build --input my_student.yaml
```
В `my_student.yaml` задайте `report_scope: "task2"`.

Файловый режим с review перед сборкой:
```bash
python3 -m src.cli build --input inputs/examples/student_example.yaml --review
```

Интерактивный режим:
```bash
python3 -m src.cli build --interactive
```

Интерактивный режим с optional delivery в той же сессии:
```bash
python3 -m src.cli build --interactive --offer-delivery
```

Поведение `build` теперь двухслойное:
- канонический preserved result: `runs/<run_id>/...`
- convenience mirror для совместимости: обновляются указанные working-set paths, если они заданы

Review/confirm UX:
- `build --interactive` спрашивает дату рождения одним полем `ДД.ММ.ГГГГ`, не спрашивает `report_year` в нормальном пути и по умолчанию подставляет преподавателя `Берчун Юрий Валерьевич`;
- в интерактивном пути группа выбирается через quick-select `РК9-81Б / РК9-82Б / РК9-83Б / РК9-84Б / другая группа`, а `report_scope` по умолчанию равен `full`;
- `build --interactive` после ввода всегда показывает нормализованный raw input и требует `confirm`, `edit` или `cancel`;
- `edit` меняет одно выбранное поле и повторно валидирует весь canonical raw input без перезапуска ввода с нуля;
- `build --input ... --review` показывает тот же нормализованный summary и требует `confirm` или `cancel` перед фактической сборкой;
- без `--review` файловый режим работает как раньше: валидирует input file и сразу запускает build.
- `build --offer-delivery` после успешного `build` открывает отдельный post-build delivery prompt в той же operator session, но не смешивает внутренние semantics `build` и `deliver`;
- unified session сначала завершает truth-bearing `build`, а уже потом предлагает `none / report_only / study_pack / guide_only / print_pack`;
- перед фактическим delivery unified session показывает нормализованный delivery request и требует `confirm`, `edit` или `cancel`.

Если не переопределять пути, команда `build`:
- создаст новый bundle в `runs/<run_id>/...` или переиспользует существующий успешный bundle при идентичном полном canonical raw input;
- обновит convenience mirrors:
  - raw input: `inputs/variant_me.yaml`
  - derived parameters: `inputs/derived_parameters.json`
  - solver outputs: `out/data/*.json`
  - figures: `figures/*.png`
  - figure manifest: `out/artifacts/figure_manifest.json`
  - report source: `report/final_report.tex`
  - final PDF: `report/final_report.pdf`
  - report manifest: `report/assets_manifest.json`

Безопасность reuse:
- reuse разрешён только при полном совпадении всех normalized raw-input fields;
- изменение `student_full_name`, `student_group`, `teacher_full_name`, `journal_number`, `birth_date`, `report_scope` или `report_year` создаёт новый run;
- поведение вида “взять старый отчёт и просто заменить имя” не поддерживается.

Изолированный прогон без перезаписи канонического пакета можно сделать так:
```bash
python3 -m src.cli build \
  --input inputs/examples/student_example.yaml \
  --runs-dir /tmp/berchun_run/runs \
  --variant-path /tmp/berchun_run/inputs/variant_me.yaml \
  --derived-path /tmp/berchun_run/inputs/derived_parameters.json \
  --out-dir /tmp/berchun_run/out/data \
  --figures-dir /tmp/berchun_run/figures \
  --manifest-path /tmp/berchun_run/out/artifacts/figure_manifest.json \
  --report-source-path /tmp/berchun_run/report/final_report.tex \
  --report-pdf-path /tmp/berchun_run/report/final_report.pdf \
  --report-assets-manifest-path /tmp/berchun_run/report/assets_manifest.json
```

## Delivery Workflow
Команда `deliver` не пересчитывает solver truth.

Она пакует уже существующие surfaces из успешного `runs/<run_id>/...` и пишет результат в `deliveries/<delivery_id>/...`.

Текущий delivery slice после `F02C3` реально поддерживает:
- `report_only` + `pdf`
- `guide_only` + `variant_aware` + `md`
- `guide_only` + `variant_aware` + `pdf`
- `guide_only` + `general` + `md`
- `guide_only` + `general` + `pdf`
- `study_pack` + `bundle_dir` + `variant_aware`
- `study_pack` + `bundle_dir` + `general`
- `print_pack` + `bundle_dir`

Пример: только formal report из уже успешного run.
```bash
python3 -m src.cli deliver \
  --delivery-profile report_only \
  --output-format pdf \
  --report-scope full \
  --source-run-id <run_id>
```

Пример: variant-aware methodical guide только по задаче 1.
```bash
python3 -m src.cli deliver \
  --delivery-profile guide_only \
  --output-format md \
  --guide-mode variant_aware \
  --guide-scope task1 \
  --source-run-id <run_id>
```

Пример: полный `study_pack` из уже успешного run.
```bash
python3 -m src.cli deliver \
  --delivery-profile study_pack \
  --output-format bundle_dir \
  --report-scope full \
  --guide-mode variant_aware \
  --guide-scope full \
  --source-run-id <run_id>
```

Пример: общий guide без привязки к конкретному run.
```bash
python3 -m src.cli deliver \
  --delivery-profile guide_only \
  --output-format md \
  --guide-mode general \
  --guide-scope full
```

Пример: variant-aware guide сразу в PDF.
```bash
python3 -m src.cli deliver \
  --delivery-profile guide_only \
  --output-format pdf \
  --guide-mode variant_aware \
  --guide-scope full \
  --source-run-id <run_id>
```

Пример: `study_pack` с formal report и общим guide.
```bash
python3 -m src.cli deliver \
  --delivery-profile study_pack \
  --output-format bundle_dir \
  --report-scope full \
  --guide-mode general \
  --guide-scope full \
  --source-run-id <run_id>
```

Пример: `print_pack` только для formal report surface.
```bash
python3 -m src.cli deliver \
  --delivery-profile print_pack \
  --output-format bundle_dir \
  --report-scope task1 \
  --source-run-id <run_id>
```

Важные правила `deliver`:
- для variant-aware delivery нужен явный `--source-run-id`;
- `guide_only/general` не требует `--source-run-id`, потому что использует явный baseline [METHODICAL_GUIDE_GENERAL_SOURCE.md](docs/METHODICAL_GUIDE_GENERAL_SOURCE.md), а не run bundle;
- `deliver` использует уже существующий successful run bundle и не вызывает `solve`, `figures` или `report`;
- `guide_only/variant_aware` и `study_pack/variant_aware` работают только для run, который совпадает с текущим frozen guide baseline по `derived_parameters.json` и `out/data/*.json`;
- `guide_only/general` и `study_pack/general` используют отдельный general-guide source и не строятся blind-redaction из variant-aware guide;
- `guide_only/pdf` теперь строится из того же frozen guide baseline, что и `guide_only/md`, через local `pandoc + xelatex`, а не из нового authoring surface;
- `guide_only/general` и `study_pack/general` теперь дополнительно получают delivery-time блок `Режимные оговорки delivery` только для реально присутствующих sensitive sections `1.3`, `1.4`, `2.1`;
- эти regime notes не добавляют новые числа и не притворяются новым guide content: они только запрещают unsafe universal reading для stationary boundary, truncation-sensitive prose и `P_ож` vs queue-state semantics;
- `study_pack/variant_aware` теперь реально включает `report/final_report.pdf`, `report/assets_manifest.json`, `guide/methodical_guide__variant.md`, `guide/methodical_guide__variant.pdf`, scope-aware guide schemes и scope-aware guide plots;
- `guide_only/general` теперь реально включает `guide/methodical_guide__general.md` и `guide/assets/schemes/...`, но не включает `guide/assets/plots/...`;
- `guide_only/pdf` теперь реально включает `guide/methodical_guide__variant.pdf` или `guide/methodical_guide__general.pdf` плюс тот же scope-aware asset set, который уже действует для соответствующего guide mode;
- `study_pack/general` теперь реально включает formal report surface плюс `guide/methodical_guide__general.md`, `guide/methodical_guide__general.pdf` и guide schemes, но без guide plots;
- variant-aware guide delivery в `F02C3` теперь явно валидирует sensitive JSON support: `task_1_3.json` не должен подсовывать метрики для `non_stationary` points, `task_1_4.json` обязан нести truncation metadata/bounds, а `task_2_1.json` обязан сохранять `waiting_probability_interpretation = arrival_weighted_probability_for_new_breakdown`;
- partial-run limitation сохранена явно: `guide_only/full + variant_aware` по-прежнему требует source run с `report_scope='full'`, а не магический fallback;
- `print_pack` в F02C1/F02C2 реально включает `report/final_report.pdf`, `report/final_report.tex`, `report/assets_manifest.json`, `report/assets/...` и scope-aware `figures/...`;
- начиная с `F02F`, copied `report/assets_manifest.json` внутри report-bearing deliveries нормализуется в delivery-local subset: локальные ссылки идут только на `report/...` и `figures/...`, а неупакованные source-run references очищаются до `null` или пустых списков;
- для `study_pack` по frozen contract требуется `guide_scope = report_scope`;
- начиная с `F02I`, `study_pack` дополнительно кладёт guide PDF как internal artifact при сохранении top-level `output_format = bundle_dir`;
- `print_pack` по-прежнему не получает guide PDF copies в текущем runtime slice;
- `docx` по-прежнему намеренно не реализован;
- `print_pack` в текущем v1 остаётся report-centric и не включает guide surface.

## Unified Build + Delivery Session
Если нужен один operator-facing session без отдельного повторного запуска `deliver`, используйте `build --offer-delivery`.

Пример: file-based review, затем optional delivery в той же сессии.
```bash
python3 -m src.cli build \
  --input inputs/examples/student_example.yaml \
  --review \
  --offer-delivery
```

Что поддерживает unified session в `F02E`:
- завершить `build` и выбрать `none`, то есть без дополнительного delivery;
- после `build` собрать `report_only`;
- после `build` собрать `study_pack`;
- после `build` собрать `guide_only`;
- после `build` собрать `print_pack`.

Важные ограничения unified session:
- она переиспользует уже существующие `run_build` и `run_delivery`, а не создаёт новый truth path;
- она не показывает unsupported combinations как будто они работают;
- для report-bearing deliveries `report_scope` внутри session ограничен `report_scope` только что собранного run;
- для `guide_only + variant_aware` в partial run предлагаются только реально допустимые `guide_scope`;
- для `guide_only` unified session теперь показывает `md` и `pdf`, но остальные profiles не получают новых format choices в этом pass;
- `docx` по-прежнему не открыт.

## Required Raw Inputs
Пользователь задаёт только raw fields:
- `student_full_name`
- `student_group`
- `teacher_full_name`
- `journal_number`
- `birth_date`
- `report_scope`

Опционально в file-based input можно явно задать `report_year`, но в нормальном operator path он определяется автоматически по локальной системной дате и не спрашивается интерактивно.

Derived parameters вручную не редактируются и не вводятся.

## What To Edit
- Для запуска по шаблону используйте [inputs/examples/student_example.yaml](inputs/examples/student_example.yaml) как пример формата.
- Для собственного прогона либо:
  - подготовьте свой input file по тому же schema и передайте его в `build --input`;
  - либо используйте `build --interactive`.
- В input file поле `report_scope` принимает только `task1`, `task2` или `full`.
- Если нужно проверить, как файл был нормализован, используйте `build --input ... --review`.
- Если нужно исправить уже введённые интерактивные значения перед сборкой, используйте `edit` на review-шаге.

Не редактируйте вручную, если цель не в аудите/отладке:
- `runs/<run_id>/...`
- `inputs/derived_parameters.json`
- `out/data/*.json`
- `out/artifacts/figure_manifest.json`
- `report/final_report.tex`
- `report/assets_manifest.json`

## Canonical Vs Internal
Канонические operator-facing entrypoints и артефакты:
- `python3 -m src.cli build ...`
- `python3 -m src.cli deliver ...`
- [inputs/examples/student_example.yaml](inputs/examples/student_example.yaml)
- `runs/<run_id>/report/final_report.pdf`
- `runs/<run_id>/run_metadata.json`
- `runs/index.json`
- `deliveries/<delivery_id>/delivery_manifest.json`

Working-set mirrors для совместимости и локального inspection:
- [report/final_report.pdf](report/final_report.pdf)
- [out/artifacts/figure_manifest.json](out/artifacts/figure_manifest.json)
- [report/assets_manifest.json](report/assets_manifest.json)

Нижележащие команды сохранены для аудита и debugging:
- `python3 -m src.cli solve`
- `python3 -m src.cli figures`
- `python3 -m src.cli report`

Исторические и внутренние детали, которые не стоит путать с каноническим usage path:
- текущие root-level `inputs/`, `out/`, `figures/` и `report/` после `P2` являются refreshed working-set mirrors; preserved source of truth for `build` lives under `runs/<run_id>/`;
- текущий [inputs/variant_me.yaml](inputs/variant_me.yaml) в репозитории остаётся working-set mirror; он может быть обновлён новым `build`, но reuse никогда не делается по одному этому файлу или по подмножеству его полей;
- `figures/task_1_1.png`, `figures/task_1_2.png`, `figures/task_1_3.png`, `figures/task_1_4.png`, `figures/task_2_1.png` являются overview PNG, полезными для inspection, но не теми figure files, которые вставляются в финальный отчёт;
- `out/audit/math_lock_checks.json` является closeout audit evidence из `Stage 09A`, а не обязательным runtime artifact для обычного оператора;
- `reports/` хранит stage reports и audit trail, а не runtime outputs.

## Repository Map
- `docs/`: замороженные спецификации и контракт отчёта.
- `inputs/`: raw input artifacts, derived parameters, example input.
- `runs/`: preserved per-run bundles and run registry for high-level `build`.
- `deliveries/`: delivery bundles, assembled only from already existing frozen surfaces.
- `out/data/`: машинно-читаемые solver outputs.
- `out/artifacts/`: figure manifest.
- `out/audit/`: audit evidence, produced only by dedicated verification passes.
- `figures/`: PNG-графики и overview sheets.
- `report/`: итоговый TeX/PDF пакет и scheme assets.
- `src/`: вычислительный, plotting, rendering, intake и CLI код.
- `tests/`: узкие regression tests для вычислителя и orchestration path.
- `reports/`: stage-by-stage execution and audit reports.

## Scope And Non-goals
Текущая цель репозитория ограничена:
- воспроизводимым аналитическим расчётом по учебному варианту;
- генерацией графиков и итогового отчёта;
- operator-friendly intake/build path;
- узким delivery/export layer поверх already built runs и frozen guide baseline.

Вне текущего scope:
- general-purpose queueing toolkit;
- packaging/distribution outside repository workflow;
- изменение solver mathematics без отдельного доказанного основания;
- альтернативная report family или новый визуальный redesign.

## Validation Shortcuts
Проверить CLI help:
```bash
python3 -m src.cli --help
```

Проверить тесты:
```bash
python3 -m unittest discover -s tests -v
```
