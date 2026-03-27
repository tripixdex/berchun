from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.build_pipeline import resolve_build_input, run_build
from src.pipeline import run
from src.plots import generate_figure_artifacts
from src.render import build_report_package

DEFAULT_VARIANT_PATH = Path("inputs/variant_me.yaml")
DEFAULT_DERIVED_PATH = Path("inputs/derived_parameters.json")
DEFAULT_OUT_DIR = Path("out/data")
DEFAULT_FIGURES_DIR = Path("figures")
DEFAULT_FIGURE_MANIFEST_PATH = Path("out/artifacts/figure_manifest.json")
DEFAULT_REPORT_SOURCE_PATH = Path("report/final_report.tex")
DEFAULT_REPORT_PDF_PATH = Path("report/final_report.pdf")
DEFAULT_REPORT_ASSETS_MANIFEST_PATH = Path("report/assets_manifest.json")
DEFAULT_RUNS_DIR = Path("runs")
DEFAULT_REPORT_YEAR = 2026
CLI_DESCRIPTION = (
    "Canonical repository CLI for the analytical pipeline.\n"
    "Use `build` for normal operator work; `solve`, `figures`, and `report`\n"
    "remain available as lower-level audit/debug steps."
)
CLI_EPILOG = """Examples:
  python3 -m src.cli build --input inputs/examples/student_example.yaml
  python3 -m src.cli build --input inputs/examples/student_example.yaml --review
  python3 -m src.cli build --interactive
  python3 -m src.cli solve

Default generated outputs for `build`:
  runs/<run_id>/
  plus refreshed working-set mirrors at the requested output paths
"""


def _stderr_display(message: str) -> None:
    print(message, file=sys.stderr)


def _stderr_prompt(message: str) -> str:
    print(message, end="", file=sys.stderr, flush=True)
    return input()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=CLI_DESCRIPTION,
        epilog=CLI_EPILOG,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("solve", "figures", "report", "build"),
        default="solve",
        help="Pipeline step to run. `build` is the canonical operator entrypoint; omitted command keeps the legacy default `solve`.",
    )
    parser.add_argument("--input", dest="input_path", help="Path to the canonical raw-input file for `build`.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for canonical raw-input fields interactively. Valid only with `build` and mutually exclusive with `--input`.",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Preview normalized raw input before `build`. Interactive builds always use confirm/edit/cancel; file-based builds prompt confirm/cancel when this flag is set.",
    )
    parser.add_argument(
        "--variant-path",
        default=str(DEFAULT_VARIANT_PATH),
        help="Raw-input artifact path. Default: inputs/variant_me.yaml",
    )
    parser.add_argument(
        "--derived-path",
        default=str(DEFAULT_DERIVED_PATH),
        help="Derived-parameters artifact path. Default: inputs/derived_parameters.json",
    )
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for solver JSON outputs. Default: out/data")
    parser.add_argument(
        "--data-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory with solver JSON inputs for `figures` and `report`. Default: out/data",
    )
    parser.add_argument(
        "--figures-dir",
        default=str(DEFAULT_FIGURES_DIR),
        help="Directory for generated figure PNG files. Default: figures",
    )
    parser.add_argument(
        "--manifest-path",
        default=str(DEFAULT_FIGURE_MANIFEST_PATH),
        help="Figure manifest path. Default: out/artifacts/figure_manifest.json",
    )
    parser.add_argument(
        "--report-source-path",
        default=str(DEFAULT_REPORT_SOURCE_PATH),
        help="TeX report output path. Default: report/final_report.tex",
    )
    parser.add_argument(
        "--report-pdf-path",
        default=str(DEFAULT_REPORT_PDF_PATH),
        help="PDF report output path. Default: report/final_report.pdf",
    )
    parser.add_argument(
        "--report-year",
        type=int,
        default=DEFAULT_REPORT_YEAR,
        help="Explicit report year for low-level `report` builds. Default: 2026",
    )
    parser.add_argument(
        "--report-assets-manifest-path",
        default=str(DEFAULT_REPORT_ASSETS_MANIFEST_PATH),
        help="Report assets manifest path. Default: report/assets_manifest.json",
    )
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR), help="Per-run archive root for `build`. Default: runs")
    args = parser.parse_args(argv)
    if args.command != "build" and args.review:
        parser.exit(2, "error: --review is valid only with `build`\n")

    try:
        if args.command == "solve":
            summary = run(
                variant_path=Path(args.variant_path),
                derived_path=Path(args.derived_path),
                out_dir=Path(args.out_dir),
            )
        elif args.command == "figures":
            summary = generate_figure_artifacts(
                data_dir=Path(args.data_dir),
                figures_dir=Path(args.figures_dir),
                manifest_path=Path(args.manifest_path),
            )
        elif args.command == "report":
            summary = build_report_package(
                variant_path=Path(args.variant_path),
                derived_path=Path(args.derived_path),
                data_dir=Path(args.data_dir),
                figure_manifest_path=Path(args.manifest_path),
                report_source_path=Path(args.report_source_path),
                report_pdf_path=Path(args.report_pdf_path),
                assets_manifest_path=Path(args.report_assets_manifest_path),
                report_year=args.report_year,
            )
        else:
            raw_input = resolve_build_input(
                input_path=Path(args.input_path) if args.input_path else None,
                interactive=args.interactive,
                review=args.review,
                prompt=_stderr_prompt,
                display=_stderr_display,
            )
            summary = run_build(
                raw_input=raw_input,
                variant_path=Path(args.variant_path),
                derived_path=Path(args.derived_path),
                out_dir=Path(args.out_dir),
                figures_dir=Path(args.figures_dir),
                figure_manifest_path=Path(args.manifest_path),
                report_source_path=Path(args.report_source_path),
                report_pdf_path=Path(args.report_pdf_path),
                assets_manifest_path=Path(args.report_assets_manifest_path),
                runs_dir=Path(args.runs_dir),
            )
    except ValueError as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
