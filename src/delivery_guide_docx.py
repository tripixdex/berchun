from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from src.compute.common import ensure_directory


def export_guide_docx(*, markdown_path: Path, docx_path: Path, title: str) -> None:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise ValueError("guide DOCX export requires local pandoc")
    ensure_directory(docx_path.parent)
    command = [
        pandoc,
        str(markdown_path),
        "--from=gfm",
        "--to=docx",
        "--standalone",
        "--resource-path",
        _resource_path(markdown_path),
        "--metadata",
        f"title={title}",
        "-o",
        str(docx_path),
    ]
    result = subprocess.run(command, cwd=markdown_path.parent, capture_output=True, text=True)
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip().splitlines()
        message = details[-1] if details else "unknown pandoc failure"
        raise ValueError(f"guide DOCX export failed: {message}")
    if "Could not fetch resource" in result.stderr:
        raise ValueError("guide DOCX export failed: unresolved guide assets")
    if not docx_path.exists() or docx_path.stat().st_size == 0:
        raise ValueError("guide DOCX export did not produce a non-empty DOCX")


def _resource_path(markdown_path: Path) -> str:
    guide_dir = markdown_path.parent
    delivery_dir = guide_dir.parent
    return f"{guide_dir}:{delivery_dir}"
