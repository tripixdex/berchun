from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


class DeliverySafetyTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_general_guide_delivery_inserts_regime_notes_for_sensitive_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            general_source = paths["guide_general_source_path"]
            general_source.parent.mkdir(parents=True, exist_ok=True)
            general_source.write_text(
                "\n".join(
                    [
                        "# Methodical Guide",
                        "",
                        "## Что это за guide и чем он отличается от formal report",
                        "intro",
                        "",
                        "## Задача 1. Проектирование колл-центра",
                        "### 1.3. Система с неограниченной очередью",
                        "task13 body",
                        "",
                        "### 1.4. Система с неограниченной очередью и уходом клиентов",
                        "task14 body",
                        "",
                        "## Задача 2. Производственный участок",
                        "### 2.1. Метрики производственного участка по числу наладчиков",
                        "task21 body",
                        "",
                        "## Как использовать guide на защите",
                        "tail",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(
                    paths,
                    None,
                    "--delivery-profile",
                    "guide_only",
                    "--output-format",
                    "md",
                    "--guide-mode",
                    "general",
                    "--guide-scope",
                    "full",
                )
            )

            text = (Path(summary["delivery_dir"]) / "guide" / "methodical_guide__general.md").read_text(encoding="utf-8")
            self.assertIn("## Режимные оговорки delivery", text)
            self.assertIn("первая стационарная точка не считается универсальным числом", text)
            self.assertIn("Численные truncation bounds и цена ухода клиентов", text)
            self.assertIn("`P_ож` трактуется только как вероятность ожидания нового отказа", text)
            self.assertLess(text.index("## Режимные оговорки delivery"), text.index("## Как использовать guide на защите"))

    def test_variant_aware_delivery_rejects_sensitive_artifact_drift(self) -> None:
        cases = [
            ("task1", self._break_task_1_3, "non-stationary points with metric values"),
            ("task1", self._break_task_1_4, "truncation"),
            ("task2", self._break_task_2_1, "waiting_probability_interpretation"),
        ]
        for guide_scope, mutator, needle in cases:
            with self.subTest(guide_scope=guide_scope, needle=needle), tempfile.TemporaryDirectory() as temp_dir:
                paths = self.workspace_paths(Path(temp_dir))
                self.write_mock_guide(paths["guide_source_path"])
                build = self.run_success(self.build_args(paths))
                self._mutate_workspace_and_run_bundle(paths, build["bundle"]["out_dir"], mutator)
                error = self.run_failure(
                    self.deliver_args(
                        paths,
                        build["run_id"],
                        "--delivery-profile",
                        "guide_only",
                        "--output-format",
                        "md",
                        "--guide-mode",
                        "variant_aware",
                        "--guide-scope",
                        guide_scope,
                    )
                )
                self.assertIn(needle, error)

    def test_variant_aware_full_guide_rejects_partial_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            paths = self.workspace_paths(temp_path)
            self.write_mock_guide(paths["guide_source_path"])
            build = self.run_success(self.build_args(paths, self.write_input_file(temp_path, "task1")))
            error = self.run_failure(
                self.deliver_args(
                    paths,
                    build["run_id"],
                    "--delivery-profile",
                    "guide_only",
                    "--output-format",
                    "md",
                    "--guide-mode",
                    "variant_aware",
                    "--guide-scope",
                    "full",
                )
            )
            self.assertIn("guide_only/full requires a source run built with report_scope='full'", error)

    def _mutate_workspace_and_run_bundle(self, paths: dict[str, Path], bundle_out_dir: str, mutator) -> None:
        targets = [paths["out_dir"], Path(bundle_out_dir)]
        for base in targets:
            mutator(base)

    def _break_task_1_3(self, out_dir: Path) -> None:
        path = out_dir / "task_1_3.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["sweeps"][0]["points"][0]["metrics"]["busy_operators_expected"] = 0.0
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _break_task_1_4(self, out_dir: Path) -> None:
        path = out_dir / "task_1_4.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["metadata"].pop("truncation_policy", None)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _break_task_2_1(self, out_dir: Path) -> None:
        path = out_dir / "task_2_1.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        for point in payload["sweeps"][0]["points"]:
            point["diagnostics"]["waiting_probability_interpretation"] = "queue_state_share"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
