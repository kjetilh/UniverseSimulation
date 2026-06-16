#!/usr/bin/env python3
"""v0.15dj support-conditioned pre-run audit.

No-new-dynamics audit of whether cheap base/support geometry can propose
plausible add_chord placements before spending more dynamic runtime.

Inputs:
- v15di growth-seed placement summary, itself synthesized from v15dg/v15dh.

Outputs:
- placement-level support features
- simple rule predictions by growth seed
- aggregate rule scores
- a skeptical diagnosis and short reports

This is not a validated selector. It is a scout for the next pre-registered
fresh growth-seed holdout.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


DOC = Path("Documentation")
INPUT_PLACEMENT_SUMMARY = DOC / "v15di_growth_seed_placement_summary.csv"

PLACEMENT_FEATURES = DOC / "v15dj_support_conditioned_placement_features.csv"
RULE_PREDICTIONS = DOC / "v15dj_support_conditioned_rule_predictions.csv"
RULE_SCORES = DOC / "v15dj_support_conditioned_rule_scores.csv"
DIAGNOSIS = DOC / "v15dj_support_conditioned_diagnosis.csv"
REPORT = DOC / "v15dj_support_conditioned_pre_run_audit.md"
RECOMMENDATION = DOC / "v0_15dj_operativ_anbefaling.md"
NON_SPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dj.md"

ACTIVE_ESTABLISHED_RATE = 0.50

BASE_FEATURES = (
    "static_mean_support_degree",
    "static_support_ball_1",
    "static_support_ball_2",
    "static_support_ball_3",
    "static_support_boundary_to_volume",
    "static_support_pairwise_mean_distance",
)

DERIVED_FEATURES = (
    "ball1_over_ball3",
    "ball2_over_ball3",
    "ball3_over_ball1",
    "ball3_over_ball2",
    "ball2_minus_ball1",
    "ball3_minus_ball1",
    "ball3_minus_ball2",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_support_signature(sig: str) -> List[int]:
    out: List[int] = []
    for part in str(sig).split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(int(part))
        except ValueError:
            continue
    return out


def parse_label_counts(raw: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for item in str(raw).split(";"):
        if not item or ":" not in item:
            continue
        key, val = item.rsplit(":", 1)
        try:
            out[key] = int(val)
        except ValueError:
            out[key] = 0
    return out


def placement_feature_rows(rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        support = parse_support_signature(row.get("support_signature_mode", ""))
        ball1 = safe_float(row.get("median_static_support_ball_1"))
        ball2 = safe_float(row.get("median_static_support_ball_2"))
        ball3 = safe_float(row.get("median_static_support_ball_3"))
        established_rate = safe_float(row.get("established_rate"))
        label_counts = parse_label_counts(row.get("label_counts", ""))
        active = int(established_rate >= ACTIVE_ESTABLISHED_RATE)
        feature_row: Dict[str, Any] = {
            "growth_seed": int(safe_float(row["growth_seed"])),
            "placement": int(safe_float(row["placement"])),
            "n_runs": int(safe_float(row["n_runs"])),
            "support_signature": row.get("support_signature_mode", ""),
            "support_node_count": len(support),
            "established_rate": established_rate,
            "active_placement": active,
            "label_counts": row.get("label_counts", ""),
            "established_count": label_counts.get("established_far_shell_horizon", 0),
            "mixed_count": label_counts.get("mixed_far_shell_horizon", 0),
            "no_horizon_count": label_counts.get("no_far_shell_horizon", 0),
            "static_mean_support_degree": safe_float(row.get("median_static_mean_support_degree")),
            "static_support_ball_1": ball1,
            "static_support_ball_2": ball2,
            "static_support_ball_3": ball3,
            "static_support_boundary_to_volume": safe_float(row.get("median_static_support_boundary_to_volume")),
            "static_support_pairwise_mean_distance": safe_float(row.get("median_static_support_pairwise_mean_distance")),
            "ball1_over_ball3": safe_div(ball1, ball3),
            "ball2_over_ball3": safe_div(ball2, ball3),
            "ball3_over_ball1": safe_div(ball3, ball1),
            "ball3_over_ball2": safe_div(ball3, ball2),
            "ball2_minus_ball1": ball2 - ball1 if math.isfinite(ball2) and math.isfinite(ball1) else float("nan"),
            "ball3_minus_ball1": ball3 - ball1 if math.isfinite(ball3) and math.isfinite(ball1) else float("nan"),
            "ball3_minus_ball2": ball3 - ball2 if math.isfinite(ball3) and math.isfinite(ball2) else float("nan"),
        }
        out.append(feature_row)
    return sorted(out, key=lambda x: (x["growth_seed"], x["placement"]))


def seed_groups(rows: Sequence[Mapping[str, Any]]) -> Dict[int, List[Mapping[str, Any]]]:
    grouped: Dict[int, List[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(int(row["growth_seed"]), []).append(row)
    for key in grouped:
        grouped[key] = sorted(grouped[key], key=lambda x: int(x["placement"]))
    return grouped


def rank_rows(rows: Sequence[Mapping[str, Any]], metric: str, direction: str) -> List[Mapping[str, Any]]:
    reverse = direction == "high"
    return sorted(
        rows,
        key=lambda x: (
            -safe_float(x.get(metric)) if reverse else safe_float(x.get(metric)),
            int(x["placement"]),
        ),
    )


def as_placement_list(rows: Iterable[Mapping[str, Any]]) -> str:
    return ";".join(f"p{int(row['placement'])}" for row in rows)


def prediction_rows(feature_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    metrics = list(BASE_FEATURES) + list(DERIVED_FEATURES)
    grouped = seed_groups(feature_rows)
    out: List[Dict[str, Any]] = []
    for metric in metrics:
        for direction in ("low", "high"):
            rule = f"{direction}_{metric}"
            for growth_seed, rows in sorted(grouped.items()):
                ranked = rank_rows(rows, metric, direction)
                top1 = ranked[:1]
                top2 = ranked[:2]
                active_rows = [row for row in rows if int(row["active_placement"]) == 1]
                active_placements = {int(row["placement"]) for row in active_rows}
                top1_placements = {int(row["placement"]) for row in top1}
                top2_placements = {int(row["placement"]) for row in top2}
                active_count = len(active_placements)
                top1_capture = len(active_placements & top1_placements)
                top2_capture = len(active_placements & top2_placements)
                out.append(
                    {
                        "rule": rule,
                        "metric": metric,
                        "direction": direction,
                        "growth_seed": growth_seed,
                        "active_threshold_established_rate": ACTIVE_ESTABLISHED_RATE,
                        "active_placements": as_placement_list(active_rows),
                        "active_count": active_count,
                        "ranked_placements": as_placement_list(ranked),
                        "top1_placements": as_placement_list(top1),
                        "top2_placements": as_placement_list(top2),
                        "top1_hit": int(top1_capture > 0),
                        "top2_hit": int(top2_capture > 0),
                        "top1_capture_count": top1_capture,
                        "top2_capture_count": top2_capture,
                        "top1_capture_fraction": safe_div(top1_capture, active_count),
                        "top2_capture_fraction": safe_div(top2_capture, active_count),
                        "top1_inactive_selected": len(top1_placements - active_placements),
                        "top2_inactive_selected": len(top2_placements - active_placements),
                        "top1_metric_value": safe_float(top1[0].get(metric)) if top1 else float("nan"),
                        "top2_metric_values": ";".join(fmt(row.get(metric)) for row in top2),
                    }
                )
    return out


def mean(values: Iterable[float]) -> float:
    vals = [safe_float(x) for x in values]
    vals = [x for x in vals if math.isfinite(x)]
    return sum(vals) / len(vals) if vals else float("nan")


def rule_status(row: Mapping[str, Any]) -> str:
    top1_hit_rate = safe_float(row["growth_seed_hit_rate_top1"])
    top2_hit_rate = safe_float(row["growth_seed_hit_rate_top2"])
    capture_top1 = safe_float(row["total_active_capture_fraction_top1"])
    capture_top2 = safe_float(row["total_active_capture_fraction_top2"])
    if top1_hit_rate == 1.0 and capture_top1 == 1.0:
        return "candidate_full_capture_tiny_n"
    if top1_hit_rate == 1.0:
        return "scout_candidate_top1_hits_each_seed_but_incomplete"
    if top2_hit_rate == 1.0 and capture_top2 >= 0.50:
        return "weak_broad_scout_candidate"
    return "not_supported_as_scout_rule"


def score_rows(predictions: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = {}
    for row in predictions:
        grouped.setdefault(str(row["rule"]), []).append(row)
    out: List[Dict[str, Any]] = []
    for rule, rows in sorted(grouped.items()):
        active_total = sum(int(row["active_count"]) for row in rows)
        top1_capture_total = sum(int(row["top1_capture_count"]) for row in rows)
        top2_capture_total = sum(int(row["top2_capture_count"]) for row in rows)
        row = {
            "rule": rule,
            "metric": rows[0]["metric"],
            "direction": rows[0]["direction"],
            "n_growth_seeds": len(rows),
            "active_total": active_total,
            "growth_seed_hit_rate_top1": mean(safe_float(row["top1_hit"]) for row in rows),
            "growth_seed_hit_rate_top2": mean(safe_float(row["top2_hit"]) for row in rows),
            "mean_capture_fraction_top1": mean(safe_float(row["top1_capture_fraction"]) for row in rows),
            "mean_capture_fraction_top2": mean(safe_float(row["top2_capture_fraction"]) for row in rows),
            "total_active_capture_fraction_top1": safe_div(top1_capture_total, active_total),
            "total_active_capture_fraction_top2": safe_div(top2_capture_total, active_total),
            "inactive_selected_top1_total": sum(int(row["top1_inactive_selected"]) for row in rows),
            "inactive_selected_top2_total": sum(int(row["top2_inactive_selected"]) for row in rows),
        }
        row["status"] = rule_status(row)
        out.append(row)
    return sorted(
        out,
        key=lambda x: (
            -safe_float(x["growth_seed_hit_rate_top1"]),
            -safe_float(x["total_active_capture_fraction_top1"]),
            safe_float(x["inactive_selected_top1_total"]),
            -safe_float(x["growth_seed_hit_rate_top2"]),
            str(x["rule"]),
        ),
    )


def diagnosis_rows(scores: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    best = scores[0] if scores else {}
    scout_rules = [
        str(row["rule"])
        for row in scores
        if str(row.get("status")) == "scout_candidate_top1_hits_each_seed_but_incomplete"
    ]
    broad_rules = [
        str(row["rule"])
        for row in scores
        if str(row.get("status")) in {"scout_candidate_top1_hits_each_seed_but_incomplete", "weak_broad_scout_candidate"}
    ]
    return [
        {
            "key": "artifact_scope",
            "value": "no_new_dynamics",
            "evidence": f"read {INPUT_PLACEMENT_SUMMARY}",
        },
        {
            "key": "active_definition",
            "value": f"established_rate_ge_{fmt(ACTIVE_ESTABLISHED_RATE, 2)}",
            "evidence": "active placements are label-derived only for evaluating pre-run support rules",
        },
        {
            "key": "best_scout_rule",
            "value": str(best.get("rule", "")),
            "evidence": (
                f"top1_hit_rate={fmt(best.get('growth_seed_hit_rate_top1'))}; "
                f"total_capture_top1={fmt(best.get('total_active_capture_fraction_top1'))}; "
                f"status={best.get('status', '')}"
            ),
        },
        {
            "key": "scout_candidate",
            "value": "found_sparse_candidate" if scout_rules else "not_found",
            "evidence": ";".join(scout_rules[:8]) if scout_rules else "no rule hit top1 on every available growth seed",
        },
        {
            "key": "selector_validation",
            "value": "not_validated",
            "evidence": "only two growth seeds and six placement summaries; at least one active placement remains missed by top1 scout rules",
        },
        {
            "key": "static_direction",
            "value": "not_universal",
            "evidence": "v15di already showed static degree direction changed across growth seeds; v15dj only ranks cheap base support features",
        },
        {
            "key": "next_step",
            "value": "pre_register_low_local_support_volume_holdout",
            "evidence": (
                "run fresh growth seed with support-only ranking before dynamics; test top1/top2 scout placements plus a contrast"
                if broad_rules
                else "need one more cheap support audit before any dynamic holdout"
            ),
        },
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> str:
    if not rows:
        return ""
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        parts = []
        for field in fields:
            val = row.get(field, "")
            if isinstance(val, float):
                parts.append(fmt(val))
            else:
                parts.append(str(val))
        lines.append("| " + " | ".join(parts) + " |")
    return "\n".join(lines)


def write_reports(
    features: Sequence[Mapping[str, Any]],
    predictions: Sequence[Mapping[str, Any]],
    scores: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> None:
    best_scores = list(scores[:8])
    active_features = [row for row in features if int(row["active_placement"]) == 1]
    best_rule = str(scores[0]["rule"]) if scores else ""
    best_predictions = [row for row in predictions if str(row["rule"]) == best_rule]

    REPORT.write_text(
        "\n".join(
            [
                "# Relasjonell universgraf v0.15dj: support-conditioned pre-run audit",
                "",
                "## Formal",
                "",
                "`v15dj` er en no-new-dynamics audit. Den leser `v15di_growth_seed_placement_summary.csv` og tester om billige support-/base-features kan rangere plausible `1024/add_chord` placements foer mer dynamikk brukes.",
                "",
                "Dette er ikke en validert selector. Det er en scout for neste pre-registrerte fresh growth-seed holdout.",
                "",
                "## Active placements used only for audit scoring",
                "",
                markdown_table(
                    active_features,
                    (
                        "growth_seed",
                        "placement",
                        "support_signature",
                        "established_rate",
                        "static_support_ball_1",
                        "static_support_ball_2",
                        "static_support_ball_3",
                        "static_mean_support_degree",
                    ),
                ),
                "",
                "## Best simple support rules",
                "",
                markdown_table(
                    best_scores,
                    (
                        "rule",
                        "growth_seed_hit_rate_top1",
                        "total_active_capture_fraction_top1",
                        "growth_seed_hit_rate_top2",
                        "total_active_capture_fraction_top2",
                        "inactive_selected_top1_total",
                        "status",
                    ),
                ),
                "",
                "## Best-rule per-seed predictions",
                "",
                markdown_table(
                    best_predictions,
                    (
                        "growth_seed",
                        "active_placements",
                        "ranked_placements",
                        "top1_placements",
                        "top2_placements",
                        "top1_hit",
                        "top2_hit",
                        "top1_capture_fraction",
                        "top2_capture_fraction",
                    ),
                ),
                "",
                "## Diagnosis",
                "",
                markdown_table(diagnosis, ("key", "value", "evidence")),
                "",
                "## Interpretation",
                "",
                "- En liten klasse av `low local support volume/gap`-regler treffer minst en aktiv placement i begge tilgjengelige growth seeds.",
                "- Regelen er ikke nok til aa velge alle aktive placements: growth seed 303 har baade p0 og p2 aktive, mens low-volume-reglene typisk peker paa p2.",
                "- Dette er dermed en nyttig pre-run prior, ikke en universell supportlov og ikke en dynamisk forklaring.",
                "- Neste riktige dynamiske steg er aa pre-registrere support-rankingen paa en fresh growth seed foer runtime brukes, og saa teste top1/top2 pluss en kontrast.",
                "",
                "## Files",
                "",
                "- `relational_universe_v15dj_support_conditioned_pre_run_audit.py`",
                "- `Documentation/v15dj_support_conditioned_placement_features.csv`",
                "- `Documentation/v15dj_support_conditioned_rule_predictions.csv`",
                "- `Documentation/v15dj_support_conditioned_rule_scores.csv`",
                "- `Documentation/v15dj_support_conditioned_diagnosis.csv`",
                "- `Documentation/v0_15dj_operativ_anbefaling.md`",
                "- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dj.md`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    RECOMMENDATION.write_text(
        "\n".join(
            [
                "# Operativ anbefaling v0.15dj",
                "",
                "- `artifact_scope`: `no_new_dynamics`; v15dj bruker eksisterende v15di-sammendrag og lager ingen nye simulasjonsresultater.",
                "- `best_scout_rule`: se `v15dj_support_conditioned_rule_scores.csv`; beste enkle regler er low local support volume/gap-regler.",
                "- `selector_status`: `not_validated`; bare to growth seeds og seks placement-sammendrag er for lite, og scout-reglene fanger ikke alle aktive placements.",
                "- `interpretation`: supportgeometri ser relevant ut som pre-run prior, men retningen er ikke en universell lov.",
                "- `next_step`: pre-registrer en fresh growth-seed dynamisk holdout der placements velges av support-rangering foer dynamikken kjores: top1, top2 og en kontrast.",
                "",
                "- Ikke gjenoppliv fixed `p1/1024` som generell anchor.",
                "- Ikke bruk label-frekvensene til aa refitte en selector uten fresh holdout.",
                "- Ikke oppgrader dette til invariant-, Lorentz-, entanglement-, partikkel- eller universell-geometri-evidens.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    NON_SPECIALIST.write_text(
        "\n".join(
            [
                "# v0.15dj forklart for ikke-spesialister",
                "",
                "Vi har sett at samme type forstyrrelse (`add_chord`) kan gi langtrekkende respons, men hvilken plassering som virker flytter seg naar basegrafen byttes.",
                "",
                "`v15dj` bruker derfor ikke mer simulasjonstid. I stedet spoer den: kan vi se paa den lokale geometrien rundt en mulig plassering foer vi kjorer dynamikken, og bruke det til aa velge bedre kandidater?",
                "",
                "Det forelopige svaret er: kanskje, men bare som en svak prior. Regler som velger plasseringer med lav lokal support-volume treffer minst en aktiv plassering i begge basegrafene vi har. Men datasettet er lite, og regelen bommer paa noe av den positive strukturen.",
                "",
                "Neste steg er derfor ikke aa paastaa at vi har funnet en regel. Neste steg er aa la denne billige regelen velge kandidater paa en ny basegraf foer vi kjorer dynamikk, og se om den faktisk hjelper der.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run() -> None:
    input_rows = read_csv(INPUT_PLACEMENT_SUMMARY)
    features = placement_feature_rows(input_rows)
    predictions = prediction_rows(features)
    scores = score_rows(predictions)
    diagnosis = diagnosis_rows(scores)

    write_csv(PLACEMENT_FEATURES, features)
    write_csv(RULE_PREDICTIONS, predictions)
    write_csv(RULE_SCORES, scores)
    write_csv(DIAGNOSIS, diagnosis)
    write_reports(features, predictions, scores, diagnosis)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    run()


if __name__ == "__main__":
    main()
