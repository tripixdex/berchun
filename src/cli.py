from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.build_pipeline import resolve_build_input, run_build
from src.cli_surface import cli_summary
from src.delivery_request import build_delivery_request
from src.delivery_runtime import run_delivery
from src.delivery_session import run_build_delivery_session
from src.input_schema import current_report_year
from src.pipeline import run
from src.plots import generate_figure_artifacts
from src.render import build_report_package
from src.report_scope import REPORT_SCOPES

DEFAULT_VARIANT_PATH, DEFAULT_DERIVED_PATH = Path("inputs/variant_me.yaml"), Path("inputs/derived_parameters.json")
DEFAULT_OUT_DIR, DEFAULT_FIGURES_DIR = Path("out/data"), Path("figures")
DEFAULT_FIGURE_MANIFEST_PATH = Path("out/artifacts/figure_manifest.json")
DEFAULT_REPORT_SOURCE_PATH, DEFAULT_REPORT_PDF_PATH = Path("report/final_report.tex"), Path("report/final_report.pdf")
DEFAULT_REPORT_ASSETS_MANIFEST_PATH = Path("report/assets_manifest.json")
DEFAULT_RUNS_DIR, DEFAULT_DELIVERIES_DIR = Path("runs"), Path("deliveries")
DEFAULT_GUIDE_SOURCE_PATH = Path("docs/METHODICAL_GUIDE.md")
DEFAULT_GUIDE_GENERAL_SOURCE_PATH = Path("docs/METHODICAL_GUIDE_GENERAL_SOURCE.md")
DEFAULT_REPORT_YEAR = current_report_year()
CLI_DESCRIPTION = "Canonical repository CLI for the analytical pipeline.\nRecommended operator path: `build --interactive --offer-delivery`.\nUse direct `deliver` only when you already know the technical delivery request.\nUse `--json` only for raw technical output."
CLI_EPILOG = """Examples:
  python3 -m src.cli build --interactive --offer-delivery
  python3 -m src.cli build --input inputs/examples/student_example.yaml
  python3 -m src.cli build --input inputs/examples/student_example.yaml --review
  python3 -m src.cli build --interactive
  python3 -m src.cli report --report-scope task1
  python3 -m src.cli solve
  python3 -m src.cli deliver --delivery-profile report_only --output-format pdf --report-scope full --source-run-id <run_id>
  python3 -m src.cli deliver --delivery-profile report_only --output-format docx --report-scope full --source-run-id <run_id>

Default generated outputs for `build`:
  runs/<run_id>/
  plus refreshed working-set mirrors at the requested output paths
"""
def _stderr_display(message: str) -> None: print(message, file=sys.stderr)
def _stderr_prompt(message: str) -> str: print(message, end="", file=sys.stderr, flush=True); return input()

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION, epilog=CLI_EPILOG, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", nargs="?", choices=("solve", "figures", "report", "build", "deliver"), default="solve", help="Pipeline step to run. `build` stays the canonical truth path; `deliver` packages existing baselines.")
    parser.add_argument("--input", dest="input_path", help="Path to the canonical raw-input file for `build`.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for canonical raw-input fields interactively. Valid only with `build` and mutually exclusive with `--input`.")
    parser.add_argument("--review", action="store_true", help="Preview normalized raw input before `build`. Default confirmation is Enter; edit/cancel stay available via short keys.")
    parser.add_argument("--offer-delivery", action="store_true", help="After successful `build`, stay in the same session and choose the final result to create.")
    parser.add_argument("--json", action="store_true", help="Print raw JSON summary to stdout. Without this flag the CLI shows only human operator summaries.")
    parser.add_argument("--variant-path", default=str(DEFAULT_VARIANT_PATH), help="Raw-input artifact path. Default: inputs/variant_me.yaml")
    parser.add_argument("--derived-path", default=str(DEFAULT_DERIVED_PATH), help="Derived-parameters artifact path. Default: inputs/derived_parameters.json")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for solver JSON outputs. Default: out/data")
    parser.add_argument("--data-dir", default=str(DEFAULT_OUT_DIR), help="Directory with solver JSON inputs for `figures`, `report`, and the frozen guide baseline. Default: out/data")
    parser.add_argument("--figures-dir", default=str(DEFAULT_FIGURES_DIR), help="Directory for generated figure PNG files. Default: figures")
    parser.add_argument("--manifest-path", default=str(DEFAULT_FIGURE_MANIFEST_PATH), help="Figure manifest path. Default: out/artifacts/figure_manifest.json")
    parser.add_argument("--report-source-path", default=str(DEFAULT_REPORT_SOURCE_PATH), help="TeX report output path. Default: report/final_report.tex")
    parser.add_argument("--report-pdf-path", default=str(DEFAULT_REPORT_PDF_PATH), help="PDF report output path. Default: report/final_report.pdf")
    parser.add_argument("--report-year", type=int, default=DEFAULT_REPORT_YEAR, help=f"Explicit report year for low-level `report` builds. Default: {DEFAULT_REPORT_YEAR}")
    parser.add_argument("--report-scope", choices=REPORT_SCOPES, default=None, help="Report scope for `report` and report-bearing `deliver`: task1, task2, or full.")
    parser.add_argument("--report-assets-manifest-path", default=str(DEFAULT_REPORT_ASSETS_MANIFEST_PATH), help="Report assets manifest path. Default: report/assets_manifest.json")
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR), help="Per-run archive root for `build`. Default: runs")
    parser.add_argument("--deliveries-dir", default=str(DEFAULT_DELIVERIES_DIR), help="Delivery root for `deliver`. Default: deliveries")
    parser.add_argument("--delivery-profile", default=None, help="Delivery profile for `deliver`.")
    parser.add_argument("--output-format", default=None, help="Output format for `deliver`.")
    parser.add_argument("--guide-scope", choices=REPORT_SCOPES, default=None, help="Guide scope for `deliver`: task1, task2, or full.")
    parser.add_argument("--guide-mode", default=None, help="Guide mode for `deliver`: variant_aware or general.")
    parser.add_argument("--source-run-id", default=None, help="Successful run source for `deliver`.")
    parser.add_argument("--guide-source-path", default=str(DEFAULT_GUIDE_SOURCE_PATH), help="Guide baseline path for `deliver`.")
    parser.add_argument("--guide-general-source-path", default=str(DEFAULT_GUIDE_GENERAL_SOURCE_PATH), help="General-guide baseline path for `deliver`.")
    args = parser.parse_args(argv)
    if args.command != "build" and args.review:
        parser.exit(2, "error: --review is valid only with `build`\n")
    if args.command != "build" and args.offer_delivery:
        parser.exit(2, "error: --offer-delivery is valid only with `build`\n")

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
                report_scope=args.report_scope,
            )
        elif args.command == "build":
            raw_input = resolve_build_input(
                input_path=Path(args.input_path) if args.input_path else None,
                interactive=args.interactive,
                review=args.review,
                prompt=_stderr_prompt,
                display=_stderr_display,
            )
            build_summary = run_build(
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
            summary = (
                {
                    "session_mode": "build_with_optional_delivery",
                    "build": build_summary,
                    "delivery": run_build_delivery_session(
                        build_summary=build_summary,
                        prompt=_stderr_prompt,
                        display=_stderr_display,
                        runs_dir=Path(args.runs_dir),
                        deliveries_dir=Path(args.deliveries_dir),
                        guide_source_path=Path(args.guide_source_path),
                        general_guide_source_path=Path(args.guide_general_source_path),
                        guide_derived_path=Path(args.derived_path),
                        guide_data_dir=Path(args.data_dir),
                        general_assets_manifest_path=Path(args.report_assets_manifest_path),
                    ),
                }
                if args.offer_delivery
                else build_summary
            )
        else:
            request = build_delivery_request(
                delivery_profile=args.delivery_profile,
                output_format=args.output_format,
                report_scope=args.report_scope,
                guide_scope=args.guide_scope,
                guide_mode=args.guide_mode,
                source_run_id=args.source_run_id,
            )
            summary = run_delivery(
                request=request,
                runs_dir=Path(args.runs_dir),
                deliveries_dir=Path(args.deliveries_dir),
                guide_source_path=Path(args.guide_source_path),
                general_guide_source_path=Path(args.guide_general_source_path),
                guide_derived_path=Path(args.derived_path),
                guide_data_dir=Path(args.data_dir),
                general_assets_manifest_path=Path(args.report_assets_manifest_path),
            )
    except ValueError as error:
        parser.exit(2, f"error: {error}\n")
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        rendered = cli_summary(args.command, summary, request if args.command == "deliver" else None)
        if rendered:
            _stderr_display(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
