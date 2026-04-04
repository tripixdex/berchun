# Report G2F — Guide Surface Consistency + User Voice Pass

## Scope ID and name
- `G2F — Guide Surface Consistency + User Voice Pass`

## Objective
- Снять два remaining user-facing surface defects в current variant-aware guide:
  - локальные места, где prose звучала так, будто график показан прямо здесь, хотя в PDF в этом подпункте вставлен только один опорный plot;
  - неудачную guide voice вроде `в моём варианте` и `постановка преподавателя`.
- Перевыпустить current full user-facing pack через system path без изменения numbers, formulas, checkpoints и guide logic.

## Files created
- `reports/report_G2F_surface_consistency_voice.md`

## Files updated
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/master_report.md`
- regenerated full pack:
  - `deliveries/20260331T130104484834Z__study_pack__full/report/final_report.pdf`
  - `deliveries/20260331T130104484834Z__study_pack__full/guide/methodical_guide__variant.md`
  - `deliveries/20260331T130104484834Z__study_pack__full/guide/methodical_guide__variant.pdf`
  - `deliveries/20260331T130104484834Z__study_pack__full/delivery_manifest.json`

## What graph-surface inconsistencies were fixed
- `1.1`
  - unplotted block renamed from `график занятых операторов` to `зависимость занятых операторов`
  - added a narrow cue that the guide shows one opor graph for the subsection, while `M_зан` is read from the same checkpoint set
- `1.2`
  - added one explicit cue that the PDF shows one opor graph for the subsection and the other families should be read through the same checkpoint values
  - reworded unplotted family prose from `график ...` to `зависимость ...` / `семейство зависимостей ...`
- `1.3`
  - added the same one-graph cue for the subsection
  - reworded unplotted `P_wait` and `M_зан / K_загр` blocks away from immediate-graph wording
  - tightened the local defense cue to `нельзя начинать ... с опорного графика`
- `1.4`
  - added the same one-graph cue for the subsection
  - reworded the unplotted `M_зан / K_загр` block away from immediate-graph wording
- `2.1`
  - added the same one-graph cue for the subsection
  - reworded the unplotted `M_пр / M_ож` and `M_зан / K_загр` blocks away from immediate-graph wording

## What user-facing voice changes were made
- top opening:
  - `постановка преподавателя` -> `постановка задачи`
  - `для текущего варианта` at the main assignment frame -> `для твоего варианта`
- local subsection voice:
  - `Что дано в моём варианте` -> `Что дано в твоём варианте`
  - `В моём варианте` / `Для моего варианта` -> `В твоём варианте` / `Для твоего варианта`
- defense-card prompts:
  - `по моему варианту` -> `по твоему варианту`
- the tone stays direct and student-facing, but not slangy.

## How the full pack was regenerated
- Fresh canonical build:
  - `build --input inputs/variant_me.yaml --runs-dir /tmp/berchun_g2f_runs_clean`
- Fresh delivery:
  - `deliver --runs-dir /tmp/berchun_g2f_runs_clean --source-run-id 20260331T130052226532Z__2aaa6e434b2c --delivery-profile study_pack --output-format bundle_dir --report-scope full --guide-mode variant_aware --guide-scope full`
- Resulting visible pack:
  - `deliveries/20260331T130104484834Z__study_pack__full`

## How it was validated
- Source-level checks:
  - no `постановка преподавателя`
  - no `в моём варианте` / `по моему варианту`
  - numeric token multiset exactly preserved against the previous generated guide markdown
  - formula lines exactly preserved against the previous generated guide markdown
- Automated checks:
  - `python3 -m py_compile src/delivery_guide_pdf.py tests/test_delivery_guide_pdf_runtime.py tests/test_pdf_surface_integrity.py`
  - `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_guide_pdf_runtime tests.test_pdf_surface_integrity tests.test_delivery_validation -v`
- Pack checks:
  - regenerated pack markdown equals current `docs/methodical/content/METHODICAL_GUIDE.md`
  - regenerated guide PDF text contains `Постановка задачи для твоего варианта`
  - regenerated guide PDF no longer contains old voice phrases

## What intentionally remained unchanged
- all numbers
- all formulas
- all checkpoints
- all defense logic
- all graph logic
- all formula-surface additions from `G2E`
- all figure choices and placements
- all section/subsection order
- delivery model and broader export architecture

## Remaining risks
- `G2F` intentionally fixed only current guide-surface voice and graph-consistency defects; it did not open denser figure coverage or broader guide rewrite.
- The guide still deliberately shows only one opor plot per major subsection; if later denser local plot coverage is needed, that must be opened as a separate narrow surface scope.
- This pass touched only the current variant-aware guide source, not the separate general-guide baseline.

## Ready for G3? YES/NO
- `YES`

## Exact recommendation for next step
- Open `G3 — Guide Surface Freeze Review`.
- Keep it narrow: review the current teacher-first, visually supported, navigation-enabled, formula-self-sufficient and now user-voice-normalized guide/report surface as one user-facing artifact set; fix only tiny real inconsistencies if found, without reopening numbers, formulas, checkpoints, guide logic or delivery semantics.
