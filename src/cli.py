from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.pipeline import run
from src.plots import generate_figure_artifacts

DEFAULT_VARIANT_PATH = Path("inputs/variant_me.yaml")
DEFAULT_DERIVED_PATH = Path("inputs/derived_parameters.json")
DEFAULT_OUT_DIR = Path("out/data")
DEFAULT_FIGURES_DIR = Path("figures")
DEFAULT_FIGURE_MANIFEST_PATH = Path("out/artifacts/figure_manifest.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analytical solver for Stage 02.")
    parser.add_argument("command", nargs="?", choices=("solve", "figures"), default="solve")
    parser.add_argument("--variant-path", default=str(DEFAULT_VARIANT_PATH))
    parser.add_argument("--derived-path", default=str(DEFAULT_DERIVED_PATH))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--data-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--figures-dir", default=str(DEFAULT_FIGURES_DIR))
    parser.add_argument("--manifest-path", default=str(DEFAULT_FIGURE_MANIFEST_PATH))
    args = parser.parse_args(argv)

    if args.command == "solve":
        summary = run(
            variant_path=Path(args.variant_path),
            derived_path=Path(args.derived_path),
            out_dir=Path(args.out_dir),
        )
    else:
        summary = generate_figure_artifacts(
            data_dir=Path(args.data_dir),
            figures_dir=Path(args.figures_dir),
            manifest_path=Path(args.manifest_path),
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
