from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping

from src.compute.common import validate_positive_int
from src.report_scope import normalize_report_scope

STAGE_ID = "FEATURE 01"
SCHEMA_ID = "canonical_raw_input_v2"
DEFAULT_TEACHER_FULL_NAME = "Берчун Юрий Валерьевич"
DATE_PATTERN = re.compile(r"\d{2}\.\d{2}\.\d{4}")


@dataclass(frozen=True)
class CanonicalInput:
    student_full_name: str
    student_group: str
    teacher_full_name: str
    journal_number: int
    birth_date: str
    report_scope: str
    report_year: int

    @property
    def birth_day(self) -> int:
        return int(self.birth_date[:2])

    @property
    def birth_month(self) -> int:
        return int(self.birth_date[3:5])

    @property
    def birth_year(self) -> int:
        return int(self.birth_date[6:10])


def current_report_year() -> int:
    return datetime.now().astimezone().year


def _normalize_text(name: str, value: Any, default: str | None = None) -> str:
    if value is None and default is not None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    normalized = " ".join(value.split())
    if not normalized:
        raise ValueError(f"{name} must be non-empty")
    return normalized


def _parse_int(name: str, value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value.strip()):
        return int(value.strip())
    raise ValueError(f"{name} must be an integer")


def _parse_scalar(raw_value: str) -> Any:
    if raw_value.startswith('"') and raw_value.endswith('"'):
        return json.loads(raw_value)
    if raw_value.startswith("'") and raw_value.endswith("'"):
        return raw_value[1:-1]
    if re.fullmatch(r"[+-]?\d+", raw_value):
        return int(raw_value)
    return raw_value


def _normalize_birth_date(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("birth_date must be a string in DD.MM.YYYY format")
    normalized = value.strip()
    if not DATE_PATTERN.fullmatch(normalized):
        raise ValueError("birth_date must match DD.MM.YYYY")
    day, month, year = (int(part) for part in normalized.split("."))
    try:
        return date(year, month, day).strftime("%d.%m.%Y")
    except ValueError as error:
        raise ValueError("birth_date must be a valid date") from error


def _legacy_birth_date(payload: Mapping[str, Any]) -> str | None:
    fields = ("birth_day", "birth_month", "birth_year")
    if not any(payload.get(field) is not None for field in fields):
        return None
    day = _parse_int("birth_day", payload.get("birth_day"))
    month = _parse_int("birth_month", payload.get("birth_month"))
    year = _parse_int("birth_year", payload.get("birth_year"))
    validate_positive_int("birth_day", day)
    validate_positive_int("birth_month", month)
    validate_positive_int("birth_year", year)
    try:
        return date(year, month, day).strftime("%d.%m.%Y")
    except ValueError as error:
        raise ValueError("birth_day, birth_month, birth_year must form a valid date") from error


def _resolve_birth_date(payload: Mapping[str, Any]) -> str:
    birth_date = payload.get("birth_date")
    legacy = _legacy_birth_date(payload)
    if birth_date is None and legacy is None:
        raise ValueError("birth_date is required")
    if birth_date is None:
        return legacy
    normalized = _normalize_birth_date(birth_date)
    if legacy is not None and legacy != normalized:
        raise ValueError("birth_date conflicts with birth_day/birth_month/birth_year")
    return normalized


def parse_input_text(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {}
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" not in stripped:
                raise ValueError(f"Invalid YAML line {line_number}: {line}")
            key, raw_value = stripped.split(":", 1)
            if not key.strip() or not raw_value.strip():
                raise ValueError(f"Invalid YAML line {line_number}: {line}")
            payload[key.strip()] = _parse_scalar(raw_value.strip())
    if not isinstance(payload, dict):
        raise ValueError("Input document must be a mapping")
    return payload


def validate_input_payload(payload: Mapping[str, Any]) -> CanonicalInput:
    journal_number = _parse_int("journal_number", payload.get("journal_number"))
    validate_positive_int("journal_number", journal_number)
    report_year = payload.get("report_year", current_report_year())
    report_year = _parse_int("report_year", report_year)
    if report_year < 2000 or report_year > 2100:
        raise ValueError(f"report_year must be within [2000, 2100], got {report_year!r}")
    return CanonicalInput(
        student_full_name=_normalize_text("student_full_name", payload.get("student_full_name")),
        student_group=_normalize_text("student_group", payload.get("student_group")),
        teacher_full_name=_normalize_text(
            "teacher_full_name",
            payload.get("teacher_full_name"),
            default=DEFAULT_TEACHER_FULL_NAME,
        ),
        journal_number=journal_number,
        birth_date=_resolve_birth_date(payload),
        report_scope=normalize_report_scope(payload.get("report_scope")),
        report_year=report_year,
    )


def load_input_file(path: Path) -> CanonicalInput:
    return validate_input_payload(parse_input_text(path.read_text(encoding="utf-8")))


def canonical_input_document(raw_input: CanonicalInput) -> dict[str, Any]:
    return {
        "meta": {
            "stage": STAGE_ID,
            "language": "ru",
            "schema": SCHEMA_ID,
            "format_note": "Файл хранится в JSON-подмножестве YAML для детерминированной записи без внешних зависимостей.",
        },
        "student_full_name": raw_input.student_full_name,
        "student_group": raw_input.student_group,
        "teacher_full_name": raw_input.teacher_full_name,
        "journal_number": raw_input.journal_number,
        "birth_date": raw_input.birth_date,
        "report_scope": raw_input.report_scope,
        "report_year": raw_input.report_year,
    }
