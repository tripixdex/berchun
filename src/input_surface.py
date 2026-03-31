from __future__ import annotations

from pathlib import Path
from typing import Callable

INPUT_CHOOSER_SENTINEL = "__choose_input__"
_CANCEL_WORDS = {"cancel", "x", "no", "n", "нет", "н"}
_PREFERRED_INPUTS = (
    (Path("inputs/variant_me.yaml"), "текущий рабочий YAML"),
    (Path("inputs/examples/student_example.yaml"), "пример полного ввода"),
    (Path("inputs/examples/gurov.yaml"), "ещё один пример"),
)


def discover_input_candidates(root: Path | None = None) -> list[Path]:
    root = Path.cwd() if root is None else root
    candidates: list[Path] = []
    seen: set[str] = set()

    def add(path: Path) -> None:
        resolved = path if path.is_absolute() else root / path
        if not resolved.exists():
            return
        key = str(resolved.resolve())
        if key in seen:
            return
        seen.add(key)
        candidates.append(path if path.is_absolute() else resolved.relative_to(root))

    for preferred, _note in _PREFERRED_INPUTS:
        add(preferred)
    inputs_dir = root / "inputs"
    if inputs_dir.exists():
        for pattern in ("*.yaml", "*.yml"):
            for candidate in sorted(inputs_dir.rglob(pattern)):
                add(candidate.relative_to(root))
    return candidates


def _candidate_note(path: Path) -> str:
    notes = {preferred: note for preferred, note in _PREFERRED_INPUTS}
    return notes.get(path, "найденный YAML")


def _prompt_custom_input_path(prompt: Callable[[str], str], display: Callable[[str], None]) -> Path:
    while True:
        raw = prompt("Путь к YAML (например: inputs/examples/student_example.yaml, x=отмена): ").strip()
        if raw.lower() in _CANCEL_WORDS:
            raise ValueError("build cancelled by user")
        if raw:
            candidate = Path(raw)
            if candidate.exists():
                return candidate
            display("Файл не найден. Укажите существующий YAML-файл.")


def choose_input_path(
    prompt: Callable[[str], str],
    display: Callable[[str], None],
    root: Path | None = None,
) -> Path:
    candidates = discover_input_candidates(root)
    if not candidates:
        display("Готового списка YAML не найдено. Укажите путь вручную.")
        return _prompt_custom_input_path(prompt, display)

    display("Найденные YAML-файлы:")
    for index, candidate in enumerate(candidates, start=1):
        display(f"{index}. {candidate} — {_candidate_note(candidate)}")
    custom_index = len(candidates) + 1
    display(f"{custom_index}. Ввести путь вручную")
    while True:
        raw = prompt(f"Выберите YAML [Enter=1, 1-{custom_index}, x=отмена]: ").strip()
        if raw.lower() in _CANCEL_WORDS:
            raise ValueError("build cancelled by user")
        if raw == "":
            return candidates[0]
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(candidates):
                return candidates[choice - 1]
            if choice == custom_index:
                return _prompt_custom_input_path(prompt, display)
        candidate = Path(raw)
        if candidate.exists():
            return candidate
        display("Неизвестный выбор. Выберите номер, нажмите Enter для первого YAML или укажите путь вручную.")
