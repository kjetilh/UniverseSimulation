#!/usr/bin/env python3
"""v0.15dg pre-registered boundary/mass holdout.

v15df found a promising strict pre-entry non-route metric:
`w32_mean_boundary_per_mass`. This round freezes that single dynamic metric and
tests it on fresh 1024/add_chord placement runs.

Discipline:
- fresh seed deltas, no reuse from v15da/v15dd/v15df
- same narrow placement contrast: p0, p1, p2
- primary metric is fixed before reading holdout results
- static support geometry is reported only as confound/audit
- route-entry/retention is not used as a feature
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15df_pre_entry_support_topology_synthesis as v15df


DOC = Path("Documentation")

TARGET_NODES = v15da.TARGET_NODES
GROWTH_SEED = v15da.GROWTH_SEED
PERTURBATION = v15da.PERTURBATION
PLACEMENTS = v15da.PLACEMENTS
PRIMARY_METRIC = "w32_mean_boundary_per_mass"
PRIMARY_DIRECTION = "higher_is_established"
STATIC_AUDIT_METRIC = "static_mean_support_degree"
FALSE_POSITIVE_SCORE_FLOOR = v15df.FALSE_POSITIVE_SCORE_FLOOR

FRESH_SEED_DELTAS = (
    10091, 10133, 10177, 10223,
    10271, 10331, 10391, 10453,
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
    vals = sorted(x for x in values if math.isfinite(x))
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
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_key(row: Mapping[str, Any]) -> Tuple[int, int]:
    return int(safe_float(row["placement"])), int(safe_float(row["seed_delta"]))


def pairwise_auc(pos_values: Sequence[float], neg_values: Sequence[float]) -> float:
    return v15df.pairwise_auc(pos_values, neg_values)


def oriented(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row.get(metric))
    return -value if direction == "lower_is_established" else value


def feature_fields_from_components(component_rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    snapshots = v15df.summarize_run_snapshots(component_rows)
    out: Dict[str, Any] = {}
    for window in v15df.STRICT_WINDOWS:
        out.update(v15df.window_summary(snapshots, window))
    return out


def analysis_group(row: Mapping[str, Any]) -> str:
    placement = int(safe_float(row["placement"]))
    label = str(row["far_shell_horizon_label"])
    score = safe_float(row[v15da.PRIMARY_SCORE])
    return v15df.analysis_group(placement, label, score)


def enrich_holdout_rows(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    spec_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    grouped_components: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in component_rows:
        grouped_components[run_key(row)].append(row)

    enriched_raw: List[Dict[str, Any]] = []
    for raw in raw_rows:
        key = run_key(raw)
        features = feature_fields_from_components(grouped_components[key])
        row = {
            **dict(raw),
            "pre_registered_primary_metric": PRIMARY_METRIC,
            "primary_metric_direction": PRIMARY_DIRECTION,
            "metric_source": "v15df_frozen_boundary_mass_no_refit",
        }
        row.update(v15df.static_features(raw))
        row.update(features)
        row["boundary_mass_score"] = safe_float(row[PRIMARY_METRIC])
        row["static_support_audit_score"] = safe_float(row[STATIC_AUDIT_METRIC])
        enriched_raw.append(row)

    scored, blind = v15da.add_frozen_scores(enriched_raw, spec_rows)
    for row in scored:
        row["analysis_group"] = analysis_group(row)
        row["is_p0_high_score_no_horizon"] = int(row["analysis_group"] == "p0_high_score_no_horizon")
    return scored, blind


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    p1_established = [row for row in rows if str(row["analysis_group"]) == "p1_established"]
    p0_false = [row for row in rows if str(row["analysis_group"]) == "p0_high_score_no_horizon"]
    p2_no = [row for row in rows if str(row["analysis_group"]) == "p2_no_horizon"]

    specs = [
        (PRIMARY_METRIC, PRIMARY_DIRECTION, "primary_frozen_dynamic"),
        ("w32_mean_boundary_to_volume", "higher_is_established", "secondary_same_snapshot"),
        ("w32_mean_total_boundary_edges", "higher_is_established", "secondary_same_snapshot"),
        ("w64_mean_boundary_per_mass", "higher_is_established", "secondary_later_strict"),
        ("w96_mean_boundary_per_mass", "higher_is_established", "secondary_later_strict"),
        (STATIC_AUDIT_METRIC, "higher_is_established", "static_support_audit"),
        ("static_support_ball_1", "higher_is_established", "static_support_audit"),
        (v15da.PRIMARY_SCORE, "higher_is_established", "baseline_failed_selector"),
    ]

    out: List[Dict[str, Any]] = []
    for metric, direction, role in specs:
        est_values = [oriented(row, metric, direction) for row in established]
        no_values = [oriented(row, metric, direction) for row in no_horizon]
        p1_values = [oriented(row, metric, direction) for row in p1_established]
        p0_values = [oriented(row, metric, direction) for row in p0_false]
        p2_values = [oriented(row, metric, direction) for row in p2_no]
        raw_est = [safe_float(row.get(metric)) for row in established]
        raw_no = [safe_float(row.get(metric)) for row in no_horizon]
        raw_p1 = [safe_float(row.get(metric)) for row in p1_established]
        raw_p0 = [safe_float(row.get(metric)) for row in p0_false]
        raw_p2 = [safe_float(row.get(metric)) for row in p2_no]
        out.append(
            {
                "metric": metric,
                "role": role,
                "direction": direction,
                "n_established": len(established),
                "n_no_horizon": len(no_horizon),
                "n_p1_established": len(p1_established),
                "n_p0_high_score_no_horizon": len(p0_false),
                "n_p2_no_horizon": len(p2_no),
                "auc_established_vs_no": pairwise_auc(est_values, no_values),
                "auc_p1_established_vs_p0_false_positive": pairwise_auc(p1_values, p0_values),
                "auc_p1_established_vs_p2_no_horizon": pairwise_auc(p1_values, p2_values),
                "median_established_raw": median_defined(raw_est),
                "median_no_horizon_raw": median_defined(raw_no),
                "median_p1_established_raw": median_defined(raw_p1),
                "median_p0_false_positive_raw": median_defined(raw_p0),
                "median_p2_no_horizon_raw": median_defined(raw_p2),
                "median_p1_minus_p0_false_raw": median_defined(raw_p1) - median_defined(raw_p0),
                "median_p1_minus_p2_no_raw": median_defined(raw_p1) - median_defined(raw_p2),
            }
        )
    return out


def group_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["analysis_group"])].append(row)
    out: List[Dict[str, Any]] = []
    for group, group_rows in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group_rows)
        placements = Counter(f"p{int(safe_float(row['placement']))}" for row in group_rows)
        out.append(
            {
                "analysis_group": group,
                "n_runs": len(group_rows),
                "placements": ";".join(f"{k}:{v}" for k, v in sorted(placements.items())),
                "labels": ";".join(f"{k}:{v}" for k, v in sorted(labels.items())),
                "median_boundary_mass": median_defined(safe_float(row[PRIMARY_METRIC]) for row in group_rows),
                "median_static_support_degree": median_defined(safe_float(row[STATIC_AUDIT_METRIC]) for row in group_rows),
                "median_genealogy_intensity": median_defined(safe_float(row[v15da.PRIMARY_SCORE]) for row in group_rows),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group_rows),
            }
        )
    return out


def matched_seed_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_seed: Dict[int, Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_seed[int(safe_float(row["seed_delta"]))][int(safe_float(row["placement"]))] = row
    out: List[Dict[str, Any]] = []
    for seed_delta, group in sorted(by_seed.items()):
        if any(p not in group for p in PLACEMENTS):
            continue
        p0, p1, p2 = group[0], group[1], group[2]
        out.append(
            {
                "seed_delta": seed_delta,
                "p0_label": p0["far_shell_horizon_label"],
                "p1_label": p1["far_shell_horizon_label"],
                "p2_label": p2["far_shell_horizon_label"],
                "p0_analysis_group": p0["analysis_group"],
                "p1_analysis_group": p1["analysis_group"],
                "p2_analysis_group": p2["analysis_group"],
                "p0_boundary_mass": safe_float(p0[PRIMARY_METRIC]),
                "p1_boundary_mass": safe_float(p1[PRIMARY_METRIC]),
                "p2_boundary_mass": safe_float(p2[PRIMARY_METRIC]),
                "p1_minus_p0_boundary_mass": safe_float(p1[PRIMARY_METRIC]) - safe_float(p0[PRIMARY_METRIC]),
                "p1_minus_p2_boundary_mass": safe_float(p1[PRIMARY_METRIC]) - safe_float(p2[PRIMARY_METRIC]),
                "p0_static_support_degree": safe_float(p0[STATIC_AUDIT_METRIC]),
                "p1_static_support_degree": safe_float(p1[STATIC_AUDIT_METRIC]),
                "p2_static_support_degree": safe_float(p2[STATIC_AUDIT_METRIC]),
                "p0_genealogy_intensity": safe_float(p0[v15da.PRIMARY_SCORE]),
                "p1_genealogy_intensity": safe_float(p1[v15da.PRIMARY_SCORE]),
                "p2_genealogy_intensity": safe_float(p2[v15da.PRIMARY_SCORE]),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    group_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    primary = next(row for row in metric_rows if str(row["metric"]) == PRIMARY_METRIC)
    static = next(row for row in metric_rows if str(row["metric"]) == STATIC_AUDIT_METRIC)
    baseline = next(row for row in metric_rows if str(row["metric"]) == v15da.PRIMARY_SCORE)
    n_p1 = int(primary["n_p1_established"])
    n_p0_false = int(primary["n_p0_high_score_no_horizon"])
    n_no = int(primary["n_no_horizon"])
    auc_p0 = safe_float(primary["auc_p1_established_vs_p0_false_positive"])
    auc_all = safe_float(primary["auc_established_vs_no"])
    delta_p0 = safe_float(primary["median_p1_minus_p0_false_raw"])

    enough_false_positive_balance = n_p1 >= 4 and n_p0_false >= 3
    enough_overall_balance = int(primary["n_established"]) >= 4 and n_no >= 8
    if enough_false_positive_balance and auc_p0 >= 0.80 and auc_all >= 0.70 and delta_p0 > 0:
        primary_status = "boundary_mass_holdout_supported"
        next_status = "scale_or_second_growth_seed_with_frozen_boundary_mass"
        next_note = "Kandidaten overlever fresh holdout; neste test bor bruke samme frosne metric paa ny growth seed eller naboskala."
    elif enough_false_positive_balance and (auc_p0 < 0.65 or delta_p0 <= 0):
        primary_status = "boundary_mass_holdout_failed"
        next_status = "retire_boundary_mass_as_selector"
        next_note = "Ikke press boundary/mass videre som selector; behold eventuelt som mekanistisk observabel."
    elif enough_overall_balance and auc_all >= 0.75:
        primary_status = "boundary_mass_overall_promising_but_false_positive_balance_thin"
        next_status = "extend_same_holdout_for_false_positive_balance"
        next_note = "Overordnet established/no signal holder, men p0 high-score/no-horizon-gruppen er for tynn for hovedkontrasten."
    else:
        primary_status = "boundary_mass_holdout_inconclusive_balance"
        next_status = "extend_or_choose_better_negative_control"
        next_note = "Holdouten gir ikke nok balansert p1-vs-p0-false-positive data til aa avgjore kandidaten."

    p1 = next((row for row in group_rows if str(row["analysis_group"]) == "p1_established"), None)
    p0 = next((row for row in group_rows if str(row["analysis_group"]) == "p0_high_score_no_horizon"), None)
    group_note = "Mangler p1-established eller p0 high-score/no-horizon gruppe."
    if p1 and p0:
        group_note = (
            f"p1 median boundary/mass={fmt(p1['median_boundary_mass'])}; "
            f"p0 false-positive median={fmt(p0['median_boundary_mass'])}; "
            f"p1 static support degree={fmt(p1['median_static_support_degree'])}; "
            f"p0 static support degree={fmt(p0['median_static_support_degree'])}."
        )

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
            "status": "frozen_w32_boundary_mass_no_refit",
            "note": f"Primarmetric er frosset til `{PRIMARY_METRIC}` fra v15df; seed-deltaer er fresh og route-entry brukes ikke som feature.",
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "holdout_label_balance",
            "note": (
                f"Labels: {';'.join(f'{k}:{v}' for k, v in sorted(labels.items()))}; "
                f"p1-established={n_p1}, p0-high-score/no-horizon={n_p0_false}, no_horizon={n_no}."
            ),
        },
        {
            "diagnostic_family": "primary_result",
            "status": primary_status,
            "note": (
                f"`{PRIMARY_METRIC}` har AUC={fmt(auc_p0)} mot p0 false positives, "
                f"AUC={fmt(auc_all)} established-vs-no, median p1-p0false delta={fmt(delta_p0)}."
            ),
        },
        {
            "diagnostic_family": "static_confound_audit",
            "status": "static_support_reported_not_primary",
            "note": (
                f"`{STATIC_AUDIT_METRIC}` har AUC={fmt(static['auc_p1_established_vs_p0_false_positive'])} "
                "mot p0 false positives og rapporteres som placement/support-audit, ikke dynamisk selector."
            ),
        },
        {
            "diagnostic_family": "group_reading",
            "status": "p1_vs_p0_false_positive_boundary_mass",
            "note": group_note,
        },
        {
            "diagnostic_family": "baseline_check",
            "status": "genealogy_intensity_control",
            "note": f"Baseline genealogy-intensity har AUC={fmt(baseline['auc_p1_established_vs_p0_false_positive'])} mot p0 false positives.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def build_report(
    *,
    group_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    matched_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dg: boundary/mass holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en fresh dynamisk holdout av v15df-kandidaten.")
    lines.append(f"Primarmetric er frosset til `{PRIMARY_METRIC}` med retning `{PRIMARY_DIRECTION}`.")
    lines.append("Statisk supportgeometri rapporteres bare som confound/audit.")
    lines.append("Route-entry/retention brukes ikke som candidate feature.")
    lines.append("")
    lines.append("## Pre-registered scope")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| target | {TARGET_NODES} |")
    lines.append(f"| growth seed | {GROWTH_SEED} |")
    lines.append(f"| perturbation | {PERTURBATION} |")
    lines.append(f"| placements | {';'.join(f'p{x}' for x in PLACEMENTS)} |")
    lines.append(f"| seed deltas | {';'.join(str(x) for x in FRESH_SEED_DELTAS)} |")
    lines.append(f"| primary metric | {PRIMARY_METRIC} |")
    lines.append(f"| static audit | {STATIC_AUDIT_METRIC} |")
    lines.append("")
    lines.append("## Group summary")
    lines.append("")
    lines.append("| group | n | placements | labels | boundary/mass | static degree | genealogy intensity | mean horizon |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in group_rows:
        lines.append(
            f"| {row['analysis_group']} | {int(row['n_runs'])} | {row['placements']} | {row['labels']} | {fmt(row['median_boundary_mass'])} | {fmt(row['median_static_support_degree'])} | {fmt(row['median_genealogy_intensity'])} | {fmt(row['mean_horizon_span'])} |"
        )
    lines.append("")
    lines.append("## Metric scores")
    lines.append("")
    lines.append("| metric | role | AUC est/no | AUC p1/p0 false | AUC p1/p2 no | median p1 | median p0 false | median p2 no |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in metric_rows:
        lines.append(
            f"| {row['metric']} | {row['role']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['auc_p1_established_vs_p2_no_horizon'])} | {fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} | {fmt(row['median_p2_no_horizon_raw'])} |"
        )
    lines.append("")
    lines.append("## Matched seed comparison")
    lines.append("")
    lines.append("| seed | p0 label | p1 label | p2 label | p0 group | p1 group | p2 group | p0 bm | p1 bm | p2 bm | p1-p0 | p1-p2 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in matched_rows:
        lines.append(
            f"| {int(row['seed_delta'])} | {row['p0_label']} | {row['p1_label']} | {row['p2_label']} | {row['p0_analysis_group']} | {row['p1_analysis_group']} | {row['p2_analysis_group']} | {fmt(row['p0_boundary_mass'])} | {fmt(row['p1_boundary_mass'])} | {fmt(row['p2_boundary_mass'])} | {fmt(row['p1_minus_p0_boundary_mass'])} | {fmt(row['p1_minus_p2_boundary_mass'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette kan validere eller svekke en lokal pre-entry observabel; det kan ikke bevise partikler, Lorentz-likhet, entanglement eller global invariant.")
    lines.append("- Hvis p0 false-positive-gruppen er tynn, er riktig konklusjon balansebegrensning, ikke positivt funn.")
    lines.append("- Statisk supportgeometri maa holdes adskilt fra dynamisk boundary/mass.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dg", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit `w32_mean_boundary_per_mass` etter denne holdouten.")
    lines.append("- Ikke bruk statisk supportgeometri som dynamisk selector.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dg",
            "",
            "Denne runden testet en tidlig lokal form-maaling paa nye runs.",
            "",
            "Spoersmaalet var: kan boundary per defect-masse ved step 32 si noe foer systemet faktisk gaar inn i lang fjernhale?",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er fortsatt en test av en mulig observabel, ikke en paastand om en fysikklov.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dg pre-registered boundary/mass holdout.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dg_boundary_mass_target_summary.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15dg_boundary_mass_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15dg_boundary_mass_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15dg_boundary_mass_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dg_boundary_mass_run_features.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dg_boundary_mass_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15dg_boundary_mass_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dg_boundary_mass_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dg_boundary_mass_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dg_boundary_mass_holdout.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dg_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dg.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
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

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    raw_rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        for seed_delta in FRESH_SEED_DELTAS:
            print(f"running p{placement} seed_delta {seed_delta}")
            comps, events, row = v15da.run_single(
                base_state=base_state,
                base_row=base_row,
                params=params,
                placement=int(placement),
                seed_delta=int(seed_delta),
            )
            component_rows.extend(comps)
            event_rows.extend(events)
            raw_rows.append(row)

    run_rows, blind_rows = enrich_holdout_rows(
        raw_rows=raw_rows,
        component_rows=component_rows,
        spec_rows=spec_rows,
    )
    metric_rows = metric_score_rows(run_rows)
    group_rows = group_summary_rows(run_rows)
    matched_rows = matched_seed_rows(run_rows)
    target_summary = [
        row for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        metric_rows=metric_rows,
        group_rows=group_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            group_rows=group_rows,
            metric_rows=metric_rows,
            matched_rows=matched_rows,
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
