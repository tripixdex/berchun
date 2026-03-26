from __future__ import annotations

from pathlib import Path
from typing import Any

from src.plots.task1_family import build_task_1_2_artifacts
from src.plots.task1_simple import (
    build_task_1_1_artifacts,
    build_task_1_3_artifacts,
    build_task_1_4_artifacts,
)


def build_task1_artifacts(data_dir: Path, figures_dir: Path) -> list[dict[str, Any]]:
    artifacts = build_task_1_1_artifacts(data_dir, figures_dir)
    artifacts.extend(build_task_1_2_artifacts(data_dir, figures_dir))
    artifacts.extend(build_task_1_3_artifacts(data_dir, figures_dir))
    artifacts.extend(build_task_1_4_artifacts(data_dir, figures_dir))
    return artifacts
