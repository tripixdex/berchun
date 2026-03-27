from __future__ import annotations

from typing import Any

from src.render.common import latex_escape

TITLE_METADATA = {"student_full_name": "Гуров Владислав Александрович", "student_group": "РК9-84Б", "teacher_full_name": "Берчун Юрий Валерьевич"}
TITLE_REFERENCE = {"institution": "Министерство науки и высшего образования Российской Федерации\\\\Федеральное государственное автономное образовательное учреждение высшего образования\\\\«Московский государственный технический университет имени Н.Э. Баумана\\\\(национальный исследовательский университет)»\\\\(МГТУ им. Н.Э. Баумана)", "faculty": "ФАКУЛЬТЕТ «РОБОТОТЕХНИКА И КОМПЛЕКСНАЯ АВТОМАТИЗАЦИЯ»", "department": "КАФЕДРА РК-9 «КОМПЬЮТЕРНЫЕ СИСТЕМЫ АВТОМАТИЗАЦИИ ПРОИЗВОДСТВА»", "course": "Имитационное моделирование технологических производственных процессов"}


def _title_value(raw_inputs: dict[str, Any], key: str, default: Any | None = None) -> Any:
    value = raw_inputs.get(key, default)
    return value["value"] if isinstance(value, dict) else value


def title_page(raw_inputs: dict[str, Any], report_year: int) -> str:
    student = latex_escape(str(_title_value(raw_inputs, "student_full_name", TITLE_METADATA["student_full_name"])))
    group = latex_escape(str(_title_value(raw_inputs, "student_group", TITLE_METADATA["student_group"])))
    teacher = latex_escape(str(_title_value(raw_inputs, "teacher_full_name", TITLE_METADATA["teacher_full_name"])))
    return f"""
\\begin{{titlepage}}
\\thispagestyle{{empty}}
\\noindent
\\begin{{minipage}}[t]{{0.17\\textwidth}}
\\vspace{{0pt}}
\\centering
{{\\setlength{{\\fboxsep}}{{5pt}}\\fbox{{\\parbox[c][24mm][c]{{20mm}}{{\\centering\\bfseries МГТУ\\\\[-1pt] \\scriptsize РК-9}}}}}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.78\\textwidth}}
\\vspace{{0pt}}
\\begin{{center}}
{{\\small {TITLE_REFERENCE['institution']}}}
\\end{{center}}
\\end{{minipage}}

\\vspace{{0.45cm}}
\\noindent\\rule{{\\textwidth}}{{1.2pt}}

\\vspace{{0.8cm}}
\\begin{{center}}
{{\\bfseries {TITLE_REFERENCE['faculty']}}}\\\\[0.35cm]
{{\\bfseries {TITLE_REFERENCE['department']}}}
\\end{{center}}

\\vspace{{1.8cm}}
\\begin{{center}}
{{\\large\\bfseries Домашнее задание №1}}\\\\[0.2cm]
{{\\normalsize по курсу}}\\\\[0.2cm]
{{\\large\\bfseries «{TITLE_REFERENCE['course']}»}}
\\end{{center}}

\\vfill
\\begin{{flushright}}
\\begin{{tabular}}{{@{{}}p{{3.6cm}}p{{8.4cm}}@{{}}}}
Студент: & {student}\\\\[0.15cm]
Группа: & {group}\\\\[0.15cm]
Преподаватель: & {teacher}
\\end{{tabular}}
\\end{{flushright}}

\\vfill
\\begin{{center}}
{report_year} г.
\\end{{center}}
\\end{{titlepage}}
"""
