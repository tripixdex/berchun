from __future__ import annotations

import math
from pathlib import Path
from typing import Callable, Sequence


def validate_positive_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")


def validate_probability(name: str, value: float) -> None:
    if value < -1e-12 or value > 1.0 + 1e-12:
        raise ValueError(f"{name} must be within [0, 1], got {value!r}")


def build_birth_death_probabilities(ratios: Sequence[float]) -> list[float]:
    weights = [1.0]
    for ratio in ratios:
        if ratio < 0.0:
            raise ValueError(f"Birth-death ratio must be non-negative, got {ratio!r}")
        weights.append(weights[-1] * ratio)
    total_weight = sum(weights)
    if total_weight <= 0.0 or not math.isfinite(total_weight):
        raise ValueError("Birth-death normalization failed")
    probabilities = [weight / total_weight for weight in weights]
    for index, probability in enumerate(probabilities):
        validate_probability(f"probabilities[{index}]", probability)
    return probabilities


def expected_from_probabilities(
    probabilities: Sequence[float], projector: Callable[[int], float]
) -> float:
    return sum(projector(index) * probability for index, probability in enumerate(probabilities))


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def erlang_a_probabilities_with_truncation(
    arrival_rate: float,
    service_rate: float,
    servers: int,
    abandonment_rate: float,
    epsilon_probability: float,
    epsilon_queue: float,
    max_state: int,
) -> tuple[list[float], dict[str, float | int | bool]]:
    validate_positive_int("servers", servers)
    if arrival_rate <= 0.0 or service_rate <= 0.0 or abandonment_rate <= 0.0:
        raise ValueError("Rates must be positive for Erlang-A")

    weights = [1.0]
    for state in range(1, servers + 1):
        weights.append(weights[-1] * arrival_rate / (state * service_rate))

    current_sum = sum(weights)
    last_state = servers
    tail_probability_upper_bound = math.inf
    tail_queue_upper_bound = math.inf

    while True:
        queued_customers_next = last_state - servers + 1
        next_ratio = arrival_rate / (servers * service_rate + queued_customers_next * abandonment_rate)
        next_weight = weights[-1] * next_ratio

        if next_ratio < 1.0:
            tail_probability_upper_bound = next_weight / (1.0 - next_ratio)
            tail_queue_upper_bound = next_weight * (
                (queued_customers_next / (1.0 - next_ratio))
                + (next_ratio / ((1.0 - next_ratio) ** 2))
            )
            normalized_prob_bound = tail_probability_upper_bound / current_sum
            normalized_queue_bound = tail_queue_upper_bound / current_sum
            if (
                normalized_prob_bound <= epsilon_probability
                and normalized_queue_bound <= epsilon_queue
            ):
                break

        if last_state >= max_state:
            raise RuntimeError(
                "Erlang-A truncation did not reach requested tolerance "
                f"before state {max_state}"
            )

        weights.append(next_weight)
        current_sum += next_weight
        last_state += 1

    probabilities = [weight / current_sum for weight in weights]
    return probabilities, {
        "used": True,
        "included_max_state": last_state,
        "epsilon_probability": epsilon_probability,
        "epsilon_queue": epsilon_queue,
        "tail_probability_upper_bound": tail_probability_upper_bound / current_sum,
        "tail_queue_upper_bound": tail_queue_upper_bound / current_sum,
    }
