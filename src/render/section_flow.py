from __future__ import annotations

from pathlib import Path
from typing import Any

from src.render.content import plot_caption
from src.render.notation import notation_items, task_input_items
from src.render.common import figure_block, formulas_block, latex_escape
from src.render.presentation import labeled_lines_block
from src.render.task1_reflow import task1_blocks
from src.render.task2_reflow import task2_blocks

PLOT_WIDTH = r"0.8\textwidth"

def _paragraphs(paragraphs: list[str]) -> str:
    return "".join(f"{latex_escape(paragraph)}\n\n" for paragraph in paragraphs)

def _lead_line(title: str | None, lead: list[str]) -> str:
    if not title:
        return _paragraphs(lead)
    if not lead:
        return f"\\noindent\\textbf{{{latex_escape(title)}}}\n\n"
    first, *rest = lead
    return f"\\noindent\\textbf{{{latex_escape(title)}}} {latex_escape(first)}\n\n" + _paragraphs(rest)


def _render_block(
    spec: dict[str, Any],
    block: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    figure_index: int,
) -> tuple[str, int]:
    parts = []
    parts.append(_lead_line(block["title"], block["lead"]))
    if block["formulas"]:
        parts.append(formulas_block(block["formulas"]))
    if block.get("after_formulas"):
        parts.append(_paragraphs(block["after_formulas"]))
    for figure_id in block["figure_ids"]:
        entry = figure_entries[figure_id]
        caption = f"Рисунок {spec['section_id']}.{figure_index}. {plot_caption(figure_id)}"
        parts.append(figure_block(entry["tex_path"], caption, width=PLOT_WIDTH))
        figure_index += 1
    if block["tail"]:
        parts.append(_paragraphs(block["tail"]))
    return "".join(parts), figure_index


def _render_blocks(
    spec: dict[str, Any],
    blocks: list[dict[str, Any]],
    figure_entries: dict[str, dict[str, Any]],
    figure_index: int,
) -> tuple[str, int]:
    parts = []
    for block in blocks:
        block_tex, figure_index = _render_block(spec, block, figure_entries, figure_index)
        parts.append(block_tex)
    return "".join(parts), figure_index

def subsection_tex(
    spec: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    task_output: dict[str, Any],
    derived: dict[str, Any],
    visible_label: str | None,
) -> str:
    parts = []
    label = latex_escape(spec["statement"])
    if visible_label is None:
        parts.append(f"{label}\n\n")
    else:
        parts.append(f"\\noindent\\textbf{{{latex_escape(visible_label)}}} {label}\n\n")
    parts.append(labeled_lines_block("Исходные данные:", task_input_items(spec["section_id"], derived)))
    parts.append(
        figure_block(
            str(Path("assets") / f"{spec['scheme_id']}.png"),
            f"Рисунок {spec['section_id']}.1. Расчетная схема.",
            width=r"0.9\textwidth",
        )
    )
    parts.append(labeled_lines_block("Обозначения:", notation_items(spec["section_id"], derived)))
    if spec["section_id"].startswith("1."):
        state_blocks, metric_blocks = task1_blocks(spec, task_output, derived)
    else:
        state_blocks, metric_blocks = task2_blocks(spec, task_output, derived)
    figure_index = 2
    state_tex, figure_index = _render_blocks(spec, state_blocks, figure_entries, figure_index)
    metric_tex, figure_index = _render_blocks(spec, metric_blocks, figure_entries, figure_index)
    parts.append(state_tex)
    parts.append(metric_tex)
    parts.append("\\clearpage\n")
    return "".join(parts)
