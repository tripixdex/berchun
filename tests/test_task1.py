from __future__ import annotations

import unittest
from pathlib import Path

from src.compute.task1 import solve_task_1_1, solve_task_1_3, solve_task_1_4
from src.variant import derive_inputs, load_variant


class Task1SolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        raw = load_variant(Path("inputs/variant_me.yaml"))
        cls.derived_inputs, _ = derive_inputs(raw)

    def test_task_1_1_reaches_refusal_target(self) -> None:
        result = solve_task_1_1(self.derived_inputs.task1)
        points = result["sweeps"][0]["points"]
        self.assertGreater(len(points), 0)
        last_point = points[-1]
        self.assertEqual(last_point["status"], "ok")
        self.assertLess(last_point["metrics"]["refusal_probability"], 0.01)
        self.assertEqual(
            result["summary"]["minimal_operators_for_refusal_below_target"],
            last_point["x_value"],
        )

    def test_task_1_3_marks_non_stationary_points(self) -> None:
        result = solve_task_1_3(self.derived_inputs.task1)
        points = result["sweeps"][0]["points"]
        non_stationary = [point for point in points if point["status"] == "non_stationary"]
        stationary = [point for point in points if point["status"] == "ok"]
        self.assertGreater(len(non_stationary), 0)
        self.assertGreater(len(stationary), 0)
        self.assertIsNone(non_stationary[0]["metrics"]["queue_length_expected"])

    def test_task_1_4_exposes_truncation_metadata(self) -> None:
        result = solve_task_1_4(self.derived_inputs.task1)
        points = result["sweeps"][0]["points"]
        self.assertEqual(points[0]["status"], "stationary_truncated")
        self.assertIsNotNone(points[0]["truncation"])
        self.assertIn("tail_probability_upper_bound", points[0]["truncation"])


if __name__ == "__main__":
    unittest.main()
