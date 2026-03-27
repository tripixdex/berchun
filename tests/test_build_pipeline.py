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

    def test_build_requires_exactly_one_input_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one"):
            resolve_build_input(input_path=None, interactive=False)

    def test_cli_build_from_input_file_produces_run_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            summary = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"))
            bundle = summary["bundle"]
            registry_path = Path(summary["registry_path"])
            run_metadata_path = Path(summary["run_metadata_path"])
            report_pdf_path = Path(bundle["report_pdf_path"])

            self.assertEqual(summary["build_mode"], "fresh")
            self.assertEqual(summary["report"]["report_year"], 2026)
            self.assertTrue(report_pdf_path.exists())
            self.assertGreater(report_pdf_path.stat().st_size, 0)
            self.assertTrue(run_metadata_path.exists())
            self.assertTrue(registry_path.exists())
            self.assertEqual(summary["solve"]["variant_path"], bundle["variant_path"])
            self.assertTrue(Path(summary["working_set"]["report_pdf_path"]).exists())

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

    def test_changed_input_creates_new_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            changed_input = temp_path / "student_changed.yaml"
            changed_input.write_text(
                Path("inputs/examples/student_example.yaml").read_text(encoding="utf-8").replace(
                    'student_full_name: "Иванов Иван Иванович"',
                    'student_full_name: "Петров Петр Петрович"',
                ),
                encoding="utf-8",
            )

            first = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"))
            second = self._run_build(temp_path, changed_input)

            self.assertEqual(first["build_mode"], "fresh")
            self.assertEqual(second["build_mode"], "fresh")
            self.assertNotEqual(first["run_id"], second["run_id"])
            self.assertNotEqual(first["raw_input_hash"], second["raw_input_hash"])
            self.assertTrue(Path(second["bundle"]["report_pdf_path"]).exists())
            registry = json.loads((temp_path / "runs" / "index.json").read_text(encoding="utf-8"))
            self.assertEqual([entry["status"] for entry in registry["runs"]], ["success", "success"])

    def test_file_review_then_build_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, patch("builtins.input", side_effect=["confirm"]):
            temp_path = Path(temp_dir)
            summary = self._run_build(temp_path, Path("inputs/examples/student_example.yaml"), extra_args=["--review"])

            self.assertEqual(summary["build_mode"], "fresh")
            self.assertEqual(summary["report"]["report_year"], 2026)
            self.assertTrue(Path(summary["bundle"]["report_pdf_path"]).exists())
            self.assertGreater(Path(summary["bundle"]["report_pdf_path"]).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
