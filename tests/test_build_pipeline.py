from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.build_pipeline import resolve_build_input
from src.cli import main


class BuildPipelineTests(unittest.TestCase):
    def test_build_requires_exactly_one_input_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolve_build_input(input_path=None, interactive=False)

    def test_cli_build_from_input_file_produces_report_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            variant_path = temp_path / "inputs" / "variant_me.yaml"
            derived_path = temp_path / "inputs" / "derived_parameters.json"
            out_dir = temp_path / "out" / "data"
            figures_dir = temp_path / "figures"
            figure_manifest_path = temp_path / "out" / "artifacts" / "figure_manifest.json"
            report_source_path = temp_path / "report" / "final_report.tex"
            report_pdf_path = temp_path / "report" / "final_report.pdf"
            assets_manifest_path = temp_path / "report" / "assets_manifest.json"
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "build",
                        "--input",
                        "inputs/examples/student_example.yaml",
                        "--variant-path",
                        str(variant_path),
                        "--derived-path",
                        str(derived_path),
                        "--out-dir",
                        str(out_dir),
                        "--figures-dir",
                        str(figures_dir),
                        "--manifest-path",
                        str(figure_manifest_path),
                        "--report-source-path",
                        str(report_source_path),
                        "--report-pdf-path",
                        str(report_pdf_path),
                        "--report-assets-manifest-path",
                        str(assets_manifest_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(report_pdf_path.exists())
            self.assertGreater(report_pdf_path.stat().st_size, 0)
            self.assertTrue(report_source_path.exists())
            self.assertTrue(assets_manifest_path.exists())
            self.assertTrue(variant_path.exists())
            self.assertTrue(derived_path.exists())
            summary = json.loads(stdout.getvalue())
            self.assertEqual(summary["report"]["report_year"], 2026)
            self.assertEqual(summary["solve"]["variant_path"], str(variant_path))


if __name__ == "__main__":
    unittest.main()
