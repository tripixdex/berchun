from __future__ import annotations

from pathlib import Path

from src.compute.common import ensure_directory
from src.delivery_guide_docx import export_guide_docx
from src.delivery_guide_pdf import export_guide_pdf
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
        export_guide_pdf(markdown_path=markdown_path, pdf_path=pdf_path, title=title)
        copied.append(pdf_path.relative_to(delivery_dir).as_posix())
    if "docx" in formats:
        docx_path = guide_dir / f"methodical_guide__{stem}.docx"
        export_guide_docx(markdown_path=markdown_path, docx_path=docx_path, title=title)
        copied.append(docx_path.relative_to(delivery_dir).as_posix())
    if "md" in formats:
        return copied
    markdown_path.unlink()
    return copied[1:]
