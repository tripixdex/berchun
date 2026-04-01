from __future__ import annotations

from typing import Callable

_CANCEL_WORDS = {"x", "cancel", "c", "нет", "н"}

_OPERATOR_MENU = (
    ("interactive_delivery", "Интерактивная сборка + выбор итоговых артефактов"),
    ("yaml_delivery", "Выбрать YAML в CLI + review + выбор итоговых артефактов"),
    ("starter_yaml", "Создать starter YAML"),
)


def resolve_operator_start_args(
    prompt: Callable[[str], str],
    display: Callable[[str], None],
) -> list[str]:
    while True:
        display("Как запустить работу?")
        for index, (_key, label) in enumerate(_OPERATOR_MENU, start=1):
            display(f"{index}. {label}")

        raw = prompt("Выбор [Enter=1, 1-3, x=отмена]: ").strip().lower()

        if raw in _CANCEL_WORDS:
            raise ValueError("operator session cancelled by user")
        if raw in {"", "1"}:
            return ["build", "--interactive", "--offer-delivery"]
        if raw == "2":
            return ["build", "--input", "--review", "--offer-delivery"]
        if raw == "3":
            return ["build", "--starter-yaml"]

        display("Нажмите Enter, 1, 2, 3 или x.")
