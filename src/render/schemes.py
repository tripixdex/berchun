from __future__ import annotations

from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from src.compute.common import ensure_directory

SCHEME_SPECS = {
    "task1_1__scheme": {
        "boxes": [
            (0.05, 0.33, 0.20, 0.34, "Поток заявок\nλ"),
            (0.40, 0.33, 0.23, 0.34, "n операторов\nобслуживание μ"),
            (0.78, 0.33, 0.17, 0.34, "Обслужено"),
            (0.40, 0.08, 0.23, 0.16, "Отказ при\nполной занятости"),
        ]
    },
    "task1_2__scheme": {
        "boxes": [
            (0.05, 0.33, 0.18, 0.34, "Поток заявок\nλ"),
            (0.31, 0.33, 0.18, 0.34, "Очередь\nm мест"),
            (0.58, 0.33, 0.20, 0.34, "n операторов\nобслуживание μ"),
            (0.84, 0.33, 0.11, 0.34, "Выход"),
        ]
    },
    "task1_3__scheme": {
        "boxes": [
            (0.05, 0.33, 0.18, 0.34, "Поток заявок\nλ"),
            (0.31, 0.33, 0.20, 0.34, "Очередь\nбез ограничения"),
            (0.60, 0.33, 0.20, 0.34, "n операторов\nобслуживание μ"),
            (0.86, 0.33, 0.09, 0.34, "Выход"),
        ]
    },
    "task1_4__scheme": {
        "boxes": [
            (0.05, 0.33, 0.18, 0.34, "Поток заявок\nλ"),
            (0.31, 0.33, 0.20, 0.34, "Очередь\nбез ограничения"),
            (0.60, 0.33, 0.20, 0.34, "n операторов\nобслуживание μ"),
            (0.86, 0.33, 0.09, 0.34, "Выход"),
            (0.31, 0.08, 0.20, 0.16, "Уход из очереди\nν = 1/Tw"),
        ]
    },
    "task2_1__scheme": {
        "boxes": [
            (0.05, 0.33, 0.20, 0.34, "N станков"),
            (0.38, 0.33, 0.22, 0.34, "i неисправных\nстанков"),
            (0.69, 0.33, 0.20, 0.34, "r наладчиков\nобслуживание μ"),
        ]
    },
}


def _draw_box(ax: plt.Axes, x: float, y: float, w: float, h: float, text: str) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            linewidth=1.4,
            edgecolor="#2d3a4b",
            facecolor="#f3f5f7",
        )
    )
    ax.text(x + w / 2.0, y + h / 2.0, text, ha="center", va="center", fontsize=11)


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], text: str = "") -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", linewidth=1.6, mutation_scale=12))
    if text:
        ax.text((start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0 + 0.06, text, ha="center", fontsize=10)


def _draw_scheme(asset_id: str, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    fig, ax = plt.subplots(figsize=(8.2, 2.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for box in SCHEME_SPECS[asset_id]["boxes"]:
        _draw_box(ax, *box)

    if asset_id == "task1_1__scheme":
        _arrow(ax, (0.25, 0.50), (0.40, 0.50))
        _arrow(ax, (0.63, 0.50), (0.78, 0.50))
        _arrow(ax, (0.51, 0.33), (0.51, 0.24))
    elif asset_id in {"task1_2__scheme", "task1_3__scheme", "task1_4__scheme"}:
        _arrow(ax, (0.23, 0.50), (0.31, 0.50))
        _arrow(ax, (0.51, 0.50), (0.60, 0.50))
        _arrow(ax, (0.80, 0.50), (0.86, 0.50))
        if asset_id == "task1_4__scheme":
            _arrow(ax, (0.41, 0.33), (0.41, 0.24))
    else:
        _arrow(ax, (0.25, 0.50), (0.38, 0.50), "поломки")
        _arrow(ax, (0.60, 0.50), (0.69, 0.50), "ожидание/наладка")
        _arrow(ax, (0.79, 0.33), (0.15, 0.18), "возврат в работу")
        ax.text(0.50, 0.08, "Состояние i = число неисправных станков", ha="center", fontsize=10)

    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def build_scheme_assets(output_dir: Path) -> list[dict[str, str]]:
    ensure_directory(output_dir)
    assets = []
    for asset_id in SCHEME_SPECS:
        output_path = output_dir / f"{asset_id}.png"
        _draw_scheme(asset_id, output_path)
        assets.append(
            {
                "asset_id": asset_id,
                "kind": "scheme",
                "path": str(output_path),
            }
        )
    return assets
