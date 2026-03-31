# Report G2A — Teacher Baseline Front Matter Pass

## Scope ID and name
- `G2A — Teacher Baseline Front Matter Pass`

## Objective
- Перестроить только opening/front matter guide так, чтобы guide начинался с teacher-origin постановки задания и блока `Исходные данные`, уже адаптированных к текущему варианту.
- Сохранить downstream guide body, numbers, formulas, checkpoints и defense logic без дрейфа.
- Синхронизировать текущий visible guide artifact с новым opening.

## Files created
- `reports/report_G2A_teacher_front_matter.md`

## Files updated
- `docs/METHODICAL_GUIDE.md`
- `deliveries/20260330T233806934237Z__study_pack__full/guide/methodical_guide__variant.md`
- `deliveries/20260330T233806934237Z__study_pack__full/guide/methodical_guide__variant.pdf`
- `reports/master_report.md`

## What front-matter was changed
- Removed the old self-explanatory opening that started from `Что это за guide...` and `Мой вариант и откуда взялись числа`.
- Added a new top-level section `Постановка преподавателя для текущего варианта`.
- Added two teacher-first front-matter blocks:
  - `Задача 1. Что именно задано`
  - `Задача 2. Что именно задано`
- In each block:
  - restated what the teacher originally asks,
  - showed the current variant values,
  - kept the same derived intensities and load values,
  - added simple student-facing meanings for the key variables.
- Replaced the old intro transition with `Как этим руководством пользоваться дальше`, so the guide now goes from teacher framing to explanatory methodical body in a cleaner order.

## How `my_var.md` / teacher baseline was incorporated
- `my_var.md` was used as the canonical teacher-origin baseline for:
  - the task framing of call-center and production-area problems,
  - the original `Исходные данные` logic,
  - the list of regimes/subtasks the teacher expects.
- The guide opening was adapted from that baseline into user-facing wording for the current variant only.
- No repository/runtime provenance was introduced; the opening now speaks only about the assignment, the current variant, the calculations, and the resulting report/graphs.

## What intentionally remained unchanged
- All numbers.
- All formulas.
- All checkpoints.
- All defense logic.
- All graph-reading logic.
- All section/subsection order after `## Как читать схемы, обозначения, формулы и графики`.
- All figures and figure references.
- Delivery/runtime design and export logic.

## Remaining risks
- This pass changed only the front matter of the current guide baseline; later stylistic compression of the whole opening was intentionally not opened.
- The visible synced artifact is the current `variant_aware` study-pack guide; broader historical artifact sweep was intentionally not opened here.
- PDF layout/pacing around the new front matter was left as-is; any further visual tightening should be a separate narrow pass.

## Ready for G2B? YES/NO
- `YES`

## Exact recommendation for next step
- Open `G2B — Guide Opening Compression + Navigation Pass`.
- Keep it narrow: compress only the now teacher-first opening so that it stays clearer and shorter for a weak student, add only minimal navigation help if needed, and do not change numbers, formulas, checkpoints, downstream guide body, or delivery semantics.
