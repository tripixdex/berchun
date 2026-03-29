from __future__ import annotations

import json
from pathlib import Path

from src.report_scope import normalize_report_scope

TASK_PREFIXES = {
    "task1": ("task1_1__", "task1_2__", "task1_3__", "task1_4__"),
    "task2": ("task2_1__",),
    "full": ("task1_1__", "task1_2__", "task1_3__", "task1_4__", "task2_1__"),
}
TASK_HEADINGS = {
    "task1": "## Задача 1.",
    "task2": "## Задача 2.",
    "tail": "## Как использовать guide на защите",
}


def scope_prefixes(scope: str) -> tuple[str, ...]:
    return TASK_PREFIXES[normalize_report_scope(scope)]


def filter_guide_text(markdown: str, guide_scope: str) -> str:
    scope = normalize_report_scope(guide_scope)
    if scope == "full":
        return markdown if markdown.endswith("\n") else f"{markdown}\n"
    lines = markdown.splitlines()
    task1_idx = _find_heading(lines, TASK_HEADINGS["task1"])
    task2_idx = _find_heading(lines, TASK_HEADINGS["task2"])
    tail_idx = _find_heading(lines, TASK_HEADINGS["tail"])
    shared = lines[:task1_idx]
    task1_block = lines[task1_idx:task2_idx]
    task2_block = lines[task2_idx:tail_idx]
    tail = lines[tail_idx:]
    selected = task1_block if scope == "task1" else task2_block
    return "\n".join(shared + selected + tail).rstrip() + "\n"


def select_scheme_paths(assets_manifest_path: Path, scope: str) -> list[Path]:
    manifest = _load_manifest(assets_manifest_path)
    return _select_paths(
        entries=manifest.get("additional_artifacts_used", []),
        key_name="asset_id",
        path_name="path",
        prefixes=scope_prefixes(scope),
    )


def select_plot_paths(figure_manifest_path: Path, scope: str) -> list[Path]:
    manifest = _load_manifest(figure_manifest_path)
    eligible = [item for item in manifest.get("artifacts", []) if item.get("kind") == "plot" and item.get("status") == "generated"]
    return _select_paths(
        entries=eligible,
        key_name="figure_id",
        path_name="output_image_path",
        prefixes=scope_prefixes(scope),
    )


def select_report_asset_paths(assets_manifest_path: Path, scope: str) -> list[Path]:
    manifest = _load_manifest(assets_manifest_path)
    schemes = _select_paths(
        entries=manifest.get("additional_artifacts_used", []),
        key_name="asset_id",
        path_name="path",
        prefixes=scope_prefixes(scope),
    )
    titles = _collect_paths(manifest.get("title_assets_used", []), "output_image_path")
    return _dedupe_paths([*titles, *schemes])


def select_report_figure_paths(assets_manifest_path: Path, scope: str) -> list[Path]:
    prefixes = scope_prefixes(scope)
    manifest = _load_manifest(assets_manifest_path)
    paths = [Path(path) for path in manifest.get("figure_inputs_used", []) if isinstance(path, str)]
    return [path for path in paths if path.name.startswith(prefixes)]


def _load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_heading(lines: list[str], prefix: str) -> int:
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return index
    raise ValueError(f"guide baseline is missing heading {prefix!r}")


def _select_paths(entries: list[dict[str, object]], key_name: str, path_name: str, prefixes: tuple[str, ...]) -> list[Path]:
    selected: list[Path] = []
    for entry in entries:
        key = entry.get(key_name)
        path_value = entry.get(path_name)
        if not isinstance(key, str) or not isinstance(path_value, str):
            continue
        if key.startswith(prefixes):
            selected.append(Path(path_value))
    return selected


def _collect_paths(entries: list[dict[str, object]], path_name: str) -> list[Path]:
    selected: list[Path] = []
    for entry in entries:
        path_value = entry.get(path_name)
        if isinstance(path_value, str):
            selected.append(Path(path_value))
    return selected


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique
