from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.cli import main
from src.delivery_session import PROFILE_FORMATS


class CliOperatorSurfaceTests(unittest.TestCase):
    def _base_build_args(self, temp_path: Path) -> list[str]:
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
        ]

    def _delivery_build_args(self, temp_path: Path) -> list[str]:
        return [
            *self._base_build_args(temp_path),
            "--offer-delivery",
            "--input",
            "inputs/examples/student_example.yaml",
            "--review",
        ]

    def test_unified_session_exposes_supported_formats_per_profile(self) -> None:
        self.assertEqual(PROFILE_FORMATS["report_only"], ("pdf", "docx"))
        self.assertEqual(PROFILE_FORMATS["study_pack"], ("bundle_dir",))
        self.assertEqual(PROFILE_FORMATS["guide_only"], ("pdf", "docx"))
        self.assertEqual(PROFILE_FORMATS["print_pack"], ("bundle_dir",))

    def test_default_operator_flow_is_quiet_and_enter_first(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with patch("builtins.input", side_effect=["", "3", "", ""]), redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(self._delivery_build_args(Path(temp_dir)))
            self.assertEqual(exit_code, 0, stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("Действие [Enter=подтвердить, x=отмена]:", stderr.getvalue())
            self.assertIn("Действие [Enter=создать, e=изменить, x=отмена]:", stderr.getvalue())
            self.assertIn("Готово.", stderr.getvalue())
            self.assertIn("Что создано:", stderr.getvalue())
            self.assertNotIn('"session_mode"', stderr.getvalue())
            self.assertNotIn('"delivery"', stderr.getvalue())

    def test_build_can_choose_yaml_inside_same_cli_session(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            stderr = io.StringIO()
            args = [*self._base_build_args(Path(temp_dir)), "--json", "--input", "--review"]
            with patch("builtins.input", side_effect=["2", ""]), redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(args)
            self.assertEqual(exit_code, 0, stderr.getvalue())
            summary = json.loads(stdout.getvalue())
            self.assertEqual(summary["report_scope"], "full")
            self.assertIn("Найденные YAML-файлы:", stderr.getvalue())
            self.assertIn("inputs/examples/student_example.yaml", stderr.getvalue())
            self.assertIn("Выберите YAML [Enter=1,", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
