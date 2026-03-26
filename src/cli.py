from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.pipeline import run

DEFAULT_VARIANT_PATH = Path("inputs/variant_me.yaml")
DEFAULT_DERIVED_PATH = Path("inputs/derived_parameters.json")
DEFAULT_OUT_DIR = Path("out/data")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analytical solver for Stage 02.")
    parser.add_argument("--variant-path", default=str(DEFAULT_VARIANT_PATH))
    parser.add_argument("--derived-path", default=str(DEFAULT_DERIVED_PATH))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args(argv)

    summary = run(
        variant_path=Path(args.variant_path),
        derived_path=Path(args.derived_path),
        out_dir=Path(args.out_dir),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
