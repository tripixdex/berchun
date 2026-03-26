from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.plots import generate_figure_artifacts


class PlotGenerationTests(unittest.TestCase):
    def test_generate_figure_artifacts_writes_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            figures_dir = temp_path / "figures"
            manifest_path = temp_path / "out" / "artifacts" / "figure_manifest.json"
            summary = generate_figure_artifacts(
                data_dir=Path("out/data"),
                figures_dir=figures_dir,
                manifest_path=manifest_path,
            )

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["generated_count"], manifest["meta"]["generated_count"])
            for filename in ["task_1_1.png", "task_1_2.png", "task_1_3.png", "task_1_4.png", "task_2_1.png"]:
                image_path = figures_dir / filename
                self.assertTrue(image_path.exists(), msg=str(image_path))
                self.assertGreater(image_path.stat().st_size, 0)

            generated = [item for item in manifest["artifacts"] if item["status"] == "generated"]
            self.assertTrue(generated)
            self.assertEqual(
                {source for item in generated for source in item["source_data_files"]},
                {
                    "out/data/task_1_1.json",
                    "out/data/task_1_2.json",
                    "out/data/task_1_3.json",
                    "out/data/task_1_4.json",
                    "out/data/task_2_1.json",
                },
            )


if __name__ == "__main__":
    unittest.main()
