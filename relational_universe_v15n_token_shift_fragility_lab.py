#!/usr/bin/env python3
"""v0.15n token_shift fragility lab.

This round is the next narrow step after v15m. It does not try to rescue a
clean survival/extinction story. Instead it asks a smaller question:

is the partial `token_shift` fragility signal structured by local support
geometry, with `add_chord` retained as an alive control family on the same
bases and placement indices?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15m_single_defect_survival_lab as v15m


TARGETS = (48, 96)
GROWTH_SEEDS = (101, 202)
PLACEMENTS = tuple(range(12))
PERTURBATIONS = ("token_shift", "add_chord")
STEPS = 960
LOG_EVERY = 8
FEATURES = (
    "mean_support_degree",
    "support_ball_2",
    "support_ball_3",
    "support_shell_2",
    "shell2_over_shell1",
    "ball3_over_ball1",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def run_rows(
    *,
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for ens in ensembles:
        target = int(ens.target_nodes)
        if target not in TARGETS:
            continue
        for growth_seed in GROWTH_SEEDS:
            base = base_states[(ens.name, int(growth_seed))]
            token_count = max(1, len(base.sorted_token_ids()))
            max_placement = min(len(PLACEMENTS), token_count)
            for perturbation in PERTURBATIONS:
                for placement in PLACEMENTS[:max_placement]:
                    run_seed = (
                        target * 100000
                        + int(growth_seed) * 1000
                        + int(placement)
                        + (0 if perturbation == "token_shift" else 50000000)
                    )
                    res = v15.run_defect_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=STEPS,
                        perturbation=perturbation,
                        center_token_index=int(placement),
                        local_coupling="maximal",
                        log_every=LOG_EVERY,
                    )
                    info = dict(res["perturbation_info"])
                    actual = str(info.get("type", "unknown"))
                    requested_match = 1 if v15.v14.perturbation_requested_match(perturbation, actual) else 0
                    support = list(info.get("support", []))
                    geom = v14c.support_geometry_features(base, support)

                    log_rows = list(res["log_rows"])
                    tail_rows = log_rows[max(0, int(math.floor(0.75 * len(log_rows)))) :]
                    tail_change_count = sum(
                        1
                        for a, b in zip(tail_rows, tail_rows[1:])
                        if int(a["damage_component_count"]) != int(b["damage_component_count"])
                        or int(a["alive"]) != int(b["alive"])
                    )
                    tail_dual_fraction = mean_defined(
                        1.0 if int(row["damage_component_count"]) >= 2 else 0.0
                        for row in tail_rows
                    )
                    tail_mean_component_count = mean_defined(
                        safe_float(row["damage_component_count"]) for row in tail_rows
                    )
                    tail_mean_radius = mean_defined(
                        safe_float(row["radius_control"])
                        for row in tail_rows
                        if safe_float(row["radius_control"]) >= 0
                    )

                    summary = dict(res["summary"])
                    tail_label = v15m.classify_single_tail(
                        final_alive=int(summary["final_alive"]),
                        first_zero_step=safe_float(summary["first_zero_step"]),
                        last_alive_fraction=safe_float(summary["last_alive_fraction"]),
                        tail_dual_fraction=safe_float(tail_dual_fraction),
                        tail_mean_component_count=safe_float(tail_mean_component_count),
                        tail_mean_radius=safe_float(tail_mean_radius),
                        tail_change_count=int(tail_change_count),
                        steps=STEPS,
                    )
                    fragility_label = (
                        "extinct"
                        if tail_label in {"extinction", "late_extinction"}
                        else "alive_tail"
                    )
                    rows.append(
                        {
                            "target_nodes": target,
                            "growth_seed": int(growth_seed),
                            "placement": int(placement),
                            "run_seed": int(run_seed),
                            "requested_perturbation": perturbation,
                            "actual_perturbation": actual,
                            "requested_match": int(requested_match),
                            "support_size": len(support),
                            "support_signature": ",".join(str(x) for x in support),
                            "final_alive": int(summary["final_alive"]),
                            "first_zero_step": safe_float(summary["first_zero_step"]),
                            "last_alive_fraction": safe_float(summary["last_alive_fraction"]),
                            "mean_radius_control": safe_float(summary["mean_radius_control"]),
                            "mean_component_count": safe_float(summary["mean_component_count"]),
                            "outcome_class": str(summary["outcome_class"]),
                            "tail_dual_fraction": safe_float(tail_dual_fraction),
                            "tail_mean_component_count": safe_float(tail_mean_component_count),
                            "tail_mean_radius": safe_float(tail_mean_radius),
                            "tail_change_count": int(tail_change_count),
                            "tail_label": tail_label,
                            "fragility_label": fragility_label,
                            **geom,
                        }
                    )
    return rows


def aggregate_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        grouped.setdefault((str(row["requested_perturbation"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (perturbation, target_nodes), rows in sorted(grouped.items()):
        tail_counts: Dict[str, int] = {}
        for row in rows:
            tail_counts[str(row["tail_label"])] = tail_counts.get(str(row["tail_label"]), 0) + 1
        dominant = max(tail_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        out.append(
            {
                "requested_perturbation": perturbation,
                "target_nodes": int(target_nodes),
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "extinction_rate": mean_defined(1.0 if str(r["fragility_label"]) == "extinct" else 0.0 for r in rows),
                "persistent_split_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "persistent_split_tail" else 0.0 for r in rows),
                "persistent_diffuse_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "persistent_diffuse_tail" else 0.0 for r in rows),
                "quiet_singleton_tail_rate": mean_defined(1.0 if str(r["tail_label"]) == "quiet_singleton_tail" else 0.0 for r in rows),
                "mean_support_ball_3": mean_defined(safe_float(r["support_ball_3"]) for r in rows),
                "mean_support_degree": mean_defined(safe_float(r["mean_support_degree"]) for r in rows),
                "mean_tail_radius": mean_defined(safe_float(r["tail_mean_radius"]) for r in rows),
                "dominant_tail_label": dominant,
            }
        )
    return out


def feature_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    token_rows = [
        dict(r)
        for r in run_rows
        if str(r["requested_perturbation"]) == "token_shift" and int(r["requested_match"]) == 1
    ]
    extinct = [r for r in token_rows if str(r["fragility_label"]) == "extinct"]
    alive = [r for r in token_rows if str(r["fragility_label"]) == "alive_tail"]
    out: List[Dict[str, Any]] = []
    for feature in FEATURES:
        extinct_vals = [safe_float(r[feature]) for r in extinct]
        alive_vals = [safe_float(r[feature]) for r in alive]
        out.append(
            {
                "feature_name": feature,
                "n_token_extinct": len(extinct_vals),
                "n_token_alive": len(alive_vals),
                "mean_token_extinct": mean_defined(extinct_vals),
                "mean_token_alive": mean_defined(alive_vals),
                "delta_extinct_minus_alive": mean_defined(extinct_vals) - mean_defined(alive_vals),
                "q10_token_alive": quantile(alive_vals, 0.10) if alive_vals else float("nan"),
                "q90_token_alive": quantile(alive_vals, 0.90) if alive_vals else float("nan"),
            }
        )
    return out


def placement_contrast_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    keyed: Dict[Tuple[int, int, int, str], Dict[str, Any]] = {}
    for row in run_rows:
        keyed[(int(row["target_nodes"]), int(row["growth_seed"]), int(row["placement"]), str(row["requested_perturbation"]))] = dict(row)
    out: List[Dict[str, Any]] = []
    keys = sorted({(k[0], k[1], k[2]) for k in keyed})
    for target_nodes, growth_seed, placement in keys:
        token = keyed.get((target_nodes, growth_seed, placement, "token_shift"))
        chord = keyed.get((target_nodes, growth_seed, placement, "add_chord"))
        if token is None or chord is None:
            continue
        out.append(
            {
                "target_nodes": int(target_nodes),
                "growth_seed": int(growth_seed),
                "placement": int(placement),
                "token_requested_match": int(token["requested_match"]),
                "add_requested_match": int(chord["requested_match"]),
                "token_fragility_label": str(token["fragility_label"]),
                "add_fragility_label": str(chord["fragility_label"]),
                "token_tail_label": str(token["tail_label"]),
                "add_tail_label": str(chord["tail_label"]),
                "token_support_ball_3": safe_float(token["support_ball_3"]),
                "add_support_ball_3": safe_float(chord["support_ball_3"]),
                "token_mean_support_degree": safe_float(token["mean_support_degree"]),
                "add_mean_support_degree": safe_float(chord["mean_support_degree"]),
                "token_extinct_add_alive": 1
                if str(token["fragility_label"]) == "extinct" and str(chord["fragility_label"]) == "alive_tail"
                else 0,
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
    feature_summary: Sequence[Dict[str, Any]],
    placement_contrast: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((safe_float(row["strict_match_rate"]) for row in aggregate), default=0.0) >= 0.999
    token_ext = max(
        (
            safe_float(row["extinction_rate"])
            for row in aggregate
            if str(row["requested_perturbation"]) == "token_shift"
        ),
        default=0.0,
    )
    add_ext = max(
        (
            safe_float(row["extinction_rate"])
            for row in aggregate
            if str(row["requested_perturbation"]) == "add_chord"
        ),
        default=0.0,
    )
    contrast_hits = sum(int(row["token_extinct_add_alive"]) for row in placement_contrast)
    ball3_row = next((row for row in feature_summary if str(row["feature_name"]) == "support_ball_3"), None)
    degree_row = next((row for row in feature_summary if str(row["feature_name"]) == "mean_support_degree"), None)
    ball3_delta = safe_float(ball3_row["delta_extinct_minus_alive"]) if ball3_row else float("nan")
    degree_delta = safe_float(degree_row["delta_extinct_minus_alive"]) if degree_row else float("nan")

    rows = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle testede perturbasjoner matcher ønsket type."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        }
    ]
    if token_ext >= 0.10 and add_ext <= 0.05 and contrast_hits >= 2:
        if (math.isfinite(ball3_delta) and abs(ball3_delta) >= 1.0) or (
            math.isfinite(degree_delta) and abs(degree_delta) >= 0.5
        ):
            status = "placement_structured_fragility"
            note = (
                "Token_shift-extinctionen ser delvis plassering-/støttestruert ut, med lokale støttefeatures som skiller extinct fra levende runs bedre enn i v15m alene."
            )
            next_status = "follow_fragility_geometry"
            next_note = "Neste steg bør være en enda smalere token_shift-runde rundt de mest skjøre støtteprofilene, ikke brede survival-paastander."
        else:
            status = "fragility_signal_without_clean_geometry"
            note = (
                "Token_shift er fortsatt skjørere enn add_chord, men de enkle støttefeature-ene skiller ikke extinct fra levende runs rent nok."
            )
            next_status = "avoid_geometry_claims"
            next_note = "Neste steg bør bruke andre defect-observabler enn bare enkel støttegeometri, eller bytte defect-spørsmål igjen."
        rows.append(
            {
                "diagnostic_family": "fragility_signal",
                "status": status,
                "note": note,
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": next_status,
                "note": next_note,
            }
        )
    else:
        rows.append(
            {
                "diagnostic_family": "fragility_signal",
                "status": "not_clean",
                "note": "Token_shift er fortsatt ikke klart nok separert fra add_chord til å bære et robust fragility-spor alene.",
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": "pivot_again",
                "note": "Neste steg bør være et annet smalt defect-spørsmål, ikke mer survival-/fragility-claiming langs samme akse.",
            }
        )
    return rows


def build_report(
    *,
    target_summary: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
    feature_summary: Sequence[Dict[str, Any]],
    placement_contrast: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15n: token_shift fragility lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester ikke om `token_shift` har en stor egen survival-lov. Den spør mer presist om den delvise skjørheten i `v15m` følger lokal støttegeometri, med `add_chord` som levende kontroll."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregate fragility")
    lines.append("")
    lines.append("| perturbation | target | extinction | split tail | diffuse tail | quiet tail | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['requested_perturbation']} | {int(row['target_nodes'])} | {fmt(row['extinction_rate'])} | {fmt(row['persistent_split_tail_rate'])} | {fmt(row['persistent_diffuse_tail_rate'])} | {fmt(row['quiet_singleton_tail_rate'])} | {row['dominant_tail_label']} |"
        )
    lines.append("")
    lines.append("## Token_shift feature contrast")
    lines.append("")
    lines.append("| feature | extinct mean | alive mean | delta |")
    lines.append("| --- | --- | --- | --- |")
    for row in feature_summary:
        lines.append(
            f"| {row['feature_name']} | {fmt(row['mean_token_extinct'])} | {fmt(row['mean_token_alive'])} | {fmt(row['delta_extinct_minus_alive'])} |"
        )
    lines.append("")
    lines.append("## Placement contrast")
    lines.append("")
    lines.append(
        f"- `token_extinct_add_alive_count`: `{sum(int(row['token_extinct_add_alive']) for row in placement_contrast)}`"
    )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal fragility-runde, ikke en ny collision-runde.")
    lines.append("- Les fortsatt dette som defect-dynamikk, ikke som partikkelbevis eller ny generell geometri.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15n token_shift fragility lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15n_token_shift_fragility_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15n_token_shift_fragility_aggregate.csv")
    p.add_argument("--out-feature-csv", type=str, default="Documentation/v15n_token_shift_fragility_feature_summary.csv")
    p.add_argument("--out-placement-csv", type=str, default="Documentation/v15n_token_shift_fragility_placement_contrast.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15n_token_shift_fragility_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15n_token_shift_fragility_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15n_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15n.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_summary = v10e.summarize_bases(base_rows)
    rows = run_rows(ensembles=ensembles, base_states=base_states)
    aggregate = aggregate_rows(rows)
    feature_summary = feature_rows(rows)
    placement_contrast = placement_contrast_rows(rows)
    recommendation = recommendation_rows(target_summary, aggregate, feature_summary, placement_contrast)
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        feature_summary=feature_summary,
        placement_contrast=placement_contrast,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15n operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som en smal fragility-/støttegeometrirunde, ikke som partikkelbevis.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15n",
            "",
            "Denne runden spør om den litt skjøre `token_shift`-defekten dør ut oftere på bestemte typer lokale steder i grafen.",
            "",
            "Det er nyttig fordi det kan fortelle oss om skjørheten er strukturert, eller om den fortsatt bare er blandet og vanskelig å forutsi.",
        ]
    ) + "\n"

    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_feature_csv, feature_summary)
    write_csv(args.out_placement_csv, placement_contrast)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
