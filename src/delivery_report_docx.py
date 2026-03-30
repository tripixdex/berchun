from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from src.compute.common import ensure_directory

DETOKENIZE_PATTERN = re.compile(r"\{\\detokenize\{([^}]*)\}\}")


def export_report_docx(*, report_source_path: Path, docx_path: Path) -> None:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise ValueError("report DOCX export requires local pandoc")
    report_source_path = report_source_path.resolve()
    docx_path = docx_path.resolve()
    ensure_directory(docx_path.parent)
    with tempfile.TemporaryDirectory(prefix="berchun_report_docx_") as temp_dir:
        sanitized_path = Path(temp_dir) / report_source_path.name
        sanitized_path.write_text(_sanitize_report_tex(report_source_path), encoding="utf-8")
        command = [
            pandoc,
            str(sanitized_path),
            "--from=latex",
            "--to=docx",
            "--standalone",
            "--resource-path",
            str(report_source_path.parent.resolve()),
            "-o",
            str(docx_path),
        ]
        result = subprocess.run(command, cwd=report_source_path.parent, capture_output=True, text=True)
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip().splitlines()
        message = details[-1] if details else "unknown pandoc failure"
        raise ValueError(f"report DOCX export failed: {message}")
    if "Could not fetch resource" in result.stderr:
        raise ValueError("report DOCX export failed: unresolved report assets or figures")
    if not docx_path.exists() or docx_path.stat().st_size == 0:
        raise ValueError("report DOCX export did not produce a non-empty DOCX")


def _sanitize_report_tex(report_source_path: Path) -> str:
    return DETOKENIZE_PATTERN.sub(r"{\1}", report_source_path.read_text(encoding="utf-8"))
