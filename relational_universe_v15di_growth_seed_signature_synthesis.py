#!/usr/bin/env python3
"""v0.15di growth-seed signature synthesis.

No-new-dynamics synthesis of v15dg and v15dh. The goal is not to squeeze more
label budget, but to understand why the v15dg boundary/mass candidate failed
to transfer under the original p1 anchor on growth seed 303.

Inputs:
- v15dg growth seed 202 boundary/mass holdout
- v15dh growth seed 303 boundary/mass holdout

Outputs compare placement response, support signatures, and metric direction.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


DOC = Path("Documentation")

RUN_FEATURE_FILES = (
    ("v15dg", DOC / "v15dg_boundary_mass_run_features.csv"),
    ("v15dh", DOC / "v15dh_boundary_mass_run_features.csv"),
)
TARGET_FILES = (
    ("v15dg", DOC / "v15dg_boundary_mass_target_summary.csv"),
    ("v15dh", DOC / "v15dh_boundary_mass_target_summary.csv"),
)

METRIC_SPECS = (
    ("w32_mean_boundary_per_mass", "primary_frozen_dynamic"),
    ("w32_mean_total_boundary_edges", "secondary_boundary_mass"),
    ("static_mean_support_degree", "static_support_audit"),
    ("static_support_ball_1", "static_support_audit"),
    ("static_support_ball_3", "static_support_audit"),
    ("genealogy_intensity_index", "baseline_descriptive"),
)

SUMMARY_FIELDS = (
    "w32_mean_boundary_per_mass",
    "w32_mean_total_boundary_edges",
    "static_mean_support_degree",
    "static_support_ball_1",
    "static_support_ball_2",
    "static_support_ball_3",
    "static_support_boundary_to_volume",
    "static_support_pairwise_mean_distance",
    "genealogy_intensity_index",
    "high_horizon_span",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def mean_defined(values: Iterable[float]) -> float:
    vals = [safe_float(x) for x in values]
    vals = [x for x in vals if math.isfinite(x)]
    return sum(vals) / len(vals) if vals else float("nan")


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


def pairwise_auc(pos_values: Sequence[float], neg_values: Sequence[float]) -> float:
    pos = [x for x in pos_values if math.isfinite(x)]
    neg = [x for x in neg_values if math.isfinite(x)]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    total = 0
    for p in pos:
        for n in neg:
            total += 1
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total if total else float("nan")


def decisive_label(row: Mapping[str, Any]) -> int:
    label = str(row.get("far_shell_horizon_label", ""))
    if label == "established_far_shell_horizon":
        return 1
    if label == "no_far_shell_horizon":
        return 0
    return -1


def label_counts(rows: Sequence[Mapping[str, Any]]) -> Counter[str]:
    return Counter(str(row["far_shell_horizon_label"]) for row in rows)


def count_label(rows: Sequence[Mapping[str, Any]], label: str) -> int:
    return sum(1 for row in rows if str(row["far_shell_horizon_label"]) == label)


def mode_string(values: Sequence[str]) -> str:
    if not values:
        return ""
    counts = Counter(values)
    best_count = max(counts.values())
    best = sorted(k for k, v in counts.items() if v == best_count)
    return "|".join(best)


def load_run_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for lab, path in RUN_FEATURE_FILES:
        for row in read_csv(path):
            out = dict(row)
            out["source_lab"] = lab
            rows.append(out)
    return rows


def load_target_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for lab, path in TARGET_FILES:
        for row in read_csv(path):
            out = dict(row)
            out["source_lab"] = lab
            rows.append(out)
    return rows


def placement_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(safe_float(row["growth_seed"])), int(safe_float(row["placement"])))].append(row)

    out: List[Dict[str, Any]] = []
    for (growth_seed, placement), group in sorted(grouped.items()):
        counts = label_counts(group)
        n = len(group)
        row: Dict[str, Any] = {
            "growth_seed": growth_seed,
            "placement": placement,
            "n_runs": n,
            "support_signature_mode": mode_string([str(x["support_signature"]) for x in group]),
            "support_signature_unique_count": len({str(x["support_signature"]) for x in group}),
            "label_counts": ";".join(f"{k}:{v}" for k, v in sorted(counts.items())),
            "established_rate": count_label(group, "established_far_shell_horizon") / max(1, n),
            "no_horizon_rate": count_label(group, "no_far_shell_horizon") / max(1, n),
            "mixed_rate": count_label(group, "mixed_far_shell_horizon") / max(1, n),
        }
        for field in SUMMARY_FIELDS:
            row[f"median_{field}"] = median_defined(safe_float(x.get(field)) for x in group)
            row[f"mean_{field}"] = mean_defined(safe_float(x.get(field)) for x in group)
        out.append(row)
    return out


def support_delta_rows(summary_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_placement: Dict[int, Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in summary_rows:
        by_placement[int(row["placement"])][int(row["growth_seed"])] = row

    out: List[Dict[str, Any]] = []
    for placement, group in sorted(by_placement.items()):
        if 202 not in group or 303 not in group:
            continue
        a = group[202]
        b = group[303]
        est_a = safe_float(a["established_rate"])
        est_b = safe_float(b["established_rate"])
        if est_a >= 0.75 and est_b <= 0.25:
            response_shift = "lost_positive_anchor"
        elif est_a <= 0.25 and est_b >= 0.50:
            response_shift = "gained_positive_anchor"
        elif abs(est_b - est_a) >= 0.50:
            response_shift = "large_response_shift"
        else:
            response_shift = "roughly_stable_or_partial"
        out.append(
            {
                "placement": placement,
                "response_shift": response_shift,
                "support_signature_202": a["support_signature_mode"],
                "support_signature_303": b["support_signature_mode"],
                "same_support_signature": int(a["support_signature_mode"] == b["support_signature_mode"]),
                "established_rate_202": est_a,
                "established_rate_303": est_b,
                "delta_established_rate_303_minus_202": est_b - est_a,
                "median_boundary_mass_202": safe_float(a["median_w32_mean_boundary_per_mass"]),
                "median_boundary_mass_303": safe_float(b["median_w32_mean_boundary_per_mass"]),
                "delta_boundary_mass_303_minus_202": safe_float(b["median_w32_mean_boundary_per_mass"]) - safe_float(a["median_w32_mean_boundary_per_mass"]),
                "median_static_support_degree_202": safe_float(a["median_static_mean_support_degree"]),
                "median_static_support_degree_303": safe_float(b["median_static_mean_support_degree"]),
                "delta_static_support_degree_303_minus_202": safe_float(b["median_static_mean_support_degree"]) - safe_float(a["median_static_mean_support_degree"]),
                "median_static_support_ball_1_202": safe_float(a["median_static_support_ball_1"]),
                "median_static_support_ball_1_303": safe_float(b["median_static_support_ball_1"]),
                "delta_static_support_ball_1_303_minus_202": safe_float(b["median_static_support_ball_1"]) - safe_float(a["median_static_support_ball_1"]),
                "median_static_support_ball_3_202": safe_float(a["median_static_support_ball_3"]),
                "median_static_support_ball_3_303": safe_float(b["median_static_support_ball_3"]),
                "delta_static_support_ball_3_303_minus_202": safe_float(b["median_static_support_ball_3"]) - safe_float(a["median_static_support_ball_3"]),
                "median_genealogy_intensity_202": safe_float(a["median_genealogy_intensity_index"]),
                "median_genealogy_intensity_303": safe_float(b["median_genealogy_intensity_index"]),
                "delta_genealogy_intensity_303_minus_202": safe_float(b["median_genealogy_intensity_index"]) - safe_float(a["median_genealogy_intensity_index"]),
            }
        )
    return out


def outcome_matrix_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(safe_float(row["growth_seed"])), int(safe_float(row["placement"])))].append(row)
    for (growth_seed, placement), group in sorted(grouped.items()):
        counts = label_counts(group)
        out.append(
            {
                "growth_seed": growth_seed,
                "placement": placement,
                "n_runs": len(group),
                "established": counts.get("established_far_shell_horizon", 0),
                "no_horizon": counts.get("no_far_shell_horizon", 0),
                "mixed": counts.get("mixed_far_shell_horizon", 0),
                "dominant_label": counts.most_common(1)[0][0] if counts else "",
            }
        )
    return out


def metric_audit_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    scopes: List[Tuple[str, List[Mapping[str, Any]]]] = [("all", list(rows))]
    for growth_seed in sorted({int(safe_float(row["growth_seed"])) for row in rows}):
        scopes.append((f"growth_seed_{growth_seed}", [row for row in rows if int(safe_float(row["growth_seed"])) == growth_seed]))

    out: List[Dict[str, Any]] = []
    for scope, scope_rows in scopes:
        decisive = [row for row in scope_rows if decisive_label(row) in (0, 1)]
        established = [row for row in decisive if decisive_label(row) == 1]
        no_horizon = [row for row in decisive if decisive_label(row) == 0]
        for metric, role in METRIC_SPECS:
            pos = [safe_float(row.get(metric)) for row in established]
            neg = [safe_float(row.get(metric)) for row in no_horizon]
            auc = pairwise_auc(pos, neg)
            if math.isfinite(auc) and auc >= 0.80:
                status = "strong_positive_direction"
            elif math.isfinite(auc) and auc <= 0.40:
                status = "inverted_or_failed_direction"
            elif math.isfinite(auc):
                status = "weak_or_mixed_direction"
            else:
                status = "undefined_balance"
            out.append(
                {
                    "scope": scope,
                    "metric": metric,
                    "role": role,
                    "n_established": len(established),
                    "n_no_horizon": len(no_horizon),
                    "auc_established_vs_no": auc,
                    "median_established": median_defined(pos),
                    "median_no_horizon": median_defined(neg),
                    "status": status,
                }
            )
    return out


def diagnosis_rows(
    *,
    run_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    support_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    artifact_clean = all(int(safe_float(row.get("requested_match"), 0)) == 1 for row in run_rows)
    artifact_clean = artifact_clean and all(int(safe_float(row.get("separated_from_prev"), 0)) == 1 for row in target_rows)
    p1 = next(row for row in support_rows if int(row["placement"]) == 1)
    p0 = next(row for row in support_rows if int(row["placement"]) == 0)
    p2 = next(row for row in support_rows if int(row["placement"]) == 2)
    bm_202 = next(row for row in metric_rows if row["scope"] == "growth_seed_202" and row["metric"] == "w32_mean_boundary_per_mass")
    bm_303 = next(row for row in metric_rows if row["scope"] == "growth_seed_303" and row["metric"] == "w32_mean_boundary_per_mass")
    stat_202 = next(row for row in metric_rows if row["scope"] == "growth_seed_202" and row["metric"] == "static_mean_support_degree")
    stat_303 = next(row for row in metric_rows if row["scope"] == "growth_seed_303" and row["metric"] == "static_mean_support_degree")
    gene_303 = next(row for row in metric_rows if row["scope"] == "growth_seed_303" and row["metric"] == "genealogy_intensity_index")

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if artifact_clean else "unclear",
            "note": "Requested perturbations matcher og target-storrelsesseparasjon er clean." if artifact_clean else "Artifact-controls er ikke clean.",
        },
        {
            "diagnostic_family": "placement_transfer",
            "status": "placement_landscape_not_growth_seed_stable",
            "note": (
                f"p1 established-rate endres {fmt(p1['established_rate_202'])}->{fmt(p1['established_rate_303'])}; "
                f"p0 endres {fmt(p0['established_rate_202'])}->{fmt(p0['established_rate_303'])}; "
                f"p2 endres {fmt(p2['established_rate_202'])}->{fmt(p2['established_rate_303'])}."
            ),
        },
        {
            "diagnostic_family": "support_signature",
            "status": "support_signatures_change_by_growth_seed",
            "note": (
                f"p1-support endres `{p1['support_signature_202']}` -> `{p1['support_signature_303']}`; "
                f"p0 `{p0['support_signature_202']}` -> `{p0['support_signature_303']}`; "
                f"p2 `{p2['support_signature_202']}` -> `{p2['support_signature_303']}`."
            ),
        },
        {
            "diagnostic_family": "boundary_mass_transfer",
            "status": "boundary_mass_seed_conditioned_not_general",
            "note": (
                f"AUC for `w32_mean_boundary_per_mass` er {fmt(bm_202['auc_established_vs_no'])} paa seed 202 "
                f"men {fmt(bm_303['auc_established_vs_no'])} paa seed 303."
            ),
        },
        {
            "diagnostic_family": "static_support_audit",
            "status": "static_support_direction_not_general",
            "note": (
                f"`static_mean_support_degree` AUC endres fra {fmt(stat_202['auc_established_vs_no'])} "
                f"til {fmt(stat_303['auc_established_vs_no'])}; supportgeometri er viktig, men retningen er ikke universell."
            ),
        },
        {
            "diagnostic_family": "genealogy_audit",
            "status": "genealogy_intensity_descriptive_not_selector",
            "note": (
                f"`genealogy_intensity_index` er {fmt(gene_303['auc_established_vs_no'])} paa seed 303, "
                "men dette var ikke primary metric og maa ikke refittes til claim."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": "condition_on_base_support_before_more_dynamics",
            "note": (
                "Ikke bruk mer blind label-budget paa fast p1-anchor. Bygg forst en support-/base-kondisjonert "
                "selector eller billig pre-run audit som predikerer hvilke placements som er plausible paa gitt basegraf."
            ),
        },
    ]


def build_report(
    *,
    placement_rows: Sequence[Mapping[str, Any]],
    support_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15di: growth-seed signature synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en no-new-dynamics syntese av v15dg og v15dh.")
    lines.append("Den sammenligner placement-respons, support-signaturer og metric-retning mellom growth seed 202 og 303.")
    lines.append("Ingen metric er refittet, og ingen nye dynamiske runs er laget.")
    lines.append("")
    lines.append("## Placement summary")
    lines.append("")
    lines.append("| seed | p | labels | established | support | bm | static degree | genealogy | horizon |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placement_rows:
        lines.append(
            f"| {row['growth_seed']} | p{row['placement']} | {row['label_counts']} | "
            f"{fmt(row['established_rate'])} | `{row['support_signature_mode']}` | "
            f"{fmt(row['median_w32_mean_boundary_per_mass'])} | {fmt(row['median_static_mean_support_degree'])} | "
            f"{fmt(row['median_genealogy_intensity_index'])} | {fmt(row['median_high_horizon_span'])} |"
        )
    lines.append("")
    lines.append("## Growth-seed deltas")
    lines.append("")
    lines.append("| p | shift | support 202 | support 303 | est 202 | est 303 | bm delta | static degree delta | genealogy delta |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in support_rows:
        lines.append(
            f"| p{row['placement']} | {row['response_shift']} | `{row['support_signature_202']}` | "
            f"`{row['support_signature_303']}` | {fmt(row['established_rate_202'])} | "
            f"{fmt(row['established_rate_303'])} | {fmt(row['delta_boundary_mass_303_minus_202'])} | "
            f"{fmt(row['delta_static_support_degree_303_minus_202'])} | {fmt(row['delta_genealogy_intensity_303_minus_202'])} |"
        )
    lines.append("")
    lines.append("## Metric audit")
    lines.append("")
    lines.append("| scope | metric | role | AUC | median established | median no-horizon | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in metric_rows:
        if row["metric"] not in {"w32_mean_boundary_per_mass", "static_mean_support_degree", "genealogy_intensity_index"}:
            continue
        lines.append(
            f"| {row['scope']} | {row['metric']} | {row['role']} | {fmt(row['auc_established_vs_no'])} | "
            f"{fmt(row['median_established'])} | {fmt(row['median_no_horizon'])} | {row['status']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- v15dg sin positive boundary/mass-lesning var reell i seed-202-landskapet, men ikke growth-seed-general.")
    lines.append("- v15dh viser at p1 ikke er et universelt anker; p0/p2 kan bli de aktive plasseringene paa en annen base.")
    lines.append("- Neste arbeid bor kondisjonere paa base/support-signaturer foer mer dynamikk brukes.")
    lines.append("- Dette er fortsatt defect/response-instrumentering, ikke invariant-, Lorentz-, partikkel- eller entanglement-evidens.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15di", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke bruk `p1/1024` som generell anchor uten base/support-kondisjonering.")
    lines.append("- Ikke refit boundary/mass eller genealogy-intensity til et positivt claim.")
    lines.append("- Neste steg bor vaere en billig pre-run support/base-audit eller selector, ikke mer blind label-budget.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15di",
            "",
            "Denne runden brukte ingen nye simuleringer. Den sammenlignet to tidligere runder der startgrafen var bygget med ulike growth seeds.",
            "",
            "Hovedpoenget er enkelt: samme perturbasjon og samme placement-label gir ikke samme rolle naar startgrafen endres.",
            "",
            f"- Placement-lesning: `{diag['placement_transfer']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}`.",
            "",
            "Dette styrker ikke en paastand om en universell lov. Det sier at vi maa forstaa hvilke lokale/support-betingelser som gjor en placement plausibel foer vi kjorer mer dyr dynamikk.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15di growth-seed signature synthesis.")
    p.add_argument("--out-summary-md", default=str(DOC / "v15di_growth_seed_signature_synthesis.md"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15di_growth_seed_placement_summary.csv"))
    p.add_argument("--out-support-delta-csv", default=str(DOC / "v15di_growth_seed_support_delta.csv"))
    p.add_argument("--out-outcome-csv", default=str(DOC / "v15di_growth_seed_outcome_matrix.csv"))
    p.add_argument("--out-metric-csv", default=str(DOC / "v15di_growth_seed_metric_audit.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15di_growth_seed_diagnosis.csv"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15di_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15di.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = load_run_rows()
    target_rows = load_target_rows()
    placement_rows = placement_summary_rows(run_rows)
    support_rows = support_delta_rows(placement_rows)
    outcome_rows = outcome_matrix_rows(run_rows)
    metric_rows = metric_audit_rows(run_rows)
    diagnosis = diagnosis_rows(
        run_rows=run_rows,
        target_rows=target_rows,
        support_rows=support_rows,
        metric_rows=metric_rows,
    )

    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_support_delta_csv, support_rows)
    write_csv(args.out_outcome_csv, outcome_rows)
    write_csv(args.out_metric_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            placement_rows=placement_rows,
            support_rows=support_rows,
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
