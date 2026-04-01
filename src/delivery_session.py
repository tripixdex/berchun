from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.delivery_request import DeliveryRequest, GUIDE_PROFILES, REPORT_PROFILES, build_delivery_request
from src.delivery_runtime import run_delivery
from src.delivery_session_labels import (
    BUNDLE_GUIDE_FORMAT_OPTIONS,
    BUNDLE_REPORT_FORMAT_OPTIONS,
    FORMAT_OPTIONS,
    MATERIAL_OPTIONS,
    SCENARIO_OPTIONS,
    SCOPE_OPTIONS,
    human_scope,
    result_summary,
    selection_summary,
)

PROFILE_FORMATS = {profile: tuple(key for key, _label in options) for profile, options in FORMAT_OPTIONS.items()}
CONFIRM_WORDS, EDIT_WORDS, CANCEL_WORDS = {"", "confirm", "c", "yes", "y", "да", "д"}, {"edit", "e", "редактировать", "r"}, {
    "cancel",
    "x",
    "no",
    "n",
    "нет",
    "н",
}


def run_build_delivery_session(
    *,
    build_summary: dict[str, Any],
    prompt: Callable[[str], str],
    display: Callable[[str], None],
    runs_dir: Path,
    deliveries_dir: Path,
    guide_source_path: Path,
    general_guide_source_path: Path,
    guide_derived_path: Path,
    guide_data_dir: Path,
    general_assets_manifest_path: Path,
) -> dict[str, Any]:
    build_scope, run_id, draft = str(build_summary["report_scope"]), str(build_summary["run_id"]), {"scenario": "none"}
    while True:
        draft = _prompt_delivery_draft(prompt, display, build_scope, draft)
        if draft["scenario"] == "none":
            return {"status": "skipped", "selection": "none"}
        request = _build_request(run_id, draft)
        display(selection_summary(draft, REPORT_PROFILES, GUIDE_PROFILES))
        action = prompt("Действие [Enter=создать, e=изменить, x=отмена]: ").strip().lower()
        if action in CONFIRM_WORDS:
            result = run_delivery(
                request=request,
                runs_dir=runs_dir,
                deliveries_dir=deliveries_dir,
                guide_source_path=guide_source_path,
                general_guide_source_path=general_guide_source_path,
                guide_derived_path=guide_derived_path,
                guide_data_dir=guide_data_dir,
                general_assets_manifest_path=general_assets_manifest_path,
            )
            display(result_summary(build_summary, request, result))
            return {"status": "success", "request": _request_payload(request), "result": result}
        if action in EDIT_WORDS:
            continue
        if action in CANCEL_WORDS:
            return {"status": "cancelled", "request": _request_payload(request)}
        display("Не понял действие. Нажмите Enter для создания, e для изменения или x для отмены.")


def _prompt_delivery_draft(prompt: Callable[[str], str], display: Callable[[str], None], build_scope: str, draft: dict[str, str | None]) -> dict[str, str | None]:
    scenario = _ask_menu_choice(prompt, display, "Что вы хотите получить на выходе?", SCENARIO_OPTIONS, str(draft.get("scenario") or "none"), "сценария результата")
    if scenario == "none":
        return {"scenario": "none"}
    if scenario == "report_only":
        output_format = _ask_menu_choice(prompt, display, "В каком формате вам нужен отчёт?", FORMAT_OPTIONS["report_only"], str(draft.get("output_format") or "pdf"), "формата отчёта")
        return {
            "scenario": scenario,
            "delivery_profile": scenario,
            "report_scope": build_scope,
            "guide_mode": None,
            "guide_scope": None,
            "output_format": output_format,
            "report_output_format": None,
            "guide_output_format": None,
        }
    if scenario == "print_pack":
        return {
            "scenario": scenario,
            "delivery_profile": scenario,
            "report_scope": build_scope,
            "guide_mode": None,
            "guide_scope": None,
            "output_format": "bundle_dir",
            "report_output_format": None,
            "guide_output_format": None,
        }
    guide_mode = _ask_menu_choice(prompt, display, "Какие материалы для подготовки вам нужны?", MATERIAL_OPTIONS, str(draft.get("guide_mode") or "variant_aware"), "типа материалов")
    if scenario == "study_pack":
        report_output_format = _ask_menu_choice(
            prompt,
            display,
            "В каком формате нужен отчёт внутри комплекта?",
            BUNDLE_REPORT_FORMAT_OPTIONS,
            str(draft.get("report_output_format") or "pdf"),
            "формата отчёта в комплекте",
        )
        guide_output_format = _ask_menu_choice(
            prompt,
            display,
            "В каком формате нужны материалы внутри комплекта?",
            BUNDLE_GUIDE_FORMAT_OPTIONS,
            str(draft.get("guide_output_format") or "pdf"),
            "формата материалов в комплекте",
        )
        return {
            "scenario": scenario,
            "delivery_profile": scenario,
            "report_scope": build_scope,
            "guide_mode": guide_mode,
            "guide_scope": build_scope,
            "output_format": "bundle_dir",
            "report_output_format": report_output_format,
            "guide_output_format": guide_output_format,
        }
    guide_scope = _ask_menu_choice(
        prompt,
        display,
        "Какой объём методички вам нужен?",
        tuple((key, human_scope(key)) for key in _guide_scope_options(guide_mode, build_scope)),
        str(draft.get("guide_scope") or _guide_scope_options(guide_mode, build_scope)[0]),
        "объёма материалов",
    )
    output_format = _ask_menu_choice(prompt, display, "В каком формате вам нужна методичка?", FORMAT_OPTIONS["guide_only"], str(draft.get("output_format") or "pdf"), "формата методички")
    return {
        "scenario": scenario,
        "delivery_profile": scenario,
        "report_scope": None,
        "guide_mode": guide_mode,
        "guide_scope": guide_scope,
        "output_format": output_format,
        "report_output_format": None,
        "guide_output_format": None,
    }


def _ask_menu_choice(
    prompt: Callable[[str], str],
    display: Callable[[str], None],
    title: str,
    options: tuple[tuple[str, str], ...],
    default: str,
    error_name: str,
) -> str:
    labels = {str(index): key for index, (key, _label) in enumerate(options, start=1)}
    normalized_labels = {label.lower(): key for key, label in options}
    display("\n".join([title, *[f"{index}. {label}" for index, (_key, label) in enumerate(options, start=1)]]))
    default_label = next(label for key, label in options if key == default)
    while True:
        raw = prompt(f"Выбор [{default_label}]: ").strip().lower()
        value = default if raw == "" else labels.get(raw) or normalized_labels.get(raw)
        if value in {key for key, _label in options}:
            return value
        display(f"Недопустимое значение для {error_name}. Разрешено: {', '.join(label for _key, label in options)}.")


def _guide_scope_options(guide_mode: str, build_scope: str) -> tuple[str, ...]:
    if guide_mode == "general":
        return tuple(key for key, _label in SCOPE_OPTIONS)
    return tuple(key for key, _label in SCOPE_OPTIONS) if build_scope == "full" else (build_scope,)


def _build_request(run_id: str, draft: dict[str, str | None]) -> DeliveryRequest:
    return build_delivery_request(
        delivery_profile=str(draft["delivery_profile"]),
        output_format=str(draft["output_format"]),
        report_scope=draft.get("report_scope"),
        guide_scope=draft.get("guide_scope"),
        guide_mode=draft.get("guide_mode"),
        source_run_id=run_id if draft["delivery_profile"] in REPORT_PROFILES or draft.get("guide_mode") == "variant_aware" else None,
        report_output_format=draft.get("report_output_format"),
        guide_output_format=draft.get("guide_output_format"),
    )
def _request_payload(request: DeliveryRequest) -> dict[str, str | None]:
    return {
        "delivery_profile": request.delivery_profile,
        "report_scope": request.report_scope,
        "guide_mode": request.guide_mode,
        "guide_scope": request.guide_scope,
        "output_format": request.output_format,
        "report_output_format": request.report_output_format,
        "guide_output_format": request.guide_output_format,
    }
