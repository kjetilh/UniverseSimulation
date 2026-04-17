#!/usr/bin/env python3
"""v0.15bl conditional quasi-invariant lab.

This round returns to the quasi-invariant question, but it does not reopen the
global v12/v13 search. It asks a narrower question:

does the best non-trivial quasi-invariant candidate look cleaner if we
condition on the mesoscale families that survived in the later v15 track?

The comparison is intentionally small:

- add_chord: the local cycle/core-shell band from v15ac
- local_swap: the growth_seed 202 mode map from v15bk

We keep the stable anchor regime and measure the same relative drift family
that powered v12/v13, especially spectral vs dim drift.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15q_single_defect_recurrence_lab as v15q


ADD_CHORD_RUNS_CSV = Path("Documentation/v15ac_add_chord_core_shell_runs.csv")
LOCAL_SWAP_MODE_CSV = Path("Documentation/v15bk_local_swap_load_stabilizer_mode_rows.csv")

ADD_CHORD_FAMILY = "add_chord_cycle_core_shell_band"
LOCAL_SWAP_FAMILY = "local_swap_growth202_mode_map"

NONTRIVIAL_REL_METRICS = [
    "abs_delta_spectral_radius_rel",
    "abs_delta_dim_proxy_rel",
    "abs_delta_clustering_rel",
    "abs_delta_triangles_rel",
]
SANITY_REL_METRICS = [
    "abs_delta_nodes_rel",
    "abs_delta_beta1_rel",
]
ALL_REL_METRICS = [
    "abs_delta_tokens_rel",
    *SANITY_REL_METRICS,
    "abs_delta_triangles_rel",
    "abs_delta_spectral_radius_rel",
    "abs_delta_clustering_rel",
    "abs_delta_dim_proxy_rel",
]


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


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def add_chord_setup(rows: Sequence[Mapping[str, str]]) -> Tuple[int, int, List[int], List[int]]:
    filtered = [row for row in rows if int(row["placement"]) in (0, 1, 2)]
    target = max({int(row["target_nodes"]) for row in filtered})
    growth_seed = max({int(row["growth_seed"]) for row in filtered})
    placements = sorted({int(row["placement"]) for row in filtered})
    seed_deltas = sorted({int(row["seed_delta"]) for row in filtered})
    return target, growth_seed, placements, seed_deltas


def local_swap_mode_setup(rows: Sequence[Mapping[str, str]]) -> Dict[int, str]:
    mode_map: Dict[int, str] = {}
    for row in rows:
        placement = int(row["placement"])
        mode = str(row["mode"])
        if placement in (1, 2, 3):
            mode_map[placement] = mode
    return dict(sorted(mode_map.items()))


def rel_from_abs(abs_delta: float, initial: float, *, min_floor: float) -> float:
    return abs_delta / max(min_floor, initial)


def relative_drift_fields(last: Mapping[str, Any], base_row: Mapping[str, Any]) -> Dict[str, Any]:
    initial_tokens = max(1.0, safe_float(base_row["initial_tokens"], 1.0))
    initial_nodes = max(1.0, safe_float(base_row["initial_nodes"], 1.0))
    initial_beta1 = max(1.0, safe_float(base_row["initial_beta1"], 1.0))
    initial_triangles = max(1.0, safe_float(base_row["initial_triangles"], 1.0))
    initial_spectral = max(1e-9, safe_float(base_row["initial_spectral_radius"], 1.0))
    initial_dim = max(1e-9, safe_float(base_row["initial_dim_proxy"], 1.0))
    initial_clustering = max(1e-9, safe_float(base_row["initial_clustering"], 1e-9))

    abs_delta_tokens = abs(safe_float(last.get("delta_tokens"), 0.0))
    abs_delta_nodes = abs(safe_float(last.get("delta_nodes"), 0.0))
    abs_delta_beta1 = abs(safe_float(last.get("delta_beta1"), 0.0))
    abs_delta_triangles = abs(safe_float(last.get("delta_triangles"), 0.0))
    abs_delta_spectral = abs(safe_float(last.get("delta_spectral_radius"), 0.0))
    abs_delta_clustering = abs(safe_float(last.get("delta_clustering"), 0.0))
    abs_delta_dim = abs(safe_float(last.get("delta_dim_proxy"), 0.0))

    return {
        "abs_delta_tokens": abs_delta_tokens,
        "abs_delta_nodes": abs_delta_nodes,
        "abs_delta_beta1": abs_delta_beta1,
        "abs_delta_triangles": abs_delta_triangles,
        "abs_delta_spectral_radius": abs_delta_spectral,
        "abs_delta_clustering": abs_delta_clustering,
        "abs_delta_dim_proxy": abs_delta_dim,
        "abs_delta_tokens_rel": rel_from_abs(abs_delta_tokens, initial_tokens, min_floor=1.0),
        "abs_delta_nodes_rel": rel_from_abs(abs_delta_nodes, initial_nodes, min_floor=1.0),
        "abs_delta_beta1_rel": rel_from_abs(abs_delta_beta1, initial_beta1, min_floor=1.0),
        "abs_delta_triangles_rel": rel_from_abs(abs_delta_triangles, initial_triangles, min_floor=1.0),
        "abs_delta_spectral_radius_rel": rel_from_abs(abs_delta_spectral, initial_spectral, min_floor=1e-9),
        "abs_delta_clustering_rel": rel_from_abs(abs_delta_clustering, initial_clustering, min_floor=1e-9),
        "abs_delta_dim_proxy_rel": rel_from_abs(abs_delta_dim, initial_dim, min_floor=1e-9),
    }


def aggregate_group(
    rows: Sequence[Mapping[str, Any]],
    *,
    group_level: str,
    family_name: str,
    group_name: str,
    perturbation: str,
) -> Dict[str, Any]:
    nontrivial_pairs = [
        (metric, mean_defined(safe_float(row[metric]) for row in rows))
        for metric in NONTRIVIAL_REL_METRICS
    ]
    nontrivial_pairs.sort(key=lambda item: item[1])
    rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
    best_metric, best_mean = nontrivial_pairs[0]
    runnerup_metric, runnerup_mean = nontrivial_pairs[1]
    return {
        "group_level": group_level,
        "family_name": family_name,
        "group_name": group_name,
        "perturbation": perturbation,
        "n_runs": len(rows),
        "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "structured_core_shell_rate": mean_defined(
            1.0
            if str(row["core_shell_label"]) in ("stable_core_variable_shell", "dominant_static_core")
            else 0.0
            for row in rows
        ),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "mean_abs_delta_clustering_rel": mean_defined(safe_float(row["abs_delta_clustering_rel"]) for row in rows),
        "mean_abs_delta_triangles_rel": mean_defined(safe_float(row["abs_delta_triangles_rel"]) for row in rows),
        "mean_abs_delta_nodes_rel": mean_defined(safe_float(row["abs_delta_nodes_rel"]) for row in rows),
        "mean_abs_delta_beta1_rel": mean_defined(safe_float(row["abs_delta_beta1_rel"]) for row in rows),
        "best_nontrivial_metric": best_metric,
        "best_nontrivial_mean_relative_drift": best_mean,
        "runnerup_nontrivial_metric": runnerup_metric,
        "runnerup_nontrivial_mean_relative_drift": runnerup_mean,
        "spectral_rank_nontrivial": rank_map["abs_delta_spectral_radius_rel"],
        "dim_rank_nontrivial": rank_map["abs_delta_dim_proxy_rel"],
        "mean_dim_minus_spectral": (
            mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) - safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows)
        ),
        "spectral_lt_dim_rate": mean_defined(
            1.0 if safe_float(row["abs_delta_spectral_radius_rel"]) < safe_float(row["abs_delta_dim_proxy_rel"]) else 0.0
            for row in rows
        ),
        "spectral_lt_clustering_rate": mean_defined(
            1.0 if safe_float(row["abs_delta_spectral_radius_rel"]) < safe_float(row["abs_delta_clustering_rel"]) else 0.0
            for row in rows
        ),
        "spectral_lt_triangles_rate": mean_defined(
            1.0 if safe_float(row["abs_delta_spectral_radius_rel"]) < safe_float(row["abs_delta_triangles_rel"]) else 0.0
            for row in rows
        ),
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_condition: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}
    by_family: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in rows:
        by_condition.setdefault(
            (str(row["family_name"]), str(row["condition_name"]), str(row["perturbation"])),
            [],
        ).append(dict(row))
        by_family.setdefault((str(row["family_name"]), str(row["perturbation"])), []).append(dict(row))

    for (family_name, condition_name, perturbation), group in sorted(by_condition.items()):
        out.append(
            aggregate_group(
                group,
                group_level="condition",
                family_name=family_name,
                group_name=condition_name,
                perturbation=perturbation,
            )
        )

    for (family_name, perturbation), group in sorted(by_family.items()):
        out.append(
            aggregate_group(
                group,
                group_level="family_pool",
                family_name=family_name,
                group_name=f"{family_name}_pool",
                perturbation=perturbation,
            )
        )

    out.append(
        aggregate_group(
            list(rows),
            group_level="global_pool",
            family_name="all_conditional_runs",
            group_name="all_conditional_runs",
            perturbation="mixed",
        )
    )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    agg_map = {(str(row["group_level"]), str(row["group_name"])): dict(row) for row in aggregate}

    add_pool = agg_map[("family_pool", f"{ADD_CHORD_FAMILY}_pool")]
    swap_pool = agg_map[("family_pool", f"{LOCAL_SWAP_FAMILY}_pool")]
    global_pool = agg_map[("global_pool", "all_conditional_runs")]

    add_conditions = [
        dict(row)
        for row in aggregate
        if str(row["group_level"]) == "condition" and str(row["family_name"]) == ADD_CHORD_FAMILY
    ]
    swap_conditions = [
        dict(row)
        for row in aggregate
        if str(row["group_level"]) == "condition" and str(row["family_name"]) == LOCAL_SWAP_FAMILY
    ]
    best_add = max(add_conditions, key=lambda row: safe_float(row["mean_dim_minus_spectral"]))
    best_swap = max(swap_conditions, key=lambda row: safe_float(row["mean_dim_minus_spectral"]))

    add_pool_margin = safe_float(add_pool["mean_dim_minus_spectral"])
    swap_pool_margin = safe_float(swap_pool["mean_dim_minus_spectral"])
    add_best_margin = safe_float(best_add["mean_dim_minus_spectral"])
    swap_best_margin = safe_float(best_swap["mean_dim_minus_spectral"])

    if safe_float(best_add["spectral_rank_nontrivial"]) <= 1 and add_best_margin > add_pool_margin + 0.01:
        add_status = "conditioning_sharpens_spectral"
        add_note = (
            f"Innen add_chord-bandet blir spektral drift skarpere i `{best_add['group_name']}` "
            f"enn i den blandede familie-poolen ({fmt(add_best_margin)} vs {fmt(add_pool_margin)} dim-minus-spectral)."
        )
    elif safe_float(best_add["spectral_rank_nontrivial"]) <= 1:
        add_status = "spectral_best_but_not_much_sharper"
        add_note = (
            f"Spektral drift er fortsatt beste ikke-trivielle kandidat i `{best_add['group_name']}`, "
            "men conditioning gir bare en liten ekstra margin mot den pooled add_chord-familien."
        )
    else:
        add_status = "add_chord_conditional_mixed"
        add_note = "Add_chord-bandet gir fortsatt ikke en ren kondisjonert spektral fordel over de andre ikke-trivielle driftmålene."

    if safe_float(best_swap["spectral_rank_nontrivial"]) <= 1 and swap_best_margin > swap_pool_margin + 0.01:
        swap_status = "conditioning_sharpens_spectral"
        swap_note = (
            f"Innen local_swap-moduskartet blir spektral drift skarpere i `{best_swap['group_name']}` "
            f"enn i den pooled mode-familien ({fmt(swap_best_margin)} vs {fmt(swap_pool_margin)} dim-minus-spectral)."
        )
    elif safe_float(best_swap["spectral_rank_nontrivial"]) <= 1:
        swap_status = "spectral_best_but_not_much_sharper"
        swap_note = (
            f"Spektral drift vinner i `{best_swap['group_name']}`, men conditioning gir bare en svak gevinst utover den pooled local_swap-familien."
        )
    else:
        swap_status = "local_swap_conditional_mixed"
        swap_note = "Local_swap-modiene bryter fortsatt ikke ut en ren spektral kandidat over dim/clustering/triangles."

    shared_add = int(safe_float(best_add["spectral_rank_nontrivial"])) == 1
    shared_swap = int(safe_float(best_swap["spectral_rank_nontrivial"])) == 1
    if shared_add and shared_swap:
        cross_status = "shared_family_level_spectral_candidate"
        cross_note = (
            f"Bade add_chord (`{best_add['group_name']}`) og local_swap (`{best_swap['group_name']}`) "
            "har nå minst ett kondisjonert delsignal der spektral drift er beste ikke-trivielle kandidat."
        )
        next_step = "carrier_first_cross_family_validation"
        next_note = "Neste steg bor teste om denne spektrale kandidaten holder under en liten carrier-first sammenlikning pa tvers av perturbasjonstyper."
    elif shared_add or shared_swap:
        winner = best_add if shared_add else best_swap
        cross_status = "family_specific_spectral_candidate"
        cross_note = (
            f"Det beste spektrale delsignalet er fortsatt familiespesifikt og sitter forelopig i `{winner['group_name']}`, "
            "ikke som en delt kandidat pa tvers av carrier-typer."
        )
        next_step = "stay_with_winning_family"
        next_note = "Neste steg bor ga ett hakk dypere i den vinnende familien i stedet for a gjenapne brede globale quasi-invariant-scans."
    else:
        cross_status = "conditional_signal_still_mixed"
        cross_note = (
            "Conditioning gjor familiene mer lesbare, men gir fortsatt ikke en delt spektral kandidat "
            "som slar dim/clustering/triangles pa tvers av disse lokale carrier-sporene."
        )
        next_step = "change_conditional_basis"
        next_note = "Neste steg bor bytte conditioning-akse eller observabel, ikke bare oke budsjettet pa samme oppsett."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle reruns matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "zero_sanity_metrics",
            "status": "do_not_read_as_laws",
            "note": (
                f"Globalt holder nodes/beta1 fortsatt lavest drift ({fmt(global_pool['mean_abs_delta_nodes_rel'])} / "
                f"{fmt(global_pool['mean_abs_delta_beta1_rel'])}), men de skal fortsatt behandles som sanity-metrikker, ikke nye lover."
            ),
        },
        {
            "diagnostic_family": "add_chord_conditional_signal",
            "status": add_status,
            "note": add_note,
        },
        {
            "diagnostic_family": "local_swap_conditional_signal",
            "status": swap_status,
            "note": swap_note,
        },
        {
            "diagnostic_family": "cross_family_reading",
            "status": cross_status,
            "note": cross_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    family_pools = [row for row in aggregate if str(row["group_level"]) == "family_pool"]
    conditions = [row for row in aggregate if str(row["group_level"]) == "condition"]

    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bl: conditional quasi-invariant lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden gar tilbake til quasi-invariant-sporet, men condition-er pa de lokale mesoskopiske familiene som faktisk har overlevd i defect-sporet, i stedet for a blande alle run sammen.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated | mean dim proxy |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} | {fmt(row['mean_initial_dim_proxy'])} |"
        )
    lines.append("")
    lines.append("## Familie-pools")
    lines.append("")
    lines.append("| family pool | n | spectral | dim | clustering | triangles | best non-trivial | spectral rank | dim-spectral | spectral<dim |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in family_pools:
        lines.append(
            f"| {row['group_name']} | {int(row['n_runs'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {fmt(row['mean_abs_delta_clustering_rel'])} | {fmt(row['mean_abs_delta_triangles_rel'])} | {row['best_nontrivial_metric']} | {int(row['spectral_rank_nontrivial'])} | {fmt(row['mean_dim_minus_spectral'])} | {fmt(row['spectral_lt_dim_rate'])} |"
        )
    lines.append("")
    lines.append("## Kondisjonerte delsignaler")
    lines.append("")
    lines.append("| condition | family | n | exact return | coarse return | spectral | dim | best non-trivial | spectral rank | dim-spectral |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(conditions, key=lambda r: (str(r["family_name"]), str(r["group_name"]))):
        lines.append(
            f"| {row['group_name']} | {row['family_name']} | {int(row['n_runs'])} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {row['best_nontrivial_metric']} | {int(row['spectral_rank_nontrivial'])} | {fmt(row['mean_dim_minus_spectral'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten conditional lab, ikke en ny global invariant-scan.")
    lines.append("- `nodes` og `beta1` rapporteres fortsatt bare som sanity-metrikker; de skal ikke oppgraderes til lover av denne runden.")
    lines.append("- Et positivt signal her bor leses som familiespesifikk eller carrier-spesifikk sharpening, ikke som universell spacetime- eller Lorentz-likhet.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bl conditional quasi-invariant lab.")
    p.add_argument("--in-add-chord-runs-csv", type=str, default=str(ADD_CHORD_RUNS_CSV))
    p.add_argument("--in-local-swap-mode-csv", type=str, default=str(LOCAL_SWAP_MODE_CSV))
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bl_conditional_quasi_invariant_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bl_conditional_quasi_invariant_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bl_conditional_quasi_invariant_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bl_conditional_quasi_invariant_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bl_conditional_quasi_invariant_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bl_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bl.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    add_rows = read_csv(Path(args.in_add_chord_runs_csv))
    mode_rows = read_csv(Path(args.in_local_swap_mode_csv))
    add_target, add_growth_seed, add_placements, seed_deltas = add_chord_setup(add_rows)
    local_mode_map = local_swap_mode_setup(mode_rows)
    local_target = 96
    local_growth_seed = 202

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([add_target, local_target])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [add_growth_seed])
    base_lookup = {(str(row["ensemble"]), int(row["growth_seed"])): dict(row) for row in base_rows}
    ensemble_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    rows: List[Dict[str, Any]] = []

    add_base = base_states[(ensemble_by_target[add_target].name, add_growth_seed)]
    add_base_row = base_lookup[(ensemble_by_target[add_target].name, add_growth_seed)]
    for placement in add_placements:
        for seed_delta in seed_deltas:
            run_seed = add_target * 100000 + add_growth_seed * 1000 + int(placement) + int(seed_delta)
            res = v15q.run_defect_with_sets(
                add_base,
                params=params,
                seed=run_seed,
                steps=v15ac.FULL_STEPS,
                perturbation="add_chord",
                center_token_index=int(placement),
                local_coupling="maximal",
                log_every=v15ac.LOG_EVERY,
            )
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            full_label = v15q.classify_recurrence_label(int(res["summary"]["final_alive"]), recurrence)
            info = dict(res["perturbation_info"])
            support = list(info.get("support", []))
            core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
            drift = relative_drift_fields(res["log_rows"][-1], add_base_row)
            rows.append(
                {
                    "perturbation": "add_chord",
                    "family_name": ADD_CHORD_FAMILY,
                    "condition_name": f"cycle_band_p{int(placement)}",
                    "target_nodes": add_target,
                    "growth_seed": add_growth_seed,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "core_shell_label": str(core_shell["label"]),
                    "full_label": full_label,
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    **drift,
                }
            )

    local_base = base_states[(ensemble_by_target[local_target].name, local_growth_seed)]
    local_base_row = base_lookup[(ensemble_by_target[local_target].name, local_growth_seed)]
    for placement, mode in local_mode_map.items():
        for seed_delta in seed_deltas:
            run_seed = local_target * 100000 + local_growth_seed * 1000 + int(placement) + int(seed_delta)
            res = v15q.run_defect_with_sets(
                local_base,
                params=params,
                seed=run_seed,
                steps=v15q.STEPS,
                perturbation="local_swap",
                center_token_index=int(placement),
                local_coupling="maximal",
                log_every=v15q.LOG_EVERY,
            )
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            full_label = v15q.classify_recurrence_label(int(res["summary"]["final_alive"]), recurrence)
            info = dict(res["perturbation_info"])
            support = list(info.get("support", []))
            core_shell = v15aw.core_shell_metrics(res["damaged_sets"], support)
            drift = relative_drift_fields(res["log_rows"][-1], local_base_row)
            rows.append(
                {
                    "perturbation": "local_swap",
                    "family_name": LOCAL_SWAP_FAMILY,
                    "condition_name": mode,
                    "target_nodes": local_target,
                    "growth_seed": local_growth_seed,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("local_swap", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "core_shell_label": str(core_shell["label"]),
                    "full_label": full_label,
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    **drift,
                }
            )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in (add_target, local_target)]
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bl operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en conditional quasi-invariant test pa lokale carrier-familier, ikke som en ny global lovtest.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bl",
            "",
            "Denne runden tester om de gamle quasi-invariant-kandidatene blir tydeligere hvis vi bare ser pa bestemte lokale skadetyper i stedet for a blande alt sammen.",
            "",
            "Poenget er ikke a bevise en ny universell lov med en gang, men a se om noen familier holder formen sin litt bedre enn andre nar vi maler dem med de samme geometri-driftmalene som tidligere.",
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
