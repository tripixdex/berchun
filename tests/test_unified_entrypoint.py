from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.cli import main
class UnifiedEntrypointTests(unittest.TestCase):
    def _build_args(self, temp_path: Path, extra: list[str]) -> list[str]:
        return [
            "build",
            "--json",
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
            *extra,
        ]

    def _run_session(self, args: list[str], answers: list[str]) -> tuple[dict[str, object], str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(args)
        self.assertEqual(exit_code, 0, stderr.getvalue())
        return json.loads(stdout.getvalue()), stderr.getvalue()

    def _task1_input(self, temp_path: Path) -> Path:
        path = temp_path / "student_task1.yaml"
        path.write_text(
            Path("inputs/examples/student_example.yaml").read_text(encoding="utf-8").replace('report_scope: "full"', 'report_scope: "task1"'),
            encoding="utf-8",
        )
        return path

    def test_interactive_build_can_finish_with_no_extra_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary, _stderr = self._run_session(
                self._build_args(temp_path, ["--interactive"]),
                ["Иванов Иван Иванович", "4", "", "4", "25.06.2000", "", "", "1"],
            )

            self.assertEqual(summary["session_mode"], "build_with_optional_delivery")
            self.assertEqual(summary["build"]["report_scope"], "full")
            self.assertEqual(summary["delivery"], {"status": "skipped", "selection": "none"})

    def test_file_review_session_can_finish_with_report_only_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary, _stderr = self._run_session(
                self._build_args(temp_path, ["--input", "inputs/examples/student_example.yaml", "--review"]),
                ["", "2", "1", ""],
            )

            delivery = summary["delivery"]
            self.assertEqual(delivery["status"], "success")
            self.assertEqual(delivery["request"]["delivery_profile"], "report_only")
            self.assertEqual(delivery["request"]["report_scope"], "full")
            self.assertTrue(Path(delivery["result"]["delivery_manifest_path"]).exists())

    def test_delivery_review_edit_can_switch_to_guide_only_general(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary, _stderr = self._run_session(
                self._build_args(temp_path, ["--input", "inputs/examples/student_example.yaml", "--review"]),
                ["", "2", "1", "e", "4", "2", "2", "1", ""],
            )

            delivery = summary["delivery"]
            manifest = json.loads(Path(delivery["result"]["delivery_manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(delivery["request"]["delivery_profile"], "guide_only")
            self.assertEqual(delivery["request"]["guide_mode"], "general")
            self.assertEqual(delivery["request"]["guide_scope"], "task2")
            self.assertIn("guide/methodical_guide__general.pdf", manifest["artifacts"])
            self.assertNotIn("report/final_report.pdf", manifest["artifacts"])


    def test_unified_session_can_finish_with_study_pack_docx_choices(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary, stderr = self._run_session(
                self._build_args(temp_path, ["--input", "inputs/examples/student_example.yaml", "--review"]),
                ["", "3", "1", "3", "2", ""],
            )

            delivery = summary["delivery"]
            manifest = json.loads(Path(delivery["result"]["delivery_manifest_path"]).read_text(encoding="utf-8"))
            report_docx = Path(delivery["result"]["delivery_dir"]) / "report" / "final_report.docx"
            guide_pdf = Path(delivery["result"]["delivery_dir"]) / "guide" / "methodical_guide__variant.pdf"
            guide_docx = Path(delivery["result"]["delivery_dir"]) / "guide" / "methodical_guide__variant.docx"

            self.assertEqual(delivery["request"]["delivery_profile"], "study_pack")
            self.assertEqual(delivery["request"]["output_format"], "bundle_dir")
            self.assertEqual(delivery["request"]["report_output_format"], "pdf_docx")
            self.assertEqual(delivery["request"]["guide_output_format"], "docx")
            self.assertIn("report/final_report.pdf", manifest["artifacts"])
            self.assertIn("report/final_report.docx", manifest["artifacts"])
            self.assertIn("guide/methodical_guide__variant.docx", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__variant.pdf", manifest["artifacts"])
            self.assertGreater(report_docx.stat().st_size, 0)
            self.assertGreater(guide_docx.stat().st_size, 0)
            self.assertIn("В каком формате нужен отчёт внутри комплекта?", stderr)
            self.assertIn("В каком формате нужны материалы внутри комплекта?", stderr)

    def test_unified_session_can_finish_with_guide_only_general_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary, stderr = self._run_session(
                self._build_args(temp_path, ["--input", "inputs/examples/student_example.yaml", "--review"]),
                ["", "4", "2", "2", "1", ""],
            )

            delivery = summary["delivery"]
            manifest = json.loads(Path(delivery["result"]["delivery_manifest_path"]).read_text(encoding="utf-8"))
            pdf_path = Path(delivery["result"]["delivery_dir"]) / "guide" / "methodical_guide__general.pdf"
            self.assertEqual(delivery["request"]["delivery_profile"], "guide_only")
            self.assertEqual(delivery["request"]["guide_mode"], "general")
            self.assertEqual(delivery["request"]["output_format"], "pdf")
            self.assertIn("guide/methodical_guide__general.pdf", manifest["artifacts"])
            self.assertGreater(pdf_path.stat().st_size, 0)
            self.assertIn("Что вы хотите получить на выходе?", stderr)
            self.assertIn("Проверьте, что нужно создать:", stderr)
            self.assertIn("Действие [Enter=создать, e=изменить, x=отмена]:", stderr)
            self.assertIn("Готово.", stderr)
            self.assertIn("Что создано:", stderr)
            self.assertIn("Главный результат — откройте его первым:", stderr)
            self.assertIn("Если нужны детали:", stderr)
            self.assertNotIn("delivery_profile", stderr)
            self.assertNotIn("guide_mode", stderr)
            self.assertNotIn("guide_scope", stderr)
            self.assertNotIn("output_format", stderr)

    def test_invalid_choice_is_blocked_and_cancel_keeps_build_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary, stderr = self._run_session(
                self._build_args(temp_path, ["--input", str(self._task1_input(temp_path)), "--review"]),
                ["", "4", "1", "3", "1", "1", "x"],
            )

            self.assertEqual(summary["build"]["report_scope"], "task1")
            self.assertEqual(summary["delivery"]["status"], "cancelled")
            self.assertIn("Недопустимое значение для объёма материалов. Разрешено: Только задача 1.", stderr)
            deliveries_dir = temp_path / "deliveries"
            self.assertFalse(deliveries_dir.exists() and any(deliveries_dir.iterdir()))


if __name__ == "__main__":
    unittest.main()
