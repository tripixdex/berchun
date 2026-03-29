from __future__ import annotations

from typing import Any

from src.render.presentation import format_scientific, format_teacher_number
from src.render.task1_reflow_core import block, point


def task13_blocks(spec: dict[str, Any], task_output: dict[str, Any], derived: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    points = task_output["sweeps"][0]["points"]
    first_stationary = task_output["summary"]["first_stationary_operators"]
    non_stationary = ", ".join(str(value) for value in task_output["summary"]["non_stationary_operators"])
    stationary_points = [item for item in points if "wait_probability" in item.get("diagnostics", {})]
    n_first = stationary_points[0]
    n_mid = stationary_points[min(2, len(stationary_points) - 1)]
    n_high = stationary_points[min(5, len(stationary_points) - 1)]
    load = format_teacher_number(derived["derived"]["task1"]["offered_load_erlangs"]["value"])
    state_blocks = [
        block(
            "Проверка стационарности.",
            ["Для бесконечной очереди вычисления начинаются с условия ρ_n < 1: без него стационарное распределение и все средние характеристики просто не существуют."],
            spec["state_formulas"][:2],
            [
                f"В рассматриваемом варианте a = {load}, поэтому условие ρ_n < 1 впервые выполняется только при n = {first_stationary}.",
                f"Поэтому режимы n = {non_stationary} остаются нестационарными и в графиках не получают выдуманных стационарных значений.",
            ],
        ),
        block(
            "Вероятность ожидания.",
            ["После нормировки можно отдельно выписать вероятность того, что новая заявка застанет все n операторов занятыми; именно через неё дальше выражаются метрики очереди."],
            spec["state_formulas"][2:],
            [
                f"В первой стационарной точке n = {n_first['x_value']} получаем P_wait = {format_teacher_number(n_first['diagnostics']['wait_probability'])}, "
                "поэтому уже первая стационарная точка соответствует высокой вероятности ожидания."
            ],
        ),
    ]
    metric_blocks = [
        block(
            "Занятые операторы.",
            ["В устойчивом режиме приведённая нагрузка полностью задаёт среднее число занятых операторов, а коэффициент загрузки показывает, насколько этот спрос велик по отношению к выбранному n."],
            [spec["metric_formulas"][0]],
            [
                f"Для ориентира: M_зан остаётся равным {format_teacher_number(n_first['metrics']['busy_operators_expected'])}, "
                f"но коэффициент загрузки падает с {format_teacher_number(n_first['metrics']['operators_utilization'])} при n = {n_first['x_value']} "
                f"до {format_teacher_number(n_mid['metrics']['operators_utilization'])} при n = {n_mid['x_value']} и "
                f"{format_teacher_number(n_high['metrics']['operators_utilization'])} при n = {n_high['x_value']}."
            ],
            spec["figure_ids"][:2],
            ["По первым двум графикам видно, что при росте числа операторов меняется не обслуженная нагрузка, а запас свободной мощности системы."],
        ),
        block(
            "Ожидание в очереди.",
            ["После определения P_wait характеристики очереди выражаются через ρ_n; именно они показывают, насколько опасно приближение к границе устойчивости."],
            spec["metric_formulas"][1:],
            [
                f"По расчёту: при n = {n_first['x_value']} имеем P_оч = {format_teacher_number(n_first['metrics']['queue_exists_probability'])} и L_оч = {format_teacher_number(n_first['metrics']['queue_length_expected'])}; "
                f"уже при n = {n_mid['x_value']} эти значения снижаются до {format_teacher_number(n_mid['metrics']['queue_exists_probability'])} и {format_teacher_number(n_mid['metrics']['queue_length_expected'])}.",
                f"При n = {n_high['x_value']} очередь практически исчезает: P_оч = {format_teacher_number(n_high['metrics']['queue_exists_probability'])}, L_оч = {format_teacher_number(n_high['metrics']['queue_length_expected'])}.",
            ],
            spec["figure_ids"][2:],
            ["Графики подтверждают, что бесконечная очередь особенно чувствительна к первым стационарным значениям n: около границы устойчивости хвост очереди возрастает резко."],
        ),
    ]
    return state_blocks, metric_blocks


def task14_blocks(spec: dict[str, Any], task_output: dict[str, Any], _: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    points = task_output["sweeps"][0]["points"]
    n1, n5, n8 = (point(points, value) for value in (1, 5, 8))
    max_tail_probability = max(item["truncation"]["tail_probability_upper_bound"] for item in points)
    max_tail_queue = max(item["truncation"]["tail_queue_upper_bound"] for item in points)
    summary = task_output["summary"]
    state_blocks = [
        block(
            "Интенсивности переходов.",
            ["В этой модели поток поступления остаётся тем же, но после заполнения операторов обратные переходы ускоряются за счёт ухода клиентов из очереди."],
            spec["state_formulas"][:2],
            ["Пока k ≤ n, выход из состояния определяется только обслуживанием. После появления очереди к нему добавляется уход клиентов со скоростью ν, поэтому дальний хвост распределения затухает быстрее, чем без ухода."],
        ),
        block(
            "Рекуррентное построение и усечение хвоста.",
            ["После задания β_k и δ_k вероятности p_k строятся рекуррентно. Поскольку хвост бесконечен, численное суммирование обрывается только после достижения заданного порога точности."],
            spec["state_formulas"][2:],
            [
                f"Во всём диапазоне n = 1..15 бесконечный хвост распределения усечён при пороге усечения ε = {summary['truncation_probability_epsilon']}.",
                "Оставшийся вклад не превышает "
                f"{format_scientific(max_tail_probability)} по вероятности и {format_scientific(max_tail_queue)} по среднему числу заявок в очереди, поэтому он пренебрежим в пределах учебной точности отчёта.",
                "Во всех рассчитанных точках стационарные метрики получены после контролируемого численного усечения хвоста, а не после произвольной отсечки.",
            ],
        ),
    ]
    metric_blocks = [
        block(
            "Занятые операторы.",
            ["После нормировки суммируем среднее число занятых операторов и по нему оцениваем загрузку каждого оператора."],
            [spec["metric_formulas"][0]],
            [f"На характерных точках: при n = 1 получаем M_зан = {format_teacher_number(n1['metrics']['busy_operators_expected'])} и K_загр = {format_teacher_number(n1['metrics']['operators_utilization'])}; при n = 5 — {format_teacher_number(n5['metrics']['busy_operators_expected'])} и {format_teacher_number(n5['metrics']['operators_utilization'])}; при n = 8 — {format_teacher_number(n8['metrics']['busy_operators_expected'])} и {format_teacher_number(n8['metrics']['operators_utilization'])}."],
            spec["figure_ids"][:2],
            ["Графики показывают, что среднее число занятых операторов быстро выходит к уровню приведённой нагрузки, тогда как загрузка каждого оператора убывает по мере появления резерва обслуживания."],
        ),
        block(
            "Очередь и уход клиентов.",
            ["Теперь рассматриваем хвост состояний k > n: именно он определяет вероятность существования очереди и её среднюю длину с учётом ухода клиентов."],
            spec["metric_formulas"][1:],
            [
                f"Для ориентира: при n = 1 вероятность существования очереди равна {format_teacher_number(n1['metrics']['queue_exists_probability'])}, а средняя длина очереди — {format_teacher_number(n1['metrics']['queue_length_expected'])}.",
                f"При n = 5 эти значения снижаются до {format_teacher_number(n5['metrics']['queue_exists_probability'])} и {format_teacher_number(n5['metrics']['queue_length_expected'])}, а при n = 8 — до {format_teacher_number(n8['metrics']['queue_exists_probability'])} и {format_teacher_number(n8['metrics']['queue_length_expected'])}.",
            ],
            spec["figure_ids"][2:],
            ["То есть уход клиентов не устраняет очередь при малом n, но заметно сокращает её хвост уже на умеренных значениях числа операторов."],
        ),
    ]
    return state_blocks, metric_blocks
