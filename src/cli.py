from __future__ import annotations

import argparse
import json
from pathlib import Path

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
DEFAULT_REPORT_YEAR = 2026


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repository CLI for staged analytical/report artifacts.")
    parser.add_argument("command", nargs="?", choices=("solve", "figures", "report"), default="solve")
    parser.add_argument("--variant-path", default=str(DEFAULT_VARIANT_PATH))
    parser.add_argument("--derived-path", default=str(DEFAULT_DERIVED_PATH))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--data-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--figures-dir", default=str(DEFAULT_FIGURES_DIR))
    parser.add_argument("--manifest-path", default=str(DEFAULT_FIGURE_MANIFEST_PATH))
    parser.add_argument("--report-source-path", default=str(DEFAULT_REPORT_SOURCE_PATH))
    parser.add_argument("--report-pdf-path", default=str(DEFAULT_REPORT_PDF_PATH))
    parser.add_argument("--report-year", type=int, default=DEFAULT_REPORT_YEAR)
    parser.add_argument(
        "--report-assets-manifest-path",
        default=str(DEFAULT_REPORT_ASSETS_MANIFEST_PATH),
    )
    args = parser.parse_args(argv)

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
    else:
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
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
