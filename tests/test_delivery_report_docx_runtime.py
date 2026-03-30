from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from src.delivery_report_docx import export_report_docx
from tests._delivery_support import DeliveryCliTestMixin


class DeliveryReportDocxRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_report_only_docx_delivery_produces_non_empty_docx(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(paths, build["run_id"], "--delivery-profile", "report_only", "--output-format", "docx", "--report-scope", "full")
            )

            delivery_dir = Path(summary["delivery_dir"])
            manifest = self.assert_manifest_artifacts_exist(summary)
            docx_path = delivery_dir / "report" / "final_report.docx"
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertEqual(manifest["delivery_profile"], "report_only")
            self.assertEqual(manifest["output_format"], "docx")
            self.assertIn("report/final_report.docx", manifest["artifacts"])
            self.assertNotIn("report/final_report.pdf", manifest["artifacts"])
            self.assertGreater(docx_path.stat().st_size, 0)

    def test_report_docx_exporter_supports_relative_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_source_path = (Path.cwd() / "report" / "final_report.tex").resolve()
            current_dir = Path.cwd()
            os.chdir(temp_path)
            try:
                relative_docx = Path("nested/report.docx")
                export_report_docx(report_source_path=report_source_path, docx_path=relative_docx)
            finally:
                os.chdir(current_dir)
            self.assertGreater((temp_path / "nested" / "report.docx").stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
