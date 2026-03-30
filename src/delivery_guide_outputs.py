from __future__ import annotations

import tempfile
from pathlib import Path

from src.compute.common import ensure_directory
from src.delivery_guide_docx import export_guide_docx
from src.delivery_guide_pdf import export_guide_pdf
from src.delivery_guide_pdf_surface import build_pdf_surface_markdown
from src.delivery_request import DeliveryRequest


def guide_formats(request: DeliveryRequest) -> tuple[str, ...]:
    if request.delivery_profile == "study_pack":
        return ("md", "pdf")
    return (request.output_format,)


def write_guide_outputs(
    *,
    delivery_dir: Path,
    guide_dir: Path,
    stem: str,
    guide_text: str,
    formats: tuple[str, ...],
    title: str,
) -> list[str]:
    markdown_path = guide_dir / f"methodical_guide__{stem}.md"
    ensure_directory(markdown_path.parent)
    markdown_path.write_text(guide_text, encoding="utf-8")
    copied = [markdown_path.relative_to(delivery_dir).as_posix()]
    if "pdf" in formats:
        pdf_path = guide_dir / f"methodical_guide__{stem}.pdf"
        pdf_markdown_path = _pdf_markdown_path(markdown_path, guide_text)
        try:
            export_guide_pdf(markdown_path=pdf_markdown_path, pdf_path=pdf_path, title=title)
        finally:
            if pdf_markdown_path != markdown_path:
                pdf_markdown_path.unlink(missing_ok=True)
        copied.append(pdf_path.relative_to(delivery_dir).as_posix())
    if "docx" in formats:
        docx_path = guide_dir / f"methodical_guide__{stem}.docx"
        export_guide_docx(markdown_path=markdown_path, docx_path=docx_path, title=title)
        copied.append(docx_path.relative_to(delivery_dir).as_posix())
    if "md" in formats:
        return copied
    markdown_path.unlink()
    return copied[1:]


def _pdf_markdown_path(markdown_path: Path, guide_text: str) -> Path:
    pdf_markdown = build_pdf_surface_markdown(guide_text=guide_text, guide_dir=markdown_path.parent)
    if pdf_markdown == guide_text:
        return markdown_path
    temp_path = _temp_pdf_markdown_path(markdown_path)
    temp_path.write_text(pdf_markdown, encoding="utf-8")
    return temp_path


def _temp_pdf_markdown_path(markdown_path: Path) -> Path:
    handle = tempfile.NamedTemporaryFile(
        prefix=f"{markdown_path.stem}__pdf_",
        suffix=".md",
        dir=markdown_path.parent,
        delete=False,
    )
    handle.close()
    return Path(handle.name)
