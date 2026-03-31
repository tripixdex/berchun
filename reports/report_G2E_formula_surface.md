# Report G2E — Guide Formula Surface Integration

## Scope ID and name
- `G2E — Guide Formula Surface Integration`

## Objective
- Сделать current variant-aware guide математически самодостаточнее, не превращая его во второй formal report.
- Вставить только минимально нужные формулы в `1.1`, `1.2`, `1.3`, `1.4`, `2.1` и сразу дать после них короткие plain-language explanations.
- Перевыпустить current full user-facing pack через system path, чтобы visible report+guide artifacts уже отражали это усиление.

## Files created
- `reports/report_G2E_formula_surface.md`

## Files updated
- `docs/METHODICAL_GUIDE.md`
- `src/delivery_guide_pdf.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `reports/master_report.md`
- regenerated full pack:
  - `deliveries/20260331T123703755294Z__study_pack__full/report/final_report.pdf`
  - `deliveries/20260331T123703755294Z__study_pack__full/guide/methodical_guide__variant.md`
  - `deliveries/20260331T123703755294Z__study_pack__full/guide/methodical_guide__variant.pdf`
  - `deliveries/20260331T123703755294Z__study_pack__full/delivery_manifest.json`

## Which formulas were added where
- `1.1`
  - `a = \lambda / \mu`
  - `p_0 = (\sum_{k=0}^{n} a^k / k!)^{-1}`
  - `p_k = (a^k / k!) p_0`
  - `P_{\mathrm{отк}} = p_n`
  - `M_{\mathrm{зан}} = \sum_{k=0}^{n} k p_k`
  - `K_{\mathrm{загр}} = M_{\mathrm{зан}}/n`
- `1.2`
  - `a = \lambda / \mu`, `\rho_n = \lambda /(n\mu)`
  - `p_0 = (\sum_{k=0}^{n} a^k/k! + a^n/n! \sum_{r=1}^{m}\rho_n^r)^{-1}`
  - `p_k = (a^k / k!) p_0`
  - `p_{n+r} = (a^n / n!) \rho_n^r p_0`
  - `P_{\mathrm{отк}} = p_{n+m}`
  - `M_{\mathrm{зан}} = \sum_{k=0}^{n+m}\min(k,n)p_k`
  - `K_{\mathrm{загр}} = M_{\mathrm{зан}}/n`
  - `P_{\mathrm{оч}} = \sum_{k=n+1}^{n+m}p_k`
  - `L_{\mathrm{оч}} = \sum_{k=n+1}^{n+m}(k-n)p_k`
  - `K_{\mathrm{мест}} = L_{\mathrm{оч}}/m`
- `1.3`
  - `a = \lambda / \mu`, `\rho_n = \lambda /(n\mu)`
  - `p_0 = (\sum_{k=0}^{n-1} a^k/k! + a^n/[n!(1-\rho_n)])^{-1}`
  - `P_{\mathrm{wait}} = a^n/[n!(1-\rho_n)] \, p_0`
  - `M_{\mathrm{зан}} = a`
  - `K_{\mathrm{загр}} = a/n`
  - `P_{\mathrm{оч}} = P_{\mathrm{wait}} \rho_n`
  - `L_{\mathrm{оч}} = P_{\mathrm{wait}}\rho_n/(1-\rho_n)`
- `1.4`
  - `\nu = 1/T_w`, `\beta_k = \lambda`
  - `\delta_k = \min(k,n)\mu + \max(k-n,0)\nu`
  - `p_k = p_{k-1}\beta_k/\delta_k`
  - `p_0 = (1 + \sum_{k=1}^{\infty}\prod_{i=1}^{k}\beta_i/\delta_i)^{-1}`
  - `M_{\mathrm{зан}} = \sum_{k=0}^{\infty}\min(k,n)p_k`
  - `K_{\mathrm{загр}} = M_{\mathrm{зан}}/n`
  - `P_{\mathrm{оч}} = \sum_{k=n+1}^{\infty} p_k`
  - `L_{\mathrm{оч}} = \sum_{k=n+1}^{\infty}(k-n)p_k`
- `2.1`
  - `\lambda_i = (N-i)\lambda`
  - `\mu_i = \min(i,r)\mu`
  - `p_i = p_{i-1}\lambda_{i-1}/\mu_i`
  - `p_0 = (1 + \sum_{i=1}^{N}\prod_{j=1}^{i}\lambda_{j-1}/\mu_j)^{-1}`
  - `M_{\mathrm{пр}} = \sum_{i=0}^{N} i p_i`
  - `M_{\mathrm{ож}} = \sum_{i=0}^{N}\max(i-r,0)p_i`
  - `P_{\mathrm{ож}} = \frac{\sum_{i=r}^{N-1}(N-i)p_i}{\sum_{i=0}^{N-1}(N-i)p_i}`
  - `M_{\mathrm{зан}} = \sum_{i=0}^{N}\min(i,r)p_i`
  - `K_{\mathrm{загр}} = M_{\mathrm{зан}}/r`

## Why those formulas were chosen
- Взяты только те формулы, без которых verbal bridges `Почему формула именно такая` были слишком зависимы от formal report.
- Для каждого подпункта в guide оставлен только минимальный backbone:
  - как строится распределение/переходы;
  - как читается ключевая loss/queue/waiting metric;
  - как читается занятость/загрузка.
- Полные derivation chains, дополнительные family-specific report formulas и лишняя algebra deliberately не переносились.

## How they were explained simply
- Сразу после каждого formula block добавлен короткий one-idea explanation:
  - что именно сейчас считается;
  - что читает эта формула из модели;
  - почему она относится либо ко всем состояниям, либо только к правому хвосту, либо только к крайнему состоянию.
- Explanations intentionally kept short:
  - `Эта нормировка сразу учитывает ...`
  - `Первая формула читает только крайнее состояние ...`
  - `Эти формулы читают уже только правый хвост ...`
  - `Это именно вероятность того, что новый отказ попадёт в ожидание ...`

## How the guide PDF export was adjusted
- `src/delivery_guide_pdf.py` updated narrowly:
  - `pandoc --from` changed from `markdown+raw_tex` to `markdown+raw_tex+tex_math_dollars`
- Purpose:
  - explicitly lock PDF reader support for inserted `$...$/$$...$$` math blocks
  - avoid relying on implicit markdown-math defaults
- No broader export redesign was opened.

## How the full pack was regenerated
- Fresh canonical build:
  - `build --input inputs/variant_me.yaml --runs-dir /tmp/berchun_g2e_runs.TGOB9E`
- Fresh delivery:
  - `deliver --runs-dir /tmp/berchun_g2e_runs.TGOB9E --source-run-id 20260331T123650040233Z__2aaa6e434b2c --delivery-profile study_pack --output-format bundle_dir --report-scope full --guide-mode variant_aware --guide-scope full`
- Resulting visible pack:
  - `deliveries/20260331T123703755294Z__study_pack__full`

## How it was validated
- Syntax:
  - `python3 -m py_compile src/delivery_guide_pdf.py tests/test_delivery_guide_pdf_runtime.py`
- Automated tests:
  - `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_delivery_guide_pdf_runtime tests.test_pdf_surface_integrity tests.test_delivery_validation tests.test_build_pipeline -v`
- Guide-source consistency checks:
  - exact formula fragments inserted in `docs/METHODICAL_GUIDE.md`
  - section order preserved
  - each targeted subsection becomes byte-identical to the pre-G2E version after stripping only the newly inserted local formula prefix
- PDF end-state checks on the regenerated pack:
  - extracted PDF text contains stable formula needles:
    - `p0 =`
    - `Pотк = pn`
    - `Pоч = ∑ pk`
    - `Pwait =`
    - `Pож =`
    - `Mпр = ∑ i pi`

## What intentionally remained unchanged
- all numbers
- all formulas’ mathematical truth
- all checkpoints
- all defense logic
- all graph-reading logic
- all section/subsection order
- `docs/METHODICAL_GUIDE_GENERAL_SOURCE.md`
- report logic
- figure choices and placements
- delivery model and broader export architecture

## Remaining risks
- `G2E` made the current variant-aware guide self-sufficient enough for understanding, but deliberately did not mirror the same formula integration into the separate `general` guide baseline.
- Guide PDF formula extraction through `pdftotext` normalizes some math typography (`Pотк`, `p0`, `Pwait`) differently from the markdown source; tests now validate the real extracted surface explicitly.
- The guide is still intentionally lighter than the formal report; if a future pass wants more derivation depth, that must be opened separately and narrowly.

## Ready for G3? YES/NO
- `YES`

## Exact recommendation for next step
- Open `G3 — Guide Surface Freeze Review`.
- Keep it narrow: review the current teacher-first, visually supported, navigation-enabled, formula-self-sufficient guide/report surface as one user-facing artifact set; fix only tiny real inconsistencies if found, without reopening numbers, formulas, checkpoints, guide logic or delivery semantics.
