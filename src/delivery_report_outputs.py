from __future__ import annotations

from pathlib import Path
from typing import Any

from src.delivery_manifest_normalization import normalize_report_assets_manifest
from src.delivery_report_docx import export_report_docx
from src.delivery_request import DeliveryRequest


def copy_report_only(
    *,
    delivery_dir: Path,
    request: DeliveryRequest,
    source: dict[str, Any],
    copy_file,
) -> list[str]:
    copied = [
        copy_file(Path(source["bundle"]["report_assets_manifest_path"]), delivery_dir / "report" / "assets_manifest.json", delivery_dir),
    ]
    if request.output_format == "docx":
        docx_path = delivery_dir / "report" / "final_report.docx"
        export_report_docx(report_source_path=Path(source["bundle"]["report_source_path"]), docx_path=docx_path)
        copied.insert(0, docx_path.relative_to(delivery_dir).as_posix())
    else:
        copied.insert(0, copy_file(Path(source["bundle"]["report_pdf_path"]), delivery_dir / "report" / "final_report.pdf", delivery_dir))
    normalize_report_assets_manifest(manifest_path=delivery_dir / "report" / "assets_manifest.json", delivery_dir=delivery_dir)
    return copied
