from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin


class DeliveryGuidePdfRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_guide_only_variant_pdf_delivery_produces_non_empty_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_symbol_variant_guide(paths["guide_source_path"])
            build = self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(
                    paths,
                    build["run_id"],
                    "--delivery-profile",
                    "guide_only",
                    "--output-format",
                    "pdf",
                    "--guide-mode",
                    "variant_aware",
                    "--guide-scope",
                    "task1",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            pdf_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__variant.pdf"
            self.assertEqual(summary["assembly_state"], "populated")
            self.assertIn("guide/methodical_guide__variant.pdf", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__variant.md", manifest["artifacts"])
            self.assertGreater(pdf_path.stat().st_size, 0)
            self.assert_pdf_text_contains(
                pdf_path,
                "λ = 1 / Tc = 0.0714",
                "P_отк",
                "M_зан",
                "K_загр",
                "ρ_n < 1",
                "δ_k",
            )

    def test_guide_only_general_pdf_delivery_produces_non_empty_pdf_without_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            self.write_symbol_general_guide(paths["guide_general_source_path"])
            self.run_success(self.build_args(paths))
            summary = self.run_success(
                self.deliver_args(
                    paths,
                    None,
                    "--delivery-profile",
                    "guide_only",
                    "--output-format",
                    "pdf",
                    "--guide-mode",
                    "general",
                    "--guide-scope",
                    "full",
                )
            )

            manifest = self.assert_manifest_artifacts_exist(summary)
            pdf_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__general.pdf"
            self.assertEqual(manifest["source_kind"], "general_baseline")
            self.assertEqual(manifest["guide_source_kind"], "general_baseline")
            self.assertIn("guide/methodical_guide__general.pdf", manifest["artifacts"])
            self.assertNotIn("guide/methodical_guide__general.md", manifest["artifacts"])
            self.assertGreater(pdf_path.stat().st_size, 0)
            self.assert_pdf_text_contains(pdf_path, "λ", "μ", "P_отк", "M_зан", "K_загр", "ρ_n")

    def assert_pdf_text_contains(self, pdf_path: Path, *needles: str) -> None:
        if shutil.which("pdftotext") is None:
            self.skipTest("pdftotext is required for guide PDF text validation")
        result = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
        for needle in needles:
            self.assertIn(needle, result.stdout)

    def write_symbol_variant_guide(self, path: Path) -> None:
        self._write_guide(
            path,
            "`λ = 1 / Tc = 0.0714`, `μ = 1 / Ts = 0.0154`, `ν = 1 / Tw = 0.00943`",
            "`P_отк = p_n`, `M_зан`, `K_загр`, `ρ_n < 1`, `δ_k = min(k, n) μ + max(k - n, 0) ν`",
            "`P_ож`, `M_зан`, `K_загр`",
            "tail block",
        )

    def write_symbol_general_guide(self, path: Path) -> None:
        self._write_guide(
            path,
            "`λ`, `μ`, `ν`",
            "`P_отк`, `M_зан`, `K_загр`, `ρ_n`",
            "`P_ож`, `M_зан`, `K_загр`",
            "general tail block",
        )


if __name__ == "__main__":
    unittest.main()
