#!/usr/bin/env python3
"""v0.15o token_shift fragility replication.

This round follows the v15n placement-structured fragility hint. It does not
reopen a broad search. Instead it asks whether the specific extinct token_shift
placements from v15n still look more fragile than nearby alive controls on the
same base when we rerun them with additional seeds.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15m_single_defect_survival_lab as v15m


TARGETS = (48, 96)
GROWTH_SEEDS = (101, 202)
REPLICATE_OFFSETS = (0, 1, 2, 3, 4, 5, 6, 7)
PERTURBATIONS = ("token_shift", "add_chord")
STEPS = 960
LOG_EVERY = 8
SOURCE_V15N = Path("Documentation/v15n_token_shift_fragility_runs.csv")


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def profile_distance(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    return (
        abs(safe_float(a["support_ball_3"]) - safe_float(b["support_ball_3"]))
        + abs(safe_float(a["support_ball_2"]) - safe_float(b["support_ball_2"]))
        + 2.0 * abs(safe_float(a["mean_support_degree"]) - safe_float(b["mean_support_degree"]))
    )


def select_profile_pairs(v15n_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    token_rows = [
        dict(row)
        for row in v15n_rows
        if str(row["requested_perturbation"]) == "token_shift" and int(row["requested_match"]) == 1
    ]
    extinct_rows = [row for row in token_rows if str(row["fragility_label"]) == "extinct"]
    profile_pairs: List[Dict[str, Any]] = []
    for ext in extinct_rows:
        target = int(ext["target_nodes"])
        growth_seed = int(ext["growth_seed"])
        candidates = [
            row
            for row in token_rows
            if int(row["target_nodes"]) == target
            and int(row["growth_seed"]) == growth_seed
            and str(row["fragility_label"]) == "alive_tail"
        ]
        if not candidates:
            continue
        control = min(
            candidates,
            key=lambda row: (
                profile_distance(ext, row),
                abs(int(row["placement"]) - int(ext["placement"])),
                int(row["placement"]),
            ),
        )
        pair_id = f"t{target}_g{growth_seed}_p{int(ext['placement'])}_vs_p{int(control['placement'])}"
        profile_pairs.append(
            {
                "pair_id": pair_id,
                "target_nodes": target,
                "growth_seed": growth_seed,
                "fragile_placement": int(ext["placement"]),
                "control_placement": int(control["placement"]),
                "fragile_support_signature": str(ext["support_signature"]),
                "control_support_signature": str(control["support_signature"]),
                "fragile_support_ball_3": safe_float(ext["support_ball_3"]),
                "control_support_ball_3": safe_float(control["support_ball_3"]),
                "fragile_support_degree": safe_float(ext["mean_support_degree"]),
                "control_support_degree": safe_float(control["mean_support_degree"]),
                "matching_distance": profile_distance(ext, control),
            }
        )
    return sorted(profile_pairs, key=lambda row: (int(row["target_nodes"]), int(row["growth_seed"]), int(row["fragile_placement"])))


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


def run_rows(
    *,
    profile_pairs: Sequence[Dict[str, Any]],
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    ensembles_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    for pair in profile_pairs:
        target = int(pair["target_nodes"])
        growth_seed = int(pair["growth_seed"])
        base = base_states[(ensembles_by_target[target].name, growth_seed)]
        for role, placement in (
            ("fragile_profile", int(pair["fragile_placement"])),
            ("matched_alive_control", int(pair["control_placement"])),
        ):
            for perturbation in PERTURBATIONS:
                for rep_idx in REPLICATE_OFFSETS:
                    run_seed = (
                        target * 100000
                        + growth_seed * 1000
                        + int(placement)
                        + rep_idx * 10000000
                        + (0 if perturbation == "token_shift" else 50000000)
                    )
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
                    geom = v14c.support_geometry_features(base, support)
                    tail_label, fragility_label = classify_tail_from_result(res)
                    summary = dict(res["summary"])
                    rows.append(
                        {
                            "pair_id": str(pair["pair_id"]),
                            "profile_role": role,
                            "target_nodes": target,
                            "growth_seed": growth_seed,
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


def aggregate_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, str, str], List[Dict[str, Any]]] = {}
    for row in run_rows:
        grouped.setdefault(
            (str(row["pair_id"]), str(row["profile_role"]), str(row["requested_perturbation"])),
            [],
        ).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (pair_id, profile_role, perturbation), rows in sorted(grouped.items()):
        tail_counts: Dict[str, int] = {}
        for row in rows:
            tail_counts[str(row["tail_label"])] = tail_counts.get(str(row["tail_label"]), 0) + 1
        dominant = max(tail_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        out.append(
            {
                "pair_id": pair_id,
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


def pair_diagnosis_rows(aggregate_rows_: Sequence[Dict[str, Any]], profile_pairs: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg_index = {
        (str(row["pair_id"]), str(row["profile_role"]), str(row["requested_perturbation"])): dict(row)
        for row in aggregate_rows_
    }
    out: List[Dict[str, Any]] = []
    for pair in profile_pairs:
        pair_id = str(pair["pair_id"])
        tf = agg_index[(pair_id, "fragile_profile", "token_shift")]
        tc = agg_index[(pair_id, "matched_alive_control", "token_shift")]
        af = agg_index[(pair_id, "fragile_profile", "add_chord")]
        ac = agg_index[(pair_id, "matched_alive_control", "add_chord")]
        token_gap = safe_float(tf["extinction_rate"]) - safe_float(tc["extinction_rate"])
        add_gap = safe_float(af["extinction_rate"]) - safe_float(ac["extinction_rate"])
        if token_gap >= 0.25 and max(safe_float(af["extinction_rate"]), safe_float(ac["extinction_rate"])) <= 0.05:
            status = "fragile_profile_replicates"
        elif token_gap >= 0.10 and max(safe_float(af["extinction_rate"]), safe_float(ac["extinction_rate"])) <= 0.05:
            status = "weak_fragile_profile"
        else:
            status = "not_stable"
        out.append(
            {
                "pair_id": pair_id,
                "target_nodes": int(pair["target_nodes"]),
                "growth_seed": int(pair["growth_seed"]),
                "fragile_placement": int(pair["fragile_placement"]),
                "control_placement": int(pair["control_placement"]),
                "matching_distance": safe_float(pair["matching_distance"]),
                "token_fragile_extinction_rate": safe_float(tf["extinction_rate"]),
                "token_control_extinction_rate": safe_float(tc["extinction_rate"]),
                "token_extinction_gap": token_gap,
                "add_fragile_extinction_rate": safe_float(af["extinction_rate"]),
                "add_control_extinction_rate": safe_float(ac["extinction_rate"]),
                "add_extinction_gap": add_gap,
                "status": status,
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    aggregate_rows_: Sequence[Dict[str, Any]],
    pair_diagnosis: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((safe_float(row["strict_match_rate"]) for row in aggregate_rows_), default=0.0) >= 0.999
    strong = sum(1 for row in pair_diagnosis if str(row["status"]) == "fragile_profile_replicates")
    weak = sum(1 for row in pair_diagnosis if str(row["status"]) == "weak_fragile_profile")
    mean_gap = mean_defined(safe_float(row["token_extinction_gap"]) for row in pair_diagnosis)
    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er fortsatt rent separert og alle replikerte perturbasjoner matcher ønsket type."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        }
    ]
    if strong >= 2 and mean_gap >= 0.20:
        out.append(
            {
                "diagnostic_family": "fragility_replication",
                "status": "replicated_local_fragility_profiles",
                "note": "Minst to skjøre profiler holder høyere token_shift-extinction enn sine matchede levende kontroller, mens add_chord fortsatt holder seg levende.",
            }
        )
        out.append(
            {
                "diagnostic_family": "next_step",
                "status": "map_fragile_profiles",
                "note": "Neste steg bør være en enda smalere kartlegging rundt de replikerte skjøre token_shift-profilene, ikke brede survival-paastander.",
            }
        )
    elif (strong + weak) >= 2 and mean_gap >= 0.10:
        out.append(
            {
                "diagnostic_family": "fragility_replication",
                "status": "partially_replicated",
                "note": "Skjørhetsprofilene reproduserer noe gap mot kontrollene, men ikke rent nok til å kalles stabile lokale profiler ennå.",
            }
        )
        out.append(
            {
                "diagnostic_family": "next_step",
                "status": "refine_profiles",
                "note": "Neste steg bør være en enda smalere profilrunde rundt de beste token_shift-kandidatene med mer lokalt matchede kontroller.",
            }
        )
    else:
        out.append(
            {
                "diagnostic_family": "fragility_replication",
                "status": "not_replicated_cleanly",
                "note": "De skjøre v15n-profilene holder ikke et klart extinction-gap mot matchede kontroller under nye run-seeds.",
            }
        )
        out.append(
            {
                "diagnostic_family": "next_step",
                "status": "pivot_again",
                "note": "Neste steg bør være et annet smalt defect-spørsmål heller enn mer token_shift-fragility langs samme linje.",
            }
        )
    return out


def build_report(
    *,
    target_summary: Sequence[Dict[str, Any]],
    profile_pairs: Sequence[Dict[str, Any]],
    aggregate_rows_: Sequence[Dict[str, Any]],
    pair_diagnosis: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15o: token_shift fragility replication")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om de skjøre `token_shift`-plasseringene fra v15n fortsatt er skjørere enn nærliggende levende kontroller på samme base når vi rerunner dem med flere seeds."
    )
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
    lines.append("## Matchede profiler")
    lines.append("")
    lines.append("| pair | fragile placement | control placement | distance |")
    lines.append("| --- | --- | --- | --- |")
    for row in profile_pairs:
        lines.append(
            f"| {row['pair_id']} | {int(row['fragile_placement'])} | {int(row['control_placement'])} | {fmt(row['matching_distance'])} |"
        )
    lines.append("")
    lines.append("## Pair diagnosis")
    lines.append("")
    lines.append("| pair | token fragile ext | token control ext | token gap | add fragile ext | add control ext | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in pair_diagnosis:
        lines.append(
            f"| {row['pair_id']} | {fmt(row['token_fragile_extinction_rate'])} | {fmt(row['token_control_extinction_rate'])} | {fmt(row['token_extinction_gap'])} | {fmt(row['add_fragile_extinction_rate'])} | {fmt(row['add_control_extinction_rate'])} | {row['status']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal replikeringsrunde av lokale profiler, ikke en ny bred defect-scan.")
    lines.append("- Les fortsatt dette som defect-fragility, ikke som partikkelbevis eller generell geometri.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15o token_shift fragility replication.")
    p.add_argument("--source-v15n", type=str, default=str(SOURCE_V15N))
    p.add_argument("--out-profile-csv", type=str, default="Documentation/v15o_token_shift_fragility_profile_pairs.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15o_token_shift_fragility_replication_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15o_token_shift_fragility_replication_aggregate.csv")
    p.add_argument("--out-pair-csv", type=str, default="Documentation/v15o_token_shift_fragility_pair_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15o_token_shift_fragility_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15o_token_shift_fragility_replication.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15o_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15o.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    v15n_rows = read_csv_rows(Path(args.source_v15n))
    profile_pairs = select_profile_pairs(v15n_rows)
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_summary = v10e.summarize_bases(base_rows)
    run_rows_ = run_rows(profile_pairs=profile_pairs, ensembles=ensembles, base_states=base_states)
    aggregate = aggregate_rows(run_rows_)
    pair_diagnosis = pair_diagnosis_rows(aggregate, profile_pairs)
    recommendation = recommendation_rows(target_summary, aggregate, pair_diagnosis)
    report_md = build_report(
        target_summary=target_summary,
        profile_pairs=profile_pairs,
        aggregate_rows_=aggregate,
        pair_diagnosis=pair_diagnosis,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15o operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som en smal replikeringsrunde av token_shift-fragility, ikke som partikkelbevis.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15o",
            "",
            "Denne runden sjekker om de `token_shift`-stedene som virket skjøre i forrige runde fortsatt er skjørere når vi kjører dem flere ganger.",
            "",
            "Det er nyttig fordi det kan skille mellom ekte lokal skjørhet og ren engangsstøy.",
        ]
    ) + "\n"

    write_csv(args.out_profile_csv, profile_pairs)
    write_csv(args.out_runs_csv, run_rows_)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_pair_csv, pair_diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
