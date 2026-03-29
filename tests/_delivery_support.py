from __future__ import annotations

import io
import json
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

    def build_args(self, paths: dict[str, Path]) -> list[str]:
        return [
            "build",
            "--input",
            "inputs/examples/student_example.yaml",
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

    def deliver_args(self, paths: dict[str, Path], run_id: str, *extra: str) -> list[str]:
        return [
            "deliver",
            "--runs-dir",
            str(paths["runs_dir"]),
            "--deliveries-dir",
            str(paths["deliveries_dir"]),
            "--source-run-id",
            run_id,
            "--guide-source-path",
            str(paths["guide_source_path"]),
            "--derived-path",
            str(paths["derived_path"]),
            "--data-dir",
            str(paths["out_dir"]),
            *extra,
        ]

    def write_mock_guide(self, path: Path) -> None:
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
                    "shared variant block",
                    "",
                    "## Как читать схемы, обозначения, формулы и графики",
                    "shared reading block",
                    "",
                    "## Задача 1. Проектирование колл-центра",
                    "### 1.1. Система без очереди",
                    "task1 body",
                    "",
                    "## Задача 2. Производственный участок",
                    "### 2.1. Метрики производственного участка по числу наладчиков",
                    "task2 body",
                    "",
                    "## Как использовать guide на защите",
                    "tail block",
                    "",
                ]
            ),
            encoding="utf-8",
        )
