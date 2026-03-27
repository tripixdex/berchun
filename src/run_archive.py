from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.compute.common import ensure_directory
from src.input_schema import CanonicalInput


def raw_input_hash(raw_input: CanonicalInput) -> str:
    payload = json.dumps(asdict(raw_input), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def bundle_paths(runs_dir: Path, run_id: str) -> dict[str, Path]:
    run_dir = runs_dir / run_id
    return {
        "run_dir": run_dir,
        "variant_path": run_dir / "inputs" / "variant_me.yaml",
        "derived_path": run_dir / "inputs" / "derived_parameters.json",
        "out_dir": run_dir / "out" / "data",
        "figures_dir": run_dir / "figures",
        "figure_manifest_path": run_dir / "out" / "artifacts" / "figure_manifest.json",
        "report_source_path": run_dir / "report" / "final_report.tex",
        "report_pdf_path": run_dir / "report" / "final_report.pdf",
        "report_assets_manifest_path": run_dir / "report" / "assets_manifest.json",
        "run_metadata_path": run_dir / "run_metadata.json",
    }


def create_run_id(input_hash: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{timestamp}__{input_hash[:12]}"


def load_registry(runs_dir: Path) -> dict[str, Any]:
    index_path = runs_dir / "index.json"
    if not index_path.exists():
        return {"meta": {"schema": "run_registry_v1"}, "runs": []}
    return json.loads(index_path.read_text(encoding="utf-8"))


def write_registry(runs_dir: Path, registry: dict[str, Any]) -> Path:
    index_path = runs_dir / "index.json"
    ensure_directory(index_path.parent)
    index_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index_path


def find_successful_run(runs_dir: Path, input_hash: str) -> dict[str, Any] | None:
    for entry in reversed(load_registry(runs_dir)["runs"]):
        if entry["status"] != "success" or entry["raw_input_hash"] != input_hash:
            continue
        metadata_path = Path(entry["run_metadata_path"])
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("status") == "success":
                return metadata
    return None


def write_run_metadata(paths: dict[str, Path], payload: dict[str, Any]) -> dict[str, Any]:
    serialized = {**payload, "bundle": {name: str(path) for name, path in paths.items() if name != "run_metadata_path"}}
    ensure_directory(paths["run_metadata_path"].parent)
    paths["run_metadata_path"].write_text(json.dumps(serialized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return serialized


def register_run(runs_dir: Path, metadata: dict[str, Any]) -> Path:
    registry = load_registry(runs_dir)
    registry["runs"] = [entry for entry in registry["runs"] if entry["run_id"] != metadata["run_id"]]
    registry["runs"].append(
        {
            "run_id": metadata["run_id"],
            "created_at_utc": metadata["created_at_utc"],
            "raw_input_hash": metadata["raw_input_hash"],
            "status": metadata["status"],
            "run_dir": metadata["bundle"]["run_dir"],
            "run_metadata_path": str(Path(metadata["bundle"]["run_dir"]) / "run_metadata.json"),
            "report_pdf_path": metadata["bundle"]["report_pdf_path"],
        }
    )
    return write_registry(runs_dir, registry)


def _copy_file(source: Path, target: Path) -> None:
    if source.resolve() == target.resolve():
        return
    ensure_directory(target.parent)
    shutil.copy2(source, target)


def _copy_tree(source: Path, target: Path) -> None:
    if source.resolve() == target.resolve():
        return
    ensure_directory(target)
    shutil.copytree(source, target, dirs_exist_ok=True)


def sync_working_set(bundle: dict[str, str], working_set: dict[str, Path]) -> None:
    _copy_file(Path(bundle["variant_path"]), working_set["variant_path"])
    _copy_file(Path(bundle["derived_path"]), working_set["derived_path"])
    _copy_tree(Path(bundle["out_dir"]), working_set["out_dir"])
    _copy_tree(Path(bundle["figures_dir"]), working_set["figures_dir"])
    _copy_file(Path(bundle["figure_manifest_path"]), working_set["figure_manifest_path"])
    _copy_file(Path(bundle["report_source_path"]), working_set["report_source_path"])
    _copy_file(Path(bundle["report_pdf_path"]), working_set["report_pdf_path"])
    _copy_file(Path(bundle["report_assets_manifest_path"]), working_set["report_assets_manifest_path"])


def build_summary(metadata: dict[str, Any], working_set: dict[str, Path], build_mode: str, registry_path: Path) -> dict[str, Any]:
    return {
        "build_mode": build_mode,
        "status": metadata["status"],
        "raw_input_hash": metadata["raw_input_hash"],
        "run_id": metadata["run_id"],
        "created_at_utc": metadata["created_at_utc"],
        "run_dir": metadata["bundle"]["run_dir"],
        "run_metadata_path": str(Path(metadata["bundle"]["run_dir"]) / "run_metadata.json"),
        "registry_path": str(registry_path),
        "bundle": metadata["bundle"],
        "working_set": {name: str(path) for name, path in working_set.items()},
        "solve": metadata.get("solve"),
        "figures": metadata.get("figures"),
        "report": metadata.get("report"),
    }
