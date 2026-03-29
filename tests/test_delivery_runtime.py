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

            manifest = json.loads(Path(summary["delivery_manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "report_only")
            self.assertEqual(manifest["report_scope"], "full")
            self.assertEqual(manifest["artifacts"], ["delivery_manifest.json", "report/final_report.pdf", "report/assets_manifest.json"])
            self.assertTrue((Path(summary["delivery_dir"]) / "report" / "final_report.pdf").exists())
            self.assertTrue((Path(summary["delivery_dir"]) / "report" / "assets_manifest.json").exists())

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
            manifest = json.loads(Path(summary["delivery_manifest_path"]).read_text(encoding="utf-8"))
            scheme_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/schemes/")]
            plot_paths = [item for item in manifest["artifacts"] if item.startswith("guide/assets/plots/")]
            self.assertIn("## Задача 1. Проектирование колл-центра", guide_text)
            self.assertNotIn("## Задача 2. Производственный участок", guide_text)
            self.assertEqual(len(scheme_paths), 4)
            self.assertEqual(len(plot_paths), 22)
            self.assertEqual(manifest["guide_scope"], "task1")
            self.assertEqual(manifest["guide_mode"], "variant_aware")

    def test_bundle_profiles_create_profile_aware_skeletons(self) -> None:
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
            print_pack = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "print_pack", "--output-format", "bundle_dir", "--report-scope", "full")
            )

            self.assertTrue((Path(study["delivery_dir"]) / "report").is_dir())
            self.assertTrue((Path(study["delivery_dir"]) / "guide" / "assets" / "schemes").is_dir())
            self.assertTrue((Path(print_pack["delivery_dir"]) / "report").is_dir())
            self.assertTrue((Path(print_pack["delivery_dir"]) / "figures").is_dir())
            self.assertEqual(study["assembly_state"], "skeleton_only")
            self.assertEqual(print_pack["assembly_state"], "skeleton_only")


if __name__ == "__main__":
    unittest.main()
