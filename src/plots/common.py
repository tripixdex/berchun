from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from src.compute.common import ensure_directory
from src.plots.style import (
    apply_reference_axes,
    configure_reference_plot_style,
    figure_size,
    legend_kwargs,
    series_style,
    tight_layout_rect,
)

AXIS_LABELS = {
    "operators": "Число операторов",
    "queue_places": "Число мест в очереди",
    "repairers": "Число наладчиков",
}
FIGURE_DPI = 150
configure_reference_plot_style()

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def artifact_entry(
    figure_id: str,
    source_data_files: list[Path] | list[str],
    output_image_path: Path | str,
    semantic_description_ru: str,
    status: str,
    kind: str,
    notes_ru: str | None = None,
) -> dict[str, Any]:
    return {
        "figure_id": figure_id,
        "source_data_files": [str(path) for path in source_data_files],
        "output_image_path": str(output_image_path),
        "semantic_description_ru": semantic_description_ru,
        "status": status,
        "kind": kind,
        "generator": "matplotlib_agg",
        "deterministic": True,
        "notes_ru": notes_ru,
    }

def metric_points(points: list[dict[str, Any]], metric_name: str) -> tuple[list[int], list[float], list[int]]:
    x_values: list[int] = []
    y_values: list[float] = []
    invalid_x: list[int] = []
    for point in points:
        value = point["metrics"][metric_name]
        if value is None:
            invalid_x.append(point["x_value"])
            continue
        x_values.append(point["x_value"])
        y_values.append(float(value))
    return x_values, y_values, invalid_x

def plot_lines(
    output_path: Path,
    title: str,
    x_label: str,
    y_label: str,
    series: list[dict[str, Any]],
    y_limits: tuple[float, float] | None = None,
    note_ru: str | None = None,
    legend_columns: int = 1,
) -> None:
    ensure_directory(output_path.parent)
    fig, ax = plt.subplots(figsize=figure_size(len(series), note_ru is not None))
    apply_reference_axes(ax)
    for index, item in enumerate(series):
        ax.plot(item["x"], item["y"], label=item["label"], **series_style(index, len(series)))

    ax.set_title("")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.margins(x=0.03)
    if y_limits is not None:
        ax.set_ylim(*y_limits)
    if note_ru is not None:
        fig.text(0.02, 0.01, note_ru, ha="left", va="bottom", fontsize=7.5, style="italic", color="#555555")

    if len(series) > 1:
        ax.legend(**legend_kwargs(len(series), legend_columns))
    fig.tight_layout(rect=tight_layout_rect(len(series), note_ru is not None))
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

def build_contact_sheet(
    output_path: Path,
    title: str,
    image_paths: list[Path],
    columns: int,
) -> None:
    ensure_directory(output_path.parent)
    rows = math.ceil(len(image_paths) / columns)
    fig, axes = plt.subplots(rows, columns, figsize=(columns * 4.8, rows * 3.6))
    axes_list = axes.flatten() if hasattr(axes, "flatten") else [axes]
    for axis, image_path in zip(axes_list, image_paths):
        axis.imshow(mpimg.imread(image_path))
        axis.set_title(image_path.stem, fontsize=9)
        axis.axis("off")
    for axis in axes_list[len(image_paths) :]:
        axis.axis("off")
    fig.suptitle(title, fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

def build_simple_overview_artifacts(
    data_file: Path,
    figures_dir: Path,
    overview_name: str,
    overview_title: str,
    plot_specs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    artifacts = []
    image_paths = []
    for spec in plot_specs:
        output_path = figures_dir / spec["filename"]
        series = []
        for metric_name, label in spec["series"]:
            x_values, y_values, _ = metric_points(spec["points"], metric_name)
            series.append({"label": label, "x": x_values, "y": y_values})
        plot_lines(
            output_path=output_path,
            title=spec["title"],
            x_label=spec["x_label"],
            y_label=spec["y_label"],
            series=series,
            y_limits=spec.get("y_limits"),
            note_ru=spec.get("note_ru"),
        )
        image_paths.append(output_path)
        artifacts.append(
            artifact_entry(
                figure_id=output_path.stem,
                source_data_files=[data_file],
                output_image_path=output_path,
                semantic_description_ru=spec["description_ru"],
                status="generated",
                kind="plot",
                notes_ru=spec.get("notes_ru"),
            )
        )

    overview_path = figures_dir / overview_name
    build_contact_sheet(overview_path, overview_title, image_paths, columns=2)
    artifacts.append(
        artifact_entry(
            figure_id=overview_path.stem,
            source_data_files=[data_file],
            output_image_path=overview_path,
            semantic_description_ru=f"Сводный лист data-driven plots для {overview_title}.",
            status="generated",
            kind="overview",
        )
    )
    return artifacts
