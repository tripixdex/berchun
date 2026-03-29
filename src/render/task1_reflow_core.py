from __future__ import annotations

from typing import Any


def block(
    title: str,
    lead: list[str],
    formulas: list[str] | None = None,
    after_formulas: list[str] | None = None,
    figure_ids: list[str] | None = None,
    tail: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "title": title,
        "lead": lead,
        "formulas": formulas or [],
        "after_formulas": after_formulas or [],
        "figure_ids": figure_ids or [],
        "tail": tail or [],
    }


def point(points: list[dict[str, Any]], x_value: int) -> dict[str, Any]:
    return next(item for item in points if item["x_value"] == x_value)


def series_point(task_output: dict[str, Any], sweep_index: int, fixed_key: str, fixed_value: int, x_value: int) -> dict[str, Any]:
    series = next(item for item in task_output["sweeps"][sweep_index]["series"] if item["fixed_parameters"][fixed_key] == fixed_value)
    return point(series["points"], x_value)
