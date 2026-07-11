#!/usr/bin/env python3
"""v0.15dy sector-conditioned marginal response gate.

Fresh independent-branch holdout after v15dx. The beta1 sector itself is not a
candidate observable. The gate asks whether a +1 sector changes five frozen
marginal dynamics observables under band_zero_del.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15dv_relabel_invariant_chord_constructor as v15dv
import relational_universe_v15dw_constructor_coupling_factorial_gate as v15dw
import relational_universe_v15dx_eventwise_beta1_invariant_gate as v15dx


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
TARGET_NODES = 1024
GROWTH_SEEDS = (202, 303)
PLACEMENTS = (0, 1, 2)
FRESH_SEED_DELTAS = (20711, 20773, 20809, 20857)
SECTORS = ("beta1_base", "beta1_plus1")
STEPS = 3414
WINDOW_STEPS = (854, 1707, 2561, 3414)

PRIMARY_METRICS = (
    "birth_rate_first_half",
    "birth_rate_full",
    "swap_rate_first_half",
    "swap_rate_full",
    "mean_dt_full",
)
MAX_HOLM_P = 0.05
MIN_AUC_SEPARATION = 0.70
MIN_RELATIVE_MEDIAN_GAP = 0.10
MIN_PLACEMENT_DIRECTION_FRACTION = 2.0 / 3.0

Chord = Tuple[int, int, int]


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator != 0.0 else float("nan")


def mean_defined(values: Iterable[Any]) -> float:
    finite = [safe_float(value) for value in values]
    finite = [value for value in finite if math.isfinite(value)]
    return sum(finite) / len(finite) if finite else float("nan")


def median_defined(values: Iterable[Any]) -> float:
    finite = sorted(value for value in (safe_float(item) for item in values) if math.isfinite(value))
    if not finite:
        return float("nan")
    middle = len(finite) // 2
    return finite[middle] if len(finite) % 2 else (finite[middle - 1] + finite[middle]) / 2.0


def fmt(value: Any, digits: int = 3) -> str:
    number = safe_float(value)
    return "nan" if not math.isfinite(number) else f"{number:.{digits}f}"


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    records = list(rows)
    if not records:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: List[str] = []
    for row in records:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [fmt(row.get(field)) if isinstance(row.get(field), float) else str(row.get(field, "")) for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def chord_text(chord: Chord) -> str:
    return "-".join(str(int(node)) for node in chord)


def parse_chord(text: str) -> Chord:
    parts = tuple(int(part) for part in str(text).split("-") if part)
    if len(parts) != 3:
        raise ValueError(f"invalid chord {text!r}")
    return parts  # type: ignore[return-value]


def candidate_seed_for(growth_seed: int, placement: int, seed_delta: int) -> int:
    return 15_000_000_000 + growth_seed * 100_000 + placement * 10_000 + seed_delta + 283


def run_seed_for(growth_seed: int, placement: int, seed_delta: int, sector: str) -> int:
    sector_code = 0 if sector == "beta1_base" else 1
    return (
        TARGET_NODES * 1_000_000
        + growth_seed * 10_000
        + placement * 1_000
        + seed_delta
        + sector_code * 10_000_000
        + 2089
    )


def pre_registration_rows(base_states: Mapping[int, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        base = base_states[growth_seed]
        for placement in PLACEMENTS:
            for seed_delta in FRESH_SEED_DELTAS:
                candidate_seed = candidate_seed_for(growth_seed, placement, seed_delta)
                candidate, metadata = v15dv.sample_uniform_chord_candidate(
                    base,
                    placement,
                    random.Random(candidate_seed),
                )
                for sector in SECTORS:
                    rows.append({
                        "purpose_ref": PURPOSE_REF,
                        "target_nodes": TARGET_NODES,
                        "regime": "band_zero_del",
                        "growth_seed": growth_seed,
                        "placement": placement,
                        "seed_delta": seed_delta,
                        "sector": sector,
                        "run_seed": run_seed_for(growth_seed, placement, seed_delta, sector),
                        "candidate_seed": candidate_seed,
                        "uniform_candidate": chord_text(candidate),
                        "candidate_scope": metadata["candidate_scope"],
                        "candidate_count": metadata["candidate_count"],
                        "constructor": "uniform_relabel_invariant",
                        "independent_sector_rng": 1,
                        "steps": STEPS,
                        "primary_metrics": ";".join(PRIMARY_METRICS),
                        "max_holm_p": MAX_HOLM_P,
                        "min_auc_separation": MIN_AUC_SEPARATION,
                        "min_relative_median_gap": MIN_RELATIVE_MEDIAN_GAP,
                        "min_placement_direction_fraction": MIN_PLACEMENT_DIRECTION_FRACTION,
                        "pre_registered_before_dynamics": 1,
                    })
    return rows


def event_entropy(counts: Mapping[str, int]) -> float:
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        if count <= 0:
            continue
        probability = count / total
        entropy -= probability * math.log(probability)
    return entropy


def run_sector(base_state: Any, assignment: Mapping[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    state = base_state.clone()
    sector = str(assignment["sector"])
    candidate = parse_chord(str(assignment["uniform_candidate"]))
    if sector == "beta1_plus1":
        v15dw.apply_candidate(state, candidate, "uniform_relabel_invariant")

    initial_tokens = state.token_count()
    initial_nodes = state.g.num_nodes()
    initial_edges = state.g.num_edges()
    components = v7.count_components(state.g)
    initial_beta1 = v15dx.beta1(state, components)
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    rng = random.Random(safe_int(assignment["run_seed"]))
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    counts: Counter[str] = Counter()
    elapsed = 0.0
    beta1_violation_count = 0
    expected_delta_violation_count = 0
    component_tracker_violation_count = 0
    windows: List[Dict[str, Any]] = []
    for step in range(1, STEPS + 1):
        event, components = v15dx.single_step(state, manager, rng, params, components, step)
        event_type = str(event["event_type"])
        counts[event_type] += 1
        elapsed += safe_float(event["dt"], 0.0)
        beta1_violation_count += int(safe_int(event["delta_beta1"]) != 0)
        expected_delta_violation_count += 1 - safe_int(event["expected_delta_match"])
        component_tracker_violation_count += 1 - safe_int(event["component_tracker_match"])
        if step in WINDOW_STEPS:
            windows.append({
                "target_nodes": TARGET_NODES,
                "growth_seed": safe_int(assignment["growth_seed"]),
                "placement": safe_int(assignment["placement"]),
                "seed_delta": safe_int(assignment["seed_delta"]),
                "sector": sector,
                "run_seed": safe_int(assignment["run_seed"]),
                "window_step": step,
                "window_fraction": step / STEPS,
                "birth_count": counts.get("birth", 0),
                "birth_rate": counts.get("birth", 0) / step,
                "swap_count": counts.get("swap", 0),
                "swap_rate": counts.get("swap", 0) / step,
                "seed_count": counts.get("seed", 0),
                "seed_rate": counts.get("seed", 0) / step,
                "move_count": counts.get("move", 0),
                "move_rate": counts.get("move", 0) / step,
                "mean_dt": elapsed / step,
                "elapsed_time": elapsed,
                "event_entropy": event_entropy(counts),
                "tokens": state.token_count(),
                "nodes": state.g.num_nodes(),
                "edges": state.g.num_edges(),
            })

    exact_components = v7.count_components(state.g)
    final_beta1 = v15dx.beta1(state, exact_components)
    half = next(row for row in windows if safe_int(row["window_step"]) == 1707)
    full = next(row for row in windows if safe_int(row["window_step"]) == STEPS)
    run = {
        "target_nodes": TARGET_NODES,
        "growth_seed": safe_int(assignment["growth_seed"]),
        "placement": safe_int(assignment["placement"]),
        "seed_delta": safe_int(assignment["seed_delta"]),
        "sector": sector,
        "run_seed": safe_int(assignment["run_seed"]),
        "uniform_candidate": assignment["uniform_candidate"],
        "independent_sector_rng": 1,
        "initial_tokens": initial_tokens,
        "final_tokens": state.token_count(),
        "initial_nodes": initial_nodes,
        "final_nodes": state.g.num_nodes(),
        "initial_edges": initial_edges,
        "final_edges": state.g.num_edges(),
        "initial_beta1": initial_beta1,
        "final_beta1": final_beta1,
        "beta1_drift": final_beta1 - initial_beta1,
        "beta1_violation_count": beta1_violation_count,
        "expected_delta_violation_count": expected_delta_violation_count,
        "component_tracker_violation_count": component_tracker_violation_count,
        "birth_rate_first_half": safe_float(half["birth_rate"]),
        "birth_rate_full": safe_float(full["birth_rate"]),
        "swap_rate_first_half": safe_float(half["swap_rate"]),
        "swap_rate_full": safe_float(full["swap_rate"]),
        "mean_dt_full": safe_float(full["mean_dt"]),
        "event_entropy_full": safe_float(full["event_entropy"]),
        "seed_rate_full": safe_float(full["seed_rate"]),
        "event_counts": ";".join(f"{name}:{count}" for name, count in sorted(counts.items())),
    }
    return windows, run


def auc_score(positive: Sequence[float], negative: Sequence[float]) -> float:
    if not positive or not negative:
        return float("nan")
    wins = 0.0
    for pos in positive:
        for neg in negative:
            wins += 1.0 if pos > neg else 0.5 if pos == neg else 0.0
    return wins / (len(positive) * len(negative))


def sign_test_p(differences: Sequence[float]) -> float:
    nonzero = [difference for difference in differences if difference != 0.0]
    n = len(nonzero)
    if n == 0:
        return 1.0
    positives = sum(difference > 0.0 for difference in nonzero)
    tail = min(positives, n - positives)
    probability = sum(math.comb(n, k) for k in range(tail + 1)) / (2**n)
    return min(1.0, 2.0 * probability)


def holm_adjust(rows: List[Dict[str, Any]]) -> None:
    ordered = sorted(enumerate(rows), key=lambda item: safe_float(item[1]["sign_test_p"]))
    running = 0.0
    m = len(rows)
    adjusted: Dict[int, float] = {}
    for rank, (index, row) in enumerate(ordered):
        candidate = min(1.0, (m - rank) * safe_float(row["sign_test_p"]))
        running = max(running, candidate)
        adjusted[index] = running
    for index, row in enumerate(rows):
        row["holm_p"] = adjusted[index]


def direction(value: float) -> int:
    return 1 if value > 0.0 else -1 if value < 0.0 else 0


def comparison_rows(runs: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    paired: Dict[Tuple[int, int, int], Dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for run in runs:
        key = (safe_int(run["growth_seed"]), safe_int(run["placement"]), safe_int(run["seed_delta"]))
        paired[key][str(run["sector"])] = run
    if len(paired) != 24 or any(set(pair) != set(SECTORS) for pair in paired.values()):
        raise ValueError("expected 24 complete sector pairs")

    rows: List[Dict[str, Any]] = []
    for metric in PRIMARY_METRICS:
        differences: List[float] = []
        base_values: List[float] = []
        plus_values: List[float] = []
        by_growth: Dict[int, List[float]] = defaultdict(list)
        by_placement: Dict[int, List[float]] = defaultdict(list)
        for (growth_seed, placement, _), pair in sorted(paired.items()):
            base = safe_float(pair["beta1_base"][metric])
            plus = safe_float(pair["beta1_plus1"][metric])
            difference = plus - base
            base_values.append(base)
            plus_values.append(plus)
            differences.append(difference)
            by_growth[growth_seed].append(difference)
            by_placement[placement].append(difference)
        median_base = median_defined(base_values)
        median_plus = median_defined(plus_values)
        median_difference = median_defined(differences)
        global_direction = direction(median_difference)
        growth_directions = [direction(median_defined(values)) for _, values in sorted(by_growth.items())]
        placement_directions = [direction(median_defined(values)) for _, values in sorted(by_placement.items())]
        matching_growth = sum(item == global_direction and item != 0 for item in growth_directions)
        matching_placements = sum(item == global_direction and item != 0 for item in placement_directions)
        positive = sum(value > 0.0 for value in differences)
        negative = sum(value < 0.0 for value in differences)
        nonzero = positive + negative
        auc = auc_score(plus_values, base_values)
        rows.append({
            "metric": metric,
            "n_pairs": len(differences),
            "median_beta1_base": median_base,
            "median_beta1_plus1": median_plus,
            "median_paired_difference": median_difference,
            "relative_median_gap": abs(median_plus - median_base) / max(abs(median_base), 1.0 / STEPS),
            "positive_pair_count": positive,
            "negative_pair_count": negative,
            "zero_pair_count": len(differences) - nonzero,
            "sign_consistency": max(positive, negative) / nonzero if nonzero else 0.0,
            "sign_test_p": sign_test_p(differences),
            "auc_plus1_vs_base": auc,
            "auc_separation": max(auc, 1.0 - auc),
            "global_direction": global_direction,
            "growth_seed_direction_match": matching_growth / len(GROWTH_SEEDS),
            "placement_direction_match": matching_placements / len(PLACEMENTS),
        })
    holm_adjust(rows)
    for row in rows:
        row["metric_gate_pass"] = int(
            safe_float(row["holm_p"]) <= MAX_HOLM_P
            and safe_float(row["auc_separation"]) >= MIN_AUC_SEPARATION
            and safe_float(row["relative_median_gap"]) >= MIN_RELATIVE_MEDIAN_GAP
            and safe_float(row["growth_seed_direction_match"]) == 1.0
            and safe_float(row["placement_direction_match"]) >= MIN_PLACEMENT_DIRECTION_FRACTION
        )
        row["metric_status"] = "sector_response_candidate" if safe_int(row["metric_gate_pass"]) else "not_supported"
    return rows


def evaluation_rows(
    preregistration: Sequence[Mapping[str, Any]],
    runs: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    artifact_clean = (
        len(preregistration) == 48
        and len(runs) == 48
        and all(safe_int(row.get("pre_registered_before_dynamics")) == 1 for row in preregistration)
        and all(safe_int(row.get("independent_sector_rng")) == 1 for row in runs)
        and len({safe_int(row["run_seed"]) for row in preregistration}) == 48
    )
    invariant_clean = all(
        safe_int(run["beta1_drift"]) == 0
        and safe_int(run["beta1_violation_count"]) == 0
        and safe_int(run["expected_delta_violation_count"]) == 0
        and safe_int(run["component_tracker_violation_count"]) == 0
        for run in runs
    )
    passing = [str(row["metric"]) for row in comparisons if safe_int(row["metric_gate_pass"]) == 1]
    if not artifact_clean or not invariant_clean:
        diagnosis = "sector_response_instrumentation_failed"
        next_step = "repair_independent_branch_instrumentation"
    elif passing:
        diagnosis = "beta1_sector_conditioned_marginal_response_candidate"
        next_step = "fresh_growth_seed_holdout_of_passing_marginal_observables"
    else:
        diagnosis = "no_beta1_sector_response_detected_in_frozen_marginals"
        next_step = "retain_beta1_as_sector_label_only_and_test_local_sector_boundary_observable"
    return [
        {"key": "scope", "value": "fresh_independent_sector_response", "evidence": f"runs={len(runs)}; pairs={len(runs)//2}; steps_per_run={STEPS}"},
        {"key": "artifact_control", "value": "clean" if artifact_clean else "failed", "evidence": "48 preregistered unique independent sector runs"},
        {"key": "anchor_beta1_conservation", "value": "pass" if invariant_clean else "fail", "evidence": "eventwise and final beta1 drift must remain zero"},
        {"key": "primary_metric_gate", "value": "pass" if passing else "fail", "evidence": f"passing_metrics={';'.join(passing) if passing else 'none'}"},
        {"key": "diagnosis", "value": diagnosis, "evidence": "beta1 itself and edge-count identities excluded from primary metrics"},
        {"key": "next_step", "value": next_step, "evidence": "deduced from frozen multi-metric gate without refit"},
    ]


def claim_rows(evaluation: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    response_supported = by_key["primary_metric_gate"] == "pass"
    return [
        {
            "claim_id": "claim.v15dy.sector-marginal-response",
            "claim_type": "statistical",
            "strength": "moderated",
            "statement": "The beta1 +1 sector changes at least one frozen beta1-free marginal dynamics observable under band_zero_del.",
            "evaluation": "supported_candidate" if response_supported else "unsupported",
            "evidence_ref": "v15dy_observable_comparisons.csv",
        },
        {
            "claim_id": "claim.v15dy.sector-dynamical-species",
            "claim_type": "project_capability",
            "strength": "moderated",
            "statement": "The beta1 sectors constitute distinct physical species.",
            "evaluation": "unsupported",
            "evidence_ref": "v15dy_gate_evaluation.csv:diagnosis",
        },
        {
            "claim_id": "claim.v15dy.emergent-symmetry",
            "claim_type": "project_capability",
            "strength": "moderated",
            "statement": "A sector-conditioned marginal response would establish emergent physical symmetry.",
            "evaluation": "unsupported",
            "evidence_ref": "v15dy_gate_evaluation.csv:diagnosis",
        },
    ]


def render_report(
    comparisons: Sequence[Mapping[str, Any]],
    evaluation: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> str:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    goal_status = "satisfied" if by_key["artifact_control"] == "clean" and by_key["anchor_beta1_conservation"] == "pass" else "missed"
    response_status = "satisfied" if by_key["primary_metric_gate"] == "pass" else "missed"
    lines = [
        "# Relasjonell universgraf v0.15dy: sector-conditioned marginal response gate",
        "",
        "## Formaal og maal",
        "",
        f"`purposeRef`: `{PURPOSE_REF}`.",
        "",
        "Test om beta1-sektor `+1` endrer kontrolluavhengige marginale dynamikker etter at beta1 og algebraisk avhengige edge-identiteter er fjernet fra kandidatsettet.",
        "",
        "| goal | target | status |",
        "| --- | --- | --- |",
        f"| G1 clean independent holdout | 48 preregistered runs; zero invariant violations | {goal_status} |",
        f"| G2 sector-conditioned response | at least one frozen metric passes all thresholds | {response_status} |",
        f"| G3 next decision | no metric refit | satisfied |",
        "",
        "## Frozen design",
        "",
        f"- target `{TARGET_NODES}`; growth seeds `{';'.join(map(str, GROWTH_SEEDS))}`; placements `p0,p1,p2`",
        f"- fresh seed deltas `{';'.join(map(str, FRESH_SEED_DELTAS))}`; `{STEPS}` events per run",
        "- 24 matched contexts, each with independently randomized beta1-base and beta1-plus1 branches",
        "- uniform relabel-invariant add_chord creates the +1 sector",
        f"- primary metrics: `{';'.join(PRIMARY_METRICS)}`",
        f"- gate: Holm p <= `{MAX_HOLM_P}`, AUC separation >= `{MIN_AUC_SEPARATION}`, relative median gap >= `{MIN_RELATIVE_MEDIAN_GAP}`, same direction on both growth seeds and at least two placements",
        "",
        "Beta1, raw edge offset, far-shell, damage sets and placement labels are excluded from the primary metric set.",
        "",
        "## Observable comparisons",
        "",
    ]
    lines.extend(table(comparisons, ("metric", "n_pairs", "median_beta1_base", "median_beta1_plus1", "median_paired_difference", "relative_median_gap", "sign_consistency", "holm_p", "auc_separation", "growth_seed_direction_match", "placement_direction_match", "metric_status")))
    lines.extend(["", "## Claim adjudication", ""])
    lines.extend(table(claims, ("claim_id", "statement", "evaluation", "evidence_ref")))
    lines.extend(["", "## Decision", ""])
    lines.extend(table(evaluation, ("key", "value", "evidence")))
    lines.extend([
        "",
        "A pass would identify a fresh statistical candidate, not a particle or physical species. A fail means only that these five global marginal observables do not expose a sector effect at this budget.",
        "",
    ])
    return "\n".join(lines)


def render_operational(evaluation: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    return "\n".join([
        "# Operativ anbefaling v0.15dy",
        "",
        f"- `artifact_control`: `{by_key['artifact_control']}`.",
        f"- `anchor_beta1_conservation`: `{by_key['anchor_beta1_conservation']}`.",
        f"- `primary_metric_gate`: `{by_key['primary_metric_gate']}`.",
        f"- `diagnosis`: `{by_key['diagnosis']}`.",
        f"- `next_step`: `{by_key['next_step']}`.",
        "",
        "Ikke bruk beta1-offsetten eller edge-identiteten som response-signal.",
        "Ikke oppgrader et eventuelt marginalt signal til fysisk art, partikkel eller symmetri uten ny holdout.",
        "",
    ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--out-pre-registration-csv", default=str(DOC / "v15dy_pre_registration.csv"))
    parser.add_argument("--out-window-csv", default=str(DOC / "v15dy_marginal_windows.csv"))
    parser.add_argument("--out-run-summary-csv", default=str(DOC / "v15dy_run_summary.csv"))
    parser.add_argument("--out-comparisons-csv", default=str(DOC / "v15dy_observable_comparisons.csv"))
    parser.add_argument("--out-evaluation-csv", default=str(DOC / "v15dy_gate_evaluation.csv"))
    parser.add_argument("--out-claims-csv", default=str(DOC / "v15dy_claim_ledger.csv"))
    parser.add_argument("--out-report", default=str(DOC / "v15dy_sector_conditioned_marginal_response_gate.md"))
    parser.add_argument("--out-operational", default=str(DOC / "v0_15dy_operativ_anbefaling.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        preregistration = read_csv(args.out_pre_registration_csv)
        windows = read_csv(args.out_window_csv)
        runs = read_csv(args.out_run_summary_csv)
    else:
        base_states, _, _ = v15dw.build_bases()
        preregistration = pre_registration_rows(base_states)
        write_csv(args.out_pre_registration_csv, preregistration)
        windows: List[Dict[str, Any]] = []
        runs: List[Dict[str, Any]] = []
        for index, assignment in enumerate(preregistration, start=1):
            print(
                f"running {index}/{len(preregistration)} growth_seed={assignment['growth_seed']} "
                f"p{assignment['placement']} seed_delta={assignment['seed_delta']} sector={assignment['sector']}",
                flush=True,
            )
            run_windows, run = run_sector(base_states[safe_int(assignment["growth_seed"])], assignment)
            windows.extend(run_windows)
            runs.append(run)
        write_csv(args.out_window_csv, windows)
        write_csv(args.out_run_summary_csv, runs)

    if len(preregistration) != 48 or len(runs) != 48 or len(windows) != 48 * len(WINDOW_STEPS):
        raise ValueError("v15dy data shape mismatch")
    comparisons = comparison_rows(runs)
    evaluation = evaluation_rows(preregistration, runs, comparisons)
    claims = claim_rows(evaluation)
    write_csv(args.out_comparisons_csv, comparisons)
    write_csv(args.out_evaluation_csv, evaluation)
    write_csv(args.out_claims_csv, claims)
    Path(args.out_report).write_text(render_report(comparisons, evaluation, claims), encoding="utf-8")
    Path(args.out_operational).write_text(render_operational(evaluation), encoding="utf-8")
    for row in evaluation:
        print(f"{row['key']}: {row['value']} ({row['evidence']})")


if __name__ == "__main__":
    main()
