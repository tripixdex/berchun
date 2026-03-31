from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.build_pipeline import resolve_build_input
from src.cli import main
from src.input_schema import current_report_year


class BuildPipelineTests(unittest.TestCase):
    def _build_args(self, temp_path: Path, input_path: Path) -> list[str]:
        return [
            "build",
            "--input",
            str(input_path),
            "--runs-dir",
            str(temp_path / "runs"),
            "--variant-path",
            str(temp_path / "workspace" / "inputs" / "variant_me.yaml"),
            "--derived-path",
            str(temp_path / "workspace" / "inputs" / "derived_parameters.json"),
            "--out-dir",
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

    def _run_command(self, args: list[str]) -> dict[str, object]:
        if "--json" not in args:
            args = [*args, "--json"]
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(args)
        self.assertEqual(exit_code, 0)
        return json.loads(stdout.getvalue())

    def _run_build(self, temp_path: Path, input_path: Path, extra_args: list[str] | None = None) -> dict[str, object]:
        args = self._build_args(temp_path, input_path)
        if extra_args:
            args.extend(extra_args)
        return self._run_command(args)

    def _scoped_input(self, temp_path: Path, scope: str) -> Path:
        scoped_input = temp_path / f"student_{scope}.yaml"
        scoped_input.write_text(
            Path("inputs/examples/student_example.yaml").read_text(encoding="utf-8").replace(
                'report_scope: "full"', f'report_scope: "{scope}"'
            ),
            encoding="utf-8",
        )
        return scoped_input

    def test_build_requires_exactly_one_input_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolve_build_input(input_path=None, interactive=False)

    def test_cli_build_from_input_file_produces_full_run_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"))
            bundle = summary["bundle"]
            report_tex = Path(bundle["report_source_path"]).read_text(encoding="utf-8")

            self.assertEqual(summary["build_mode"], "fresh")
            self.assertEqual(summary["report_scope"], "full")
            self.assertEqual(summary["report"]["report_scope"], "full")
            self.assertEqual(summary["report"]["report_year"], current_report_year())
            self.assertEqual(summary["report"]["used_plot_count"], 27)
            self.assertTrue(Path(bundle["report_pdf_path"]).exists())
            self.assertIn("Задача №1. Проектирование Call-центра.", report_tex)
            self.assertIn("Задача №2. Проектирование производственного участка.", report_tex)

    def test_identical_input_reuses_existing_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            first = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"))
            second = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"))

            self.assertEqual(first["build_mode"], "fresh")
            self.assertEqual(second["build_mode"], "reused")
            self.assertEqual(first["run_id"], second["run_id"])
            self.assertEqual(first["raw_input_hash"], second["raw_input_hash"])
            registry = json.loads((temp_path / "runs" / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(len(registry["runs"]), 1)

    def test_changed_scope_creates_new_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            first = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"))
            second = self._run_build(temp_path, self._scoped_input(temp_path, "task1"))

            self.assertEqual(first["build_mode"], "fresh")
            self.assertEqual(second["build_mode"], "fresh")
            self.assertNotEqual(first["run_id"], second["run_id"])
            self.assertNotEqual(first["raw_input_hash"], second["raw_input_hash"])
            registry = json.loads((temp_path / "runs" / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(len(registry["runs"]), 2)

    def test_task1_build_produces_partial_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary = self._run_build(temp_path, self._scoped_input(temp_path, "task1"))
            report_tex = Path(summary["bundle"]["report_source_path"]).read_text(encoding="utf-8")

            self.assertEqual(summary["report_scope"], "task1")
            self.assertEqual(summary["report"]["used_plot_count"], 22)
            self.assertEqual(summary["report"]["scheme_count"], 4)
            self.assertIn("Задача №1. Проектирование Call-центра.", report_tex)
            self.assertNotIn("Задача №2. Проектирование производственного участка.", report_tex)
            self.assertNotIn("task2_1__", report_tex)

    def test_task2_build_produces_partial_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary = self._run_build(temp_path, self._scoped_input(temp_path, "task2"))
            report_tex = Path(summary["bundle"]["report_source_path"]).read_text(encoding="utf-8")

            self.assertEqual(summary["report_scope"], "task2")
            self.assertEqual(summary["report"]["used_plot_count"], 5)
            self.assertEqual(summary["report"]["scheme_count"], 1)
            self.assertNotIn("Задача №1. Проектирование Call-центра.", report_tex)
            self.assertIn("Задача №2. Проектирование производственного участка.", report_tex)
            self.assertNotIn("task1_1__", report_tex)

    def test_file_review_then_build_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, patch("builtins.input", side_effect=[""]):
            temp_path = Path(temp_dir)
            summary = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"), extra_args=["--review"])

            self.assertEqual(summary["build_mode"], "fresh")
            self.assertEqual(summary["report_scope"], "full")
            self.assertTrue(Path(summary["bundle"]["report_pdf_path"]).exists())
            self.assertGreater(Path(summary["bundle"]["report_pdf_path"]).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
