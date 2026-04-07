#!/usr/bin/env python3
"""v0.15ac add_chord core-shell recurrence lab.

This round follows v15ab. Since the local add_chord cycle band looks diffuse
in lag-space, it asks a different question:

does late recurrence come from a stable damaged-node core with a fluctuating
shell, or from broadly diffuse node turnover without a clear persistent core?
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8
CORE_THRESHOLD = 0.80
SHELL_THRESHOLD = 0.20


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


def classify_core_shell(*, core_share: float, shell_share: float, support_core_frac: float, rare_share: float) -> str:
    if core_share >= 0.60 and shell_share >= 0.10 and support_core_frac >= 0.66:
        return "stable_core_variable_shell"
    if core_share >= 0.75 and shell_share < 0.10:
        return "dominant_static_core"
    if core_share < 0.40 and shell_share >= 0.30:
        return "diffuse_shell_recurrence"
    if rare_share >= 0.30:
        return "rare_turnover_heavy"
    return "mixed_core_shell"


def core_shell_metrics(damaged_sets: Sequence[Set[int]], support: Sequence[int]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = damaged_sets[tail_start:]
    denom = max(1, len(tail_sets))

    occ: Counter[int] = Counter()
    sizes: List[int] = []
    for damaged in tail_sets:
        sizes.append(len(damaged))
        occ.update(damaged)

    union_nodes = set(occ.keys())
    occupancies = {node: count / denom for node, count in occ.items()}
    core_nodes = {node for node, frac in occupancies.items() if frac >= CORE_THRESHOLD}
    shell_nodes = {node for node, frac in occupancies.items() if SHELL_THRESHOLD <= frac < CORE_THRESHOLD}
    rare_nodes = {node for node, frac in occupancies.items() if 0.0 < frac < SHELL_THRESHOLD}
    support_set = set(support)

    support_core = len(core_nodes.intersection(support_set))
    support_shell = len(shell_nodes.intersection(support_set))
    support_rare = len(rare_nodes.intersection(support_set))
    union_count = max(1, len(union_nodes))

    core_cover = [len(core_nodes.intersection(damaged)) / max(1, len(core_nodes)) if core_nodes else float("nan") for damaged in tail_sets]
    shell_cover = [len(shell_nodes.intersection(damaged)) / max(1, len(shell_nodes)) if shell_nodes else float("nan") for damaged in tail_sets]

    core_share = len(core_nodes) / union_count
    shell_share = len(shell_nodes) / union_count
    rare_share = len(rare_nodes) / union_count
    support_core_frac = support_core / max(1, len(support_set))

    return {
        "tail_snapshot_count": denom,
        "tail_union_nodes": len(union_nodes),
        "mean_tail_damage_nodes": mean_defined(sizes),
        "q10_tail_damage_nodes": quantile(sizes, 0.10) if sizes else float("nan"),
        "q90_tail_damage_nodes": quantile(sizes, 0.90) if sizes else float("nan"),
        "core_nodes": len(core_nodes),
        "shell_nodes": len(shell_nodes),
        "rare_nodes": len(rare_nodes),
        "core_share_of_union": core_share,
        "shell_share_of_union": shell_share,
        "rare_share_of_union": rare_share,
        "mean_core_cover": mean_defined(x for x in core_cover if math.isfinite(x)),
        "q10_core_cover": quantile([x for x in core_cover if math.isfinite(x)], 0.10) if any(math.isfinite(x) for x in core_cover) else float("nan"),
        "mean_shell_cover": mean_defined(x for x in shell_cover if math.isfinite(x)),
        "support_core_count": support_core,
        "support_shell_count": support_shell,
        "support_rare_count": support_rare,
        "support_core_frac": support_core_frac,
        "support_shell_frac": support_shell / max(1, len(support_set)),
        "label": classify_core_shell(
            core_share=core_share,
            shell_share=shell_share,
            support_core_frac=support_core_frac,
            rare_share=rare_share,
        ),
    }


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
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
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            info = dict(res["perturbation_info"])
            support = list(info.get("support", []))
            core_shell = core_shell_metrics(res["damaged_sets"], support)
            full_label = v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), recurrence)
            rows.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "full_label": full_label,
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "tail_union_nodes": int(core_shell["tail_union_nodes"]),
                    "mean_tail_damage_nodes": safe_float(core_shell["mean_tail_damage_nodes"]),
                    "core_nodes": int(core_shell["core_nodes"]),
                    "shell_nodes": int(core_shell["shell_nodes"]),
                    "rare_nodes": int(core_shell["rare_nodes"]),
                    "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                    "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                    "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                    "mean_core_cover": safe_float(core_shell["mean_core_cover"]),
                    "q10_core_cover": safe_float(core_shell["q10_core_cover"]),
                    "mean_shell_cover": safe_float(core_shell["mean_shell_cover"]),
                    "support_core_count": int(core_shell["support_core_count"]),
                    "support_shell_count": int(core_shell["support_shell_count"]),
                    "support_rare_count": int(core_shell["support_rare_count"]),
                    "support_core_frac": safe_float(core_shell["support_core_frac"]),
                    "support_shell_frac": safe_float(core_shell["support_shell_frac"]),
                    "core_shell_label": str(core_shell["label"]),
                }
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "cyclic_rate": mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group),
                "stable_core_variable_shell_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "stable_core_variable_shell" else 0.0 for row in group),
                "dominant_static_core_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "dominant_static_core" else 0.0 for row in group),
                "diffuse_shell_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "diffuse_shell_recurrence" else 0.0 for row in group),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
                "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in group),
                "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in group),
                "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in group),
                "mean_core_nodes": mean_defined(safe_float(row["core_nodes"]) for row in group),
                "mean_shell_nodes": mean_defined(safe_float(row["shell_nodes"]) for row in group),
                "mean_support_core_frac": mean_defined(safe_float(row["support_core_frac"]) for row in group),
                "mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in group),
                "q10_core_cover": quantile([safe_float(row["mean_core_cover"]) for row in group], 0.10),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    by_place = {int(row["placement"]): row for row in aggregate}
    p0 = by_place[0]
    p1 = by_place[1]
    p2 = by_place[2]

    if min(safe_float(p0["stable_core_variable_shell_rate"]), safe_float(p1["stable_core_variable_shell_rate"]), safe_float(p2["stable_core_variable_shell_rate"])) >= 0.50:
        status = "cycle_band_is_core_shell"
        note = "Det lokale add_chord-båndet ser ut til å være drevet av en stabil kjerne med variabel rand, ikke av en skarp periode."
        next_step = "probe_boundary_shell"
        next_note = "Neste steg bør måle randdynamikken mer direkte, siden det nå ser ut til å være der variasjonen sitter."
    elif max(safe_float(p0["diffuse_shell_rate"]), safe_float(p1["diffuse_shell_rate"]), safe_float(p2["diffuse_shell_rate"])) >= 0.50:
        status = "core_shell_not_yet"
        note = "Selv kjerne/rand-observabelen ser fortsatt for diffus ut til å gi én ren forklaring av recurrence-båndet."
        next_step = "change_observable_again"
        next_note = "Neste steg bør være en annen observabel enn kjerne/rand langs denne aksen."
    else:
        status = "core_shell_mixed"
        note = "Kjerne/rand-observabelen gjør båndet mer konkret, men ikke rent nok til én enkel lesning ennå."
        next_step = "stay_local"
        next_note = "Neste steg bør være en enda mindre forklaringsrunde i samme band."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle smale core-shell-profiler matcher ønsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "core_shell_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ac: add_chord core-shell recurrence lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden spør om det lokale add_chord-recurrence-båndet ser ut som en stabil skadekjerne med flimrende rand, eller som bred diffus turnover uten en tydelig vedvarende kjerne.")
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
    lines.append("## Core-shell summary")
    lines.append("")
    lines.append("| placement | n | cyclic | core+shell | static core | diffuse shell | mean core share | mean shell share | mean support core frac |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['cyclic_rate'])} | {fmt(row['stable_core_variable_shell_rate'])} | {fmt(row['dominant_static_core_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_shell_share_of_union'])} | {fmt(row['mean_support_core_frac'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ny observabel inne i samme lokale add_chord-band, ikke en ny placement-scan.")
    lines.append("- Les dette som kjerne/rand-diagnostikk for recurrence, ikke som bevis for en generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ac add_chord core-shell recurrence lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ac_add_chord_core_shell_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ac_add_chord_core_shell_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ac_add_chord_core_shell_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ac_add_chord_core_shell_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ac_add_chord_core_shell_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ac_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ac.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    rows = run_rows(base_state=base_state)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ac operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en ny kjerne/rand-observabel inne i det lokale add_chord-båndet, ikke som en ny scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ac",
            "",
            "Denne runden spør om skaden som kommer tilbake ser ut til å ha en stabil kjerne av noder som nesten alltid er med, mens randen skifter litt, eller om hele skadesonen bare flyter rundt uten en tydelig kjerne.",
            "",
            "Vi måler derfor hvor ofte hver node er med i den sene delen av utviklingen for de samme tre lokale add_chord-plasseringene som før.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
