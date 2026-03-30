from __future__ import annotations

from dataclasses import dataclass

from src.report_scope import normalize_report_scope

DELIVERY_PROFILES = ("report_only", "study_pack", "guide_only", "print_pack")
GUIDE_MODES = ("variant_aware", "general")
OUTPUT_FORMATS = ("pdf", "md", "bundle_dir", "docx")
REPORT_PROFILES = frozenset({"report_only", "study_pack", "print_pack"})
GUIDE_PROFILES = frozenset({"study_pack", "guide_only"})


def _normalize_choice(name: str, value: str, allowed: tuple[str, ...]) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {value!r}")
    return normalized


def _normalize_optional(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


@dataclass(frozen=True)
class DeliveryRequest:
    delivery_profile: str
    output_format: str
    report_scope: str | None
    guide_scope: str | None
    guide_mode: str | None
    source_run_id: str | None

    @property
    def source_kind(self) -> str:
        return "general_baseline" if self.delivery_profile == "guide_only" and self.guide_mode == "general" else "run_bundle"

    @property
    def guide_source_kind(self) -> str | None:
        if self.guide_mode is None:
            return None
        return "general_baseline" if self.guide_mode == "general" else "run_bundle"

    @property
    def requires_source_run(self) -> bool:
        return self.delivery_profile in REPORT_PROFILES or self.guide_mode == "variant_aware"


def build_delivery_request(
    *,
    delivery_profile: str,
    output_format: str,
    report_scope: str | None = None,
    guide_scope: str | None = None,
    guide_mode: str | None = None,
    source_run_id: str | None = None,
) -> DeliveryRequest:
    profile = _normalize_choice("delivery_profile", delivery_profile, DELIVERY_PROFILES)
    fmt = _normalize_choice("output_format", output_format, OUTPUT_FORMATS)
    run_id = _normalize_optional(source_run_id)
    normalized_report_scope = None
    normalized_guide_scope = None
    normalized_guide_mode = None

    if profile in REPORT_PROFILES:
        normalized_report_scope = normalize_report_scope(report_scope)
    elif report_scope is not None:
        raise ValueError(f"{profile} does not accept report_scope")

    if profile in GUIDE_PROFILES:
        normalized_guide_scope = normalize_report_scope(guide_scope)
        if guide_mode is None:
            raise ValueError(f"{profile} requires guide_mode")
        normalized_guide_mode = _normalize_choice("guide_mode", guide_mode, GUIDE_MODES)
    elif guide_scope is not None or guide_mode is not None:
        raise ValueError(f"{profile} does not accept guide_scope or guide_mode")

    if profile == "report_only" and fmt not in {"pdf", "docx"}:
        raise ValueError("report_only requires output_format='pdf' or 'docx' in the current delivery runtime")
    if profile == "guide_only" and fmt not in {"md", "pdf", "docx"}:
        raise ValueError("guide_only requires output_format='md', 'pdf' or 'docx' in the current delivery runtime")
    if profile in {"study_pack", "print_pack"} and fmt != "bundle_dir":
        raise ValueError(f"{profile} requires output_format='bundle_dir' in the v1 delivery runtime")
    if profile == "study_pack" and normalized_guide_scope != normalized_report_scope:
        raise ValueError("study_pack requires guide_scope to match report_scope in the v1 delivery runtime")
    if run_id is None and (profile in REPORT_PROFILES or normalized_guide_mode == "variant_aware"):
        raise ValueError("source_run_id is required for report-bearing deliveries and variant-aware guide deliveries")
    if run_id is not None and profile == "guide_only" and normalized_guide_mode == "general":
        raise ValueError("guide_only/general does not accept source_run_id in F02C2")

    return DeliveryRequest(
        delivery_profile=profile,
        output_format=fmt,
        report_scope=normalized_report_scope,
        guide_scope=normalized_guide_scope,
        guide_mode=normalized_guide_mode,
        source_run_id=run_id,
    )
