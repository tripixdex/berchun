from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

RegimeStatus = Literal[
    "ok",
    "non_stationary",
    "stationary_truncated",
    "truncation_limit_reached",
    "invalid_input",
]


@dataclass(frozen=True)
class RawVariantInputs:
    journal_number: int
    birth_day: int
    birth_month: int
    source_tags: tuple[str, ...]


@dataclass(frozen=True)
class Task1DerivedInputs:
    tc_seconds: int
    ts_seconds: int
    tw_seconds: int
    arrival_rate_per_second: float
    service_rate_per_second: float
    abandonment_rate_per_second: float
    offered_load_erlangs: float
    max_operators_limited_queue: int = 15
    max_queue_places: int = 15
    max_operators_unlimited_queue: int = 15
    max_operators_with_abandonment: int = 15
    refusal_target_probability: float = 0.01
    truncation_probability_epsilon: float = 1e-12
    truncation_queue_epsilon: float = 1e-12
    truncation_max_state: int = 100000


@dataclass(frozen=True)
class Task2DerivedInputs:
    machine_count: int
    tc_minutes: int
    ts_minutes: int
    arrival_rate_per_minute: float
    service_rate_per_minute: float
    offered_load_per_machine_erlangs: float
    max_repairers: int


@dataclass(frozen=True)
class DerivedInputs:
    raw: RawVariantInputs
    task1: Task1DerivedInputs
    task2: Task2DerivedInputs


@dataclass(frozen=True)
class RegimeMarker:
    status: RegimeStatus
    is_stationary: bool | None
    reason: str | None = None


@dataclass(frozen=True)
class SolverPoint:
    x_value: int
    status: RegimeStatus
    regime: RegimeMarker
    metrics: dict[str, float | None]
    fixed_parameters: dict[str, int] = field(default_factory=dict)
    truncation: dict[str, Any] | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SweepResult:
    task_id: str
    model: str
    x_axis: str
    fixed_parameters: dict[str, int]
    points: list[SolverPoint]
    notes: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SolverMetadata:
    solver_kind: str
    formula_family: str
    uses_truncation: bool = False
    truncation_policy: dict[str, Any] | None = None
