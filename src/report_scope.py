from __future__ import annotations

from typing import Any

REPORT_SCOPES = ("task1", "task2", "full")
DEFAULT_REPORT_SCOPE = "full"
REPORT_SCOPE_LABELS = {
    "task1": "только задача 1",
    "task2": "только задача 2",
    "full": "полный отчёт",
}


def normalize_report_scope(value: Any) -> str:
    if value is None:
        return DEFAULT_REPORT_SCOPE
    if not isinstance(value, str):
        raise ValueError("report_scope must be a string")
    normalized = value.strip().lower()
    if normalized not in REPORT_SCOPES:
        raise ValueError(f"report_scope must be one of {REPORT_SCOPES}, got {value!r}")
    return normalized


def report_scope_label(scope: str) -> str:
    return REPORT_SCOPE_LABELS[normalize_report_scope(scope)]


def filter_section_specs(section_specs: list[dict[str, Any]], report_scope: str) -> list[dict[str, Any]]:
    normalized = normalize_report_scope(report_scope)
    if normalized == "full":
        return section_specs
    prefix = "1." if normalized == "task1" else "2."
    return [spec for spec in section_specs if spec["section_id"].startswith(prefix)]
