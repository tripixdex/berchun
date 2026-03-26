from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.pipeline import run
from src.variant import derive_inputs, load_variant


class VariantIntegrityTests(unittest.TestCase):
    def test_variant_file_is_parsed_correctly(self) -> None:
        raw = load_variant(Path("inputs/variant_me.yaml"))
        self.assertEqual(raw.journal_number, 4)
        self.assertEqual(raw.birth_day, 25)
        self.assertEqual(raw.birth_month, 6)
        self.assertIn("user_corrected_stage_02_pass_a", raw.source_tags)

    def test_derived_parameters_match_confirmed_variant(self) -> None:
        raw = load_variant(Path("inputs/variant_me.yaml"))
        derived_inputs, derived_document = derive_inputs(raw)

        self.assertEqual(derived_inputs.task1.tc_seconds, 14)
        self.assertEqual(derived_inputs.task1.ts_seconds, 65)
        self.assertEqual(derived_inputs.task1.tw_seconds, 106)
        self.assertEqual(derived_inputs.task2.machine_count, 36)
        self.assertEqual(derived_inputs.task2.tc_minutes, 104)
        self.assertEqual(derived_inputs.task2.ts_minutes, 50)
        self.assertAlmostEqual(
            derived_document["derived"]["task1"]["offered_load_erlangs"]["value"],
            65 / 14,
        )
        self.assertEqual(
            derived_document["derived"]["sweep_policies"]["task_2_1"]["repairers"],
            "1..36",
        )

    def test_cli_writes_json_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            derived_path = temp_path / "derived_parameters.json"
            out_dir = temp_path / "out"

            run(
                variant_path=Path("inputs/variant_me.yaml"),
                derived_path=derived_path,
                out_dir=out_dir,
            )

            self.assertTrue(derived_path.exists())
            for filename in [
                "task_1_1.json",
                "task_1_2.json",
                "task_1_3.json",
                "task_1_4.json",
                "task_2_1.json",
            ]:
                artifact_path = out_dir / filename
                self.assertTrue(artifact_path.exists(), msg=str(artifact_path))
                json.loads(artifact_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
