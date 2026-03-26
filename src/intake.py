from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from src.compute.common import ensure_directory
from src.input_schema import CanonicalInput, canonical_input_document, load_input_file, validate_input_payload

PROMPTS = (
    ("student_full_name", "Student full name"),
    ("student_group", "Student group"),
    ("teacher_full_name", "Teacher full name"),
    ("journal_number", "Journal number"),
    ("birth_day", "Birth day"),
    ("birth_month", "Birth month"),
    ("birth_year", "Birth year"),
    ("report_year", "Report year"),
)


def load_canonical_input(path: Path) -> CanonicalInput:
    return load_input_file(path)


def prompt_canonical_input(prompt: Callable[[str], str] | None = None) -> CanonicalInput:
    prompt = input if prompt is None else prompt
    answers = {field: prompt(f"{label}: ").strip() for field, label in PROMPTS}
    return validate_input_payload(answers)


def write_canonical_input(path: Path, raw_input: CanonicalInput) -> None:
    ensure_directory(path.parent)
    path.write_text(
        json.dumps(canonical_input_document(raw_input), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
