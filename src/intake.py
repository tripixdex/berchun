from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Callable

from src.compute.common import ensure_directory
from src.input_schema import CanonicalInput, canonical_input_document, load_input_file, validate_input_payload

PROMPTS = (
    ("student_full_name", "ФИО студента"),
    ("student_group", "Группа"),
    ("teacher_full_name", "Преподаватель"),
    ("journal_number", "Номер по журналу"),
    ("birth_day", "День рождения"),
    ("birth_month", "Месяц рождения"),
    ("birth_year", "Год рождения"),
    ("report_year", "Год отчёта"),
)
FIELD_LABELS = dict(PROMPTS)


def load_canonical_input(path: Path) -> CanonicalInput:
    return load_input_file(path)


def prompt_canonical_input(prompt: Callable[[str], str] | None = None) -> CanonicalInput:
    prompt = input if prompt is None else prompt
    answers = {field: prompt(f"{label}: ").strip() for field, label in PROMPTS}
    return validate_input_payload(answers)


def canonical_input_summary(raw_input: CanonicalInput) -> str:
    document = canonical_input_document(raw_input)
    lines = ["Нормализованный raw input:"]
    for index, (field, label) in enumerate(PROMPTS, start=1):
        lines.append(f"{index}. {label}: {document[field]}")
    return "\n".join(lines)


def _resolve_field_choice(choice: str) -> str:
    normalized = choice.strip()
    if normalized.isdigit():
        index = int(normalized)
        if 1 <= index <= len(PROMPTS):
            return PROMPTS[index - 1][0]
    if normalized in FIELD_LABELS:
        return normalized
    raise ValueError(f"unknown field for edit: {choice!r}")


def review_canonical_input(
    raw_input: CanonicalInput,
    prompt: Callable[[str], str] | None = None,
    display: Callable[[str], None] | None = None,
    allow_edit: bool = False,
) -> CanonicalInput:
    prompt = input if prompt is None else prompt
    display = print if display is None else display
    while True:
        display(canonical_input_summary(raw_input))
        action_prompt = "Действие [confirm/edit/cancel]: " if allow_edit else "Действие [confirm/cancel]: "
        action = prompt(action_prompt).strip().lower()
        if action in {"confirm", "c", "yes", "y", "да", "д"}:
            return raw_input
        if action in {"cancel", "x", "no", "n", "нет", "н"}:
            raise ValueError("build cancelled by user")
        if allow_edit and action in {"edit", "e", "редактировать", "r"}:
            field = _resolve_field_choice(prompt("Поле для редактирования (номер или имя): "))
            payload = asdict(raw_input)
            current_value = str(payload[field])
            updated_value = prompt(f"{FIELD_LABELS[field]} [{current_value}]: ").strip()
            payload[field] = current_value if not updated_value else updated_value
            raw_input = validate_input_payload(payload)
            continue
        display("Неизвестное действие. Используйте confirm, edit или cancel." if allow_edit else "Неизвестное действие. Используйте confirm или cancel.")


def write_canonical_input(path: Path, raw_input: CanonicalInput) -> None:
    ensure_directory(path.parent)
    path.write_text(
        json.dumps(canonical_input_document(raw_input), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
