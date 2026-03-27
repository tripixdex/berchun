# Reference-Compatible Rendering Contract

## Status and purpose
Этот документ замораживает target contract для следующих R-series rendering passes. Его цель: приблизить generated report к accepted reference family (`references/DZ1.pdf`) без изменения validated mathematical core, without touching solver truth, and without breaking the current deterministic pipeline.

## Scope boundary
Этот контракт управляет только presentation/rendering layer:
- title page family;
- document hierarchy and numbering;
- condition formatting;
- scheme style;
- formula exposition;
- figure placement and captions;
- conclusion policy.

Этот контракт не разрешает менять:
- solver mathematics;
- confirmed variant logic;
- machine-readable outputs under `out/data/`;
- figure data content;
- archive/build semantics;
- canonical raw-input semantics.

## Canonical target family
Target family for future passes is:
- visually and structurally much closer to `references/DZ1.pdf`;
- mathematically authoritative according to the current validated repository outputs;
- deterministic and reproducible from canonical raw input and existing pipeline artifacts.

## Title-page contract
Future passes must target the following title-page family:
- ministry/university heading in the accepted reference family;
- left institutional emblem and horizontal separator rule under the university block;
- faculty and department lines as separate high-level rows;
- centered work title and course block;
- right-aligned student/group/teacher block;
- bottom centered year-only footer in the reference family.

Additional rules:
- variant-specific raw data must not appear on the cover page;
- personal metadata must continue to autofill from canonical raw input;
- no decorative redesign, no modernized styling, no non-academic layout experiments.

## Section ordering and numbering contract
Future passes must preserve the current mathematical task order but display it in a reference-compatible hierarchy:
1. Title page.
2. `Задача №1. Проектирование Call-центра.`
3. Under task 1, visible problem items in the reference family: `1.`, `2.`, `3.`, `4.` rather than template-like subsection scaffolding.
4. `Задача №2. Проектирование производственного участка.`
5. Under task 2, visible condition block in the reference family; figure/formula numbering may still use the `2.1.*` family internally if needed for consistency.

Additional rules:
- caption numbering must remain monotone and deterministic;
- the accepted reference’s apparent local caption-order inconsistency in task 2 must not be copied intentionally.

## Condition / statement formatting policy
Each task item must begin with a fuller assignment-style statement aligned to the accepted reference, not only with a short model label.

Required policy:
- statement text should resemble the educational/task wording of the reference;
- raw values must be shown as a plain `Исходные данные:` block on separate lines;
- the condition block must precede the scheme and derivation;
- any numeric fact in the statement/condition block must still come from canonical raw input or derived artifacts, not from manual hardcoding.

## Scheme style policy
Future passes must move schemes toward the accepted reference family:
- state-based / Markov-chain style diagrams;
- visible states and transition intensities on the diagram itself;
- scheme placed immediately after the condition block;
- scheme caption in the local task numbering family.

Forbidden scheme behavior:
- replacing state schemes with generic business-process block diagrams;
- inventing new modeling semantics not present in the validated solver.

## Displayed derivation policy
Future passes must move formula presentation toward the reference’s exposition density while preserving current mathematics.

Required policy:
- formulas and explanatory text must be interleaved in smaller local blocks;
- symbol meanings and intermediate steps should appear near the formulas they support;
- the current two-block pattern (“state formulas”, then “metric formulas”) may be split or restaged to match the reference family better;
- presentation may become longer and more stepwise, but must not introduce new mathematical claims unsupported by current validated outputs.

Special semantic rules:
- `1.1`: the threshold criterion `P_отк < 0.01` must remain computed from current solver outputs for the current variant;
- `1.3`: non-stationary points must remain explicitly marked and must not receive fabricated stationary values;
- `1.4`: truncation exposition may adopt a reference-like derivation block, but must keep the current validated `epsilon = 1e-12` and the current output-derived residual bounds as the authoritative numbers;
- `2.1`: the current arrival-weighted meaning of `waiting_probability` must remain explicit, even if the surrounding exposition is reshaped toward the reference.

## Figure placement and caption policy
Future passes must preserve the current validated figures-as-data but change placement/style toward the accepted reference:
- figures should appear near the formula or explanation that motivates them;
- large figure batches after a whole subsection should be avoided where reference-like local placement is feasible;
- caption wording should move toward the concise educational style of the reference;
- figure numbering must remain deterministic and monotone;
- no figure may be detached from its underlying current JSON artifact source.

## Conclusion policy
Default target for reference-compatibility:
- no separate final `Краткие выводы` page.

If a future explicit scope reintroduces a conclusion, it must satisfy all of the following:
- be shorter than the current closeout page;
- introduce no new facts;
- remain optional relative to the reference-compatible baseline.

## What must remain mathematically from the current system
The following are frozen and must survive any future rendering pass:
- current solver outputs and their traceability chain;
- current validated section semantics;
- current canonical raw-input autofill;
- current figure counts and data provenance;
- current `1.4` truncation epsilon and diagnostics;
- current `2.1` waiting-probability interpretation;
- current `1.3` stationarity boundary handling.

## What must follow the reference even if the current system is already cleaner
The following should be changed toward the reference even if the current templated report is arguably cleaner or more systematic:
- title-page family;
- assignment-style condition wording;
- plain-line raw-data presentation instead of bullet-heavy input blocks;
- state-based scheme family;
- denser local derivation exposition;
- local formula-to-figure flow;
- omission of the extra final conclusion page by default.

## Forbidden changes for future passes
Future R-series implementation passes must not:
- change solver code to imitate reference numbers;
- copy variant-specific numeric results from the accepted reference;
- weaken current validated semantics where the reference is mathematically less explicit or less correct;
- change figure data or JSON truth without a separate validated math scope;
- silently alter build/archive/intake behavior while doing rendering work;
- blur the separation between current validated mathematics and reference-style presentation.
