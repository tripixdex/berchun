from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests._delivery_support import DeliveryCliTestMixin

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


class PdfSurfaceIntegrityTests(DeliveryCliTestMixin, unittest.TestCase):
    def test_report_pdf_has_outline_and_useoutlines_page_mode(self) -> None:
        self._require_pypdf()
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = self.workspace_paths(Path(temp_dir))
            summary = self.run_success(self.build_args(paths))
            pdf_path = Path(summary["bundle"]["report_pdf_path"])

            page_mode, titles = self._navigation_snapshot(pdf_path)
            self.assertEqual(page_mode, "/UseOutlines")
            self.assertIn("Титульный лист", titles)
            self.assertIn("Задача №1. Проектирование Call-центра.", titles)
            self.assertIn("1.1 Система без очереди", titles)
            self.assertIn("2.1 Метрики производственного участка по числу наладчиков", titles)

    def test_guide_pdf_has_separate_support_blocks_and_outline_page_mode(self) -> None:
        self._require_pypdf()
        if shutil.which("pdftotext") is None:
            self.skipTest("pdftotext is required for guide PDF surface validation")
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
            pdf_path = Path(summary["delivery_dir"]) / "guide" / "methodical_guide__variant.pdf"

            page_mode, titles = self._navigation_snapshot(pdf_path)
            self.assertEqual(page_mode, "/UseOutlines")
            self.assertGreaterEqual(len(titles), 10)

            text = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True).stdout
            self.assertNotIn("Числовой checkpoint По итоговым", text)
            self.assertNotIn("Локальный вывод Для моего варианта", text)
            self.assertNotIn("Что это значит простыми словами Поток звонков", text)

    def _require_pypdf(self) -> None:
        if PdfReader is None:
            self.skipTest("pypdf is required for PDF outline validation")

    def _navigation_snapshot(self, pdf_path: Path) -> tuple[str | None, list[str]]:
        reader = PdfReader(str(pdf_path))
        root = reader.trailer["/Root"]
        return root.get("/PageMode"), self._outline_titles(reader.outline)

    def _outline_titles(self, outline: list[object]) -> list[str]:
        titles: list[str] = []
        for item in outline:
            if isinstance(item, list):
                titles.extend(self._outline_titles(item))
                continue
            title = getattr(item, "title", None)
            if title:
                titles.append(title)
        return titles


if __name__ == "__main__":
    unittest.main()
