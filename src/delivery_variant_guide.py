from __future__ import annotations

from pathlib import Path
from typing import Any

from src.delivery_guide_pdf_surface import PDF_VISUAL_PLANS
from src.render.content import result_paragraphs
from src.render.notation import notation_items, task_input_items
from src.render.common import read_json
from src.render.specs import SECTION_SPECS
from src.render.task1_reflow import task1_blocks
from src.render.task2_reflow import task2_blocks
from src.report_scope import filter_section_specs, normalize_report_scope


def build_variant_aware_guide(*, source_bundle: dict[str, Any], guide_scope: str) -> str:
    scope = normalize_report_scope(guide_scope)
    derived = read_json(Path(source_bundle["derived_path"]))
    selected_specs = filter_section_specs(SECTION_SPECS, scope)

    lines: list[str] = [
        "# Methodical Guide",
        "",
        "## Что это за guide и чем он отличается от formal report",
        "Этот variant-aware guide собирается из текущего успешного run bundle.",
        "Он использует те же исходные данные, производные параметры и расчётные JSON-артефакты, что и итоговый отчёт, поэтому числа и локальные выводы здесь привязаны к текущему варианту.",
        "",
        "## Как этим руководством пользоваться дальше",
        "Если нужно быстро сориентироваться, идите так:",
        "- откройте нужный подпункт своего объёма работы;",
        "- посмотрите исходные данные и обозначения;",
        "- затем прочитайте локальные блоки с формулами и checkpoint-значениями;",
        "- на защите опирайтесь на схему, опорный график и короткий локальный вывод.",
        "",
    ]

    task1_specs = [spec for spec in selected_specs if spec["section_id"].startswith("1.")]
    task2_specs = [spec for spec in selected_specs if spec["section_id"].startswith("2.")]

    if task1_specs:
        lines.extend(_render_task_group(task1_specs, derived, source_bundle, "## Задача 1. Проектирование колл-центра"))
    if task2_specs:
        lines.extend(_render_task_group(task2_specs, derived, source_bundle, "## Задача 2. Производственный участок"))

    lines.extend(
        [
            "## Как использовать guide на защите",
            "Сначала назовите, что именно задано в подпункте и какие исходные данные используются в текущем варианте.",
            "Потом коротко проговорите формулу, опорную схему, один-два checkpoint-перехода и локальный вывод по графику.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_task_group(
    specs: list[dict[str, Any]],
    derived: dict[str, Any],
    source_bundle: dict[str, Any],
    heading: str,
) -> list[str]:
    lines = [heading, ""]
    anchor_map = _plot_anchor_map()

    for spec in specs:
        task_output = read_json(Path(source_bundle["out_dir"]) / spec["task_file"])
        if spec["section_id"].startswith("1."):
            state_blocks, metric_blocks = task1_blocks(spec, task_output, derived)
        else:
            state_blocks, metric_blocks = task2_blocks(spec, task_output, derived)

        section_heading = f"### {spec['section_id']}. {spec['title']}"
        lines.extend(
            [
                section_heading,
                "",
                "#### Что требуется по условию",
                spec["statement"],
                "",
                "#### Исходные данные",
                *[f"- {item}" for item in task_input_items(spec["section_id"], derived)],
                "",
                "#### Схема и состояния",
                "",
                "#### Обозначения",
                *[f"- {item}" for item in notation_items(spec["section_id"], derived)],
                "",
            ]
        )

        plot_anchor = anchor_map.get(spec["section_id"])
        plot_figure_id = _plot_figure_id(spec["section_id"])

        for block in [*state_blocks, *metric_blocks]:
            if plot_anchor and plot_figure_id and plot_figure_id in block["figure_ids"]:
                lines.extend([plot_anchor, ""])
            lines.extend(_render_block(block))

        summary_lines = result_paragraphs(spec["section_id"], task_output)
        if summary_lines:
            lines.extend(["#### Короткий вывод", ""])
            for paragraph in summary_lines:
                lines.extend([paragraph, ""])

    return lines


def _render_block(block: dict[str, Any]) -> list[str]:
    title = str(block["title"]).rstrip(".")
    lines: list[str] = [f"#### {title}", ""]

    for paragraph in block["lead"]:
        lines.extend([paragraph, ""])

    for formula in block["formulas"]:
        lines.extend(["$$", formula, "$$", ""])

    for paragraph in block["after_formulas"]:
        lines.extend([paragraph, ""])

    for paragraph in block["tail"]:
        lines.extend([paragraph, ""])

    return lines


def _plot_anchor_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for plan in PDF_VISUAL_PLANS:
        section_id = plan.section_heading.removeprefix("### ").split(" ", 1)[0].rstrip(".")
        if plan.plot_anchor:
            mapping[section_id] = plan.plot_anchor
    return mapping


def _plot_figure_id(section_id: str) -> str | None:
    for plan in PDF_VISUAL_PLANS:
        plan_section_id = plan.section_heading.removeprefix("### ").split(" ", 1)[0].rstrip(".")
        if plan_section_id == section_id and plan.plot_name:
            return plan.plot_name.removesuffix(".png")
    return None
