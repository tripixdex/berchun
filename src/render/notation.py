from __future__ import annotations

from typing import Any

from src.render.presentation import format_teacher_number


def task_input_items(section_id: str, derived: dict[str, Any]) -> list[str]:
    task1 = derived["derived"]["task1"]
    task2 = derived["derived"]["task2"]
    if section_id in {"1.1", "1.2", "1.3"}:
        return [
            f"Tc = {format_teacher_number(task1['tc_seconds']['value'])}",
            f"Ts = {format_teacher_number(task1['ts_seconds']['value'])}",
        ]
    if section_id == "1.4":
        return [
            f"Tc = {format_teacher_number(task1['tc_seconds']['value'])}",
            f"Ts = {format_teacher_number(task1['ts_seconds']['value'])}",
            f"Tw = {format_teacher_number(task1['tw_seconds']['value'])}",
        ]
    return [
        f"N = {format_teacher_number(task2['machine_count']['value'])}",
        f"Tc = {format_teacher_number(task2['tc_minutes']['value'])}",
        f"Ts = {format_teacher_number(task2['ts_minutes']['value'])}",
    ]


def notation_items(section_id: str, derived: dict[str, Any]) -> list[str]:
    task1 = derived["derived"]["task1"]
    task2 = derived["derived"]["task2"]
    if section_id == "1.1":
        return [
            "S_k — состояние с k занятыми операторами, k = 0, ..., n.",
            f"λ = 1/Tc = {format_teacher_number(task1['arrival_rate_per_second']['value'])} 1/с, μ = 1/Ts = {format_teacher_number(task1['service_rate_per_second']['value'])} 1/с.",
            "a = λ/μ — приведённая нагрузка; p_k — стационарная вероятность состояния S_k.",
            "P_отк — вероятность отказа; M_зан и K_загр — среднее число занятых операторов и их загрузка.",
        ]
    if section_id == "1.2":
        return [
            "S_k при k = 0, ..., n описывают число занятых операторов; правые состояния отвечают длине очереди r = 1, ..., m.",
            f"λ = {format_teacher_number(task1['arrival_rate_per_second']['value'])} 1/с, μ = {format_teacher_number(task1['service_rate_per_second']['value'])} 1/с; a = λ/μ.",
            "ρ_n = λ/(nμ) — коэффициент загрузки системы при фиксированном n; p_k — вероятности состояний.",
            "P_отк — вероятность отказа; P_оч — вероятность существования очереди; L_оч и K_мест — средняя длина и занятость мест очереди.",
            "M_зан — среднее число занятых операторов; K_загр — коэффициент их загрузки.",
        ]
    if section_id == "1.3":
        return [
            "Состояния до границы n описывают занятых операторов, а правый хвост схемы — число ожидающих заявок.",
            f"λ = {format_teacher_number(task1['arrival_rate_per_second']['value'])} 1/с, μ = {format_teacher_number(task1['service_rate_per_second']['value'])} 1/с; a = λ/μ.",
            "ρ_n = λ/(nμ) — условие стационарности; стационарные метрики вычисляются только при ρ_n < 1.",
            "P_ож — вероятность того, что поступившая заявка застала все n операторов занятыми.",
            "P_оч и L_оч — вероятность существования очереди и средняя длина очереди в стационарном режиме.",
        ]
    if section_id == "1.4":
        return [
            "S_k описывают общее число заявок в системе; при k > n часть заявок находится в очереди.",
            f"λ = {format_teacher_number(task1['arrival_rate_per_second']['value'])} 1/с, μ = {format_teacher_number(task1['service_rate_per_second']['value'])} 1/с, ν = 1/Tw = {format_teacher_number(task1['abandonment_rate_per_second']['value'])} 1/с.",
            "β_k — интенсивность поступления новых заявок; δ_k — суммарная интенсивность обратного перехода из состояния k.",
            "p_k — стационарная вероятность состояния после численного усечения хвоста.",
            "P_оч и L_оч — вероятность существования очереди и средняя длина очереди с учётом ухода клиентов.",
        ]
    return [
        "S_i — состояние с i неисправными станками.",
        f"λ = 1/Tc = {format_teacher_number(task2['arrival_rate_per_minute']['value'])} 1/мин, μ = 1/Ts = {format_teacher_number(task2['service_rate_per_minute']['value'])} 1/мин.",
        "λ_i = (N-i)λ — интенсивность очередного отказа; μ_i = min(i,r)μ — интенсивность восстановления.",
        "p_i — стационарная вероятность состояния S_i.",
        "M_пр и M_ож — средние числа простаивающих и ожидающих обслуживания станков; P_ож — вероятность того, что новый отказавший станок попадёт в ожидание.",
        "M_зан и K_загр — среднее число занятых наладчиков и коэффициент загрузки наладчиков.",
    ]
