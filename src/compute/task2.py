from __future__ import annotations

from dataclasses import asdict

from src.compute.common import build_birth_death_probabilities, expected_from_probabilities
from src.domain.types import RegimeMarker, SolverMetadata, SolverPoint, SweepResult, Task2DerivedInputs


def _input_snapshot(params: Task2DerivedInputs) -> dict[str, float | int]:
    return {
        "machine_count": params.machine_count,
        "tc_minutes": params.tc_minutes,
        "ts_minutes": params.ts_minutes,
        "arrival_rate_per_minute": params.arrival_rate_per_minute,
        "service_rate_per_minute": params.service_rate_per_minute,
        "offered_load_per_machine_erlangs": params.offered_load_per_machine_erlangs,
    }


def _repairer_probabilities(params: Task2DerivedInputs, repairers: int) -> list[float]:
    ratios = []
    for failed_machines in range(1, params.machine_count + 1):
        birth_rate = (params.machine_count - failed_machines + 1) * params.arrival_rate_per_minute
        death_rate = min(failed_machines, repairers) * params.service_rate_per_minute
        ratios.append(birth_rate / death_rate)
    return build_birth_death_probabilities(ratios)


def _waiting_probability_for_arrival(
    probabilities: list[float], machine_count: int, repairers: int
) -> float:
    weighted_total = sum((machine_count - state) * probabilities[state] for state in range(machine_count))
    weighted_wait = sum(
        (machine_count - state) * probabilities[state]
        for state in range(repairers, machine_count)
    )
    return 0.0 if weighted_total == 0.0 else weighted_wait / weighted_total


def _repairer_point(params: Task2DerivedInputs, repairers: int) -> SolverPoint:
    probabilities = _repairer_probabilities(params, repairers)
    idle_machines_expected = expected_from_probabilities(probabilities, float)
    waiting_machines_expected = expected_from_probabilities(
        probabilities, lambda failed: float(max(failed - repairers, 0))
    )
    busy_repairers_expected = expected_from_probabilities(
        probabilities, lambda failed: float(min(failed, repairers))
    )
    repairers_utilization = busy_repairers_expected / repairers
    waiting_probability = _waiting_probability_for_arrival(
        probabilities, params.machine_count, repairers
    )
    queue_exists_probability_state = sum(probabilities[repairers + 1 :])
    return SolverPoint(
        x_value=repairers,
        status="ok",
        regime=RegimeMarker(status="ok", is_stationary=True),
        metrics={
            "idle_machines_expected": idle_machines_expected,
            "waiting_machines_expected": waiting_machines_expected,
            "waiting_probability": waiting_probability,
            "busy_repairers_expected": busy_repairers_expected,
            "repairers_utilization": repairers_utilization,
        },
        diagnostics={
            "queue_exists_probability_state": queue_exists_probability_state,
            "waiting_probability_interpretation": (
                "arrival_weighted_probability_for_new_breakdown"
            ),
        },
    )


def solve_task_2_1(params: Task2DerivedInputs) -> dict[str, object]:
    points = [_repairer_point(params, repairers) for repairers in range(1, params.max_repairers + 1)]
    sweep = SweepResult(
        task_id="2.1",
        model="machine-repairman finite-source",
        x_axis="repairers",
        fixed_parameters={},
        points=points,
        notes=[
            "Состояние = число неисправных станков.",
            "waiting_probability трактуется как вероятность того, что новый отказ поступит в систему, где все наладчики уже заняты.",
        ],
        summary={
            "repairers_range": [1, params.max_repairers],
        },
    )
    return {
        "task_id": "2.1",
        "title_ru": "Производственный участок",
        "input_snapshot": _input_snapshot(params),
        "metadata": asdict(
            SolverMetadata(solver_kind="analytical", formula_family="birth-death finite-source")
        ),
        "sweeps": [asdict(sweep)],
        "summary": sweep.summary,
    }
