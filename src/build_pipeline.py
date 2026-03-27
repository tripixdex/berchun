from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.input_schema import CanonicalInput
from src.intake import load_canonical_input, prompt_canonical_input, review_canonical_input, write_canonical_input
from src.pipeline import run
from src.plots import generate_figure_artifacts
from src.render import build_report_package
from src.run_archive import (
    build_summary,
    bundle_paths,
    create_run_id,
    find_successful_run,
    raw_input_hash,
    register_run,
    sync_working_set,
    write_run_metadata,
)


def resolve_build_input(
    input_path: Path | None,
    interactive: bool,
    review: bool = False,
    prompt: Callable[[str], str] | None = None,
    display: Callable[[str], None] | None = None,
) -> CanonicalInput:
    if interactive == (input_path is not None):
        raise ValueError("build requires exactly one of --interactive or --input")
    if interactive:
        prompt = input if prompt is None else prompt
        raw_input = prompt_canonical_input(prompt)
        return review_canonical_input(raw_input, prompt=prompt, display=display, allow_edit=True)
    raw_input = load_canonical_input(input_path)
    if review:
        return review_canonical_input(raw_input, prompt=prompt, display=display, allow_edit=False)
    return raw_input


def run_build(
    raw_input: CanonicalInput,
    variant_path: Path,
    derived_path: Path,
    out_dir: Path,
    figures_dir: Path,
    figure_manifest_path: Path,
    report_source_path: Path,
    report_pdf_path: Path,
    assets_manifest_path: Path,
    runs_dir: Path,
) -> dict[str, Any]:
    working_set = {
        "variant_path": variant_path,
        "derived_path": derived_path,
        "out_dir": out_dir,
        "figures_dir": figures_dir,
        "figure_manifest_path": figure_manifest_path,
        "report_source_path": report_source_path,
        "report_pdf_path": report_pdf_path,
        "report_assets_manifest_path": assets_manifest_path,
    }
    input_digest = raw_input_hash(raw_input)
    reused = find_successful_run(runs_dir, input_digest)
    if reused is not None:
        registry_path = register_run(runs_dir, reused)
        sync_working_set(reused["bundle"], working_set)
        return build_summary(reused, working_set, build_mode="reused", registry_path=registry_path)

    run_id = create_run_id(input_digest)
    archive_paths = bundle_paths(runs_dir, run_id)
    metadata = {
        "meta": {"schema": "run_bundle_v1", "reuse_policy": "reuse only on identical full canonical raw input"},
        "run_id": run_id,
        "created_at_utc": run_id.split("__", 1)[0],
        "raw_input_hash": input_digest,
        "status": "running",
    }
    try:
        write_canonical_input(archive_paths["variant_path"], raw_input)
        solve_summary = run(
            variant_path=archive_paths["variant_path"],
            derived_path=archive_paths["derived_path"],
            out_dir=archive_paths["out_dir"],
        )
        figures_summary = generate_figure_artifacts(
            data_dir=archive_paths["out_dir"],
            figures_dir=archive_paths["figures_dir"],
            manifest_path=archive_paths["figure_manifest_path"],
        )
        report_summary = build_report_package(
            variant_path=archive_paths["variant_path"],
            derived_path=archive_paths["derived_path"],
            data_dir=archive_paths["out_dir"],
            figure_manifest_path=archive_paths["figure_manifest_path"],
            report_source_path=archive_paths["report_source_path"],
            report_pdf_path=archive_paths["report_pdf_path"],
            assets_manifest_path=archive_paths["report_assets_manifest_path"],
            report_year=raw_input.report_year,
        )
        metadata.update({"status": "success", "solve": solve_summary, "figures": figures_summary, "report": report_summary})
    except Exception as error:
        metadata.update({"status": "failed", "error_type": type(error).__name__, "error_message": str(error)})
        serialized = write_run_metadata(archive_paths, metadata)
        register_run(runs_dir, serialized)
        raise
    serialized = write_run_metadata(archive_paths, metadata)
    registry_path = register_run(runs_dir, serialized)
    sync_working_set(serialized["bundle"], working_set)
    return build_summary(serialized, working_set, build_mode="fresh", registry_path=registry_path)
