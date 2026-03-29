# MVP Polish Plan

## Статус и назначение
Текущий berchun MVP уже обладает сильной математической базой, воспроизводимым `build -> solve -> figures -> report` контуром и teacher-facing PDF, пригодным для сдачи. Цель этого плана не в доработке solver core, а в заморозке узкого polish-roadmap для повышения качества именно преподавательского чтения текущего отчёта.

Далее под `P1`, `P2`, `P3`, `P4` понимаются новые MVP-polish passes. Они не переопределяют исторические post-closeout scopes с теми же буквенными индексами.

## Позиционирование в общем roadmap
- Этот файл покрывает только `Polish Branch`.
- Более широкая post-freeze feature-ветка зафиксирована отдельно в `docs/GLOBAL_ROADMAP.md`.
- `Polish Branch` и `Feature Branch` не должны смешиваться в одном Codex-pass.
- Если owner меняет приоритет и уводит работу из polish-ветки, это должно оформляться как отдельный новый scope, а не как скрытый drift внутри `P1`–`P4`.

## Текущее состояние MVP
- Канонический pipeline и математическая правда уже зафиксированы.
- Текущий PDF структурно близок к accepted reference: академический титул, иерархия задач, state-based схемы, локальная связка формул и графиков уже присутствуют.
- числовые значения в тексте, пояснениях и notes часто показываются с избыточной точностью;
- блоки `Исходные данные` корректны, но ещё не выглядят как жёстко замороженный элемент страницы;
- после схем остаётся неравномерная подача обозначений и смыслов переменных;
- `1.3` уже честно отделяет нестационарную область, но её визуальная подача ещё не зафиксирована как final policy;
- family plots остаются читаемыми, но по ощущению всё ещё выглядят «сгенерированными», а не спокойно-учебными;
- derivation flow остаётся более систематизированным и компрессированным, чем в accepted reference, особенно в `1.1`, `1.4` и `2.1`.

## Приоритетный polish backlog

### Приоритет 1. Общие teacher-facing правила отображения
- Ограничить обычные teacher-facing числа максимум тремя знаками после запятой.
- Зафиксировать единый визуальный шаблон для `Исходные данные`.
- Ввести обязательный локальный блок обозначений после каждой схемы.
- Заморозить политику показа нестационарной области в `1.3`.

Почему это первое:
- это самые широкие по охвату и самые дешёвые по риску улучшения;
- они влияют сразу на текст, схемы, captions и plots;
- без этих правил дальнейшая полировка будет расползаться стилистически.

### Приоритет 2. Читаемость графиков
- Исключить любое наложение легенд на графики.
- Упростить внутренние plot titles там, где caption уже несёт идентификацию.
- Сделать family plots визуально спокойнее и последовательнее.
- Свести non-stationary marking в `1.3` к одной понятной и неагрессивной visual convention.

Почему это второе:
- это чисто teacher-facing improvement без риска задеть математику;
- визуальная читаемость графиков сейчас заметнее всего отличает generated PDF от reference-family чтения.

### Приоритет 3. Локальный derivation flow
- Разбить плотные формульные блоки на более короткие шаги.
- Добавить поясняющие мостики между формулами и графиками.
- Сделать derivation rhythm более последовательным и «учебным».
- Обязать локальные числовые checkpoint-фразы после ключевых выводов.

Почему это третье:
- эта работа уже зависит от замороженных numeric/plot rules;
- она самая объёмная и её лучше делать поверх уже стабилизированных presentation primitives.

## Стадийный план реализации

### P1 — Numeric Display + Local Notation Hygiene
Ожидаемый результат:
- teacher-facing числа, `Исходные данные` и блоки обозначений приводятся к одному frozen стилю;
- presentation rules начинают исполняться уже в text/render layer.

В scope:
- numeric display policy для teacher-facing текста, captions, notes и variable lines;
- единый вид блока `Исходные данные`;
- обязательный локальный блок `Обозначения:` сразу после схем;
- выравнивание локальных пояснений переменных под текущие section items.

Вне scope:
- переработка plot skin;
- массовая перестановка графиков;
- переписывание derivation flow по всему отчёту;
- любые изменения solver truth, `out/data`, run archive или build semantics.

### P2 — Plot Readability + Non-Stationary Visual Policy
Ожидаемый результат:
- plots становятся спокойнее, чище и ближе к reference-family по читаемости;
- легенды, shading и captions перестают визуально спорить с данными.

В scope:
- policy `no legend overlap`;
- единая постановка legends/titles/notes;
- финальная визуальная convention для `1.3` non-stationary area;
- microfit axes/grid/line hierarchy без изменения data truth.

Вне scope:
- изменение figure data, series content, scheme semantics или solver outputs;
- плотная переработка derivation prose.

### P3 — Task 1 Sequential Derivation Reflow
Ожидаемый результат:
- разделы `1.1`–`1.4` читаются более последовательно и ближе к reference;
- формулы, пояснения, checkpoints и графики идут в более естественном учебном ритме.

В scope:
- restaging derivations и nearby explanation text внутри `1.1`–`1.4`;
- локальные числовые checkpoint-фразы;
- выравнивание dense spots, прежде всего в `1.1` и `1.4`;
- более явное объяснение перехода от распределения состояний к метрикам.

Вне scope:
- `2.1`;
- изменение plot data, scheme family или task hierarchy;
- переоткрытие math/external-audit scope.

### P4 — Task 2 Readability + Final Teacher-Facing Microfit
Ожидаемый результат:
- `2.1` приведён к тому же уровню human readability;
- весь отчёт проходит финальную teacher-facing сводку без переоткрытия math/workflow scope.

В scope:
- reflow `2.1`, включая аккуратную подачу `waiting_probability`;
- final caption/prose microfit по всему PDF;
- финальная проверка соответствия `REPORT_PRESENTATION_CONTRACT`.

Вне scope:
- solver redesign;
- новый feature work;
- task1/task2 split modes, DOCX export, bot/platform expansion.

## Рationale порядка
- `P1` идёт первым, потому что задаёт presentation primitives для всех следующих правок.
- `P2` идёт вторым, потому что plots легче проверять изолированно и их лучше стабилизировать до массовой reflow-работы по тексту.
- `P3` идёт после этого, потому что readability reflow в Task 1 должен опираться на уже замороженные formatting и plot conventions.
- `P4` закрывает цикл на `2.1` и выполняет финальную teacher-facing доводку без переоткрытия математики.

## Что не входит в этот roadmap
- изменение solver mathematics;
- изменение `out/data` truth или figure data;
- перестройка intake/build/archive semantics;
- broader post-freeze feature work, вынесенный в `docs/GLOBAL_ROADMAP.md`;
- косметический cleanup репозитория вне teacher-facing report layer.

## Архитектурное ограничение для следующих passes
- Следующие polish-passes должны оставаться rendering-local.
- `src/render/section_flow.py`, `src/plots/common.py` и `src/render/content.py` уже близки к soft/hard limits, поэтому новые правки должны по возможности идти через маленькие support-files или локальные helper splits, а не через бесконтрольное наращивание этих модулей.

## Критерий завершения roadmap
Roadmap считается замороженным, если:
- приоритеты teacher-facing polish расставлены;
- boundaries следующих passes явно заданы;
- следующий pass очевиден и не требует заново обсуждать presentation rules.
