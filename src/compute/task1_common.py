from __future__ import annotations

from src.compute.common import build_birth_death_probabilities
from src.domain.types import Task1DerivedInputs


def input_snapshot(params: Task1DerivedInputs) -> dict[str, float | int]:
    return {
        "tc_seconds": params.tc_seconds,
        "ts_seconds": params.ts_seconds,
        "tw_seconds": params.tw_seconds,
        "arrival_rate_per_second": params.arrival_rate_per_second,
        "service_rate_per_second": params.service_rate_per_second,
        "abandonment_rate_per_second": params.abandonment_rate_per_second,
        "offered_load_erlangs": params.offered_load_erlangs,
    }


def finite_queue_probabilities(
    arrival_rate: float, service_rate: float, operators: int, queue_places: int
) -> list[float]:
    total_capacity = operators + queue_places
    ratios = []
    for state in range(1, total_capacity + 1):
        service_channels = state if state <= operators else operators
        ratios.append(arrival_rate / (service_channels * service_rate))
    return build_birth_death_probabilities(ratios)
