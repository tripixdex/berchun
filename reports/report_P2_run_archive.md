# Scope ID and name
P2 — Run Archive + Idempotent Rebuild

## Objective
Добавить narrow post-closeout enhancement к high-level `build`: сохранять каждый успешный прогон как отдельный run bundle, безопасно переиспользовать уже существующий bundle только при полном совпадении canonical raw input и при этом не вводить никакого partial-match или identity-swapping reuse.

## Trusted inputs used
- `README.md`
- `reports/master_report.md`
- `reports/report_P1_title_page.md`
- `src/build_pipeline.py`
- `src/cli.py`
- `src/input_schema.py`
- `src/intake.py`
- `src/pipeline.py`
- `src/render/`
- `inputs/examples/student_example.yaml`

## Files created
- `src/run_archive.py`
- `tests/test_run_archive.py`
- `reports/report_P2_run_archive.md`

## Files updated
- `src/build_pipeline.py`
- `src/cli.py`
- `README.md`
- `tests/test_build_pipeline.py`
- `tests/test_variant_integrity.py`
- `reports/master_report.md`

## What was implemented now
- Введён preserved per-run archive under `runs/<run_id>/...`.
- Каждый fresh `build` теперь пишет bundle со следующей структурой:
  - `inputs/variant_me.yaml`
  - `inputs/derived_parameters.json`
  - `out/data/*.json`
  - `figures/*.png`
  - `out/artifacts/figure_manifest.json`
  - `report/final_report.tex`
  - `report/final_report.pdf`
  - `report/assets_manifest.json`
  - `run_metadata.json`
- Добавлен registry file `runs/index.json` с минимально достаточным набором полей:
  - `run_id`
  - `created_at_utc`
  - `raw_input_hash`
  - `status`
  - `run_dir`
  - `run_metadata_path`
  - `report_pdf_path`
- High-level `build` теперь:
  - нормализует и валидирует canonical raw input;
  - вычисляет stable SHA-256 hash по всем normalized raw-input fields;
  - при cache hit находит существующий `success` run и возвращает его вместо recompute;
  - при cache miss создаёт новый run bundle и выполняет прежний `solve -> figures -> report` pipeline внутри него.
- CLI summary теперь явно сообщает:
  - `build_mode = fresh` или `build_mode = reused`;
  - `raw_input_hash`;
  - `run_id`;
  - `run_dir`;
  - `run_metadata_path`;
  - `registry_path`.
- Для backward compatibility `build` дополнительно refreshes requested working-set paths, но authoritative preserved result теперь lives in `runs/<run_id>/...`.

## Cache/reuse policy
- Reuse разрешён только при полном совпадении всех normalized canonical raw-input fields.
- Hash intentionally covers the full canonical raw input, not a subset and not only the variant-driving fields.
- New successful run is created whenever any meaningful field changes, including:
  - `student_full_name`
  - `student_group`
  - `teacher_full_name`
  - `journal_number`
  - `birth_day`
  - `birth_month`
  - `birth_year`
  - `report_year`
- Registry lookup ignores non-success entries; only a prior `success` run may be reused.

## What was explicitly forbidden and not implemented
- Не реализован partial-match reuse по `journal_number`, дате рождения или variant-only subset.
- Не реализован unsafe shortcut вида “reuse old report and just change names”.
- Не добавлены batch workflows, UI, multi-user scheduling или broader artifact management.
- Не менялись solver mathematics, figures logic и report family.

## Validation actually run
- `wc -l src/build_pipeline.py src/cli.py src/run_archive.py tests/test_build_pipeline.py tests/test_run_archive.py`
  - checked that new/updated files stay within the hard size limit.
- `python3 -m unittest tests.test_run_archive tests.test_build_pipeline -v`
  - passed: `5/5`, `OK`
- `mktemp -d /tmp/berchun_p2.XXXXXX`
  - created isolated validation workspace: `/tmp/berchun_p2.EUw2Pp`
- `python3 - <<'PY' ... PY`
  - created `/tmp/berchun_p2.EUw2Pp/student_changed.yaml` with changed `student_full_name`
- `python3 -m src.cli build --input inputs/examples/student_example.yaml --runs-dir /tmp/berchun_p2.EUw2Pp/runs ...`
  - fresh build succeeded and produced a new run bundle with PDF/report/manifests.
- repeated the same `python3 -m src.cli build ...` command against the same raw input
  - returned `build_mode = reused` with the same `run_id` and the same full-input hash.
- `python3 -m src.cli build --input /tmp/berchun_p2.EUw2Pp/student_changed.yaml --runs-dir /tmp/berchun_p2.EUw2Pp/runs ...`
  - returned `build_mode = fresh` and created a second run with a different hash and a different `run_id`.
- `python3 - <<'PY' ... PY`
  - validated `runs/index.json`, loaded both `run_metadata.json` files, and confirmed both archived PDFs exist.
- `python3 -m unittest discover -s tests -v`
  - passed: `17/17`, `OK`
  - one stale historical assertion in `tests/test_variant_integrity.py` was updated from Stage 02 tag expectations to the current Stage 07 canonical raw-input tag so the suite matches the actual committed `inputs/variant_me.yaml`.
- `python3 -m src.cli --help`
  - confirmed that `--runs-dir` and the new archive-oriented `build` outputs are exposed in the operator help text.

## Remaining risks
- Working-set mirrors under root-level `inputs/`, `out/`, `figures/`, and `report/` are still refreshed for compatibility; the preserved run bundle is the authoritative result and this distinction must remain documented.
- The mirror manifests copied to working-set paths are convenience artifacts, not the archive source of truth.
- The registry currently uses a simple append/update JSON file; it is sufficient for repository-scale operator use but not intended as a concurrent multi-user database.
- `src/cli.py`, `src/variant.py`, and `src/render/content.py` remain above the soft target but below the hard limit.

## Ready to keep as canonical run behavior? YES/NO
YES

## Exact recommendation for next scope
Сохранить `runs/<run_id>/...` plus `runs/index.json` as the canonical post-closeout build behavior and открывать следующий scope только по отдельному explicit request, например если потребуется более строгая archive browsing/reporting layer, не смешивая её с solver or report redesign.
