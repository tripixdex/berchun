from __future__ import annotations

from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

from src.compute.common import ensure_directory

ASSET_IDS = ("task1_1__scheme", "task1_2__scheme", "task1_3__scheme", "task1_4__scheme", "task2_1__scheme")
NODE_RADIUS = 0.055


def _state(ax: plt.Axes, x: float, label: str) -> None:
    ax.add_patch(Circle((x, 0.5), NODE_RADIUS, edgecolor="#2d3a4b", facecolor="white", linewidth=1.4))
    ax.text(x, 0.5, label, ha="center", va="center", fontsize=12)


def _ellipsis(ax: plt.Axes, x: float) -> None:
    ax.text(x, 0.5, r"$\cdots$", ha="center", va="center", fontsize=18)


def _paired_arrow(ax: plt.Axes, left: float, right: float, upper: str, lower: str) -> None:
    start = left + NODE_RADIUS * 0.95
    end = right - NODE_RADIUS * 0.95
    ax.add_patch(FancyArrowPatch((start, 0.56), (end, 0.56), arrowstyle="->", linewidth=1.4, mutation_scale=11))
    ax.add_patch(FancyArrowPatch((end, 0.44), (start, 0.44), arrowstyle="->", linewidth=1.4, mutation_scale=11))
    ax.text((left + right) / 2.0, 0.68, upper, ha="center", va="center", fontsize=11)
    ax.text((left + right) / 2.0, 0.30, lower, ha="center", va="center", fontsize=11)


def _side_arrow(ax: plt.Axes, x: float, upper: str, note: str) -> None:
    ax.add_patch(FancyArrowPatch((x + NODE_RADIUS, 0.56), (0.97, 0.56), arrowstyle="->", linewidth=1.4, mutation_scale=11))
    ax.text((x + 0.97) / 2.0, 0.68, upper, ha="center", va="center", fontsize=11)
    ax.text((x + 0.97) / 2.0, 0.79, note, ha="center", va="center", fontsize=10)


def _canvas() -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(9.0, 2.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def _draw_task11(ax: plt.Axes) -> None:
    xs = (0.10, 0.26, 0.42, 0.72, 0.86)
    labels = (r"$S_0$", r"$S_1$", r"$S_2$", r"$S_{n-1}$", r"$S_n$")
    for x, label in zip(xs, labels):
        _state(ax, x, label)
    _ellipsis(ax, 0.57)
    _paired_arrow(ax, xs[0], xs[1], r"$\lambda$", r"$\mu$")
    _paired_arrow(ax, xs[1], xs[2], r"$\lambda$", r"$2\mu$")
    _paired_arrow(ax, xs[2], xs[3], r"$\lambda$", r"$\cdots$")
    _paired_arrow(ax, xs[3], xs[4], r"$\lambda$", r"$n\mu$")
    _side_arrow(ax, xs[4], r"$\lambda$", "отказ")


def _draw_task12(ax: plt.Axes) -> None:
    xs = (0.08, 0.22, 0.50, 0.66, 0.90)
    labels = (r"$S_0$", r"$S_1$", r"$S_n$", r"$S_{n+1}$", r"$S_{n+m}$")
    for x, label in zip(xs, labels):
        _state(ax, x, label)
    _ellipsis(ax, 0.36)
    _ellipsis(ax, 0.79)
    _paired_arrow(ax, xs[0], xs[1], r"$\lambda$", r"$\mu$")
    _paired_arrow(ax, xs[1], xs[2], r"$\lambda$", r"$\cdots$")
    _paired_arrow(ax, xs[2], xs[3], r"$\lambda$", r"$n\mu$")
    _paired_arrow(ax, xs[3], xs[4], r"$\lambda$", r"$n\mu$")
    _side_arrow(ax, xs[4], r"$\lambda$", "отказ")


def _draw_task13(ax: plt.Axes) -> None:
    xs = (0.08, 0.22, 0.50, 0.66, 0.90)
    labels = (r"$S_0$", r"$S_1$", r"$S_n$", r"$S_{n+1}$", r"$S_{n+k}$")
    for x, label in zip(xs, labels):
        _state(ax, x, label)
    _ellipsis(ax, 0.36)
    _ellipsis(ax, 0.79)
    _paired_arrow(ax, xs[0], xs[1], r"$\lambda$", r"$\mu$")
    _paired_arrow(ax, xs[1], xs[2], r"$\lambda$", r"$\cdots$")
    _paired_arrow(ax, xs[2], xs[3], r"$\lambda$", r"$n\mu$")
    _paired_arrow(ax, xs[3], xs[4], r"$\lambda$", r"$n\mu$")
    ax.text(0.93, 0.50, r"$\cdots$", ha="left", va="center", fontsize=18)


def _draw_task14(ax: plt.Axes) -> None:
    xs = (0.08, 0.22, 0.50, 0.66, 0.90)
    labels = (r"$S_0$", r"$S_1$", r"$S_n$", r"$S_{n+1}$", r"$S_{n+k}$")
    for x, label in zip(xs, labels):
        _state(ax, x, label)
    _ellipsis(ax, 0.36)
    _ellipsis(ax, 0.79)
    _paired_arrow(ax, xs[0], xs[1], r"$\lambda$", r"$\mu$")
    _paired_arrow(ax, xs[1], xs[2], r"$\lambda$", r"$\cdots$")
    _paired_arrow(ax, xs[2], xs[3], r"$\lambda$", r"$n\mu+\nu$")
    _paired_arrow(ax, xs[3], xs[4], r"$\lambda$", r"$n\mu+k\nu$")
    ax.text(0.93, 0.50, r"$\cdots$", ha="left", va="center", fontsize=18)


def _draw_task21(ax: plt.Axes) -> None:
    xs = (0.08, 0.22, 0.50, 0.66, 0.90)
    labels = (r"$S_0$", r"$S_1$", r"$S_r$", r"$S_{r+1}$", r"$S_N$")
    for x, label in zip(xs, labels):
        _state(ax, x, label)
    _ellipsis(ax, 0.36)
    _ellipsis(ax, 0.79)
    _paired_arrow(ax, xs[0], xs[1], r"$N\lambda$", r"$\mu$")
    _paired_arrow(ax, xs[1], xs[2], r"$(N-i)\lambda$", r"$\cdots$")
    _paired_arrow(ax, xs[2], xs[3], r"$(N-r)\lambda$", r"$r\mu$")
    _paired_arrow(ax, xs[3], xs[4], r"$\cdots$", r"$r\mu$")


DRAWERS = {
    "task1_1__scheme": _draw_task11,
    "task1_2__scheme": _draw_task12,
    "task1_3__scheme": _draw_task13,
    "task1_4__scheme": _draw_task14,
    "task2_1__scheme": _draw_task21,
}


def _draw_scheme(asset_id: str, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    fig, ax = _canvas()
    DRAWERS[asset_id](ax)
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def build_scheme_assets(output_dir: Path) -> list[dict[str, str]]:
    ensure_directory(output_dir)
    assets = []
    for asset_id in ASSET_IDS:
        output_path = output_dir / f"{asset_id}.png"
        _draw_scheme(asset_id, output_path)
        assets.append({"asset_id": asset_id, "kind": "scheme", "path": str(output_path)})
    return assets
