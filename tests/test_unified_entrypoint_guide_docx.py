from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.cli import main


class UnifiedEntrypointGuideDocxTests(unittest.TestCase):
    def _build_args(self, temp_path: Path) -> list[str]:
        return [
            "build",
            "--runs-dir",
            str(temp_path / "runs"),
            "--deliveries-dir",
            str(temp_path / "deliveries"),
            "--variant-path",
            str(temp_path / "workspace" / "inputs" / "variant_me.yaml"),
            "--derived-path",
            str(temp_path / "workspace" / "inputs" / "derived_parameters.json"),
            "--out-dir",
            str(temp_path / "workspace" / "out" / "data"),
            "--data-dir",
            str(temp_path / "workspace" / "out" / "data"),
            "--figures-dir",
            str(temp_path / "workspace" / "figures"),
            "--manifest-path",
            str(temp_path / "workspace" / "out" / "artifacts" / "figure_manifest.json"),
            "--report-source-path",
            str(temp_path / "workspace" / "report" / "final_report.tex"),
            "--report-pdf-path",
            str(temp_path / "workspace" / "report" / "final_report.pdf"),
            "--report-assets-manifest-path",
            str(temp_path / "workspace" / "report" / "assets_manifest.json"),
            "--offer-delivery",
            "--input",
            "inputs/examples/student_example.yaml",
            "--review",
        ]

    def test_unified_session_can_finish_with_guide_only_general_docx(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout, stderr = io.StringIO(), io.StringIO()
            with patch("builtins.input", side_effect=["confirm", "4", "2", "3", "2", "confirm"]), redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(self._build_args(Path(temp_dir)))
            self.assertEqual(exit_code, 0, stderr.getvalue())
            summary = json.loads(stdout.getvalue())
            delivery = summary["delivery"]
            manifest = json.loads(Path(delivery["result"]["delivery_manifest_path"]).read_text(encoding="utf-8"))
            docx_path = Path(delivery["result"]["delivery_dir"]) / "guide" / "methodical_guide__general.docx"
            self.assertEqual(delivery["request"]["delivery_profile"], "guide_only")
            self.assertEqual(delivery["request"]["guide_mode"], "general")
            self.assertEqual(delivery["request"]["output_format"], "docx")
            self.assertIn("guide/methodical_guide__general.docx", manifest["artifacts"])
            self.assertGreater(docx_path.stat().st_size, 0)
            self.assertIn("Только материалы для подготовки", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
