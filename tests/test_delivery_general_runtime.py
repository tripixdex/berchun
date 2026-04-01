from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


class DeliveryGeneralRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_guide_only_general_md_delivery_uses_general_source_without_run_id(self) -> None:
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
                    "md",
                    "--guide-mode",
                    "general",
                    "--guide-scope",
                    "task1",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            guide_text = (Path(summary["delivery_dir"]) / "guide" / "methodical_guide__general.md").read_text(encoding="utf-8")
            scheme_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/schemes/")]
            plot_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/plots/")]
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "guide_only")
            self.assertEqual(manifest["source_kind"], "general_baseline")
            self.assertEqual(manifest["guide_source_kind"], "general_baseline")
            self.assertIsNone(manifest["source_run_id"])
            self.assertIn("general task1 body", guide_text)
            self.assertNotIn("## Задача 2. Производственный участок", guide_text)
            self.assertEqual(len(scheme_paths), 4)
            self.assertEqual(plot_paths, [])

    def test_study_pack_general_bundle_is_populated_without_guide_plots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_mock_general_guide(paths["guide_general_source_path"])
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(
                    paths,
                    build["run_id"],
                    "--delivery-profile",
                    "study_pack",
                    "--output-format",
                    "bundle_dir",
                    "--report-scope",
                    "full",
                    "--guide-mode",
                    "general",
                    "--guide-scope",
                    "full",
                    "--report-output-format",
                    "docx",
                    "--guide-output-format",
                    "pdf_docx",
                )
            )

            delivery_dir = Path(summary["delivery_dir"])
            manifest = self.assert_manifest_artifacts_exist(summary)
            scheme_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/schemes/")]
            plot_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/plots/")]
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "study_pack")
            self.assertEqual(manifest["source_kind"], "run_bundle")
            self.assertEqual(manifest["guide_source_kind"], "general_baseline")
            self.assertEqual(manifest["source_run_id"], build["run_id"])
            self.assertEqual(manifest["report_output_format"], "docx")
            self.assertEqual(manifest["guide_output_format"], "pdf_docx")
            self.assertNotIn("report/final_report.pdf", manifest["artifacts"])
            self.assertIn("report/final_report.docx", manifest["artifacts"])
            self.assertIn("report/assets_manifest.json", manifest["artifacts"])
            self.assertIn("guide/methodical_guide__general.md", manifest["artifacts"])
            self.assertIn("guide/methodical_guide__general.pdf", manifest["artifacts"])
            self.assertIn("guide/methodical_guide__general.docx", manifest["artifacts"])
            self.assertGreater((delivery_dir / "guide" / "methodical_guide__general.pdf").stat().st_size, 0)
            self.assertGreater((delivery_dir / "guide" / "methodical_guide__general.docx").stat().st_size, 0)
            self.assertGreater((delivery_dir / "report" / "final_report.docx").stat().st_size, 0)
            self.assertEqual(len(scheme_paths), 5)
            self.assertEqual(plot_paths, [])


if __name__ == "__main__":
    unittest.main()
