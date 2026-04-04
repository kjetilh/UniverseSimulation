#!/usr/bin/env python3
"""v0.15w add_chord p0-vs-p1 support contrast.

This round does not run a new family scan. It uses the existing v15v triplet
mechanism outputs plus local base-graph geometry to test a small explanatory
hypothesis:

does the remaining p0-vs-p1 ambiguity look like a speed-vs-stability tradeoff
that is at least partly aligned with their support geometry?
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15


TARGET = 48
GROWTH_SEED = 202
P0_SUPPORT = (5, 6, 8)
P1_SUPPORT = (6, 8, 10)
V15V_RUNS = "Documentation/v15v_add_chord_triplet_mechanism_runs.csv"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def singleton_geometry(base_state: Any, node: int) -> Dict[str, float]:
    ball_shell = v14c.ball_and_shell_counts(base_state.g, [node], r_max=3)
    return {
        "node_degree": float(base_state.g.degree(node)),
        "node_ball_1": float(ball_shell["support_ball_1"]),
        "node_ball_2": float(ball_shell["support_ball_2"]),
        "node_ball_3": float(ball_shell["support_ball_3"]),
    }


def support_rows(base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    common_support = sorted(set(P0_SUPPORT).intersection(P1_SUPPORT))
    common_geom = v14c.support_geometry_features(base_state, common_support)
    for label, support, unique_node in (
        ("p0", P0_SUPPORT, 5),
        ("p1", P1_SUPPORT, 10),
    ):
        geom = v14c.support_geometry_features(base_state, support)
        uniq = singleton_geometry(base_state, unique_node)
        rows.append(
            {
                "placement_label": label,
                "support_signature": ",".join(str(x) for x in support),
                "unique_node": int(unique_node),
                "mean_support_degree": safe_float(geom["mean_support_degree"]),
                "support_ball_1": safe_float(geom["support_ball_1"]),
                "support_ball_2": safe_float(geom["support_ball_2"]),
                "support_ball_3": safe_float(geom["support_ball_3"]),
                "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
                "ball3_over_ball1": safe_float(geom["ball3_over_ball1"]),
                "unique_node_degree": safe_float(uniq["node_degree"]),
                "unique_node_ball_1": safe_float(uniq["node_ball_1"]),
                "unique_node_ball_2": safe_float(uniq["node_ball_2"]),
                "unique_node_ball_3": safe_float(uniq["node_ball_3"]),
                "common_support_signature": ",".join(str(x) for x in common_support),
                "common_mean_support_degree": safe_float(common_geom["mean_support_degree"]),
            }
        )
    return rows


def duel_label(
    *,
    first_gap: float,
    switch_gap: float,
    exact_gap: float,
    lock_gap: float,
) -> str:
    p1_earlier = first_gap <= -8.0
    p0_earlier = first_gap >= 8.0
    p1_calmer = switch_gap <= -2.0
    p0_calmer = switch_gap >= 2.0
    p1_stronger = exact_gap >= 0.03 and lock_gap >= 0.03
    p0_stronger = exact_gap <= -0.03 and lock_gap <= -0.03
    if p1_earlier and p1_calmer and p1_stronger:
        return "p1_clean_advantage"
    if p1_earlier and p0_calmer:
        return "speed_stability_tradeoff"
    if (not p1_earlier and not p0_earlier) and p0_calmer and p0_stronger:
        return "p0_calm_advantage"
    if (not p1_earlier and not p0_earlier) and p1_calmer and p1_stronger:
        return "p1_calm_advantage"
    if p0_earlier and p0_calmer and p0_stronger:
        return "p0_clean_advantage"
    return "mixed_duel"


def duel_rows(v15v_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_delta: Dict[int, Dict[int, Mapping[str, str]]] = {}
    for row in v15v_rows:
        placement = int(row["placement"])
        if placement not in {0, 1}:
            continue
        by_delta.setdefault(int(row["seed_delta"]), {})[placement] = row
    for seed_delta in sorted(by_delta):
        pair = by_delta[seed_delta]
        if set(pair) != {0, 1}:
            continue
        p0 = pair[0]
        p1 = pair[1]
        exact_gap = safe_float(p1["full_exact_return_rate"]) - safe_float(p0["full_exact_return_rate"])
        lock_gap = safe_float(p1["exact_lock_fraction"]) - safe_float(p0["exact_lock_fraction"])
        first_gap = safe_float(p1["first_exact_return_step"]) - safe_float(p0["first_exact_return_step"])
        switch_gap = safe_float(p1["exact_switch_count"]) - safe_float(p0["exact_switch_count"])
        out.append(
            {
                "seed_delta": int(seed_delta),
                "p0_mechanism": str(p0["tail_lock_mechanism"]),
                "p1_mechanism": str(p1["tail_lock_mechanism"]),
                "p0_full_exact_return_rate": safe_float(p0["full_exact_return_rate"]),
                "p1_full_exact_return_rate": safe_float(p1["full_exact_return_rate"]),
                "p1_minus_p0_exact_gap": exact_gap,
                "p0_first_exact_return_step": safe_float(p0["first_exact_return_step"]),
                "p1_first_exact_return_step": safe_float(p1["first_exact_return_step"]),
                "p1_minus_p0_first_exact_gap": first_gap,
                "p0_exact_lock_fraction": safe_float(p0["exact_lock_fraction"]),
                "p1_exact_lock_fraction": safe_float(p1["exact_lock_fraction"]),
                "p1_minus_p0_lock_gap": lock_gap,
                "p0_exact_switch_count": safe_float(p0["exact_switch_count"]),
                "p1_exact_switch_count": safe_float(p1["exact_switch_count"]),
                "p1_minus_p0_switch_gap": switch_gap,
                "duel_label": duel_label(
                    first_gap=first_gap,
                    switch_gap=switch_gap,
                    exact_gap=exact_gap,
                    lock_gap=lock_gap,
                ),
            }
        )
    return out


def duel_aggregate(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["duel_label"]) for row in rows})
    total = max(1, len(rows))
    out: List[Dict[str, Any]] = []
    for label in labels:
        grp = [row for row in rows if str(row["duel_label"]) == label]
        out.append(
            {
                "duel_label": label,
                "n_duels": len(grp),
                "rate": len(grp) / total,
                "mean_p1_minus_p0_exact_gap": mean_defined(safe_float(row["p1_minus_p0_exact_gap"]) for row in grp),
                "mean_p1_minus_p0_first_exact_gap": mean_defined(safe_float(row["p1_minus_p0_first_exact_gap"]) for row in grp),
                "mean_p1_minus_p0_lock_gap": mean_defined(safe_float(row["p1_minus_p0_lock_gap"]) for row in grp),
                "mean_p1_minus_p0_switch_gap": mean_defined(safe_float(row["p1_minus_p0_switch_gap"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], support_summary: Sequence[Dict[str, Any]], duel_rows_out: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    duel_total = max(1, len(duel_rows_out))
    counts: Dict[str, int] = {}
    for row in duel_rows_out:
        counts[str(row["duel_label"])] = counts.get(str(row["duel_label"]), 0) + 1
    tradeoff_rate = counts.get("speed_stability_tradeoff", 0) / duel_total
    p0_calm_rate = counts.get("p0_calm_advantage", 0) / duel_total
    p1_clean_rate = counts.get("p1_clean_advantage", 0) / duel_total
    p0 = next(row for row in support_summary if str(row["placement_label"]) == "p0")
    p1 = next(row for row in support_summary if str(row["placement_label"]) == "p1")
    degree_gap = safe_float(p1["mean_support_degree"]) - safe_float(p0["mean_support_degree"])
    ball1_gap = safe_float(p1["support_ball_1"]) - safe_float(p0["support_ball_1"])
    expansion_gap = safe_float(p1["ball3_over_ball1"]) - safe_float(p0["ball3_over_ball1"])

    if tradeoff_rate >= 0.30 and degree_gap > 0 and ball1_gap > 0 and expansion_gap < 0:
        status = "timing_stability_tradeoff_supported"
        note = "P1 sitter i en litt tettere lokal støtte, men duellene viser fortsatt en gjentatt tradeoff mellom tidligere retur og roligere lock."
        next_step = "inspect_unique_node_swap"
        next_note = "Neste steg bør sammenligne den unike noden i p0 mot den unike noden i p1 direkte, siden de to støttene ellers overlapper sterkt."
    elif p1_clean_rate >= 0.50:
        status = "p1_support_advantage"
        note = "Duellene peker oftere rent i p1-retning enn mot en ekte tradeoff."
        next_step = "explain_p1_edge"
        next_note = "Neste steg bør forklare hvorfor p1-støtten faktisk gir renere fordel enn p0."
    elif p0_calm_rate >= 0.30 and degree_gap > 0:
        status = "p0_calm_counterweight"
        note = "P1 ser lokalt tettere ut geometrisk, men p0 kompenserer ofte med roligere og mer stabil lock i tailen."
        next_step = "focus_on_tail_quietness"
        next_note = "Neste steg bør forklare hva som gjør p0 roligere i senfasen."
    else:
        status = "contrast_still_mixed"
        note = "Støttekontrasten gjør p0-vs-p1 mer konkret, men ikke ren nok til å gi én enkel forklaring ennå."
        next_step = "stay_local"
        next_note = "Neste steg bør være en enda mindre forklaringsrunde på unike noder eller første tail-segment."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": "Startstørrelsene er rent separert i denne støttekontrasten." if size_clean else "Størrelsesseparasjonen er uklar i denne runden.",
        },
        {
            "diagnostic_family": "support_snapshot",
            "status": f"degree_gap={fmt(degree_gap)};ball1_gap={fmt(ball1_gap)};expansion_gap={fmt(expansion_gap)}",
            "note": "Positiv degree/ball1-gap betyr tettere lokal støtte for p1. Negativ expansion-gap betyr at p0 har litt større relativ videre ekspansjon.",
        },
        {
            "diagnostic_family": "duel_snapshot",
            "status": f"tradeoff_rate={fmt(tradeoff_rate)};p0_calm_rate={fmt(p0_calm_rate)};p1_clean_rate={fmt(p1_clean_rate)}",
            "note": "Dette oppsummerer hvordan p0 og p1 skiller lag på samme seed_delta i de smale holdout-duellene.",
        },
        {
            "diagnostic_family": "p0_p1_contrast",
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
    target_summary: Sequence[Dict[str, Any]],
    support_summary: Sequence[Dict[str, Any]],
    duel_aggr: Sequence[Dict[str, Any]],
    diagnosis: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15w: add_chord p0-vs-p1 support contrast")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden prøver å forklare den gjenværende p0-vs-p1-usikkerheten med støttegeometri og smale seed-dueller, uten å åpne ny mapping."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Support contrast")
    lines.append("")
    lines.append("| placement | support | unique node | mean degree | ball1 | ball2 | ball3 | shell2/shell1 | ball3/ball1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in support_summary:
        lines.append(
            f"| {row['placement_label']} | {row['support_signature']} | {int(row['unique_node'])} | {fmt(row['mean_support_degree'])} | {fmt(row['support_ball_1'],1)} | {fmt(row['support_ball_2'],1)} | {fmt(row['support_ball_3'],1)} | {fmt(row['shell2_over_shell1'])} | {fmt(row['ball3_over_ball1'])} |"
        )
    lines.append("")
    lines.append("## Duel aggregate")
    lines.append("")
    lines.append("| duel label | n | rate | mean exact gap | mean first-exact gap | mean lock gap | mean switch gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in duel_aggr:
        lines.append(
            f"| {row['duel_label']} | {int(row['n_duels'])} | {fmt(row['rate'])} | {fmt(row['mean_p1_minus_p0_exact_gap'])} | {fmt(row['mean_p1_minus_p0_first_exact_gap'],1)} | {fmt(row['mean_p1_minus_p0_lock_gap'])} | {fmt(row['mean_p1_minus_p0_switch_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en støttekontrast på samme lokale band, ikke en ny dynamikk-scan.")
    lines.append("- Les dette som en liten forklaringsrunde for p0-vs-p1, ikke som generell defect-teori.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15w add_chord p0-vs-p1 support contrast.")
    p.add_argument("--out-support-csv", type=str, default="Documentation/v15w_add_chord_p0_p1_support_summary.csv")
    p.add_argument("--out-duel-csv", type=str, default="Documentation/v15w_add_chord_p0_p1_duel_rows.csv")
    p.add_argument("--out-duel-aggregate-csv", type=str, default="Documentation/v15w_add_chord_p0_p1_duel_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15w_add_chord_p0_p1_support_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15w_add_chord_p0_p1_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15w_add_chord_p0_p1_support_contrast.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15w_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15w.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    support_summary = support_rows(base_state)
    v15v_rows = read_csv(V15V_RUNS)
    duel_rows_out = duel_rows(v15v_rows)
    duel_aggr = duel_aggregate(duel_rows_out)
    diagnosis = diagnosis_rows(target_summary, support_summary, duel_rows_out)
    report_md = build_report(
        target_summary=target_summary,
        support_summary=support_summary,
        duel_aggr=duel_aggr,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15w operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en liten p0-vs-p1-forklaringsrunde, ikke som bredere cycle-mapping.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15w",
            "",
            "Denne runden prøver å forklare hvorfor de to sterkeste lokale add_chord-punktene fortsatt er vanskelige å skille helt rent.",
            "",
            "Vi sammenligner både hvor de sitter i grafen og hvordan de oppfører seg på de samme små holdout-duellene.",
        ]
    ) + "\n"
    write_csv(args.out_support_csv, support_summary)
    write_csv(args.out_duel_csv, duel_rows_out)
    write_csv(args.out_duel_aggregate_csv, duel_aggr)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
