# Delivery Surface Plan

## Статус и назначение
Этот документ замораживает `F02A — Delivery / Export Surface Architecture Freeze`.

Его задача:
- зафиксировать delivery/export surface как отдельный packaging layer поверх уже frozen truth-bearing baselines;
- развести formal report delivery, methodical delivery и print-oriented packaging;
- сделать следующий implementation pass узким и implementation-ready.

Этот документ не запускает export implementation и не меняет solver/report/methodical truth.

## Зачем это отдельная ветка/scope
- Текущий `build` уже решает другую задачу: он создаёт truth-bearing run bundle из canonical raw input.
- Delivery surface должен не пересчитывать истину, а собирать operator-facing outputs поверх уже успешных baselines.
- Если смешать delivery logic с текущим `build`, быстро исчезнет граница между:
  - truth generation;
  - packaging;
  - editable/export surfaces.
- Отдельный scope позволяет ввести delivery model без reopening solver mathematics, formal report contract и frozen methodical content.

## Что именно считается delivery surface
Delivery surface понимается как слой, который:
- берёт на вход либо успешный run bundle, либо frozen general-methodical baseline;
- собирает из этого operator-facing delivery artifacts;
- раскладывает их в отдельный delivery bundle;
- фиксирует, что именно было выдано, в каком формате и из какого source baseline.

Delivery surface не должен:
- повторно запускать solver как часть packaging semantics;
- переписывать report prose;
- переписывать frozen methodical guide content;
- invent variant-specific or general-study numbers.

## Source-of-truth separation
- `build` остаётся каноническим truth-producing path.
- `deliver` должен стать отдельным packaging path.
- Variant-aware delivery должна опираться на успешный run bundle, а не на случайный working-set snapshot.
- General guide delivery не должна получаться blind-redaction из variant-aware guide; это отдельный general explanatory surface без student-specific чисел.
- Delivery outputs должны жить отдельно от `runs/`: канонический корень для них — `deliveries/<delivery_id>/...`.

## Frozen v1 direction
Для первой delivery family замораживается такой целевой принцип:
- report-bearing surfaces используют уже существующий formal report baseline;
- guide-bearing surfaces используют frozen methodical branch;
- v1 delivery formats ограничиваются `pdf`, `md` и `bundle_dir`;
- `docx` не входит в первый runtime slice и должен идти отдельным follow-up pass после нормализации delivery model.

## Staged Roadmap

### F02B — Delivery Request Model + Bundle Skeleton
Результат:
- вводится отдельная canonical delivery request model;
- появляется `deliveries/<delivery_id>/...` и `delivery_manifest.json`;
- фиксируется runtime validation для `delivery_profile`, `report_scope`, `guide_scope`, `guide_mode`, `output_format`;
- собирается минимальный packaging path поверх уже существующих `pdf` и `md` surfaces.

### F02C — Bundle Profiles + General Guide Surface
Результат:
- появляются profile-aware assemblies для `study_pack` и `print_pack`;
- вводится explicit path для `guide_mode = general`;
- фиксируются copy/include rules для guide/report assets внутри delivery bundle.

### F02D — DOCX Extension For Report-Bearing Profiles
Результат:
- delivery surface получает editable export только как расширение уже нормализованной модели;
- `docx` подключается без переоткрытия delivery concepts и without ad-hoc flags.

## Recommended Implementation Order
1. Сначала ввести отдельный delivery request contract и layout `deliveries/<delivery_id>/...`.
2. Потом собрать минимальные single-surface outputs на уже существующих truths:
   - `report_only` на текущем report PDF;
   - `guide_only` на текущем methodical Markdown.
3. После этого добавить multi-artifact bundles:
   - `study_pack`;
   - `print_pack`.
4. Только затем открывать `guide_mode = general`.
5. `docx` вводить последним как расширение, а не как главный organizing principle всей ветки.

## Почему это не должно переписать solver/report/methodical truth
- Solver truth уже frozen и не должен заново обсуждаться в delivery scope.
- Formal report уже frozen как teacher-facing baseline и остаётся отдельным surface.
- Methodical guide уже frozen как student-facing baseline и не должен скрыто превращаться в delivery contract source для report branch.
- Delivery layer лишь:
  - выбирает нужные frozen surfaces;
  - упаковывает их в нормализованный bundle;
  - описывает operator-facing combination rules.

## Что считается успехом для delivery surface architecture
F02A считается успешным, если после него:
- есть явная delivery model вместо ad-hoc checkbox logic;
- matrix `profile x scope x mode x format` выписан явно;
- следующий implementation pass можно сделать узким, без redesign drift.

## Exact Next Implementation Target
Следующий правильный шаг после F02A:
- `F02B — Delivery Request Model + Bundle Skeleton`.
