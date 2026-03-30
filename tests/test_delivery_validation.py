from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


class DeliveryValidationTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_invalid_delivery_combinations_fail_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_mock_guide(paths["guide_source_path"])
            self.write_mock_general_guide(paths["guide_general_source_path"])
            build = self.run_success(self.build_args(paths))
            cases = [
                (
                    self.deliver_args(
                        paths,
                        build["run_id"],
                        "--delivery-profile",
                        "guide_only",
                        "--output-format",
                        "md",
                        "--guide-mode",
                        "general",
                        "--guide-scope",
                        "full",
                    ),
                    "does not accept source_run_id",
                ),
                (
                    self.deliver_args(
                        paths,
                        build["run_id"],
                        "--delivery-profile",
                        "study_pack",
                        "--output-format",
                        "bundle_dir",
                        "--report-scope",
                        "task1",
                        "--guide-mode",
                        "variant_aware",
                        "--guide-scope",
                        "task2",
                    ),
                    "guide_scope",
                ),
                (
                    self.deliver_args(
                        paths,
                        build["run_id"],
                        "--delivery-profile",
                        "study_pack",
                        "--output-format",
                        "docx",
                        "--report-scope",
                        "full",
                        "--guide-mode",
                        "variant_aware",
                        "--guide-scope",
                        "full",
                    ),
                    "bundle_dir",
                ),
                (
                    self.deliver_args(
                        paths,
                        build["run_id"],
                        "--delivery-profile",
                        "print_pack",
                        "--output-format",
                        "docx",
                        "--report-scope",
                        "full",
                    ),
                    "bundle_dir",
                ),
                (["deliver", "--runs-dir", str(paths["runs_dir"]), "--deliveries-dir", str(paths["deliveries_dir"]), "--delivery-profile", "report_only", "--output-format", "pdf", "--report-scope", "full"], "source_run_id"),
            ]
            for args, needle in cases:
                with self.subTest(args=args):
                    self.assertIn(needle, self.run_failure(args))


if __name__ == "__main__":
    unittest.main()
