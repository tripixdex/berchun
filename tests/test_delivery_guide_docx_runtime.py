from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from src.delivery_assets import filter_guide_text
from src.delivery_guide_docx import export_guide_docx
from tests._delivery_support import DeliveryCliTestMixin


class DeliveryGuideDocxRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_guide_only_variant_docx_delivery_produces_non_empty_docx(self) -> None:
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
                    "docx",
                    "--guide-mode",
                    "variant_aware",
                    "--guide-scope",
                    "task1",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            docx_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__variant.docx"
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertIn("guide/methodical_guide__variant.docx", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__variant.md", manifest["artifacts"])
            self.assertGreater(docx_path.stat().st_size, 0)

    def test_guide_only_general_docx_delivery_produces_non_empty_docx_without_run_id(self) -> None:
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
                    "docx",
                    "--guide-mode",
                    "general",
                    "--guide-scope",
                    "task2",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            docx_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__general.docx"
            self.assertEqual(manifest["source_kind"], "general_baseline")
            self.assertEqual(manifest["guide_source_kind"], "general_baseline")
            self.assertIn("guide/methodical_guide__general.docx", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__general.md", manifest["artifacts"])
            self.assertGreater(docx_path.stat().st_size, 0)

    def test_guide_docx_exporter_supports_relative_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            guide_dir = temp_path / "delivery" / "guide"
            guide_dir.mkdir(parents=True)
            guide_text = filter_guide_text(Path("docs/methodical/content/METHODICAL_GUIDE_GENERAL_SOURCE.md").read_text(encoding="utf-8"), "task2")
            markdown_path = guide_dir / "methodical_guide__general.md"
            markdown_path.write_text(guide_text, encoding="utf-8")
            current_dir = Path.cwd()
            os.chdir(temp_path)
            try:
                relative_docx = Path("nested/guide.docx")
                export_guide_docx(markdown_path=markdown_path, docx_path=relative_docx, title="General Guide")
            finally:
                os.chdir(current_dir)
            self.assertGreater((temp_path / "nested" / "guide.docx").stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
