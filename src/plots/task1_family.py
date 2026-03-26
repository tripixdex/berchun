from __future__ import annotations

from pathlib import Path
from typing import Any

from src.plots.common import AXIS_LABELS, artifact_entry, build_contact_sheet, load_json, metric_points, plot_lines

FAMILY_METRICS = (
    ("refusal_probability", "refusal", "Вероятность отказа", (0.0, 1.0)),
    ("busy_operators_expected", "busy_operators", "Мат. ожидание занятых операторов", None),
    ("operators_utilization", "operators_utilization", "Коэффициент загрузки операторов", (0.0, 1.0)),
    ("queue_exists_probability", "queue_exists", "Вероятность существования очереди", (0.0, 1.0)),
    ("queue_length_expected", "queue_length", "Мат. ожидание длины очереди", None),
    ("queue_occupancy", "queue_occupancy", "Коэффициент занятости мест в очереди", (0.0, 1.0)),
)


def build_task_1_2_artifacts(data_dir: Path, figures_dir: Path) -> list[dict[str, Any]]:
    data_file = data_dir / "task_1_2.json"
    data = load_json(data_file)
    artifacts = []
    image_paths = []
    for sweep in data["sweeps"]:
        by_queue = sweep["sweep_kind"] == "families_by_queue_places"
        x_label = AXIS_LABELS["queue_places" if by_queue else "operators"]
        label_prefix = "n" if by_queue else "m"
        suffix = "vs_queue__family_by_operators" if by_queue else "vs_operators__family_by_queue"
        fixed_key = "operators" if by_queue else "queue_places"
        for metric_name, slug, y_label, y_limits in FAMILY_METRICS:
            output_path = figures_dir / f"task1_2__{slug}_{suffix}.png"
            series = []
            for series_block in sweep["series"]:
                x_values, y_values, _ = metric_points(series_block["points"], metric_name)
                fixed_value = series_block["fixed_parameters"][fixed_key]
                series.append({"label": f"{label_prefix}={fixed_value}", "x": x_values, "y": y_values})
            title_suffix = "от мест в очереди" if by_queue else "от числа операторов"
            plot_lines(
                output_path=output_path,
                title=f"1.2 {y_label} {title_suffix}",
                x_label=x_label,
                y_label=y_label,
                series=series,
                y_limits=y_limits,
                legend_columns=2,
            )
            image_paths.append(output_path)
            artifacts.append(
                artifact_entry(
                    figure_id=output_path.stem,
                    source_data_files=[data_file],
                    output_image_path=output_path,
                    semantic_description_ru=f"1.2: {y_label.lower()} ({suffix}).",
                    status="generated",
                    kind="plot",
                )
            )

    overview_path = figures_dir / "task_1_2.png"
    build_contact_sheet(overview_path, "1.2 Система с ограниченной очередью", image_paths, columns=3)
    artifacts.append(
        artifact_entry(
            figure_id=overview_path.stem,
            source_data_files=[data_file],
            output_image_path=overview_path,
            semantic_description_ru="Сводный лист data-driven plots для 1.2.",
            status="generated",
            kind="overview",
        )
    )
    return artifacts
