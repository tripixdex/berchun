from __future__ import annotations

from typing import Any

from src.render.presentation import format_teacher_number
from src.render.task1_reflow_core import block, point


def _safe_checkpoint(points: list[dict[str, Any]], target: int) -> dict[str, Any]:
    by_value = {item["x_value"]: item for item in points}
    if target in by_value:
        return by_value[target]
    return min(points, key=lambda item: (abs(item["x_value"] - target), item["x_value"]))


def task2_blocks(spec: dict[str, Any], task_output: dict[str, Any], _: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    points = task_output["sweeps"][0]["points"]
    r1 = _safe_checkpoint(points, 1)
    r5 = _safe_checkpoint(points, 5)
    r10 = _safe_checkpoint(points, 10)
    r20 = _safe_checkpoint(points, 20)
    r33 = _safe_checkpoint(points, 33)
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
            ["Из найденного распределения считаются общее среднее число простаивающих станков M_пр и отдельно та их часть, которая уже ждёт наладчика, M_ож."],
            [spec["metric_formulas"][0]],
            [
                f"На опорных точках получаем: при r = {r1['x_value']} имеем M_пр = {format_teacher_number(r1['metrics']['idle_machines_expected'])} и M_ож = {format_teacher_number(r1['metrics']['waiting_machines_expected'])}; при r = {r10['x_value']} — {format_teacher_number(r10['metrics']['idle_machines_expected'])} и {format_teacher_number(r10['metrics']['waiting_machines_expected'])}.",
                f"При r = {r20['x_value']} среднее число ожидающих станков становится {format_teacher_number(r20['metrics']['waiting_machines_expected'])}, то есть очередь практически исчезает уже до полного насыщения по числу наладчиков.",
            ],
            spec["figure_ids"][:2],
            ["Первые два графика показывают переход от режима почти полного ожидания при малом r к режиму, где дальнейший рост числа наладчиков влияет уже главным образом на резерв, а не на длину очереди."],
        ),
        block(
            "Вероятность ожидания нового отказа.",
            ["Отдельно рассматривается вероятность того, что новый отказавший станок будет ожидать обслуживания: он может либо сразу попасть на обслуживание, либо встать в очередь к уже занятым наладчикам."],
            [spec["metric_formulas"][2]],
            [
                "Здесь P_ож означает вероятность того, что новый отказ увидит все r наладчиков занятыми; это не стационарная доля календарного времени, когда в системе вообще есть очередь.",
                f"Для сравнения: P_ож убывает с {format_teacher_number(r1['metrics']['waiting_probability'])} при r = {r1['x_value']} до {format_teacher_number(r10['metrics']['waiting_probability'])} при r = {r10['x_value']} и до {format_teacher_number(r20['metrics']['waiting_probability'])} при r = {r20['x_value']}.",
                f"В характерной точке r = {r10['x_value']} вероятность того, что новый отказ будет ожидать обслуживания, равна {format_teacher_number(r10['metrics']['waiting_probability'])}, тогда как стационарная вероятность наличия очереди составляет {queue_state_share}.",
            ],
            [spec["figure_ids"][2]],
            ["Кривая подтверждает, что после выхода из режима острой нехватки наладчиков эта вероятность сначала убывает быстрее всего, а затем продолжает снижаться по мере уменьшения очереди."],
        ),
        block(
            "Занятые наладчики и их загрузка.",
            ["После этого по тем же p_i считаются среднее число реально занятых наладчиков и коэффициент их загрузки; эти величины показывают уже цену выбранного резерва обслуживания."],
            [spec["metric_formulas"][1]],
            [
                f"На характерных точках: при r = {r5['x_value']} имеем M_зан = {format_teacher_number(r5['metrics']['busy_repairers_expected'])} и K_загр = {format_teacher_number(r5['metrics']['repairers_utilization'])}; при r = {r10['x_value']} — {format_teacher_number(r10['metrics']['busy_repairers_expected'])} и {format_teacher_number(r10['metrics']['repairers_utilization'])}.",
                f"Даже при r = {r33['x_value']} в среднем заняты лишь {format_teacher_number(r33['metrics']['busy_repairers_expected'])} наладчика, поэтому коэффициент загрузки снижается до {format_teacher_number(r33['metrics']['repairers_utilization'])}.",
            ],
            spec["figure_ids"][3:],
            ["Последние два графика показывают компромисс: абсолютное число занятых наладчиков быстро выходит к своему пределу, а относительная загрузка каждого наладчика убывает по мере роста резерва."],
        ),
    ]
    return state_blocks, metric_blocks
