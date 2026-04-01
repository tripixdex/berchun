from __future__ import annotations

from pathlib import Path
from typing import Callable

from src.compute.common import ensure_directory

INPUT_CHOOSER_SENTINEL = "__choose_input__"
_CANCEL_WORDS = {"cancel", "x", "no", "n", "нет", "н"}
_PREFERRED_INPUTS = (
    (Path("inputs/variant_me.yaml"), "текущий рабочий YAML"),
    (Path("inputs/examples/student_example.yaml"), "пример полного ввода"),
    (Path("inputs/examples/gurov.yaml"), "ещё один пример"),
)
STARTER_YAML_SENTINEL = "__choose_starter_yaml__"
STARTER_YAML_DEFAULT_PATH = Path("inputs/starter.yaml")
STARTER_YAML_TEMPLATE = """# Starter YAML for a new coursework input.
# Fill the fields below, save the file, and run `build --input <path>`.
student_full_name: "Иванов Иван Иванович"
student_group: "РК9-84Б"
teacher_full_name: "Берчун Юрий Валерьевич"
journal_number: 7
birth_date: "25.06.2000"
report_scope: "full"
report_year: 2026
"""

_VALIDATION_HINTS = (
    (
        "student_full_name must be non-empty",
        "ФИО студента пустое",
        "Укажи ФИО одной строкой, например `Иванов Иван Иванович`.",
    ),
    (
        "student_group must be non-empty",
        "Группа пустая",
        "Укажи группу одной строкой, например `РК9-84Б`.",
    ),
    (
        "teacher_full_name must be non-empty",
        "Поле преподавателя пустое",
        "Укажи ФИО преподавателя, например `Берчун Юрий Валерьевич`.",
    ),
    (
        "journal_number must be an integer",
        "Номер по журналу должен быть целым числом",
        "Например: `7`.",
    ),
    (
        "journal_number must be a positive integer",
        "Номер по журналу должен быть положительным целым числом",
        "Например: `7`.",
    ),
    (
        "birth_date must be a string in DD.MM.YYYY format",
        "Дата рождения должна быть строкой в формате ДД.ММ.ГГГГ",
        "Например: `25.06.2000`.",
    ),
    (
        "birth_date must match DD.MM.YYYY",
        "Дата рождения должна быть в формате ДД.ММ.ГГГГ",
        "Например: `25.06.2000`.",
    ),
    (
        "birth_date must be a valid date",
        "Дата рождения не является реальной календарной датой",
        "Проверь день и месяц, например `25.06.2000`.",
    ),
    (
        "birth_date is required",
        "Дата рождения не указана",
        "Укажи дату в формате `ДД.ММ.ГГГГ` или возьми starter YAML.",
    ),
    (
        "birth_date conflicts with birth_day/birth_month/birth_year",
        "Смешаны новый и старый форматы даты рождения",
        "Оставь только `birth_date` или только старые поля `birth_day/birth_month/birth_year`.",
    ),
    (
        "report_scope must be a string",
        "Состав отчёта должен быть текстом",
        "Используй одно из значений: `full`, `task1`, `task2`.",
    ),
    (
        "report_scope must be one of",
        "Состав отчёта указан неверно",
        "Используй `full`, `task1` или `task2`.",
    ),
    (
        "report_year must be within [2000, 2100]",
        "Год отчёта вне допустимого диапазона",
        "Используй год между 2000 и 2100 или возьми starter YAML.",
    ),
    (
        "Invalid YAML line",
        "Файл не похож на YAML с парами ключ: значение",
        "Проверь строку, отступы и двоеточия. Если нужно начать с образца, создай starter YAML.",
    ),
    (
        "Input document must be a mapping",
        "Файл должен содержать ключи и значения",
        "Используй формат `ключ: значение` или возьми starter YAML.",
    ),
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


def choose_starter_yaml_path(
    prompt: Callable[[str], str],
    display: Callable[[str], None],
    root: Path | None = None,
) -> Path:
    root = Path.cwd() if root is None else root
    while True:
        raw = prompt("Куда сохранить стартовый YAML [Enter=inputs/starter.yaml, x=отмена]: ").strip()
        if raw.lower() in _CANCEL_WORDS:
            raise ValueError("starter YAML creation cancelled by user")
        target = STARTER_YAML_DEFAULT_PATH if raw == "" else Path(raw)
        resolved = target if target.is_absolute() else root / target
        if resolved.exists():
            display(f"Файл уже существует: {target}. Укажите новый путь.")
            continue
        return target


def write_starter_yaml(path: Path) -> Path:
    if path.exists():
        raise ValueError(f"starter YAML already exists: {path}")
    ensure_directory(path.parent)
    path.write_text(STARTER_YAML_TEMPLATE, encoding="utf-8")
    return path


def format_input_validation_error(error: Exception) -> str | None:
    message = str(error)
    for needle, title, hint in _VALIDATION_HINTS:
        if needle in message:
            return "\n".join(
                [
                    "Не удалось принять YAML-ввод.",
                    f"Проблема: {title}.",
                    f"Что сделать: {hint}",
                    "Дальше: нажмите Enter, чтобы попробовать снова; при необходимости можно выбрать другой YAML или starter YAML.",
                    "Подсказка: `python3 -m src.cli build --starter-yaml inputs/my_input.yaml` создаёт стартовый шаблон.",
                ]
            )
    return None


def prompt_build_input_recovery_action(
    prompt: Callable[[str], str],
    display: Callable[[str], None],
    allow_choose_yaml: bool,
) -> str:
    message = (
        "Что дальше [Enter=повторить, e=другой YAML, s=starter YAML, x=отмена]: "
        if allow_choose_yaml
        else "Что дальше [Enter=повторить, s=starter YAML, x=отмена]: "
    )
    while True:
        raw = prompt(message).strip().lower()
        if raw in {"", "retry", "r", "repeat", "повторить", "п"}:
            return "retry"
        if allow_choose_yaml and raw in {"e", "edit", "choose", "другой yaml", "yaml", "y"}:
            return "choose_yaml"
        if raw in {"s", "starter", "template", "шаблон"}:
            return "starter"
        if raw in {"x", "cancel", "c", "отмена", "н"}:
            return "cancel"
        display("Нажмите Enter, e, s или x." if allow_choose_yaml else "Нажмите Enter, s или x.")


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
