from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Any

from src.compute.common import ensure_directory
from src.delivery_assets import (
    filter_guide_text,
    select_plot_paths,
    select_report_asset_paths,
    select_report_figure_paths,
    select_scheme_paths,
)
from src.delivery_guide_outputs import guide_formats, write_guide_outputs
from src.delivery_variant_guide import build_variant_aware_guide
from src.delivery_guide_safety import apply_general_guide_safety, validate_variant_guide_safety
from src.delivery_manifest_normalization import normalize_report_assets_manifest
from src.delivery_report_outputs import copy_report_only, copy_report_outputs, report_formats
from src.delivery_request import DeliveryRequest


def populate_delivery(
    *,
    delivery_dir: Path,
    request: DeliveryRequest,
    source: dict[str, Any] | None,
    guide_source_path: Path,
    general_guide_source_path: Path,
    guide_derived_path: Path,
    guide_data_dir: Path,
    general_assets_manifest_path: Path,
) -> tuple[str, list[str]]:
    if request.delivery_profile == "report_only":
        if source is None:
            raise ValueError("report_only requires a successful run source")
        return "populated", copy_report_only(delivery_dir=delivery_dir, request=request, source=source, copy_file=_copy_file)
    if request.delivery_profile == "guide_only":
        if request.guide_mode == "general":
            return "populated", _copy_general_guide(delivery_dir, request, general_guide_source_path, general_assets_manifest_path)
        if source is None:
            raise ValueError("guide_only/variant_aware requires a successful run source")
        _validate_guide_baseline(source, guide_derived_path, guide_data_dir)
        validate_variant_guide_safety(Path(source["bundle"]["out_dir"]), request.guide_scope or "full")
        return "populated", _copy_variant_aware_guide(delivery_dir, request, source, guide_source_path)
    if request.delivery_profile == "study_pack":
        if source is None:
            raise ValueError("study_pack requires a successful run source")
        if request.guide_mode == "general":
            artifacts = copy_report_outputs(
                delivery_dir=delivery_dir,
                formats=report_formats(request),
                source=source,
                copy_file=_copy_file,
            )
            artifacts.extend(_copy_general_guide(delivery_dir, request, general_guide_source_path, general_assets_manifest_path))
            return "populated", artifacts
        _validate_guide_baseline(source, guide_derived_path, guide_data_dir)
        validate_variant_guide_safety(Path(source["bundle"]["out_dir"]), request.guide_scope or "full")
        artifacts = copy_report_outputs(
            delivery_dir=delivery_dir,
            formats=report_formats(request),
            source=source,
            copy_file=_copy_file,
        )
        artifacts.extend(_copy_variant_aware_guide(delivery_dir, request, source, guide_source_path))
        return "populated", artifacts
    if source is None:
        raise ValueError("print_pack requires a successful run source")
    return "populated", _copy_print_pack(delivery_dir, request, source)


def _copy_variant_aware_guide(delivery_dir: Path, request: DeliveryRequest, source: dict[str, Any], guide_source_path: Path) -> list[str]:
    guide_dir = delivery_dir / "guide"
    guide_scope = request.guide_scope or "full"
    copied_assets = _copy_guide_assets(
        delivery_dir=delivery_dir,
        guide_dir=guide_dir,
        scheme_paths=select_scheme_paths(Path(source["bundle"]["report_assets_manifest_path"]), guide_scope),
        plot_paths=select_plot_paths(Path(source["bundle"]["figure_manifest_path"]), guide_scope),
    )
    guide_text = build_variant_aware_guide(source_bundle=source["bundle"], guide_scope=guide_scope)
    copied = write_guide_outputs(delivery_dir=delivery_dir, guide_dir=guide_dir, stem="variant", guide_text=guide_text, formats=guide_formats(request), title="Methodical Guide Variant")
    return copied + copied_assets


def _copy_general_guide(delivery_dir: Path, request: DeliveryRequest, guide_source_path: Path, assets_manifest_path: Path) -> list[str]:
    guide_dir = delivery_dir / "guide"
    guide_scope = request.guide_scope or "full"
    copied_assets = _copy_guide_assets(delivery_dir=delivery_dir, guide_dir=guide_dir, scheme_paths=select_scheme_paths(assets_manifest_path, guide_scope), plot_paths=[])
    guide_text = filter_guide_text(guide_source_path.read_text(encoding="utf-8"), guide_scope)
    guide_text = apply_general_guide_safety(guide_text, guide_scope)
    copied = write_guide_outputs(delivery_dir=delivery_dir, guide_dir=guide_dir, stem="general", guide_text=guide_text, formats=guide_formats(request), title="Methodical Guide General")
    return copied + copied_assets


def _copy_print_pack(delivery_dir: Path, request: DeliveryRequest, source: dict[str, Any]) -> list[str]:
    copied = [
        _copy_file(Path(source["bundle"]["report_pdf_path"]), delivery_dir / "report" / "final_report.pdf", delivery_dir),
        _copy_file(Path(source["bundle"]["report_source_path"]), delivery_dir / "report" / "final_report.tex", delivery_dir),
        _copy_file(Path(source["bundle"]["report_assets_manifest_path"]), delivery_dir / "report" / "assets_manifest.json", delivery_dir),
    ]
    report_scope = request.report_scope or "full"
    assets_manifest_path = Path(source["bundle"]["report_assets_manifest_path"])
    for asset_path in select_report_asset_paths(assets_manifest_path, report_scope):
        copied.append(_copy_file(asset_path, delivery_dir / "report" / "assets" / asset_path.name, delivery_dir))
    for figure_path in select_report_figure_paths(assets_manifest_path, report_scope):
        copied.append(_copy_file(figure_path, delivery_dir / "figures" / figure_path.name, delivery_dir))
    normalize_report_assets_manifest(manifest_path=delivery_dir / "report" / "assets_manifest.json", delivery_dir=delivery_dir)
    return copied

def _validate_guide_baseline(source: dict[str, Any], guide_derived_path: Path, guide_data_dir: Path) -> None:
    source_bundle = source["bundle"]
    pairs = [(Path(source_bundle["derived_path"]), guide_derived_path)]
    for name in ("task_1_1.json", "task_1_2.json", "task_1_3.json", "task_1_4.json", "task_2_1.json"):
        pairs.append((Path(source_bundle["out_dir"]) / name, guide_data_dir / name))
    for source_path, baseline_path in pairs:
        if not baseline_path.exists():
            raise ValueError(f"guide baseline artifact is missing: {baseline_path}")
        if _sha256(source_path) != _sha256(baseline_path):
            raise ValueError("variant-aware guide delivery currently supports only runs that match the frozen guide baseline artifacts")


def _copy_file(source: Path, target: Path, delivery_dir: Path) -> str:
    ensure_directory(target.parent)
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    return target.relative_to(delivery_dir).as_posix()


def _copy_guide_assets(
    *,
    delivery_dir: Path,
    guide_dir: Path,
    scheme_paths: list[Path],
    plot_paths: list[Path],
) -> list[str]:
    scheme_copies = [_copy_file(path, guide_dir / "assets" / "schemes" / path.name, delivery_dir) for path in scheme_paths]
    plot_copies = [_copy_file(path, guide_dir / "assets" / "plots" / path.name, delivery_dir) for path in plot_paths]
    return scheme_copies + plot_copies


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
