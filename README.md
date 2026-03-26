# Analytical Queueing Coursework Repository

## Purpose
Репозиторий воспроизводимо строит аналитическое решение и итоговый отчёт по двум учебным задачам:
- задача 1: проектирование call-центра;
- задача 2: проектирование производственного участка.

Канонический пользовательский путь с `Stage 07` и далее: один raw-input intake, затем детерминированный проход `solve -> figures -> report`.

## Canonical Workflow
Для обычной работы используйте только команду `build`.

Файловый режим:
```bash
python3 -m src.cli build --input inputs/examples/student_example.yaml
```

Интерактивный режим:
```bash
python3 -m src.cli build --interactive
```

Если не переопределять пути, команда `build` запишет:
- raw input: `inputs/variant_me.yaml`
- derived parameters: `inputs/derived_parameters.json`
- solver outputs: `out/data/*.json`
- figures: `figures/*.png`
- figure manifest: `out/artifacts/figure_manifest.json`
- report source: `report/final_report.tex`
- final PDF: `report/final_report.pdf`
- report manifest: `report/assets_manifest.json`

Изолированный прогон без перезаписи канонического пакета можно сделать так:
```bash
python3 -m src.cli build \
  --input inputs/examples/student_example.yaml \
  --variant-path /tmp/berchun_run/inputs/variant_me.yaml \
  --derived-path /tmp/berchun_run/inputs/derived_parameters.json \
  --out-dir /tmp/berchun_run/out/data \
  --figures-dir /tmp/berchun_run/figures \
  --manifest-path /tmp/berchun_run/out/artifacts/figure_manifest.json \
  --report-source-path /tmp/berchun_run/report/final_report.tex \
  --report-pdf-path /tmp/berchun_run/report/final_report.pdf \
  --report-assets-manifest-path /tmp/berchun_run/report/assets_manifest.json
```

## Required Raw Inputs
Пользователь задаёт только raw fields:
- `student_full_name`
- `student_group`
- `teacher_full_name`
- `journal_number`
- `birth_day`
- `birth_month`
- `birth_year`
- `report_year`

Derived parameters вручную не редактируются и не вводятся.

## What To Edit
- Для запуска по шаблону используйте [inputs/examples/student_example.yaml](inputs/examples/student_example.yaml) как пример формата.
- Для собственного прогона либо:
  - подготовьте свой input file по тому же schema и передайте его в `build --input`;
  - либо используйте `build --interactive`.

Не редактируйте вручную, если цель не в аудите/отладке:
- `inputs/derived_parameters.json`
- `out/data/*.json`
- `out/artifacts/figure_manifest.json`
- `report/final_report.tex`
- `report/assets_manifest.json`

## Canonical Vs Internal
Канонические operator-facing entrypoints и артефакты:
- `python3 -m src.cli build ...`
- [inputs/examples/student_example.yaml](inputs/examples/student_example.yaml)
- [report/final_report.pdf](report/final_report.pdf)
- [out/artifacts/figure_manifest.json](out/artifacts/figure_manifest.json)
- [report/assets_manifest.json](report/assets_manifest.json)

Нижележащие команды сохранены для аудита и debugging:
- `python3 -m src.cli solve`
- `python3 -m src.cli figures`
- `python3 -m src.cli report`

Исторические и внутренние детали, которые не стоит путать с каноническим usage path:
- текущий [inputs/variant_me.yaml](inputs/variant_me.yaml) в репозитории остаётся historical confirmed artifact для прежнего validated variant; новый `build` может перезаписать этот путь своим raw input, если использовать default outputs;
- `figures/task_1_1.png`, `figures/task_1_2.png`, `figures/task_1_3.png`, `figures/task_1_4.png`, `figures/task_2_1.png` являются overview PNG, полезными для inspection, но не теми figure files, которые вставляются в финальный отчёт;
- `out/audit/math_lock_checks.json` является closeout audit evidence из `Stage 09A`, а не обязательным runtime artifact для обычного оператора;
- `reports/` хранит stage reports и audit trail, а не runtime outputs.

## Repository Map
- `docs/`: замороженные спецификации и контракт отчёта.
- `inputs/`: raw input artifacts, derived parameters, example input.
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
- operator-friendly intake/build path.

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
