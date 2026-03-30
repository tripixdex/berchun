from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def normalize_report_assets_manifest(*, manifest_path: Path, delivery_dir: Path) -> None:
    if not manifest_path.exists():
        raise ValueError(f"delivery-local report manifest is missing: {manifest_path}")
    pdf_path = _local_if_exists(delivery_dir, "report/final_report.pdf")
    docx_path = _local_if_exists(delivery_dir, "report/final_report.docx")
    if pdf_path is None and docx_path is None:
        raise ValueError("delivery-local report manifest normalization requires report/final_report.pdf or report/final_report.docx")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_assets = _local_name_map(delivery_dir / "report" / "assets", "report/assets")
    figures = _local_name_map(delivery_dir / "figures", "figures")
    normalized = {
        **manifest,
        "meta": _normalize_meta(manifest.get("meta")),
        "report_source_file": _local_if_exists(delivery_dir, "report/final_report.tex"),
        "report_pdf_path": pdf_path,
        "report_docx_path": docx_path,
        "variant_source_file": None,
        "derived_source_file": None,
        "data_inputs_used": [],
        "figure_inputs_used": _rewrite_path_list(manifest.get("figure_inputs_used"), figures),
        "additional_artifacts_used": _rewrite_entry_list(manifest.get("additional_artifacts_used"), "path", report_assets),
        "title_assets_used": _rewrite_entry_list(manifest.get("title_assets_used"), "output_image_path", report_assets),
        "formula_assets_used": _rewrite_formula_entries(manifest.get("formula_assets_used"), report_assets),
    }
    _validate_normalized_manifest(normalized)
    manifest_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _normalize_meta(meta: Any) -> dict[str, Any]:
    normalized = dict(meta) if isinstance(meta, dict) else {}
    normalized["delivery_local_paths"] = True
    normalized["delivery_manifest_role"] = "delivery_bundle_subset"
    return normalized


def _local_if_exists(delivery_dir: Path, relative_path: str) -> str | None:
    path = delivery_dir / relative_path
    return relative_path if path.exists() else None


def _local_name_map(directory: Path, prefix: str) -> dict[str, str]:
    if not directory.exists():
        return {}
    return {path.name: f"{prefix}/{path.name}" for path in directory.iterdir() if path.is_file()}


def _rewrite_path_list(entries: Any, local_paths: dict[str, str]) -> list[str]:
    if not isinstance(entries, list):
        return []
    return [local_paths[Path(item).name] for item in entries if isinstance(item, str) and Path(item).name in local_paths]


def _rewrite_entry_list(entries: Any, path_key: str, local_paths: dict[str, str]) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        return []
    rewritten: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        path_value = entry.get(path_key)
        if not isinstance(path_value, str):
            continue
        local_path = local_paths.get(Path(path_value).name)
        if local_path is None:
            continue
        updated = dict(entry)
        updated[path_key] = local_path
        rewritten.append(updated)
    return rewritten


def _rewrite_formula_entries(entries: Any, local_paths: dict[str, str]) -> list[dict[str, Any]]:
    combined: list[dict[str, Any]] = []
    seen: set[tuple[tuple[str, Any], ...]] = set()
    for item in _rewrite_entry_list(entries, "output_image_path", local_paths) + _rewrite_entry_list(entries, "path", local_paths):
        signature = tuple(sorted(item.items()))
        if signature in seen:
            continue
        seen.add(signature)
        combined.append(item)
    return combined


def _validate_normalized_manifest(manifest: dict[str, Any]) -> None:
    _expect_report_surface_paths(manifest.get("report_pdf_path"), manifest.get("report_docx_path"))
    _expect_local_report_path(manifest.get("report_source_file"), allow_none=True)
    _expect_none(manifest.get("variant_source_file"), "variant_source_file")
    _expect_none(manifest.get("derived_source_file"), "derived_source_file")
    _expect_empty_list(manifest.get("data_inputs_used"), "data_inputs_used")
    _expect_local_list(manifest.get("figure_inputs_used"), "figure_inputs_used", "figures/")
    _expect_local_entries(manifest.get("additional_artifacts_used"), "additional_artifacts_used", "path")
    _expect_local_entries(manifest.get("title_assets_used"), "title_assets_used", "output_image_path")
    _expect_local_entries(manifest.get("formula_assets_used"), "formula_assets_used", "output_image_path", allow_fallback_key="path")


def _expect_report_surface_paths(pdf_value: Any, docx_value: Any) -> None:
    _expect_local_report_path(pdf_value, allow_none=True)
    _expect_local_report_path(docx_value, allow_none=True)
    if pdf_value is None and docx_value is None:
        raise ValueError("normalized report manifest does not keep any delivery-local report surface")


def _expect_local_report_path(value: Any, *, allow_none: bool = False) -> None:
    if value is None and allow_none:
        return
    if not isinstance(value, str) or not value.startswith("report/"):
        raise ValueError("normalized report manifest contains a non-local report path")


def _expect_none(value: Any, field_name: str) -> None:
    if value is not None:
        raise ValueError(f"normalized report manifest keeps unsupported external field {field_name}")


def _expect_empty_list(value: Any, field_name: str) -> None:
    if value != []:
        raise ValueError(f"normalized report manifest keeps unsupported external list {field_name}")


def _expect_local_list(value: Any, field_name: str, prefix: str) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.startswith(prefix) for item in value):
        raise ValueError(f"normalized report manifest contains non-local paths in {field_name}")


def _expect_local_entries(value: Any, field_name: str, key_name: str, *, allow_fallback_key: str | None = None) -> None:
    if not isinstance(value, list):
        raise ValueError(f"normalized report manifest contains invalid entries in {field_name}")
    for entry in value:
        if not isinstance(entry, dict):
            raise ValueError(f"normalized report manifest contains invalid entries in {field_name}")
        path_value = entry.get(key_name)
        if allow_fallback_key is not None and path_value is None:
            path_value = entry.get(allow_fallback_key)
        if not isinstance(path_value, str) or not path_value.startswith("report/"):
            raise ValueError(f"normalized report manifest contains non-local asset paths in {field_name}")
