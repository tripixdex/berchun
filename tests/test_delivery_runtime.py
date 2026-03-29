from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


class DeliveryRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_report_only_pdf_delivery_copies_report_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "report_only", "--output-format", "pdf", "--report-scope", "full")
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "report_only")
            self.assertEqual(manifest["report_scope"], "full")
            self.assertEqual(manifest["artifacts"], ["delivery_manifest.json", "report/final_report.pdf", "report/assets_manifest.json"])

    def test_guide_only_variant_md_delivery_filters_scope_and_copies_assets(self) -> None:
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
                    "md",
                    "--guide-mode",
                    "variant_aware",
                    "--guide-scope",
                    "task1",
                )
            )

            delivery_dir = Path(summary["delivery_dir"])
            guide_text = (delivery_dir / "guide" / "methodical_guide__variant.md").read_text(encoding="utf-8")
            manifest = self.assert_manifest_artifacts_exist(summary)
            scheme_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/schemes/")]
            plot_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/plots/")]
            self.assertIn("## Задача 1. Проектирование колл-центра", guide_text)
            self.assertNotIn("## Задача 2. Производственный участок", guide_text)
            self.assertEqual(len(scheme_paths), 4)
            self.assertEqual(len(plot_paths), 22)
            self.assertEqual(manifest["guide_scope"], "task1")
            self.assertEqual(manifest["guide_mode"], "variant_aware")

    def test_study_pack_variant_bundle_is_populated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_mock_guide(paths["guide_source_path"])
            build = self.run_success(self.build_args(paths))
            study = self.run_success(
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
                    "variant_aware",
                    "--guide-scope",
                    "full",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(study)
            scheme_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/schemes/")]
            plot_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/plots/")]
            self.assertEqual(study["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "study_pack")
            self.assertEqual(manifest["report_scope"], "full")
            self.assertEqual(manifest["guide_scope"], "full")
            self.assertIn("report/final_report.pdf", manifest["artifacts"])
            self.assertIn("report/assets_manifest.json", manifest["artifacts"])
            self.assertIn("guide/methodical_guide__variant.md", manifest["artifacts"])
            self.assertEqual(len(scheme_paths), 5)
            self.assertEqual(len(plot_paths), 27)

    def test_print_pack_bundle_filters_assets_by_report_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            paths = self.workspace_paths(temp_path)
            input_path = self.write_input_file(temp_path, "task1")
            build = self.run_success(self.build_args(paths, input_path))
            print_pack = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "print_pack", "--output-format", "bundle_dir", "--report-scope", "task1")
            )

            manifest = self.assert_manifest_artifacts_exist(print_pack)
            asset_paths = [item for item in manifest["artifacts"] if item.startswith("report/assets/")]
            figure_paths = [item for item in manifest["artifacts"] if item.startswith("figures/")]
            report_manifest = json.loads((Path(print_pack["delivery_dir"]) / "report" / "assets_manifest.json").read_text(encoding="utf-8"))
            referenced_paths = [
                *report_manifest.get("figure_inputs_used", []),
                *(item.get("path") for item in report_manifest.get("additional_artifacts_used", [])),
                *(item.get("output_image_path") for item in report_manifest.get("title_assets_used", [])),
            ]
            self.assertEqual(print_pack["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "print_pack")
            self.assertEqual(manifest["report_scope"], "task1")
            self.assertIn("report/final_report.pdf", manifest["artifacts"])
            self.assertIn("report/final_report.tex", manifest["artifacts"])
            self.assertIn("report/assets_manifest.json", manifest["artifacts"])
            self.assertIn("report/assets/title_emblem.jpeg", asset_paths)
            self.assertEqual(len(asset_paths), 5)
            self.assertEqual(len(figure_paths), 22)
            self.assertTrue(all(path.startswith("figures/task1_") for path in figure_paths))
            self.assertFalse(any(path.startswith("figures/task2_") for path in figure_paths))
            self.assertTrue(all(isinstance(path, str) and Path(path).exists() for path in referenced_paths))


if __name__ == "__main__":
    unittest.main()
