from __future__ import annotations

import shutil
import subprocess
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
    command = [
        pandoc,
        str(markdown_path),
        "--from=gfm",
        "--to=pdf",
        "--standalone",
        "--pdf-engine=xelatex",
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
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip().splitlines()
        message = details[-1] if details else "unknown pandoc/xelatex failure"
        raise ValueError(f"guide PDF export failed: {message}")
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise ValueError("guide PDF export did not produce a non-empty PDF")


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
