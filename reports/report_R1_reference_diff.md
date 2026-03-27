# Scope ID and name
R1 — Reference Diff Map + Reference-Compatible Contract

## Objective
Собрать доказуемую diff-map между accepted reference report и текущим generated report, классифицировать различия по teacher-acceptance risk и заморозить базу для следующих rendering passes без изменения solver mathematics, figures, schemes и pipeline logic.

## Trusted inputs used
- `README.md`
- `reports/master_report.md`
- `report/final_report.pdf`
- `report/final_report.tex`
- `references/DZ1.pdf`
- `src/render/content.py`
- `src/render/report_builder.py`
- `src/render/common.py`
- `src/render/specs.py`
- `docs/SPEC.md`
- `docs/REPORT_CONTRACT.md`
- `reports/report_P1_title_page.md`

## Files created
- `reports/report_R1_reference_diff.md`
- `docs/REFERENCE_COMPAT_CONTRACT.md`

## Files updated
- `reports/master_report.md`

## Full categorized difference map
| Area | Accepted reference | Current generated report | Risk | Why it matters |
| --- | --- | --- | --- | --- |
| Title page | Page 1 reference shows left emblem, thick horizontal separator, year-only bottom block, no variant-data line on cover, and tighter institutional composition. | Page 1 current report is already academic, but still omits emblem and separator rule, keeps extra variant-data line, and uses `Москва, 2026 г.` instead of reference-like year-only footer. | High-risk for teacher acceptance | Это первое визуальное впечатление и одна из самых заметных family-level разниц; текущий титул ближе к reference, но ещё не в его узнаваемой академической конфигурации. |
| Section hierarchy and numbering | Task 1 starts with one section title, далее подпункты подаются как numbered assignment items `1.`, `2.`, `3.`, `4.`; Task 2 likewise starts from task statement rather than explicit template subsection. | Current report uses fixed template `section* + subsection* + subsubsection*`, with visible headings `1.1`, `1.2`, `1.3`, `1.4`, `2.1`. | High-risk for teacher acceptance | Различается не только typography, но и сама логика развёртки материала; teacher sees a template report, а не раскладку, близкую к принятому образцу. |
| Format of task statements / conditions | Reference opens each part with full assignment-style condition text and immediately lists raw values as plain lines (`Tc = ...`, `Ts = ...`, etc.). | Current report uses short model-summary sentences and bullet lists for исходные данные. | High-risk for teacher acceptance | В reference формулировка задачи выглядит как учебное решение по варианту; текущий текст выглядит как краткая техническая спецификация модели. |
| Placement and style of calculation schemes | Reference uses state-transition / chain-of-states schemes with `S_0, S_1, ...`, transition intensities on arcs, and mathematical symbols directly on the scheme. | Current report uses simplified block-diagram PNG schemes with process boxes (“Поток заявок”, “Очередь”, “n операторов...” и т.д.). | High-risk for teacher acceptance | Это одна из главных визуальных и содержательных разниц: accepted reference демонстрирует именно state-based расчётную схему, а не process-flow diagram. |
| Style of displayed derivations/formulas | Reference interleaves formulas, symbol explanations, intermediate manipulations and narrative derivation across multiple pages. | Current report groups formulas into two compact blocks: “Формулы вероятностей состояний” and “Формулы производных метрик”, without extended derivation. | High-risk for teacher acceptance | Даже при корректной математике exposition density заметно отличается; teacher can read current version as under-explained relative to the accepted reference. |
| Figure ordering | Reference usually introduces a formula or metric immediately before the corresponding figure, often one figure at a time or in small page-local groups. | Current report prints scheme, then all formula blocks, then results text, then batches the figures of the subsection. | High-risk for teacher acceptance | Это меняет reading rhythm всего отчёта и делает его structurally unlike the accepted reference even when the figures themselves are valid. |
| Figure captions and numbering style | Reference captions are short, reference-like and tied to local section flow; task 2 also contains an apparent accepted inconsistency in caption order (`2.1`, `2.2`, `2.3`, `2.5`, `2.4`). | Current report uses systematic synthetic captions and monotone numbering such as `1.2.1`, `1.2.2`, ... and `2.1.1`, `2.1.2`, ... | Medium-risk | Caption wording and numbering family visibly differ, but this is less dangerous than scheme/style mismatches; monotone numbering itself should not be intentionally broken just to imitate the reference’s apparent local inconsistency. |
| Final conclusions / summaries | Accepted reference ends after the last figure block of task 2; a separate concluding page was not found. | Current report ends with an extra page `Краткие выводы` summarizing several computed facts. | Medium-risk | Дополнительная conclusion page делает current report менее reference-like, хотя математически сама по себе не конфликтует с accepted scope. |
| 1.1 threshold presentation | Reference task statement explicitly requires the threshold criterion `< 1%`, but the visible reference pages emphasize formulas and figures rather than a separate synthetic conclusion bullet. | Current report states the validated threshold in prose and again repeats it in `Краткие выводы`. | Medium-risk | Сам критерий должен остаться; менять можно только место и style of exposition. Нельзя подменять вычисленный threshold reference-number’ом из чужого варианта. |
| 1.4 truncation exposition style | Reference devotes several pages to the convergence/truncation derivation, explicitly introduces `ε = 10^-6`, derives a bound and a truncation index. | Current report keeps the validated current math but explains truncation in one compact paragraph with `epsilon = 1e-12` and output-derived residual upper bounds. | High-risk | Здесь опасно слепо копировать reference: style should move toward reference, but current validated epsilon and diagnostics must remain authoritative. |
| 2.1 waiting probability interpretation | Reference page 25 presents `P_ож` in the older stationary-state style without an explicit clarification that it is not the same as the stationary share of queue states. | Current report explicitly states that `waiting_probability` is the probability that a newly arriving failed machine must wait, and contrasts it with the stationary queue-state probability. | High-risk | Это semantic divergence, а не косметика: future passes must keep current validated interpretation even while moving the presentation toward the reference family. |
| Document density / pagination | Reference PDF is 28 pages and spreads formulas/figures more granularly. | Current generated PDF is 23 pages and is visibly denser because of subsection templating and grouped figures. | Low-risk | Это скорее следствие других differences, чем самостоятельный acceptance blocker, but it confirms that the current render layer is still structurally more compact than the reference. |

## High-risk mismatches
- Title page family is still not reference-close enough: emblem, separator rule, footer policy and removal of variant-data line remain unresolved.
- The body hierarchy is template-driven instead of reference-driven: numbered assignment items and task-flow structure are not yet mirrored.
- Calculation schemes are the wrong visual family: accepted reference uses state-transition schemes, current report uses process blocks.
- Formula exposition is too compressed relative to the reference: the report states formulas, but does not stage the derivation in the accepted narrative rhythm.
- Figure placement is batch-oriented instead of locally interleaved with the formulas and text they explain.
- Section `1.4` needs reference-like truncation exposition, but without surrendering the current validated `epsilon = 1e-12` and current residual diagnostics.
- Section `2.1` must not regress to the weaker reference-style waiting interpretation; the current arrival-weighted meaning has to survive any stylistic refit.

## What should remain from current system
- Вся validated mathematics and all `out/data/*.json` outputs remain authoritative.
- The current machine-traceable `solve -> figures -> report` pipeline and manifests remain authoritative.
- The current section-level mathematical invariants remain:
  - `1.1` threshold is computed from current solver outputs for the current variant, not copied from the reference;
  - `1.3` non-stationary points stay explicitly marked and must not receive fake stationary values;
  - `1.4` truncation policy stays tied to current validated `epsilon = 1e-12` and current output-derived residual bounds;
  - `2.1` `waiting_probability` remains the probability that a newly arriving failure waits, not the stationary share of queue states.
- Deterministic autofill from canonical raw input remains mandatory.
- Figure data and scheme/data traceability remain mandatory even if the layout is reworked.

## What should be moved toward reference
- Title page family, including emblem/rule hierarchy and more reference-like footer policy.
- Visible body structure: task statement first, numbered problem items, and less template-like subsection scaffolding.
- Condition formatting: full assignment-style wording plus plain-line raw data block instead of terse one-line model summaries and bullet lists.
- Scheme family: state-based / Markov-chain style diagrams with labeled intensities.
- Formula exposition: denser derivation with intermediate explanatory steps, not only compact final formulas.
- Figure placement: closer to the local formulas and discussion they support.
- Conclusion policy: default target should be no separate final conclusion page unless a future explicit scope requires one.

## Exact recommended next pass
`R2 — Reference-Compatible Structural Skeleton`: implement only the high-risk rendering skeleton changes frozen in the new contract, in this order: title-page family, task/item hierarchy, condition formatting, and scheme family. Do not touch solver outputs, figures-as-data, or any mathematical semantics in that pass.
