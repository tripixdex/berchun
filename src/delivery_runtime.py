from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.compute.common import ensure_directory
from src.delivery_population import populate_delivery
from src.delivery_request import DeliveryRequest
from src.run_archive import load_registry


def run_delivery(
    *,
    request: DeliveryRequest,
    runs_dir: Path,
    deliveries_dir: Path,
    guide_source_path: Path,
    general_guide_source_path: Path,
    guide_derived_path: Path,
    guide_data_dir: Path,
    general_assets_manifest_path: Path,
) -> dict[str, Any]:
    source = _load_successful_run(runs_dir, request.source_run_id) if request.requires_source_run else None
    if source is not None:
        _validate_source_scope(request, source)
    delivery_id = _create_delivery_id(request)
    delivery_dir = deliveries_dir / delivery_id
    assembly_state, delivered = populate_delivery(
        delivery_dir=delivery_dir,
        request=request,
        source=source,
        guide_source_path=guide_source_path,
        general_guide_source_path=general_guide_source_path,
        guide_derived_path=guide_derived_path,
        guide_data_dir=guide_data_dir,
        general_assets_manifest_path=general_assets_manifest_path,
    )
    artifacts = ["delivery_manifest.json", *delivered]
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
        "guide_source_kind": request.guide_source_kind,
        "report_output_format": request.report_output_format,
        "guide_output_format": request.guide_output_format,
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


def _load_successful_run(runs_dir: Path, run_id: str | None) -> dict[str, Any]:
    if run_id is None:
        raise ValueError("source_run_id is required for run-backed delivery profiles")
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


def _create_delivery_id(request: DeliveryRequest) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    scope_tag = request.report_scope or request.guide_scope or "na"
    return f"{timestamp}__{request.delivery_profile}__{scope_tag}"
