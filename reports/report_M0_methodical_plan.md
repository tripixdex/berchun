# Report M0 — Methodical Guide Roadmap Freeze

## Scope ID and Name
- Scope ID: `M0`
- Scope name: `Methodical Guide Roadmap Freeze`

## Objective
Заморозить purpose, boundaries, contract и staged roadmap для новой отдельной methodical guide branch, которая объясняет курсовую очень простым русским языком, опирается на реальный вариант и реальные вычисленные значения и помогает устной защите.

## Trusted Inputs Used
- `reports/master_report.md`
- `report/final_report.pdf` — существование текущего PDF verified; text extraction не выполнен, потому что в окружении отсутствует `pdftotext`
- `report/final_report.tex` — использован как доступная teacher-facing structure surface текущего отчёта
- `docs/governance/WORK_PROTOCOL.md`
- `docs/governance/GLOBAL_ROADMAP.md`
- `docs/report/REPORT_CONTRACT.md`
- `docs/report/REPORT_PRESENTATION_CONTRACT.md`

## Files Created
- `docs/methodical/architecture/METHODICAL_GUIDE_PLAN.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `reports/report_M0_methodical_plan.md`

## Files Updated
- `reports/master_report.md`

## Commands Run
- `sed -n '1,260p' reports/master_report.md`
- `sed -n '1,260p' docs/governance/GLOBAL_ROADMAP.md`
- `sed -n '1,260p' docs/governance/WORK_PROTOCOL.md`
- `sed -n '1,260p' docs/report/REPORT_CONTRACT.md`
- `sed -n '1,260p' docs/report/REPORT_PRESENTATION_CONTRACT.md`
- `pdftotext report/final_report.pdf - | sed -n '1,220p'` — failed because `pdftotext` is unavailable in the current environment
- `rg -n '^\\\\(section|subsection|chapter|title|tableofcontents)' report/final_report.tex` — initial section-scan attempt did not return usable output
- `sed -n '1,220p' report/final_report.tex`
- `sed -n '220,520p' report/final_report.tex`
- `ls -l report/final_report.pdf report/final_report.tex`
- `rg -n '^\\section\\*|^\\section\\*\\{Задача №2' report/final_report.tex`
- `sed -n '100,178p' reports/master_report.md`
- `sed -n '1,120p' reports/report_M0_methodical_plan.md`

## What Was Defined Now
- Зафиксировано, что methodical guide branch является отдельной веткой поверх formal report baseline и не заменяет teacher-facing report.
- Зафиксирован target reader: очень слабый студент почти без опоры на теорию.
- Заморожены две главные цели guide:
  - learning goal — объяснить логику решения шаг за шагом;
  - defense goal — помочь коротко и уверенно проговорить решение по своему варианту.
- Зафиксирован future generation target: guide должен быть variant-aware и собираться по реальным student-specific данным и вычисленным артефактам.
- Заморожен content contract: порядок объяснения, mandatory subsection blocks, policy для формул, policy для графиков и обязательный defense layer.

## Frozen Roadmap For The Methodical Branch
- `M1 — Methodical Section Skeleton + Artifact Mapping`
- `M2 — Variant-Aware Core Explanation Generation`
- `M3 — Defense Layer Integration`
- `M4 — End-to-End Assembly + Consistency Validation`

## Why A Variant-Aware Guide Is The Right Target
- Защищать нужно собственный вариант, поэтому generic guide без variant-specific чисел быстро превращается в чужой шаблон.
- Реальные значения варианта позволяют объяснять не только формулы, но и конкретные точки на графиках и конкретные выводы.
- Variant-aware generation уменьшает риск расхождения между guide и formal report.
- Именно слабому студенту важнее всего видеть свои данные, а не обезличенный пример.

## Validation
- Scope является `planning-only` / `documentation-only`.
- Проверено наличие и читаемость trusted input docs.
- Проверено наличие текущих `report/final_report.pdf` и `report/final_report.tex`.
- Teacher-facing structure текущего отчёта просмотрена по `report/final_report.tex`.
- Новых runtime claims, implementation claims и validation claims не добавлялось.

## Remaining Risks / Not Done
- Реализация methodical guide не начиналась и остаётся вне scope M0.
- Канонический export surface будущего guide пока специально не зафиксирован глубже content/generation contract.
- M0 не исправляет и не отменяет существующие formal report branch findings из `V2`; это отдельная линия работы.

## Ready for M1?
- `YES`

## Exact Recommendation For Next Step
- Открыть `M1 — Methodical Section Skeleton + Artifact Mapping` как первый implementation-oriented pass новой methodical branch.
- В `M1` ограничиться только skeleton-level структурой и точной artifact map для `1.1`, `1.2`, `1.3`, `1.4`, `2.1`, не начиная ещё prose generation beyond the frozen template.
