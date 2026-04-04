#!/usr/bin/env python3
"""v0.15v add_chord triplet mechanism lab.

This round follows v15u. It does not reopen mapping. It re-runs the same
microcenter triplet and explains the mixed p0-p1-p2 picture with simple
late-tail lock observables.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def tail_hit_vectors(log_rows: Sequence[Dict[str, Any]], damaged_sets: Sequence[set[int]]) -> List[Dict[str, Any]]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    out: List[Dict[str, Any]] = []
    for idx in range(tail_start, len(log_rows)):
        cur_set = damaged_sets[idx]
        cur_sig = v15q.coarse_signature(log_rows[idx])
        best_exact = -1.0
        coarse_hit = False
        for prev in range(0, max(0, idx - v15q.MIN_GAP_SNAPSHOTS)):
            best_exact = max(best_exact, v15q.exact_jaccard(cur_set, damaged_sets[prev]))
            if v15q.coarse_signature(log_rows[prev]) == cur_sig:
                coarse_hit = True
        exact_hit = bool(math.isfinite(best_exact) and best_exact >= 0.95)
        coarse_only = bool(coarse_hit and not exact_hit)
        out.append(
            {
                "tail_index": idx,
                "step": int(log_rows[idx]["step"]),
                "best_exact_return_jaccard": best_exact if best_exact >= 0.0 else float("nan"),
                "exact_hit": 1 if exact_hit else 0,
                "coarse_hit": 1 if coarse_hit else 0,
                "coarse_only": 1 if coarse_only else 0,
            }
        )
    return out


def longest_streak(bits: Sequence[int]) -> int:
    best = 0
    cur = 0
    for bit in bits:
        if int(bit):
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def switch_count(bits: Sequence[int]) -> int:
    if not bits:
        return 0
    count = 0
    prev = int(bits[0])
    for bit in bits[1:]:
        bit = int(bit)
        if bit != prev:
            count += 1
        prev = bit
    return count


def classify_mechanism(
    *,
    first_exact_return_step: float,
    exact_hit_rate: float,
    coarse_hit_rate: float,
    coarse_only_rate: float,
    exact_lock_fraction: float,
    longest_exact_streak: int,
    exact_switch_count: int,
) -> str:
    if (
        math.isfinite(first_exact_return_step)
        and first_exact_return_step <= 1600
        and exact_hit_rate >= 0.80
        and exact_lock_fraction >= 0.80
        and longest_exact_streak >= 6
        and exact_switch_count <= 2
    ):
        return "early_stable_lock"
    if (
        math.isfinite(first_exact_return_step)
        and first_exact_return_step > 1600
        and exact_hit_rate >= 0.65
        and exact_lock_fraction >= 0.70
        and longest_exact_streak >= 4
    ):
        return "late_stable_lock"
    if exact_hit_rate >= 0.60 and exact_switch_count >= 3:
        return "intermittent_cycle_lock"
    if coarse_hit_rate >= 0.85 and coarse_only_rate >= 0.20 and exact_hit_rate < 0.60:
        return "coarse_cycle_shell"
    return "mixed_tail_lock"


def run_rows(*, base_state: Any) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    run_rows: List[Dict[str, Any]] = []
    tail_rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for placement in PLACEMENTS:
        base_run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
        for seed_delta in SEED_DELTAS:
            run_seed = int(base_run_seed + seed_delta)
            res = v15q.run_defect_with_sets(
                base_state,
                params=params,
                seed=run_seed,
                steps=FULL_STEPS,
                perturbation="add_chord",
                center_token_index=placement,
                local_coupling="maximal",
                log_every=LOG_EVERY,
            )
            metrics = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            vectors = tail_hit_vectors(res["log_rows"], res["damaged_sets"])
            exact_bits = [int(row["exact_hit"]) for row in vectors]
            coarse_bits = [int(row["coarse_hit"]) for row in vectors]
            coarse_only_bits = [int(row["coarse_only"]) for row in vectors]
            first_exact = safe_float(metrics["first_exact_return_step"])
            if math.isfinite(first_exact):
                post_first = [row for row in vectors if int(row["step"]) >= int(first_exact)]
            else:
                post_first = []
            exact_lock_fraction = mean_defined(float(row["exact_hit"]) for row in post_first)
            mechanism = classify_mechanism(
                first_exact_return_step=first_exact,
                exact_hit_rate=safe_float(metrics["exact_return_rate"]),
                coarse_hit_rate=safe_float(metrics["coarse_return_rate"]),
                coarse_only_rate=mean_defined(coarse_only_bits),
                exact_lock_fraction=exact_lock_fraction,
                longest_exact_streak=longest_streak(exact_bits),
                exact_switch_count=switch_count(exact_bits),
            )
            info = dict(res["perturbation_info"])
            run_rows.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in info.get("support", [])),
                    "full_label": v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), metrics),
                    "full_exact_return_rate": safe_float(metrics["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(metrics["coarse_return_rate"]),
                    "first_exact_return_step": first_exact,
                    "first_coarse_return_step": safe_float(metrics["first_coarse_return_step"]),
                    "exact_lock_fraction": exact_lock_fraction,
                    "longest_exact_streak": int(longest_streak(exact_bits)),
                    "exact_switch_count": int(switch_count(exact_bits)),
                    "coarse_only_rate": mean_defined(coarse_only_bits),
                    "tail_lock_mechanism": mechanism,
                }
            )
            for row in vectors:
                tail_rows.append(
                    {
                        "placement": int(placement),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        **row,
                    }
                )
    return run_rows, tail_rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        labels = [str(row["tail_lock_mechanism"]) for row in group]
        dominant = max(sorted(set(labels)), key=labels.count) if labels else "none"
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "early_stable_lock_rate": mean_defined(1.0 if str(row["tail_lock_mechanism"]) == "early_stable_lock" else 0.0 for row in group),
                "late_stable_lock_rate": mean_defined(1.0 if str(row["tail_lock_mechanism"]) == "late_stable_lock" else 0.0 for row in group),
                "intermittent_cycle_lock_rate": mean_defined(1.0 if str(row["tail_lock_mechanism"]) == "intermittent_cycle_lock" else 0.0 for row in group),
                "coarse_cycle_shell_rate": mean_defined(1.0 if str(row["tail_lock_mechanism"]) == "coarse_cycle_shell" else 0.0 for row in group),
                "mixed_tail_lock_rate": mean_defined(1.0 if str(row["tail_lock_mechanism"]) == "mixed_tail_lock" else 0.0 for row in group),
                "mean_first_exact_return_step": mean_defined(safe_float(row["first_exact_return_step"]) for row in group),
                "mean_exact_lock_fraction": mean_defined(safe_float(row["exact_lock_fraction"]) for row in group),
                "mean_longest_exact_streak": mean_defined(safe_float(row["longest_exact_streak"]) for row in group),
                "mean_exact_switch_count": mean_defined(safe_float(row["exact_switch_count"]) for row in group),
                "dominant_mechanism": dominant,
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], run_rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_place = {int(row["placement"]): row for row in aggregate}
    p0 = by_place[0]
    p1 = by_place[1]
    p2 = by_place[2]
    p0_lock = safe_float(p0["early_stable_lock_rate"])
    p1_lock = safe_float(p1["early_stable_lock_rate"])
    p2_lock = safe_float(p2["early_stable_lock_rate"])
    p0_switch = safe_float(p0["mean_exact_switch_count"])
    p1_switch = safe_float(p1["mean_exact_switch_count"])
    p2_switch = safe_float(p2["mean_exact_switch_count"])
    p0_first = safe_float(p0["mean_first_exact_return_step"])
    p1_first = safe_float(p1["mean_first_exact_return_step"])
    p2_first = safe_float(p2["mean_first_exact_return_step"])

    if p1_lock > p0_lock and p1_lock > p2_lock and p1_switch <= p0_switch and p1_switch <= p2_switch:
        status = "p1_mechanistically_sharpest"
        note = "P1 far flest tidlige stabile lock-runder og minst eller like lite switching som flankene."
        next_step = "inspect_p1_support_geometry"
        next_note = "Neste steg bør forklare hvorfor akkurat p1-støtten låser tidligere eller roligere enn flankene."
    elif p0_lock >= p1_lock and p0_first <= p1_first and p0_switch <= p1_switch:
        status = "p0_competes_by_lock"
        note = "P0 konkurrerer med eller slår p1 fordi den låser minst like tidlig og minst like rolig i tailen."
        next_step = "compare_p0_p1_support"
        next_note = "Neste steg bør sammenligne p0 og p1 støttegeometri direkte, ikke anta et rent sentrum."
    elif p2_lock < p0_lock and p2_lock < p1_lock and p2_switch >= max(p0_switch, p1_switch):
        status = "p2_weaker_tail_lock"
        note = "P2 er tydeligst svakere i tail-lock enn de to andre, så usikkerheten sitter mest mellom p0 og p1."
        next_step = "explain_left_pair"
        next_note = "Neste steg bør være en ren p0-vs-p1 forklaringsrunde."
    else:
        status = "triplet_mechanism_still_mixed"
        note = "Mekanismelesningen gjør triplet-en mer forklarbar, men ikke ren nok til å løse sentrumssporsmalet."
        next_step = "stay_micro"
        next_note = "Neste steg bør være en enda mindre støtte-/mekanismetest inne i samme triplet."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle add_chord-rundene matcher ønsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "triplet_mechanism_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "tail_lock_snapshot",
            "status": f"p0_lock={fmt(p0_lock)};p1_lock={fmt(p1_lock)};p2_lock={fmt(p2_lock)}",
            "note": f"Mean first exact return: p0={fmt(p0_first,1)}, p1={fmt(p1_first,1)}, p2={fmt(p2_first,1)}. Mean switch count: p0={fmt(p0_switch,1)}, p1={fmt(p1_switch,1)}, p2={fmt(p2_switch,1)}.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15v: add_chord triplet mechanism lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden forklarer det blandede `p0-p1-p2`-bildet med enkle tail-lock-observabler i stedet for å åpne et nytt søk."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Triplet mechanism summary")
    lines.append("")
    lines.append("| placement | n | early stable | late stable | intermittent | coarse shell | mean first exact | mean lock frac | mean switch count | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['early_stable_lock_rate'])} | {fmt(row['late_stable_lock_rate'])} | {fmt(row['intermittent_cycle_lock_rate'])} | {fmt(row['coarse_cycle_shell_rate'])} | {fmt(row['mean_first_exact_return_step'],1)} | {fmt(row['mean_exact_lock_fraction'])} | {fmt(row['mean_exact_switch_count'])} | {row['dominant_mechanism']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en mekanistisk forklaringsrunde inne i samme triplet, ikke en ny cycle-map.")
    lines.append("- Les dette som lokal tail-lock-struktur, ikke som generell defect-fysikk.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15v add_chord triplet mechanism lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15v_add_chord_triplet_mechanism_runs.csv")
    p.add_argument("--out-tail-csv", type=str, default="Documentation/v15v_add_chord_triplet_mechanism_tail_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15v_add_chord_triplet_mechanism_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15v_add_chord_triplet_mechanism_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15v_add_chord_triplet_mechanism_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15v_add_chord_triplet_mechanism_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15v_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15v.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    run_rows_out, tail_rows_out = run_rows(base_state=base_state)
    aggregate = aggregate_rows(run_rows_out)
    diagnosis = diagnosis_rows(target_summary, run_rows_out, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15v operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en liten mekanistisk forklaringsrunde i `p0-p1-p2`, ikke som en ny bred mapping.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15v",
            "",
            "Denne runden prøver å forklare hvorfor de tre nærmeste add_chord-punktene holder såpass godt, uten å lete etter flere punkter.",
            "",
            "Vi måler hvor tidlig og hvor stabilt skaden låser seg inn i senfase-retur, for å se om ett punkt virkelig er mer stabilt enn de andre.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, run_rows_out)
    write_csv(args.out_tail_csv, tail_rows_out)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
