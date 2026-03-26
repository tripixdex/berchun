# Stage ID and name
STAGE 05 — External Expert Audit
Corrective Pass A — Report reproducibility and report-binding cleanup

## Objective
Fix only the confirmed Stage 05 report-generation findings:

- report path-coupling to fixed data/figure locations;
- time-dependent title-page year;
- hardcoded prose bounds/endpoints that should be bound to current artifacts.

Then rerun the same style of technical audit checks and decide technical readiness honestly.

## What was wrong before
- `src/render/report_builder.py` read task outputs from fixed `out/data`.
- Report generation was not safely relocatable when the canonical `out/artifacts/figure_manifest.json` was reused with a different report output directory.
- `src/render/content.py` used `date.today().year`, so regenerated report source changed over time.
- `src/render/content.py` and `src/render/report_builder.py` still contained report prose literals that should have come from current artifacts.

## What was fixed now
- `src/render/report_builder.py` now consumes report data through an explicit `data_dir` input instead of hardwiring `out/data`.
- `src/render/common.py` now resolves actual figure paths for TeX generation:
  - repo-local builds keep repo-relative figure paths;
  - relocatable builds fall back to absolute paths when report and figure directories share only filesystem root.
- `src/render/content.py` now receives an explicit report year and no longer depends on wall-clock time.
- `src/cli.py` now exposes deterministic report metadata via `--report-year` and passes `--data-dir` through the report build path.
- Report prose now binds to current artifacts where it previously relied on reviewer-fragile literals:
  - task `1.2` range sentence uses `summary.operators_range` and `summary.queue_places_range`;
  - task `2.1` endpoint sentence uses `summary.repairers_range` and current endpoint metrics;
  - final closeout bullets for tasks `1.4` and `2.1` now use current outputs instead of hand-written constants.
- The canonical report package was rebuilt:
  - `report/final_report.tex`
  - `report/final_report.pdf`
  - `report/assets_manifest.json`

## What remains unfixed
- The local TeX environment still emits the previously observed `polyglossia` warning about missing Russian hyphenation patterns. This pass did not widen scope into TeX environment repair.
- Large binary/reference files under `references/DZ2/.vs/` and related paths remain in the repo. This pass did not widen scope into repository cleanup.
- `src/render/report_builder.py` remains above the soft `150`-line target at `178` lines, but stays below the hard `180`-line limit. It was not split further to avoid widening the pass beyond the scoped reproducibility fixes.

## Trusted inputs used
- `reports/report_stage_05_codex_audit.md` previous revision
- `reports/master_report.md`
- `report/final_report.tex`
- `report/assets_manifest.json`
- `out/artifacts/figure_manifest.json`
- `inputs/variant_me.yaml`
- `inputs/derived_parameters.json`
- `src/render/report_builder.py`
- `src/render/content.py`
- `src/render/common.py`
- `src/cli.py`

## Commands actually run
- `mktemp -d /tmp/berchun_stage05_fix.XXXXXX`
- `python3 -m unittest discover -s tests -v`
- `python3 -m src.cli solve --derived-path /tmp/berchun_stage05_fix.EqdoUJ/derived_parameters.json --out-dir /tmp/berchun_stage05_fix.EqdoUJ/out_data`
- `python3 -m src.cli figures --data-dir out/data --figures-dir /tmp/berchun_stage05_fix.EqdoUJ/figures --manifest-path /tmp/berchun_stage05_fix.EqdoUJ/figure_manifest.json`
- `python3 -m src.cli report --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path report/final_report.tex --report-pdf-path report/final_report.pdf --report-assets-manifest-path report/assets_manifest.json`
- `python3 -m src.cli report --data-dir out/data --manifest-path out/artifacts/figure_manifest.json --report-source-path /tmp/berchun_stage05_fix.EqdoUJ/report/final_report.tex --report-pdf-path /tmp/berchun_stage05_fix.EqdoUJ/report/final_report.pdf --report-assets-manifest-path /tmp/berchun_stage05_fix.EqdoUJ/report/assets_manifest.json`
- The same temp-directory report command above was run twice during this pass:
  - first rerun failed after the initial patch because XeLaTeX could not load a cross-root relative path back into the workspace;
  - second rerun succeeded after the absolute-path fallback was added in `src/render/common.py`.
- `python3 -m json.tool out/artifacts/figure_manifest.json >/dev/null`
- `python3 -m json.tool report/assets_manifest.json >/dev/null`
- `python3 -m json.tool /tmp/berchun_stage05_fix.EqdoUJ/report/assets_manifest.json >/dev/null`
- `python3 -m json.tool /tmp/berchun_stage05_fix.EqdoUJ/figure_manifest.json >/dev/null`
- `python3 - <<'PY' ... PY` local audit script to compare temp solver outputs with committed JSON, compare temp-generated PNG hashes with committed `figures/*.png`, parse rebuilt canonical and temp `final_report.tex`, and verify report traceability/path consistency

## Verified now
- Raw inputs remain `journal_number = 4`, `birth_day = 25`, `birth_month = 6`.
- `inputs/derived_parameters.json` still matches those raw inputs exactly.
- Fresh temp replay of `python3 -m src.cli solve` produced JSON exactly equal to:
  - `inputs/derived_parameters.json`;
  - `out/data/task_1_1.json`;
  - `out/data/task_1_2.json`;
  - `out/data/task_1_3.json`;
  - `out/data/task_1_4.json`;
  - `out/data/task_2_1.json`.
- Fresh temp replay of `python3 -m src.cli figures` produced a normalized manifest equal to `out/artifacts/figure_manifest.json`.
- All `32` generated temp PNGs are byte-identical to committed `figures/*.png`.
- The canonical report build succeeds in-place.
- The previously problematic relocatable report build now succeeds with the canonical figure manifest and a temp report output directory.
- Both canonical and temp report builds use `report_year = 2026`, and both resulting assets manifests record that value explicitly.
- Rebuilt `report/final_report.tex` now shows a deterministic title page year: `Москва, 2026 г.`
- Rebuilt `report/final_report.tex` still contains `32` `\includegraphics` references:
  - `27` plot references;
  - `5` scheme references.
- All figure paths referenced by the rebuilt canonical and temp TeX files resolve to existing files.
- Rebuilt canonical report prose reflects artifact-bound values for:
  - task `1.2` sweep ranges;
  - task `2.1` endpoint sentence;
  - final closeout bullets for tasks `1.4` and `2.1`.
- `report/final_report.tex`, `report/final_report.pdf`, `report/assets_manifest.json`, and the temp-built report artifacts are non-empty.
- The current test suite passed: `9/9`, `OK`.

## Likely but not fully verified
- Scientific correctness of the analytical formulas beyond what the repository itself proves through tests and replay checks.
- Byte-for-byte identity of a future rebuilt PDF on another machine; this pass verified successful rebuild and traceability, not PDF metadata stability across environments.
- Clean-environment portability to a machine that does not already have the current Python/TeX/font stack installed.

## Not verified
- External academic correctness of `references/*`.
- Full manual visual review of every page and figure beyond existence, rebuild success, and path-resolution checks.
- Fresh-machine provisioning of TeX packages needed to eliminate the `polyglossia` hyphenation warning.

## Reproducibility findings
- The current `raw inputs -> derived parameters -> out/data` chain is reproducible from committed inputs.
- The current `out/data -> figures` chain is reproducible from committed JSON outputs.
- The canonical `report` build path is reproducible in-place.
- The previously failing relocatable report build case is now reproducible with the canonical figure manifest and a different report output directory.
- Deterministic report metadata is now explicit for the year:
  - CLI default: `2026`;
  - manifest field: `report/assets_manifest.json.meta.report_year`.
- No hidden manual data-edit step was observed in this corrective pass.

## Structural risk findings
- The `polyglossia` Russian hyphenation warning remains an environment-quality risk, but not a proven technical blocker for the repository build path.
- Large binary/reference files under `references/DZ2/.vs/` and related directories remain a repository hygiene risk, but were out of scope for this pass.
- `src/render/report_builder.py` remains near the hard file-size limit at `178` lines; the file stayed below the hard cap and was not split further to avoid scope expansion.

## Ready for external expert audit? YES/NO
YES

## Ready for final closeout from technical side? YES/NO
YES

## Exact recommendation for the next step
Proceed to final closeout / external expert handoff without additional code changes in this corrective pass.

Residual note:
- keep the `polyglossia` hyphenation warning and large reference binaries documented as non-blocking residual risks unless a separate environment-cleanup or repository-hygiene pass is explicitly requested.
