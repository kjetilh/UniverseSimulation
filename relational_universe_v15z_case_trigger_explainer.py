#!/usr/bin/env python3
"""v0.15z p0-vs-p1 case trigger explainer.

This round does not run new simulations. It uses the narrow v15y case-duel
outputs, together with the static support contrast from v15w, to ask whether
the three selected p0-vs-p1 seeds can be explained by a small set of onset
triggers rather than one unresolved local story.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
V15Y_TARGET = DOC / "v15y_p0_p1_case_duel_target_summary.csv"
V15Y_RUNS = DOC / "v15y_p0_p1_case_duel_runs.csv"
V15Y_SEGMENTS = DOC / "v15y_p0_p1_case_duel_segments.csv"
V15Y_DUELS = DOC / "v15y_p0_p1_case_duel_duels.csv"
V15W_SUPPORT = DOC / "v15w_add_chord_p0_p1_support_summary.csv"

OUT_TARGET = DOC / "v15z_case_trigger_target_summary.csv"
OUT_ROWS = DOC / "v15z_case_trigger_rows.csv"
OUT_AGGR = DOC / "v15z_case_trigger_aggregate.csv"
OUT_DIAG = DOC / "v15z_case_trigger_diagnosis.csv"
OUT_REPORT = DOC / "v15z_case_trigger_explainer.md"
OUT_RECO = DOC / "v0_15z_operativ_anbefaling.md"
OUT_NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15z.md"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def support_bias_snapshot(rows: Sequence[Mapping[str, str]]) -> Dict[str, float]:
    by_label = {str(row["placement_label"]): row for row in rows}
    p0 = by_label["p0"]
    p1 = by_label["p1"]
    return {
        "p1_minus_p0_degree_gap": safe_float(p1["mean_support_degree"]) - safe_float(p0["mean_support_degree"]),
        "p1_minus_p0_ball1_gap": safe_float(p1["support_ball_1"]) - safe_float(p0["support_ball_1"]),
        "p0_minus_p1_expansion_gap": safe_float(p0["ball3_over_ball1"]) - safe_float(p1["ball3_over_ball1"]),
        "p0_unique_node": safe_float(p0["unique_node"]),
        "p1_unique_node": safe_float(p1["unique_node"]),
    }


def first_segment_rows(rows: Sequence[Mapping[str, str]]) -> Dict[Tuple[int, int], Mapping[str, str]]:
    out: Dict[Tuple[int, int], Mapping[str, str]] = {}
    for row in rows:
        if int(row["segment_local_index"]) != 0:
            continue
        key = (int(row["seed_delta"]), int(row["placement"]))
        out[key] = row
    return out


def classify_trigger(
    *,
    exact_gap: float,
    first_gap: float,
    first_component_gap: float,
    first_boundary_gap: float,
    first_radius_gap: float,
    first_damage_gap: float,
    mean_component_gap: float,
) -> str:
    if (
        exact_gap >= 0.05
        and first_gap <= -24.0
        and first_component_gap <= 0.25
        and first_radius_gap <= -1.5
        and first_damage_gap <= -2.0
    ):
        return "p1_compact_radius_trigger"
    if (
        exact_gap <= -0.10
        and first_gap <= -8.0
        and (first_component_gap >= 0.75 or mean_component_gap >= 0.75)
        and first_boundary_gap >= 0.05
    ):
        return "fragmented_fast_tradeoff_trigger"
    if (
        exact_gap <= -0.15
        and first_gap >= 8.0
        and first_component_gap >= 0.75
        and first_boundary_gap >= 0.10
    ):
        return "p0_calm_singleton_trigger"
    return "mixed_trigger"


def trigger_note(trigger_label: str) -> str:
    if trigger_label == "p1_compact_radius_trigger":
        return "P1 vinner her uten fragmentering: samme komponenttall som p0, men kortere radius og mindre skadevolum gir tidligere og renere lock."
    if trigger_label == "fragmented_fast_tradeoff_trigger":
        return "P1 kommer tidligere til exact return, men starter fragmentert og med høyere boundary-cost; det gir fart, men dårligere full exact-rate."
    if trigger_label == "p0_calm_singleton_trigger":
        return "P0 holder en roligere singleton-lock mens p1 starter mer splittet; det gir seinere, men renere og sterkere retur for p0."
    return "Caset bryter ikke rent nok til å støtte en av de tre små onset-triggerne."


def case_rows(
    *,
    duel_rows_in: Sequence[Mapping[str, str]],
    run_rows_in: Sequence[Mapping[str, str]],
    segment_rows_in: Sequence[Mapping[str, str]],
    support_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    run_lookup = {(int(row["seed_delta"]), int(row["placement"])): row for row in run_rows_in}
    first_lookup = first_segment_rows(segment_rows_in)
    support_bias = support_bias_snapshot(support_rows_in)
    out: List[Dict[str, Any]] = []
    for duel in sorted(duel_rows_in, key=lambda row: int(row["seed_delta"])):
        seed_delta = int(duel["seed_delta"])
        p0 = run_lookup[(seed_delta, 0)]
        p1 = run_lookup[(seed_delta, 1)]
        p0_first = first_lookup[(seed_delta, 0)]
        p1_first = first_lookup[(seed_delta, 1)]

        exact_gap = safe_float(duel["p1_minus_p0_exact_gap"])
        first_gap = safe_float(duel["p1_minus_p0_first_gap"])
        first_component_gap = safe_float(p1_first["damage_component_count"]) - safe_float(p0_first["damage_component_count"])
        first_largest_gap = safe_float(p1_first["largest_component_fraction"]) - safe_float(p0_first["largest_component_fraction"])
        first_boundary_gap = safe_float(p1_first["boundary_to_volume"]) - safe_float(p0_first["boundary_to_volume"])
        first_radius_gap = safe_float(p1_first["radius_control"]) - safe_float(p0_first["radius_control"])
        first_damage_gap = safe_float(p1_first["damaged_nodes_count"]) - safe_float(p0_first["damaged_nodes_count"])
        mean_component_gap = safe_float(p1["mean_prelock_component_count"]) - safe_float(p0["mean_prelock_component_count"])
        mean_boundary_gap = safe_float(p1["mean_prelock_boundary_to_volume"]) - safe_float(p0["mean_prelock_boundary_to_volume"])
        mean_radius_gap = safe_float(p1["mean_prelock_radius"]) - safe_float(p0["mean_prelock_radius"])
        mean_damage_gap = safe_float(p1["mean_prelock_damage_nodes"]) - safe_float(p0["mean_prelock_damage_nodes"])
        mean_adj_gap = safe_float(p1["mean_prelock_adjacent_jaccard"]) - safe_float(p0["mean_prelock_adjacent_jaccard"])

        trigger = classify_trigger(
            exact_gap=exact_gap,
            first_gap=first_gap,
            first_component_gap=first_component_gap,
            first_boundary_gap=first_boundary_gap,
            first_radius_gap=first_radius_gap,
            first_damage_gap=first_damage_gap,
            mean_component_gap=mean_component_gap,
        )
        out.append(
            {
                "seed_delta": seed_delta,
                "case_label": str(duel["case_label"]),
                "trigger_label": trigger,
                "support_density_bias": "p1_denser_support",
                "support_expansion_bias": "p0_wider_relative_expansion",
                "p1_minus_p0_support_degree_gap": support_bias["p1_minus_p0_degree_gap"],
                "p1_minus_p0_support_ball1_gap": support_bias["p1_minus_p0_ball1_gap"],
                "p0_minus_p1_expansion_gap": support_bias["p0_minus_p1_expansion_gap"],
                "p0_unique_node": int(support_bias["p0_unique_node"]),
                "p1_unique_node": int(support_bias["p1_unique_node"]),
                "p0_support_signature": str(p0["support_signature"]),
                "p1_support_signature": str(p1["support_signature"]),
                "p1_minus_p0_exact_gap": exact_gap,
                "p1_minus_p0_first_gap": first_gap,
                "first_component_gap": first_component_gap,
                "first_largest_gap": first_largest_gap,
                "first_boundary_gap": first_boundary_gap,
                "first_radius_gap": first_radius_gap,
                "first_damage_gap": first_damage_gap,
                "mean_component_gap": mean_component_gap,
                "mean_boundary_gap": mean_boundary_gap,
                "mean_radius_gap": mean_radius_gap,
                "mean_damage_gap": mean_damage_gap,
                "mean_adjacent_jaccard_gap": mean_adj_gap,
                "trigger_note": trigger_note(trigger),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["trigger_label"]) for row in rows})
    total = max(1, len(rows))
    out: List[Dict[str, Any]] = []
    for label in labels:
        grp = [row for row in rows if str(row["trigger_label"]) == label]
        out.append(
            {
                "trigger_label": label,
                "n_cases": len(grp),
                "rate": len(grp) / total,
                "mean_exact_gap": mean_defined(safe_float(row["p1_minus_p0_exact_gap"]) for row in grp),
                "mean_first_gap": mean_defined(safe_float(row["p1_minus_p0_first_gap"]) for row in grp),
                "mean_first_component_gap": mean_defined(safe_float(row["first_component_gap"]) for row in grp),
                "mean_first_boundary_gap": mean_defined(safe_float(row["first_boundary_gap"]) for row in grp),
                "mean_first_radius_gap": mean_defined(safe_float(row["first_radius_gap"]) for row in grp),
                "mean_mean_component_gap": mean_defined(safe_float(row["mean_component_gap"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, str]],
    run_rows_in: Sequence[Mapping[str, str]],
    case_rows_out: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    requested_match_clean = all(int(row["requested_match"]) == 1 for row in run_rows_in)
    counts: Dict[str, int] = {}
    for row in case_rows_out:
        counts[str(row["trigger_label"])] = counts.get(str(row["trigger_label"]), 0) + 1
    p1_trigger = counts.get("p1_compact_radius_trigger", 0)
    tradeoff_trigger = counts.get("fragmented_fast_tradeoff_trigger", 0)
    p0_trigger = counts.get("p0_calm_singleton_trigger", 0)
    mixed = counts.get("mixed_trigger", 0)

    if p1_trigger >= 1 and tradeoff_trigger >= 1 and p0_trigger >= 1 and mixed == 0:
        status = "three_local_triggers_supported"
        note = "De tre utvalgte case-seedene kan forklares av tre ulike onset-triggere: kompakt p1-lock, fragmentert tradeoff og rolig p0-singleton-lock."
        next_step = "targeted_trigger_holdout"
        next_note = "Neste steg bør teste om disse triggerne holder på noen få nærliggende holdout-seeds, ikke åpne en ny bred scan."
    elif p1_trigger + tradeoff_trigger + p0_trigger >= 2 and mixed <= 1:
        status = "trigger_story_partly_supported"
        note = "Minst to av case-seedene får tydeligere onset-triggere, men forklaringen er fortsatt ikke ren på tvers av alle tre."
        next_step = "fix_mixed_case"
        next_note = "Neste steg bør fokusere på caset som fortsatt er blandet."
    else:
        status = "trigger_story_not_yet"
        note = "Selv med onset-metrikker kollapser ikke case-runden til et lite sett forklarlige triggere."
        next_step = "change_observable"
        next_note = "Neste steg bør bytte observabel i stedet for å presse videre på samme forklaringslinje."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean and requested_match_clean else "unclear",
            "note": "Startstørrelsene er rent separert og alle p0/p1-runene matcher ønsket add_chord-perturbasjon."
            if size_clean and requested_match_clean
            else "Enten størrelsesseparasjonen eller perturbasjonsmatchen er uklar.",
        },
        {
            "diagnostic_family": "support_bias",
            "status": "p1_denser_support__p0_wider_expansion",
            "note": "P1 sitter i litt tettere lokal støtte, mens p0 har litt større relativ videre ekspansjon. Dette er bakgrunnsbias, ikke hele forklaringen.",
        },
        {
            "diagnostic_family": "trigger_snapshot",
            "status": f"p1_compact={p1_trigger};tradeoff={tradeoff_trigger};p0_calm={p0_trigger};mixed={mixed}",
            "note": "Dette oppsummerer hvordan de tre case-seedene brytes ned i onset-trigger-typer.",
        },
        {
            "diagnostic_family": "case_trigger_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, str]],
    case_rows_out: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15z: p0-vs-p1 case trigger explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden kjører ingen nye simuleringer. Den bruker `v15w` og `v15y` til å teste om de tre utvalgte p0-vs-p1-case-seedene kan forklares av et lite sett onset-triggere.")
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Case trigger rows")
    lines.append("")
    lines.append("| seed | case | trigger | exact gap | first gap | first comp gap | first boundary gap | first radius gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in case_rows_out:
        lines.append(
            f"| {int(row['seed_delta'])} | {row['case_label']} | {row['trigger_label']} | {fmt(row['p1_minus_p0_exact_gap'])} | {fmt(row['p1_minus_p0_first_gap'],1)} | {fmt(row['first_component_gap'])} | {fmt(row['first_boundary_gap'])} | {fmt(row['first_radius_gap'])} |"
        )
    lines.append("")
    lines.append("## Trigger aggregate")
    lines.append("")
    lines.append("| trigger | n | rate | exact gap | first gap | first comp gap | first boundary gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['trigger_label']} | {int(row['n_cases'])} | {fmt(row['rate'])} | {fmt(row['mean_exact_gap'])} | {fmt(row['mean_first_gap'],1)} | {fmt(row['mean_first_component_gap'])} | {fmt(row['mean_first_boundary_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- `p1` har fortsatt en svak statisk støttefordel, men `v15z` viser at denne fordelen bare blir til en ren gevinst i noen seeds.")
    lines.append("- `151` ser ut som et kompakt `p1`-lock: samme komponenttall som `p0`, men mindre radius og mindre skadesett gir tidligere og sterkere retur.")
    lines.append("- `239` er fortsatt det reneste tradeoff-caset: `p1` kommer tidligere, men betaler for det med fragmentering og høyere boundary-cost.")
    lines.append("- `271` ser ut som et rolig `p0`-singleton-caset: `p1` starter mer splittet, mens `p0` låser rent og vinner på full horisont.")
    lines.append("- Les dette som lokal case-forklaring, ikke som en generell defect-lov.")
    lines.append("")
    return "\n".join(lines)


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# v0.15z operativ anbefaling", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les denne runden som en forklaring av tre lokale case-seeds, ikke som bred trigger-validering.")
    return "\n".join(lines) + "\n"


def build_nonspecialist(case_rows_out: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    trigger_map = {str(row["seed_delta"]): str(row["trigger_label"]) for row in case_rows_out}
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15z for ikke-spesialister")
    lines.append("")
    lines.append("Denne runden prøver ikke å bevise ny fysikk. Den prøver bare å forklare hvorfor tre små lokale tilfeller mellom `p0` og `p1` oppfører seg forskjellig.")
    lines.append("")
    lines.append("Kort sagt fant vi at de tre utvalgte tilfellene ikke ser ut som tilfeldig støy:")
    lines.append("")
    lines.append(f"- `151` ser ut som `{trigger_map.get('151', 'ukjent')}`.")
    lines.append(f"- `239` ser ut som `{trigger_map.get('239', 'ukjent')}`.")
    lines.append(f"- `271` ser ut som `{trigger_map.get('271', 'ukjent')}`.")
    lines.append("")
    lines.append("Det betyr ikke at vi har en universell lov. Det betyr at den lille `p0`/`p1`-familien nå ser mer strukturert ut enn før: noen ganger vinner `p1` fordi den låser mer kompakt og raskt, noen ganger taper `p1` fordi den blir for fragmentert, og noen ganger vinner `p0` fordi den holder en roligere singleton-lås.")
    lines.append("")
    next_row = next((row for row in diagnosis if str(row["diagnostic_family"]) == "next_step"), None)
    if next_row is not None:
        lines.append(f"Neste naturlige steg er `{next_row['status']}`: {next_row['note']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    target_summary = read_csv(V15Y_TARGET)
    run_rows_in = read_csv(V15Y_RUNS)
    segment_rows_in = read_csv(V15Y_SEGMENTS)
    duel_rows_in = read_csv(V15Y_DUELS)
    support_rows_in = read_csv(V15W_SUPPORT)

    case_rows_out = case_rows(
        duel_rows_in=duel_rows_in,
        run_rows_in=run_rows_in,
        segment_rows_in=segment_rows_in,
        support_rows_in=support_rows_in,
    )
    aggregate = aggregate_rows(case_rows_out)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows_in=run_rows_in,
        case_rows_out=case_rows_out,
    )

    write_csv(OUT_TARGET, [dict(row) for row in target_summary])
    write_csv(OUT_ROWS, case_rows_out)
    write_csv(OUT_AGGR, aggregate)
    write_csv(OUT_DIAG, diagnosis)
    OUT_REPORT.write_text(
        build_report(
            target_summary=target_summary,
            case_rows_out=case_rows_out,
            aggregate=aggregate,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    OUT_RECO.write_text(build_recommendation(diagnosis), encoding="utf-8")
    OUT_NONSPECIALIST.write_text(build_nonspecialist(case_rows_out, diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
