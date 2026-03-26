from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.compute.common import ensure_directory
from src.compute.task1 import solve_task_1_1, solve_task_1_2, solve_task_1_3, solve_task_1_4
from src.compute.task2 import solve_task_2_1
from src.domain.types import DerivedInputs
from src.variant import derive_inputs, load_variant


def solve_all(derived_inputs: DerivedInputs) -> dict[str, dict[str, Any]]:
    return {
        "task_1_1.json": solve_task_1_1(derived_inputs.task1),
        "task_1_2.json": solve_task_1_2(derived_inputs.task1),
        "task_1_3.json": solve_task_1_3(derived_inputs.task1),
        "task_1_4.json": solve_task_1_4(derived_inputs.task1),
        "task_2_1.json": solve_task_2_1(derived_inputs.task2),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_outputs(out_dir: Path, outputs: dict[str, dict[str, Any]]) -> None:
    ensure_directory(out_dir)
    for filename, payload in outputs.items():
        write_json(out_dir / filename, payload)


def run(variant_path: Path, derived_path: Path, out_dir: Path) -> dict[str, Any]:
    raw = load_variant(variant_path)
    derived_inputs, derived_document = derive_inputs(raw)
    outputs = solve_all(derived_inputs)
    write_json(derived_path, derived_document)
    write_outputs(out_dir, outputs)
    written_files = [str(derived_path)] + [str(out_dir / filename) for filename in outputs]
    return {
        "variant_path": str(variant_path),
        "derived_path": str(derived_path),
        "out_dir": str(out_dir),
        "written_files": written_files,
    }
