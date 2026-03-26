from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.input_schema import load_input_file, validate_input_payload
from src.intake import prompt_canonical_input, write_canonical_input
from src.variant import load_variant


class InputValidationTests(unittest.TestCase):
    def test_example_input_file_is_valid(self) -> None:
        raw_input = load_input_file(Path("inputs/examples/student_example.yaml"))
        self.assertEqual(raw_input.journal_number, 4)
        self.assertEqual(raw_input.birth_day, 25)
        self.assertEqual(raw_input.birth_month, 6)

    def test_invalid_birth_date_fails_cleanly(self) -> None:
        with self.assertRaisesRegex(ValueError, "must form a valid date"):
            validate_input_payload(
                {
                    "student_full_name": " Иванов   Иван Иванович ",
                    "student_group": " РК9-00Б ",
                    "teacher_full_name": " Петров Петр Петрович ",
                    "journal_number": "4",
                    "birth_day": "31",
                    "birth_month": "2",
                    "birth_year": "2000",
                    "report_year": "2026",
                }
            )

    def test_interactive_intake_writes_pipeline_compatible_variant(self) -> None:
        answers = [
            "  Иванов   Иван Иванович  ",
            " РК9-00Б ",
            " Петров Петр Петрович ",
            "4",
            "25",
            "6",
            "2000",
            "2026",
        ]
        with tempfile.TemporaryDirectory() as temp_dir, patch("builtins.input", side_effect=answers):
            variant_path = Path(temp_dir) / "variant_me.yaml"
            raw_input = prompt_canonical_input()
            write_canonical_input(variant_path, raw_input)

            stored = json.loads(variant_path.read_text(encoding="utf-8"))
            variant = load_variant(variant_path)
            self.assertEqual(stored["student_full_name"], "Иванов Иван Иванович")
            self.assertEqual(variant.journal_number, 4)
            self.assertEqual(variant.birth_day, 25)
            self.assertEqual(variant.birth_month, 6)


if __name__ == "__main__":
    unittest.main()
