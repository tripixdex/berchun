from __future__ import annotations

from pathlib import Path
from typing import Any

from src.delivery_manifest_normalization import normalize_report_assets_manifest
from src.delivery_report_docx import export_report_docx
from src.delivery_request import DeliveryRequest


def report_formats(request: DeliveryRequest) -> tuple[str, ...]:
    if request.delivery_profile == "study_pack":
        return _bundle_report_formats(request.report_output_format)
    return (request.output_format,)


def copy_report_only(
    *,
    delivery_dir: Path,
    request: DeliveryRequest,
    source: dict[str, Any],
    copy_file,
) -> list[str]:
    return copy_report_outputs(
        delivery_dir=delivery_dir,
        formats=report_formats(request),
        source=source,
        copy_file=copy_file,
    )


def copy_report_outputs(
    *,
    delivery_dir: Path,
    formats: tuple[str, ...],
    source: dict[str, Any],
    copy_file,
) -> list[str]:
    copied: list[str] = []
    if "pdf" in formats:
        copied.append(copy_file(Path(source["bundle"]["report_pdf_path"]), delivery_dir / "report" / "final_report.pdf", delivery_dir))
    if "docx" in formats:
        docx_path = delivery_dir / "report" / "final_report.docx"
        export_report_docx(report_source_path=Path(source["bundle"]["report_source_path"]), docx_path=docx_path)
        copied.append(docx_path.relative_to(delivery_dir).as_posix())
    copied.append(copy_file(Path(source["bundle"]["report_assets_manifest_path"]), delivery_dir / "report" / "assets_manifest.json", delivery_dir))
    normalize_report_assets_manifest(manifest_path=delivery_dir / "report" / "assets_manifest.json", delivery_dir=delivery_dir)
    return copied


def _bundle_report_formats(value: str | None) -> tuple[str, ...]:
    if value == "pdf":
        return ("pdf",)
    if value == "docx":
        return ("docx",)
    if value == "pdf_docx":
        return ("pdf", "docx")
    raise ValueError(f"unsupported study_pack report_output_format: {value!r}")
