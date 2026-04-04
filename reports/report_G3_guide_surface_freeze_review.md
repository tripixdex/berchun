# Report G3 — Guide Surface Freeze Review

## Scope ID and name
- `G3 — Guide Surface Freeze Review`

## Objective
- Честно проверить текущий guide/report set как один user-facing artifact set после накопленных surface passes `G1..G2F`.
- Исправить только tiny real inconsistency, если она действительно мешает freeze.
- Перевыпустить current full visible pack через system path, чтобы freeze verdict опирался на актуальное состояние артефактов.

## Files created
- `reports/report_G3_guide_surface_freeze_review.md`

## Files updated
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `reports/master_report.md`
- regenerated full pack:
  - `deliveries/20260331T132111141738Z__study_pack__full/report/final_report.pdf`
  - `deliveries/20260331T132111141738Z__study_pack__full/guide/methodical_guide__variant.md`
  - `deliveries/20260331T132111141738Z__study_pack__full/guide/methodical_guide__variant.pdf`
  - `deliveries/20260331T132111141738Z__study_pack__full/delivery_manifest.json`

## What was validated
- Guide opening and user voice:
  - teacher-first opening still intact;
  - direct student-facing voice remains consistent;
  - old phrases like `постановка преподавателя`, `в моём варианте`, `для моего варианта` absent in source and regenerated PDF.
- Formula presence and self-sufficiency:
  - local `Почему формула именно такая` blocks still contain the inserted key formulas;
  - formula lines in current source stayed exactly aligned with the previously regenerated guide markdown.
- Graph-surface consistency:
  - the guide still clearly separates one opor plot per subsection from the rest of the checkpoint-read dependencies;
  - no remaining prose was left that falsely promises a local graph where none is shown.
- Typography and navigation:
  - guide support blocks remain visually separate instead of run-in;
  - guide PDF `PageMode = /UseOutlines`, outline count `14`;
  - report PDF `PageMode = /UseOutlines`, outline count `8`.
- De-internalization:
  - no `inputs/`, `out/`, `manifest`, `figure_manifest`, or similar repository/runtime leakage remains in current guide source or regenerated guide PDF.
- Full-pack health:
  - fresh canonical build succeeded with run id `20260331T132059861125Z__2aaa6e434b2c`;
  - fresh delivery succeeded with bundle `deliveries/20260331T132111141738Z__study_pack__full`;
  - regenerated guide markdown is byte-identical to current `docs/methodical/content/METHODICAL_GUIDE.md`.

## What was corrected, if anything
- Found one real tiny surface inconsistency:
  - several local cues still used raw anglophone `guide` inside otherwise Russian user-facing prose.
- Fixed only that:
  - `Ниже в guide ...` -> `Ниже в этом руководстве ...`
  - `Как использовать guide на защите` -> `Как использовать руководство на защите`
- No numbers, formulas, checkpoints, defense logic, graph logic, figure placements, or section order changed.

## Current guide-surface summary
- The current guide/report set now reads as one coherent user-facing artifact set:
  - teacher-first opening;
  - clean direct voice;
  - embedded schemes and selected key plots;
  - visible local support blocks;
  - practical PDF outline navigation;
  - key formulas already integrated into the guide;
  - no internal repository/runtime leakage.
- The guide is now self-sufficient enough for weak-student orientation and defense rehearsal without turning into a duplicate of the formal report.

## Remaining risks
- The current freeze review intentionally covered the current variant-aware guide surface, not a broader redesign of the separate general-guide baseline.
- Guide PDF and report PDF still depend on the local supported `pandoc + xelatex` toolchain; the pass did not open fallback export work.
- The guide still deliberately shows one opor plot per major subsection instead of denser visual packing; this remains a conscious surface choice, not a defect.
- `checkpoint` terminology remains part of the frozen teaching style; this pass did not open a broader terminology rewrite.

## Final verdict: freeze current guide surface now? YES/NO
- `YES`

## Exact recommendation for next step
- Freeze the current guide/report surface now and shift Codex effort away from heavy guide prose work.
- If further work is needed, open a separate non-guide scope on program logic / operator UX / delivery behavior rather than extending guide-surface writing again.
