from __future__ import annotations

from pathlib import Path
from typing import Any

from src.render.common import (
    compile_tex,
    latex_escape,
    read_json,
    relative_path_for_tex,
    resolve_path,
    write_json,
    write_text,
)
from src.render.schemes import build_scheme_assets
from src.render.section_flow import subsection_tex
from src.render.specs import SECTION_SPECS, TASK_INTROS, TASK_TITLES
from src.render.title_page import title_page
from src.report_scope import DEFAULT_REPORT_SCOPE, filter_section_specs, normalize_report_scope

TITLE_EMBLEM_SOURCE = Path(__file__).parent / "assets" / "bmstu_emblem.jpeg"


def _pdf_bookmark(level: int, title: str, anchor: str) -> str:
    return f"\\pdfbookmark[{level}]{{{latex_escape(title)}}}{{{anchor}}}\n"


def _task_body(
    task_key: str,
    specs: list[dict[str, Any]],
    figure_entries: dict[str, dict[str, Any]],
    task_outputs: dict[str, dict[str, Any]],
    derived: dict[str, Any],
) -> str:
    if not specs:
        return ""
    if task_key == "1":
        blocks = [
            subsection_tex(spec, figure_entries, task_outputs[spec["task_file"]], derived, f"{index}.")
            for index, spec in enumerate(specs, start=1)
        ]
    else:
        blocks = [
            subsection_tex(spec, figure_entries, task_outputs[spec["task_file"]], derived, None)
            for spec in specs
        ]
    return (
        _pdf_bookmark(0, TASK_TITLES[task_key], f"report-task-{task_key}")
        +
        f"\\section*{{{TASK_TITLES[task_key]}}}\n"
        f"{latex_escape(TASK_INTROS[task_key])}\n\n"
        f"{''.join(blocks)}"
    )


def _tex_document(
    variant: dict[str, Any],
    derived: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    task_outputs: dict[str, dict[str, Any]],
    report_year: int,
    report_scope: str,
) -> str:
    selected_specs = filter_section_specs(SECTION_SPECS, report_scope)
    task1_specs = [spec for spec in selected_specs if spec["section_id"].startswith("1.")]
    task2_specs = [spec for spec in selected_specs if spec["section_id"].startswith("2.")]
    body = "".join(
        [
            _task_body("1", task1_specs, figure_entries, task_outputs, derived),
            _task_body("2", task2_specs, figure_entries, task_outputs, derived),
        ]
    )
    return f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage{{geometry}}
\\usepackage{{fontspec}}
\\usepackage{{polyglossia}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{float}}
\\usepackage{{caption}}
\\usepackage[unicode,pdfpagemode=UseOutlines,bookmarksopen=true,bookmarksopenlevel=2,hidelinks]{{hyperref}}
\\geometry{{left=30mm,right=20mm,top=20mm,bottom=20mm}}
\\setdefaultlanguage{{russian}}
\\setmainfont{{Times New Roman}}
\\setsansfont{{Arial}}
\\raggedbottom
\\setlength{{\\parindent}}{{1.25cm}}
\\setlength{{\\parskip}}{{0.18em}}
\\setlength{{\\abovedisplayskip}}{{7pt plus 2pt minus 3pt}}
\\setlength{{\\belowdisplayskip}}{{7pt plus 2pt minus 3pt}}
\\setlength{{\\abovedisplayshortskip}}{{5pt plus 2pt minus 2pt}}
\\setlength{{\\belowdisplayshortskip}}{{5pt plus 2pt minus 2pt}}
\\setlength{{\\textfloatsep}}{{9pt plus 2pt minus 2pt}}
\\setlength{{\\floatsep}}{{8pt plus 2pt minus 2pt}}
\\setlength{{\\intextsep}}{{8pt plus 2pt minus 2pt}}
\\captionsetup{{font=small,justification=centering,singlelinecheck=false,skip=3pt}}
\\begin{{document}}
{_pdf_bookmark(0, "Титульный лист", "report-title-page")}
{title_page(variant, report_year)}
{body}
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
    report_scope: str | None = None,
) -> dict[str, Any]:
    variant = read_json(variant_path)
    derived = read_json(derived_path)
    selected_scope = normalize_report_scope(report_scope or variant.get("report_scope", DEFAULT_REPORT_SCOPE))
    selected_specs = filter_section_specs(SECTION_SPECS, selected_scope)
    report_dir = report_source_path.parent
    figure_manifest = read_json(figure_manifest_path)
    figure_entries = {
        entry["figure_id"]: {**entry, "tex_path": relative_path_for_tex(entry["output_image_path"], report_dir)}
        for entry in figure_manifest["artifacts"]
        if entry["status"] == "generated" and entry["kind"] == "plot"
    }
    scheme_assets = {entry["asset_id"]: entry for entry in build_scheme_assets(report_dir / "assets")}
    title_asset_path = report_dir / "assets" / "title_emblem.jpeg"
    title_asset_path.write_bytes(TITLE_EMBLEM_SOURCE.read_bytes())
    title_asset = {"asset_id": "title_page__emblem", "kind": "title_asset", "output_image_path": str(title_asset_path)}
    data_inputs_used = []
    task_outputs = {}
    for task_file in dict.fromkeys(spec["task_file"] for spec in selected_specs):
        data_path = data_dir / task_file
        data_inputs_used.append(str(data_path))
        task_outputs[task_file] = read_json(resolve_path(data_path))
    tex_content = _tex_document(variant, derived, figure_entries, task_outputs, report_year, selected_scope)
    write_text(report_source_path, tex_content)
    build_commands = compile_tex(report_dir, report_source_path.name)
    used_plot_paths = [figure_entries[figure_id]["output_image_path"] for spec in selected_specs for figure_id in spec["figure_ids"]]
    scheme_asset_list = [scheme_assets[spec["scheme_id"]] for spec in selected_specs]
    manifest = {
        "meta": {
            "stage": "STAGE 04",
            "language": "ru",
            "source_format": "tex",
            "build_engine": "xelatex",
            "reference_style_basis": "references/DZ1.docx",
            "report_year": report_year,
            "report_scope": selected_scope,
        },
        "report_source_file": str(report_source_path),
        "report_pdf_path": str(report_pdf_path),
        "variant_source_file": str(variant_path),
        "derived_source_file": str(derived_path),
        "data_inputs_used": data_inputs_used,
        "figure_inputs_used": used_plot_paths,
        "additional_artifacts_used": scheme_asset_list,
        "title_assets_used": [title_asset],
        "formula_assets_used": [],
        "build_commands": build_commands,
        "notes_ru": [
            "Индивидуальные plot PNG берутся из figure manifest без изменения solver truth.",
            "Расчётные схемы подключаются только для секций, входящих в выбранный report_scope.",
        ],
    }
    write_json(assets_manifest_path, manifest)
    return {
        "report_source_file": str(report_source_path),
        "report_pdf_path": str(report_pdf_path),
        "assets_manifest_path": str(assets_manifest_path),
        "used_plot_count": len(used_plot_paths),
        "scheme_count": len(scheme_asset_list),
        "report_scope": selected_scope,
        "report_year": report_year,
    }
