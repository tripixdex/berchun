from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


class DeliveryGuidePdfRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_guide_only_variant_pdf_delivery_produces_non_empty_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_mock_guide(paths["guide_source_path"])
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(
                    paths,
                    build["run_id"],
                    "--delivery-profile",
                    "guide_only",
                    "--output-format",
                    "pdf",
                    "--guide-mode",
                    "variant_aware",
                    "--guide-scope",
                    "task1",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            pdf_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__variant.pdf"
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertIn("guide/methodical_guide__variant.pdf", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__variant.md", manifest["artifacts"])
            self.assertGreater(pdf_path.stat().st_size, 0)

    def test_guide_only_general_pdf_delivery_produces_non_empty_pdf_without_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_mock_general_guide(paths["guide_general_source_path"])
            self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(
                    paths,
                    None,
                    "--delivery-profile",
                    "guide_only",
                    "--output-format",
                    "pdf",
                    "--guide-mode",
                    "general",
                    "--guide-scope",
                    "task2",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            pdf_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__general.pdf"
            self.assertEqual(manifest["source_kind"], "general_baseline")
            self.assertEqual(manifest["guide_source_kind"], "general_baseline")
            self.assertIn("guide/methodical_guide__general.pdf", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__general.md", manifest["artifacts"])
            self.assertGreater(pdf_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
