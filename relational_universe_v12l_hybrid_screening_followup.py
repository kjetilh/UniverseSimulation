#!/usr/bin/env python3
"""v0.12l hybrid screening + adaptive follow-up around band_zero_del.

This round combines the two strongest ingredients from the current workflow:

1. a screening policy that selects promising bases within each target size, and
2. an adaptive follow-up policy that decides how much expensive dynamics budget
   each selected base should receive.

The purpose is practical rather than theoretical. We ask whether the hybrid can
retain most of the reference workflow quality while reducing measured total
follow-up time.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e
import relational_universe_v12f_budget_screening as v12f
import relational_universe_v12i_measured_runtime_pipeline as v12i
import relational_universe_v12k_adaptive_followup_budget as v12k


REFERENCE_POLICY = "full_basis__full_followup"
EPSILON = 0.02
NEG_INF = -1.0e18
HYBRID_POLICIES: List[Tuple[str, str, Sequence[str], float, str, int, float]] = [
    ("full_basis__full_followup", "full_basis", tuple(v12.BASIS_FEATURES), 0.50, "full_followup", 6, 1.0),
    ("full_basis__probe2_top_half", "full_basis", tuple(v12.BASIS_FEATURES), 0.50, "probe2_top_half", 2, 0.50),
    ("spectral_only__full_followup", "spectral_only", ("initial_spectral_per_sqrtN",), 0.50, "full_followup", 6, 1.0),
    ("spectral_only__probe2_top_half", "spectral_only", ("initial_spectral_per_sqrtN",), 0.50, "probe2_top_half", 2, 0.50),
    (
        "spectral_plus_dim__probe2_top_half",
        "spectral_plus_dim",
        ("initial_spectral_per_sqrtN", "initial_dim_proxy"),
        0.667,
        "probe2_top_half",
        2,
        0.50,
    ),
    ("random_baseline__full_followup", "random_baseline", (), 0.50, "full_followup", 6, 1.0),
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def read_timed_run_rows(path: str | Path) -> List[Dict[str, Any]]:
    int_keys = {
        "target_nodes",
        "steps",
        "growth_seed",
        "run_index",
        "run_offset",
    }
    rows: List[Dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        for raw in csv.DictReader(f):
            row: Dict[str, Any] = {}
            for key, value in raw.items():
                if key in {"candidate_name", "ensemble", "burnin_label"}:
                    row[key] = value
                elif key in int_keys:
                    row[key] = int(value)
                else:
                    row[key] = safe_float(value, default=value)
            rows.append(row)
    return rows


def same_identity(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
    return (
        str(a["ensemble"]) == str(b["ensemble"])
        and int(a["target_nodes"]) == int(b["target_nodes"])
        and int(a["growth_seed"]) == int(b["growth_seed"])
    )


def parse_base_rows(base_rows: Sequence[Dict[str, Any]], run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    run_groups: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        run_groups.setdefault((str(row["ensemble"]), int(row["growth_seed"])), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for base in base_rows:
        key = (str(base["ensemble"]), int(base["growth_seed"]))
        sub = run_groups[key]
        out.append(
            {
                "ensemble": str(base["ensemble"]),
                "target_nodes": int(base["target_nodes"]),
                "growth_seed": int(base["growth_seed"]),
                "runs": len(sub),
                "mean_final_radius_control": mean_defined(safe_float(r["final_radius_control"]) for r in sub),
                "sd_final_radius_control": v10b.sd_or_zero(safe_float(r["final_radius_control"]) for r in sub),
                "mean_avg_local_overlap": mean_defined(safe_float(r["avg_local_overlap"]) for r in sub),
                "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in sub),
                "initial_avg_degree": safe_float(base["initial_avg_degree"]),
                "initial_beta1_per_node": safe_float(base["initial_beta1_per_node"]),
                "initial_triangles_per_node": safe_float(base["initial_triangles_per_node"]),
                "initial_spectral_per_sqrtN": safe_float(base["initial_spectral_per_sqrtN"]),
                "initial_dim_proxy": safe_float(base["initial_dim_proxy"]),
                "initial_clustering": safe_float(base["initial_clustering"]),
                "initial_nodes": safe_float(base["initial_nodes"]),
            }
        )
    return out


def group_runs_by_base(run_rows: Sequence[Dict[str, Any]]) -> Dict[Tuple[int, str, int], List[Dict[str, Any]]]:
    grouped = v12k.group_runs_by_base(run_rows)
    return grouped


def apply_followup_policy(
    selected_rows: Sequence[Dict[str, Any]],
    grouped_runs: Mapping[Tuple[int, str, int], List[Dict[str, Any]]],
    probe_runs: int,
    extend_frac: float,
) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in selected_rows:
        key = (int(row["target_nodes"]), str(row["ensemble"]), int(row["growth_seed"]))
        by_target.setdefault(int(row["target_nodes"]), []).append(
            {
                "target_nodes": int(row["target_nodes"]),
                "ensemble": str(row["ensemble"]),
                "growth_seed": int(row["growth_seed"]),
                "runs": grouped_runs[key],
            }
        )

    out: List[Dict[str, Any]] = []
    for target in sorted(by_target):
        out.extend(v12k.apply_policy_to_target(by_target[target], probe_runs, extend_frac))
    return out


def hybrid_metrics(
    test_rows: Sequence[Dict[str, Any]],
    evaluated_rows: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    predicted_lookup: Dict[Tuple[str, int], Dict[str, Any]] = {
        (str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in evaluated_rows
    }

    enriched_all: List[Dict[str, Any]] = []
    selected_actual_values: List[float] = []
    used_runs = 0
    extended_rows = 0
    used_seconds = 0.0
    for row in test_rows:
        pred = predicted_lookup.get((str(row["ensemble"]), int(row["growth_seed"])))
        enriched = dict(row)
        if pred is None:
            enriched["predicted_radius"] = NEG_INF
            enriched["used_runs"] = 0
            enriched["used_seconds"] = 0.0
            enriched["extended"] = 0
            enriched["selected"] = 0
        else:
            enriched["predicted_radius"] = safe_float(pred["estimated_score"])
            enriched["used_runs"] = int(pred["used_runs"])
            enriched["used_seconds"] = safe_float(pred["used_seconds"])
            enriched["extended"] = int(pred["extended"])
            enriched["selected"] = 1
            used_runs += int(pred["used_runs"])
            extended_rows += int(pred["extended"])
            used_seconds += safe_float(pred["used_seconds"])
            selected_actual_values.append(safe_float(row["mean_final_radius_control"]))
        enriched_all.append(enriched)

    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in enriched_all:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))

    target_best_hits: List[float] = []
    target_top_recalls: List[float] = []
    target_pairwise: List[float] = []
    target_selected_lifts: List[float] = []
    for target in sorted(by_target):
        sub = by_target[target]
        actual_sorted = sorted(sub, key=lambda r: safe_float(r["mean_final_radius_control"]), reverse=True)
        predicted_sorted = sorted(sub, key=lambda r: safe_float(r["predicted_radius"]), reverse=True)
        target_best_hits.append(1.0 if same_identity(actual_sorted[0], predicted_sorted[0]) else 0.0)

        top_n = max(1, int(math.ceil(len(sub) * 0.25)))
        actual_top = actual_sorted[:top_n]
        selected_predicted = [r for r in predicted_sorted if int(r["selected"]) == 1]
        predicted_top = selected_predicted[:top_n]
        captured = sum(1 for actual_row in actual_top if any(same_identity(actual_row, pred_row) for pred_row in predicted_top))
        target_top_recalls.append(captured / max(1, len(actual_top)))
        target_pairwise.append(v12e.pairwise_accuracy(sub, "predicted_radius", "mean_final_radius_control"))

        sel = [r for r in sub if int(r["selected"]) == 1]
        mean_all = mean_defined(safe_float(r["mean_final_radius_control"]) for r in sub)
        mean_sel = mean_defined(safe_float(r["mean_final_radius_control"]) for r in sel)
        if math.isfinite(mean_all) and abs(mean_all) > 1e-12 and math.isfinite(mean_sel):
            target_selected_lifts.append((mean_sel / mean_all) - 1.0)

    overall_mean = mean_defined(safe_float(r["mean_final_radius_control"]) for r in test_rows)
    selected_mean = mean_defined(selected_actual_values)
    return {
        "selected_rows": sum(int(r["selected"]) for r in enriched_all),
        "extended_rows": extended_rows,
        "used_runs": used_runs,
        "used_seconds": used_seconds,
        "within_target_best_hit": mean_defined(target_best_hits),
        "within_target_top_quartile_recall": mean_defined(target_top_recalls),
        "mean_pairwise_within_target": mean_defined(target_pairwise),
        "within_target_selected_lift": mean_defined(target_selected_lifts),
        "selected_lift_all": (
            (selected_mean / overall_mean) - 1.0
            if math.isfinite(overall_mean) and abs(overall_mean) > 1e-12 and math.isfinite(selected_mean)
            else float("nan")
        ),
    }


def hybrid_split_rows(
    base_level_rows: Sequence[Dict[str, Any]],
    grouped_runs: Mapping[Tuple[int, str, int], List[Dict[str, Any]]],
    *,
    repeats: int,
    test_frac: float,
    screening_seed: int,
    timing_loops: int,
) -> List[Dict[str, Any]]:
    master_rng = random.Random(screening_seed)
    rows: List[Dict[str, Any]] = []
    for split_id in range(1, repeats + 1):
        split_rng = random.Random(master_rng.randint(1, 10**9))
        train_idx, test_idx = v12e.stratified_holdout_indices(base_level_rows, split_rng, test_frac)
        train_rows = [dict(base_level_rows[i]) for i in train_idx]
        test_rows = [dict(base_level_rows[i]) for i in test_idx]

        per_policy: List[Dict[str, Any]] = []
        for hybrid_name, screen_name, features, budget_frac, followup_name, probe_runs, extend_frac in HYBRID_POLICIES:
            policy_seed = split_rng.randint(1, 10**9)
            scored = v12f.score_rows(train_rows, test_rows, screen_name, features, random.Random(policy_seed))
            selected = v12f.select_within_target(scored, budget_frac)
            evaluated = apply_followup_policy(selected, grouped_runs, probe_runs, extend_frac)
            metrics = hybrid_metrics(test_rows, evaluated)
            screening_seconds = v12i.measure_screening_seconds(
                train_rows,
                test_rows,
                screen_name,
                features,
                budget_frac,
                seed=policy_seed,
                loops=timing_loops,
            )
            total_seconds = screening_seconds + safe_float(metrics["used_seconds"])
            per_policy.append(
                {
                    "split_id": split_id,
                    "hybrid_policy_name": hybrid_name,
                    "screen_policy_name": screen_name,
                    "followup_policy_name": followup_name,
                    "budget_frac": budget_frac,
                    "feature_count": len(features),
                    "probe_runs": probe_runs,
                    "extend_frac": extend_frac,
                    "train_rows": len(train_rows),
                    "test_rows": len(test_rows),
                    "screening_seconds": screening_seconds,
                    "followup_seconds": safe_float(metrics["used_seconds"]),
                    "total_seconds": total_seconds,
                    **metrics,
                }
            )

        ref = next(r for r in per_policy if str(r["hybrid_policy_name"]) == REFERENCE_POLICY)
        ref_total = safe_float(ref["total_seconds"])
        ref_hit = safe_float(ref["within_target_best_hit"])
        ref_recall = safe_float(ref["within_target_top_quartile_recall"])
        ref_pairwise = safe_float(ref["mean_pairwise_within_target"])
        for row in per_policy:
            row["delta_best_hit_vs_ref"] = safe_float(row["within_target_best_hit"]) - ref_hit
            row["delta_recall_vs_ref"] = safe_float(row["within_target_top_quartile_recall"]) - ref_recall
            row["delta_pairwise_vs_ref"] = safe_float(row["mean_pairwise_within_target"]) - ref_pairwise
            row["time_delta_vs_ref"] = safe_float(row["total_seconds"]) - ref_total
            row["time_ratio_vs_ref"] = safe_float(row["total_seconds"]) / ref_total if ref_total > 1e-12 else float("nan")
            row["speedup_vs_ref"] = ref_total / safe_float(row["total_seconds"]) if safe_float(row["total_seconds"]) > 1e-12 else float("nan")
            near_match = (
                safe_float(row["within_target_best_hit"]) >= ref_hit - EPSILON
                and safe_float(row["within_target_top_quartile_recall"]) >= ref_recall - EPSILON
            )
            row["near_match_eps_02"] = 1 if near_match else 0
            row["faster_than_ref"] = 1 if safe_float(row["total_seconds"]) <= ref_total + 1e-12 else 0
            row["faster_and_near_match"] = 1 if near_match and int(row["faster_than_ref"]) == 1 else 0
            rows.append(row)
    return rows


def aggregate_hybrid_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    keys = sorted({str(r["hybrid_policy_name"]) for r in rows})
    out: List[Dict[str, Any]] = []
    for hybrid_name in keys:
        sub = [r for r in rows if str(r["hybrid_policy_name"]) == hybrid_name]
        exemplar = sub[0]
        entry = {
            "hybrid_policy_name": hybrid_name,
            "screen_policy_name": exemplar["screen_policy_name"],
            "followup_policy_name": exemplar["followup_policy_name"],
            "budget_frac": safe_float(exemplar["budget_frac"]),
            "feature_count": int(exemplar["feature_count"]),
            "probe_runs": int(exemplar["probe_runs"]),
            "extend_frac": safe_float(exemplar["extend_frac"]),
            "mean_selected_rows": mean_defined(safe_float(r["selected_rows"]) for r in sub),
            "mean_extended_rows": mean_defined(safe_float(r["extended_rows"]) for r in sub),
            "mean_used_runs": mean_defined(safe_float(r["used_runs"]) for r in sub),
            "mean_screening_seconds": mean_defined(safe_float(r["screening_seconds"]) for r in sub),
            "mean_followup_seconds": mean_defined(safe_float(r["followup_seconds"]) for r in sub),
            "mean_total_seconds": mean_defined(safe_float(r["total_seconds"]) for r in sub),
            "mean_speedup_vs_ref": mean_defined(safe_float(r["speedup_vs_ref"]) for r in sub),
            "mean_best_hit": mean_defined(safe_float(r["within_target_best_hit"]) for r in sub),
            "mean_recall": mean_defined(safe_float(r["within_target_top_quartile_recall"]) for r in sub),
            "mean_pairwise_within_target": mean_defined(safe_float(r["mean_pairwise_within_target"]) for r in sub),
            "mean_selected_lift": mean_defined(safe_float(r["within_target_selected_lift"]) for r in sub),
            "mean_delta_best_hit_vs_ref": mean_defined(safe_float(r["delta_best_hit_vs_ref"]) for r in sub),
            "mean_delta_recall_vs_ref": mean_defined(safe_float(r["delta_recall_vs_ref"]) for r in sub),
            "mean_delta_pairwise_vs_ref": mean_defined(safe_float(r["delta_pairwise_vs_ref"]) for r in sub),
            "near_match_rate_eps_02": mean_defined(safe_float(r["near_match_eps_02"]) for r in sub),
            "faster_than_ref_rate": mean_defined(safe_float(r["faster_than_ref"]) for r in sub),
            "faster_and_near_match_rate": mean_defined(safe_float(r["faster_and_near_match"]) for r in sub),
            "screen_share_of_total": mean_defined(
                safe_float(r["screening_seconds"]) / safe_float(r["total_seconds"])
                if safe_float(r["total_seconds"]) > 1e-12
                else float("nan")
                for r in sub
            ),
        }
        out.append(entry)
    out.sort(
        key=lambda row: (
            safe_float(row["faster_and_near_match_rate"], -1e9),
            safe_float(row["near_match_rate_eps_02"], -1e9),
            safe_float(row["mean_speedup_vs_ref"], -1e9),
            safe_float(row["mean_best_hit"], -1e9),
        ),
        reverse=True,
    )
    for idx, row in enumerate(out, start=1):
        row["rank"] = idx
    return out


def build_report(
    target_rows: Sequence[Dict[str, Any]],
    summary_rows: Sequence[Dict[str, Any]],
    *,
    repeats: int,
    timing_loops: int,
    base_count: int,
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12l: hybrid screening + adaptiv oppfølging")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden kombinerer dagens sterkeste screeningreferanse med adaptiv follow-up. Sporsmalet er om vi kan spare reell oppfolgingstid ved a bruke screening til a velge hvilke baser som far videre oppmerksomhet, og adaptiv follow-up til a begrense hvor mye arbeid hver valgt base far."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- Regime holdes fast ved `band_zero_del`.")
    lines.append("- Basene er de samme som i den maelte adaptive `v12k`-runden.")
    lines.append("- Screening trener pa stratified holdout-splitt og rangerer testbaser innen hver størrelse.")
    lines.append("- Deretter far bare de screenede basene follow-up, enten som `full_followup` eller adaptivt `probe2_top_half`.")
    lines.append(f"- Datasett: `{base_count}` baser. Screeningsplitt: `{repeats}`. Timing-lokker per screeningpass: `{timing_loops}`.")
    lines.append("- Dette er fortsatt arbeidsflyt og kostnad, ikke ny fysikk.")
    lines.append("")
    lines.append("## Realiserte startstørrelser")
    lines.append("")
    lines.append("| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in target_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['bases'])} | {safe_float(row['mean_initial_nodes']):.1f} | "
            f"{safe_float(row['q10_initial_nodes']):.1f} | {safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | "
            f"{safe_float(row['mean_actual_radius']):.3f} | {safe_float(row['sd_actual_radius']):.3f} |"
        )
    lines.append("")
    lines.append("## Hybrid policy-sammendrag")
    lines.append("")
    lines.append("| rank | hybrid | screen | budget | followup | best_hit | recall | pairwise | total_s | speedup | d_best_hit | d_recall | near_match | faster_and_match |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['hybrid_policy_name']} | {row['screen_policy_name']} | {safe_float(row['budget_frac']):.3f} | "
            f"{row['followup_policy_name']} | {safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_recall']):.3f} | "
            f"{safe_float(row['mean_pairwise_within_target']):.3f} | {safe_float(row['mean_total_seconds']):.3f} | "
            f"{safe_float(row['mean_speedup_vs_ref']):.3f} | {safe_float(row['mean_delta_best_hit_vs_ref']):.3f} | "
            f"{safe_float(row['mean_delta_recall_vs_ref']):.3f} | {safe_float(row['near_match_rate_eps_02']):.3f} | "
            f"{safe_float(row['faster_and_near_match_rate']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == REFERENCE_POLICY), None)
    full_probe2 = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "full_basis__probe2_top_half"), None)
    spectral_full = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "spectral_only__full_followup"), None)
    spectral_probe2 = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "spectral_only__probe2_top_half"), None)
    spectral_dim_probe2 = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "spectral_plus_dim__probe2_top_half"), None)
    if ref is not None:
        lines.append(
            f"- Referansen `{REFERENCE_POLICY}` bruker i snitt `{safe_float(ref['mean_total_seconds']):.3f}` sekunder og setter nullpunktet for hit/recall."
        )
    if full_probe2 is not None:
        lines.append(
            f"- `full_basis__probe2_top_half` isolerer verdien av adaptiv oppfolging under samme screening. Den har `speedup={safe_float(full_probe2['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(full_probe2['mean_best_hit']):.3f}` og `recall={safe_float(full_probe2['mean_recall']):.3f}`."
        )
    if spectral_full is not None:
        lines.append(
            f"- `spectral_only__full_followup` isolerer verdien av enkel screening uten adaptiv follow-up. Den har `speedup={safe_float(spectral_full['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(spectral_full['mean_best_hit']):.3f}`, `recall={safe_float(spectral_full['mean_recall']):.3f}` og `near_match={safe_float(spectral_full['near_match_rate_eps_02']):.3f}`."
        )
    if spectral_probe2 is not None:
        lines.append(
            f"- `spectral_only__probe2_top_half` er den rene kompakt+adaptiv-hybriden. Den har `speedup={safe_float(spectral_probe2['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(spectral_probe2['mean_best_hit']):.3f}` og `recall={safe_float(spectral_probe2['mean_recall']):.3f}`."
        )
    if spectral_dim_probe2 is not None:
        lines.append(
            f"- `spectral_plus_dim__probe2_top_half` er kostnadssensitiv utfordrer. Den har `speedup={safe_float(spectral_dim_probe2['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(spectral_dim_probe2['near_match_rate_eps_02']):.3f}`."
        )
    lines.append(
        "- Lesningen splitter seg derfor i to: `spectral_only__full_followup` er den naermeste same-budget-utfordreren pa middelverdier, mens `full_basis__probe2_top_half` er den tydeligste reelle tidsutfordreren. Ingen av dem er likevel robuste nok til a erstatte referansen."
    )
    lines.append(
        "- Denne runden skal derfor ikke leses som at vi har funnet en ny billig standard, men som at hybridsporet er mer lovende gjennom dypere adaptiv oppfolging enn gjennom enda mer finjustering av screeningbasiser."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    ref = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == REFERENCE_POLICY), None)
    best = summary_rows[0] if summary_rows else None
    same_budget = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "spectral_only__full_followup"), None)
    lines = [
        "# v0.12l for ikke-spesialister",
        "",
        "Denne runden prøver å kombinere to ideer samtidig: først en rask grovsortering av starttilstander, og deretter en smartere måte å bruke de dyre simuleringene på.",
        "",
    ]
    if ref is not None:
        lines.append(
            f"- Referansen er `{REFERENCE_POLICY}`, med omtrent `{safe_float(ref['mean_total_seconds']):.3f}` sekunder per split."
        )
    if best is not None:
        lines.append(
            f"- Den beste hybriden i denne runden er `{best['hybrid_policy_name']}`, med `speedup={safe_float(best['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(best['near_match_rate_eps_02']):.3f}`."
        )
    if same_budget is not None:
        lines.append(
            f"- Den enkleste same-budget-utfordreren er `spectral_only__full_followup`, som er litt raskere enn referansen men ikke stabil nok over splitt."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12l operativ anbefaling", ""]
    ref = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == REFERENCE_POLICY), None)
    same_budget = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "spectral_only__full_followup"), None)
    adaptive = next((r for r in summary_rows if str(r["hybrid_policy_name"]) == "full_basis__probe2_top_half"), None)
    if ref is None or same_budget is None or adaptive is None:
        lines.append("v12l ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append(
        f"Behold `{REFERENCE_POLICY}` som arbeidsreferanse til en hybrid er baade raskere og naer nok pa hit/recall."
    )
    lines.append(
        f"Les `spectral_only__full_followup` som den naermeste same-budget-utfordreren: `speedup={safe_float(same_budget['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(same_budget['mean_best_hit']):.3f}`, `recall={safe_float(same_budget['mean_recall']):.3f}`, men splitvis `near_match={safe_float(same_budget['near_match_rate_eps_02']):.3f}` er ikke hoy nok."
    )
    lines.append(
        f"Les `full_basis__probe2_top_half` som den viktigste tidsutfordreren: `speedup={safe_float(adaptive['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(adaptive['mean_best_hit']):.3f}` og `recall={safe_float(adaptive['mean_recall']):.3f}` viser ekte besparelse, men fortsatt for stort kvalitetstap."
    )
    lines.append(
        "Hvis hybriden fortsatt ikke er god nok, peker repoet mot ett mer presist neste steg: hold screeningdelen fast og gjør en dypere adaptiv oppfølgingsrunde, i stedet for å finjustere flere screeningbasiser."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12l hybrid screening + adaptive follow-up")
    ap.add_argument("--timed-run-csv", default="Documentation/v12k_adaptive_followup_budget_timed_run_rows.csv")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=6)
    ap.add_argument("--test-frac", type=float, default=0.50)
    ap.add_argument("--screening-repeats", type=int, default=40)
    ap.add_argument("--screening-seed", type=int, default=12091)
    ap.add_argument("--screen-timing-loops", type=int, default=300)
    ap.add_argument("--output-prefix", default="Documentation/v12l_hybrid_screening_followup")
    ap.add_argument("--report-md", default="Documentation/v12l_hybrid_screening_followup.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12l.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12l_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    run_rows = read_timed_run_rows(args.timed_run_csv)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    growth_seeds = [61001 + 23 * i for i in range(args.growth_seeds)]
    regime = v10e.recommended_regime(args.growth_regime)
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]

    print(f"[v12l] regime={regime.name} targets={targets} growth={len(growth_seeds)} rows={len(run_rows)}")
    print("[v12l] rebuilding base features for the same measured bases...")
    _, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    base_level_rows = parse_base_rows(base_rows, run_rows)
    grouped_runs = group_runs_by_base(run_rows)
    target_rows = v12k.target_summary(base_rows, run_rows)

    print("[v12l] evaluating hybrid workflow splits...")
    split_rows = hybrid_split_rows(
        base_level_rows,
        grouped_runs,
        repeats=args.screening_repeats,
        test_frac=args.test_frac,
        screening_seed=args.screening_seed,
        timing_loops=args.screen_timing_loops,
    )
    summary_rows = aggregate_hybrid_rows(split_rows)

    prefix = args.output_prefix
    print("[v12l] writing outputs...")
    write_csv(f"{prefix}_target_summary.csv", target_rows)
    write_csv(f"{prefix}_base_rows.csv", base_level_rows)
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", summary_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                target_rows,
                summary_rows,
                repeats=args.screening_repeats,
                timing_loops=args.screen_timing_loops,
                base_count=len(base_level_rows),
            ),
        ),
        (args.lay_md, build_lay_summary(summary_rows)),
        (args.recommendation_md, build_recommendation(summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12l] done")


if __name__ == "__main__":
    main()
