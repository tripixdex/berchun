from __future__ import annotations

import io
import json
import shutil
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from src.cli import main


class DeliveryCliTestMixin:
    def workspace_paths(self, temp_path: Path) -> dict[str, Path]:
        return {
            "runs_dir": temp_path / "runs",
            "deliveries_dir": temp_path / "deliveries",
            "variant_path": temp_path / "workspace" / "inputs" / "variant_me.yaml",
            "derived_path": temp_path / "workspace" / "inputs" / "derived_parameters.json",
            "out_dir": temp_path / "workspace" / "out" / "data",
            "figures_dir": temp_path / "workspace" / "figures",
            "manifest_path": temp_path / "workspace" / "out" / "artifacts" / "figure_manifest.json",
            "report_source_path": temp_path / "workspace" / "report" / "final_report.tex",
            "report_pdf_path": temp_path / "workspace" / "report" / "final_report.pdf",
            "report_assets_manifest_path": temp_path / "workspace" / "report" / "assets_manifest.json",
            "guide_source_path": temp_path / "workspace" / "docs" / "METHODICAL_GUIDE.md",
            "guide_general_source_path": temp_path / "workspace" / "docs" / "METHODICAL_GUIDE_GENERAL_SOURCE.md",
        }

    def run_success(self, args: list[str]) -> dict[str, object]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(args)
        self.assertEqual(exit_code, 0, stderr.getvalue())
        return json.loads(stdout.getvalue())

    def run_failure(self, args: list[str]) -> str:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr), self.assertRaises(SystemExit) as ctx:
            main(args)
        self.assertEqual(ctx.exception.code, 2)
        return stderr.getvalue()

    def build_args(self, paths: dict[str, Path], input_path: Path | None = None) -> list[str]:
        return [
            "build",
            "--input",
            str(input_path or Path("inputs/examples/student_example.yaml")),
            "--runs-dir",
            str(paths["runs_dir"]),
            "--variant-path",
            str(paths["variant_path"]),
            "--derived-path",
            str(paths["derived_path"]),
            "--out-dir",
            str(paths["out_dir"]),
            "--data-dir",
            str(paths["out_dir"]),
            "--figures-dir",
            str(paths["figures_dir"]),
            "--manifest-path",
            str(paths["manifest_path"]),
            "--report-source-path",
            str(paths["report_source_path"]),
            "--report-pdf-path",
            str(paths["report_pdf_path"]),
            "--report-assets-manifest-path",
            str(paths["report_assets_manifest_path"]),
        ]

    def deliver_args(self, paths: dict[str, Path], run_id: str | None = None, *extra: str) -> list[str]:
        args = [
            "deliver",
            "--runs-dir",
            str(paths["runs_dir"]),
            "--deliveries-dir",
            str(paths["deliveries_dir"]),
        ]
        if run_id is not None:
            args.extend(["--source-run-id", run_id])
        return [
            *args,
            "--guide-source-path",
            str(paths["guide_source_path"]),
            "--guide-general-source-path",
            str(paths["guide_general_source_path"]),
            "--derived-path",
            str(paths["derived_path"]),
            "--data-dir",
            str(paths["out_dir"]),
            "--report-assets-manifest-path",
            str(paths["report_assets_manifest_path"]),
            *extra,
        ]

    def write_input_file(self, temp_path: Path, report_scope: str) -> Path:
        input_path = temp_path / f"student_{report_scope}.yaml"
        shutil.copy2("inputs/examples/student_example.yaml", input_path)
        input_path.write_text(input_path.read_text(encoding="utf-8").replace('report_scope: "full"', f'report_scope: "{report_scope}"'), encoding="utf-8")
        return input_path

    def write_mock_guide(self, path: Path) -> None:
        self._write_guide(path, "shared variant block", "task1 body", "task2 body", "tail block")

    def write_mock_general_guide(self, path: Path) -> None:
        self._write_guide(path, "no student-specific numbers here", "general task1 body", "general task2 body", "general tail block")

    def _write_guide(self, path: Path, variant_block: str, task1_body: str, task2_body: str, tail_block: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(
                [
                    "# Methodical Guide",
                    "",
                    "## Что это за guide и чем он отличается от formal report",
                    "shared intro",
                    "",
                    "## Мой вариант и откуда взялись числа",
                    variant_block,
                    "",
                    "## Как читать схемы, обозначения, формулы и графики",
                    "shared reading block",
                    "",
                    "## Задача 1. Проектирование колл-центра",
                    "### 1.1. Система без очереди",
                    task1_body,
                    "",
                    "## Задача 2. Производственный участок",
                    "### 2.1. Метрики производственного участка по числу наладчиков",
                    task2_body,
                    "",
                    "## Как использовать guide на защите",
                    tail_block,
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def assert_manifest_artifacts_exist(self, summary: dict[str, object]) -> dict[str, object]:
        manifest = json.loads(Path(summary["delivery_manifest_path"]).read_text(encoding="utf-8"))
        delivery_dir = Path(summary["delivery_dir"])
        for relative_path in manifest["artifacts"]:
            self.assertTrue((delivery_dir / relative_path).exists(), relative_path)
        return manifest
