from __future__ import annotations

from pathlib import Path
from typing import Any

from src.render.content import plot_caption, post_figure_paragraphs, result_paragraphs
from src.render.notation import notation_items, task_input_items
from src.render.common import figure_block, formulas_block, latex_escape
from src.render.presentation import labeled_lines_block
PLOT_WIDTH = r"0.8\textwidth"
STATE_TITLES = {
    "1.1": "Распределение состояний.",
    "1.2": "Распределение состояний.",
    "1.3": "Стационарное распределение.",
    "1.4": "Рекуррентное распределение.",
    "2.1": "Распределение состояний.",
}
STATE_LEADS = {
    "1.1": "Система без очереди полностью задаётся числом занятых операторов, поэтому после распределения состояний сразу определяются загрузка операторов и вероятность отказа.",
    "1.2": "После состояний с k = 0, ..., n занятыми операторами добавляются состояния очереди длины r = 1, ..., m, поэтому то же распределение используется и для потерь, и для характеристик ожидания.",
    "1.3": "Для бесконечной очереди сначала фиксируется условие стационарности ρ_n < 1; только в устойчивых точках допускается вычисление стационарных средних характеристик.",
    "1.4": "В модели с уходом клиентов стационарное распределение строится рекуррентно по birth-death переходам, где после заполнения операторов обратные переходы ускоряются за счёт ухода ожидающих клиентов.",
    "2.1": "Вероятности состояний строятся по числу неисправных станков i, а интенсивности отказов и восстановления меняются вместе с текущим состоянием участка.",
}

def _paragraphs(paragraphs: list[str]) -> str:
    return "".join(f"{latex_escape(paragraph)}\n\n" for paragraph in paragraphs)

def _lead_line(title: str | None, lead: list[str]) -> str:
    if not title:
        return _paragraphs(lead)
    if not lead:
        return f"\\noindent\\textbf{{{latex_escape(title)}}}\n\n"
    first, *rest = lead
    return f"\\noindent\\textbf{{{latex_escape(title)}}} {latex_escape(first)}\n\n" + _paragraphs(rest)


def _render_block(
    spec: dict[str, Any],
    block: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    figure_index: int,
) -> tuple[str, int]:
    parts = []
    parts.append(_lead_line(block["title"], block["lead"]))
    if block["formulas"]:
        parts.append(formulas_block(block["formulas"]))
    for figure_id in block["figure_ids"]:
        entry = figure_entries[figure_id]
        caption = f"Рисунок {spec['section_id']}.{figure_index}. {plot_caption(figure_id)}"
        parts.append(figure_block(entry["tex_path"], caption, width=PLOT_WIDTH))
        figure_index += 1
    if block["tail"]:
        parts.append(_paragraphs(block["tail"]))
    return "".join(parts), figure_index
def _state_block(spec: dict[str, Any], task_output: dict[str, Any]) -> str:
    state_tail = {"1.2": result_paragraphs(spec["section_id"], task_output), "1.3": result_paragraphs(spec["section_id"], task_output), "1.4": result_paragraphs(spec["section_id"], task_output)}.get(spec["section_id"], [])
    return (
        _lead_line(STATE_TITLES[spec["section_id"]], [STATE_LEADS[spec["section_id"]]])
        + formulas_block(spec["state_formulas"])
        + _paragraphs(state_tail)
    )
def _metric_blocks(spec: dict[str, Any], task_output: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = spec["metric_formulas"]
    figures = spec["figure_ids"]
    results = result_paragraphs(spec["section_id"], task_output)
    if spec["section_id"] == "1.1":
        return [
            {
                "title": "Число занятых операторов.",
                "lead": ["После нахождения p_k среднее число занятых операторов и их средняя загрузка вычисляются по тому же распределению состояний."],
                "formulas": [metrics[1], metrics[2]],
                "figure_ids": [figures[0]],
                "tail": [],
            },
            {
                "title": "Вероятность отказа.",
                "lead": ["Отказ возникает только при полной занятости всех операторов, поэтому отдельного анализа требует именно крайнее состояние цепи."],
                "formulas": [metrics[0]],
                "figure_ids": [figures[1]],
                "tail": results,
            },
        ]
    if spec["section_id"] == "1.2":
        return [
            {"title": "Семейства по числу мест в очереди.", "lead": ["Сначала фиксируется число операторов n, а по оси абсцисс изменяется число мест в очереди m."], "formulas": [], "figure_ids": [], "tail": []},
            {"title": "Вероятность отказа.", "lead": ["При фиксированном n вероятность отказа определяется последним состоянием цепи с заполненной очередью."], "formulas": [metrics[0]], "figure_ids": [figures[0]], "tail": []},
            {"title": "Занятые операторы и их загрузка.", "lead": ["По тем же точкам отдельно прослеживаются среднее число занятых операторов и относительная загрузка имеющегося ресурса обслуживания."], "formulas": [metrics[1]], "figure_ids": [figures[1], figures[2]], "tail": []},
            {"title": "Очередь.", "lead": ["Следующие графики показывают, как уменьшение потерь перераспределяется в вероятность появления очереди, её среднюю длину и занятость мест."], "formulas": [metrics[2], metrics[3]], "figure_ids": [figures[3], figures[4], figures[5]], "tail": post_figure_paragraphs(spec["section_id"], figures[5], task_output)},
            {"title": "Семейства по числу операторов.", "lead": ["Затем фиксируется число мест в очереди m, а по оси абсцисс изменяется число операторов n."], "formulas": [], "figure_ids": [], "tail": []},
            {"title": "Вероятность отказа.", "lead": ["При фиксированном m рост числа операторов меняет как общий уровень отказов, так и скорость их убывания; используется то же выражение для P_отк, что и в предыдущем семействе."], "formulas": [], "figure_ids": [figures[6]], "tail": []},
            {"title": "Занятые операторы и их загрузка.", "lead": ["На том же sweep сравниваются те же характеристики M_зан и загрузки операторов, но уже при изменении n."], "formulas": [], "figure_ids": [figures[7], figures[8]], "tail": []},
            {"title": "Очередь.", "lead": ["Последний блок показывает, как увеличение n одновременно уменьшает вероятность очереди, её длину и занятость выделенных мест при тех же формулах для P_оч, L_оч и K_мест."], "formulas": [], "figure_ids": [figures[9], figures[10], figures[11]], "tail": post_figure_paragraphs(spec["section_id"], figures[11], task_output)},
        ]
    if spec["section_id"] == "1.3":
        return [
            {
                "title": "Занятые операторы.",
                "lead": ["В устойчивом режиме offered load a полностью определяет среднее число занятых операторов, а коэффициент загрузки нормирует это среднее по n."],
                "formulas": [metrics[0]],
                "figure_ids": [figures[0], figures[1]],
                "tail": [],
            },
            {
                "title": "Ожидание в очереди.",
                "lead": ["После определения P_wait стационарные характеристики очереди выражаются через ρ_n и показывают цену приближения к границе устойчивости."],
                "formulas": [metrics[1], metrics[2]],
                "figure_ids": [figures[2], figures[3]],
                "tail": [],
            },
        ]
    if spec["section_id"] == "1.4":
        return [
            {
                "title": "Занятые операторы.",
                "lead": ["После усечения хвоста на уровне текущей численной точности по распределению суммируется среднее число занятых операторов и их загрузка."],
                "formulas": [metrics[0]],
                "figure_ids": [figures[0], figures[1]],
                "tail": [],
            },
            {
                "title": "Очередь и уход клиентов.",
                "lead": ["Хвост распределения начиная с состояний k > n даёт вероятность существования очереди и её среднюю длину уже с учётом ухода клиентов."],
                "formulas": [metrics[1], metrics[2]],
                "figure_ids": [figures[2], figures[3]],
                "tail": [],
            },
        ]
    return [
        {
            "title": "Простаивающие и ожидающие станки.",
            "lead": ["Сначала по распределению состояний вычисляются средние числа простаивающих станков и станков, ожидающих обслуживания."],
            "formulas": [metrics[0]],
            "figure_ids": [figures[0], figures[1]],
            "tail": [],
        },
        {
            "title": "Вероятность ожидания обслуживания.",
            "lead": ["Отдельно рассматривается вероятность того, что новый отказавший станок попадёт именно в ожидание, а не сразу на обслуживание."],
            "formulas": [metrics[2]],
            "figure_ids": [figures[2]],
            "tail": results,
        },
        {
            "title": "Занятые наладчики.",
            "lead": ["После этого по тем же вероятностям состояний определяются среднее число занятых наладчиков и коэффициент их занятости."],
            "formulas": [metrics[1]],
            "figure_ids": [figures[3], figures[4]],
            "tail": [],
        },
    ]
def subsection_tex(
    spec: dict[str, Any],
    figure_entries: dict[str, dict[str, Any]],
    task_output: dict[str, Any],
    derived: dict[str, Any],
    visible_label: str | None,
) -> str:
    parts = []
    label = latex_escape(spec["statement"])
    if visible_label is None:
        parts.append(f"{label}\n\n")
    else:
        parts.append(f"\\noindent\\textbf{{{latex_escape(visible_label)}}} {label}\n\n")
    parts.append(labeled_lines_block("Исходные данные:", task_input_items(spec["section_id"], derived)))
    parts.append(
        figure_block(
            str(Path("assets") / f"{spec['scheme_id']}.png"),
            f"Рисунок {spec['section_id']}.1. Расчетная схема.",
            width=r"0.9\textwidth",
        )
    )
    parts.append(labeled_lines_block("Обозначения:", notation_items(spec["section_id"], derived)))
    parts.append(_state_block(spec, task_output))
    figure_index = 2
    for block in _metric_blocks(spec, task_output):
        block_tex, figure_index = _render_block(spec, block, figure_entries, figure_index)
        parts.append(block_tex)
    parts.append("\\clearpage\n")
    return "".join(parts)
