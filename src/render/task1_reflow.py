from __future__ import annotations

from typing import Any

from src.render.task1_reflow_11_12 import task11_blocks, task12_blocks
from src.render.task1_reflow_13_14 import task13_blocks, task14_blocks


def task1_blocks(spec: dict[str, Any], task_output: dict[str, Any], derived: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return {
        "1.1": task11_blocks,
        "1.2": task12_blocks,
        "1.3": task13_blocks,
        "1.4": task14_blocks,
    }[spec["section_id"]](spec, task_output, derived)
