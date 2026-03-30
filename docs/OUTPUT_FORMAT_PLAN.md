# Output Format Plan

## Статус и назначение
Этот документ замораживает `F02G — Output Format Expansion Freeze`.

Его задача:
- зафиксировать output-format expansion как отдельный explicit scope поверх уже работающего delivery layer;
- развести format work от solver truth, formal report truth и frozen methodical content;
- сделать следующий implementation pass узким и безопасным.

Этот документ не реализует новые exporters и не меняет текущие runtime combinations.

## Почему это отдельный scope
- Текущий delivery runtime уже стабилизирован на `pdf`, `md` и `bundle_dir`.
- Расширение форматов легко превращается в скрытый redesign, если не развести:
  - single-surface outputs;
  - multi-artifact bundles;
  - editable/exportable copies.
- `docx` и дополнительные `pdf` surfaces требуют отдельных conversion paths и toolchain assumptions.
- Без отдельной freeze-фазы операторский UX быстро деградирует в ad-hoc набор format toggles.

## Что считается output-format expansion
Output-format expansion понимается как controlled расширение delivery surface для уже существующих artifacts:
- formal report surface;
- methodical guide surface;
- multi-artifact delivery bundles.

Это расширение не должно:
- пересчитывать solver truth;
- переписывать formal report prose;
- переписывать frozen methodical guide content;
- менять delivery profiles или unified session semantics без отдельного explicit scope.

## Separation From Truth-Bearing Layers
- `build` остаётся единственным truth-producing path.
- `deliver` остаётся packaging path.
- Output-format expansion работает только поверх уже frozen surfaces:
  - report PDF / TeX baseline;
  - methodical guide Markdown baselines;
  - existing delivery bundles.
- Новый format не должен становиться новым источником истины. Он только представляет уже существующий frozen surface в другом operator-facing виде.

## Current Baseline Before Expansion
- Formal report уже реально поддерживается как `pdf`.
- Methodical guide уже реально поддерживается как `md`.
- Multi-artifact deliveries уже реально поддерживаются как `bundle_dir`.
- `docx` frozen как concept, но не реализован.
- Guide `pdf` ещё не открыт даже как planning-backed runtime target.

## Frozen Expansion Direction
- Для formal report целевой format family: `pdf`, `docx`.
- Для methodical guide целевой format family: `md`, `pdf`, `docx`.
- Для multi-artifact deliveries canonical container family остаётся: `bundle_dir`.
- Для bundles новые formats должны добавляться как включённые artifacts внутри bundle, а не как повод отменять `bundle_dir` как top-level output.

## v1 / v2 Boundary

### Current mandatory baseline
- `report_only -> pdf`
- `guide_only -> md`
- `study_pack -> bundle_dir`
- `print_pack -> bundle_dir`

### Next safe expansion target
- `guide_only -> pdf` для `variant_aware` и `general`

### Deferred beyond the next runtime slice
- `report_only -> docx`
- `guide_only -> docx`
- bundle-level inclusion rules for additional `docx` copies
- any zip/archive container work

## Staged Roadmap

### F02H — Guide PDF Runtime
Результат:
- появляется explicit guide PDF runtime поверх existing Markdown baselines;
- поддерживаются `guide_only + variant_aware + pdf` и `guide_only + general + pdf`;
- unified session начинает показывать `pdf` только для `guide_only`, когда runtime действительно готов.

### F02I — Study Pack Format Enrichment
Результат:
- `study_pack` остаётся `bundle_dir`;
- после готовности guide PDF bundle может включать guide Markdown и guide PDF как internal artifacts;
- delivery request model не меняется: top-level `output_format` остаётся `bundle_dir`.

### F02J — Report DOCX Runtime
Результат:
- появляется explicit `report_only + docx`;
- source-of-truth separation сохраняется: DOCX остаётся export copy поверх formal report baseline, а не новым editable origin.

### F02K — Guide DOCX Runtime
Результат:
- появляется `guide_only + docx`;
- bundle inclusion of guide DOCX обсуждается только после стабильного single-surface runtime.

## Recommended Implementation Order
1. Сначала открыть `guide_only + pdf`.
2. Затем, при необходимости, добавить guide PDF внутрь `study_pack`, не меняя `bundle_dir` как top-level format.
3. После этого отдельно открыть `report_only + docx`.
4. Только затем обсуждать `guide_only + docx`.

## Why This Order Is Smallest And Safest
- Guide already has Markdown baseline, so PDF export можно строить поверх существующего surface без вмешательства в formal report pipeline.
- `study_pack` already carries guide artifacts, поэтому bundle enrichment after guide PDF — локальное packaging extension.
- Report DOCX заметно сложнее: formal report baseline опирается на TeX/PDF family и не должен получать случайный lossy shortcut.
- Guide DOCX стоит открывать последним, чтобы не раздувать сразу две новые conversion families.

## What This Scope Explicitly Does Not Decide
- конкретный exporter/toolchain command;
- dependency installation policy;
- zip packaging;
- redesign unified operator prompts beyond showing only valid formats.

## Exact Next Implementation Target
Следующий правильный шаг после F02G:
- `F02H — Guide PDF Runtime`.
