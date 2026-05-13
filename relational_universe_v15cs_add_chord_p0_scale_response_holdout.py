#!/usr/bin/env python3
"""v0.15cs add_chord p0 scale-response holdout.

v15cr downgraded p2 as a scale selector and identified a more interesting
control-derived clue: add_chord_p0 had a far-shell horizon that grew across the
768 -> 896 -> 1024 ladder. This lab does not claim that p0 is a law or a
particle. It asks the narrow holdout question:

does the add_chord_p0 far-shell response survive fresh seed deltas at targets
896 and 1024 strongly enough to become the next scale-response candidate?

Design:
- regime: band_zero_del
- growth seed: 202
- targets: 896, 1024
- budgets: scaled from the target-768 step budget
- primary profile: add_chord_p0
- controls: add_chord_p2 and local_swap_p0
- fresh seed deltas: not reused from v15cn/v15cp/v15cq
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGETS = (896, 1024)
REFERENCE_TARGET = 768
REFERENCE_STEPS = v15ac.FULL_STEPS
GROWTH_SEED = v15cn.GROWTH_SEED
LOG_EVERY = v15ac.LOG_EVERY

PRIMARY_PROFILE = ("add_chord", 0)
CONTROL_PROFILES = (("add_chord", 2), ("local_swap", 0))
PROFILES = (PRIMARY_PROFILE, *CONTROL_PROFILES)
FRESH_SEED_DELTAS = (6203, 6269)

HISTORICAL_LADDER_CSV = Path("Documentation/v15cq_intermediate_scale_ladder.csv")


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def scaled_steps_for_target(target: int) -> int:
    return int(math.ceil(REFERENCE_STEPS * int(target) / REFERENCE_TARGET))


def profile_label(perturbation: str, placement: int) -> str:
    return f"{perturbation}_p{int(placement)}"


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def analyze_run(
    *,
    target: int,
    base_state: Any,
    base_row: Mapping[str, Any],
    perturbation: str,
    placement: int,
    seed_delta: int,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    steps = scaled_steps_for_target(target)
    run_seed = v15cn.run_seed_for(
        target=target,
        perturbation=perturbation,
        placement=placement,
        seed_delta=seed_delta,
    )
    res = v15q.run_defect_with_sets(
        base_state,
        params=params,
        seed=run_seed,
        steps=steps,
        perturbation=perturbation,
        center_token_index=placement,
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
    info = dict(res["perturbation_info"])
    support = [int(x) for x in info.get("support", [])]
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(res["log_rows"]))))
    tail_series = v15cn.raw_far_shell_tail_series(base_state, support, res["damaged_sets"][tail_start:])
    horizon = v15cn.horizon_fields(tail_series)
    drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    return {
        "profile_role": "primary" if (perturbation, placement) == PRIMARY_PROFILE else "control",
        "profile_label": profile_label(perturbation, placement),
        "perturbation": perturbation,
        "target_nodes": int(target),
        "reference_target_nodes": REFERENCE_TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "reference_step_budget": int(REFERENCE_STEPS),
        "step_budget": int(steps),
        "budget_scale_factor": float(int(target) / REFERENCE_TARGET),
        "log_every": int(LOG_EVERY),
        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
        "support_signature": ",".join(str(x) for x in support),
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
        "mean_far_shell_share": mean_defined(safe_float(row["far_shell_share"]) for row in tail_series),
        "q90_far_shell_share": v15.quantile([safe_float(row["far_shell_share"]) for row in tail_series], 0.90)
        if tail_series
        else float("nan"),
        "mean_weighted_mean_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in tail_series),
        "max_weighted_mean_distance": max((safe_float(row["weighted_mean_distance"]) for row in tail_series), default=float("nan")),
        **horizon,
        **drift,
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        for perturbation, placement in PROFILES:
            group = [
                row
                for row in rows
                if int(row["target_nodes"]) == int(target)
                and str(row["perturbation"]) == perturbation
                and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "target_nodes": int(target),
                    "profile_role": "primary" if (perturbation, placement) == PRIMARY_PROFILE else "control",
                    "profile_label": profile_label(perturbation, placement),
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "seed_deltas": ";".join(str(int(row["seed_delta"])) for row in group),
                    "step_budget": int(scaled_steps_for_target(target)),
                    "established_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                        for row in group
                    ),
                    "late_probe_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "late_far_shell_probe" else 0.0 for row in group
                    ),
                    "failed_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "failed_far_shell_horizon" else 0.0
                        for row in group
                    ),
                    "no_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "no_far_shell_horizon" else 0.0 for row in group
                    ),
                    "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                    "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                    "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in group),
                    "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group),
                    "mean_total_high_count": mean_defined(safe_float(row["total_high_count"]) for row in group),
                    "mean_longest_high_run": mean_defined(safe_float(row["longest_high_run"]) for row in group),
                    "mean_far_shell_share": mean_defined(safe_float(row["mean_far_shell_share"]) for row in group),
                    "mean_q90_far_shell_share": mean_defined(safe_float(row["q90_far_shell_share"]) for row in group),
                    "mean_weighted_mean_distance": mean_defined(safe_float(row["mean_weighted_mean_distance"]) for row in group),
                    "mean_abs_delta_spectral_radius_rel": mean_defined(
                        safe_float(row["abs_delta_spectral_radius_rel"]) for row in group
                    ),
                }
            )
    return out


def control_compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {
        (int(row["target_nodes"]), str(row["perturbation"]), int(row["placement"])): row
        for row in aggregate
    }
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        primary = by_key[(int(target), PRIMARY_PROFILE[0], PRIMARY_PROFILE[1])]
        for perturbation, placement in CONTROL_PROFILES:
            control = by_key[(int(target), perturbation, placement)]
            row = {
                "target_nodes": int(target),
                "compare_label": f"{profile_label(*PRIMARY_PROFILE)}_minus_{profile_label(perturbation, placement)}",
                "primary_profile": primary["profile_label"],
                "control_profile": control["profile_label"],
                "established_rate_gap": safe_float(primary["established_far_shell_rate"]) - safe_float(control["established_far_shell_rate"]),
                "no_horizon_control_gap": safe_float(control["no_far_shell_rate"]) - safe_float(primary["no_far_shell_rate"]),
                "high_retention_gap": safe_float(primary["mean_high_retention_rate"]) - safe_float(control["mean_high_retention_rate"]),
                "last12_high_gap": safe_float(primary["mean_last12_high_rate"]) - safe_float(control["mean_last12_high_rate"]),
                "high_horizon_gap": safe_float(primary["mean_high_horizon_span"]) - safe_float(control["mean_high_horizon_span"]),
                "total_high_gap": safe_float(primary["mean_total_high_count"]) - safe_float(control["mean_total_high_count"]),
                "far_share_gap": safe_float(primary["mean_far_shell_share"]) - safe_float(control["mean_far_shell_share"]),
                "distance_gap": safe_float(primary["mean_weighted_mean_distance"]) - safe_float(control["mean_weighted_mean_distance"]),
                "spectral_gap": safe_float(primary["mean_abs_delta_spectral_radius_rel"]) - safe_float(control["mean_abs_delta_spectral_radius_rel"]),
            }
            row["control_weaker"] = int(
                safe_float(row["high_horizon_gap"]) >= 16.0
                and safe_float(row["established_rate_gap"]) >= 0.0
            )
            out.append(row)
    return out


def p0_response_score(primary: Mapping[str, Any], controls: Sequence[Mapping[str, Any]]) -> int:
    max_control_est = max((safe_float(row["established_far_shell_rate"]) for row in controls), default=0.0)
    max_control_horizon = max((safe_float(row["mean_high_horizon_span"]) for row in controls), default=0.0)
    score = 0
    if safe_float(primary["established_far_shell_rate"]) >= 0.50:
        score += 1
    if safe_float(primary["mean_high_horizon_span"]) >= 32.0:
        score += 1
    if safe_float(primary["mean_high_retention_rate"]) >= 0.25:
        score += 1
    if safe_float(primary["mean_last12_high_rate"]) >= 0.25:
        score += 1
    if safe_float(primary["established_far_shell_rate"]) >= max_control_est:
        score += 1
    if safe_float(primary["mean_high_horizon_span"]) - max_control_horizon >= 16.0:
        score += 1
    return score


def scale_response_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in aggregate:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for target, rows in sorted(by_target.items()):
        primary = next(row for row in rows if str(row["profile_label"]) == profile_label(*PRIMARY_PROFILE))
        controls = [row for row in rows if str(row["profile_role"]) == "control"]
        max_control_est = max(safe_float(row["established_far_shell_rate"]) for row in controls)
        max_control_horizon = max(safe_float(row["mean_high_horizon_span"]) for row in controls)
        score = p0_response_score(primary, controls)
        out.append(
            {
                "target_nodes": int(target),
                "primary_profile": primary["profile_label"],
                "control_profiles": ";".join(str(row["profile_label"]) for row in controls),
                "p0_established_rate": safe_float(primary["established_far_shell_rate"]),
                "p0_horizon_span": safe_float(primary["mean_high_horizon_span"]),
                "p0_retention_rate": safe_float(primary["mean_high_retention_rate"]),
                "p0_last12_high_rate": safe_float(primary["mean_last12_high_rate"]),
                "max_control_established_rate": max_control_est,
                "max_control_horizon_span": max_control_horizon,
                "p0_minus_max_control_established_gap": safe_float(primary["established_far_shell_rate"]) - max_control_est,
                "p0_minus_max_control_horizon_gap": safe_float(primary["mean_high_horizon_span"]) - max_control_horizon,
                "p0_response_score": int(score),
                "p0_scale_response_supported": int(score >= 5),
            }
        )
    return out


def historical_compare_rows(scale_response: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    if not HISTORICAL_LADDER_CSV.exists():
        return []
    old_rows = read_csv(HISTORICAL_LADDER_CSV)
    old_by_target = {
        int(row["target_nodes"]): row
        for row in old_rows
        if str(row["perturbation"]) == "add_chord"
    }
    out: List[Dict[str, Any]] = []
    for current in scale_response:
        target = int(current["target_nodes"])
        old = old_by_target.get(target)
        if not old:
            continue
        out.append(
            {
                "target_nodes": target,
                "old_budget_label": old["budget_label"],
                "fresh_budget_label": "v15cs_fresh_seed_scaled",
                "old_p0_established_rate": safe_float(old["p0_established_rate"]),
                "fresh_p0_established_rate": safe_float(current["p0_established_rate"]),
                "p0_established_delta": safe_float(current["p0_established_rate"]) - safe_float(old["p0_established_rate"]),
                "old_p0_horizon_span": safe_float(old["p0_horizon_span"]),
                "fresh_p0_horizon_span": safe_float(current["p0_horizon_span"]),
                "p0_horizon_delta": safe_float(current["p0_horizon_span"]) - safe_float(old["p0_horizon_span"]),
                "fresh_max_control_horizon_span": safe_float(current["max_control_horizon_span"]),
                "fresh_p0_response_score": int(current["p0_response_score"]),
                "fresh_p0_supported": int(current["p0_scale_response_supported"]),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    scale_response: Sequence[Mapping[str, Any]],
    historical_compare: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    supported_targets = [row for row in scale_response if int(row["p0_scale_response_supported"]) == 1]
    both_targets_supported = len(supported_targets) == len(TARGETS)
    any_target_supported = bool(supported_targets)
    old_horizon_sum = sum(safe_float(row["old_p0_horizon_span"]) for row in historical_compare)
    fresh_horizon_sum = sum(safe_float(row["fresh_p0_horizon_span"]) for row in historical_compare)

    if both_targets_supported:
        status = "p0_scale_response_supported"
        note = "Fresh seed deltas support add_chord_p0 response at both 896 and 1024 with weaker controls."
        next_step = "conditional_quasi_invariant_on_p0_response"
        next_note = "Neste steg bor teste om p0-responsfamilien har et stabilt response-fingerprint eller conditional quasi-invariant."
    elif any_target_supported:
        status = "p0_scale_response_target_specific"
        labels = ";".join(str(row["target_nodes"]) for row in supported_targets)
        note = f"Fresh seed deltas support add_chord_p0 at target(s) {labels}, but not all targets."
        next_step = "replicate_or_bracket_p0_response"
        next_note = "Neste steg bor replikere eller bracketter p0-responsen foer ny kandidatstatus."
    elif fresh_horizon_sum > 0.0:
        status = "p0_scale_response_partial_not_supported"
        note = (
            f"Fresh p0 horizon sum is {fmt(fresh_horizon_sum)} versus prior {fmt(old_horizon_sum)}, "
            "but support criteria are not met."
        )
        next_step = "response_fingerprint_synthesis"
        next_note = "Neste steg bor syntetisere responsfingerprints fremfor mer p0/p2-labelbudget."
    else:
        status = "p0_scale_response_not_supported"
        note = "Fresh seed deltas do not reproduce the add_chord_p0 far-shell response."
        next_step = "retire_p0_scale_candidate_and_synthesize_observables"
        next_note = "Neste steg bor pensjonere p0 som scale-kandidat og lage en bedre observable-syntese."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelser er rene og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "fresh_seed_scope",
            "status": "fresh_seed_deltas",
            "note": f"Seed-deltaene {FRESH_SEED_DELTAS} er ikke brukt i v15cn/v15cp/v15cq p2-scale-ladderen.",
        },
        {
            "diagnostic_family": "add_chord_p0_scale_response",
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
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    control_compare: Sequence[Mapping[str, Any]],
    scale_response: Sequence[Mapping[str, Any]],
    historical_compare: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cs: add_chord p0 scale-response holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om `add_chord_p0`-responsen fra v15cq/v15cp holder paa friske seed-deltaer.")
    lines.append("Dette er en kontroll-avledet scale-response holdout, ikke en partikkel-, invariant- eller Lorentz-test.")
    lines.append("")
    lines.append("## Design")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| targets | {';'.join(str(x) for x in TARGETS)} |")
    lines.append(f"| primary | {profile_label(*PRIMARY_PROFILE)} |")
    lines.append(f"| controls | {';'.join(profile_label(*profile) for profile in CONTROL_PROFILES)} |")
    lines.append(f"| fresh seed deltas | {';'.join(str(x) for x in FRESH_SEED_DELTAS)} |")
    lines.append(f"| reference steps | {REFERENCE_STEPS} at target {REFERENCE_TARGET} |")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Profile summary")
    lines.append("")
    lines.append("| target | profile | role | established | none | horizon | retention | last12 high | far share | distance | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['profile_label']} | {row['profile_role']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['no_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_far_shell_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## P0 versus controls")
    lines.append("")
    lines.append("| target | compare | est gap | horizon gap | retention gap | last12 gap | distance gap | control weaker |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in control_compare:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['compare_label']} | {fmt(row['established_rate_gap'])} | {fmt(row['high_horizon_gap'])} | {fmt(row['high_retention_gap'])} | {fmt(row['last12_high_gap'])} | {fmt(row['distance_gap'])} | {int(row['control_weaker'])} |"
        )
    lines.append("")
    lines.append("## Scale response summary")
    lines.append("")
    lines.append("| target | p0 est | p0 horizon | max control est | max control horizon | horizon gap | score | supported |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in scale_response:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['p0_established_rate'])} | {fmt(row['p0_horizon_span'])} | {fmt(row['max_control_established_rate'])} | {fmt(row['max_control_horizon_span'])} | {fmt(row['p0_minus_max_control_horizon_gap'])} | {int(row['p0_response_score'])} | {int(row['p0_scale_response_supported'])} |"
        )
    lines.append("")
    lines.append("## Historical comparison")
    lines.append("")
    lines.append("| target | old p0 est | fresh p0 est | old horizon | fresh horizon | horizon delta | fresh supported |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in historical_compare:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['old_p0_established_rate'])} | {fmt(row['fresh_p0_established_rate'])} | {fmt(row['old_p0_horizon_span'])} | {fmt(row['fresh_p0_horizon_span'])} | {fmt(row['p0_horizon_delta'])} | {int(row['fresh_p0_supported'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Positivt p0-resultat betyr bare at en scale-response-observabel fortjener ny analyse; det er ikke en lov.")
    lines.append("- Negativt p0-resultat betyr at kontroll-inversjonen i v15cq/v15cp trolig var small-n eller seed-avhengig.")
    lines.append("- Uansett skal Lorentz-, global invariant- og entanglement-sprak holdes nede.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cs", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens. Dette er en fresh-seed holdout av en kontroll-avledet scale-response kandidat.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_family = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cs",
        "",
        "Denne runden tester om det nye p0-sporet holder naar vi bytter til friske tilfeldighets-seeds.",
        "",
        f"- Hovedresultat: `{by_family['add_chord_p0_scale_response']['status']}`.",
        f"- Kontrollstatus: `{by_family['artifact_control']['status']}`.",
        f"- Seed-scope: `{by_family['fresh_seed_scope']['status']}`.",
        "",
        "Hvis p0 holder, er det en ny skala-respons-kandidat.",
        "Hvis p0 faller sammen, var sporet trolig en liten kontroll- eller seed-effekt.",
        "",
        f"- Neste steg: `{by_family['next_step']['status']}` fordi {by_family['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cs add_chord p0 scale-response holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_aggregate.csv")
    p.add_argument("--out-control-compare-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_control_compare.csv")
    p.add_argument("--out-scale-response-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_summary.csv")
    p.add_argument("--out-historical-compare-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_historical_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cs_add_chord_p0_scale_response_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cs_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cs.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    by_target_state = {ens.target_nodes: base_states[(ens.name, GROWTH_SEED)] for ens in ensembles}
    by_target_row = {
        int(row["target_nodes"]): row
        for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) in TARGETS
    }

    run_rows = [
        analyze_run(
            target=target,
            base_state=by_target_state[int(target)],
            base_row=by_target_row[int(target)],
            perturbation=perturbation,
            placement=placement,
            seed_delta=seed_delta,
        )
        for target in TARGETS
        for perturbation, placement in PROFILES
        for seed_delta in FRESH_SEED_DELTAS
    ]
    aggregate = aggregate_rows(run_rows)
    control_compare = control_compare_rows(aggregate)
    scale_response = scale_response_rows(aggregate)
    historical_compare = historical_compare_rows(scale_response)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in TARGETS]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        scale_response=scale_response,
        historical_compare=historical_compare,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_control_compare_csv, control_compare)
    write_csv(args.out_scale_response_csv, scale_response)
    write_csv(args.out_historical_compare_csv, historical_compare)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            control_compare=control_compare,
            scale_response=scale_response,
            historical_compare=historical_compare,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
