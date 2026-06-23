#!/usr/bin/env python3
"""v0.15do active-set type discriminator synthesis.

No-new-dynamics synthesis after v15dn.

Goal:
- keep v15dn's active-set framing,
- ask whether the false positives in the best v15dn set screen can be explained
  by a small seed-level pre-run contrast,
- distinguish the two observed landscape types (`p1` vs `p0;p2`) without
  pretending that this tiny post-hoc screen is validated.

This script reuses v15dn's combined placement rows. It does not run defect
dynamics.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn


DOC = Path("Documentation")
OBSERVED_TYPES = {
    "p1_only": frozenset({1}),
    "p0_p2": frozenset({0, 2}),
}


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15dn.safe_float(x, default=default)


def safe_div(num: float, den: float) -> float:
    return v15dn.safe_div(num, den)


def fmt(x: Any, digits: int = 3) -> str:
    return v15dn.fmt(x, digits=digits)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dn.write_csv(path, rows)


def format_set(values: Iterable[int]) -> str:
    vals = sorted(values)
    return ";".join(f"p{x}" for x in vals) if vals else "none"


def actual_set_for_group(group: Sequence[Mapping[str, Any]]) -> frozenset[int]:
    return frozenset(
        int(row["placement"])
        for row in group
        if int(safe_float(row.get("active_placement"))) == 1
    )


def actual_type_for_set(active: frozenset[int]) -> str:
    for label, value in OBSERVED_TYPES.items():
        if active == value:
            return label
    return "other"


def predicted_set_for_type(label: str) -> frozenset[int]:
    return OBSERVED_TYPES.get(label, frozenset())


def metric_value(group: Sequence[Mapping[str, Any]], placement: int, metric: str) -> float:
    for row in group:
        if int(row["placement"]) == placement:
            return safe_float(row.get(metric))
    return float("nan")


def seed_feature_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for seed, group in v15dn.group_by_seed(rows).items():
        active = actual_set_for_group(group)
        row: Dict[str, Any] = {
            "growth_seed": seed,
            "actual_type": actual_type_for_set(active),
            "active_placements": format_set(active),
            "placement_rates": ";".join(
                f"p{int(r['placement'])}:{fmt(r.get('established_rate'))}"
                for r in sorted(group, key=lambda x: int(x["placement"]))
            ),
        }
        for metric in v15dn.MORPHOLOGY_METRICS:
            vals = {p: metric_value(group, p, metric) for p in (0, 1, 2)}
            if not any(math.isfinite(v) for v in vals.values()):
                continue
            row[f"{metric}_p0"] = vals[0]
            row[f"{metric}_p1"] = vals[1]
            row[f"{metric}_p2"] = vals[2]
            row[f"{metric}_p0_minus_p1"] = vals[0] - vals[1]
            row[f"{metric}_p2_minus_p1"] = vals[2] - vals[1]
            row[f"{metric}_p2_minus_p0"] = vals[2] - vals[0]
        out.append(row)
    return out


def score_predictions(
    seed_rows: Sequence[Mapping[str, Any]],
    predictions: Mapping[int, str],
) -> Dict[str, Any]:
    total_active = 0
    total_predicted = 0
    total_captured = 0
    total_false_positive = 0
    exact = 0
    type_hits = 0
    details: List[str] = []
    for row in seed_rows:
        seed = int(row["growth_seed"])
        actual_type = str(row["actual_type"])
        actual_set = set_from_label(str(row["active_placements"]))
        predicted_type = predictions.get(seed, "none")
        predicted_set = set(predicted_set_for_type(predicted_type))
        captured = actual_set & predicted_set
        false_positive = predicted_set - actual_set
        missed = actual_set - predicted_set
        total_active += len(actual_set)
        total_predicted += len(predicted_set)
        total_captured += len(captured)
        total_false_positive += len(false_positive)
        exact += int(actual_set == predicted_set)
        type_hits += int(actual_type == predicted_type)
        details.append(
            f"{seed}:pred={predicted_type}/{format_set(predicted_set)}"
            f" actual={actual_type}/{format_set(actual_set)}"
            f" miss={format_set(missed)} fp={format_set(false_positive)}"
        )
    seed_count = len(seed_rows)
    return {
        "seed_count": seed_count,
        "type_accuracy": safe_div(type_hits, seed_count),
        "exact_set_match_rate": safe_div(exact, seed_count),
        "coverage_fraction": safe_div(total_captured, total_active),
        "precision_fraction": safe_div(total_captured, total_predicted),
        "burden_fraction": safe_div(total_predicted, seed_count * 3),
        "mean_predicted_count": safe_div(total_predicted, seed_count),
        "total_active": total_active,
        "total_predicted": total_predicted,
        "total_captured": total_captured,
        "total_false_positive": total_false_positive,
        "seed_details": " | ".join(details),
    }


def set_from_label(label: str) -> set[int]:
    if label == "none" or not label:
        return set()
    out: set[int] = set()
    for part in label.split(";"):
        part = part.strip()
        if part.startswith("p"):
            out.add(int(part[1:]))
    return out


def comparison_rule_rows(seed_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    placements = (0, 1, 2)
    for metric in v15dn.MORPHOLOGY_METRICS:
        for left in placements:
            for right in placements:
                if left == right:
                    continue
                for op in ("lt", "le", "gt", "ge"):
                    for true_type in ("p1_only", "p0_p2"):
                        false_type = "p0_p2" if true_type == "p1_only" else "p1_only"
                        predictions: Dict[int, str] = {}
                        usable = True
                        for row in seed_rows:
                            seed = int(row["growth_seed"])
                            left_value = safe_float(row.get(f"{metric}_p{left}"))
                            right_value = safe_float(row.get(f"{metric}_p{right}"))
                            if not math.isfinite(left_value) or not math.isfinite(right_value):
                                usable = False
                                break
                            condition = compare(left_value, right_value, op)
                            predictions[seed] = true_type if condition else false_type
                        if not usable:
                            continue
                        score = score_predictions(seed_rows, predictions)
                        out.append(
                            {
                                "rule_family": "placement_comparison",
                                "metric": metric,
                                "feature_family": v15dn.feature_family(metric),
                                "comparison": f"p{left}_{op}_p{right}",
                                "true_type": true_type,
                                "false_type": false_type,
                                "rule_status": rule_status(score),
                                "posthoc_warning": "screened after seeing v15dn active-set labels; not validated",
                                **score,
                            }
                        )
    return sorted_rules(out)


def compare(left: float, right: float, op: str) -> bool:
    if op == "lt":
        return left < right
    if op == "le":
        return left <= right
    if op == "gt":
        return left > right
    if op == "ge":
        return left >= right
    raise ValueError(op)


def threshold_rule_rows(seed_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for metric in v15dn.MORPHOLOGY_METRICS:
        for diff_name in ("p0_minus_p1", "p2_minus_p1", "p2_minus_p0"):
            feature = f"{metric}_{diff_name}"
            values = [safe_float(row.get(feature)) for row in seed_rows]
            if not all(math.isfinite(v) for v in values):
                continue
            thresholds = midpoint_thresholds(values)
            for threshold in thresholds:
                for op in ("le", "gt"):
                    for true_type in ("p1_only", "p0_p2"):
                        false_type = "p0_p2" if true_type == "p1_only" else "p1_only"
                        predictions: Dict[int, str] = {}
                        for row in seed_rows:
                            seed = int(row["growth_seed"])
                            value = safe_float(row.get(feature))
                            condition = value <= threshold if op == "le" else value > threshold
                            predictions[seed] = true_type if condition else false_type
                        score = score_predictions(seed_rows, predictions)
                        out.append(
                            {
                                "rule_family": "seed_threshold",
                                "metric": metric,
                                "feature_family": v15dn.feature_family(metric),
                                "feature": feature,
                                "operator": op,
                                "threshold": threshold,
                                "true_type": true_type,
                                "false_type": false_type,
                                "rule_status": rule_status(score),
                                "posthoc_warning": "screened after seeing v15dn active-set labels; not validated",
                                **score,
                            }
                        )
    return sorted_rules(out)


def midpoint_thresholds(values: Sequence[float]) -> List[float]:
    unique = sorted(set(v for v in values if math.isfinite(v)))
    if len(unique) < 2:
        return []
    return [(a + b) / 2.0 for a, b in zip(unique, unique[1:])]


def rule_status(score: Mapping[str, Any]) -> str:
    exact = safe_float(score.get("exact_set_match_rate"))
    false_positive = safe_float(score.get("total_false_positive"))
    burden = safe_float(score.get("burden_fraction"))
    if exact == 1.0 and false_positive == 0.0 and burden < 1.0:
        return "posthoc_exact_compact_type_discriminator_not_validated"
    if exact >= 0.75 and burden < 1.0:
        return "posthoc_partial_type_discriminator_not_validated"
    return "not_type_discriminator_ready"


def sorted_rules(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        (dict(row) for row in rows),
        key=lambda r: (
            -safe_float(r.get("exact_set_match_rate")),
            -safe_float(r.get("coverage_fraction")),
            -safe_float(r.get("precision_fraction")),
            safe_float(r.get("burden_fraction")),
            safe_float(r.get("total_false_positive")),
            str(r.get("metric")),
            str(r.get("comparison", r.get("feature", ""))),
        ),
    )


def diagnosis_rows(
    comparison_rules: Sequence[Mapping[str, Any]],
    threshold_rules: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    exact_rules = [
        row for row in list(comparison_rules) + list(threshold_rules)
        if str(row.get("rule_status")) == "posthoc_exact_compact_type_discriminator_not_validated"
    ]
    best = exact_rules[0] if exact_rules else (comparison_rules[0] if comparison_rules else {})
    exact_metrics = sorted({str(row.get("metric")) for row in exact_rules})
    if len(exact_rules) > 1:
        status = "many_posthoc_exact_type_discriminators_found_underdetermined"
        next_step = "choose_one_pre_registered_guard_then_v15dp_two_seed_holdout"
        note = (
            f"Found {len(exact_rules)} exact compact rules across {len(exact_metrics)} metrics "
            f"({';'.join(exact_metrics)}). Best sorted rule is {best.get('metric')}/"
            f"{best.get('comparison', best.get('feature', ''))}, but the screen is underdetermined."
        )
    elif exact_rules:
        status = "single_posthoc_exact_type_discriminator_found_not_validated"
        next_step = "freeze_type_discriminator_for_v15dp_two_seed_holdout"
        note = (
            f"Best exact rule is {best.get('metric')}/"
            f"{best.get('comparison', best.get('feature', ''))}; "
            f"details: {best.get('seed_details', '')}."
        )
    else:
        status = "no_compact_type_discriminator_found"
        next_step = "do_not_run_holdout; design_new_pre_run_observable"
        note = "No exact compact type discriminator was found in existing pre-run morphology contrasts."
    return [
        {
            "diagnostic_family": "input_scope",
            "status": "no_new_dynamics_synthesis",
            "note": "Reads v15dn placement rows and derives seed-level pre-run contrasts only.",
        },
        {
            "diagnostic_family": "type_scope",
            "status": "observed_two_type_landscape_only",
            "note": "Only observed classes are p1_only and p0_p2 across four seeds; this is too small for validation.",
        },
        {
            "diagnostic_family": "multiplicity_guard",
            "status": "underdetermined" if len(exact_rules) > 1 else "single_or_none",
            "note": f"Exact compact rules={len(exact_rules)}; exact metrics={';'.join(exact_metrics)}.",
        },
        {
            "diagnostic_family": "type_discriminator_screen",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Do not claim a selector before a fresh pre-registered holdout over at least two new growth seeds.",
        },
    ]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str], limit: int | None = None) -> List[str]:
    clipped = list(rows[:limit] if limit is not None else rows)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in clipped:
        vals = []
        for field in fields:
            val = row.get(field, "")
            vals.append(fmt(val) if isinstance(val, float) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def build_report(
    seed_rows: Sequence[Mapping[str, Any]],
    comparison_rules: Sequence[Mapping[str, Any]],
    threshold_rules: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15do: active-set type discriminator synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en no-new-dynamics syntese etter v15dn.")
    lines.append("Den bruker v15dn sine placement-rader og lager seed-level pre-run kontraster for aa se om")
    lines.append("det finnes et lite signal som skiller `p1`-only seeds fra `p0;p2` seeds.")
    lines.append("Alle regler er post-hoc screens; ingen dynamikk er kjort her.")
    lines.append("")
    lines.append("## Seed features")
    lines.append("")
    lines.extend(
        table(
            seed_rows,
            (
                "growth_seed",
                "actual_type",
                "active_placements",
                "local_ball3_beta1_p0",
                "local_ball3_beta1_p1",
                "local_ball3_beta1_p2",
                "local_ball3_beta1_p2_minus_p1",
                "placement_rates",
            ),
        )
    )
    lines.append("")
    lines.append("## Best comparison rules")
    lines.append("")
    lines.extend(
        table(
            comparison_rules,
            (
                "metric",
                "comparison",
                "true_type",
                "false_type",
                "type_accuracy",
                "exact_set_match_rate",
                "coverage_fraction",
                "precision_fraction",
                "burden_fraction",
                "rule_status",
            ),
            limit=12,
        )
    )
    lines.append("")
    lines.append("## Best threshold rules")
    lines.append("")
    lines.extend(
        table(
            threshold_rules,
            (
                "metric",
                "feature",
                "operator",
                "threshold",
                "true_type",
                "false_type",
                "exact_set_match_rate",
                "precision_fraction",
                "burden_fraction",
                "rule_status",
            ),
            limit=12,
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
    lines.append("- v15do er en forklarings-/observabelrunde, ikke en selector-validering.")
    lines.append("- Hvis regelen brukes videre, maa den fryses noyaktig foer fresh growth-seed holdout.")
    lines.append("- Den interessante muligheten er at aktivt-sett-typen kan vaere mer stabil enn enkeltplacement-rankingen.")
    lines.append("- Dette er ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell geometri.")
    lines.append("")
    return "\n".join(lines)


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]], comparison_rules: Sequence[Mapping[str, Any]]) -> str:
    best = comparison_rules[0] if comparison_rules else {}
    lines = [
        "# Operativ anbefaling v0.15do",
        "",
        "## Kortversjon",
        "",
        "v15do fant flere post-hoc aktivt-sett-type-screens som kan forklare v15dn sine falske positive,",
        "men nettopp mangfoldet av perfekte regler viser at datasettet er underbestemt.",
        "Dette er en kandidatgenerator, ikke en selector.",
        "",
        "## Beste screen",
        "",
        f"- Regel: `{best.get('metric', '')}` / `{best.get('comparison', '')}` -> true=`{best.get('true_type', '')}`.",
        f"- Exact-set-match: `{fmt(best.get('exact_set_match_rate'))}`.",
        f"- Precision: `{fmt(best.get('precision_fraction'))}`.",
        f"- Burden: `{fmt(best.get('burden_fraction'))}`.",
        "",
        "## Neste steg",
        "",
        "- Hvis vi bruker dynamisk budsjett: velg og frys en enkel regel eksakt, og test paa minst to nye growth seeds.",
        "- Hvis vi vil vaere mer konservative: legg til en pre-run guard som begrunner valgt metrikfamilie, ikke bare en terskel.",
        "- Ikke refit terskler etter holdout; da mister runden verdi.",
        "",
        "## Diagnose",
        "",
    ]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}`.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-report", default=str(DOC / "v15do_active_set_type_discriminator_synthesis.md"))
    p.add_argument("--out-seed-features", default=str(DOC / "v15do_active_set_type_seed_features.csv"))
    p.add_argument("--out-comparison-rules", default=str(DOC / "v15do_active_set_type_comparison_rules.csv"))
    p.add_argument("--out-threshold-rules", default=str(DOC / "v15do_active_set_type_threshold_rules.csv"))
    p.add_argument("--out-diagnosis", default=str(DOC / "v15do_active_set_type_diagnosis.csv"))
    p.add_argument("--out-recommendation", default=str(DOC / "v0_15do_operativ_anbefaling.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placement_rows = v15dn.load_combined_rows()
    seed_rows = seed_feature_rows(placement_rows)
    comparison_rules = comparison_rule_rows(seed_rows)
    threshold_rules = threshold_rule_rows(seed_rows)
    diagnosis = diagnosis_rows(comparison_rules, threshold_rules)

    write_csv(Path(args.out_seed_features), seed_rows)
    write_csv(Path(args.out_comparison_rules), comparison_rules)
    write_csv(Path(args.out_threshold_rules), threshold_rules)
    write_csv(Path(args.out_diagnosis), diagnosis)
    Path(args.out_report).write_text(build_report(seed_rows, comparison_rules, threshold_rules, diagnosis))
    Path(args.out_recommendation).write_text(build_recommendation(diagnosis, comparison_rules))
    print(f"Wrote {args.out_report}")
    print(f"Wrote {args.out_comparison_rules}")
    print(f"Wrote {args.out_diagnosis}")


if __name__ == "__main__":
    main()
