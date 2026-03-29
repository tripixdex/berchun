from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.build_pipeline import resolve_build_input
from src.input_schema import current_report_year, load_input_file, validate_input_payload
from src.intake import prompt_canonical_input, write_canonical_input
from src.variant import load_variant


class InputValidationTests(unittest.TestCase):
    @staticmethod
    def _prompt_from(answers: list[str], prompts: list[str] | None = None):
        iterator = iter(answers)

        def _prompt(message: str) -> str:
            if prompts is not None:
                prompts.append(message)
            return next(iterator)

        return _prompt

    def test_example_input_file_is_valid(self) -> None:
        raw_input = load_input_file(Path("inputs/examples/student_example.yaml"))
        self.assertEqual(raw_input.journal_number, 4)
        self.assertEqual(raw_input.birth_date, "25.06.2000")
        self.assertEqual(raw_input.report_scope, "full")
        self.assertEqual(raw_input.report_year, current_report_year())

    def test_invalid_birth_date_fails_cleanly(self) -> None:
        with self.assertRaisesRegex(ValueError, "valid date"):
            validate_input_payload(
                {
                    "student_full_name": " Иванов   Иван Иванович ",
                    "student_group": " РК9-00Б ",
                    "teacher_full_name": " Петров Петр Петрович ",
                    "journal_number": "4",
                    "birth_date": "31.02.2000",
                    "report_scope": "full",
                }
            )

    def test_interactive_intake_quick_select_default_teacher_and_auto_year(self) -> None:
        prompts: list[str] = []
        answers = ["  Иванов   Иван Иванович  ", "4", "", "4", "25.06.2000", ""]
        raw_input = prompt_canonical_input(prompt=self._prompt_from(answers, prompts))
        self.assertEqual(raw_input.student_full_name, "Иванов Иван Иванович")
        self.assertEqual(raw_input.student_group, "РК9-84Б")
        self.assertEqual(raw_input.teacher_full_name, "Берчун Юрий Валерьевич")
        self.assertEqual(raw_input.report_scope, "full")
        self.assertEqual(raw_input.report_year, current_report_year())
        self.assertTrue(all("Год отчёта" not in message for message in prompts))

    def test_interactive_intake_custom_group_is_supported(self) -> None:
        answers = ["Иванов Иван Иванович", "5", " РК9-00Б ", "", "7", "25.06.2000", "task2"]
        raw_input = prompt_canonical_input(prompt=self._prompt_from(answers))
        self.assertEqual(raw_input.student_group, "РК9-00Б")
        self.assertEqual(raw_input.report_scope, "task2")

    def test_interactive_intake_writes_pipeline_compatible_variant(self) -> None:
        answers = ["Иванов Иван Иванович", "4", "", "4", "25.06.2000", ""]
        with tempfile.TemporaryDirectory() as temp_dir:
            variant_path = Path(temp_dir) / "variant_me.yaml"
            raw_input = prompt_canonical_input(prompt=self._prompt_from(answers))
            write_canonical_input(variant_path, raw_input)

            stored = json.loads(variant_path.read_text(encoding="utf-8"))
            variant = load_variant(variant_path)
            self.assertEqual(stored["birth_date"], "25.06.2000")
            self.assertEqual(stored["report_scope"], "full")
            self.assertEqual(variant.journal_number, 4)
            self.assertEqual(variant.birth_day, 25)
            self.assertEqual(variant.birth_month, 6)

    def test_interactive_review_edit_updates_normalized_input(self) -> None:
        answers = [
            "Иванов Иван Иванович",
            "4",
            "",
            "4",
            "25.06.2000",
            "",
            "edit",
            "6",
            "task1",
            "confirm",
        ]
        messages: list[str] = []
        raw_input = resolve_build_input(
            input_path=None,
            interactive=True,
            prompt=self._prompt_from(answers),
            display=messages.append,
        )
        self.assertEqual(raw_input.report_scope, "task1")
        self.assertTrue(messages)
        self.assertIn("Состав отчёта: task1", messages[-1])

    def test_interactive_review_cancel_fails_cleanly(self) -> None:
        answers = ["Иванов Иван Иванович", "4", "", "4", "25.06.2000", "", "cancel"]
        with self.assertRaisesRegex(ValueError, "build cancelled"):
            resolve_build_input(
                input_path=None,
                interactive=True,
                prompt=self._prompt_from(answers),
                display=lambda _message: None,
            )

    def test_file_review_preview_returns_normalized_input(self) -> None:
        messages: list[str] = []
        raw_input = resolve_build_input(
            input_path=Path("inputs/examples/student_example.yaml"),
            interactive=False,
            review=True,
            prompt=self._prompt_from(["confirm"]),
            display=messages.append,
        )
        self.assertEqual(raw_input.student_group, "РК9-84Б")
        self.assertEqual(raw_input.report_scope, "full")
        self.assertTrue(messages)
        self.assertIn("Дата рождения: 25.06.2000", messages[0])
        self.assertIn("Состав отчёта: full", messages[0])


if __name__ == "__main__":
    unittest.main()
