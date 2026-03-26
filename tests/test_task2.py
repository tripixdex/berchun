from __future__ import annotations

import unittest
from pathlib import Path

from src.compute.task2 import solve_task_2_1
from src.variant import derive_inputs, load_variant


class Task2SolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        raw = load_variant(Path("inputs/variant_me.yaml"))
        cls.derived_inputs, _ = derive_inputs(raw)

    def test_task_2_1_returns_structured_points(self) -> None:
        result = solve_task_2_1(self.derived_inputs.task2)
        points = result["sweeps"][0]["points"]
        self.assertEqual(len(points), self.derived_inputs.task2.machine_count)
        self.assertIn("waiting_probability", points[0]["metrics"])
        self.assertIn("queue_exists_probability_state", points[0]["diagnostics"])

    def test_waiting_probability_is_not_silently_out_of_range(self) -> None:
        result = solve_task_2_1(self.derived_inputs.task2)
        for point in result["sweeps"][0]["points"]:
            waiting_probability = point["metrics"]["waiting_probability"]
            self.assertGreaterEqual(waiting_probability, 0.0)
            self.assertLessEqual(waiting_probability, 1.0)


if __name__ == "__main__":
    unittest.main()
