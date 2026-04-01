from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


def _collect_report_manifest_paths(manifest: dict[str, object]) -> list[str]:
    paths: list[str] = []
    for key in ("report_source_file", "report_pdf_path", "report_docx_path", "variant_source_file", "derived_source_file"):
        value = manifest.get(key)
        if isinstance(value, str):
            paths.append(value)
    for key in ("data_inputs_used", "figure_inputs_used"):
        values = manifest.get(key)
        if isinstance(values, list):
            paths.extend(item for item in values if isinstance(item, str))
    for list_key, path_key in (
        ("additional_artifacts_used", "path"),
        ("title_assets_used", "output_image_path"),
        ("formula_assets_used", "output_image_path"),
        ("formula_assets_used", "path"),
    ):
        entries = manifest.get(list_key)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get(path_key), str):
                paths.append(entry[path_key])
    return paths


class DeliveryManifestNormalizationTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_report_only_docx_bundle_uses_delivery_local_report_manifest_subset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "report_only", "--output-format", "docx", "--report-scope", "full")
            )

            report_manifest = json.loads((Path(summary["delivery_dir"]) / "report" / "assets_manifest.json").read_text(encoding="utf-8"))
            self.assertIsNone(report_manifest["report_pdf_path"])
            self.assertEqual(report_manifest["report_docx_path"], "report/final_report.docx")
            self.assertIsNone(report_manifest["report_source_file"])
            self.assertIsNone(report_manifest["variant_source_file"])
            self.assertIsNone(report_manifest["derived_source_file"])
            self.assertEqual(report_manifest["data_inputs_used"], [])
            self.assertEqual(report_manifest["figure_inputs_used"], [])
            self.assertEqual(report_manifest["additional_artifacts_used"], [])
            self.assertEqual(report_manifest["title_assets_used"], [])
            self.assertTrue(report_manifest["meta"]["delivery_local_paths"])
            self.assertFalse(any("runs/" in path for path in _collect_report_manifest_paths(report_manifest)))

    def test_report_only_bundle_uses_delivery_local_report_manifest_subset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "report_only", "--output-format", "pdf", "--report-scope", "full")
            )

            report_manifest = json.loads((Path(summary["delivery_dir"]) / "report" / "assets_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(report_manifest["report_pdf_path"], "report/final_report.pdf")
            self.assertIsNone(report_manifest["report_source_file"])
            self.assertIsNone(report_manifest["variant_source_file"])
            self.assertIsNone(report_manifest["derived_source_file"])
            self.assertEqual(report_manifest["data_inputs_used"], [])
            self.assertEqual(report_manifest["figure_inputs_used"], [])
            self.assertEqual(report_manifest["additional_artifacts_used"], [])
            self.assertEqual(report_manifest["title_assets_used"], [])
            self.assertTrue(report_manifest["meta"]["delivery_local_paths"])
            self.assertFalse(any("runs/" in path for path in _collect_report_manifest_paths(report_manifest)))

    def test_study_pack_general_bundle_keeps_only_delivery_local_report_refs(self) -> None:
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
                    "pdf",
                )
            )

            report_manifest = json.loads((Path(summary["delivery_dir"]) / "report" / "assets_manifest.json").read_text(encoding="utf-8"))
            self.assertIsNone(report_manifest["report_pdf_path"])
            self.assertEqual(report_manifest["report_docx_path"], "report/final_report.docx")
            self.assertEqual(report_manifest["figure_inputs_used"], [])
            self.assertEqual(report_manifest["additional_artifacts_used"], [])
            self.assertEqual(report_manifest["title_assets_used"], [])
            self.assertFalse(any(path.startswith("guide/") for path in _collect_report_manifest_paths(report_manifest)))
            self.assertFalse(any("runs/" in path for path in _collect_report_manifest_paths(report_manifest)))

    def test_print_pack_bundle_rewrites_report_manifest_to_bundle_local_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            paths = self.workspace_paths(temp_path)
            input_path = self.write_input_file(temp_path, "task1")
            build = self.run_success(self.build_args(paths, input_path))
            summary = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "print_pack", "--output-format", "bundle_dir", "--report-scope", "task1")
            )

            delivery_dir = Path(summary["delivery_dir"])
            report_manifest = json.loads((delivery_dir / "report" / "assets_manifest.json").read_text(encoding="utf-8"))
            normalized_paths = _collect_report_manifest_paths(report_manifest)
            self.assertEqual(report_manifest["report_source_file"], "report/final_report.tex")
            self.assertEqual(report_manifest["report_pdf_path"], "report/final_report.pdf")
            self.assertEqual(report_manifest["data_inputs_used"], [])
            self.assertTrue(all(not Path(path).is_absolute() for path in normalized_paths))
            self.assertFalse(any("runs/" in path for path in normalized_paths))
            self.assertTrue(all((delivery_dir / path).exists() for path in normalized_paths))
            self.assertTrue(all(path.startswith("figures/task1_") for path in report_manifest["figure_inputs_used"]))
            self.assertTrue(all(item["path"].startswith("report/assets/task1_") for item in report_manifest["additional_artifacts_used"]))
            self.assertEqual(report_manifest["title_assets_used"][0]["output_image_path"], "report/assets/title_emblem.jpeg")


if __name__ == "__main__":
    unittest.main()
