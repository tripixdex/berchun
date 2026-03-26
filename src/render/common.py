from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from src.compute.common import ensure_directory

LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


def resolve_path(path: Path | str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return (Path.cwd() / candidate).resolve()


def relative_path_for_tex(target: Path | str, base_dir: Path) -> str:
    resolved_target = resolve_path(target)
    resolved_base = base_dir.resolve()
    try:
        common_path = Path(os.path.commonpath([resolved_base, resolved_target]))
    except ValueError:
        return str(resolved_target)
    if common_path == Path(resolved_base.anchor):
        return str(resolved_target)
    return os.path.relpath(resolved_target, start=resolved_base)


def latex_escape(text: str) -> str:
    escaped = text
    for source, target in LATEX_REPLACEMENTS.items():
        escaped = escaped.replace(source, target)
    return escaped


def format_float(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def figure_block(path: str, caption: str, width: str = r"0.9\textwidth") -> str:
    return (
        "\\begin{figure}[H]\n"
        "\\centering\n"
        f"\\includegraphics[width={width}]{{\\detokenize{{{path}}}}}\n"
        f"\\caption*{{{latex_escape(caption)}}}\n"
        "\\end{figure}\n"
    )


def itemize_block(items: list[str]) -> str:
    body = "\n".join(f"    \\item {latex_escape(item)}" for item in items)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}\n"


def formulas_block(formulas: list[str]) -> str:
    return "\n".join(f"\\[\n{formula}\n\\]\n" for formula in formulas)


def compile_tex(report_dir: Path, tex_name: str) -> list[str]:
    commands = []
    latexmk_available = shutil.which("latexmk") is not None
    if latexmk_available:
        command_sets = [
            [
                "latexmk",
                "-xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                tex_name,
            ]
        ]
    else:
        command_sets = [
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_name],
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_name],
        ]

    for command in command_sets:
        try:
            subprocess.run(
                command,
                cwd=report_dir,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stdout) from error
        commands.append(" ".join(command))
    if latexmk_available:
        clean_command = ["latexmk", "-c", tex_name]
        try:
            subprocess.run(
                clean_command,
                cwd=report_dir,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stdout) from error
        commands.append(" ".join(clean_command))
    return commands
