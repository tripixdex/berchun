from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from src.compute.common import ensure_directory

PREFERRED_FONTS = ("Times New Roman", "Arial", "DejaVu Serif")
PREFERRED_MONO_FONTS = ("Courier New", "Menlo", "DejaVu Sans Mono", "Liberation Mono")


def export_guide_pdf(*, markdown_path: Path, pdf_path: Path, title: str) -> None:
    pandoc = shutil.which("pandoc")
    xelatex = shutil.which("xelatex")
    if pandoc is None or xelatex is None:
        raise ValueError("guide PDF export requires local pandoc and xelatex")
    ensure_directory(pdf_path.parent)
    header_path = _header_include_path(markdown_path.parent)
    command = [
        pandoc,
        str(markdown_path),
        "--from=markdown+raw_tex",
        "--to=pdf",
        "--standalone",
        "--pdf-engine=xelatex",
        "--include-in-header",
        str(header_path),
        "--resource-path",
        _resource_path(markdown_path),
        "-V",
        f"mainfont={_choose_font()}",
        "-V",
        f"monofont={_choose_mono_font()}",
        "-V",
        "geometry:margin=1in",
        "--metadata",
        f"title={title}",
        "-o",
        str(pdf_path),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip().splitlines()
            message = details[-1] if details else "unknown pandoc/xelatex failure"
            raise ValueError(f"guide PDF export failed: {message}")
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            raise ValueError("guide PDF export did not produce a non-empty PDF")
    finally:
        header_path.unlink(missing_ok=True)


def _resource_path(markdown_path: Path) -> str:
    guide_dir = markdown_path.parent
    delivery_dir = guide_dir.parent
    return f"{guide_dir}:{delivery_dir}"


def _choose_font() -> str:
    return _choose_available_font(PREFERRED_FONTS)


def _choose_mono_font() -> str:
    return _choose_available_font(PREFERRED_MONO_FONTS)


def _choose_available_font(preferred_fonts: tuple[str, ...]) -> str:
    fc_match = shutil.which("fc-match")
    if fc_match is None:
        return preferred_fonts[0]
    for font in preferred_fonts:
        result = subprocess.run([fc_match, font], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return font
    return preferred_fonts[0]


def _header_include_path(parent_dir: Path) -> Path:
    handle = tempfile.NamedTemporaryFile(
        prefix="guide_pdf_header__",
        suffix=".tex",
        dir=parent_dir,
        delete=False,
    )
    Path(handle.name).write_text(_header_include_content(), encoding="utf-8")
    handle.close()
    return Path(handle.name)


def _header_include_content() -> str:
    return "\n".join(
        [
            "\\usepackage{graphicx}",
            "\\makeatletter",
            "\\renewcommand\\paragraph{\\@startsection{paragraph}{4}{\\z@}{1.15ex \\@plus .3ex \\@minus .2ex}{0.55ex \\@plus .1ex}{\\normalfont\\normalsize\\bfseries}}",
            "\\renewcommand\\subparagraph{\\@startsection{subparagraph}{5}{\\z@}{1.0ex \\@plus .3ex \\@minus .2ex}{0.45ex \\@plus .1ex}{\\normalfont\\normalsize\\bfseries}}",
            "\\AtBeginDocument{%",
            "  \\@ifpackageloaded{hyperref}{%",
            "    \\hypersetup{hidelinks,pdfpagemode=UseOutlines,bookmarksopen=true,bookmarksopenlevel=2}%",
            "  }{}%",
            "}",
            "\\makeatother",
            "",
        ]
    )
