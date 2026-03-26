from __future__ import annotations

from pathlib import Path
from typing import Any

from src.render.content import plot_caption, result_paragraphs, task_input_items, title_page
from src.render.common import (
    compile_tex,
    figure_block,
    format_float,
    formulas_block,
    itemize_block,
    latex_escape,
    relative_path_for_tex,
    read_json,
    resolve_path,
    write_json,
    write_text,
)
from src.render.schemes import build_scheme_assets
from src.render.specs import SECTION_SPECS


def _subsection_tex(
    spec: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    task_output: dict[str, Any],
    derived: dict[str, Any],
) -> str:
    parts = [f"\\subsection*{{{latex_escape(spec['section_id'] + '. ' + spec['title'])}}}\n"]
    parts.append(f"{latex_escape(spec['statement'])}\n\n")
    parts.append("\\subsubsection*{Исходные данные}\n")
    parts.append(itemize_block(task_input_items(spec["section_id"], derived)))
    parts.append("\\subsubsection*{Расчётная схема}\n")
    parts.append(
        figure_block(
            str(Path("assets") / f"{spec['scheme_id']}.png"),
            f"Рисунок {spec['section_id']}.1. Расчётная схема.",
            width=r"0.82\textwidth",
        )
    )
    parts.append("\\subsubsection*{Формулы вероятностей состояний}\n")
    parts.append(formulas_block(spec["state_formulas"]))
    parts.append("\\subsubsection*{Формулы производных метрик}\n")
    parts.append(formulas_block(spec["metric_formulas"]))
    parts.append("\\subsubsection*{Результаты и пояснения}\n")
    for paragraph in result_paragraphs(spec["section_id"], task_output):
        parts.append(f"{latex_escape(paragraph)}\n\n")
    for index, figure_id in enumerate(spec["figure_ids"], start=2):
        entry = figure_entries[figure_id]
        parts.append(
            figure_block(
                entry["tex_path"],
                f"Рисунок {spec['section_id']}.{index}. {plot_caption(figure_id)}",
            )
        )
    parts.append("\\clearpage\n")
    return "".join(parts)


def _tex_document(
    variant: dict[str, Any],
    derived: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    task_outputs: dict[str, dict[str, Any]],
    report_year: int,
) -> str:
    sections = [
        _subsection_tex(spec, figure_entries, task_outputs[spec["task_file"]], derived)
        for spec in SECTION_SPECS
    ]
    waiting_points = task_outputs["task_2_1.json"]["sweeps"][0]["points"]
    first_waiting = waiting_points[0]
    last_waiting = waiting_points[-1]
    closeout_items = [
        "В задаче 1.1 условие P_отк < 0.01 впервые выполняется при "
        f"n = {task_outputs['task_1_1.json']['summary']['minimal_operators_for_refusal_below_target']}.",
        "В задаче 1.3 стационарный режим начинается с "
        f"n = {task_outputs['task_1_3.json']['summary']['first_stationary_operators']}, "
        "а режимы n = "
        f"{', '.join(str(value) for value in task_outputs['task_1_3.json']['summary']['non_stationary_operators'])} "
        "остаются нестационарными.",
        "В задаче 1.4 все расчёты выполнены с детерминированным усечением хвоста "
        f"распределения при epsilon = {task_outputs['task_1_4.json']['summary']['truncation_probability_epsilon']}.",
        "В задаче 2.1 при выбранной трактовке вероятности ожидания она меняется от "
        f"{format_float(first_waiting['metrics']['waiting_probability'])} при r = {first_waiting['x_value']} "
        f"до {format_float(last_waiting['metrics']['waiting_probability'])} при r = {last_waiting['x_value']}.",
    ]
    return f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage{{geometry}}
\\usepackage{{fontspec}}
\\usepackage{{polyglossia}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{float}}
\\usepackage{{caption}}
\\geometry{{left=30mm,right=20mm,top=20mm,bottom=20mm}}
\\setdefaultlanguage{{russian}}
\\setmainfont{{Times New Roman}}
\\setsansfont{{Arial}}
\\setlength{{\\parindent}}{{1.25cm}}
\\setlength{{\\parskip}}{{0.4em}}
\\captionsetup{{font=small}}
\\begin{{document}}
{title_page(variant, report_year)}
\\section*{{Задача №1. Проектирование Call-центра}}
{"".join(sections[:4])}
\\section*{{Задача №2. Проектирование производственного участка}}
{sections[4]}
\\section*{{Краткие выводы}}
{itemize_block(closeout_items)}
\\end{{document}}
"""


def build_report_package(
    variant_path: Path,
    derived_path: Path,
    data_dir: Path,
    figure_manifest_path: Path,
    report_source_path: Path,
    report_pdf_path: Path,
    assets_manifest_path: Path,
    report_year: int,
) -> dict[str, Any]:
    variant = read_json(variant_path)
    derived = read_json(derived_path)
    figure_manifest = read_json(figure_manifest_path)
    report_dir = report_source_path.parent
    figure_entries = {
        entry["figure_id"]: {**entry, "tex_path": relative_path_for_tex(entry["output_image_path"], report_dir)}
        for entry in figure_manifest["artifacts"]
        if entry["status"] == "generated" and entry["kind"] == "plot"
    }
    scheme_assets = {entry["asset_id"]: entry for entry in build_scheme_assets(report_dir / "assets")}
    data_inputs_used = []
    task_outputs = {}
    for task_file in dict.fromkeys(spec["task_file"] for spec in SECTION_SPECS):
        data_path = data_dir / task_file
        data_inputs_used.append(str(data_path))
        task_outputs[task_file] = read_json(resolve_path(data_path))
    tex_content = _tex_document(variant, derived, figure_entries, task_outputs, report_year)
    write_text(report_source_path, tex_content)
    build_commands = compile_tex(report_dir, report_source_path.name)
    used_plot_paths = [figure_entries[figure_id]["output_image_path"] for spec in SECTION_SPECS for figure_id in spec["figure_ids"]]
    manifest = {
        "meta": {
            "stage": "STAGE 04",
            "language": "ru",
            "source_format": "tex",
            "build_engine": "xelatex",
            "reference_style_basis": "references/DZ1.docx",
            "report_year": report_year,
        },
        "report_source_file": str(report_source_path),
        "report_pdf_path": str(report_pdf_path),
        "variant_source_file": str(variant_path),
        "derived_source_file": str(derived_path),
        "data_inputs_used": data_inputs_used,
        "figure_inputs_used": used_plot_paths,
        "additional_artifacts_used": list(scheme_assets.values()),
        "formula_assets_used": [],
        "build_commands": build_commands,
        "notes_ru": [
            "Индивидуальные plot PNG взяты из Stage 03 без пересчёта solver logic.",
            "Расчётные схемы достроены на Stage 04 как детерминированные PNG-артефакты для закрытия deferred-части figure contract.",
            "Формулы встроены непосредственно в final_report.tex и не вынесены в отдельные файлы, чтобы не дублировать источник истины.",
        ],
    }
    write_json(assets_manifest_path, manifest)
    return {
        "report_source_file": str(report_source_path),
        "report_pdf_path": str(report_pdf_path),
        "assets_manifest_path": str(assets_manifest_path),
        "used_plot_count": len(used_plot_paths),
        "scheme_count": len(scheme_assets),
        "report_year": report_year,
    }
