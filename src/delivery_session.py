from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.delivery_request import DeliveryRequest, GUIDE_PROFILES, REPORT_PROFILES, build_delivery_request
from src.delivery_runtime import run_delivery

SESSION_PROFILES = ("none", "report_only", "study_pack", "guide_only", "print_pack")
PROFILE_FORMATS = {"report_only": ("pdf", "docx"), "study_pack": ("bundle_dir",), "guide_only": ("md", "pdf"), "print_pack": ("bundle_dir",)}
GUIDE_SCOPE_OPTIONS = ("task1", "task2", "full")
GUIDE_MODE_OPTIONS = ("variant_aware", "general")
CONFIRM_WORDS, EDIT_WORDS, CANCEL_WORDS = {"confirm", "c", "yes", "y", "да", "д"}, {"edit", "e", "редактировать", "r"}, {
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
    build_scope, run_id, draft = str(build_summary["report_scope"]), str(build_summary["run_id"]), {"delivery_profile": "none"}
    while True:
        draft = _prompt_delivery_draft(prompt, display, build_scope, draft)
        if draft["delivery_profile"] == "none":
            return {"status": "skipped", "selection": "none"}
        request = _build_request(run_id, draft)
        display(_request_summary(request))
        action = prompt("Действие для delivery [confirm/edit/cancel]: ").strip().lower()
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
            return {"status": "success", "request": _request_payload(request), "result": result}
        if action in EDIT_WORDS:
            draft = _request_payload(request)
            continue
        if action in CANCEL_WORDS:
            return {"status": "cancelled", "request": _request_payload(request)}
        display("Неизвестное действие. Используйте confirm, edit или cancel.")


def _prompt_delivery_draft(prompt: Callable[[str], str], display: Callable[[str], None], build_scope: str, draft: dict[str, str | None]) -> dict[str, str | None]:
    profile = _ask_choice(prompt, display, "delivery_profile", SESSION_PROFILES, str(draft.get("delivery_profile") or "none"))
    if profile == "none":
        return {"delivery_profile": "none"}
    report_scope = _ask_choice(prompt, display, "report_scope", (build_scope,), str(draft.get("report_scope") or build_scope)) if profile in REPORT_PROFILES else None
    guide_mode = None
    guide_scope = None
    if profile in GUIDE_PROFILES:
        guide_mode = _ask_choice(prompt, display, "guide_mode", GUIDE_MODE_OPTIONS, str(draft.get("guide_mode") or "variant_aware"))
        options = _guide_scope_options(profile, guide_mode, build_scope)
        default_scope = str(draft.get("guide_scope") or options[0])
        guide_scope = _ask_choice(prompt, display, "guide_scope", options, default_scope if default_scope in options else options[0])
    output_format = _ask_choice(prompt, display, "output_format", PROFILE_FORMATS[profile], str(draft.get("output_format") or PROFILE_FORMATS[profile][0]))
    return {
        "delivery_profile": profile,
        "report_scope": report_scope,
        "guide_mode": guide_mode,
        "guide_scope": guide_scope,
        "output_format": output_format,
    }


def _ask_choice(prompt: Callable[[str], str], display: Callable[[str], None], name: str, options: tuple[str, ...], default: str) -> str:
    hint = ", ".join(options)
    while True:
        raw = prompt(f"{name} [{default}] [{hint}]: ").strip().lower()
        value = default if raw == "" else raw
        if value in options:
            return value
        display(f"Недопустимое значение для {name}. Разрешено: {hint}.")


def _guide_scope_options(profile: str, guide_mode: str, build_scope: str) -> tuple[str, ...]:
    if profile == "study_pack":
        return (build_scope,)
    if guide_mode == "general":
        return GUIDE_SCOPE_OPTIONS
    return GUIDE_SCOPE_OPTIONS if build_scope == "full" else (build_scope,)


def _build_request(run_id: str, draft: dict[str, str | None]) -> DeliveryRequest:
    return build_delivery_request(
        delivery_profile=str(draft["delivery_profile"]),
        output_format=str(draft["output_format"]),
        report_scope=draft.get("report_scope"),
        guide_scope=draft.get("guide_scope"),
        guide_mode=draft.get("guide_mode"),
        source_run_id=run_id if draft["delivery_profile"] in REPORT_PROFILES or draft.get("guide_mode") == "variant_aware" else None,
    )


def _request_summary(request: DeliveryRequest) -> str:
    lines = ["Нормализованный delivery request:"]
    fields = [
        ("delivery_profile", request.delivery_profile),
        ("report_scope", request.report_scope or "—"),
        ("guide_mode", request.guide_mode or "—"),
        ("guide_scope", request.guide_scope or "—"),
        ("output_format", request.output_format),
        ("source_run_id", request.source_run_id or "—"),
    ]
    for index, (name, value) in enumerate(fields, start=1):
        lines.append(f"{index}. {name}: {value}")
    return "\n".join(lines)


def _request_payload(request: DeliveryRequest) -> dict[str, str | None]:
    return {
        "delivery_profile": request.delivery_profile,
        "report_scope": request.report_scope,
        "guide_mode": request.guide_mode,
        "guide_scope": request.guide_scope,
        "output_format": request.output_format,
    }
