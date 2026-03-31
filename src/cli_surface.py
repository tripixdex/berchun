from __future__ import annotations

from pathlib import Path
from typing import Any

from src.delivery_request import DeliveryRequest
from src.delivery_session_labels import extra_result_paths, first_open_path, human_created_label, human_format, human_scope, main_result_path


def cli_summary(command: str, summary: dict[str, Any], request: DeliveryRequest | None = None) -> str | None:
    if command == "build":
        return _build_cli_summary(summary)
    if command == "deliver" and request is not None:
        return _delivery_cli_summary(request, summary)
    if command == "report":
        return _report_cli_summary(summary)
    if command == "figures":
        return _figures_cli_summary(summary)
    if command == "solve":
        return _solve_cli_summary(summary)
    return None


def _build_cli_summary(summary: dict[str, Any]) -> str | None:
    if summary.get("session_mode") == "build_with_optional_delivery":
        delivery = summary["delivery"]
        if delivery["status"] == "success":
            return None
        note = "Дополнительно ничего не создавалось." if delivery["status"] == "skipped" else "Дополнительное создание результата отменено."
        return _build_summary_lines(summary["build"], note)
    return _build_summary_lines(summary)


def _build_summary_lines(build: dict[str, Any], note: str | None = None) -> str:
    lines = [
        "Готово.",
        "Что создано:",
        f"- Сборка работы ({human_scope(str(build['report_scope']))})",
        "Главный результат — откройте его первым:",
        f"- {Path(str(build['bundle']['report_pdf_path']))}",
        "Где лежит полный пакет расчёта:",
        f"- {Path(str(build['run_dir']))}",
    ]
    if note:
        lines.append(note)
    lines.extend(["Если нужны детали:", f"- run_id: {build['run_id']}", f"- режим сборки: {build['build_mode']}"])
    return "\n".join(lines)


def _delivery_cli_summary(request: DeliveryRequest, result: dict[str, Any]) -> str:
    delivery_dir = Path(str(result["delivery_dir"]))
    main_path = main_result_path(delivery_dir, request)
    first_path = first_open_path(delivery_dir, request)
    lines = [
        "Готово.",
        "Что создано:",
        f"- {human_created_label(request.delivery_profile, request.guide_mode)} ({human_format(request.delivery_profile, request.output_format)})",
    ]
    if main_path == first_path:
        lines.extend(["Главный результат — откройте его первым:", f"- {main_path}"])
    else:
        lines.extend(["Где лежит основной результат:", f"- {main_path}", "Что открыть сначала:", f"- {first_path}"])
    extras = [path for path in extra_result_paths(delivery_dir, request) if path.exists()]
    if extras:
        lines.append("Что ещё создано рядом:")
        lines.extend(f"- {path}" for path in extras)
    lines.append("Если нужны детали:")
    if request.source_run_id:
        lines.append(f"- run_id: {request.source_run_id}")
    lines.append(f"- delivery_id: {result['delivery_id']}")
    return "\n".join(lines)


def _report_cli_summary(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Готово.",
            "Что создано:",
            "- Итоговый отчёт (PDF)",
            "Главный результат — откройте его первым:",
            f"- {Path(str(summary['report_pdf_path']))}",
            "Что ещё создано рядом:",
            f"- {Path(str(summary['report_source_file']))}",
        ]
    )


def _figures_cli_summary(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Готово.",
            "Что создано:",
            "- Набор графиков и manifest",
            "Где лежит основной результат:",
            f"- {Path(str(summary['figures_dir']))}",
            "Что открыть сначала:",
            f"- {Path(str(summary['manifest_path']))}",
        ]
    )


def _solve_cli_summary(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Готово.",
            "Что создано:",
            "- Расчётные данные по текущему варианту",
            "Где лежит основной результат:",
            f"- {Path(str(summary['out_dir']))}",
            "Что открыть сначала:",
            f"- {Path(str(summary['derived_path']))}",
        ]
    )
