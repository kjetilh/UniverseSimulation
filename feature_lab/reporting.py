"""Markdown reporting helpers for the feature lab."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .analysis import AnalysisReport, DriftStat, ScaleStat, SVDCandidate, SVDResult


@dataclass(frozen=True)
class SimulationReportMetadata:
    """Metadata for a simulation run report."""

    title: str
    parameters: tuple[tuple[str, object], ...]
    trajectory_csv: str


def markdown_table(rows: Sequence[Sequence[str]]) -> str:
    """Render a GitHub-flavored Markdown table."""
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    separator = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join([header, separator, body])


def _format_candidate(candidate: SVDCandidate) -> str:
    if not candidate.coefficients:
        return "(sparse near-zero)"
    terms = []
    for feature, coef in candidate.coefficients:
        basis_name = f"z({feature})" if candidate.standardized else feature
        terms.append(f"{coef:+.4f}·{basis_name}")
    return " ".join(terms)


def _scale_rows(scale_stats: Sequence[ScaleStat]) -> list[list[str]]:
    rows = [["feature", "mean", "std", "min", "max"]]
    for stat in scale_stats:
        rows.append(
            [
                stat.feature,
                f"{stat.mean:.6g}",
                f"{stat.std:.6g}",
                f"{stat.minimum:.6g}",
                f"{stat.maximum:.6g}",
            ]
        )
    return rows


def _drift_rows(drift_stats: Sequence[DriftStat]) -> list[list[str]]:
    rows = [["feature", "slope", "mean", "std", "rel_slope_per_mean"]]
    for stat in drift_stats:
        rows.append(
            [
                stat.feature,
                f"{stat.slope:.6g}",
                f"{stat.mean:.6g}",
                f"{stat.std:.6g}",
                f"{stat.rel_slope_per_mean:.6g}",
            ]
        )
    return rows


def _svd_table(result: SVDResult) -> str:
    rows = [["rank", "type", "combinasjon", "increment_var", "time_slope"]]
    for candidate in result.candidates:
        rows.append(
            [
                str(candidate.rank),
                result.matrix_label,
                _format_candidate(candidate),
                f"{candidate.increment_variance:.6g}",
                f"{candidate.time_slope:.6g}",
            ]
        )
    return markdown_table(rows)


def render_analysis_report(report: AnalysisReport) -> str:
    """Render a standalone Markdown analysis report."""
    lines = [
        "# Feature-lab analyse",
        "",
        f"- source_csv: `{report.source_csv}`",
        f"- feature_basis: `{report.feature_basis}`",
        f"- analysis_mode: `{report.analysis_mode}`",
        f"- row_count: {report.summary.row_count}",
        f"- t_start: {report.summary.t_start:.6g}",
        f"- t_end: {report.summary.t_end:.6g}",
        "",
        "## Feature-set",
        "",
        ", ".join(report.feature_names),
        "",
        "## Algebraiske identiteter og konstante features",
        "",
        f"- constant_features: {', '.join(report.summary.constant_features) if report.summary.constant_features else '(ingen)'}",
    ]
    for name, value in sorted(report.summary.identity_max_abs.items()):
        lines.append(f"- max_abs_{name}: {value:.6g}")

    if report.notes:
        lines.extend(["", "## Analysemerknader", ""])
        lines.extend(f"- {note}" for note in report.notes)

    if report.scale_stats:
        lines.extend(["", "## Skalaeffekter", ""])
        lines.append(
            "Rå analyse vektlegger store absolutte skalaer, mens standardisert analyse bruker z-skårte features for å teste robusthet mot slike skalaeffekter."
        )
        lines.extend(["", markdown_table(_scale_rows(report.scale_stats))])

    if report.svd_results:
        lines.extend(["", "## Singularverdier", ""])
        singular_rows = [["matrix", "singular_values"]]
        for result in report.svd_results:
            singular_rows.append([result.matrix_label, ", ".join(f"{value:.4g}" for value in result.singular_values)])
        lines.append(markdown_table(singular_rows))
        for result in report.svd_results:
            lines.extend(["", _svd_table(result)])

    if report.drift_stats:
        lines.extend(["", "## Enkel drift per feature", "", markdown_table(_drift_rows(report.drift_stats))])

    lines.extend(
        [
            "",
            "## Tolkning",
            "",
            "Lineære kombinasjoner med liten increment_var og liten time_slope er kandidater til quasi-invarianter i det valgte feature-rommet.",
            "De må fortsatt skilles fra rene algebraiske identiteter og fra artefakter som bare oppstår på grunn av ulik feature-skala.",
        ]
    )
    return "\n".join(lines)


def render_simulation_report(
    metadata: SimulationReportMetadata,
    analysis_report: AnalysisReport | None,
) -> str:
    """Render a run report that embeds optional analysis output."""
    lines = [
        f"# {metadata.title}",
        "",
        "## Parametre",
        "",
    ]
    for key, value in metadata.parameters:
        lines.append(f"- {key}: {value}")
    lines.extend(["", f"- trajectory_csv: `{metadata.trajectory_csv}`", ""])
    if analysis_report is None:
        lines.append("Ingen analyse ble kjørt for denne kjøringen.")
    else:
        lines.append(render_analysis_report(analysis_report))
    return "\n".join(lines)


def render_analyze_only_example(command: str, input_csv: str, output_md: str) -> str:
    """Render a short note documenting an analyze-only invocation."""
    return "\n".join(
        [
            "# Analyze-only Example",
            "",
            "Denne kjøringen bruker eksisterende CSV som input og hopper over ny simulering.",
            "",
            f"- input_csv: `{input_csv}`",
            f"- output_md: `{output_md}`",
            "",
            "## Kommando",
            "",
            "```bash",
            command,
            "```",
            "",
            "Denne modusen er nyttig når man vil sammenligne rå og standardisert quasi-invariantanalyse på allerede genererte regimer.",
        ]
    )
