from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.input_schema import CanonicalInput
from src.intake import load_canonical_input, prompt_canonical_input, write_canonical_input
from src.pipeline import run
from src.plots import generate_figure_artifacts
from src.render import build_report_package


def resolve_build_input(
    input_path: Path | None,
    interactive: bool,
    prompt: Callable[[str], str] | None = None,
) -> CanonicalInput:
    if interactive == (input_path is not None):
        raise ValueError("build requires exactly one of --interactive or --input")
    if interactive:
        prompt = input if prompt is None else prompt
        return prompt_canonical_input(prompt)
    return load_canonical_input(input_path)


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
) -> dict[str, Any]:
    write_canonical_input(variant_path, raw_input)
    solve_summary = run(variant_path=variant_path, derived_path=derived_path, out_dir=out_dir)
    figures_summary = generate_figure_artifacts(
        data_dir=out_dir,
        figures_dir=figures_dir,
        manifest_path=figure_manifest_path,
    )
    report_summary = build_report_package(
        variant_path=variant_path,
        derived_path=derived_path,
        data_dir=out_dir,
        figure_manifest_path=figure_manifest_path,
        report_source_path=report_source_path,
        report_pdf_path=report_pdf_path,
        assets_manifest_path=assets_manifest_path,
        report_year=raw_input.report_year,
    )
    return {
        "variant_path": str(variant_path),
        "derived_path": str(derived_path),
        "out_dir": str(out_dir),
        "figures_dir": str(figures_dir),
        "figure_manifest_path": str(figure_manifest_path),
        "report_source_path": str(report_source_path),
        "report_pdf_path": str(report_pdf_path),
        "report_assets_manifest_path": str(assets_manifest_path),
        "solve": solve_summary,
        "figures": figures_summary,
        "report": report_summary,
    }
