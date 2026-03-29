from __future__ import annotations

from pathlib import Path

from src.plots.common import AXIS_LABELS, build_simple_overview_artifacts, load_json


def build_task_1_1_artifacts(data_dir: Path, figures_dir: Path) -> list[dict[str, Any]]:
    data_file = data_dir / "task_1_1.json"
    data = load_json(data_file)
    return build_simple_overview_artifacts(
        data_file,
        figures_dir,
        "task_1_1.png",
        "1.1 Система без очереди",
        [
            {
                "filename": "task1_1__busy_operators_vs_operators.png",
                "title": "1.1 Мат. ожидание числа занятых операторов",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Мат. ожидание занятых операторов",
                "series": [("busy_operators_expected", "Занятые операторы")],
                "description_ru": "1.1: математическое ожидание числа занятых операторов от числа операторов.",
                "points": data["sweeps"][0]["points"],
            },
            {
                "filename": "task1_1__refusal_and_utilization_vs_operators.png",
                "title": "1.1 Вероятность отказа и коэффициент загрузки",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Вероятность / коэффициент",
                "series": [
                    ("refusal_probability", "Вероятность отказа"),
                    ("operators_utilization", "Коэффициент загрузки"),
                ],
                "y_limits": (0.0, 1.0),
                "description_ru": "1.1: совмещённый график вероятности отказа и коэффициента загрузки операторов.",
                "points": data["sweeps"][0]["points"],
            },
        ],
    )


def build_task_1_3_artifacts(data_dir: Path, figures_dir: Path) -> list[dict[str, Any]]:
    data_file = data_dir / "task_1_3.json"
    data = load_json(data_file)
    return build_simple_overview_artifacts(
        data_file,
        figures_dir,
        "task_1_3.png",
        "1.3 Система с неограниченной очередью",
        [
            {
                "filename": "task1_3__busy_operators_vs_operators.png",
                "title": "1.3 Мат. ожидание числа занятых операторов",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Мат. ожидание занятых операторов",
                "series": [("busy_operators_expected", "Занятые операторы")],
                "description_ru": "1.3: математическое ожидание числа занятых операторов.",
                "points": data["sweeps"][0]["points"],
            },
            {
                "filename": "task1_3__operators_utilization_vs_operators.png",
                "title": "1.3 Коэффициент загрузки операторов",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Коэффициент загрузки",
                "series": [("operators_utilization", "Коэффициент загрузки")],
                "y_limits": (0.0, 1.0),
                "description_ru": "1.3: коэффициент загрузки операторов.",
                "points": data["sweeps"][0]["points"],
            },
            {
                "filename": "task1_3__queue_exists_vs_operators.png",
                "title": "1.3 Вероятность существования очереди",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Вероятность очереди",
                "series": [("queue_exists_probability", "Вероятность очереди")],
                "y_limits": (0.0, 1.0),
                "description_ru": "1.3: вероятность существования очереди.",
                "points": data["sweeps"][0]["points"],
            },
            {
                "filename": "task1_3__queue_length_vs_operators.png",
                "title": "1.3 Мат. ожидание длины очереди",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Мат. ожидание длины очереди",
                "series": [("queue_length_expected", "Длина очереди")],
                "description_ru": "1.3: математическое ожидание длины очереди.",
                "points": data["sweeps"][0]["points"],
            },
        ],
    )


def build_task_1_4_artifacts(data_dir: Path, figures_dir: Path) -> list[dict[str, Any]]:
    data_file = data_dir / "task_1_4.json"
    data = load_json(data_file)
    return build_simple_overview_artifacts(
        data_file,
        figures_dir,
        "task_1_4.png",
        "1.4 Система с уходом клиентов",
        [
            {
                "filename": "task1_4__busy_operators_vs_operators.png",
                "title": "1.4 Мат. ожидание числа занятых операторов",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Мат. ожидание занятых операторов",
                "series": [("busy_operators_expected", "Занятые операторы")],
                "description_ru": "1.4: математическое ожидание числа занятых операторов.",
                "points": data["sweeps"][0]["points"],
                "notes_ru": "Все точки получены в stationary_truncated режиме.",
            },
            {
                "filename": "task1_4__operators_utilization_vs_operators.png",
                "title": "1.4 Коэффициент загрузки операторов",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Коэффициент загрузки",
                "series": [("operators_utilization", "Коэффициент загрузки")],
                "y_limits": (0.0, 1.0),
                "description_ru": "1.4: коэффициент загрузки операторов.",
                "points": data["sweeps"][0]["points"],
                "notes_ru": "Все точки получены в stationary_truncated режиме.",
            },
            {
                "filename": "task1_4__queue_exists_vs_operators.png",
                "title": "1.4 Вероятность существования очереди",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Вероятность очереди",
                "series": [("queue_exists_probability", "Вероятность очереди")],
                "y_limits": (0.0, 1.0),
                "description_ru": "1.4: вероятность существования очереди.",
                "points": data["sweeps"][0]["points"],
                "notes_ru": "Все точки получены в stationary_truncated режиме.",
            },
            {
                "filename": "task1_4__queue_length_vs_operators.png",
                "title": "1.4 Мат. ожидание длины очереди",
                "x_label": AXIS_LABELS["operators"],
                "y_label": "Мат. ожидание длины очереди",
                "series": [("queue_length_expected", "Длина очереди")],
                "description_ru": "1.4: математическое ожидание длины очереди.",
                "points": data["sweeps"][0]["points"],
                "notes_ru": "Все точки получены в stationary_truncated режиме.",
            },
        ],
    )
