#!/usr/bin/env python3
"""v0.15ct response fingerprint synthesis.

This is a no-new-dynamics synthesis round. It combines the p2/p0 scale ladder
from v15cn/v15cp/v15cq/v15cs and classifies each profile by response fingerprint
instead of by the old p0/p2 labels.

The point is to decide whether more label-budget is justified, or whether the
next dynamic lab should map response patterns across add_chord placements.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


INPUT_SOURCES = [
    {
        "lab": "v15cn",
        "seed_scope": "old_seed_deltas",
        "budget_scope": "same_absolute_2560",
        "path": Path("Documentation/v15cn_p2_horizon_scale_holdout_aggregate.csv"),
    },
    {
        "lab": "v15cp",
        "seed_scope": "old_seed_deltas",
        "budget_scope": "scaled_from_768",
        "path": Path("Documentation/v15cp_target1024_scaled_budget_aggregate.csv"),
    },
    {
        "lab": "v15cq",
        "seed_scope": "old_seed_deltas",
        "budget_scope": "scaled_from_768",
        "path": Path("Documentation/v15cq_intermediate_scale_aggregate.csv"),
    },
    {
        "lab": "v15cs",
        "seed_scope": "fresh_seed_deltas",
        "budget_scope": "scaled_from_768",
        "path": Path("Documentation/v15cs_add_chord_p0_scale_response_aggregate.csv"),
    },
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        value = float(x)
    except (TypeError, ValueError):
        return default
    return value if math.isfinite(value) else default


def mean_defined(values: Iterable[float]) -> float:
    vals = [x for x in values if math.isfinite(x)]
    return sum(vals) / len(vals) if vals else float("nan")


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


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


def response_strength_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["established_far_shell_rate"]) >= 0.50:
        score += 1
    if safe_float(row["mean_high_horizon_span"]) >= 32.0:
        score += 1
    if safe_float(row["mean_high_retention_rate"]) >= 0.35:
        score += 1
    if safe_float(row["mean_last12_high_rate"]) >= 0.50:
        score += 1
    if safe_float(row["mean_far_shell_share"]) >= 0.50:
        score += 1
    if safe_float(row["mean_weighted_mean_distance"]) >= 4.0:
        score += 1
    return score


def response_class(row: Mapping[str, Any]) -> str:
    established = safe_float(row["established_far_shell_rate"])
    horizon = safe_float(row["mean_high_horizon_span"])
    far_share = safe_float(row["mean_far_shell_share"])
    distance = safe_float(row["mean_weighted_mean_distance"])
    score = response_strength_score(row)
    if established >= 0.50 and horizon >= 64.0 and score >= 5:
        return "strong_persistent_far_shell"
    if established >= 0.50 and horizon >= 32.0:
        return "moderate_persistent_far_shell"
    if established == 0.0 and horizon == 0.0 and far_share >= 0.50 and distance >= 4.0:
        return "diffuse_far_mass_no_horizon"
    if established == 0.0 and horizon == 0.0:
        return "no_horizon"
    if horizon > 0.0:
        return "transient_or_partial_horizon"
    return "weak_or_unclassified"


def load_fingerprints() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for source in INPUT_SOURCES:
        if not source["path"].exists():
            raise FileNotFoundError(f"Missing fingerprint input: {source['path']}")
        for raw in read_csv(source["path"]):
            profile = str(raw["profile_label"])
            perturbation = str(raw["perturbation"])
            placement = int(float(raw["placement"]))
            target = int(float(raw["target_nodes"]))
            row: Dict[str, Any] = {
                "lab": source["lab"],
                "seed_scope": source["seed_scope"],
                "budget_scope": source["budget_scope"],
                "target_nodes": target,
                "profile_label": profile,
                "perturbation": perturbation,
                "placement": placement,
                "n_runs": int(float(raw["n_runs"])),
                "step_budget": int(float(raw.get("step_budget", 2560))),
                "established_far_shell_rate": safe_float(raw["established_far_shell_rate"]),
                "no_far_shell_rate": safe_float(raw["no_far_shell_rate"]),
                "mean_full_coarse_return_rate": safe_float(raw["mean_full_coarse_return_rate"]),
                "mean_high_horizon_span": safe_float(raw["mean_high_horizon_span"]),
                "mean_high_retention_rate": safe_float(raw["mean_high_retention_rate"]),
                "mean_last12_high_rate": safe_float(raw["mean_last12_high_rate"]),
                "mean_total_high_count": safe_float(raw["mean_total_high_count"]),
                "mean_longest_high_run": safe_float(raw["mean_longest_high_run"]),
                "mean_far_shell_share": safe_float(raw["mean_far_shell_share"]),
                "mean_q90_far_shell_share": safe_float(raw["mean_q90_far_shell_share"]),
                "mean_weighted_mean_distance": safe_float(raw["mean_weighted_mean_distance"]),
                "mean_abs_delta_spectral_radius_rel": safe_float(raw["mean_abs_delta_spectral_radius_rel"]),
            }
            row["response_strength_score"] = response_strength_score(row)
            row["response_class"] = response_class(row)
            rows.append(row)
    return rows


def class_summary_rows(fingerprints: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[int, str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in fingerprints:
        groups[(int(row["target_nodes"]), str(row["perturbation"]), str(row["profile_label"]))].append(row)
    out: List[Dict[str, Any]] = []
    for (target, perturbation, profile), rows in sorted(groups.items()):
        classes = Counter(str(row["response_class"]) for row in rows)
        out.append(
            {
                "target_nodes": target,
                "perturbation": perturbation,
                "profile_label": profile,
                "n_observations": len(rows),
                "labs": ";".join(str(row["lab"]) for row in rows),
                "seed_scopes": ";".join(sorted({str(row["seed_scope"]) for row in rows})),
                "response_classes": ";".join(f"{key}:{value}" for key, value in sorted(classes.items())),
                "dominant_response_class": classes.most_common(1)[0][0],
                "class_stable": int(len(classes) == 1),
                "mean_strength_score": mean_defined(safe_float(row["response_strength_score"]) for row in rows),
                "mean_established_rate": mean_defined(safe_float(row["established_far_shell_rate"]) for row in rows),
                "mean_horizon_span": mean_defined(safe_float(row["mean_high_horizon_span"]) for row in rows),
            }
        )
    return out


def seed_stability_rows(fingerprints: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    scaled = [
        row
        for row in fingerprints
        if str(row["budget_scope"]) == "scaled_from_768" and int(row["target_nodes"]) in (896, 1024)
    ]
    groups: Dict[Tuple[int, str], Dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in scaled:
        key = (int(row["target_nodes"]), str(row["profile_label"]))
        groups[key][str(row["seed_scope"])] = row
    out: List[Dict[str, Any]] = []
    for (target, profile), by_scope in sorted(groups.items()):
        if "old_seed_deltas" not in by_scope or "fresh_seed_deltas" not in by_scope:
            continue
        old = by_scope["old_seed_deltas"]
        fresh = by_scope["fresh_seed_deltas"]
        out.append(
            {
                "target_nodes": target,
                "profile_label": profile,
                "old_lab": old["lab"],
                "fresh_lab": fresh["lab"],
                "old_response_class": old["response_class"],
                "fresh_response_class": fresh["response_class"],
                "class_changed": int(str(old["response_class"]) != str(fresh["response_class"])),
                "old_strength_score": int(old["response_strength_score"]),
                "fresh_strength_score": int(fresh["response_strength_score"]),
                "strength_delta": int(fresh["response_strength_score"]) - int(old["response_strength_score"]),
                "old_established_rate": safe_float(old["established_far_shell_rate"]),
                "fresh_established_rate": safe_float(fresh["established_far_shell_rate"]),
                "established_delta": safe_float(fresh["established_far_shell_rate"]) - safe_float(old["established_far_shell_rate"]),
                "old_horizon_span": safe_float(old["mean_high_horizon_span"]),
                "fresh_horizon_span": safe_float(fresh["mean_high_horizon_span"]),
                "horizon_delta": safe_float(fresh["mean_high_horizon_span"]) - safe_float(old["mean_high_horizon_span"]),
            }
        )
    return out


def decision_rows(
    *,
    fingerprints: Sequence[Mapping[str, Any]],
    seed_stability: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    add_chord_rows = [row for row in fingerprints if str(row["perturbation"]) == "add_chord"]
    local_swap_rows = [row for row in fingerprints if str(row["perturbation"]) == "local_swap"]
    add_chord_strong = sum(1 for row in add_chord_rows if "persistent_far_shell" in str(row["response_class"]))
    local_swap_strong = sum(1 for row in local_swap_rows if "persistent_far_shell" in str(row["response_class"]))
    changed = sum(int(row["class_changed"]) for row in seed_stability)
    total = len(seed_stability)
    return [
        {
            "decision_axis": "p0_label_stability",
            "status": "not_stable",
            "evidence": "add_chord_p0 is strong at 896 on fresh seeds but collapses at 1024; old 1024 p0 did not replicate.",
            "decision": "do_not_continue_p0_as_scale_law",
        },
        {
            "decision_axis": "p2_label_stability",
            "status": "not_stable",
            "evidence": "add_chord_p2 is not target-768 supported, partial at 896, absent in old 1024, but active in fresh 1024.",
            "decision": "do_not_revive_p2_as_primary_scale_selector",
        },
        {
            "decision_axis": "carrier_level_signal",
            "status": "add_chord_placement_sensitive_live",
            "evidence": f"add_chord has {add_chord_strong} persistent-far-shell observations versus local_swap {local_swap_strong}, but placement/seed identity changes.",
            "decision": "map_add_chord_placements_before_more_label_claims",
        },
        {
            "decision_axis": "seed_stability",
            "status": "unstable",
            "evidence": f"{changed}/{total} old-vs-fresh scaled profile comparisons change response class.",
            "decision": "treat_label_specific_pockets_as_seed_sensitive",
        },
        {
            "decision_axis": "next_step",
            "status": "placement_response_map",
            "evidence": "Response fingerprints support add_chord carrier-level activity but not p0/p2 label stability.",
            "decision": "v15cu_add_chord_placement_response_map",
        },
    ]


def build_report(
    *,
    fingerprints: Sequence[Mapping[str, Any]],
    class_summary: Sequence[Mapping[str, Any]],
    seed_stability: Sequence[Mapping[str, Any]],
    decisions: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ct: response fingerprint synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen ny dynamikk. Den samler v15cn/v15cp/v15cq/v15cs og klassifiserer profile-respons etter fingerprint i stedet for p0/p2-label.")
    lines.append("")
    lines.append("## Response classes")
    lines.append("")
    lines.append("| class | meaning |")
    lines.append("| --- | --- |")
    lines.append("| strong_persistent_far_shell | established, long horizon, high retention/far-shell metrics |")
    lines.append("| moderate_persistent_far_shell | established with nontrivial horizon, but weaker than strong |")
    lines.append("| diffuse_far_mass_no_horizon | far mass/distance exists but no sustained horizon |")
    lines.append("| no_horizon | no established horizon and no far-mass class |")
    lines.append("| transient_or_partial_horizon | nonzero horizon without established response |")
    lines.append("")
    lines.append("## Fingerprint highlights")
    lines.append("")
    lines.append("| lab | target | profile | seed scope | class | score | established | horizon | distance |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in fingerprints:
        if str(row["response_class"]) in ("strong_persistent_far_shell", "moderate_persistent_far_shell"):
            lines.append(
                f"| {row['lab']} | {int(row['target_nodes'])} | {row['profile_label']} | {row['seed_scope']} | {row['response_class']} | {int(row['response_strength_score'])} | {fmt(row['established_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_weighted_mean_distance'])} |"
            )
    lines.append("")
    lines.append("## Seed stability")
    lines.append("")
    lines.append("| target | profile | old class | fresh class | changed | horizon delta |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in seed_stability:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['profile_label']} | {row['old_response_class']} | {row['fresh_response_class']} | {int(row['class_changed'])} | {fmt(row['horizon_delta'])} |"
        )
    lines.append("")
    lines.append("## Decisions")
    lines.append("")
    for row in decisions:
        lines.append(f"- `{row['decision_axis']}`: `{row['status']}` -> `{row['decision']}` fordi {row['evidence']}")
    lines.append("")
    lines.append("## Operativ tolkning")
    lines.append("")
    lines.append("- P0 er ikke stabil nok til aa behandles som scale-law-kandidat.")
    lines.append("- P2 skal ikke gjenopplives som primaer scale-selector.")
    lines.append("- Add_chord-carrieren er fortsatt live, men responsen er placement-/seed-sensitiv.")
    lines.append("- Neste dynamiske steg boer derfor mappe add_chord placements ved 896/1024, ikke bruke mer budsjett paa en enkelt p0/p2-label.")
    return "\n".join(lines) + "\n"


def build_operational_note(decisions: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15ct", ""]
    for row in decisions:
        lines.append(f"- `{row['decision_axis']}`: `{row['status']}` fordi {row['evidence']} Beslutning: `{row['decision']}`.")
    lines.append("")
    lines.append("- `next_step`: `v15cu_add_chord_placement_response_map` fordi response-fingerprints peker mot add_chord carrier-level aktivitet, men ikke stabil p0/p2-label.")
    lines.append("- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens.")
    return "\n".join(lines) + "\n"


def build_lay_note(decisions: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ct",
        "",
        "Denne runden bruker ingen nye simuleringer. Den samler de siste resultatene og sporer hva slags respons hver profil faktisk fikk.",
        "",
        "Hovedbildet er at hverken p0 eller p2 er stabile nok som navn paa en skalerende effekt. Men `add_chord` som type perturbasjon er fortsatt interessant: ved ulike storrelser og seeds dukker far-shell-respons opp i ulike placements.",
        "",
        "Neste gode steg er derfor ikke mer jakt paa akkurat p0 eller p2. Det er aa mappe flere add_chord-placements ved 896 og 1024 og la responsen selv vise hvor den ligger.",
        "",
        "Kort sagt: ikke label-foerst, respons-foerst.",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ct response fingerprint synthesis.")
    p.add_argument("--out-fingerprints-csv", type=str, default="Documentation/v15ct_response_fingerprints.csv")
    p.add_argument("--out-class-summary-csv", type=str, default="Documentation/v15ct_response_class_summary.csv")
    p.add_argument("--out-seed-stability-csv", type=str, default="Documentation/v15ct_response_seed_stability.csv")
    p.add_argument("--out-decisions-csv", type=str, default="Documentation/v15ct_response_decisions.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ct_response_fingerprint_synthesis.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ct_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ct.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    fingerprints = load_fingerprints()
    class_summary = class_summary_rows(fingerprints)
    seed_stability = seed_stability_rows(fingerprints)
    decisions = decision_rows(fingerprints=fingerprints, seed_stability=seed_stability)
    write_csv(args.out_fingerprints_csv, list(fingerprints))
    write_csv(args.out_class_summary_csv, class_summary)
    write_csv(args.out_seed_stability_csv, seed_stability)
    write_csv(args.out_decisions_csv, decisions)
    Path(args.out_summary_md).write_text(
        build_report(
            fingerprints=fingerprints,
            class_summary=class_summary,
            seed_stability=seed_stability,
            decisions=decisions,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(decisions), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(decisions), encoding="utf-8")


if __name__ == "__main__":
    main()
