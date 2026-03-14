"""CLI entrypoint for the refactored feature lab."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import random
from typing import Sequence

from .analysis import AnalysisReport, analyze_csv
from .features import FULL_FEATURE_ORDER, feature_row, resolve_feature_names
from .graph_core import bootstrap
from .reporting import SimulationReportMetadata, render_analysis_report, render_simulation_report
from .rules import FeatureLabSimulator, SimulationParameters


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for simulation and analyze-only modes."""
    parser = argparse.ArgumentParser(description="Relational-universe feature lab.")
    parser.add_argument("--mode", choices=("simulate", "analyze"), default="simulate")

    parser.add_argument("--steps", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--initial-cycle", type=int, default=6)
    parser.add_argument("--initial-tokens", type=int, default=4)
    parser.add_argument("--r-seed", type=float, default=0.05)
    parser.add_argument("--r-token", type=float, default=1.0)
    parser.add_argument("--r-birth", type=float, default=0.0)
    parser.add_argument("--r-death", type=float, default=0.0)
    parser.add_argument("--p-triad", type=float, default=0.08)
    parser.add_argument("--p-del", type=float, default=0.04)
    parser.add_argument("--p-swap", type=float, default=0.06)
    parser.add_argument("--avoid-disconnect", action="store_true", default=False)
    parser.add_argument("--relocate-tokens", action="store_true", default=False)
    parser.add_argument("--log-every", type=int, default=1000)
    parser.add_argument("--out", type=str, default="feature_trajectory.csv")

    parser.add_argument("--summary-md", type=str, default="")
    parser.add_argument("--analyze", action="store_true", default=False)
    parser.add_argument("--input-csv", type=str, default="")
    parser.add_argument("--analysis-mode", choices=("raw", "standardized", "both"), default="both")
    parser.add_argument("--feature-basis", choices=("full", "reduced"), default="full")
    parser.add_argument(
        "--analyze-features",
        type=str,
        default="",
        help="Comma-separated feature list. Empty means the default basis.",
    )
    parser.add_argument("--top-k", type=int, default=3)
    return parser


def _run_analysis(
    csv_path: str,
    summary_md: str,
    feature_basis: str,
    analyze_features: str,
    analysis_mode: str,
    top_k: int,
) -> AnalysisReport:
    feature_names = resolve_feature_names(feature_basis, analyze_features or None)
    report = analyze_csv(
        csv_path=csv_path,
        feature_names=feature_names,
        feature_basis=feature_basis,
        analysis_mode=analysis_mode,
        top_k=top_k,
    )
    Path(summary_md).write_text(render_analysis_report(report), encoding="utf-8")
    return report


def _emit_trajectory(writer: csv.DictWriter[str], step_idx: int, event_name: str, state) -> None:
    row = feature_row(state, FULL_FEATURE_ORDER)
    payload = {"event": event_name, "step": step_idx}
    payload.update(row)
    writer.writerow(payload)


def run_simulation(args: argparse.Namespace) -> None:
    """Run a new simulation and optionally analyze the resulting CSV."""
    rng = random.Random(args.seed)
    state = bootstrap(args.initial_cycle, args.initial_tokens, rng)
    params = SimulationParameters(
        r_seed=args.r_seed,
        r_token=args.r_token,
        r_birth=args.r_birth,
        r_death=args.r_death,
        p_triad=args.p_triad,
        p_del=args.p_del,
        p_swap=args.p_swap,
        avoid_disconnect=args.avoid_disconnect,
        relocate_tokens=args.relocate_tokens,
    )
    simulator = FeatureLabSimulator(params=params)

    out_path = Path(args.out)
    fieldnames = ["event", "step", "t", *FULL_FEATURE_ORDER]
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        _emit_trajectory(writer, 0, "init", state)
        for step_idx in range(1, args.steps + 1):
            event = simulator.step(state, rng)
            if step_idx % args.log_every == 0 or step_idx == args.steps:
                _emit_trajectory(writer, step_idx, event.event_name, state)

    report: AnalysisReport | None = None
    summary_md = args.summary_md.strip()
    if args.analyze:
        if not summary_md:
            summary_md = str(out_path.with_suffix(".md"))
        report = _run_analysis(
            csv_path=str(out_path),
            summary_md=summary_md,
            feature_basis=args.feature_basis,
            analyze_features=args.analyze_features.strip(),
            analysis_mode=args.analysis_mode,
            top_k=args.top_k,
        )
    elif summary_md:
        metadata = SimulationReportMetadata(
            title="Feature-lab kjøringsrapport",
            parameters=(
                ("steps", args.steps),
                ("seed", args.seed),
                ("initial_cycle", args.initial_cycle),
                ("initial_tokens", args.initial_tokens),
                ("r_seed", args.r_seed),
                ("r_token", args.r_token),
                ("r_birth", args.r_birth),
                ("r_death", args.r_death),
                ("p_triad", args.p_triad),
                ("p_del", args.p_del),
                ("p_swap", args.p_swap),
                ("avoid_disconnect", args.avoid_disconnect),
                ("relocate_tokens", args.relocate_tokens),
                ("log_every", args.log_every),
            ),
            trajectory_csv=str(out_path),
        )
        Path(summary_md).write_text(render_simulation_report(metadata, None), encoding="utf-8")

    if args.analyze and summary_md:
        metadata = SimulationReportMetadata(
            title="Feature-lab kjøringsrapport",
            parameters=(
                ("steps", args.steps),
                ("seed", args.seed),
                ("initial_cycle", args.initial_cycle),
                ("initial_tokens", args.initial_tokens),
                ("r_seed", args.r_seed),
                ("r_token", args.r_token),
                ("r_birth", args.r_birth),
                ("r_death", args.r_death),
                ("p_triad", args.p_triad),
                ("p_del", args.p_del),
                ("p_swap", args.p_swap),
                ("avoid_disconnect", args.avoid_disconnect),
                ("relocate_tokens", args.relocate_tokens),
                ("log_every", args.log_every),
                ("feature_basis", args.feature_basis),
                ("analysis_mode", args.analysis_mode),
            ),
            trajectory_csv=str(out_path),
        )
        Path(summary_md).write_text(render_simulation_report(metadata, report), encoding="utf-8")


def run_analysis_only(args: argparse.Namespace) -> None:
    """Analyze an existing CSV without running a new simulation."""
    if not args.input_csv.strip():
        raise SystemExit("--input-csv er påkrevd i analyze-modus")
    summary_md = args.summary_md.strip()
    if not summary_md:
        summary_md = str(Path(args.input_csv).with_name(Path(args.input_csv).stem + "_analysis.md"))
    _run_analysis(
        csv_path=args.input_csv,
        summary_md=summary_md,
        feature_basis=args.feature_basis,
        analyze_features=args.analyze_features.strip(),
        analysis_mode=args.analysis_mode,
        top_k=args.top_k,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""
    args = build_parser().parse_args(argv)
    if args.mode == "analyze":
        run_analysis_only(args)
        return 0
    run_simulation(args)
    return 0
