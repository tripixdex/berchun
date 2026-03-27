from __future__ import annotations

import unittest

from src.input_schema import CanonicalInput
from src.run_archive import raw_input_hash


class RunArchiveTests(unittest.TestCase):
    def test_hash_uses_full_canonical_raw_input(self) -> None:
        baseline = CanonicalInput(
            student_full_name="Иванов Иван Иванович",
            student_group="РК9-00Б",
            teacher_full_name="Берчун Юрий Валерьевич",
            journal_number=4,
            birth_day=25,
            birth_month=6,
            birth_year=2003,
            report_year=2026,
        )
        changed_identity = CanonicalInput(
            student_full_name="Петров Петр Петрович",
            student_group="РК9-00Б",
            teacher_full_name="Берчун Юрий Валерьевич",
            journal_number=4,
            birth_day=25,
            birth_month=6,
            birth_year=2003,
            report_year=2026,
        )

        self.assertNotEqual(raw_input_hash(baseline), raw_input_hash(changed_identity))


if __name__ == "__main__":
    unittest.main()
