#!/usr/bin/env python3
"""v0.15dk pre-registered support-rank holdout.

Fresh growth-seed dynamic holdout for the v15dj scout:
low local support volume/gap as a placement prior.

Discipline:
- compute support ranking before any dynamic runs
- write the pre-run ranking CSV before the run loop
- keep target/perturbation/placements narrow: 1024/add_chord/p0,p1,p2
- run all three placements so the frozen top1/top2 can be judged against a
  contrast
- do not refit labels or dynamic observables into a new selector
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split as v15cw
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15dg_boundary_mass_holdout as v15dg
import relational_universe_v15q_single_defect_recurrence_lab as v15q


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEED = 404
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
LOG_EVERY = v15da.LOG_EVERY
ACTIVE_ESTABLISHED_RATE = 0.50

PRIMARY_SUPPORT_RANK_METRIC = "support_ball2_minus_ball1"
PRIMARY_SUPPORT_RANK_DIRECTION = "lower_is_better"
SECONDARY_SUPPORT_RANK_METRIC = "support_ball_3"
SECONDARY_SUPPORT_RANK_DIRECTION = "lower_is_better"
PRIMARY_DYNAMIC_METRIC = v15dg.PRIMARY_METRIC

FRESH_SEED_DELTAS = (
    12011, 12071, 12143, 12203,
    12281, 12347, 12413, 12491,
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in (safe_float(v) for v in values) if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


def profile_label(placement: int) -> str:
    return f"{PERTURBATION}_p{int(placement)}"


def run_seed_for(*, target: int, growth_seed: int, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 1913, "local_swap": 1979}[perturbation]
    return (
        int(target) * 1_000_000
        + int(growth_seed) * 10_000
        + int(placement) * 1_000
        + int(seed_delta)
        + perturbation_offset
    )


def support_for_placement(base_state: Any, placement: int) -> Tuple[List[int], Dict[str, Any]]:
    probe = base_state.clone()
    info = v15.v14.v08b.apply_custom_perturbation(
        probe,
        PERTURBATION,
        center_token_index=placement,
    )
    support = [int(x) for x in info.get("support", [])]
    return support, dict(info)


def support_rank_rows(base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        support, info = support_for_placement(base_state, placement)
        features = v15cv.support_mechanism_features(
            target=TARGET_NODES,
            base_state=base_state,
            placement=placement,
            seed_delta=-1,
            run_seed=-1,
            support=support,
        )
        ball1 = safe_float(features["support_ball_1"])
        ball2 = safe_float(features["support_ball_2"])
        ball3 = safe_float(features["support_ball_3"])
        row = {
            "target_nodes": TARGET_NODES,
            "growth_seed": GROWTH_SEED,
            "perturbation": PERTURBATION,
            "placement": int(placement),
            "support_signature": ",".join(str(x) for x in support),
            "requested_match": int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
            "support_size": safe_float(features["support_size"]),
            "mean_support_degree": safe_float(features["mean_support_degree"]),
            "support_ball_1": ball1,
            "support_ball_2": ball2,
            "support_ball_3": ball3,
            "support_boundary_to_volume": safe_float(features["support_boundary_to_volume"]),
            "support_pairwise_mean_distance": safe_float(features["support_pairwise_mean_distance"]),
            "support_ball2_minus_ball1": ball2 - ball1 if math.isfinite(ball2) and math.isfinite(ball1) else float("nan"),
            "support_ball3_minus_ball1": ball3 - ball1 if math.isfinite(ball3) and math.isfinite(ball1) else float("nan"),
            "support_ball3_minus_ball2": ball3 - ball2 if math.isfinite(ball3) and math.isfinite(ball2) else float("nan"),
            "ball1_over_ball3": safe_div(ball1, ball3),
            "ball2_over_ball3": safe_div(ball2, ball3),
            "ball3_over_ball1": safe_div(ball3, ball1),
        }
        rows.append(row)

    ranked = sorted(
        rows,
        key=lambda row: (
            safe_float(row[PRIMARY_SUPPORT_RANK_METRIC]),
            safe_float(row[SECONDARY_SUPPORT_RANK_METRIC]),
            int(row["placement"]),
        ),
    )
    for rank, row in enumerate(ranked, start=1):
        row["pre_run_primary_rank"] = rank
        row["pre_run_top1"] = int(rank == 1)
        row["pre_run_top2"] = int(rank <= 2)
        row["pre_run_rank_metric"] = PRIMARY_SUPPORT_RANK_METRIC
        row["pre_run_rank_direction"] = PRIMARY_SUPPORT_RANK_DIRECTION
        row["pre_run_secondary_tiebreak"] = SECONDARY_SUPPORT_RANK_METRIC
    return sorted(ranked, key=lambda row: int(row["placement"]))


def run_single(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    run_seed = run_seed_for(
        target=TARGET_NODES,
        growth_seed=GROWTH_SEED,
        perturbation=PERTURBATION,
        placement=placement,
        seed_delta=seed_delta,
    )
    res = v15ae.run_defect_with_control_graphs(
        base_state,
        params=params,
        seed=run_seed,
        steps=v15cs.scaled_steps_for_target(TARGET_NODES),
        perturbation=PERTURBATION,
        center_token_index=placement,
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    info = dict(res["perturbation_info"])
    support = [int(x) for x in info.get("support", [])]
    support_signature = ",".join(str(x) for x in support)
    base_dist = v7.bfs_distances(base_state.g, support)
    fallback = (max(base_dist.values()) + 1) if base_dist else 1
    snapshot_rows = v15cv.snapshot_rows_for_run(
        target=TARGET_NODES,
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        log_rows=res["log_rows"],
        damaged_sets=res["damaged_sets"],
        control_graphs=res["control_graphs"],
        base_dist=base_dist,
        fallback=fallback,
    )
    recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
    final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    support_features = v15cv.support_mechanism_features(
        target=TARGET_NODES,
        base_state=base_state,
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support=support,
    )
    mechanism_row = v15cv.run_summary_row(
        target=TARGET_NODES,
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        requested_match=int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
        support_signature=support_signature,
        support_features=support_features,
        recurrence=recurrence,
        final_drift=final_drift,
        snapshot_rows=snapshot_rows,
    )
    run_ids = {
        "target_nodes": TARGET_NODES,
        "growth_seed": GROWTH_SEED,
        "profile_label": profile_label(placement),
        "perturbation": PERTURBATION,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "support_signature": support_signature,
    }
    comps, events, genealogy_summary = v15cw.genealogy_for_run(
        run_ids=run_ids,
        log_rows=res["log_rows"],
        damaged_sets=res["damaged_sets"],
        control_graphs=res["control_graphs"],
        support=support,
    )
    row = {
        **mechanism_row,
        **genealogy_summary,
        "growth_seed": GROWTH_SEED,
        "profile_label": profile_label(placement),
        "source_scope": f"v15dk_growth_seed_{GROWTH_SEED}_p{placement}",
        "pre_registered_support_rank_holdout": 1,
    }
    return comps, events, row


def add_pre_run_rank_fields(run_rows: Sequence[Mapping[str, Any]], rank_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_placement = {int(row["placement"]): row for row in rank_rows}
    out: List[Dict[str, Any]] = []
    for raw in run_rows:
        row = dict(raw)
        rank = by_placement[int(safe_float(row["placement"]))]
        for field in (
            "pre_run_primary_rank",
            "pre_run_top1",
            "pre_run_top2",
            "pre_run_rank_metric",
            "pre_run_rank_direction",
            "pre_run_secondary_tiebreak",
            PRIMARY_SUPPORT_RANK_METRIC,
            SECONDARY_SUPPORT_RANK_METRIC,
            "support_ball3_minus_ball1",
            "support_ball3_minus_ball2",
        ):
            row[field] = rank[field]
        out.append(row)
    return out


def placement_summary_rows(run_rows: Sequence[Mapping[str, Any]], rank_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rank_by_placement = {int(row["placement"]): row for row in rank_rows}
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[int(safe_float(row["placement"]))].append(row)
    out: List[Dict[str, Any]] = []
    for placement, group in sorted(grouped.items()):
        counts = Counter(str(row["far_shell_horizon_label"]) for row in group)
        n = len(group)
        rank = rank_by_placement[placement]
        out.append(
            {
                "growth_seed": GROWTH_SEED,
                "placement": placement,
                "pre_run_primary_rank": int(rank["pre_run_primary_rank"]),
                "pre_run_top1": int(rank["pre_run_top1"]),
                "pre_run_top2": int(rank["pre_run_top2"]),
                "support_signature": rank["support_signature"],
                "rank_metric": PRIMARY_SUPPORT_RANK_METRIC,
                "rank_metric_value": safe_float(rank[PRIMARY_SUPPORT_RANK_METRIC]),
                "support_ball_3": safe_float(rank["support_ball_3"]),
                "n_runs": n,
                "label_counts": ";".join(f"{key}:{counts[key]}" for key in sorted(counts)),
                "established_rate": counts.get("established_far_shell_horizon", 0) / max(1, n),
                "mixed_rate": counts.get("mixed_far_shell_horizon", 0) / max(1, n),
                "no_horizon_rate": counts.get("no_far_shell_horizon", 0) / max(1, n),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "median_boundary_mass": median_defined(safe_float(row.get(PRIMARY_DYNAMIC_METRIC)) for row in group),
                "median_genealogy_intensity": median_defined(safe_float(row.get(v15da.PRIMARY_SCORE)) for row in group),
            }
        )
    return out


def support_rank_evaluation_rows(placement_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    active = [row for row in placement_rows if safe_float(row["established_rate"]) >= ACTIVE_ESTABLISHED_RATE]
    active_set = {int(row["placement"]) for row in active}
    top1 = [row for row in placement_rows if int(row["pre_run_top1"]) == 1]
    top2 = [row for row in placement_rows if int(row["pre_run_top2"]) == 1]
    top1_set = {int(row["placement"]) for row in top1}
    top2_set = {int(row["placement"]) for row in top2}
    active_total = len(active_set)
    top1_capture = len(active_set & top1_set)
    top2_capture = len(active_set & top2_set)
    contrast = [row for row in placement_rows if int(row["pre_run_top2"]) == 0]

    if active_total == 0:
        status = "support_rank_inconclusive_no_active_placements"
    elif top1_capture > 0 and top2_capture == active_total and len(active_set) < len(placement_rows):
        status = "support_rank_supported_full_capture"
    elif top1_capture > 0 and top2_capture > 0:
        status = "support_rank_supported_as_sparse_prior"
    elif top2_capture > 0:
        status = "support_rank_weak_top2_only"
    else:
        status = "support_rank_not_supported"

    return [
        {
            "key": "primary_rank_metric",
            "value": PRIMARY_SUPPORT_RANK_METRIC,
            "evidence": f"direction={PRIMARY_SUPPORT_RANK_DIRECTION}; tiebreak={SECONDARY_SUPPORT_RANK_METRIC}",
        },
        {
            "key": "active_threshold",
            "value": f"established_rate_ge_{fmt(ACTIVE_ESTABLISHED_RATE, 2)}",
            "evidence": "active placement is evaluated after dynamics, not used in support ranking",
        },
        {
            "key": "top1_placements",
            "value": ";".join(f"p{int(row['placement'])}" for row in top1),
            "evidence": ";".join(f"p{int(row['placement'])}:est={fmt(row['established_rate'])}" for row in top1),
        },
        {
            "key": "top2_placements",
            "value": ";".join(f"p{int(row['placement'])}" for row in top2),
            "evidence": ";".join(f"p{int(row['placement'])}:est={fmt(row['established_rate'])}" for row in top2),
        },
        {
            "key": "contrast_placements",
            "value": ";".join(f"p{int(row['placement'])}" for row in contrast),
            "evidence": ";".join(f"p{int(row['placement'])}:est={fmt(row['established_rate'])}" for row in contrast),
        },
        {
            "key": "active_placements",
            "value": ";".join(f"p{x}" for x in sorted(active_set)),
            "evidence": f"active_total={active_total}",
        },
        {
            "key": "top1_capture_fraction",
            "value": fmt(safe_div(top1_capture, active_total)),
            "evidence": f"captured={top1_capture}; active_total={active_total}",
        },
        {
            "key": "top2_capture_fraction",
            "value": fmt(safe_div(top2_capture, active_total)),
            "evidence": f"captured={top2_capture}; active_total={active_total}",
        },
        {
            "key": "support_rank_status",
            "value": status,
            "evidence": "fresh growth-seed evaluation of the pre-run ranking",
        },
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    support_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    label_note = ";".join(f"{key}:{labels[key]}" for key in sorted(labels))
    support_status = next(row for row in support_eval if row["key"] == "support_rank_status")
    top1_capture = next(row for row in support_eval if row["key"] == "top1_capture_fraction")
    top2_capture = next(row for row in support_eval if row["key"] == "top2_capture_fraction")
    primary = next(row for row in metric_rows if str(row["metric"]) == PRIMARY_DYNAMIC_METRIC)

    if support_status["value"] in {"support_rank_supported_full_capture", "support_rank_supported_as_sparse_prior"}:
        next_status = "replicate_support_rank_or_expand_growth_seed_count"
        next_note = (
            "Support-rankingen overlevde som prior paa fresh growth seed; neste steg bor replikere paa en ny growth seed "
            "eller kjoere to nye growth seeds med samme pre-run ranking."
        )
    elif support_status["value"] == "support_rank_weak_top2_only":
        next_status = "support_rank_needs_second_fresh_seed_before_trust"
        next_note = "Top2 traff men top1 sviktet; dette er for svakt til aa bruke som selector uten ny fresh seed."
    else:
        next_status = "retire_support_rank_as_selector_candidate"
        next_note = "Pre-run support-rankingen traff ikke; gaa tilbake til observabeldesign eller skala/placement-landskap."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "pre_registration",
            "status": "support_rank_written_before_dynamics",
            "note": (
                f"Pre-run ranking er frosset til `{PRIMARY_SUPPORT_RANK_METRIC}` lower-is-better "
                f"med `{SECONDARY_SUPPORT_RANK_METRIC}` som tiebreak foer dynamikk-loop."
            ),
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "fresh_growth_seed_label_balance_recorded",
            "note": f"Labels: {label_note}.",
        },
        {
            "diagnostic_family": "support_rank_result",
            "status": str(support_status["value"]),
            "note": (
                f"Top1 capture={top1_capture['value']}; top2 capture={top2_capture['value']}. "
                f"{support_status['evidence']}"
            ),
        },
        {
            "diagnostic_family": "dynamic_boundary_mass_audit",
            "status": "reported_descriptive_not_primary_selector",
            "note": (
                f"`{PRIMARY_DYNAMIC_METRIC}` AUC established-vs-no={fmt(primary['auc_established_vs_no'])}; "
                "dette er audit etter support-rankingen, ikke en refittet selector."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            val = row.get(field, "")
            vals.append(fmt(val) if isinstance(val, float) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def build_report(
    *,
    rank_rows: Sequence[Mapping[str, Any]],
    placement_rows: Sequence[Mapping[str, Any]],
    support_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dk: pre-registered support-rank holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en fresh growth-seed holdout av v15dj sin support-conditioned scout.")
    lines.append("Support-rangering beregnes foer dynamikk, skrives til CSV, og brukes deretter som frossen placement-prior.")
    lines.append("Dynamiske observabler rapporteres etterpaa som audit, ikke som refit.")
    lines.append("")
    lines.append("## Pre-registered scope")
    lines.append("")
    lines.extend(
        table(
            [
                {"field": "target", "value": TARGET_NODES},
                {"field": "growth_seed", "value": GROWTH_SEED},
                {"field": "perturbation", "value": PERTURBATION},
                {"field": "placements", "value": ";".join(f"p{x}" for x in PLACEMENTS)},
                {"field": "seed_deltas", "value": ";".join(str(x) for x in FRESH_SEED_DELTAS)},
                {"field": "rank_metric", "value": PRIMARY_SUPPORT_RANK_METRIC},
                {"field": "rank_tiebreak", "value": SECONDARY_SUPPORT_RANK_METRIC},
            ],
            ("field", "value"),
        )
    )
    lines.append("")
    lines.append("## Pre-run support ranking")
    lines.append("")
    lines.extend(
        table(
            sorted(rank_rows, key=lambda row: int(row["pre_run_primary_rank"])),
            (
                "pre_run_primary_rank",
                "placement",
                "support_signature",
                PRIMARY_SUPPORT_RANK_METRIC,
                "support_ball_3",
                "mean_support_degree",
                "support_boundary_to_volume",
            ),
        )
    )
    lines.append("")
    lines.append("## Placement outcomes")
    lines.append("")
    lines.extend(
        table(
            sorted(placement_rows, key=lambda row: int(row["pre_run_primary_rank"])),
            (
                "pre_run_primary_rank",
                "placement",
                "label_counts",
                "established_rate",
                "mean_horizon_span",
                "median_boundary_mass",
                "median_genealogy_intensity",
            ),
        )
    )
    lines.append("")
    lines.append("## Support-rank evaluation")
    lines.append("")
    lines.extend(table(support_eval, ("key", "value", "evidence")))
    lines.append("")
    lines.append("## Dynamic metric audit")
    lines.append("")
    lines.extend(table(metric_rows, ("metric", "role", "auc_established_vs_no", "median_established_raw", "median_no_horizon_raw")))
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en lokal defect/response-test, ikke Lorentz-, invariant-, entanglement- eller partikkel-evidens.")
    lines.append("- Hvis support-rankingen treffer, er det en placement-prior som maa replikeres, ikke en fysikklov.")
    lines.append("- Hvis support-rankingen feiler, skal v15dj-scouten pensjoneres eller nedgraderes til deskriptiv audit.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dk", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit support-rankingen etter outcome.")
    lines.append("- Ikke bruk boundary/mass eller genealogy-intensity som primary selector i denne runden.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dk",
            "",
            "Denne runden testet om vi kan velge bedre plasseringer foer simulasjonen starter, bare ved aa se paa lokal supportgeometri.",
            "",
            "Det viktige er rekkefolgen: forst ble support-rangeringen skrevet ned, deretter ble dynamikken kjort.",
            "",
            f"- Hovedlesning: `{diag['support_rank_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er en test av en lokal prior, ikke en paastand om en universell fysikklov.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dk pre-registered support-rank holdout.")
    p.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregate/report files from existing v15dk CSV outputs.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dk_support_rank_target_summary.csv"))
    p.add_argument("--out-pre-rank-csv", default=str(DOC / "v15dk_support_rank_pre_run_ranking.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15dk_support_rank_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15dk_support_rank_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15dk_support_rank_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dk_support_rank_run_features.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dk_support_rank_placement_summary.csv"))
    p.add_argument("--out-support-eval-csv", default=str(DOC / "v15dk_support_rank_evaluation.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dk_support_rank_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15dk_support_rank_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dk_support_rank_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dk_support_rank_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dk_pre_registered_support_rank_holdout.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dk_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dk.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        rank_rows = read_csv(args.out_pre_rank_csv)
        run_rows = read_csv(args.out_runs_csv)
        blind_rows = read_csv(args.out_blind_csv)
        component_rows = read_csv(args.out_components_csv)
        event_rows = read_csv(args.out_events_csv)
        target_summary = read_csv(args.out_target_csv)
    else:
        spec_rows = read_csv(v15da.V15CZ_SCORE_SPEC)
        regime = v10e.recommended_regime("fast_balanced")
        ensembles = v15.deep_ensembles([TARGET_NODES])
        base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
        base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
        base_row = next(
            row for row in base_rows
            if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) == TARGET_NODES
        )
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

        rank_rows = support_rank_rows(base_state)
        write_csv(args.out_pre_rank_csv, rank_rows)
        print(f"wrote pre-run ranking {args.out_pre_rank_csv}")
        for row in sorted(rank_rows, key=lambda x: int(x["pre_run_primary_rank"])):
            print(
                "pre-run rank "
                f"{int(row['pre_run_primary_rank'])}: p{int(row['placement'])} "
                f"{PRIMARY_SUPPORT_RANK_METRIC}={fmt(row[PRIMARY_SUPPORT_RANK_METRIC])} "
                f"{SECONDARY_SUPPORT_RANK_METRIC}={fmt(row[SECONDARY_SUPPORT_RANK_METRIC])}"
            )

        component_rows: List[Dict[str, Any]] = []
        event_rows: List[Dict[str, Any]] = []
        raw_rows: List[Dict[str, Any]] = []
        for placement in PLACEMENTS:
            for seed_delta in FRESH_SEED_DELTAS:
                print(f"running growth_seed {GROWTH_SEED} p{placement} seed_delta {seed_delta}")
                comps, events, row = run_single(
                    base_state=base_state,
                    base_row=base_row,
                    params=params,
                    placement=int(placement),
                    seed_delta=int(seed_delta),
                )
                component_rows.extend(comps)
                event_rows.extend(events)
                raw_rows.append(row)

        run_rows, blind_rows = v15dg.enrich_holdout_rows(
            raw_rows=raw_rows,
            component_rows=component_rows,
            spec_rows=spec_rows,
        )
        run_rows = add_pre_run_rank_fields(run_rows, rank_rows)
        target_summary = [
            row for row in v10e.summarize_bases(base_rows)
            if int(row["target_nodes"]) == TARGET_NODES
        ]

    metric_rows = v15dg.metric_score_rows(run_rows)
    group_rows = v15dg.group_summary_rows(run_rows)
    matched_rows = v15dg.matched_seed_rows(run_rows)
    placement_rows = placement_summary_rows(run_rows, rank_rows)
    support_eval = support_rank_evaluation_rows(placement_rows)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        support_eval=support_eval,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_pre_rank_csv, rank_rows)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_support_eval_csv, support_eval)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            rank_rows=rank_rows,
            placement_rows=placement_rows,
            support_eval=support_eval,
            metric_rows=metric_rows,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")
    print(f"wrote {args.out_summary_md}")
    print(f"wrote {args.out_diagnosis_csv}")


if __name__ == "__main__":
    main()
