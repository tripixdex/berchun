from __future__ import annotations

from typing import Any

from src.render.common import format_float

TITLE_METADATA = {"student_full_name": "Гуров Владислав Александрович", "student_group": "РК9-84Б", "teacher_full_name": "Берчун Юрий Валерьевич"}


def plot_caption(figure_id: str) -> str:
    special_captions = {"task1_1__refusal_and_utilization_vs_operators": "Совмещённый график вероятности отказа и коэффициента загрузки операторов от числа операторов."}
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
def _series_point(task_output: dict[str, Any], sweep_index: int, fixed_key: str, fixed_value: int, x_value: int) -> dict[str, Any]:
    series = next(item for item in task_output["sweeps"][sweep_index]["series"] if item["fixed_parameters"][fixed_key] == fixed_value)
    return next(point for point in series["points"] if point["x_value"] == x_value)


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
        operators_start, operators_end = summary["operators_range"]
        queue_start, queue_end = summary["queue_places_range"]
        return [
            "Построены оба требуемых sweep-режима: по числу мест в очереди при фиксированном числе операторов и по числу операторов при фиксированном числе мест в очереди.",
            f"Во всех сериях использованы диапазоны по операторам {operators_start}..{operators_end} и по местам в очереди {queue_start}..{queue_end} без ручного отбора точек.",
        ]
    if section_id == "1.3":
        unstable = ", ".join(str(value) for value in summary["non_stationary_operators"])
        return [
            f"Нестационарными остаются режимы n = {unstable}; для них стационарные метрики в отчёте не подставляются.",
            f"Первое стационарное значение достигается при n = {summary['first_stationary_operators']}.",
        ]
    if section_id == "1.4":
        max_tail_probability = max(point["truncation"]["tail_probability_upper_bound"] for point in sweep["points"])
        max_tail_queue, first_point = max(point["truncation"]["tail_queue_upper_bound"] for point in sweep["points"]), sweep["points"][0]
        eight_operators = next(point for point in sweep["points"] if point["x_value"] == 8)
        return [
            f"Во всех точках sweep бесконечный хвост распределения усечён при epsilon = {summary['truncation_probability_epsilon']}.",
            "Максимальные верхние оценки невключённого остатка не превышают "
            f"{max_tail_probability:.3e} по вероятности и {max_tail_queue:.3e} по среднему числу заявок в очереди, "
            "поэтому их вклад пренебрежим в пределах учебной точности данного отчёта.",
            "Например, при n = "
            f"{first_point['x_value']} вероятность существования очереди составляет {format_float(first_point['metrics']['queue_exists_probability'])}, "
            f"а средняя длина очереди равна {format_float(first_point['metrics']['queue_length_expected'])}; "
            f"при n = {eight_operators['x_value']} эти значения снижаются до "
            f"{format_float(eight_operators['metrics']['queue_exists_probability'])} и {format_float(eight_operators['metrics']['queue_length_expected'])}.",
            "Статусы точек остаются stationary_truncated и прямо отражают используемую численную политику.",
        ]
    first_point = sweep["points"][0]["metrics"]
    last_point = sweep["points"][-1]["metrics"]
    repairers_start, repairers_end = summary["repairers_range"]
    characteristic_point = next(point for point in sweep["points"] if point["x_value"] == 10)
    queue_state_share = characteristic_point["diagnostics"]["queue_exists_probability_state"]
    return [
        "Вероятность ожидания в задаче 2.1 трактуется как вероятность того, что новый отказавший станок попадёт в ожидание обслуживания; это не стационарная доля состояний системы с очередью.",
        f"На концах диапазона r = {repairers_start} и r = {repairers_end} значения P_ож составляют {format_float(first_point['waiting_probability'])} и {format_float(last_point['waiting_probability'])} соответственно.",
        f"Для характерной точки r = {characteristic_point['x_value']} получаем P_ож = {format_float(characteristic_point['metrics']['waiting_probability'])}, "
        f"тогда как стационарная вероятность наличия очереди равна {format_float(queue_state_share)}; "
        f"среднее число ожидающих станков при этом составляет {format_float(characteristic_point['metrics']['waiting_machines_expected'])}.",
    ]


def post_figure_paragraphs(section_id: str, figure_id: str, task_output: dict[str, Any]) -> list[str]:
    if section_id != "1.2":
        return []
    if figure_id == "task1_2__queue_occupancy_vs_queue__family_by_operators":
        one_place = _series_point(task_output, 0, "operators", 5, 1)["metrics"]
        many_places = _series_point(task_output, 0, "operators", 5, 15)["metrics"]
        return [
            "При фиксированном n = 5 рост числа мест в очереди с m = 1 до m = 15 снижает вероятность отказа "
            f"с {format_float(one_place['refusal_probability'])} до {format_float(many_places['refusal_probability'])}, "
            "но одновременно переводит потерянные вызовы в ожидание: вероятность существования очереди растёт "
            f"с {format_float(one_place['queue_exists_probability'])} до {format_float(many_places['queue_exists_probability'])}, "
            f"а её средняя длина увеличивается с {format_float(one_place['queue_length_expected'])} до {format_float(many_places['queue_length_expected'])}.",
            "Математическое ожидание числа занятых операторов на том же примере растёт лишь "
            f"с {format_float(one_place['busy_operators_expected'])} до {format_float(many_places['busy_operators_expected'])}, "
            "то есть дополнительные места прежде всего уменьшают потери, а не создают новый ресурс обслуживания.",
        ]
    if figure_id == "task1_2__queue_occupancy_vs_operators__family_by_queue":
        five_operators = _series_point(task_output, 1, "queue_places", 5, 5)["metrics"]
        eleven_operators = _series_point(task_output, 1, "queue_places", 5, 11)["metrics"]
        return [
            "При фиксированном m = 5 увеличение числа операторов с n = 5 до n = 11 снижает вероятность отказа "
            f"с {format_float(five_operators['refusal_probability'])} до {format_float(eleven_operators['refusal_probability'])} "
            f"и среднюю длину очереди с {format_float(five_operators['queue_length_expected'])} до {format_float(eleven_operators['queue_length_expected'])}.",
            "Одновременно коэффициент загрузки операторов падает "
            f"с {format_float(five_operators['operators_utilization'])} до {format_float(eleven_operators['operators_utilization'])}, "
            "поэтому правое семейство графиков показывает цену снижения потерь и ожидания через недогрузку части операторов.",
        ]
    return []


def _title_value(raw_inputs: dict[str, Any], key: str) -> Any:
    value = raw_inputs.get(key)
    return value["value"] if isinstance(value, dict) else value


def title_page(raw_inputs: dict[str, Any], report_year: int) -> str:
    return f"""
\\begin{{titlepage}}
\\begin{{center}}
{{\\large Домашнее задание №1}}\\\\[1.0cm]
{{\\normalsize по курсу}}\\\\[0.2cm]
{{\\large «Имитационное моделирование технологических производственных процессов»}}\\\\[2.2cm]
{{\\normalsize Индивидуальный вариант}}\\\\[0.4cm]
{{\\normalsize Номер по журналу: {_title_value(raw_inputs, 'journal_number')}}}\\\\
{{\\normalsize День рождения: {_title_value(raw_inputs, 'birth_day')}}}\\\\
{{\\normalsize Месяц рождения: {_title_value(raw_inputs, 'birth_month')}}}\\\\[2.5cm]
\\begin{{flushright}}
Студент: {raw_inputs.get('student_full_name', TITLE_METADATA['student_full_name'])}\\\\[0.6cm]
Группа: {raw_inputs.get('student_group', TITLE_METADATA['student_group'])}\\\\[0.6cm]
Преподаватель: {raw_inputs.get('teacher_full_name', TITLE_METADATA['teacher_full_name'])}
\\end{{flushright}}
\\vfill
Москва, {report_year} г.
\\end{{center}}
\\end{{titlepage}}
"""
