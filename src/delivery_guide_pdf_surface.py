from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GuidePdfVisualPlan:
    section_heading: str
    scheme_caption: str
    scheme_name: str
    plot_anchor: str | None = None
    plot_caption: str | None = None
    plot_name: str | None = None


PDF_VISUAL_PLANS = (
    GuidePdfVisualPlan(
        section_heading="### 1.1. Система без очереди",
        scheme_caption="Схема подпункта 1.1.",
        scheme_name="task1_1__scheme.png",
        plot_anchor="#### Как читать совмещённый график отказа и загрузки",
        plot_caption="Опорный график 1.1: отказ и загрузка при изменении числа операторов.",
        plot_name="task1_1__refusal_and_utilization_vs_operators.png",
    ),
    GuidePdfVisualPlan(
        section_heading="### 1.2. Система с ограниченной очередью",
        scheme_caption="Схема подпункта 1.2.",
        scheme_name="task1_2__scheme.png",
        plot_anchor="#### Блок `Семейства по числу операторов при фиксированном m`",
        plot_caption="Опорный график 1.2: отказ при изменении числа операторов для разных очередей.",
        plot_name="task1_2__refusal_vs_operators__family_by_queue.png",
    ),
    GuidePdfVisualPlan(
        section_heading="### 1.3. Система с неограниченной очередью",
        scheme_caption="Схема подпункта 1.3.",
        scheme_name="task1_3__scheme.png",
        plot_anchor="#### Блок `Очередь`",
        plot_caption="Опорный график 1.3: средняя длина очереди при увеличении числа операторов.",
        plot_name="task1_3__queue_length_vs_operators.png",
    ),
    GuidePdfVisualPlan(
        section_heading="### 1.4. Система с неограниченной очередью и уходом клиентов",
        scheme_caption="Схема подпункта 1.4.",
        scheme_name="task1_4__scheme.png",
        plot_anchor="#### Блок `Очередь и уход клиентов`",
        plot_caption="Опорный график 1.4: средняя длина очереди при увеличении числа операторов.",
        plot_name="task1_4__queue_length_vs_operators.png",
    ),
    GuidePdfVisualPlan(
        section_heading="### 2.1. Метрики производственного участка по числу наладчиков",
        scheme_caption="Схема подпункта 2.1.",
        scheme_name="task2_1__scheme.png",
        plot_anchor="#### Блок `Вероятность ожидания нового отказа`",
        plot_caption="Опорный график 2.1: вероятность ожидания обслуживания при увеличении числа наладчиков.",
        plot_name="task2_1__waiting_probability_vs_repairers.png",
    ),
)


def build_pdf_surface_markdown(*, guide_text: str, guide_dir: Path) -> str:
    lines = guide_text.splitlines()
    output: list[str] = []
    current_plan: GuidePdfVisualPlan | None = None
    inserted_scheme = False
    inserted_plot = False
    plans_by_section = {plan.section_heading: plan for plan in PDF_VISUAL_PLANS}
    for line in lines:
        if line.startswith("### "):
            current_plan = plans_by_section.get(line)
            inserted_scheme = False
            inserted_plot = False
        output.append(line)
        if current_plan is None:
            continue
        if line == "#### Схема и состояния" and not inserted_scheme:
            output.extend(_figure_block(guide_dir, "assets/schemes", current_plan.scheme_name, current_plan.scheme_caption))
            inserted_scheme = True
        if line == current_plan.plot_anchor and not inserted_plot and current_plan.plot_name and current_plan.plot_caption:
            output.extend(_figure_block(guide_dir, "assets/plots", current_plan.plot_name, current_plan.plot_caption))
            inserted_plot = True
    return "\n".join(output).rstrip() + "\n"


def _figure_block(guide_dir: Path, relative_dir: str, file_name: str, caption: str) -> list[str]:
    asset_path = guide_dir / relative_dir / file_name
    if not asset_path.exists():
        return []
    relative_path = asset_path.relative_to(guide_dir).as_posix()
    return [
        "",
        f"![{caption}]({relative_path})",
        "",
        f"*{caption}*",
        "",
    ]
