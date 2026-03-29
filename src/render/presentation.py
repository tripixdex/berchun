from __future__ import annotations

from src.render.common import latex_escape

DISPLAY_DIGITS = 3
DISPLAY_THRESHOLD = 10 ** -DISPLAY_DIGITS


def format_teacher_number(value: float | int) -> str:
    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    if 0 < abs(numeric) < DISPLAY_THRESHOLD:
        return f"< {DISPLAY_THRESHOLD:.{DISPLAY_DIGITS}f}"
    rendered = f"{numeric:.{DISPLAY_DIGITS}f}".rstrip("0").rstrip(".")
    return "0" if rendered == "-0" else rendered


def format_scientific(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}e}"


def labeled_lines_block(title: str, items: list[str]) -> str:
    body = "\n".join(f"\\noindent {latex_escape(item)}\\par" for item in items)
    return (
        f"\\noindent\\textbf{{{latex_escape(title)}}}\\par\n"
        "\\smallskip\n"
        f"{body}\n\n"
    )
