from __future__ import annotations

import math
from dataclasses import asdict

from src.compute.common import erlang_a_probabilities_with_truncation, expected_from_probabilities
from src.compute.task1_common import input_snapshot
from src.domain.types import RegimeMarker, SolverMetadata, SolverPoint, SweepResult, Task1DerivedInputs

def _unlimited_queue_point(params: Task1DerivedInputs, operators: int) -> SolverPoint:
    traffic_intensity = params.offered_load_erlangs / operators
    if traffic_intensity >= 1.0:
        return SolverPoint(
            x_value=operators,
            status="non_stationary",
            regime=RegimeMarker(
                status="non_stationary",
                is_stationary=False,
                reason="lambda >= operators * mu",
            ),
            metrics={
                "busy_operators_expected": None,
                "operators_utilization": None,
                "queue_exists_probability": None,
                "queue_length_expected": None,
            },
            diagnostics={"traffic_intensity": traffic_intensity},
        )

    offered_load = params.offered_load_erlangs
    erlang_term = (offered_load**operators) / math.factorial(operators)
    p0_denominator = sum(
        (offered_load**state) / math.factorial(state) for state in range(operators)
    ) + erlang_term / (1.0 - traffic_intensity)
    p0 = 1.0 / p0_denominator
    wait_probability = (erlang_term * p0) / (1.0 - traffic_intensity)
    return SolverPoint(
        x_value=operators,
        status="ok",
        regime=RegimeMarker(status="ok", is_stationary=True),
        metrics={
            "busy_operators_expected": offered_load,
            "operators_utilization": offered_load / operators,
            "queue_exists_probability": wait_probability * traffic_intensity,
            "queue_length_expected": wait_probability * traffic_intensity / (1.0 - traffic_intensity),
        },
        diagnostics={
            "traffic_intensity": traffic_intensity,
            "wait_probability": wait_probability,
        },
    )

def _abandonment_point(params: Task1DerivedInputs, operators: int) -> SolverPoint:
    try:
        probabilities, truncation = erlang_a_probabilities_with_truncation(
            arrival_rate=params.arrival_rate_per_second,
            service_rate=params.service_rate_per_second,
            servers=operators,
            abandonment_rate=params.abandonment_rate_per_second,
            epsilon_probability=params.truncation_probability_epsilon,
            epsilon_queue=params.truncation_queue_epsilon,
            max_state=params.truncation_max_state,
        )
    except RuntimeError as error:
        return SolverPoint(
            x_value=operators,
            status="truncation_limit_reached",
            regime=RegimeMarker(
                status="truncation_limit_reached",
                is_stationary=None,
                reason=str(error),
            ),
            metrics={
                "busy_operators_expected": None,
                "operators_utilization": None,
                "queue_exists_probability": None,
                "queue_length_expected": None,
            },
            diagnostics={"traffic_intensity": params.offered_load_erlangs / operators},
        )

    busy_expected = expected_from_probabilities(
        probabilities, lambda state: float(min(state, operators))
    )
    return SolverPoint(
        x_value=operators,
        status="stationary_truncated",
        regime=RegimeMarker(
            status="stationary_truncated",
            is_stationary=True,
            reason="Infinite-state Erlang-A normalized after deterministic tail truncation.",
        ),
        metrics={
            "busy_operators_expected": busy_expected,
            "operators_utilization": busy_expected / operators,
            "queue_exists_probability": sum(probabilities[operators + 1 :]),
            "queue_length_expected": sum(
                (state - operators) * probabilities[state]
                for state in range(operators + 1, len(probabilities))
            ),
        },
        truncation=truncation,
        diagnostics={"traffic_intensity": params.offered_load_erlangs / operators},
    )

def solve_task_1_3(params: Task1DerivedInputs) -> dict[str, object]:
    points = [
        _unlimited_queue_point(params, operators)
        for operators in range(1, params.max_operators_unlimited_queue + 1)
    ]
    stable_operators = [point.x_value for point in points if point.status == "ok"]
    sweep = SweepResult(
        task_id="1.3",
        model="M/M/n",
        x_axis="operators",
        fixed_parameters={},
        points=points,
        notes=[
            "Точки с lambda >= n * mu помечаются как non_stationary и не получают фиктивных стационарных метрик."
        ],
        summary={
            "first_stationary_operators": stable_operators[0] if stable_operators else None,
            "non_stationary_operators": [
                point.x_value for point in points if point.status == "non_stationary"
            ],
        },
    )
    return {
        "task_id": "1.3",
        "title_ru": "Система с неограниченной очередью",
        "input_snapshot": input_snapshot(params),
        "metadata": asdict(
            SolverMetadata(solver_kind="analytical", formula_family="Erlang-C closed form")
        ),
        "sweeps": [asdict(sweep)],
        "summary": sweep.summary,
    }

def solve_task_1_4(params: Task1DerivedInputs) -> dict[str, object]:
    points = [
        _abandonment_point(params, operators)
        for operators in range(1, params.max_operators_with_abandonment + 1)
    ]
    sweep = SweepResult(
        task_id="1.4",
        model="M/M/n+M",
        x_axis="operators",
        fixed_parameters={},
        points=points,
        notes=[
            "Интенсивность ухода считается как nu = 1 / Tw.",
            "Бесконечный хвост распределения усекается по детерминированной верхней оценке на хвост вероятностей и хвост среднего размера очереди.",
        ],
        summary={
            "operators_range": [1, params.max_operators_with_abandonment],
            "truncation_probability_epsilon": params.truncation_probability_epsilon,
            "truncation_queue_epsilon": params.truncation_queue_epsilon,
        },
    )
    return {
        "task_id": "1.4",
        "title_ru": "Система с неограниченной очередью и уходом клиентов",
        "input_snapshot": input_snapshot(params),
        "metadata": asdict(
            SolverMetadata(
                solver_kind="analytical",
                formula_family="birth-death infinite with abandonment",
                uses_truncation=True,
                truncation_policy={
                    "epsilon_probability": params.truncation_probability_epsilon,
                    "epsilon_queue": params.truncation_queue_epsilon,
                    "max_state": params.truncation_max_state,
                },
            )
        ),
        "sweeps": [asdict(sweep)],
        "summary": sweep.summary,
    }
