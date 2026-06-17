#!/usr/bin/env python3
"""v0.15dm frozen return-probability morphology holdout.

Fresh small growth-seed holdout for the v15dl scout:
`delta_return_t2` higher-is-better.

Discipline:
- compute the v15dl morphology ranking before any dynamic run,
- write the pre-run ranking CSV before the run loop,
- keep scope narrow: target 1024, add_chord, placements p0/p1/p2,
- run all three placements so top1/top2 capture can be judged honestly,
- do not refit the morphology rule after outcomes.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15dg_boundary_mass_holdout as v15dg
import relational_universe_v15dk_pre_registered_support_rank_holdout as v15dk
import relational_universe_v15dl_base_landscape_morphology_synthesis as v15dl


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEED = 505
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
ACTIVE_ESTABLISHED_RATE = 0.50

PRIMARY_MORPHOLOGY_METRIC = "delta_return_t2"
PRIMARY_MORPHOLOGY_DIRECTION = "higher_is_better"
SECONDARY_MORPHOLOGY_TIEBREAK = "delta_return_t4"
SECONDARY_MORPHOLOGY_DIRECTION = "higher_is_better"

FRESH_SEED_DELTAS = (13007, 13063, 13127, 13187)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


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
    return v15dk.read_csv(path)


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dk.write_csv(path, rows)


def build_base() -> tuple[Any, Mapping[str, Any], Sequence[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(
        row for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) == TARGET_NODES
    )
    target_summary = [
        row for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    return base_state, base_row, target_summary


def pre_run_rank_rows(base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        row = dict(v15dl.morphology_for_seed_placement(base_state, GROWTH_SEED, placement))
        row["rank_metric"] = PRIMARY_MORPHOLOGY_METRIC
        row["rank_direction"] = PRIMARY_MORPHOLOGY_DIRECTION
        row["rank_tiebreak"] = SECONDARY_MORPHOLOGY_TIEBREAK
        rows.append(row)

    ranked = sorted(
        rows,
        key=lambda row: (
            -safe_float(row[PRIMARY_MORPHOLOGY_METRIC]),
            -safe_float(row[SECONDARY_MORPHOLOGY_TIEBREAK]),
            int(row["placement"]),
        ),
    )
    for rank, row in enumerate(ranked, start=1):
        row["pre_run_primary_rank"] = rank
        row["pre_run_top1"] = int(rank == 1)
        row["pre_run_top2"] = int(rank <= 2)
        row["pre_run_rank_metric"] = PRIMARY_MORPHOLOGY_METRIC
        row["pre_run_rank_direction"] = PRIMARY_MORPHOLOGY_DIRECTION
        row["pre_run_secondary_tiebreak"] = SECONDARY_MORPHOLOGY_TIEBREAK
    return sorted(ranked, key=lambda row: int(row["placement"]))


def patch_v15dk_globals() -> None:
    v15dk.GROWTH_SEED = GROWTH_SEED
    v15dk.FRESH_SEED_DELTAS = FRESH_SEED_DELTAS


def run_single(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    patch_v15dk_globals()
    comps, events, row = v15dk.run_single(
        base_state=base_state,
        base_row=base_row,
        params=params,
        placement=int(placement),
        seed_delta=int(seed_delta),
    )
    out = dict(row)
    out["source_scope"] = f"v15dm_growth_seed_{GROWTH_SEED}_p{placement}"
    out["pre_registered_support_rank_holdout"] = 0
    out["pre_registered_return_probability_holdout"] = 1
    return comps, events, out


def add_pre_run_rank_fields(
    run_rows: Sequence[Mapping[str, Any]],
    rank_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
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
            PRIMARY_MORPHOLOGY_METRIC,
            SECONDARY_MORPHOLOGY_TIEBREAK,
            "delta_return_t6",
            "base_return_spectral_dim_proxy",
            "post_return_spectral_dim_proxy",
            "local_ball3_beta1",
            "local_ball3_boundary_to_volume",
            "new_edge_mean_forman",
        ):
            row[field] = rank.get(field, "")
        out.append(row)
    return out


def placement_summary_rows(
    run_rows: Sequence[Mapping[str, Any]],
    rank_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    rank_by_placement = {int(row["placement"]): row for row in rank_rows}
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[int(safe_float(row["placement"]))].append(row)

    out: List[Dict[str, Any]] = []
    for placement, group in sorted(grouped.items()):
        counts = Counter(str(row["far_shell_horizon_label"]) for row in group)
        n = len(group)
        rank = rank_by_placement[placement]
        established_rate = counts.get("established_far_shell_horizon", 0) / max(1, n)
        out.append(
            {
                "growth_seed": GROWTH_SEED,
                "placement": placement,
                "pre_run_primary_rank": int(rank["pre_run_primary_rank"]),
                "pre_run_top1": int(rank["pre_run_top1"]),
                "pre_run_top2": int(rank["pre_run_top2"]),
                "support_signature": rank["support_signature"],
                "rank_metric": PRIMARY_MORPHOLOGY_METRIC,
                "rank_metric_value": safe_float(rank[PRIMARY_MORPHOLOGY_METRIC]),
                "rank_tiebreak": SECONDARY_MORPHOLOGY_TIEBREAK,
                "rank_tiebreak_value": safe_float(rank[SECONDARY_MORPHOLOGY_TIEBREAK]),
                "n_runs": n,
                "label_counts": ";".join(f"{key}:{counts[key]}" for key in sorted(counts)),
                "established_rate": established_rate,
                "active_placement": int(established_rate >= ACTIVE_ESTABLISHED_RATE),
                "mixed_rate": counts.get("mixed_far_shell_horizon", 0) / max(1, n),
                "no_horizon_rate": counts.get("no_far_shell_horizon", 0) / max(1, n),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "median_boundary_mass": median_defined(safe_float(row.get(v15dg.PRIMARY_METRIC)) for row in group),
                "median_genealogy_intensity": median_defined(safe_float(row.get(v15da.PRIMARY_SCORE)) for row in group),
            }
        )
    return out


def morphology_evaluation_rows(placement_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
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
        status = "return_scout_inconclusive_no_active_placements"
    elif top1_capture == active_total and len(active_set) == 1:
        status = "return_scout_supported_top1_single_active"
    elif top2_capture == active_total and top1_capture > 0:
        status = "return_scout_supported_top2_full_capture"
    elif top1_capture > 0 or top2_capture > 0:
        status = "return_scout_weak_partial_capture"
    else:
        status = "return_scout_not_supported"

    return [
        {
            "key": "primary_rank_metric",
            "value": PRIMARY_MORPHOLOGY_METRIC,
            "evidence": f"direction={PRIMARY_MORPHOLOGY_DIRECTION}; tiebreak={SECONDARY_MORPHOLOGY_TIEBREAK}",
        },
        {
            "key": "pre_registration",
            "value": "morphology_rank_written_before_dynamics",
            "evidence": "pre-run ranking CSV is written before defect run loop",
        },
        {
            "key": "active_threshold",
            "value": f"established_rate_ge_{fmt(ACTIVE_ESTABLISHED_RATE, 2)}",
            "evidence": "active placement is evaluated after dynamics, not used in morphology ranking",
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
            "key": "return_scout_status",
            "value": status,
            "evidence": "fresh growth-seed evaluation of the frozen v15dl morphology scout",
        },
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    morphology_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    label_note = ";".join(f"{key}:{labels[key]}" for key in sorted(labels))
    scout_status = next(row for row in morphology_eval if row["key"] == "return_scout_status")
    top1_capture = next(row for row in morphology_eval if row["key"] == "top1_capture_fraction")
    top2_capture = next(row for row in morphology_eval if row["key"] == "top2_capture_fraction")
    primary_dynamic = next(row for row in metric_rows if str(row["metric"]) == v15dg.PRIMARY_METRIC)

    if str(scout_status["value"]).startswith("return_scout_supported"):
        next_status = "replicate_return_probability_scout_on_second_fresh_seed"
        next_note = "Frozen return-probability scout survived this small holdout; replicate before trusting it as selector."
    elif str(scout_status["value"]) == "return_scout_weak_partial_capture":
        next_status = "return_probability_scout_needs_repeat_or_downgrade"
        next_note = "Scout partially captured active placements; too weak for selector language without another fresh seed."
    elif str(scout_status["value"]) == "return_scout_inconclusive_no_active_placements":
        next_status = "choose_new_growth_seed_before_selector_judgement"
        next_note = "No active placement means the selector cannot be judged on this base."
    else:
        next_status = "retire_delta_return_t2_as_selector_candidate"
        next_note = "Frozen return-probability ranking did not capture active placement; do not refit it after outcome."

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
            "status": "return_probability_rank_written_before_dynamics",
            "note": f"Pre-run ranking er frosset til `{PRIMARY_MORPHOLOGY_METRIC}` high-is-better foer dynamikk-loop.",
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "fresh_growth_seed_label_balance_recorded",
            "note": f"Labels: {label_note}.",
        },
        {
            "diagnostic_family": "return_scout_result",
            "status": str(scout_status["value"]),
            "note": f"Top1 capture={top1_capture['value']}; top2 capture={top2_capture['value']}. {scout_status['evidence']}",
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
    rank_rows: Sequence[Mapping[str, Any]],
    placement_rows: Sequence[Mapping[str, Any]],
    morphology_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dm: frozen return-probability morphology holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en liten fresh growth-seed holdout av v15dl sin beste morfologi-scout.")
    lines.append("Ranking beregnes fra basegraf/add_chord-probe foer dynamikk og skrives til CSV foer run-loop.")
    lines.append("Dynamiske observabler rapporteres etterpaa som evaluering/audit, ikke som refit.")
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
                {"field": "rank_metric", "value": PRIMARY_MORPHOLOGY_METRIC},
                {"field": "rank_direction", "value": PRIMARY_MORPHOLOGY_DIRECTION},
                {"field": "rank_tiebreak", "value": SECONDARY_MORPHOLOGY_TIEBREAK},
            ],
            ("field", "value"),
        )
    )
    lines.append("")
    lines.append("## Pre-run morphology ranking")
    lines.append("")
    lines.extend(
        table(
            sorted(rank_rows, key=lambda row: int(row["pre_run_primary_rank"])),
            (
                "pre_run_primary_rank",
                "placement",
                "support_signature",
                PRIMARY_MORPHOLOGY_METRIC,
                SECONDARY_MORPHOLOGY_TIEBREAK,
                "delta_return_t6",
                "base_return_spectral_dim_proxy",
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
    lines.append("## Morphology-scout evaluation")
    lines.append("")
    lines.extend(table(morphology_eval, ("key", "value", "evidence")))
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
    lines.append("- Hvis return-probability-rankingen treffer, er det en placement-prior som maa replikeres, ikke en fysikklov.")
    lines.append("- Hvis den feiler, skal `delta_return_t2` pensjoneres eller nedgraderes til deskriptiv audit.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dm", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit `delta_return_t2` etter outcome.")
    lines.append("- Ikke bruk boundary/mass eller genealogy-intensity som primary selector i denne runden.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dm",
            "",
            "Denne runden testet om en ny forhåndsregel fra v15dl kunne velge bedre add_chord-plasseringer.",
            "",
            "Regelen ble skrevet ned foer simulasjonen startet: velg hoyest `delta_return_t2`.",
            "",
            f"- Hovedlesning: `{diag['return_scout_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er en test av en lokal prior, ikke en paastand om en universell fysikklov.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dm frozen return-probability morphology holdout.")
    p.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregate/report files from existing v15dm CSV outputs.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dm_frozen_return_target_summary.csv"))
    p.add_argument("--out-pre-rank-csv", default=str(DOC / "v15dm_frozen_return_pre_run_ranking.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15dm_frozen_return_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15dm_frozen_return_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15dm_frozen_return_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dm_frozen_return_run_features.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dm_frozen_return_placement_summary.csv"))
    p.add_argument("--out-eval-csv", default=str(DOC / "v15dm_frozen_return_evaluation.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dm_frozen_return_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15dm_frozen_return_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dm_frozen_return_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dm_frozen_return_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dm_frozen_return_probability_holdout.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dm_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dm.md"))
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
        patch_v15dk_globals()
        spec_rows = read_csv(v15da.V15CZ_SCORE_SPEC)
        base_state, base_row, target_summary = build_base()
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

        rank_rows = pre_run_rank_rows(base_state)
        write_csv(args.out_pre_rank_csv, rank_rows)
        print(f"wrote pre-run morphology ranking {args.out_pre_rank_csv}")
        for row in sorted(rank_rows, key=lambda x: int(x["pre_run_primary_rank"])):
            print(
                "pre-run rank "
                f"{int(row['pre_run_primary_rank'])}: p{int(row['placement'])} "
                f"{PRIMARY_MORPHOLOGY_METRIC}={fmt(row[PRIMARY_MORPHOLOGY_METRIC])} "
                f"{SECONDARY_MORPHOLOGY_TIEBREAK}={fmt(row[SECONDARY_MORPHOLOGY_TIEBREAK])}"
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

    metric_rows = v15dg.metric_score_rows(run_rows)
    group_rows = v15dg.group_summary_rows(run_rows)
    matched_rows = v15dg.matched_seed_rows(run_rows)
    placement_rows = placement_summary_rows(run_rows, rank_rows)
    morphology_eval = morphology_evaluation_rows(placement_rows)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        morphology_eval=morphology_eval,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_pre_rank_csv, rank_rows)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_eval_csv, morphology_eval)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            rank_rows=rank_rows,
            placement_rows=placement_rows,
            morphology_eval=morphology_eval,
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
