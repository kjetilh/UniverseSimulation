#!/usr/bin/env python3
"""v0.15p token_shift profile refinement.

This round follows the strongest partially replicated token_shift fragility
profile from v15o. It does not widen the search. It asks whether the fragile
placement `p3` on target 48 / growth seed 101 still looks unusually fragile
when compared against two better-matched alive controls on the same base:

- `p1`: same support_ball_3 as the fragile profile in v15n
- `p4`: adjacent and degree-close control used in v15o
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15m_single_defect_survival_lab as v15m


TARGET = 48
GROWTH_SEED = 101
REPLICATE_OFFSETS = tuple(range(16))
PERTURBATIONS = ("token_shift", "add_chord")
STEPS = 960
LOG_EVERY = 8
PROFILE_ROLES = (
    ("fragile_p3", 3, "fragile reference profile"),
    ("control_ball3_p1", 1, "same support_ball_3 family"),
    ("control_adjacent_p4", 4, "adjacent degree-close control"),
)


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


def classify_tail_from_result(res: Mapping[str, Any]) -> Tuple[str, str]:
    log_rows = list(res["log_rows"])
    tail_rows = log_rows[max(0, int(math.floor(0.75 * len(log_rows)))) :]
    tail_change_count = sum(
        1
        for a, b in zip(tail_rows, tail_rows[1:])
        if int(a["damage_component_count"]) != int(b["damage_component_count"])
        or int(a["alive"]) != int(b["alive"])
    )
    tail_dual_fraction = mean_defined(
        1.0 if int(row["damage_component_count"]) >= 2 else 0.0 for row in tail_rows
    )
    tail_mean_component_count = mean_defined(
        safe_float(row["damage_component_count"]) for row in tail_rows
    )
    tail_mean_radius = mean_defined(
        safe_float(row["radius_control"]) for row in tail_rows if safe_float(row["radius_control"]) >= 0
    )
    summary = dict(res["summary"])
    tail_label = v15m.classify_single_tail(
        final_alive=int(summary["final_alive"]),
        first_zero_step=safe_float(summary["first_zero_step"]),
        last_alive_fraction=safe_float(summary["last_alive_fraction"]),
        tail_dual_fraction=safe_float(tail_dual_fraction),
        tail_mean_component_count=safe_float(tail_mean_component_count),
        tail_mean_radius=safe_float(tail_mean_radius),
        tail_change_count=int(tail_change_count),
        steps=STEPS,
    )
    fragility_label = "extinct" if tail_label in {"extinction", "late_extinction"} else "alive_tail"
    return tail_label, fragility_label


def run_rows(base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for role_name, placement, role_note in PROFILE_ROLES:
        for perturbation in PERTURBATIONS:
            for rep_idx in REPLICATE_OFFSETS:
                run_seed = (
                    TARGET * 100000
                    + GROWTH_SEED * 1000
                    + int(placement)
                    + rep_idx * 10000000
                    + (0 if perturbation == "token_shift" else 50000000)
                )
                res = v15.run_defect_from_base(
                    base_state,
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
                geom = v14c.support_geometry_features(base_state, support)
                tail_label, fragility_label = classify_tail_from_result(res)
                summary = dict(res["summary"])
                rows.append(
                    {
                        "profile_role": role_name,
                        "role_note": role_note,
                        "target_nodes": TARGET,
                        "growth_seed": GROWTH_SEED,
                        "placement": int(placement),
                        "replicate_index": int(rep_idx),
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
                        "tail_label": tail_label,
                        "fragility_label": fragility_label,
                        **geom,
                    }
                )
    return rows


def aggregate_rows(run_rows_: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in run_rows_:
        grouped.setdefault((str(row["profile_role"]), str(row["requested_perturbation"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (profile_role, perturbation), rows in sorted(grouped.items()):
        tail_counts: Dict[str, int] = {}
        for row in rows:
            tail_counts[str(row["tail_label"])] = tail_counts.get(str(row["tail_label"]), 0) + 1
        dominant = max(tail_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        out.append(
            {
                "profile_role": profile_role,
                "requested_perturbation": perturbation,
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "extinction_rate": mean_defined(1.0 if str(r["fragility_label"]) == "extinct" else 0.0 for r in rows),
                "persistent_split_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "persistent_split_tail" else 0.0 for r in rows),
                "persistent_diffuse_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "persistent_diffuse_tail" else 0.0 for r in rows),
                "quiet_singleton_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "quiet_singleton_tail" else 0.0 for r in rows),
                "mean_first_zero_step": mean_defined(
                    safe_float(r["first_zero_step"]) for r in rows if safe_float(r["first_zero_step"]) >= 0
                ),
                "mean_support_ball_3": mean_defined(safe_float(r["support_ball_3"]) for r in rows),
                "mean_support_degree": mean_defined(safe_float(r["mean_support_degree"]) for r in rows),
                "dominant_tail_label": dominant,
            }
        )
    return out


def role_diagnosis_rows(aggregate_rows_: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg = {
        (str(row["profile_role"]), str(row["requested_perturbation"])): dict(row)
        for row in aggregate_rows_
    }
    fragile_token = agg[("fragile_p3", "token_shift")]
    fragile_chord = agg[("fragile_p3", "add_chord")]
    out: List[Dict[str, Any]] = []
    for control_role in ("control_ball3_p1", "control_adjacent_p4"):
        token_control = agg[(control_role, "token_shift")]
        chord_control = agg[(control_role, "add_chord")]
        token_gap = safe_float(fragile_token["extinction_rate"]) - safe_float(token_control["extinction_rate"])
        chord_gap = safe_float(fragile_chord["extinction_rate"]) - safe_float(chord_control["extinction_rate"])
        if token_gap >= 0.20 and max(safe_float(fragile_chord["extinction_rate"]), safe_float(chord_control["extinction_rate"])) <= 0.05:
            status = "fragile_profile_beats_control"
        elif token_gap >= 0.10 and max(safe_float(fragile_chord["extinction_rate"]), safe_float(chord_control["extinction_rate"])) <= 0.05:
            status = "weak_gap"
        else:
            status = "no_clean_gap"
        out.append(
            {
                "fragile_role": "fragile_p3",
                "control_role": control_role,
                "token_fragile_extinction_rate": safe_float(fragile_token["extinction_rate"]),
                "token_control_extinction_rate": safe_float(token_control["extinction_rate"]),
                "token_extinction_gap": token_gap,
                "add_fragile_extinction_rate": safe_float(fragile_chord["extinction_rate"]),
                "add_control_extinction_rate": safe_float(chord_control["extinction_rate"]),
                "add_extinction_gap": chord_gap,
                "status": status,
            }
        )
    return out


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], aggregate_rows_: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    strict_match = min((safe_float(row["strict_match_rate"]) for row in aggregate_rows_), default=0.0) >= 0.999
    strong = sum(1 for row in diagnosis if str(row["status"]) == "fragile_profile_beats_control")
    weak = sum(1 for row in diagnosis if str(row["status"]) == "weak_gap")
    rows = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsen holder fortsatt rent og alle replikerte perturbasjoner matcher ønsket type."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        }
    ]
    if strong == 2:
        rows.append(
            {
                "diagnostic_family": "profile_refinement",
                "status": "strong_local_fragile_profile",
                "note": "Den skjøre `p3`-profilen holder et klart extinction-gap mot begge de bedre matchede kontrollene, mens add_chord fortsatt er levende.",
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": "map_nearest_neighbors",
                "note": "Neste steg bør være en mikro-kartlegging rett rundt `p3` med enda tettere lokale kontroller, ikke bred survival-retorikk.",
            }
        )
    elif strong + weak >= 1:
        rows.append(
            {
                "diagnostic_family": "profile_refinement",
                "status": "partially_supported_local_profile",
                "note": "Den skjøre `p3`-profilen holder noe extinction-gap, men ikke like rent mot begge kontrollene.",
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": "refine_controls_again",
                "note": "Neste steg bør være å justere de lokale kontrollene enda mer presist rundt `p3`, ikke å generalisere utover denne profilen.",
            }
        )
    else:
        rows.append(
            {
                "diagnostic_family": "profile_refinement",
                "status": "not_supported",
                "note": "Den skjøre `p3`-profilen holder ikke et rent extinction-gap mot de bedre matchede kontrollene.",
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": "pivot_again",
                "note": "Neste steg bør være et annet smalt defect-spørsmål heller enn mer token_shift-fragility langs denne profilen.",
            }
        )
    return rows


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate_rows_: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15p: token_shift profile refinement")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester bare den sterkeste skjøre `token_shift`-profilen fra v15o (`p3` på target 48 / growth seed 101) mot to bedre matchede levende kontroller på samme base."
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
    lines.append("## Aggregate by role")
    lines.append("")
    lines.append("| role | perturbation | extinction | split tail | diffuse tail | quiet tail | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows_:
        lines.append(
            f"| {row['profile_role']} | {row['requested_perturbation']} | {fmt(row['extinction_rate'])} | {fmt(row['persistent_split_tail_rate'])} | {fmt(row['persistent_diffuse_tail_rate'])} | {fmt(row['quiet_singleton_tail_rate'])} | {row['dominant_tail_label']} |"
        )
    lines.append("")
    lines.append("## Role diagnosis")
    lines.append("")
    lines.append("| control | token fragile ext | token control ext | token gap | add fragile ext | add control ext | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in diagnosis:
        lines.append(
            f"| {row['control_role']} | {fmt(row['token_fragile_extinction_rate'])} | {fmt(row['token_control_extinction_rate'])} | {fmt(row['token_extinction_gap'])} | {fmt(row['add_fragile_extinction_rate'])} | {fmt(row['add_control_extinction_rate'])} | {row['status']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en mikro-runde rundt én lokal profil, ikke en ny bred defect-scan.")
    lines.append("- Les fortsatt dette som local fragility, ikke som partikkelbevis eller generell geometri.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15p token_shift profile refinement.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15p_token_shift_profile_refinement_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15p_token_shift_profile_refinement_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15p_token_shift_profile_refinement_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15p_token_shift_profile_refinement_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15p_token_shift_profile_refinement.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15p_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15p.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = [ens for ens in v15.deep_ensembles([TARGET]) if int(ens.target_nodes) == TARGET]
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    rows = run_rows(base_state)
    aggregate = aggregate_rows(rows)
    diagnosis = role_diagnosis_rows(aggregate)
    recommendation = recommendation_rows(target_summary, aggregate, diagnosis)
    report_md = build_report(
        target_summary=target_summary,
        aggregate_rows_=aggregate,
        diagnosis=diagnosis,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15p operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som mikro-raffinement av én token_shift-profil, ikke som partikkelbevis.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15p",
            "",
            "Denne runden sjekker om ett bestemt skjørt `token_shift`-sted fortsatt er skjørere enn to lignende steder på samme graf når vi kjører det mange ganger.",
            "",
            "Det er nyttig fordi det kan vise om vi har funnet en ekte lokal skjørhetsprofil eller bare en svak forskjell som forsvinner ved nærmere kontroll.",
        ]
    ) + "\n"

    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
