from __future__ import annotations

from typing import Any

from src.render.presentation import format_teacher_number
from src.render.task1_reflow_core import block, point, series_point


def task11_blocks(spec: dict[str, Any], task_output: dict[str, Any], derived: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    points = task_output["sweeps"][0]["points"]
    threshold = task_output["summary"]["minimal_operators_for_refusal_below_target"]
    target = task_output["summary"]["refusal_target_probability"]
    threshold_point = point(points, threshold)["metrics"]
    lower_n = max(points[0]["x_value"], threshold - 1)
    upper_n = min(points[-1]["x_value"], threshold + 1)
    lower_point = point(points, lower_n)["metrics"]
    upper_point = point(points, upper_n)["metrics"]
    load = format_teacher_number(derived["derived"]["task1"]["offered_load_erlangs"]["value"])
    state_blocks = [
        block(
            "Переход от исходных данных к вероятностям состояний.",
            ["По Tc и Ts определяем интенсивности потока и обслуживания, после чего записываем стационарные вероятности состояний S_k, где k равно числу занятых операторов."],
            spec["state_formulas"],
            [
                f"В рассматриваемом варианте приведённая нагрузка равна {load}, поэтому даже в системе без очереди крайнее состояние S_n заметно влияет на итоговые метрики.",
                "Далее из того же распределения последовательно получаются средняя занятость операторов и вероятность отказа.",
            ],
        )
    ]
    metric_blocks = [
        block(
            "Занятые операторы и загрузка.",
            ["Из найденных p_k суммируем среднее число занятых операторов, а затем делим его на n и получаем коэффициент загрузки."],
            [spec["metric_formulas"][1], spec["metric_formulas"][2]],
            [
                f"В числах это даёт: при n = {lower_n} имеем M_зан = {format_teacher_number(lower_point['busy_operators_expected'])} и K_загр = {format_teacher_number(lower_point['operators_utilization'])}; "
                f"при n = {upper_n} — {format_teacher_number(upper_point['busy_operators_expected'])} и {format_teacher_number(upper_point['operators_utilization'])}."
            ],
            [spec["figure_ids"][0]],
            [
                f"График показывает, что после n = {lower_n} среднее число занятых операторов растёт уже слабо: добавление новых операторов дальше создаёт прежде всего запас по отказам, а не существенный прирост фактической занятости."
            ],
        ),
        block(
            "Вероятность отказа.",
            ["Крайнее состояние S_n отвечает ситуации, когда новый звонок приходит в момент полной занятости всех операторов."],
            [spec["metric_formulas"][0]],
            [
                f"Для ориентира: при n = {lower_n} вероятность отказа равна {format_teacher_number(lower_point['refusal_probability'])}, "
                f"а при n = {threshold} — {format_teacher_number(threshold_point['refusal_probability'])}."
            ],
            [spec["figure_ids"][1]],
            [
                f"По графику отказов условие P_отк < {target} впервые выполняется при n = {threshold}.",
                f"В этой точке вероятность отказа равна {format_teacher_number(threshold_point['refusal_probability'])}, поэтому значение n = {threshold} принимается как минимально достаточное для текущего варианта.",
            ],
        ),
    ]
    return state_blocks, metric_blocks


def task12_blocks(spec: dict[str, Any], task_output: dict[str, Any], _: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    n5m1, n5m5, n5m15 = (series_point(task_output, 0, "operators", 5, value)["metrics"] for value in (1, 5, 15))
    m5n5, m5n8, m5n11 = (series_point(task_output, 1, "queue_places", 5, value)["metrics"] for value in (5, 8, 11))
    state_blocks = [
        block(
            "Нормировка распределения.",
            ["После состояний обслуживания добавляются состояния ожидания, поэтому сначала выписываем приведённую нагрузку a, коэффициент ρ_n и нормировочную формулу p_0."],
            spec["state_formulas"][:2],
            ["На этом шаге вся вероятность уже делится между занятыми операторами и правым хвостом очереди, поэтому одна и та же нормировка дальше обслуживает и потери, и показатели ожидания."],
        ),
        block(
            "Вероятности состояний обслуживания и очереди.",
            ["Вероятности удобно разделить на две части: состояния k = 0, ..., n описывают обслуживание, а состояния n + r — очередь длины r."],
            spec["state_formulas"][2:],
            [
                "Именно эти p_k затем используются во всех семействах графиков без ручной подстановки отдельных режимов.",
                "В текущем варианте просматриваются все сочетания n = 1..15 и m = 1..15, поэтому сравнение по графикам остаётся полным и последовательным.",
            ],
        ),
    ]
    metric_blocks = [
        block("Семейства по числу мест в очереди.", ["Фиксируем число операторов n и смотрим, как изменение m перераспределяет потери и ожидание."]),
        block(
            "Вероятность отказа.",
            ["При фиксированном n отказ определяется последним состоянием цепи с заполненной очередью."],
            [spec["metric_formulas"][0]],
            [f"По расчёту: при n = 5 рост m от 1 до 5 снижает P_отк с {format_teacher_number(n5m1['refusal_probability'])} до {format_teacher_number(n5m5['refusal_probability'])}, а при m = 15 вероятность отказа становится {format_teacher_number(n5m15['refusal_probability'])}."],
            [spec["figure_ids"][0]],
            ["Левое семейство подтверждает, что первые дополнительные места в очереди дают наибольший выигрыш по потерям, после чего эффект постепенно насыщается."],
        ),
        block(
            "Занятые операторы и загрузка.",
            ["По тем же вероятностям состояний отдельно вычисляем среднее число занятых операторов и коэффициент их загрузки."],
            [spec["metric_formulas"][1]],
            [f"При том же n = 5 среднее число занятых операторов увеличивается лишь с {format_teacher_number(n5m1['busy_operators_expected'])} до {format_teacher_number(n5m15['busy_operators_expected'])}, а коэффициент загрузки — с {format_teacher_number(n5m1['operators_utilization'])} до {format_teacher_number(n5m15['operators_utilization'])}."],
            [spec["figure_ids"][1], spec["figure_ids"][2]],
            ["Так расширение очереди почти не создаёт новый ресурс обслуживания, а прежде всего уменьшает долю потерянных вызовов."],
        ),
        block(
            "Очередь.",
            ["Теперь переходим к метрикам ожидания: они показывают, какая часть ранее потерянных вызовов переходит в очередь."],
            [spec["metric_formulas"][2], spec["metric_formulas"][3]],
            [
                f"При n = 5 переход от m = 1 к m = 15 увеличивает вероятность существования очереди с {format_teacher_number(n5m1['queue_exists_probability'])} до {format_teacher_number(n5m15['queue_exists_probability'])}, а среднюю длину очереди — с {format_teacher_number(n5m1['queue_length_expected'])} до {format_teacher_number(n5m15['queue_length_expected'])}.",
                f"Одновременно занятость одного места падает с {format_teacher_number(n5m1['queue_occupancy'])} до {format_teacher_number(n5m15['queue_occupancy'])}, то есть очередь становится длиннее, но каждое отдельное место используется менее интенсивно.",
            ],
            spec["figure_ids"][3:6],
            ["Графики этого блока показывают цену снижения отказов: потери уменьшаются, но часть нагрузки переносится в ожидание."],
        ),
        block("Семейства по числу операторов.", ["Во второй серии графиков, наоборот, фиксируем m и смотрим, как добавление операторов меняет те же метрики."]),
        block(
            "Вероятность отказа.",
            ["При фиксированном m используется то же выражение для P_отк, но теперь основной фактор — увеличение доступного числа операторов."],
            [],
            [f"В числах это видно так: при m = 5 увеличение числа операторов с n = 5 до n = 8 снижает P_отк с {format_teacher_number(m5n5['refusal_probability'])} до {format_teacher_number(m5n8['refusal_probability'])}; при n = 11 оно остаётся на уровне {format_teacher_number(m5n11['refusal_probability'])}."],
            [spec["figure_ids"][6]],
            ["Здесь отказ убывает быстрее, чем в предыдущем семействе, поскольку система получает новый обслуживающий ресурс, а не только дополнительный буфер ожидания."],
        ),
        block(
            "Занятые операторы и загрузка.",
            ["В той же серии графиков видно, что абсолютная занятость системы меняется мало, зато загрузка каждого отдельного оператора заметно падает."],
            [],
            [f"Для m = 5 среднее число занятых операторов меняется с {format_teacher_number(m5n5['busy_operators_expected'])} при n = 5 до {format_teacher_number(m5n11['busy_operators_expected'])} при n = 11, а коэффициент загрузки падает с {format_teacher_number(m5n5['operators_utilization'])} до {format_teacher_number(m5n11['operators_utilization'])}."],
            [spec["figure_ids"][7], spec["figure_ids"][8]],
            ["Это и есть плата за снижение потерь и ожидания: часть операторов работает как резерв, а не как постоянно загруженный ресурс."],
        ),
        block(
            "Очередь.",
            ["Последний блок показывает, как рост n одновременно уменьшает и вероятность очереди, и её среднюю длину при неизменном числе мест ожидания."],
            [],
            [
                f"При m = 5 вероятность существования очереди снижается с {format_teacher_number(m5n5['queue_exists_probability'])} при n = 5 до {format_teacher_number(m5n8['queue_exists_probability'])} при n = 8 и до {format_teacher_number(m5n11['queue_exists_probability'])} при n = 11.",
                f"Средняя длина очереди за тот же переход падает с {format_teacher_number(m5n5['queue_length_expected'])} до {format_teacher_number(m5n8['queue_length_expected'])} и далее до {format_teacher_number(m5n11['queue_length_expected'])}.",
            ],
            spec["figure_ids"][9:12],
            ["Таким образом, второе семейство графиков показывает уже не перераспределение потерь в ожидание, а фактическое снятие перегрузки за счёт дополнительных операторов."],
        ),
    ]
    return state_blocks, metric_blocks
