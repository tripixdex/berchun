from __future__ import annotations

import json
from pathlib import Path

from src.report_scope import normalize_report_scope

GENERAL_NOTE_HEADING = "## Режимные оговорки delivery"
TAIL_HEADING = "## Как использовать guide на защите"
TASK13_HEADING = "### 1.3. Система с неограниченной очередью"
TASK14_HEADING = "### 1.4. Система с неограниченной очередью и уходом клиентов"
TASK21_HEADING = "### 2.1. Метрики производственного участка по числу наладчиков"

GENERAL_SAFETY_NOTES = (
    (
        TASK13_HEADING,
        [
            "- В общем guide первая стационарная точка не считается универсальным числом.",
            "- До variant-aware проверки `ρ_n < 1` нельзя произносить `P_ож`, `P_оч` и `L_оч` как стационарные факты своего варианта.",
        ],
    ),
    (
        TASK14_HEADING,
        [
            "- В общем guide уменьшение очереди не объявляется безусловным улучшением обслуживания.",
            "- Численные truncation bounds и цена ухода клиентов относятся только к variant-aware guide.",
        ],
    ),
    (
        TASK21_HEADING,
        [
            "- В общем guide `P_ож` трактуется только как вероятность ожидания нового отказа.",
            "- Сравнение с календарной долей состояний с очередью делается только через variant-aware diagnostics.",
        ],
    ),
)


def apply_general_guide_safety(markdown: str, guide_scope: str) -> str:
    lines = markdown.rstrip().splitlines()
    note_blocks = _select_general_note_blocks(lines, guide_scope)
    if not note_blocks:
        return markdown if markdown.endswith("\n") else f"{markdown}\n"
    tail_idx = _find_heading(lines, TAIL_HEADING)
    note_lines = [GENERAL_NOTE_HEADING, ""]
    for heading, bullets in note_blocks:
        note_lines.append(heading)
        note_lines.append("")
        note_lines.extend(bullets)
        note_lines.append("")
    merged = [*lines[:tail_idx], "", *note_lines, *lines[tail_idx:]]
    return "\n".join(merged).rstrip() + "\n"


def validate_variant_guide_safety(out_dir: Path, guide_scope: str) -> None:
    scope = normalize_report_scope(guide_scope)
    if scope in {"task1", "full"}:
        _validate_task_1_3(out_dir / "task_1_3.json")
        _validate_task_1_4(out_dir / "task_1_4.json")
    if scope in {"task2", "full"}:
        _validate_task_2_1(out_dir / "task_2_1.json")


def _select_general_note_blocks(lines: list[str], guide_scope: str) -> list[tuple[str, list[str]]]:
    scope = normalize_report_scope(guide_scope)
    allowed = {TASK13_HEADING, TASK14_HEADING} if scope == "task1" else {TASK21_HEADING} if scope == "task2" else {
        TASK13_HEADING,
        TASK14_HEADING,
        TASK21_HEADING,
    }
    present = {line for line in lines if line in allowed}
    return [(heading, bullets) for heading, bullets in GENERAL_SAFETY_NOTES if heading in present]


def _find_heading(lines: list[str], prefix: str) -> int:
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return index
    return len(lines)


def _validate_task_1_3(path: Path) -> None:
    points = _load_points(path)
    stationary_count = 0
    for point in points:
        regime = point.get("regime", {})
        is_stationary = regime.get("is_stationary")
        if not isinstance(is_stationary, bool):
            raise ValueError("task_1_3.json is missing boolean regime.is_stationary required for variant-aware guide delivery")
        stationary_count += int(is_stationary)
        if is_stationary:
            continue
        metrics = point.get("metrics", {})
        names = ("busy_operators_expected", "operators_utilization", "queue_exists_probability", "queue_length_expected")
        if any(metrics.get(name) is not None for name in names):
            raise ValueError("task_1_3.json contains non-stationary points with metric values; variant-aware guide delivery would be misleading")
    if stationary_count == 0:
        raise ValueError("task_1_3.json does not contain a stationary point required for variant-aware guide delivery")


def _validate_task_1_4(path: Path) -> None:
    payload = _load_json(path)
    policy = payload.get("metadata", {}).get("truncation_policy")
    if not isinstance(policy, dict) or not all(key in policy for key in ("epsilon_probability", "epsilon_queue", "max_state")):
        raise ValueError("task_1_4.json is missing truncation_policy required for variant-aware guide delivery")
    for point in _points_from_payload(payload, path):
        truncation = point.get("truncation")
        if not isinstance(truncation, dict) or truncation.get("used") is not True:
            raise ValueError("task_1_4.json is missing truncation support required for variant-aware guide delivery")
        for key in ("tail_probability_upper_bound", "tail_queue_upper_bound"):
            if not isinstance(truncation.get(key), (int, float)):
                raise ValueError(f"task_1_4.json is missing numeric truncation.{key} required for variant-aware guide delivery")


def _validate_task_2_1(path: Path) -> None:
    for point in _load_points(path):
        metrics, diagnostics = point.get("metrics", {}), point.get("diagnostics", {})
        if not isinstance(metrics.get("waiting_probability"), (int, float)):
            raise ValueError("task_2_1.json is missing metrics.waiting_probability required for variant-aware guide delivery")
        if not isinstance(diagnostics.get("queue_exists_probability_state"), (int, float)):
            raise ValueError("task_2_1.json is missing diagnostics.queue_exists_probability_state required for variant-aware guide delivery")
        if diagnostics.get("waiting_probability_interpretation") != "arrival_weighted_probability_for_new_breakdown":
            raise ValueError(
                "task_2_1.json is missing diagnostics.waiting_probability_interpretation='arrival_weighted_probability_for_new_breakdown' required for variant-aware guide delivery"
            )


def _load_points(path: Path) -> list[dict[str, object]]:
    return _points_from_payload(_load_json(path), path)


def _points_from_payload(payload: dict[str, object], path: Path) -> list[dict[str, object]]:
    sweeps = payload.get("sweeps")
    if not isinstance(sweeps, list) or not sweeps:
        raise ValueError(f"{path.name} is missing sweeps required for guide delivery")
    points = sweeps[0].get("points")
    if not isinstance(points, list) or not points:
        raise ValueError(f"{path.name} is missing sweep points required for guide delivery")
    return points


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))
