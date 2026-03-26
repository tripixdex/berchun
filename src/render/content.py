from __future__ import annotations

from datetime import date
from typing import Any

from src.render.common import format_float


def plot_caption(figure_id: str) -> str:
    special_captions = {
        "task1_1__refusal_and_utilization_vs_operators": (
            "Совмещённый график вероятности отказа и коэффициента загрузки операторов "
            "от числа операторов."
        )
    }
    metric_names = {
        "busy_operators": "математического ожидания числа занятых операторов",
        "refusal": "вероятности отказа",
        "operators_utilization": "коэффициента загрузки операторов",
        "queue_exists": "вероятности существования очереди",
        "queue_length": "математического ожидания длины очереди",
        "queue_occupancy": "коэффициента занятости мест в очереди",
        "idle_machines": "математического ожидания числа простаивающих станков",
        "waiting_machines": "математического ожидания числа станков, ожидающих обслуживания",
        "waiting_probability": "вероятности ожидания обслуживания",
        "busy_repairers": "математического ожидания числа занятых наладчиков",
        "repairers_utilization": "коэффициента занятости наладчиков",
    }
    if figure_id in special_captions:
        return special_captions[figure_id]
    if figure_id.startswith("task1_2__"):
        metric = figure_id.split("__", 1)[1].split("_vs_", 1)[0]
        if figure_id.endswith("vs_queue__family_by_operators"):
            return f"Семейство графиков {metric_names[metric]} от числа мест в очереди при различных числах операторов."
        return f"Семейство графиков {metric_names[metric]} от числа операторов при различных числах мест в очереди."
    metric = figure_id.split("__", 1)[1].rsplit("_vs_", 1)[0]
    if figure_id.startswith("task2_1__"):
        return f"График {metric_names[metric]} от числа наладчиков."
    return f"График {metric_names[metric]} от числа операторов."


def task_input_items(section_id: str, derived: dict[str, Any]) -> list[str]:
    task1 = derived["derived"]["task1"]
    task2 = derived["derived"]["task2"]
    if section_id in {"1.1", "1.2", "1.3"}:
        return [
            f"Tc = {task1['tc_seconds']['value']} с",
            f"Ts = {task1['ts_seconds']['value']} с",
            f"λ = {format_float(task1['arrival_rate_per_second']['value'])} 1/с",
            f"μ = {format_float(task1['service_rate_per_second']['value'])} 1/с",
        ]
    if section_id == "1.4":
        return [
            f"Tc = {task1['tc_seconds']['value']} с",
            f"Ts = {task1['ts_seconds']['value']} с",
            f"Tw = {task1['tw_seconds']['value']} с",
            f"λ = {format_float(task1['arrival_rate_per_second']['value'])} 1/с",
            f"μ = {format_float(task1['service_rate_per_second']['value'])} 1/с",
            f"ν = {format_float(task1['abandonment_rate_per_second']['value'])} 1/с",
        ]
    return [
        f"N = {task2['machine_count']['value']}",
        f"Tc = {task2['tc_minutes']['value']} мин",
        f"Ts = {task2['ts_minutes']['value']} мин",
        f"λ = {format_float(task2['arrival_rate_per_minute']['value'])} 1/мин",
        f"μ = {format_float(task2['service_rate_per_minute']['value'])} 1/мин",
    ]


def result_paragraphs(section_id: str, task_output: dict[str, Any]) -> list[str]:
    summary = task_output["summary"]
    sweep = task_output["sweeps"][0]
    if section_id == "1.1":
        refusal = sweep["points"][-1]["metrics"]["refusal_probability"]
        return [
            f"Перебор по числу операторов выполнен до первого выполнения условия P_отк < {summary['refusal_target_probability']}.",
            f"Для текущего варианта минимальное число операторов равно {summary['minimal_operators_for_refusal_below_target']}, при этом вероятность отказа составляет {format_float(refusal)}.",
        ]
    if section_id == "1.2":
        return [
            "Построены оба требуемых sweep-режима: по числу мест в очереди при фиксированном числе операторов и по числу операторов при фиксированном числе мест в очереди.",
            "Во всех сериях использованы диапазоны от 1 до 15 без ручного отбора точек.",
        ]
    if section_id == "1.3":
        unstable = ", ".join(str(value) for value in summary["non_stationary_operators"])
        return [
            f"Нестационарными остаются режимы n = {unstable}; для них стационарные метрики в отчёте не подставляются.",
            f"Первое стационарное значение достигается при n = {summary['first_stationary_operators']}.",
        ]
    if section_id == "1.4":
        return [
            f"Во всех точках sweep используется детерминированное усечение бесконечного хвоста с epsilon = {summary['truncation_probability_epsilon']}.",
            "Статусы точек остаются stationary_truncated и прямо отражают используемую численную политику.",
        ]
    first_point = sweep["points"][0]["metrics"]
    last_point = sweep["points"][-1]["metrics"]
    return [
        "Вероятность ожидания в задаче 2.1 трактуется как arrival-weighted вероятность ожидания для нового отказа.",
        f"На концах диапазона r = 1 и r = 36 значения P_ож составляют {format_float(first_point['waiting_probability'])} и {format_float(last_point['waiting_probability'])} соответственно.",
    ]


def title_page(raw_inputs: dict[str, Any]) -> str:
    return f"""
\\begin{{titlepage}}
\\begin{{center}}
{{\\large Домашнее задание №1}}\\\\[1.0cm]
{{\\normalsize по курсу}}\\\\[0.2cm]
{{\\large «Имитационное моделирование технологических производственных процессов»}}\\\\[2.2cm]
{{\\normalsize Индивидуальный вариант}}\\\\[0.4cm]
{{\\normalsize Номер по журналу: {raw_inputs['journal_number']['value']}}}\\\\
{{\\normalsize День рождения: {raw_inputs['birth_day']['value']}}}\\\\
{{\\normalsize Месяц рождения: {raw_inputs['birth_month']['value']}}}\\\\[2.5cm]
\\begin{{flushright}}
Студент: \\rule{{7cm}}{{0.4pt}}\\\\[0.6cm]
Группа: \\rule{{7cm}}{{0.4pt}}\\\\[0.6cm]
Преподаватель: \\rule{{7cm}}{{0.4pt}}
\\end{{flushright}}
\\vfill
Москва, {date.today().year} г.
\\end{{center}}
\\end{{titlepage}}
"""
