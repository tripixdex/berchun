from __future__ import annotations

from dataclasses import asdict

from src.compute.common import expected_from_probabilities
from src.compute.task1_common import finite_queue_probabilities, input_snapshot
from src.domain.types import RegimeMarker, SolverMetadata, SolverPoint, SweepResult, Task1DerivedInputs

def _loss_system_point(params: Task1DerivedInputs, operators: int) -> SolverPoint:
    probabilities = finite_queue_probabilities(
        params.arrival_rate_per_second,
        params.service_rate_per_second,
        operators,
        queue_places=0,
    )
    refusal_probability = probabilities[-1]
    busy_expected = expected_from_probabilities(probabilities, lambda state: float(state))
    return SolverPoint(
        x_value=operators,
        status="ok",
        regime=RegimeMarker(status="ok", is_stationary=True),
        metrics={
            "refusal_probability": refusal_probability,
            "busy_operators_expected": busy_expected,
            "operators_utilization": busy_expected / operators,
        },
        diagnostics={
            "throughput_rate_per_second": params.arrival_rate_per_second * (1.0 - refusal_probability),
        },
    )

def _limited_queue_point(
    params: Task1DerivedInputs, operators: int, queue_places: int, x_value: int
) -> SolverPoint:
    probabilities = finite_queue_probabilities(
        params.arrival_rate_per_second,
        params.service_rate_per_second,
        operators,
        queue_places=queue_places,
    )
    total_capacity = operators + queue_places
    busy_expected = expected_from_probabilities(
        probabilities, lambda state: float(min(state, operators))
    )
    queue_length_expected = sum(
        (state - operators) * probabilities[state]
        for state in range(operators + 1, total_capacity + 1)
    )
    return SolverPoint(
        x_value=x_value,
        status="ok",
        regime=RegimeMarker(status="ok", is_stationary=True),
        metrics={
            "refusal_probability": probabilities[total_capacity],
            "busy_operators_expected": busy_expected,
            "operators_utilization": busy_expected / operators,
            "queue_exists_probability": sum(probabilities[operators + 1 :]),
            "queue_length_expected": queue_length_expected,
            "queue_occupancy": queue_length_expected / queue_places,
        },
        fixed_parameters={"operators": operators, "queue_places": queue_places},
    )

def solve_task_1_1(params: Task1DerivedInputs) -> dict[str, object]:
    points: list[SolverPoint] = []
    operators = 1
    minimal_operators = None
    while True:
        point = _loss_system_point(params, operators)
        points.append(point)
        refusal_probability = point.metrics["refusal_probability"]
        if refusal_probability is not None and refusal_probability < params.refusal_target_probability:
            minimal_operators = operators
            break
        operators += 1
        if operators > 200:
            raise RuntimeError("Refusal target < 0.01 was not reached up to 200 operators")

    sweep = SweepResult(
        task_id="1.1",
        model="M/M/n/n",
        x_axis="operators",
        fixed_parameters={},
        points=points,
        notes=[
            "Вероятность отказа вычисляется как вероятность полного заполнения системы без очереди.",
            "Останов перебора: первое число операторов, где P_refusal < 0.01.",
        ],
        summary={
            "minimal_operators_for_refusal_below_target": minimal_operators,
            "refusal_target_probability": params.refusal_target_probability,
        },
    )
    return {
        "task_id": "1.1",
        "title_ru": "Система без очереди",
        "input_snapshot": input_snapshot(params),
        "metadata": asdict(
            SolverMetadata(solver_kind="analytical", formula_family="birth-death finite")
        ),
        "sweeps": [asdict(sweep)],
        "summary": sweep.summary,
    }

def solve_task_1_2(params: Task1DerivedInputs) -> dict[str, object]:
    by_queue_places = []
    for operators in range(1, params.max_operators_limited_queue + 1):
        points = [
            _limited_queue_point(params, operators, queue_places, x_value=queue_places)
            for queue_places in range(1, params.max_queue_places + 1)
        ]
        by_queue_places.append(
            asdict(
                SweepResult(
                    task_id="1.2",
                    model="M/M/n/K",
                    x_axis="queue_places",
                    fixed_parameters={"operators": operators},
                    points=points,
                )
            )
        )

    by_operators = []
    for queue_places in range(1, params.max_queue_places + 1):
        points = [
            _limited_queue_point(params, operators, queue_places, x_value=operators)
            for operators in range(1, params.max_operators_limited_queue + 1)
        ]
        by_operators.append(
            asdict(
                SweepResult(
                    task_id="1.2",
                    model="M/M/n/K",
                    x_axis="operators",
                    fixed_parameters={"queue_places": queue_places},
                    points=points,
                )
            )
        )

    return {
        "task_id": "1.2",
        "title_ru": "Система с ограниченной очередью",
        "input_snapshot": input_snapshot(params),
        "metadata": asdict(
            SolverMetadata(solver_kind="analytical", formula_family="birth-death finite")
        ),
        "sweeps": [
            {"sweep_kind": "families_by_queue_places", "series": by_queue_places},
            {"sweep_kind": "families_by_operators", "series": by_operators},
        ],
        "summary": {
            "operators_range": [1, params.max_operators_limited_queue],
            "queue_places_range": [1, params.max_queue_places],
        },
    }
