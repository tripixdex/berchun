from __future__ import annotations

from typing import Any

import matplotlib
from matplotlib.axes import Axes

REFERENCE_COLORS = (
    "#355c8c",
    "#5f7ea7",
    "#dd8b3d",
    "#5f8d59",
    "#c65d5d",
    "#8b6fb3",
    "#7ea0c9",
    "#bd9f68",
    "#5ba7a0",
    "#d58ab2",
    "#6b6b6b",
    "#a6a64a",
    "#4f90c2",
    "#d3b872",
    "#9a7a62",
)


def configure_reference_plot_style() -> None:
    matplotlib.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "mathtext.fontset": "dejavuserif",
            "axes.titlesize": 10,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 8,
            "axes.titlepad": 6,
        }
    )


def apply_reference_axes(ax: Axes) -> None:
    ax.set_facecolor("#fffefd")
    for spine in ax.spines.values():
        spine.set_color("#4a4a4a")
        spine.set_linewidth(0.85)
    ax.tick_params(axis="both", colors="#303030", width=0.8, length=3.5)
    ax.grid(axis="y", color="#d8d8d8", linewidth=0.55)
    ax.grid(axis="x", color="#ececec", linewidth=0.4)


def series_style(index: int, series_count: int) -> dict[str, Any]:
    return {
        "color": REFERENCE_COLORS[index % len(REFERENCE_COLORS)],
        "linewidth": 1.55 if series_count < 5 else 1.35,
        "alpha": 0.97,
        "solid_capstyle": "round",
    }


def figure_size(series_count: int, note: bool) -> tuple[float, float]:
    if series_count > 8:
        return (8.1, 5.0 if not note else 5.25)
    if series_count > 1:
        return (7.7, 4.7 if not note else 4.95)
    return (7.4, 4.55 if not note else 4.8)


def legend_kwargs(series_count: int, legend_columns: int) -> dict[str, Any]:
    shared = {
        "frameon": True,
        "fancybox": False,
        "edgecolor": "#b8b8b8",
        "facecolor": "white",
        "framealpha": 1.0,
        "borderaxespad": 0.3,
    }
    if series_count > 8:
        return {
            **shared,
            "loc": "lower center",
            "bbox_to_anchor": (0.5, 1.03),
            "ncol": legend_columns,
            "columnspacing": 1.1,
            "handlelength": 2.3,
        }
    return {
        **shared,
        "loc": "lower center",
        "bbox_to_anchor": (0.5, 1.03),
        "ncol": min(series_count, legend_columns),
        "columnspacing": 1.1,
        "handlelength": 2.3,
    }


def tight_layout_rect(series_count: int, note: bool) -> tuple[float, float, float, float]:
    if series_count > 8:
        top = 0.70
    elif series_count > 1:
        top = 0.83
    else:
        top = 0.98
    bottom = 0.08 if note else 0.05
    return (0.0, bottom, 1.0, top)
