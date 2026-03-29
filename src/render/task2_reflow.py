from __future__ import annotations

from typing import Any

from src.render.presentation import format_teacher_number
from src.render.task1_reflow_core import block, point


def task2_blocks(spec: dict[str, Any], task_output: dict[str, Any], _: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    points = task_output["sweeps"][0]["points"]
    r1, r5, r10, r20, r33 = (point(points, value) for value in (1, 5, 10, 20, 33))
    queue_state_share = format_teacher_number(r10["diagnostics"]["queue_exists_probability_state"])
    state_blocks = [
        block(
            "Состояния отказов и восстановлений.",
            ["Состояние S_i задаёт число неисправных станков, поэтому при росте i поток новых отказов ослабевает, а суммарная скорость восстановления сначала растёт, а затем ограничивается числом наладчиков r."],
            [spec["state_formulas"][0]],
            ["Именно так локально задаются интенсивности переходов между соседними состояниями, из которых потом последовательно строится всё стационарное распределение."],
        ),
        block(
            "Рекуррентное распределение состояний.",
            ["После задания интенсивностей вероятности p_i удобно получать рекуррентно: сначала выражаем очередное состояние через предыдущее, затем закрываем цепь нормировкой по всем i = 0, ..., N."],
            spec["state_formulas"][1:],
            ["Таким образом, одна и та же последовательность p_i затем используется и для показателей простоя, и для вероятности ожидания, и для загрузки наладчиков."],
        ),
    ]
    metric_blocks = [
        block(
            "Простаивающие и ожидающие станки.",
            ["Сначала из найденного распределения считаются общее среднее число простаивающих станков M_пр и отдельно та их часть, которая уже ждёт наладчика, M_ож."],
            [spec["metric_formulas"][0]],
            [
                f"Числовой checkpoint: при r = 1 получаем M_пр = {format_teacher_number(r1['metrics']['idle_machines_expected'])} и M_ож = {format_teacher_number(r1['metrics']['waiting_machines_expected'])}; при r = 10 — {format_teacher_number(r10['metrics']['idle_machines_expected'])} и {format_teacher_number(r10['metrics']['waiting_machines_expected'])}.",
                f"При r = 20 среднее число ожидающих станков становится {format_teacher_number(r20['metrics']['waiting_machines_expected'])}, то есть очередь практически исчезает уже до полного насыщения по числу наладчиков.",
            ],
            spec["figure_ids"][:2],
            ["Первые два графика показывают переход от режима почти полного ожидания при малом r к режиму, где дальнейший рост числа наладчиков влияет уже главным образом на резерв, а не на длину очереди."],
        ),
        block(
            "Вероятность ожидания нового отказа.",
            ["Затем отдельно рассматривается именно arrival-weighted вероятность: новый отказавший станок может либо сразу попасть на обслуживание, либо встать в очередь к уже занятым наладчикам."],
            [spec["metric_formulas"][2]],
            [
                "Здесь P_ож означает вероятность того, что новый отказ увидит все r наладчиков занятыми; это не стационарная доля календарного времени, когда в системе вообще есть очередь.",
                f"Числовой checkpoint: P_ож убывает с {format_teacher_number(r1['metrics']['waiting_probability'])} при r = 1 до {format_teacher_number(r10['metrics']['waiting_probability'])} при r = 10 и до {format_teacher_number(r20['metrics']['waiting_probability'])} при r = 20.",
                f"В характерной точке r = 10 arrival-weighted вероятность ожидания равна {format_teacher_number(r10['metrics']['waiting_probability'])}, тогда как стационарная вероятность наличия очереди составляет {queue_state_share}.",
            ],
            [spec["figure_ids"][2]],
            ["График подтверждает, что после выхода из режима острой нехватки наладчиков эта вероятность падает быстрее всего, а затем стремится к нулю уже без заметной очереди."],
        ),
        block(
            "Занятые наладчики и их загрузка.",
            ["После этого по тем же p_i считаются среднее число реально занятых наладчиков и коэффициент их загрузки; эти величины показывают уже цену выбранного резерва обслуживания."],
            [spec["metric_formulas"][1]],
            [
                f"Числовой checkpoint: при r = 5 имеем M_зан = {format_teacher_number(r5['metrics']['busy_repairers_expected'])} и K_загр = {format_teacher_number(r5['metrics']['repairers_utilization'])}; при r = 10 — {format_teacher_number(r10['metrics']['busy_repairers_expected'])} и {format_teacher_number(r10['metrics']['repairers_utilization'])}.",
                f"Даже при r = 33 в среднем заняты лишь {format_teacher_number(r33['metrics']['busy_repairers_expected'])} наладчика, поэтому коэффициент загрузки снижается до {format_teacher_number(r33['metrics']['repairers_utilization'])}.",
            ],
            spec["figure_ids"][3:],
            ["Последние два графика показывают типичный компромисс: абсолютное число занятых наладчиков быстро выходит к своему пределу, а относительная загрузка каждого наладчика убывает по мере роста резерва."],
        ),
    ]
    return state_blocks, metric_blocks
