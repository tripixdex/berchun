from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

if "MPLCONFIGDIR" not in os.environ:
    mpl_config_dir = Path(tempfile.gettempdir()) / "berchun-mplconfig"
    mpl_config_dir.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(mpl_config_dir)
if "XDG_CACHE_HOME" not in os.environ:
    xdg_cache_dir = Path(tempfile.gettempdir()) / "berchun-xdg-cache"
    xdg_cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["XDG_CACHE_HOME"] = str(xdg_cache_dir)

from src.compute.common import ensure_directory
from src.plots.common import artifact_entry
from src.plots.task1 import build_task1_artifacts
from src.plots.task2 import build_task2_artifacts

DEFERRED_SCHEMES = (
    ("task1_1__scheme", "task1_1__scheme.png", "Расчётная схема для 1.1."),
    ("task1_2__scheme", "task1_2__scheme.png", "Расчётная схема для 1.2."),
    ("task1_3__scheme", "task1_3__scheme.png", "Расчётная схема для 1.3."),
    ("task1_4__scheme", "task1_4__scheme.png", "Расчётная схема для 1.4."),
    ("task2_1__scheme", "task2_1__scheme.png", "Расчётная схема для 2.1."),
)


def _deferred_scheme_entries(figures_dir: Path) -> list[dict[str, Any]]:
    entries = []
    for figure_id, filename, description in DEFERRED_SCHEMES:
        entries.append(
            artifact_entry(
                figure_id=figure_id,
                source_data_files=[],
                output_image_path=figures_dir / filename,
                semantic_description_ru=description,
                status="deferred_missing_non_json_source",
                kind="scheme",
                notes_ru="Stage 03 генерирует только data-driven figures из out/data/*.json.",
            )
        )
    return entries


def generate_figure_artifacts(
    data_dir: Path, figures_dir: Path, manifest_path: Path
) -> dict[str, Any]:
    ensure_directory(figures_dir)
    ensure_directory(manifest_path.parent)
    artifacts = build_task1_artifacts(data_dir, figures_dir)
    artifacts.extend(build_task2_artifacts(data_dir, figures_dir))
    artifacts.extend(_deferred_scheme_entries(figures_dir))
    manifest = {
        "meta": {
            "stage": "STAGE 03",
            "language": "ru",
            "source_policy_ru": "Все plot-артефакты строятся только из существующих out/data/*.json без пересчёта solver logic.",
            "generated_count": sum(1 for item in artifacts if item["status"] == "generated"),
            "deferred_count": sum(1 for item in artifacts if item["status"] != "generated"),
        },
        "artifacts": artifacts,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "figures_dir": str(figures_dir),
        "manifest_path": str(manifest_path),
        "generated_count": manifest["meta"]["generated_count"],
        "deferred_count": manifest["meta"]["deferred_count"],
    }
