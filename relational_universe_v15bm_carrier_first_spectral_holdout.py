#!/usr/bin/env python3
"""v0.15bm carrier-first spectral holdout.

This round follows v15bl. It does not reopen a broad conditional sweep.
Instead it asks a narrower question:

if we take the best spectral conditional pockets from v15bl and compare them
against the nearest dim-favored controls on fresh holdout seeds, does the
spectral advantage survive in a carrier-first reading?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


HOLDOUT_SEED_DELTAS = (163, 195, 223, 287)
GROWTH_SEED = 202

CARRIER_SPECS = [
    {
        "perturbation": "add_chord",
        "family_name": v15bl.ADD_CHORD_FAMILY,
        "condition_name": "cycle_band_p2",
        "carrier_role": "spectral_candidate",
        "target_nodes": 48,
        "placement": 2,
        "steps": v15ac.FULL_STEPS,
        "log_every": v15ac.LOG_EVERY,
    },
    {
        "perturbation": "add_chord",
        "family_name": v15bl.ADD_CHORD_FAMILY,
        "condition_name": "cycle_band_p1",
        "carrier_role": "dim_control",
        "target_nodes": 48,
        "placement": 1,
        "steps": v15ac.FULL_STEPS,
        "log_every": v15ac.LOG_EVERY,
    },
    {
        "perturbation": "local_swap",
        "family_name": v15bl.LOCAL_SWAP_FAMILY,
        "condition_name": "low_load_diffuse",
        "carrier_role": "spectral_candidate",
        "target_nodes": 96,
        "placement": 3,
        "steps": v15q.STEPS,
        "log_every": v15q.LOG_EVERY,
    },
    {
        "perturbation": "local_swap",
        "family_name": v15bl.LOCAL_SWAP_FAMILY,
        "condition_name": "buffered_heavy_load",
        "carrier_role": "dim_control",
        "target_nodes": 96,
        "placement": 1,
        "steps": v15q.STEPS,
        "log_every": v15q.LOG_EVERY,
    },
]


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


def aggregate_role_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_condition: Dict[str, List[Dict[str, Any]]] = {}
    by_role: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        by_condition.setdefault(str(row["condition_name"]), []).append(dict(row))
        by_role.setdefault(str(row["carrier_role"]), []).append(dict(row))

    for condition_name, group in sorted(by_condition.items()):
        sample = group[0]
        out.append(
            v15bl.aggregate_group(
                group,
                group_level="condition",
                family_name=str(sample["family_name"]),
                group_name=condition_name,
                perturbation=str(sample["perturbation"]),
            )
        )

    for carrier_role, group in sorted(by_role.items()):
        out.append(
            v15bl.aggregate_group(
                group,
                group_level="role_pool",
                family_name="carrier_first_holdout",
                group_name=f"{carrier_role}_pool",
                perturbation="mixed",
            )
        )

    out.append(
        v15bl.aggregate_group(
            list(rows),
            group_level="global_pool",
            family_name="carrier_first_holdout",
            group_name="all_holdout_runs",
            perturbation="mixed",
        )
    )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    agg_map = {(str(row["group_level"]), str(row["group_name"])): dict(row) for row in aggregate}

    add_winner = agg_map[("condition", "cycle_band_p2")]
    add_control = agg_map[("condition", "cycle_band_p1")]
    swap_winner = agg_map[("condition", "low_load_diffuse")]
    swap_control = agg_map[("condition", "buffered_heavy_load")]
    spectral_pool = agg_map[("role_pool", "spectral_candidate_pool")]
    control_pool = agg_map[("role_pool", "dim_control_pool")]

    add_support = int(safe_float(add_winner["spectral_rank_nontrivial"])) == 1 and int(safe_float(add_control["spectral_rank_nontrivial"])) > 1
    swap_support = int(safe_float(swap_winner["spectral_rank_nontrivial"])) == 1 and int(safe_float(swap_control["spectral_rank_nontrivial"])) > 1

    if add_support and swap_support:
        status = "carrier_first_spectral_split_supported"
        note = (
            "Begge carrier-parene holder holdout-splittelsen: spektral-vinnerne beholder rank 1, "
            "mens de naerliggende kontrollene fortsatt ikke gjor det."
        )
        next_step = "micro_cross_family_transfer"
        next_note = "Neste steg bor teste om den spektrale lommen overlever en liten overforing pa tvers av carrier-typer eller naerliggende plasseringer."
    elif int(safe_float(spectral_pool["spectral_rank_nontrivial"])) == 1 and safe_float(spectral_pool["mean_dim_minus_spectral"]) > safe_float(control_pool["mean_dim_minus_spectral"]):
        status = "carrier_first_pool_supported_controls_mixed"
        note = (
            "Holdouten holder best som pooled carrier-first lesning: spektral-kandidatene samlet ser bedre ut enn kontrollene, "
            "men minst ett av de to parene er fortsatt blandet."
        )
        next_step = "stay_small_on_failed_pair"
        next_note = "Neste steg bor forklare det svakere paret, ikke a aapne en bred ny scan."
    else:
        status = "carrier_first_holdout_not_yet"
        note = "Holdouten bekrefter ikke en ren carrier-first spektral splittelse pa disse friske seedene."
        next_step = "keep_family_specific"
        next_note = "Neste steg bor holde seg innen den sterkeste familien i stedet for a presse en delt cross-family-lesning."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle holdout-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "add_chord_holdout_status",
            "status": "supported" if add_support else "mixed",
            "note": (
                f"`cycle_band_p2` har spectral rank {int(add_winner['spectral_rank_nontrivial'])}, mens `cycle_band_p1` har {int(add_control['spectral_rank_nontrivial'])}."
            ),
        },
        {
            "diagnostic_family": "local_swap_holdout_status",
            "status": "supported" if swap_support else "mixed",
            "note": (
                f"`low_load_diffuse` har spectral rank {int(swap_winner['spectral_rank_nontrivial'])}, mens `buffered_heavy_load` har {int(swap_control['spectral_rank_nontrivial'])}."
            ),
        },
        {
            "diagnostic_family": "carrier_first_pool",
            "status": "spectral_candidate_pool_beats_controls"
            if safe_float(spectral_pool["mean_dim_minus_spectral"]) > safe_float(control_pool["mean_dim_minus_spectral"])
            else "pool_mixed",
            "note": (
                f"Spectral-kandidat-poolen har dim-minus-spectral {fmt(spectral_pool['mean_dim_minus_spectral'])}, "
                f"mot {fmt(control_pool['mean_dim_minus_spectral'])} i kontroll-poolen."
            ),
        },
        {
            "diagnostic_family": "carrier_first_reading",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    condition_rows = [row for row in aggregate if str(row["group_level"]) == "condition"]
    role_rows = [row for row in aggregate if str(row["group_level"]) == "role_pool"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bm: carrier-first spectral holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om de to beste spektrale lommene fra v15bl holder mot naerliggende kontrollcarrier-pa friske holdout-seeds.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Holdout-conditions")
    lines.append("")
    lines.append("| condition | perturbation | role | spectral | dim | best non-trivial | spectral rank | dim-spectral |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in condition_rows:
        role = next(spec["carrier_role"] for spec in CARRIER_SPECS if spec["condition_name"] == row["group_name"])
        lines.append(
            f"| {row['group_name']} | {row['perturbation']} | {role} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {row['best_nontrivial_metric']} | {int(row['spectral_rank_nontrivial'])} | {fmt(row['mean_dim_minus_spectral'])} |"
        )
    lines.append("")
    lines.append("## Role-pools")
    lines.append("")
    lines.append("| pool | n | spectral | dim | best non-trivial | spectral rank | dim-spectral |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in role_rows:
        lines.append(
            f"| {row['group_name']} | {int(row['n_runs'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {row['best_nontrivial_metric']} | {int(row['spectral_rank_nontrivial'])} | {fmt(row['mean_dim_minus_spectral'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en liten carrier-first holdout, ikke en ny global invariant-test.")
    lines.append("- Positivt signal her betyr at spektral lomme holder mot en naer kontrollcarrier, ikke at Lorentz-likhet eller spacetime er etablert.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bm carrier-first spectral holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bm_carrier_first_spectral_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bm_carrier_first_spectral_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bm_carrier_first_spectral_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bm_carrier_first_spectral_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bm_carrier_first_spectral_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bm_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bm.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([48, 96])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in (48, 96)]
    ensemble_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    base_lookup = {(str(row["ensemble"]), int(row["growth_seed"])): dict(row) for row in base_rows}
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    rows: List[Dict[str, Any]] = []
    for spec in CARRIER_SPECS:
        ens = ensemble_by_target[int(spec["target_nodes"])]
        base = base_states[(ens.name, GROWTH_SEED)]
        base_row = base_lookup[(ens.name, GROWTH_SEED)]
        for seed_delta in HOLDOUT_SEED_DELTAS:
            run_seed = int(spec["target_nodes"]) * 100000 + GROWTH_SEED * 1000 + int(spec["placement"]) + int(seed_delta)
            res = v15q.run_defect_with_sets(
                base,
                params=params,
                seed=run_seed,
                steps=int(spec["steps"]),
                perturbation=str(spec["perturbation"]),
                center_token_index=int(spec["placement"]),
                local_coupling="maximal",
                log_every=int(spec["log_every"]),
            )
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            info = dict(res["perturbation_info"])
            support = list(info.get("support", []))
            if str(spec["perturbation"]) == "add_chord":
                core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
            else:
                core_shell = v15aw.core_shell_metrics(res["damaged_sets"], support)
            drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
            rows.append(
                {
                    "perturbation": str(spec["perturbation"]),
                    "family_name": str(spec["family_name"]),
                    "condition_name": str(spec["condition_name"]),
                    "carrier_role": str(spec["carrier_role"]),
                    "target_nodes": int(spec["target_nodes"]),
                    "growth_seed": GROWTH_SEED,
                    "placement": int(spec["placement"]),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match(str(spec["perturbation"]), str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "core_shell_label": str(core_shell["label"]),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    **drift,
                }
            )

    aggregate = aggregate_role_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bm operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en liten carrier-first holdout, ikke som en ny global invariant-lovtest.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bm",
            "",
            "Denne runden prover bare noe lite men viktig: om de to beste spektrale lommene holder seg bedre enn naerliggende kontrollretninger nar vi bytter til friske seed-varianter.",
            "",
            "Det er en strengere test enn v15bl fordi den sjekker om signalet holder utenfor den opprinnelige lille pakken.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
