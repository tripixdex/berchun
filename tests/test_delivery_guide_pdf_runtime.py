from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import re
import unicodedata

from src.delivery_guide_pdf_surface import build_pdf_surface_markdown
from tests._delivery_support import DeliveryCliTestMixin


class DeliveryGuidePdfRuntimeTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_variant_guide_source_contains_key_formula_blocks(self) -> None:
        guide_text = Path("docs/METHODICAL_GUIDE.md").read_text(encoding="utf-8")
        for fragment in (
            r"p_0 = \left(\sum_{k=0}^{n}\frac{a^k}{k!}\right)^{-1}",
            r"P_{\mathrm{отк}} = p_n",
            r"p_{n+r} = \frac{a^n}{n!}\rho_n^{\,r}p_0",
            r"P_{\mathrm{wait}} = \frac{a^n}{n!(1-\rho_n)}p_0",
            r"\delta_k = \min(k,n)\mu + \max(k-n,0)\nu",
            r"P_{\mathrm{ож}} = \frac{\sum_{i=r}^{N-1}(N-i)p_i}{\sum_{i=0}^{N-1}(N-i)p_i}",
        ):
            self.assertIn(fragment, guide_text)

    def test_pdf_surface_markdown_uses_inline_figures_with_keep_together_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            guide_dir = Path(temp_dir) / "guide"
            (guide_dir / "assets" / "schemes").mkdir(parents=True, exist_ok=True)
            (guide_dir / "assets" / "plots").mkdir(parents=True, exist_ok=True)
            (guide_dir / "assets" / "schemes" / "task1_1__scheme.png").write_bytes(b"png")
            (guide_dir / "assets" / "plots" / "task1_1__refusal_and_utilization_vs_operators.png").write_bytes(b"png")
            guide_text = "\n".join(
                [
                    "# Methodical Guide",
                    "",
                    "## Задача 1. Проектирование колл-центра",
                    "",
                    "### 1.1. Система без очереди",
                    "",
                    "#### Схема и состояния",
                    "",
                    "#### Как читать совмещённый график отказа и загрузки",
                    "",
                ]
            )

            pdf_surface = build_pdf_surface_markdown(guide_text=guide_text, guide_dir=guide_dir)
            scheme_path = (guide_dir / "assets" / "schemes" / "task1_1__scheme.png").resolve().as_posix()
            plot_path = (guide_dir / "assets" / "plots" / "task1_1__refusal_and_utilization_vs_operators.png").resolve().as_posix()

            self.assertIn("\\clearpage", pdf_surface)
            self.assertIn(
                f"\\includegraphics[width=0.76\\textwidth]{{{scheme_path}}}",
                pdf_surface,
            )
            self.assertIn(
                f"\\includegraphics[width=0.86\\textwidth]{{{plot_path}}}",
                pdf_surface,
            )
            self.assertIn(
                "\\parbox{0.86\\textwidth}{\\centering\\emph{Опорный график 1.1: отказ и загрузка при изменении числа операторов.}}",
                pdf_surface,
            )

    def test_guide_only_variant_pdf_delivery_produces_non_empty_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            paths["guide_source_path"].parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2("docs/METHODICAL_GUIDE.md", paths["guide_source_path"])
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
                    "full",
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
                "Если нужно быстро сориентироваться, идите так:",
                "λ = 1/Tc = 0.071",
                "P_отк",
                "p0 =",
                "Pотк = pn",
                "Pоч = ∑ pk",
                "Pwait =",
                "Pож =",
                "Mпр = ∑ i pi",
                "M_зан",
                "K_загр",
                "ρ_n < 1",
                "δ_k",
                "Схема подпункта 1.1.",
                "Опорный график 1.1: отказ и загрузка при изменении числа операторов.",
                "Схема подпункта 2.1.",
                "Опорный график 2.1: вероятность ожидания обслуживания при увеличении числа наладчиков.",
            )
            self.assert_pdf_embeds_images(pdf_path, minimum_images=10)

    def test_guide_only_general_pdf_delivery_produces_non_empty_pdf_without_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            paths["guide_general_source_path"].parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2("docs/METHODICAL_GUIDE_GENERAL_SOURCE.md", paths["guide_general_source_path"])
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
            self.assert_pdf_text_contains(
                pdf_path,
                "λ",
                "μ",
                "P_отк",
                "M_зан",
                "K_загр",
                "ρ_n",
                "Схема подпункта 1.1.",
                "Схема подпункта 2.1.",
            )
            self.assert_pdf_text_does_not_contain(pdf_path, "Опорный график 1.1", "guide/assets/plots")
            self.assert_pdf_embeds_images(pdf_path, minimum_images=5)

    def assert_pdf_text_contains(self, pdf_path: Path, *needles: str) -> None:
        if shutil.which("pdftotext") is None:
            self.skipTest("pdftotext is required for guide PDF text validation")
        result = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
        normalized = self._normalize_pdf_text(result.stdout)
        for needle in needles:
            self.assertIn(self._normalize_pdf_text(needle), normalized)

    def assert_pdf_text_does_not_contain(self, pdf_path: Path, *needles: str) -> None:
        if shutil.which("pdftotext") is None:
            self.skipTest("pdftotext is required for guide PDF text validation")
        result = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
        normalized = self._normalize_pdf_text(result.stdout)
        for needle in needles:
            self.assertNotIn(self._normalize_pdf_text(needle), normalized)

    def assert_pdf_embeds_images(self, pdf_path: Path, *, minimum_images: int) -> None:
        if shutil.which("pdfimages") is None:
            self.skipTest("pdfimages is required for guide PDF image validation")
        result = subprocess.run(["pdfimages", "-list", str(pdf_path)], capture_output=True, text=True, check=True)
        image_rows = 0
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[2] == "image":
                image_rows += 1
        self.assertGreaterEqual(image_rows, minimum_images)

    def _normalize_pdf_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


if __name__ == "__main__":
    unittest.main()
