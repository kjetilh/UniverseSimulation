#!/usr/bin/env python3
"""v0.15ds active-set landscape atlas.

Fresh dynamic atlas after v15dr.

Goal:
- stop refitting the failed repeated-class taxonomy mapper,
- keep the scope narrow at 1024/add_chord/p0,p1,p2,
- spend the next budget on more fresh growth seeds,
- estimate active-set class frequencies and novelty before trying another
  selector.

This is local defect/response-landscape work. It is not evidence for
particles, Lorentz behavior, entanglement, global invariants, or universal
geometry.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15dg_boundary_mass_holdout as v15dg
import relational_universe_v15dk_pre_registered_support_rank_holdout as v15dk
import relational_universe_v15dl_base_landscape_morphology_synthesis as v15dl
import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn
import relational_universe_v15dq_active_set_taxonomy_synthesis as v15dq
import relational_universe_v15dr_active_set_taxonomy_mapper_holdout as v15dr


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEEDS = (1201, 1301, 1409, 1511, 1601, 1709)
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
ACTIVE_ESTABLISHED_RATE = 0.50
FRESH_SEED_DELTAS = (18107, 18161, 18223, 18289)
ATLAS_SOURCE = "v15ds_fresh_active_set_landscape_atlas_after_failed_v15dr_mapper"

V15DQ_SEED_SUMMARY = DOC / "v15dq_active_set_taxonomy_seed_summary.csv"
V15DR_SEED_EVALUATION = DOC / "v15dr_active_set_taxonomy_mapper_seed_evaluation.csv"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15dn.safe_float(x, default)


def safe_int(x: Any, default: int = 0) -> int:
    return v15dn.safe_int(x, default)


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


def fmt(x: Any, digits: int = 3) -> str:
    return v15dn.fmt(x, digits=digits)


def mean_defined(values: Iterable[Any]) -> float:
    return v15dn.mean_defined(values)


def median_defined(values: Iterable[Any]) -> float:
    return v15dn.median_defined(values)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    return v15dn.read_csv(Path(path))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dn.write_csv(Path(path), rows)


def format_set(values: Iterable[int]) -> str:
    vals = sorted(int(x) for x in values)
    return ";".join(f"p{x}" for x in vals) if vals else "none"


def set_from_label(label: str) -> set[int]:
    return v15dq.parse_set(label)


def build_bases() -> Tuple[Dict[int, Any], Dict[int, Mapping[str, Any]], Sequence[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))

    states: Dict[int, Any] = {}
    base_by_seed: Dict[int, Mapping[str, Any]] = {}
    for seed in GROWTH_SEEDS:
        states[seed] = base_states[(ensembles[0].name, seed)]
        base_by_seed[seed] = next(
            row
            for row in base_rows
            if int(row["growth_seed"]) == seed and int(row["target_nodes"]) == TARGET_NODES
        )

    target_summary = [
        {
            **dict(row),
            "atlas_growth_seeds": ";".join(str(seed) for seed in GROWTH_SEEDS),
            "atlas_kind": "v15ds_active_set_landscape_atlas",
        }
        for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    return states, base_by_seed, target_summary


def morphology_rows_for_seed(base_state: Any, growth_seed: int) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        row = dict(v15dl.morphology_for_seed_placement(base_state, growth_seed, placement))
        row["atlas_source"] = ATLAS_SOURCE
        row["pre_registered_before_dynamics"] = 1
        rows.append(row)
    return rows


def prior_seed_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for raw in read_csv(V15DQ_SEED_SUMMARY):
        rows.append(
            {
                "prior_source": "v15dq",
                "growth_seed": safe_int(raw.get("growth_seed")),
                "landscape_class": raw.get("landscape_class", ""),
                "active_placements": raw.get("active_placements", ""),
            }
        )
    for raw in read_csv(V15DR_SEED_EVALUATION):
        rows.append(
            {
                "prior_source": "v15dr",
                "growth_seed": safe_int(raw.get("growth_seed")),
                "landscape_class": raw.get("actual_type", ""),
                "active_placements": raw.get("actual_active_placements", ""),
            }
        )
    return rows


def class_summary_rows(seed_rows: Sequence[Mapping[str, Any]], *, source_label: str) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in seed_rows:
        grouped[str(row["landscape_class"])].append(row)

    out: List[Dict[str, Any]] = []
    total = len(seed_rows)
    for klass, group in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(
            {
                "source": source_label,
                "landscape_class": klass,
                "n_seeds": len(group),
                "seed_fraction": safe_div(len(group), total),
                "growth_seeds": ";".join(str(safe_int(row["growth_seed"])) for row in group),
                "active_placements_examples": ";".join(sorted(set(str(row["active_placements"]) for row in group))),
                "mean_active_count": mean_defined(row.get("active_count", len(set_from_label(str(row["active_placements"])))) for row in group),
                "median_p0_established_rate": median_defined(row.get("p0_established_rate") for row in group),
                "median_p1_established_rate": median_defined(row.get("p1_established_rate") for row in group),
                "median_p2_established_rate": median_defined(row.get("p2_established_rate") for row in group),
            }
        )
    return out


def run_single(
    *,
    growth_seed: int,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    v15dk.GROWTH_SEED = int(growth_seed)
    v15dk.FRESH_SEED_DELTAS = FRESH_SEED_DELTAS
    comps, events, row = v15dk.run_single(
        base_state=base_state,
        base_row=base_row,
        params=params,
        placement=int(placement),
        seed_delta=int(seed_delta),
    )
    out = dict(row)
    out["source_scope"] = f"v15ds_growth_seed_{growth_seed}_p{placement}"
    out["pre_registered_landscape_atlas"] = 1
    out["pre_registered_taxonomy_mapper_holdout"] = 0
    out["pre_registered_active_set_type_guard_holdout"] = 0
    out["pre_registered_support_rank_holdout"] = 0
    out["pre_registered_return_probability_holdout"] = 0
    out["atlas_source"] = ATLAS_SOURCE
    return comps, events, out


def enrich_rows_seed_aware(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    spec_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    return v15dr.enrich_rows_seed_aware(
        raw_rows=raw_rows,
        component_rows=component_rows,
        spec_rows=spec_rows,
    )


def add_pre_run_morphology_fields(
    run_rows: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    morph_by_seed_placement = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"])): row
        for row in morphology_rows
    }
    out: List[Dict[str, Any]] = []
    for raw in run_rows:
        row = dict(raw)
        seed = safe_int(row["growth_seed"])
        placement = safe_int(row["placement"])
        morph = morph_by_seed_placement[(seed, placement)]
        row["atlas_source"] = ATLAS_SOURCE
        row["morph_support_signature"] = morph.get("support_signature", "")
        for field in (
            "mean_support_degree",
            "support_ball_1",
            "support_ball_2",
            "support_ball_3",
            "support_ball2_minus_ball1",
            "support_ball3_minus_ball1",
            "support_ball3_minus_ball2",
            "support_boundary_to_volume",
            "support_pairwise_mean_distance",
            "support_pairwise_max_distance",
            "local_ball3_beta1",
            "local_ball3_boundary_to_volume",
            "base_return_t2",
            "base_return_t4",
            "base_return_t6",
            "delta_return_t2",
            "delta_return_t4",
            "delta_return_t6",
            "new_edge_mean_forman",
        ):
            row[f"morph_{field}"] = morph.get(field, "")
        out.append(row)
    return out


def placement_summary_rows(
    run_rows: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    morph_by_seed_placement = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"])): row
        for row in morphology_rows
    }
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[(safe_int(row["growth_seed"]), safe_int(row["placement"]))].append(row)

    out: List[Dict[str, Any]] = []
    for (seed, placement), group in sorted(grouped.items()):
        counts = Counter(str(row["far_shell_horizon_label"]) for row in group)
        n = len(group)
        established_rate = counts.get("established_far_shell_horizon", 0) / max(1, n)
        morph = morph_by_seed_placement[(seed, placement)]
        out.append(
            {
                "target_nodes": TARGET_NODES,
                "growth_seed": seed,
                "perturbation": PERTURBATION,
                "placement": placement,
                "support_signature": morph["support_signature"],
                "n_runs": n,
                "label_counts": ";".join(f"{key}:{counts[key]}" for key in sorted(counts)),
                "established_rate": established_rate,
                "active_placement": int(established_rate >= ACTIVE_ESTABLISHED_RATE),
                "mixed_rate": counts.get("mixed_far_shell_horizon", 0) / max(1, n),
                "failed_rate": counts.get("failed_far_shell_horizon", 0) / max(1, n),
                "no_horizon_rate": counts.get("no_far_shell_horizon", 0) / max(1, n),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "median_boundary_mass": median_defined(safe_float(row.get(v15dg.PRIMARY_METRIC)) for row in group),
                "median_genealogy_intensity": median_defined(safe_float(row.get(v15da.PRIMARY_SCORE)) for row in group),
                "morph_delta_return_t2": morph.get("delta_return_t2", ""),
                "morph_delta_return_t4": morph.get("delta_return_t4", ""),
                "morph_local_ball3_beta1": morph.get("local_ball3_beta1", ""),
                "morph_new_edge_mean_forman": morph.get("new_edge_mean_forman", ""),
                "atlas_source": ATLAS_SOURCE,
            }
        )
    return out


def seed_summary_rows(
    placement_rows: Sequence[Mapping[str, Any]],
    prior_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    prior_classes = {str(row["landscape_class"]) for row in prior_rows}
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in placement_rows:
        grouped[safe_int(row["growth_seed"])].append(row)

    out: List[Dict[str, Any]] = []
    for seed, group in sorted(grouped.items()):
        active = {
            safe_int(row["placement"])
            for row in group
            if safe_int(row.get("active_placement")) == 1
        }
        rates = {safe_int(row["placement"]): safe_float(row["established_rate"]) for row in group}
        strongest = max(rates, key=lambda p: rates[p]) if rates else -1
        klass = v15dq.landscape_class(active)
        out.append(
            {
                "target_nodes": TARGET_NODES,
                "growth_seed": seed,
                "perturbation": PERTURBATION,
                "active_count": len(active),
                "active_placements": format_set(active),
                "landscape_class": klass,
                "class_seen_before_v15ds": int(klass in prior_classes),
                "new_class_in_v15ds": int(klass not in prior_classes),
                "strongest_placement": f"p{strongest}" if strongest >= 0 else "none",
                "strongest_established_rate": rates.get(strongest, float("nan")),
                "p0_established_rate": rates.get(0, float("nan")),
                "p1_established_rate": rates.get(1, float("nan")),
                "p2_established_rate": rates.get(2, float("nan")),
                "placement_rates": ";".join(f"p{p}:{fmt(rates.get(p))}" for p in PLACEMENTS),
                "support_signatures": ";".join(
                    f"p{safe_int(row['placement'])}:{row['support_signature']}"
                    for row in sorted(group, key=lambda r: safe_int(r["placement"]))
                ),
                "atlas_source": ATLAS_SOURCE,
            }
        )
    return out


def combined_seed_rows(
    prior_rows: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in prior_rows:
        active = set_from_label(str(row["active_placements"]))
        out.append(
            {
                "source": row["prior_source"],
                "growth_seed": safe_int(row["growth_seed"]),
                "landscape_class": row["landscape_class"],
                "active_placements": row["active_placements"],
                "active_count": len(active),
            }
        )
    for row in seed_rows:
        out.append(
            {
                "source": "v15ds",
                "growth_seed": safe_int(row["growth_seed"]),
                "landscape_class": row["landscape_class"],
                "active_placements": row["active_placements"],
                "active_count": row["active_count"],
            }
        )
    return out


def matched_seed_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_seed_delta: Dict[Tuple[int, int], Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        key = (safe_int(row["growth_seed"]), safe_int(row["seed_delta"]))
        by_seed_delta[key][safe_int(row["placement"])] = row

    out: List[Dict[str, Any]] = []
    for (growth_seed, seed_delta), group in sorted(by_seed_delta.items()):
        if any(p not in group for p in PLACEMENTS):
            continue
        p0, p1, p2 = group[0], group[1], group[2]
        out.append(
            {
                "growth_seed": growth_seed,
                "seed_delta": seed_delta,
                "p0_label": p0["far_shell_horizon_label"],
                "p1_label": p1["far_shell_horizon_label"],
                "p2_label": p2["far_shell_horizon_label"],
                "p0_analysis_group": p0["analysis_group"],
                "p1_analysis_group": p1["analysis_group"],
                "p2_analysis_group": p2["analysis_group"],
                "p0_boundary_mass": safe_float(p0[v15dg.PRIMARY_METRIC]),
                "p1_boundary_mass": safe_float(p1[v15dg.PRIMARY_METRIC]),
                "p2_boundary_mass": safe_float(p2[v15dg.PRIMARY_METRIC]),
                "p0_genealogy_intensity": safe_float(p0[v15da.PRIMARY_SCORE]),
                "p1_genealogy_intensity": safe_float(p1[v15da.PRIMARY_SCORE]),
                "p2_genealogy_intensity": safe_float(p2[v15da.PRIMARY_SCORE]),
            }
        )
    return out


def atlas_evaluation_rows(
    *,
    prior_rows: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
    class_rows: Sequence[Mapping[str, Any]],
    combined_class_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    prior_classes = {str(row["landscape_class"]) for row in prior_rows}
    v15ds_classes = {str(row["landscape_class"]) for row in seed_rows}
    new_classes = sorted(v15ds_classes - prior_classes)
    repeated_in_v15ds = [
        str(row["landscape_class"])
        for row in class_rows
        if safe_int(row["n_seeds"]) >= 2
    ]
    combined_repeated = [
        str(row["landscape_class"])
        for row in combined_class_rows
        if safe_int(row["n_seeds"]) >= 2
    ]
    seed_count = len(seed_rows)
    new_seed_count = sum(safe_int(row["new_class_in_v15ds"]) for row in seed_rows)
    known_seed_count = seed_count - new_seed_count
    active_seed_count = sum(1 for row in seed_rows if safe_int(row["active_count"]) > 0)
    no_active_seed_count = seed_count - active_seed_count

    return [
        {
            "key": "atlas_source",
            "value": ATLAS_SOURCE,
            "evidence": "fresh growth-seed class-frequency atlas; no selector prediction",
        },
        {
            "key": "seed_count",
            "value": seed_count,
            "evidence": ";".join(str(row["growth_seed"]) for row in seed_rows),
        },
        {
            "key": "prior_class_count",
            "value": len(prior_classes),
            "evidence": ";".join(sorted(prior_classes)),
        },
        {
            "key": "v15ds_class_count",
            "value": len(v15ds_classes),
            "evidence": ";".join(sorted(v15ds_classes)),
        },
        {
            "key": "new_class_count",
            "value": len(new_classes),
            "evidence": ";".join(new_classes) or "none",
        },
        {
            "key": "new_seed_fraction",
            "value": fmt(safe_div(new_seed_count, seed_count)),
            "evidence": f"new_seed_count={new_seed_count}; known_seed_count={known_seed_count}",
        },
        {
            "key": "active_seed_fraction",
            "value": fmt(safe_div(active_seed_count, seed_count)),
            "evidence": f"active_seed_count={active_seed_count}; no_active_seed_count={no_active_seed_count}",
        },
        {
            "key": "repeated_classes_within_v15ds",
            "value": ";".join(repeated_in_v15ds) or "none",
            "evidence": "classes with at least two v15ds growth seeds",
        },
        {
            "key": "combined_repeated_classes",
            "value": ";".join(combined_repeated) or "none",
            "evidence": "classes with at least two seeds across v15dq+v15dr+v15ds",
        },
        {
            "key": "atlas_status",
            "value": atlas_status(seed_rows, class_rows, new_classes, repeated_in_v15ds),
            "evidence": "class-frequency atlas status; not a selector metric",
        },
    ]


def atlas_status(
    seed_rows: Sequence[Mapping[str, Any]],
    class_rows: Sequence[Mapping[str, Any]],
    new_classes: Sequence[str],
    repeated_in_v15ds: Sequence[str],
) -> str:
    if not seed_rows:
        return "atlas_failed_no_rows"
    if len(repeated_in_v15ds) >= 2 and len(new_classes) == 0:
        return "class_frequency_atlas_stabilizing"
    if repeated_in_v15ds and len(new_classes) <= 1:
        return "class_frequency_atlas_partially_stable"
    if repeated_in_v15ds and len(new_classes) > 1:
        return "atlas_partial_repetition_but_taxonomy_still_expanding"
    if len(new_classes) >= 2:
        return "taxonomy_still_expanding"
    return "atlas_inconclusive_sparse_classes"


def group_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["analysis_group"])].append(row)
    out: List[Dict[str, Any]] = []
    for group, group_rows in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group_rows)
        placements = Counter(f"p{safe_int(row['placement'])}" for row in group_rows)
        seeds = Counter(str(safe_int(row["growth_seed"])) for row in group_rows)
        out.append(
            {
                "analysis_group": group,
                "n_runs": len(group_rows),
                "growth_seeds": ";".join(f"{k}:{v}" for k, v in sorted(seeds.items())),
                "placements": ";".join(f"{k}:{v}" for k, v in sorted(placements.items())),
                "labels": ";".join(f"{k}:{v}" for k, v in sorted(labels.items())),
                "median_boundary_mass": median_defined(safe_float(row[v15dg.PRIMARY_METRIC]) for row in group_rows),
                "median_static_support_degree": median_defined(safe_float(row[v15dg.STATIC_AUDIT_METRIC]) for row in group_rows),
                "median_genealogy_intensity": median_defined(safe_float(row[v15da.PRIMARY_SCORE]) for row in group_rows),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group_rows),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
    class_rows: Sequence[Mapping[str, Any]],
    atlas_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(safe_int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((safe_int(row["requested_match"]) for row in run_rows), default=0) == 1
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    classes = Counter(str(row["landscape_class"]) for row in seed_rows)
    new_class_count = next(row for row in atlas_eval if row["key"] == "new_class_count")
    new_seed_fraction = next(row for row in atlas_eval if row["key"] == "new_seed_fraction")
    repeated = next(row for row in atlas_eval if row["key"] == "repeated_classes_within_v15ds")
    status = next(row for row in atlas_eval if row["key"] == "atlas_status")
    primary_dynamic = next(row for row in metric_rows if str(row["metric"]) == v15dg.PRIMARY_METRIC)

    if status["value"] in {"class_frequency_atlas_stabilizing", "class_frequency_atlas_partially_stable"}:
        next_status = "stratify_next_selector_by_repeated_classes"
        next_note = "Atlaset viser repeterte klasser med begrenset novelty; neste selector bor vaere OOD-first og klasse-stratifisert."
    elif status["value"] == "atlas_partial_repetition_but_taxonomy_still_expanding":
        next_status = "extend_atlas_before_new_mapper"
        next_note = "Noen klasser repeterer, men taxonomy ekspanderer fortsatt; kjoer ett atlassteg til eller bygg OOD-abstention foer mapping."
    elif status["value"] == "taxonomy_still_expanding":
        next_status = "continue_landscape_atlas_or_retire_selector_ambition"
        next_note = "Fresh seeds lager flere nye klasser; selector-sprak er for tidlig uten bedre klassebase-rate."
    else:
        next_status = "one_more_small_atlas_needed"
        next_note = "Klassebildet er fortsatt for sparse til aa velge mellom stabilisering og ekspansjon."

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
            "diagnostic_family": "atlas_design",
            "status": "class_frequency_atlas_no_selector",
            "note": "Denne runden skriver pre-run morphology, men bruker ikke pre-run features som prediksjon eller refit.",
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "fresh_growth_seed_taxonomy_recorded",
            "note": (
                f"Run labels: {';'.join(f'{k}:{v}' for k, v in sorted(labels.items()))}. "
                f"Seed classes: {';'.join(f'{k}:{v}' for k, v in sorted(classes.items()))}."
            ),
        },
        {
            "diagnostic_family": "class_landscape_result",
            "status": str(status["value"]),
            "note": (
                f"new_class_count={new_class_count['value']}; new_seed_fraction={new_seed_fraction['value']}; "
                f"repeated_within_v15ds={repeated['value']}."
            ),
        },
        {
            "diagnostic_family": "dynamic_boundary_mass_audit",
            "status": "reported_descriptive_not_primary_selector",
            "note": f"`{v15dg.PRIMARY_METRIC}` AUC established-vs-no={fmt(primary_dynamic['auc_established_vs_no'])}.",
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
    placement_rows: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
    class_rows: Sequence[Mapping[str, Any]],
    combined_class_rows: Sequence[Mapping[str, Any]],
    atlas_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ds: active-set landscape atlas")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er et fresh active-set landskapsatlas etter v15dr.")
    lines.append("Mapperen fra v15dr refittes ikke. Primarproduktet er klassefrekvens, klasse-novelty og per-seed active-set.")
    lines.append("Pre-run morphology skrives foer dynamikk-loop, men brukes bare som auditgrunnlag.")
    lines.append("")
    lines.append("## Pre-registered scope")
    lines.append("")
    lines.extend(
        table(
            [
                {"field": "target", "value": TARGET_NODES},
                {"field": "growth_seeds", "value": ";".join(str(seed) for seed in GROWTH_SEEDS)},
                {"field": "perturbation", "value": PERTURBATION},
                {"field": "placements", "value": ";".join(f"p{x}" for x in PLACEMENTS)},
                {"field": "seed_deltas", "value": ";".join(str(x) for x in FRESH_SEED_DELTAS)},
                {"field": "active_threshold", "value": f"established_rate_ge_{fmt(ACTIVE_ESTABLISHED_RATE, 2)}"},
                {"field": "atlas_source", "value": ATLAS_SOURCE},
            ],
            ("field", "value"),
        )
    )
    lines.append("")
    lines.append("## Seed-level atlas")
    lines.append("")
    lines.extend(
        table(
            seed_rows,
            (
                "growth_seed",
                "landscape_class",
                "active_placements",
                "class_seen_before_v15ds",
                "new_class_in_v15ds",
                "placement_rates",
                "strongest_placement",
                "strongest_established_rate",
            ),
        )
    )
    lines.append("")
    lines.append("## v15ds class frequencies")
    lines.append("")
    lines.extend(
        table(
            class_rows,
            (
                "landscape_class",
                "n_seeds",
                "seed_fraction",
                "growth_seeds",
                "median_p0_established_rate",
                "median_p1_established_rate",
                "median_p2_established_rate",
            ),
        )
    )
    lines.append("")
    lines.append("## Combined class frequencies")
    lines.append("")
    lines.extend(
        table(
            combined_class_rows,
            (
                "landscape_class",
                "n_seeds",
                "seed_fraction",
                "growth_seeds",
                "active_placements_examples",
            ),
        )
    )
    lines.append("")
    lines.append("## Placement outcomes")
    lines.append("")
    lines.extend(
        table(
            placement_rows,
            (
                "growth_seed",
                "placement",
                "label_counts",
                "established_rate",
                "active_placement",
                "median_boundary_mass",
                "median_genealogy_intensity",
            ),
        )
    )
    lines.append("")
    lines.append("## Atlas evaluation")
    lines.append("")
    lines.extend(table(atlas_eval, ("key", "value", "evidence")))
    lines.append("")
    lines.append("## Dynamic metric audit")
    lines.append("")
    lines.extend(
        table(
            metric_rows,
            ("metric", "role", "auc_established_vs_no", "median_established_raw", "median_no_horizon_raw"),
        )
    )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en klassefrekvensrunde, ikke en ny selector.")
    lines.append("- Repeterte klasser er nyttige som atlasstruktur, men er ikke partikler eller universelle arter.")
    lines.append("- Hvis nye klasser dukker opp i senere atlasrunder, betyr det at active-set-rommet fortsatt ekspanderer under fresh growth seeds.")
    lines.append("- Ikke oppgrader dette til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15ds", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit v15dr-mapperen etter dette atlaset.")
    lines.append("- Bruk klassefrekvenser og novelty som beslutningsgrunnlag foer ny selector.")
    lines.append("- Hvis taxonomy fortsatt ekspanderer, prioriter OOD/atlas fremfor selector-claim.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ds",
            "",
            "Denne runden lager et kart over hvilke lokale plasseringer som faktisk blir aktive i nye startgrafer.",
            "",
            "Poenget er ikke aa forutsi alt ennaa. Poenget er aa finne ut om landskapet har noen faa gjentagende typer, eller om nye typer fortsatt dukker opp.",
            "",
            f"- Hovedlesning: `{diag['class_landscape_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er nyttig fordi en god selector trenger et stabilt klassekart. Hvis kartet stadig faar nye klasser, er det for tidlig aa snakke som om vi har en regel.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ds active-set landscape atlas.")
    p.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregate/report files from existing v15ds CSV outputs.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_target_summary.csv"))
    p.add_argument("--out-morphology-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_pre_run_morphology.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_run_features.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_placement_summary.csv"))
    p.add_argument("--out-seed-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_seed_summary.csv"))
    p.add_argument("--out-class-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_class_summary.csv"))
    p.add_argument("--out-prior-class-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_prior_class_summary.csv"))
    p.add_argument("--out-combined-class-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_combined_class_summary.csv"))
    p.add_argument("--out-eval-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_evaluation.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15ds_active_set_landscape_atlas_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15ds_active_set_landscape_atlas.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15ds_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15ds.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    prior_rows = prior_seed_rows()
    if args.reuse_existing:
        target_summary = read_csv(args.out_target_csv)
        morphology_rows = read_csv(args.out_morphology_csv)
        component_rows = read_csv(args.out_components_csv)
        event_rows = read_csv(args.out_events_csv)
        blind_rows = read_csv(args.out_blind_csv)
        run_rows = read_csv(args.out_runs_csv)
    else:
        spec_rows = read_csv(v15da.V15CZ_SCORE_SPEC)
        base_states, base_rows, target_summary = build_bases()
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

        morphology_rows: List[Dict[str, Any]] = []
        for growth_seed in GROWTH_SEEDS:
            morphology_rows.extend(morphology_rows_for_seed(base_states[growth_seed], growth_seed))
        write_csv(args.out_morphology_csv, morphology_rows)
        write_csv(args.out_target_csv, target_summary)
        print(f"wrote pre-run morphology {args.out_morphology_csv}")
        for row in morphology_rows:
            print(
                "pre-run morphology "
                f"seed={safe_int(row['growth_seed'])} "
                f"p{safe_int(row['placement'])} "
                f"support={row.get('support_signature', '')} "
                f"delta_return_t2={fmt(row.get('delta_return_t2'))}"
            )

        component_rows: List[Dict[str, Any]] = []
        event_rows: List[Dict[str, Any]] = []
        raw_rows: List[Dict[str, Any]] = []
        for growth_seed in GROWTH_SEEDS:
            for placement in PLACEMENTS:
                for seed_delta in FRESH_SEED_DELTAS:
                    print(f"running growth_seed {growth_seed} p{placement} seed_delta {seed_delta}")
                    comps, events, row = run_single(
                        growth_seed=growth_seed,
                        base_state=base_states[growth_seed],
                        base_row=base_rows[growth_seed],
                        params=params,
                        placement=int(placement),
                        seed_delta=int(seed_delta),
                    )
                    component_rows.extend(comps)
                    event_rows.extend(events)
                    raw_rows.append(row)

        run_rows, blind_rows = enrich_rows_seed_aware(
            raw_rows=raw_rows,
            component_rows=component_rows,
            spec_rows=spec_rows,
        )
        run_rows = add_pre_run_morphology_fields(run_rows, morphology_rows)

    metric_rows = v15dg.metric_score_rows(run_rows)
    group_rows = group_summary_rows(run_rows)
    matched_rows = matched_seed_rows(run_rows)
    placement_rows = placement_summary_rows(run_rows, morphology_rows)
    seed_rows = seed_summary_rows(placement_rows, prior_rows)
    class_rows = class_summary_rows(seed_rows, source_label="v15ds")
    prior_class_rows = class_summary_rows(prior_rows, source_label="v15dq_plus_v15dr")
    combined_rows = combined_seed_rows(prior_rows, seed_rows)
    combined_class_rows = class_summary_rows(combined_rows, source_label="v15dq_plus_v15dr_plus_v15ds")
    atlas_eval = atlas_evaluation_rows(
        prior_rows=prior_rows,
        seed_rows=seed_rows,
        class_rows=class_rows,
        combined_class_rows=combined_class_rows,
    )
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        seed_rows=seed_rows,
        class_rows=class_rows,
        atlas_eval=atlas_eval,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_morphology_csv, morphology_rows)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_seed_csv, seed_rows)
    write_csv(args.out_class_csv, class_rows)
    write_csv(args.out_prior_class_csv, prior_class_rows)
    write_csv(args.out_combined_class_csv, combined_class_rows)
    write_csv(args.out_eval_csv, atlas_eval)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            placement_rows=placement_rows,
            seed_rows=seed_rows,
            class_rows=class_rows,
            combined_class_rows=combined_class_rows,
            atlas_eval=atlas_eval,
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
