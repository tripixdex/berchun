from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.compute.common import ensure_directory
from src.delivery_assets import filter_guide_text, select_plot_paths, select_scheme_paths
from src.delivery_request import DeliveryRequest
from src.run_archive import load_registry


def run_delivery(
    *,
    request: DeliveryRequest,
    runs_dir: Path,
    deliveries_dir: Path,
    guide_source_path: Path,
    guide_derived_path: Path,
    guide_data_dir: Path,
) -> dict[str, Any]:
    source = _load_successful_run(runs_dir, request.source_run_id)
    _validate_source_scope(request, source)
    delivery_id = _create_delivery_id(request)
    delivery_dir = deliveries_dir / delivery_id
    artifacts = ["delivery_manifest.json"]
    if request.delivery_profile == "report_only":
        artifacts.extend(_assemble_report_only(delivery_dir, source))
        assembly_state = "populated"
    elif request.delivery_profile == "guide_only":
        _validate_guide_baseline(source, guide_derived_path, guide_data_dir)
        artifacts.extend(_assemble_guide_only(delivery_dir, request, source, guide_source_path))
        assembly_state = "populated"
    elif request.delivery_profile == "study_pack":
        _make_study_pack_skeleton(delivery_dir)
        assembly_state = "skeleton_only"
    else:
        _make_print_pack_skeleton(delivery_dir)
        assembly_state = "skeleton_only"
    manifest_path = delivery_dir / "delivery_manifest.json"
    ensure_directory(delivery_dir)
    manifest = {
        "meta": {"schema": "delivery_bundle_v1", "assembly_state": assembly_state},
        "delivery_id": delivery_id,
        "delivery_profile": request.delivery_profile,
        "output_format": request.output_format,
        "report_scope": request.report_scope,
        "guide_scope": request.guide_scope,
        "guide_mode": request.guide_mode,
        "source_kind": request.source_kind,
        "source_run_id": request.source_run_id,
        "artifacts": artifacts,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "success",
        "delivery_id": delivery_id,
        "delivery_dir": str(delivery_dir),
        "delivery_manifest_path": str(manifest_path),
        "assembly_state": assembly_state,
        "artifacts": artifacts,
        "source_run_id": request.source_run_id,
    }


def _assemble_report_only(delivery_dir: Path, source: dict[str, Any]) -> list[str]:
    copied: list[str] = []
    copied.append(_copy_file(Path(source["bundle"]["report_pdf_path"]), delivery_dir / "report" / "final_report.pdf", delivery_dir))
    copied.append(_copy_file(Path(source["bundle"]["report_assets_manifest_path"]), delivery_dir / "report" / "assets_manifest.json", delivery_dir))
    return copied


def _assemble_guide_only(delivery_dir: Path, request: DeliveryRequest, source: dict[str, Any], guide_source_path: Path) -> list[str]:
    copied = []
    guide_dir = delivery_dir / "guide"
    guide_text = filter_guide_text(guide_source_path.read_text(encoding="utf-8"), request.guide_scope or "full")
    guide_output = guide_dir / "methodical_guide__variant.md"
    ensure_directory(guide_output.parent)
    guide_output.write_text(guide_text, encoding="utf-8")
    copied.append(guide_output.relative_to(delivery_dir).as_posix())
    for scheme_path in select_scheme_paths(Path(source["bundle"]["report_assets_manifest_path"]), request.guide_scope or "full"):
        copied.append(_copy_file(scheme_path, guide_dir / "assets" / "schemes" / scheme_path.name, delivery_dir))
    for plot_path in select_plot_paths(Path(source["bundle"]["figure_manifest_path"]), request.guide_scope or "full"):
        copied.append(_copy_file(plot_path, guide_dir / "assets" / "plots" / plot_path.name, delivery_dir))
    return copied


def _make_study_pack_skeleton(delivery_dir: Path) -> None:
    for path in (delivery_dir / "report", delivery_dir / "guide" / "assets" / "schemes", delivery_dir / "guide" / "assets" / "plots"):
        ensure_directory(path)


def _make_print_pack_skeleton(delivery_dir: Path) -> None:
    for path in (delivery_dir / "report", delivery_dir / "figures"):
        ensure_directory(path)


def _load_successful_run(runs_dir: Path, run_id: str | None) -> dict[str, Any]:
    if run_id is None:
        raise ValueError("source_run_id is required for the supported F02B delivery profiles")
    registry = load_registry(runs_dir)
    entry = next((item for item in registry["runs"] if item["run_id"] == run_id), None)
    if entry is None:
        raise ValueError(f"source_run_id {run_id!r} was not found in {runs_dir / 'index.json'}")
    metadata_path = Path(entry["run_metadata_path"])
    if not metadata_path.exists():
        raise ValueError(f"run metadata is missing for source_run_id {run_id!r}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("status") != "success":
        raise ValueError(f"source_run_id {run_id!r} is not a successful run")
    return metadata


def _validate_source_scope(request: DeliveryRequest, source: dict[str, Any]) -> None:
    source_scope = source.get("report_scope")
    if request.delivery_profile in {"report_only", "study_pack", "print_pack"} and source_scope != request.report_scope:
        raise ValueError(f"source run report_scope={source_scope!r} does not match requested report_scope={request.report_scope!r}")
    if request.delivery_profile != "guide_only":
        return
    requested_scope = request.guide_scope
    if requested_scope == "full" and source_scope != "full":
        raise ValueError("guide_only/full requires a source run built with report_scope='full' so that all scheme assets exist")
    if requested_scope in {"task1", "task2"} and source_scope not in {requested_scope, "full"}:
        raise ValueError(f"guide_only/{requested_scope} requires a source run with report_scope={requested_scope!r} or 'full'")


def _validate_guide_baseline(source: dict[str, Any], guide_derived_path: Path, guide_data_dir: Path) -> None:
    source_bundle = source["bundle"]
    pairs = [(Path(source_bundle["derived_path"]), guide_derived_path)]
    for name in ("task_1_1.json", "task_1_2.json", "task_1_3.json", "task_1_4.json", "task_2_1.json"):
        pairs.append((Path(source_bundle["out_dir"]) / name, guide_data_dir / name))
    for source_path, baseline_path in pairs:
        if not baseline_path.exists():
            raise ValueError(f"guide baseline artifact is missing: {baseline_path}")
        if _sha256(source_path) != _sha256(baseline_path):
            raise ValueError("guide_only/variant_aware currently supports only runs that match the frozen guide baseline artifacts")


def _create_delivery_id(request: DeliveryRequest) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    scope_tag = request.report_scope or request.guide_scope or "na"
    return f"{timestamp}__{request.delivery_profile}__{scope_tag}"


def _copy_file(source: Path, target: Path, delivery_dir: Path) -> str:
    ensure_directory(target.parent)
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    return target.relative_to(delivery_dir).as_posix()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
