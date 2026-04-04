from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from src.build_pipeline import resolve_build_input, run_build
from src.cli_surface import cli_summary
from src.delivery_request import build_delivery_request
from src.delivery_runtime import run_delivery
from src.delivery_session import run_build_delivery_session
from src.input_schema import current_report_year
from src.input_surface import (
    INPUT_CHOOSER_SENTINEL,
    STARTER_YAML_SENTINEL,
    choose_input_path,
    choose_starter_yaml_path,
    format_input_validation_error,
    prompt_build_input_recovery_action,
    write_starter_yaml,
)
from src.operator_session import resolve_operator_start_args
from src.pipeline import run
from src.plots import generate_figure_artifacts
from src.render import build_report_package
from src.report_scope import REPORT_SCOPES
DEFAULT_VARIANT_PATH, DEFAULT_DERIVED_PATH = Path("inputs/variant_me.yaml"), Path("inputs/derived_parameters.json")
DEFAULT_OUT_DIR, DEFAULT_FIGURES_DIR = Path("out/data"), Path("figures")
DEFAULT_FIGURE_MANIFEST_PATH = Path("out/artifacts/figure_manifest.json")
DEFAULT_REPORT_SOURCE_PATH, DEFAULT_REPORT_PDF_PATH = Path("report/final_report.tex"), Path("report/final_report.pdf")
DEFAULT_REPORT_ASSETS_MANIFEST_PATH = Path("report/assets_manifest.json")
DEFAULT_RUNS_DIR, DEFAULT_DELIVERIES_DIR = Path("runs"), Path("deliveries")
DEFAULT_GUIDE_SOURCE_PATH = Path("docs/methodical/content/METHODICAL_GUIDE.md")
DEFAULT_GUIDE_GENERAL_SOURCE_PATH = Path("docs/methodical/content/METHODICAL_GUIDE_GENERAL_SOURCE.md")
DEFAULT_REPORT_YEAR = current_report_year()
CLI_DESCRIPTION = "Canonical repository CLI for the analytical pipeline.\nRecommended operator path: `build --interactive --offer-delivery`.\nUse direct `deliver` only when you already know the technical delivery request.\nUse `--json` only for raw technical output."
CLI_EPILOG = """Examples:
  python3 -m src.cli build --interactive --offer-delivery
  python3 -m src.cli build --input inputs/examples/student_example.yaml
  python3 -m src.cli build --input --review --offer-delivery
  python3 -m src.cli build --starter-yaml inputs/my_input.yaml
  python3 -m src.cli build --input inputs/examples/student_example.yaml --review
  python3 -m src.cli build --interactive
  python3 -m src.cli report --report-scope task1
  python3 -m src.cli solve
  python3 -m src.cli deliver --delivery-profile report_only --output-format pdf --report-scope full --source-run-id <run_id>
  python3 -m src.cli deliver --delivery-profile report_only --output-format docx --report-scope full --source-run-id <run_id>

Default generated outputs for `build`:
  runs/<run_id>/
  plus refreshed working-set mirrors at the requested output paths
"""
def _stderr_display(message: str) -> None: print(message, file=sys.stderr)
def _stderr_prompt(message: str) -> str: print(message, end="", file=sys.stderr, flush=True); return input()


def _activate_default_build_mode(args: argparse.Namespace) -> None:
    if args.command != "build":
        return
    if args.interactive or args.input_path is not None or args.starter_yaml_path is not None:
        return

    while True:
        _stderr_display(
            "\n".join(
                [
                    "Как запустить работу?",
                    "1. Интерактивная сборка + выбор итоговых артефактов",
                    "2. Выбрать YAML в CLI + review + выбор итоговых артефактов",
                    "3. Создать starter YAML",
                ]
            )
        )
        raw = _stderr_prompt("Выбор [Enter=1, 1-3, x=отмена]: ").strip().lower()
        if raw in {"", "1"}:
            args.interactive = True
            args.offer_delivery = True
            return
        if raw == "2":
            args.input_path = INPUT_CHOOSER_SENTINEL
            args.review = True
            args.offer_delivery = True
            return
        if raw == "3":
            args.starter_yaml_path = STARTER_YAML_SENTINEL
            return
        if raw in {"x", "cancel", "no", "n", "нет", "н"}:
            _stderr_display("Отменено.")
            raise SystemExit(2)
        _stderr_display("Нажмите Enter, 1, 2, 3 или x.")


def _build_summary_with_recovery(args: argparse.Namespace) -> dict[str, object]:
    input_path_value: str | None = args.input_path
    interactive = args.interactive
    while True:
        try:
            chosen_input_path = (
                choose_input_path(prompt=_stderr_prompt, display=_stderr_display)
                if input_path_value == INPUT_CHOOSER_SENTINEL
                else Path(input_path_value) if input_path_value else None
            )
            raw_input = resolve_build_input(
                input_path=chosen_input_path,
                interactive=interactive,
                review=args.review,
                prompt=_stderr_prompt,
                display=_stderr_display,
            )
            build_summary = run_build(
                raw_input=raw_input,
                variant_path=Path(args.variant_path),
                derived_path=Path(args.derived_path),
                out_dir=Path(args.out_dir),
                figures_dir=Path(args.figures_dir),
                figure_manifest_path=Path(args.manifest_path),
                report_source_path=Path(args.report_source_path),
                report_pdf_path=Path(args.report_pdf_path),
                assets_manifest_path=Path(args.report_assets_manifest_path),
                runs_dir=Path(args.runs_dir),
            )
            if args.offer_delivery:
                return {
                    "session_mode": "build_with_optional_delivery",
                    "build": build_summary,
                    "delivery": run_build_delivery_session(
                        build_summary=build_summary,
                        prompt=_stderr_prompt,
                        display=_stderr_display,
                        runs_dir=Path(args.runs_dir),
                        deliveries_dir=Path(args.deliveries_dir),
                        guide_source_path=Path(args.guide_source_path),
                        general_guide_source_path=Path(args.guide_general_source_path),
                        guide_derived_path=Path(args.derived_path),
                        guide_data_dir=Path(args.data_dir),
                        general_assets_manifest_path=Path(args.report_assets_manifest_path),
                    ),
                }
            return build_summary
        except ValueError as error:
            human_error = format_input_validation_error(error)
            if human_error is None:
                raise
            _stderr_display(human_error)
            recovery = prompt_build_input_recovery_action(
                prompt=_stderr_prompt,
                display=_stderr_display,
                allow_choose_yaml=not interactive,
            )
            if recovery == "cancel":
                raise SystemExit(2)
            if recovery == "starter":
                starter_path = choose_starter_yaml_path(prompt=_stderr_prompt, display=_stderr_display)
                write_starter_yaml(starter_path)
                return {"starter_yaml_path": str(starter_path)}
            if recovery == "choose_yaml":
                input_path_value = INPUT_CHOOSER_SENTINEL
                interactive = False
                continue
            continue


def _resolve_operator_default_argv(argv: list[str] | None) -> list[str]:
    actual_argv = list(sys.argv[1:] if argv is None else argv)

    if actual_argv[:2] == ["-m", "src.cli"]:
        actual_argv = actual_argv[2:]
    elif actual_argv[:1] == ["src.cli"]:
        actual_argv = actual_argv[1:]

    if actual_argv:
        return actual_argv

    try:
        return resolve_operator_start_args(prompt=_stderr_prompt, display=_stderr_display)
    except ValueError as error:
        if "cancelled by user" in str(error):
            _stderr_display("Отменено.")
            raise SystemExit(2)
        raise


def _run_cli_once(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION, epilog=CLI_EPILOG, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", nargs="?", choices=("solve", "figures", "report", "build", "deliver"), default="build", help="Pipeline step to run. Default launch starts the guided operator session inside the existing CLI.")
    parser.add_argument("--input", dest="input_path", nargs="?", const=INPUT_CHOOSER_SENTINEL, help="Path to the canonical raw-input file for `build`. Omit the value to choose from obvious YAML files inside the CLI; after validation failures the CLI offers retry / other YAML / starter YAML recovery.")
    parser.add_argument("--starter-yaml", dest="starter_yaml_path", nargs="?", const=STARTER_YAML_SENTINEL, help="Create a starter YAML template for `build`. Omit the value to choose where to save it inside the CLI.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for canonical raw-input fields interactively. Valid only with `build` and mutually exclusive with `--input`.")
    parser.add_argument("--review", action="store_true", help="Preview normalized raw input before `build`. Default confirmation is Enter; edit/cancel stay available via short keys.")
    parser.add_argument("--offer-delivery", action="store_true", help="After successful `build`, stay in the same session and choose the final result to create.")
    parser.add_argument("--json", action="store_true", help="Print raw JSON summary to stdout. Without this flag the CLI shows only human operator summaries.")
    parser.add_argument("--variant-path", default=str(DEFAULT_VARIANT_PATH), help="Raw-input artifact path. Default: inputs/variant_me.yaml")
    parser.add_argument("--derived-path", default=str(DEFAULT_DERIVED_PATH), help="Derived-parameters artifact path. Default: inputs/derived_parameters.json")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for solver JSON outputs. Default: out/data")
    parser.add_argument("--data-dir", default=str(DEFAULT_OUT_DIR), help="Directory with solver JSON inputs for `figures`, `report`, and the frozen guide baseline. Default: out/data")
    parser.add_argument("--figures-dir", default=str(DEFAULT_FIGURES_DIR), help="Directory for generated figure PNG files. Default: figures")
    parser.add_argument("--manifest-path", default=str(DEFAULT_FIGURE_MANIFEST_PATH), help="Figure manifest path. Default: out/artifacts/figure_manifest.json")
    parser.add_argument("--report-source-path", default=str(DEFAULT_REPORT_SOURCE_PATH), help="TeX report output path. Default: report/final_report.tex")
    parser.add_argument("--report-pdf-path", default=str(DEFAULT_REPORT_PDF_PATH), help="PDF report output path. Default: report/final_report.pdf")
    parser.add_argument("--report-year", type=int, default=DEFAULT_REPORT_YEAR, help=f"Explicit report year for low-level `report` builds. Default: {DEFAULT_REPORT_YEAR}")
    parser.add_argument("--report-scope", choices=REPORT_SCOPES, default=None, help="Report scope for `report` and report-bearing `deliver`: task1, task2, or full.")
    parser.add_argument("--report-assets-manifest-path", default=str(DEFAULT_REPORT_ASSETS_MANIFEST_PATH), help="Report assets manifest path. Default: report/assets_manifest.json")
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR), help="Per-run archive root for `build`. Default: runs")
    parser.add_argument("--deliveries-dir", default=str(DEFAULT_DELIVERIES_DIR), help="Delivery root for `deliver`. Default: deliveries")
    parser.add_argument("--delivery-profile", default=None, help="Delivery profile for `deliver`.")
    parser.add_argument("--output-format", default=None, help="Output format for `deliver`.")
    parser.add_argument(
        "--report-output-format",
        choices=("pdf", "docx", "pdf_docx"),
        default=None,
        help="Inner report format for study_pack bundle_dir: pdf, docx, or pdf_docx.",
    )
    parser.add_argument(
        "--guide-output-format",
        choices=("pdf", "docx", "pdf_docx"),
        default=None,
        help="Inner guide format for study_pack bundle_dir: pdf, docx, or pdf_docx.",
    )
    parser.add_argument("--guide-scope", choices=REPORT_SCOPES, default=None, help="Guide scope for `deliver`: task1, task2, or full.")
    parser.add_argument("--guide-mode", default=None, help="Guide mode for `deliver`: variant_aware or general.")
    parser.add_argument("--source-run-id", default=None, help="Successful run source for `deliver`.")
    parser.add_argument("--guide-source-path", default=str(DEFAULT_GUIDE_SOURCE_PATH), help="Guide baseline path for `deliver`.")
    parser.add_argument("--guide-general-source-path", default=str(DEFAULT_GUIDE_GENERAL_SOURCE_PATH), help="General-guide baseline path for `deliver`.")

    args = parser.parse_args(argv)
    _activate_default_build_mode(args)

    if args.command != "build" and args.review:
        parser.exit(2, "error: --review is valid only with `build`\\n")
    if args.command != "build" and args.offer_delivery:
        parser.exit(2, "error: --offer-delivery is valid only with `build`\\n")
    if args.command != "build" and args.starter_yaml_path is not None:
        parser.exit(2, "error: --starter-yaml is valid only with `build`\\n")

    try:
        if args.command == "solve":
            summary = run(
                variant_path=Path(args.variant_path),
                derived_path=Path(args.derived_path),
                out_dir=Path(args.out_dir),
            )
        elif args.command == "figures":
            summary = generate_figure_artifacts(
                data_dir=Path(args.data_dir),
                figures_dir=Path(args.figures_dir),
                manifest_path=Path(args.manifest_path),
            )
        elif args.command == "report":
            summary = build_report_package(
                variant_path=Path(args.variant_path),
                derived_path=Path(args.derived_path),
                data_dir=Path(args.data_dir),
                figure_manifest_path=Path(args.manifest_path),
                report_source_path=Path(args.report_source_path),
                report_pdf_path=Path(args.report_pdf_path),
                assets_manifest_path=Path(args.report_assets_manifest_path),
                report_year=args.report_year,
                report_scope=args.report_scope,
            )
        elif args.command == "build":
            if args.starter_yaml_path is not None:
                if args.interactive or args.input_path is not None:
                    parser.exit(2, "error: --starter-yaml cannot be combined with --interactive or --input\\n")
                starter_path = (
                    choose_starter_yaml_path(prompt=_stderr_prompt, display=_stderr_display)
                    if args.starter_yaml_path == STARTER_YAML_SENTINEL
                    else Path(args.starter_yaml_path)
                )
                write_starter_yaml(starter_path)
                summary = {"starter_yaml_path": str(starter_path)}
            elif args.interactive == (args.input_path is not None):
                parser.exit(2, "error: build requires exactly one of --interactive or --input\\n")
            else:
                summary = _build_summary_with_recovery(args)
        else:
            request = build_delivery_request(
                delivery_profile=args.delivery_profile,
                output_format=args.output_format,
                report_scope=args.report_scope,
                guide_scope=args.guide_scope,
                guide_mode=args.guide_mode,
                source_run_id=args.source_run_id,
                report_output_format=getattr(args, "report_output_format", None),
                guide_output_format=getattr(args, "guide_output_format", None),
            )
            summary = run_delivery(
                request=request,
                runs_dir=Path(args.runs_dir),
                deliveries_dir=Path(args.deliveries_dir),
                guide_source_path=Path(args.guide_source_path),
                general_guide_source_path=Path(args.guide_general_source_path),
                guide_derived_path=Path(args.derived_path),
                guide_data_dir=Path(args.data_dir),
                general_assets_manifest_path=Path(args.report_assets_manifest_path),
            )
    except ValueError as error:
        message = str(error)
        if "cancelled by user" in message:
            if args.json:
                print(json.dumps({"status": "cancelled", "error": message}, ensure_ascii=False, indent=2))
            else:
                _stderr_display("Отменено.")
            raise SystemExit(2)
        if message.startswith("starter YAML already exists:"):
            if args.json:
                print(json.dumps({"error": message}, ensure_ascii=False, indent=2))
            else:
                _stderr_display(message)
            raise SystemExit(2)
        human_error = format_input_validation_error(error) if args.command == "build" else None
        if human_error is not None:
            if args.json:
                print(
                    json.dumps(
                        {
                            "error": message,
                            "hint": human_error,
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
            else:
                _stderr_display(human_error)
        else:
            if args.json:
                print(json.dumps({"error": message}, ensure_ascii=False, indent=2))
            else:
                _stderr_display(f"error: {message}")
        raise SystemExit(2)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        rendered = cli_summary(args.command, summary, request if args.command == "deliver" else None)
        if rendered:
            _stderr_display(rendered)
    return 0


def _prompt_operator_followup_action() -> str:
    while True:
        _stderr_display(
            "\n".join(
                [
                    "Что дальше?",
                    "1. Новый заказ",
                    "2. Безопасный выход",
                ]
            )
        )
        raw = _stderr_prompt("Выбор [Enter=1, 1-2, x=2]: ").strip().lower()
        if raw in {"", "1"}:
            return "new_order"
        if raw in {"2", "x", "exit", "quit", "q", "выход", "в"}:
            return "exit"
        _stderr_display("Нажмите Enter, 1, 2 или x.")


def main(argv: list[str] | None = None) -> int:
    operator_entry = argv is None or argv == []

    if not operator_entry:
        resolved_argv = _resolve_operator_default_argv(argv)
        return _run_cli_once(resolved_argv)

    while True:
        resolved_argv = _resolve_operator_default_argv([])
        exit_code = _run_cli_once(resolved_argv)
        if _prompt_operator_followup_action() == "exit":
            _stderr_display("Сеанс завершён.")
            return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
