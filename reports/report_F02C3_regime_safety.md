# Report F02C3 — Regime-Aware General Guide Safety Logic

## Scope ID and Name
- Scope ID: `F02C3`
- Scope name: `Regime-Aware General Guide Safety Logic`

## Objective
Добавить narrow safety policy для guide delivery в regime-sensitive местах без открытия `docx`, UX redesign, solver redesign, formal report redesign или broad methodical rewrite.

## Trusted Inputs Used
- `reports/master_report.md`
- `docs/delivery/DELIVERY_SURFACE_PLAN.md`
- `docs/delivery/DELIVERY_SURFACE_CONTRACT.md`
- `docs/delivery/DELIVERY_OUTPUT_MATRIX.md`
- `reports/report_F02B_delivery_runtime.md`
- `reports/report_F02C1_bundle_population.md`
- `reports/report_F02C2_general_guide.md`
- `docs/methodical/architecture/METHODICAL_GUIDE_CONTRACT.md`
- `docs/methodical/architecture/METHODICAL_ARTIFACT_MAP.md`
- `docs/methodical/content/METHODICAL_GUIDE.md`
- `docs/methodical/content/METHODICAL_GUIDE_GENERAL_SOURCE.md`
- current delivery runtime files
- current formal report baseline artifacts
- current methodical guide baseline artifacts

## Files Created
- `src/delivery_guide_safety.py`
- `tests/test_delivery_safety.py`
- `reports/report_F02C3_regime_safety.md`

## Files Updated
- `src/delivery_population.py`
- `README.md`
- `reports/master_report.md`

## What Safety Logic Was Added Now
- Вынесен отдельный narrow policy module `src/delivery_guide_safety.py`.
- Для `guide_mode = general` delivery-time runtime теперь добавляет блок `Режимные оговорки delivery`, но только для реально присутствующих sensitive sections.
- Для `guide_mode = variant_aware` runtime теперь явно валидирует sensitive artifact support перед копированием guide surface.
- Existing F02B/F02C1/F02C2 guards не ослаблены: `docx` всё ещё запрещён, `study_pack` всё ещё требует `guide_scope = report_scope`, run-backed profiles всё ещё требуют compatible run source.

## Which Regime Classes Are Explicitly Handled
- `1.3` stationary vs non-stationary sensitivity:
  - general guide не выдаёт первую стационарную точку как универсальный факт;
  - variant-aware guide rejects `task_1_3.json`, если non-stationary points несут стационарные metric values;
  - variant-aware guide rejects `task_1_3.json`, если в sweep вообще нет stationary point.
- `1.4` truncation-sensitive explanatory layer:
  - general guide не выдаёт queue shrinkage как безусловное улучшение сервиса;
  - variant-aware guide требует `metadata.truncation_policy` и numeric tail bounds.
- `2.1` waiting-probability vs queue-state semantics:
  - general guide явно оговаривает, что `P_ож` нельзя читать как state-share очереди;
  - variant-aware guide требует `diagnostics.waiting_probability_interpretation = arrival_weighted_probability_for_new_breakdown` и `queue_exists_probability_state`.
- partial-run limitations:
  - explicit rejection для `guide_only/full + variant_aware` от partial run сохранена и отдельно покрыта test case.
- separation between general and variant-aware claims:
  - general delivery не получает checkpoints, run plots или universalized regime claims;
  - variant-aware delivery остаётся artifact-backed и теперь дополнительно проверяет sensitive semantics.

## What Behavior Changed For General vs Variant-aware Delivery
- `guide_only/general` и `study_pack/general` теперь отдают тот же explicit general source, но с локальным safety appendix перед финальным block `Как использовать guide на защите`.
- Appendix не добавляет новые числа и не переписывает frozen guide broadly; он только ограничивает unsafe reading в `1.3`, `1.4`, `2.1`.
- `guide_only/variant_aware` и `study_pack/variant_aware` по-прежнему копируют frozen guide baseline и plots, но теперь заранее проверяют regime-sensitive JSON semantics и fail clearly на drift.

## What Intentionally Remained Unchanged
- `docx`
- unified interactive delivery UX
- delivery-local manifest rewriting
- solver truth, report truth и frozen methodical prose
- `print_pack` as report-centric profile

## Remaining Risks
- General-guide safety layer остаётся rule-based appendix, а не full semantic generalizer; более глубокая language safety outside explicit sensitive sections всё ещё не открывалась.
- `docs/methodical/content/METHODICAL_GUIDE_GENERAL_SOURCE.md` остаётся explicit content baseline; `F02C3` его не переписывал.
- Repo-wide `tests/test_variant_integrity.py` всё ещё содержит historical expectations за пределами delivery branch.

## Ready for F02E?
- `YES`

## Exact Recommendation for Next Step
- Открыть `F02E — Unified Delivery Entrypoint Freeze/Implementation`.
- Ограничить его только unified operator-facing entry contract поверх уже существующих `build` и `deliver`, не переоткрывая solver truth, formal report truth, methodical truth или `docx`.
