from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.compute.common import validate_positive_int
from src.domain.types import DerivedInputs, RawVariantInputs, Task1DerivedInputs, Task2DerivedInputs
from src.input_schema import validate_input_payload

STAGE_ID = "STAGE 02"
LANGUAGE = "ru"
PRIMARY_SOURCE = "my_var.md"
VARIANT_SOURCE = "inputs/variant_me.yaml"
TRUNCATION_NOTE_RU = (
    "Хвост бесконечного ряда обрезается по верхней оценке на хвост вероятностей "
    "и на хвост среднего числа заявок в очереди."
)

def _legacy_variant(payload: dict[str, Any]) -> RawVariantInputs:
    journal_number = int(payload["journal_number"]["value"])
    birth_day = int(payload["birth_day"]["value"])
    birth_month = int(payload["birth_month"]["value"])
    validate_positive_int("journal_number", journal_number)
    validate_positive_int("birth_day", birth_day)
    validate_positive_int("birth_month", birth_month)
    if birth_day > 31:
        raise ValueError(f"birth_day must be <= 31, got {birth_day!r}")
    if birth_month > 12:
        raise ValueError(f"birth_month must be <= 12, got {birth_month!r}")
    source_tags = tuple(
        dict.fromkeys(
            payload["journal_number"]["source_tags"]
            + payload["birth_day"]["source_tags"]
            + payload["birth_month"]["source_tags"]
        )
    )
    return RawVariantInputs(journal_number=journal_number, birth_day=birth_day, birth_month=birth_month, source_tags=source_tags)


def load_variant(path: Path) -> RawVariantInputs:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload.get("journal_number"), dict):
        return _legacy_variant(payload)
    canonical = validate_input_payload(payload)
    return RawVariantInputs(
        journal_number=canonical.journal_number,
        birth_day=canonical.birth_day,
        birth_month=canonical.birth_month,
        source_tags=("canonical_stage_07_input", "canonical_scope_aware_input"),
    )

def _raw_entry(value: int, source_tags: tuple[str, ...]) -> dict[str, Any]:
    return {
        "value": value,
        "status": "confirmed_raw",
        "source_tags": list(source_tags),
    }

def _derived_entry(value: float | int, formula: str) -> dict[str, Any]:
    return {
        "value": value,
        "status": "derived",
        "formula": formula,
    }

def _build_task1(raw: RawVariantInputs) -> Task1DerivedInputs:
    tc_seconds = 10 + raw.journal_number
    ts_seconds = 40 + raw.birth_day
    tw_seconds = 100 + raw.birth_month
    return Task1DerivedInputs(
        tc_seconds=tc_seconds,
        ts_seconds=ts_seconds,
        tw_seconds=tw_seconds,
        arrival_rate_per_second=1.0 / tc_seconds,
        service_rate_per_second=1.0 / ts_seconds,
        abandonment_rate_per_second=1.0 / tw_seconds,
        offered_load_erlangs=ts_seconds / tc_seconds,
    )

def _build_task2(raw: RawVariantInputs) -> Task2DerivedInputs:
    machine_count = 30 + raw.birth_month
    tc_minutes = 100 + raw.journal_number
    ts_minutes = 25 + raw.birth_day
    return Task2DerivedInputs(
        machine_count=machine_count,
        tc_minutes=tc_minutes,
        ts_minutes=ts_minutes,
        arrival_rate_per_minute=1.0 / tc_minutes,
        service_rate_per_minute=1.0 / ts_minutes,
        offered_load_per_machine_erlangs=ts_minutes / tc_minutes,
        max_repairers=machine_count,
    )

def _build_derived_document(
    raw: RawVariantInputs, task1: Task1DerivedInputs, task2: Task2DerivedInputs
) -> dict[str, Any]:
    return {
        "meta": {
            "stage": STAGE_ID,
            "language": LANGUAGE,
            "primary_source": PRIMARY_SOURCE,
            "variant_source": VARIANT_SOURCE,
        },
        "raw_inputs": {
            "journal_number": _raw_entry(raw.journal_number, raw.source_tags),
            "birth_day": _raw_entry(raw.birth_day, raw.source_tags),
            "birth_month": _raw_entry(raw.birth_month, raw.source_tags),
        },
        "derived": {
            "task1": {
                "tc_seconds": _derived_entry(task1.tc_seconds, "10 + journal_number"),
                "ts_seconds": _derived_entry(task1.ts_seconds, "40 + birth_day"),
                "tw_seconds": _derived_entry(task1.tw_seconds, "100 + birth_month"),
                "arrival_rate_per_second": _derived_entry(
                    task1.arrival_rate_per_second, "1 / tc_seconds"
                ),
                "service_rate_per_second": _derived_entry(
                    task1.service_rate_per_second, "1 / ts_seconds"
                ),
                "abandonment_rate_per_second": _derived_entry(
                    task1.abandonment_rate_per_second, "1 / tw_seconds"
                ),
                "offered_load_erlangs": _derived_entry(
                    task1.offered_load_erlangs,
                    "arrival_rate_per_second / service_rate_per_second",
                ),
            },
            "task2": {
                "machine_count": _derived_entry(task2.machine_count, "30 + birth_month"),
                "tc_minutes": _derived_entry(task2.tc_minutes, "100 + journal_number"),
                "ts_minutes": _derived_entry(task2.ts_minutes, "25 + birth_day"),
                "arrival_rate_per_minute": _derived_entry(
                    task2.arrival_rate_per_minute, "1 / tc_minutes"
                ),
                "service_rate_per_minute": _derived_entry(
                    task2.service_rate_per_minute, "1 / ts_minutes"
                ),
                "offered_load_per_machine_erlangs": _derived_entry(
                    task2.offered_load_per_machine_erlangs,
                    "arrival_rate_per_minute / service_rate_per_minute",
                ),
            },
            "sweep_policies": {
                "task_1_1": {
                    "operators": "1..k, где k — первое значение с refusal_probability < 0.01"
                },
                "task_1_2": {
                    "operators": f"1..{task1.max_operators_limited_queue}",
                    "queue_places": f"1..{task1.max_queue_places}",
                },
                "task_1_3": {"operators": f"1..{task1.max_operators_unlimited_queue}"},
                "task_1_4": {"operators": f"1..{task1.max_operators_with_abandonment}"},
                "task_2_1": {"repairers": f"1..{task2.max_repairers}"},
            },
            "truncation_policy": {
                "task_1_4": {
                    "epsilon_probability": task1.truncation_probability_epsilon,
                    "epsilon_queue": task1.truncation_queue_epsilon,
                    "max_state": task1.truncation_max_state,
                    "note_ru": TRUNCATION_NOTE_RU,
                }
            },
        },
    }

def derive_inputs(raw: RawVariantInputs) -> tuple[DerivedInputs, dict[str, Any]]:
    task1 = _build_task1(raw)
    task2 = _build_task2(raw)
    derived_inputs = DerivedInputs(raw=raw, task1=task1, task2=task2)
    return derived_inputs, _build_derived_document(raw, task1, task2)
