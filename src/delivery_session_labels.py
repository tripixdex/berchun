from __future__ import annotations

from pathlib import Path
from typing import Any

from src.delivery_request import DeliveryRequest

SCENARIO_OPTIONS = (
    ("none", "Ничего дополнительно"),
    ("report_only", "Только итоговый отчёт"),
    ("study_pack", "Отчёт + материалы для подготовки"),
    ("guide_only", "Только материалы для подготовки"),
    ("print_pack", "Печатный комплект"),
)
MATERIAL_OPTIONS = (
    ("variant_aware", "Персональные материалы по этому варианту"),
    ("general", "Общие материалы без привязки к варианту"),
)
SCOPE_OPTIONS = (
    ("task1", "Только задача 1"),
    ("task2", "Только задача 2"),
    ("full", "Вся работа"),
)
FORMAT_OPTIONS = {
    "report_only": (("pdf", "PDF"), ("docx", "DOCX")),
    "guide_only": (("pdf", "PDF"), ("docx", "DOCX")),
    "study_pack": (("bundle_dir", "Папка-комплект"),),
    "print_pack": (("bundle_dir", "Папка для печати"),),
}


def label_for(options: tuple[tuple[str, str], ...], key: str) -> str:
    for option_key, label in options:
        if option_key == key:
            return label
    raise ValueError(f"unknown option key: {key!r}")


def human_scope(scope: str) -> str:
    return label_for(SCOPE_OPTIONS, scope)


def human_scenario(scenario: str) -> str:
    return label_for(SCENARIO_OPTIONS, scenario)


def human_material_mode(mode: str) -> str:
    return label_for(MATERIAL_OPTIONS, mode)


def human_format(profile: str, output_format: str) -> str:
    return label_for(FORMAT_OPTIONS[profile], output_format)


def human_created_label(profile: str, guide_mode: str | None = None) -> str:
    if profile == "report_only":
        return "Итоговый отчёт"
    if profile == "study_pack":
        return "Отчёт и персональные материалы для подготовки" if guide_mode == "variant_aware" else "Отчёт и общие материалы для подготовки"
    if profile == "guide_only":
        return "Персональная методичка" if guide_mode == "variant_aware" else "Общая методичка"
    return "Печатный комплект"


def selection_summary(draft: dict[str, str | None], report_profiles: frozenset[str], guide_profiles: frozenset[str]) -> str:
    profile = str(draft["delivery_profile"])
    lines = ["Выбранный результат:"]
    fields: list[tuple[str, str]] = [("Сценарий", human_scenario(str(draft["scenario"])))]
    if profile in report_profiles:
        fields.append(("Объём работы", human_scope(str(draft["report_scope"]))))
    if profile in guide_profiles:
        fields.append(("Материалы", human_material_mode(str(draft["guide_mode"]))))
        if profile == "guide_only":
            fields.append(("Объём методички", human_scope(str(draft["guide_scope"]))))
    fields.append(("Формат", human_format(profile, str(draft["output_format"]))))
    for index, (name, value) in enumerate(fields, start=1):
        lines.append(f"{index}. {name}: {value}")
    return "\n".join(lines)


def result_summary(build_summary: dict[str, Any], request: DeliveryRequest, result: dict[str, Any]) -> str:
    delivery_dir = Path(str(result["delivery_dir"]))
    lines = ["Что создано:", f"- {human_created_label(request.delivery_profile, request.guide_mode)} ({human_format(request.delivery_profile, request.output_format)})", "Локальные пути:"]
    for path in primary_paths(delivery_dir, request):
        if path.exists():
            lines.append(f"- {path}")
    lines.extend(["Технические детали:", f"- run_id: {build_summary['run_id']}", f"- delivery_id: {result['delivery_id']}"])
    return "\n".join(lines)


def primary_paths(delivery_dir: Path, request: DeliveryRequest) -> list[Path]:
    if request.delivery_profile == "report_only":
        return [delivery_dir / "report" / f"final_report.{request.output_format}"]
    if request.delivery_profile == "guide_only":
        suffix = "variant" if request.guide_mode == "variant_aware" else "general"
        return [delivery_dir / "guide" / f"methodical_guide__{suffix}.{request.output_format}"]
    if request.delivery_profile == "study_pack":
        suffix = "variant" if request.guide_mode == "variant_aware" else "general"
        return [delivery_dir, delivery_dir / "report" / "final_report.pdf", delivery_dir / "guide" / f"methodical_guide__{suffix}.pdf"]
    return [delivery_dir, delivery_dir / "report" / "final_report.pdf"]
