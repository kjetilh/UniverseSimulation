#!/usr/bin/env python3
"""v0.15m single-defect survival lab.

This is a new defect question after the collision mechanism line weakened on
holdout. It asks whether the partial `token_shift` extinction signal from v15
looks like a real single-defect survival/extinction split, with `add_chord` as
an alive control family.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15


TARGETS = (48, 96)
GROWTH_SEEDS = (101, 202)
PLACEMENTS = (0, 1, 2, 3, 4, 5)
PERTURBATIONS = ("token_shift", "add_chord")
STEPS = 960
LOG_EVERY = 8


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


def classify_single_tail(
    *,
    final_alive: int,
    first_zero_step: float,
    last_alive_fraction: float,
    tail_dual_fraction: float,
    tail_mean_component_count: float,
    tail_mean_radius: float,
    tail_change_count: int,
    steps: int,
) -> str:
    if final_alive == 0:
        if first_zero_step >= 0 and first_zero_step <= 0.5 * steps:
            return "extinction"
        return "late_extinction"
    if tail_dual_fraction >= 0.75:
        return "persistent_split_tail"
    if tail_mean_component_count <= 1.10 and tail_change_count == 0:
        return "quiet_singleton_tail"
    if tail_mean_radius >= 3.0 and tail_mean_component_count < 2.0:
        return "persistent_diffuse_tail"
    return "mixed_tail"


def run_rows(
    *,
    ensembles: Sequence[Any],
    base_states: Mapping[tuple[str, int], Any],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for ens in ensembles:
        target = int(ens.target_nodes)
        if target not in TARGETS:
            continue
        for growth_seed in GROWTH_SEEDS:
            base = base_states[(ens.name, int(growth_seed))]
            for perturbation in PERTURBATIONS:
                for placement in PLACEMENTS:
                    run_seed = target * 100000 + int(growth_seed) * 1000 + int(placement)
                    res = v15.run_defect_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=STEPS,
                        perturbation=perturbation,
                        center_token_index=int(placement),
                        local_coupling="maximal",
                        log_every=LOG_EVERY,
                    )
                    info = dict(res["perturbation_info"])
                    actual = str(info.get("type", "unknown"))
                    requested_match = 1 if v15.v14.perturbation_requested_match(perturbation, actual) else 0
                    support = list(info.get("support", []))
                    log_rows = list(res["log_rows"])
                    tail_rows = log_rows[max(0, int(math.floor(0.75 * len(log_rows)))) :]
                    tail_change_count = sum(
                        1
                        for a, b in zip(tail_rows, tail_rows[1:])
                        if int(a["damage_component_count"]) != int(b["damage_component_count"])
                        or int(a["alive"]) != int(b["alive"])
                    )
                    tail_dual_fraction = mean_defined(
                        1.0 if int(row["damage_component_count"]) >= 2 else 0.0
                        for row in tail_rows
                    )
                    tail_mean_component_count = mean_defined(
                        safe_float(row["damage_component_count"]) for row in tail_rows
                    )
                    tail_mean_radius = mean_defined(
                        safe_float(row["radius_control"])
                        for row in tail_rows
                        if safe_float(row["radius_control"]) >= 0
                    )
                    summary = dict(res["summary"])
                    tail_label = classify_single_tail(
                        final_alive=int(summary["final_alive"]),
                        first_zero_step=safe_float(summary["first_zero_step"]),
                        last_alive_fraction=safe_float(summary["last_alive_fraction"]),
                        tail_dual_fraction=safe_float(tail_dual_fraction),
                        tail_mean_component_count=safe_float(tail_mean_component_count),
                        tail_mean_radius=safe_float(tail_mean_radius),
                        tail_change_count=int(tail_change_count),
                        steps=STEPS,
                    )
                    rows.append(
                        {
                            "target_nodes": target,
                            "growth_seed": int(growth_seed),
                            "placement": int(placement),
                            "run_seed": int(run_seed),
                            "requested_perturbation": perturbation,
                            "actual_perturbation": actual,
                            "requested_match": int(requested_match),
                            "support_size": len(support),
                            "support_signature": ",".join(str(x) for x in support),
                            "final_alive": int(summary["final_alive"]),
                            "first_zero_step": safe_float(summary["first_zero_step"]),
                            "last_alive_fraction": safe_float(summary["last_alive_fraction"]),
                            "mean_radius_control": safe_float(summary["mean_radius_control"]),
                            "mean_component_count": safe_float(summary["mean_component_count"]),
                            "outcome_class": str(summary["outcome_class"]),
                            "tail_dual_fraction": safe_float(tail_dual_fraction),
                            "tail_mean_component_count": safe_float(tail_mean_component_count),
                            "tail_mean_radius": safe_float(tail_mean_radius),
                            "tail_change_count": int(tail_change_count),
                            "tail_label": tail_label,
                        }
                    )
    return rows


def aggregate_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        grouped.setdefault((str(row["requested_perturbation"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (perturbation, target), rows in sorted(grouped.items()):
        counts: Dict[str, int] = {}
        for row in rows:
            counts[str(row["tail_label"])] = counts.get(str(row["tail_label"]), 0) + 1
        dominant = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        out.append(
            {
                "requested_perturbation": perturbation,
                "target_nodes": int(target),
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "final_alive_rate": mean_defined(float(r["final_alive"]) for r in rows),
                "extinction_rate": mean_defined(1.0 if str(r["tail_label"]) == "extinction" else 0.0 for r in rows),
                "late_extinction_rate": mean_defined(1.0 if str(r["tail_label"]) == "late_extinction" else 0.0 for r in rows),
                "persistent_split_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "persistent_split_tail" else 0.0 for r in rows),
                "quiet_singleton_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "quiet_singleton_tail" else 0.0 for r in rows),
                "persistent_diffuse_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "persistent_diffuse_tail" else 0.0 for r in rows),
                "mixed_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "mixed_tail" else 0.0 for r in rows),
                "mean_first_zero_step": mean_defined(
                    safe_float(r["first_zero_step"])
                    for r in rows
                    if safe_float(r["first_zero_step"]) >= 0
                ),
                "mean_tail_dual_fraction": mean_defined(safe_float(r["tail_dual_fraction"]) for r in rows),
                "mean_tail_mean_component_count": mean_defined(safe_float(r["tail_mean_component_count"]) for r in rows),
                "mean_tail_change_count": mean_defined(safe_float(r["tail_change_count"]) for r in rows),
                "dominant_tail_label": dominant,
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    token_rows = [row for row in aggregate if str(row["requested_perturbation"]) == "token_shift"]
    add_rows = [row for row in aggregate if str(row["requested_perturbation"]) == "add_chord"]
    token_ext = max((safe_float(r["extinction_rate"]) + safe_float(r["late_extinction_rate"]) for r in token_rows), default=0.0)
    add_ext = max((safe_float(r["extinction_rate"]) + safe_float(r["late_extinction_rate"]) for r in add_rows), default=0.0)
    token_48 = next((r for r in token_rows if int(r["target_nodes"]) == 48), None)
    token_96 = next((r for r in token_rows if int(r["target_nodes"]) == 96), None)

    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstørrelsene er fortsatt rent separert i denne runden."
                if size_clean
                else "Startstørrelsene er ikke rent separert, så survival-lesningen må tones ned."
            ),
        }
    ]

    if token_ext >= 0.20 and add_ext <= 0.05:
        if token_48 and token_96 and (
            safe_float(token_48["extinction_rate"]) + safe_float(token_48["late_extinction_rate"])
            > safe_float(token_96["extinction_rate"]) + safe_float(token_96["late_extinction_rate"])
        ):
            signal_status = "token_shift_extinction_signal_present"
            signal_note = "Token_shift viser en reell survival/extinction-splitt mot en levende add_chord-kontroll, sterkest ved mindre størrelse."
            next_status = "map_token_shift_thresholds"
            next_note = "Neste steg bør kartlegge hvor extinction-splittet slår inn, ikke gå tilbake til collision-mekanismer."
        else:
            signal_status = "token_shift_extinction_signal_present"
            signal_note = "Token_shift viser en reell survival/extinction-splitt mot en levende add_chord-kontroll."
            next_status = "map_token_shift_thresholds"
            next_note = "Neste steg bør kartlegge terskler og plasseringseffekter for token_shift."
    else:
        signal_status = "token_shift_extinction_not_clean"
        signal_note = "Token_shift skiller seg ikke klart nok fra add_chord til å kalle dette et rent survival/extinction-spor ennå."
        next_status = "pause_survival_claims"
        next_note = "Neste steg bør være mer forsiktig eller bytte defect-spørsmål igjen."

    out.append({"diagnostic_family": "survival_signal", "status": signal_status, "note": signal_note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def build_report(
    *,
    target_summary: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15m: single-defect survival lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden skifter bort fra kollisjoner og tester et nytt defect-spørsmål: om `token_shift` viser en ekte survival/extinction-splitt, med `add_chord` som levende kontroll."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregate survival / tail")
    lines.append("")
    lines.append("| perturbation | target | alive | extinction | late extinction | split tail | quiet tail | mixed | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['requested_perturbation']} | {int(row['target_nodes'])} | {fmt(row['final_alive_rate'])} | {fmt(row['extinction_rate'])} | {fmt(row['late_extinction_rate'])} | {fmt(row['persistent_split_tail_rate'])} | {fmt(row['quiet_singleton_tail_rate'])} | {fmt(row['mixed_tail_rate'])} | {row['dominant_tail_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er et nytt defect-spørsmål, ikke en utvidelse av collision-generaliseringen.")
    lines.append("- Poenget er å se om én perturbasjonstype faktisk har en egen survival-/extinction-dynamikk.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15m single-defect survival lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15m_single_defect_survival_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15m_single_defect_survival_aggregate.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15m_single_defect_survival_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15m_single_defect_survival_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15m_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15m.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_summary = v10e.summarize_bases(base_rows)
    rows = run_rows(ensembles=ensembles, base_states=base_states)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, aggregate)
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15m operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som et nytt defect-spørsmål om survival/extinction, ikke som partikkelbevis.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15m",
            "",
            "Denne runden spør om én type lokal endring, `token_shift`, ofte dør ut på en måte som andre typer ikke gjør.",
            "",
            "Det er interessant fordi det kan bety at noen defects er mer skjøre enn andre, selv før de kolliderer med noe annet.",
        ]
    ) + "\n"

    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
