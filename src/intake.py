from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from src.compute.common import ensure_directory
from src.input_schema import (
    DEFAULT_TEACHER_FULL_NAME,
    CanonicalInput,
    canonical_input_document,
    load_input_file,
    validate_input_payload,
)
from src.report_scope import REPORT_SCOPE_LABELS

GROUP_CHOICES = ("РК9-81Б", "РК9-82Б", "РК9-83Б", "РК9-84Б")
SUMMARY_FIELDS = (
    ("student_full_name", "ФИО студента"),
    ("student_group", "Группа"),
    ("teacher_full_name", "Преподаватель"),
    ("journal_number", "Номер по журналу"),
    ("birth_date", "Дата рождения"),
    ("report_scope", "Состав отчёта"),
    ("report_year", "Год отчёта"),
)
FIELD_LABELS = dict(SUMMARY_FIELDS)


def load_canonical_input(path: Path) -> CanonicalInput:
    return load_input_file(path)


def _payload(raw_input: CanonicalInput) -> dict[str, object]:
    return {key: value for key, value in canonical_input_document(raw_input).items() if key != "meta"}


def _pretty_value(field: str, value: object) -> str:
    if field == "report_scope":
        return f"{value} ({REPORT_SCOPE_LABELS[str(value)]})"
    return str(value)


def _ask_group(prompt: Callable[[str], str], current: str | None = None) -> str:
    suffix = f" [{current}]" if current else ""
    while True:
        choice = prompt(
            "Группа" + suffix + " [1=РК9-81Б, 2=РК9-82Б, 3=РК9-83Б, 4=РК9-84Б, 5=другая группа]: "
        ).strip()
        if choice in {"1", "2", "3", "4"}:
            return GROUP_CHOICES[int(choice) - 1]
        if choice in {"5", "другая группа"}:
            custom = prompt("Введите группу (например: РК9-82Б): ").strip()
            if custom:
                return custom
            continue
        if choice:
            return choice


def _ask_scope(prompt: Callable[[str], str], current: str = "full") -> str:
    raw = prompt(f"Состав отчёта [{current}] [1=full (обе задачи), 2=task1, 3=task2, Enter={current}]: ").strip().lower()
    return {"": current, "1": "full", "2": "task1", "3": "task2"}.get(raw, raw)


def _ask_field(field: str, prompt: Callable[[str], str], current: object | None = None) -> object:
    current_text = "" if current is None else f" [{current}]"
    if field == "student_full_name":
        return prompt(f"ФИО студента (например: Иванов Иван Иванович){current_text}: ").strip()
    if field == "student_group":
        return _ask_group(prompt, None if current is None else str(current))
    if field == "teacher_full_name":
        answer = prompt(f"Преподаватель{current_text} [Enter={DEFAULT_TEACHER_FULL_NAME}]: ").strip()
        return DEFAULT_TEACHER_FULL_NAME if not answer else answer
    if field == "birth_date":
        return prompt(f"Дата рождения (ДД.ММ.ГГГГ, например: 25.06.2000){current_text}: ").strip()
    if field == "report_scope":
        return _ask_scope(prompt, "full" if current is None else str(current))
    if field == "journal_number":
        return prompt(f"Номер по журналу (например: 7){current_text}: ").strip()
    if field == "report_year":
        return prompt(f"Год отчёта (например: 2026){current_text}: ").strip()
    return prompt(f"{FIELD_LABELS[field]}{current_text}: ").strip()


def prompt_canonical_input(prompt: Callable[[str], str] | None = None) -> CanonicalInput:
    prompt = input if prompt is None else prompt
    answers = {
        "student_full_name": _ask_field("student_full_name", prompt),
        "student_group": _ask_field("student_group", prompt),
        "teacher_full_name": _ask_field("teacher_full_name", prompt),
        "journal_number": _ask_field("journal_number", prompt),
        "birth_date": _ask_field("birth_date", prompt),
        "report_scope": _ask_field("report_scope", prompt),
    }
    return validate_input_payload(answers)


def canonical_input_summary(raw_input: CanonicalInput) -> str:
    document = _payload(raw_input)
    lines = ["Нормализованный raw input:"]
    for index, (field, label) in enumerate(SUMMARY_FIELDS, start=1):
        lines.append(f"{index}. {label}: {_pretty_value(field, document[field])}")
    return "\n".join(lines)


def _resolve_field_choice(choice: str) -> str:
    normalized = choice.strip()
    if normalized.isdigit():
        index = int(normalized)
        if 1 <= index <= len(SUMMARY_FIELDS):
            return SUMMARY_FIELDS[index - 1][0]
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
        action_prompt = "Действие [Enter=подтвердить, e=исправить, x=отмена]: " if allow_edit else "Действие [Enter=подтвердить, x=отмена]: "
        action = prompt(action_prompt).strip().lower()
        if action in {"", "confirm", "c", "yes", "y", "да", "д"}:
            return raw_input
        if action in {"cancel", "x", "no", "n", "нет", "н"}:
            raise ValueError("build cancelled by user")
        if allow_edit and action in {"edit", "e", "редактировать", "r"}:
            field = _resolve_field_choice(prompt("Поле для редактирования (номер или имя): "))
            payload = _payload(raw_input)
            updated_value = _ask_field(field, prompt, payload[field])
            payload[field] = payload[field] if updated_value == "" else updated_value
            raw_input = validate_input_payload(payload)
            continue
        display("Неизвестное действие. Нажмите Enter для подтверждения, e для исправления или x для отмены." if allow_edit else "Неизвестное действие. Нажмите Enter для подтверждения или x для отмены.")


def write_canonical_input(path: Path, raw_input: CanonicalInput) -> None:
    ensure_directory(path.parent)
    path.write_text(
        json.dumps(canonical_input_document(raw_input), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
