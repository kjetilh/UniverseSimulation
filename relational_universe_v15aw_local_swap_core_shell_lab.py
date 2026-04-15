#!/usr/bin/env python3
"""v0.15aw local_swap core-shell recurrence lab.

This round leaves the add_chord fade boundary behind and asks a new narrow
question:

does the local_swap recurrence signal from v15q also look like a stable damage
core with a fluctuating shell, or is add_chord unusually clean on that axis?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGETS = (48, 96)
GROWTH_SEEDS = (101, 202)
PLACEMENTS = (0, 1, 2, 3)
FULL_STEPS = v15q.STEPS
LOG_EVERY = v15q.LOG_EVERY
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
    if core_share >= 0.55 and shell_share >= 0.08 and support_core_frac >= 0.50:
        return "stable_core_variable_shell"
    if core_share >= 0.70 and shell_share < 0.10:
        return "dominant_static_core"
    if core_share < 0.40 and shell_share >= 0.25:
        return "diffuse_shell_recurrence"
    if rare_share >= 0.30:
        return "rare_turnover_heavy"
    return "mixed_core_shell"


def core_shell_metrics(damaged_sets: Sequence[Set[int]], support: Sequence[int]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = damaged_sets[tail_start:]
    denom = max(1, len(tail_sets))

    occ: Dict[int, int] = {}
    sizes: List[int] = []
    for damaged in tail_sets:
        sizes.append(len(damaged))
        for node in damaged:
            occ[node] = occ.get(node, 0) + 1

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

    core_cover = [
        len(core_nodes.intersection(damaged)) / max(1, len(core_nodes))
        if core_nodes
        else float("nan")
        for damaged in tail_sets
    ]
    shell_cover = [
        len(shell_nodes.intersection(damaged)) / max(1, len(shell_nodes))
        if shell_nodes
        else float("nan")
        for damaged in tail_sets
    ]

    core_share = len(core_nodes) / union_count
    shell_share = len(shell_nodes) / union_count
    rare_share = len(rare_nodes) / union_count
    support_core_frac = support_core / max(1, len(support_set))

    core_cover_defined = [x for x in core_cover if math.isfinite(x)]
    shell_cover_defined = [x for x in shell_cover if math.isfinite(x)]
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
        "mean_core_cover": mean_defined(core_cover_defined),
        "q10_core_cover": quantile(core_cover_defined, 0.10) if core_cover_defined else float("nan"),
        "mean_shell_cover": mean_defined(shell_cover_defined),
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


def run_rows(*, base_states: Mapping[Tuple[str, int], Any], ensembles: Sequence[Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for ens in ensembles:
        target = int(ens.target_nodes)
        for growth_seed in GROWTH_SEEDS:
            base_state = base_states[(ens.name, growth_seed)]
            for placement in PLACEMENTS:
                run_seed = target * 100000 + int(growth_seed) * 1000 + int(placement)
                res = v15q.run_defect_with_sets(
                    base_state,
                    params=params,
                    seed=run_seed,
                    steps=FULL_STEPS,
                    perturbation="local_swap",
                    center_token_index=int(placement),
                    local_coupling="maximal",
                    log_every=LOG_EVERY,
                )
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                info = dict(res["perturbation_info"])
                support = list(info.get("support", []))
                core_shell = core_shell_metrics(res["damaged_sets"], support)
                full_label = v15q.classify_recurrence_label(int(res["summary"]["final_alive"]), recurrence)
                rows.append(
                    {
                        "target_nodes": target,
                        "growth_seed": int(growth_seed),
                        "placement": int(placement),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match("local_swap", str(info.get("type", "unknown")))),
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
    for target in TARGETS:
        group = [row for row in rows if int(row["target_nodes"]) == int(target)]
        out.append(
            {
                "target_nodes": int(target),
                "n_runs": len(group),
                "cyclic_rate": mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group),
                "morphology_return_rate": mean_defined(1.0 if str(row["full_label"]) == "morphology_return" else 0.0 for row in group),
                "stable_core_variable_shell_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "stable_core_variable_shell" else 0.0 for row in group),
                "dominant_static_core_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "dominant_static_core" else 0.0 for row in group),
                "diffuse_shell_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "diffuse_shell_recurrence" else 0.0 for row in group),
                "rare_turnover_rate": mean_defined(1.0 if str(row["core_shell_label"]) == "rare_turnover_heavy" else 0.0 for row in group),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in group),
                "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in group),
                "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in group),
                "mean_support_core_frac": mean_defined(safe_float(row["support_core_frac"]) for row in group),
                "mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in group),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) in TARGETS)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    mean_core_structured = mean_defined(
        safe_float(row["stable_core_variable_shell_rate"]) + safe_float(row["dominant_static_core_rate"])
        for row in aggregate
    )
    mean_diffuse = mean_defined(safe_float(row["diffuse_shell_rate"]) for row in aggregate)
    mean_core_share = mean_defined(safe_float(row["mean_core_share_of_union"]) for row in aggregate)

    if mean_core_structured >= 0.75 and mean_core_share >= 0.60:
        status = "local_swap_is_core_shell_like"
        note = "local_swap-recurrence leses best som en vedvarende kjerne med begrenset randvariasjon, så denne mesoskopiske observabelen generaliserer utover add_chord."
        next_step = "compare_boundary_dynamics"
        next_note = "Neste steg bør sammenligne randdynamikken i add_chord og local_swap direkte, siden begge nå ser ut til å ha en tydelig kjernekomponent."
    elif mean_diffuse >= 0.40:
        status = "local_swap_more_diffuse_than_add_chord"
        note = "local_swap holder recurrence, men ser morfologisk mer diffus ut enn add_chord på denne observabelen."
        next_step = "probe_diffuse_boundary"
        next_note = "Neste steg bør være en rand-/turnover-observabel som forklarer hvorfor local_swap ikke samler seg til samme rene kjernebilde som add_chord."
    else:
        status = "local_swap_core_shell_mixed"
        note = "local_swap får en del kjerne/rand-struktur, men ikke rent nok til én enkel generaliserende lesning ennå."
        next_step = "stay_local_on_swap"
        next_note = "Neste steg bør være en enda smalere local_swap-observabel, ikke en ny bred defect-scan."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle smale local_swap-profiler matcher ønsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "local_swap_core_shell_status",
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
    lines.append("# Relasjonell universgraf v0.15aw: local_swap core-shell recurrence lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden spør om local_swap-recurrence best leses som en stabil skadekjerne med variabel rand, slik add_chord etter hvert gjorde, eller om add_chord var et særtilfelle på denne observabelen.")
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) not in TARGETS:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Core-shell summary")
    lines.append("")
    lines.append("| target | n | cyclic | morphology return | core+shell | static core | diffuse shell | mean core share | mean shell share | mean support core frac |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['n_runs'])} | {fmt(row['cyclic_rate'])} | {fmt(row['morphology_return_rate'])} | {fmt(row['stable_core_variable_shell_rate'])} | {fmt(row['dominant_static_core_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_shell_share_of_union'])} | {fmt(row['mean_support_core_frac'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ny observabel på local_swap-sporet, ikke en ny add_chord-runde.")
    lines.append("- Les dette som mesoskopisk morfologi for recurrence, ikke som bevis for partikler eller generell geometri.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15aw local_swap core-shell recurrence lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15aw_local_swap_core_shell_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15aw_local_swap_core_shell_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15aw_local_swap_core_shell_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15aw_local_swap_core_shell_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15aw_local_swap_core_shell_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15aw_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15aw.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_summary = v10e.summarize_bases(base_rows)
    rows = run_rows(base_states=base_states, ensembles=ensembles)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15aw operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en ny local_swap-observabel, ikke som en bred ny defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15aw",
            "",
            "Denne runden spør om local_swap-skader som kommer tilbake senere gjør det ved å beholde en stabil kjerne av noder, mens bare randen skifter litt, eller om hele skadesonen flyter rundt uten noen tydelig kjerne.",
            "",
            "Det er nyttig fordi det lar oss teste om add_chord var et særtilfelle, eller om samme type lokale struktur også dukker opp for en annen type skade.",
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
