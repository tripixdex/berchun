from __future__ import annotations

from pathlib import Path

from src.plots.common import AXIS_LABELS, artifact_entry, build_contact_sheet, load_json, metric_points, plot_lines

TASK2_SPECS = (
    ("idle_machines_expected", "idle_machines", "Мат. ожидание простаивающих станков", None, None),
    ("waiting_machines_expected", "waiting_machines", "Мат. ожидание ожидающих станков", None, None),
    ("waiting_probability", "waiting_probability", "Вероятность ожидания обслуживания", (0.0, 1.0), None),
    ("busy_repairers_expected", "busy_repairers", "Мат. ожидание занятых наладчиков", None, None),
    ("repairers_utilization", "repairers_utilization", "Коэффициент занятости наладчиков", (0.0, 1.0), None),
)


def build_task2_artifacts(data_dir: Path, figures_dir: Path) -> list[dict[str, object]]:
    data_file = data_dir / "task_2_1.json"
    data = load_json(data_file)
    points = data["sweeps"][0]["points"]
    artifacts = []
    image_paths = []
    for metric_name, slug, y_label, y_limits, note_ru in TASK2_SPECS:
        output_path = figures_dir / f"task2_1__{slug}_vs_repairers.png"
        x_values, y_values, _ = metric_points(points, metric_name)
        plot_lines(
            output_path=output_path,
            title=f"2.1 {y_label}",
            x_label=AXIS_LABELS["repairers"],
            y_label=y_label,
            series=[{"label": y_label, "x": x_values, "y": y_values}],
            y_limits=y_limits,
            note_ru=note_ru,
        )
        image_paths.append(output_path)
        artifacts.append(
            artifact_entry(
                figure_id=output_path.stem,
                source_data_files=[data_file],
                output_image_path=output_path,
                semantic_description_ru=f"2.1: {y_label.lower()} от числа наладчиков.",
                status="generated",
                kind="plot",
                notes_ru=note_ru,
            )
        )

    overview_path = figures_dir / "task_2_1.png"
    build_contact_sheet(overview_path, "2.1 Производственный участок", image_paths, columns=2)
    artifacts.append(
        artifact_entry(
            figure_id=overview_path.stem,
            source_data_files=[data_file],
            output_image_path=overview_path,
            semantic_description_ru="Сводный лист data-driven plots для 2.1.",
            status="generated",
            kind="overview",
        )
    )
    return artifacts
