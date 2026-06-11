#!/usr/bin/env python3
"""v0.15cy continuous genealogy intensity synthesis.

This is a no-new-dynamics analysis round. It combines the v15cw and v15cx
genealogy run tables and asks whether continuous genealogy intensity explains
far-shell horizon outcomes better than the coarse event-chain labels.

The intensity score is built only from genealogy/event/mass observables. Horizon
labels and horizon spans are downstream evaluation targets, never score inputs.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


INPUT_SOURCES = (
    {
        "lab": "v15cw",
        "source_scope": "calibration_seed_split",
        "path": Path("Documentation/v15cw_add_chord_p1_p3_genealogy_runs.csv"),
    },
    {
        "lab": "v15cx",
        "source_scope": "p1_1024_fresh_holdout",
        "path": Path("Documentation/v15cx_p1_1024_genealogy_holdout_runs.csv"),
    },
)

INDEX_FEATURES = (
    "churn_per_step",
    "split_per_step",
    "birth_death_per_step",
    "max_component_count_per_target",
    "max_total_defect_mass_fraction",
    "mean_total_defect_mass_fraction",
    "post_split_dual_fraction",
    "first_split_earliness",
)

EVALUATED_METRICS = (
    "genealogy_intensity_index",
    "churn_per_step",
    "split_per_step",
    "birth_death_per_step",
    "merge_per_step",
    "compress_per_step",
    "max_component_count_per_target",
    "max_total_defect_mass_fraction",
    "mean_total_defect_mass_fraction",
    "final_total_defect_mass_fraction",
    "post_split_dual_fraction",
    "first_split_earliness",
    "first_birth_earliness",
    "fragmentation_pressure",
    "merge_pressure",
)

SCOPES = (
    ("all_runs", lambda row: True),
    ("v15cw_all", lambda row: str(row["lab"]) == "v15cw"),
    ("p1_1024_all", lambda row: int(row["target_nodes"]) == 1024 and int(row["placement"]) == 1),
    ("p1_1024_holdout_only", lambda row: str(row["lab"]) == "v15cx"),
)


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


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
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


def clamp01(x: float) -> float:
    if not math.isfinite(x):
        return 0.0
    return max(0.0, min(1.0, x))


def horizon_binary(label: str) -> int:
    return int(str(label) == "established_far_shell_horizon")


def horizon_order(label: str) -> float:
    if str(label) == "established_far_shell_horizon":
        return 1.0
    if str(label) == "mixed_far_shell_horizon":
        return 0.5
    return 0.0


def enriched_row(raw: Mapping[str, Any], *, lab: str, source_scope: str) -> Dict[str, Any]:
    target = int(safe_float(raw["target_nodes"]))
    step_budget = safe_float(raw["step_budget"])
    split_count = safe_float(raw["split_count"])
    merge_count = safe_float(raw["merge_count"])
    birth_count = safe_float(raw["birth_count"])
    death_count = safe_float(raw["death_count"])
    compress_count = safe_float(raw["compress_count"])
    churn = safe_float(raw["churn_event_count"])
    first_split = safe_float(raw["first_split_step"])
    first_birth = safe_float(raw["first_birth_step"])
    post_dual = safe_float(raw["post_first_split_dual_duration"])
    max_components = safe_float(raw["max_component_count"])
    max_mass = safe_float(raw["max_total_defect_mass"])
    mean_mass = safe_float(raw["mean_total_defect_mass"])
    final_mass = safe_float(raw["final_total_defect_mass"])
    label = str(raw["far_shell_horizon_label"])

    row: Dict[str, Any] = {
        "lab": lab,
        "source_scope": source_scope,
        "target_nodes": target,
        "growth_seed": int(safe_float(raw["growth_seed"])),
        "profile_label": str(raw["profile_label"]),
        "perturbation": str(raw["perturbation"]),
        "placement": int(safe_float(raw["placement"])),
        "seed_delta": int(safe_float(raw["seed_delta"])),
        "run_seed": int(safe_float(raw["run_seed"])),
        "support_signature": str(raw["support_signature"]),
        "step_budget": int(step_budget),
        "genealogy_pattern": str(raw["genealogy_pattern"]),
        "far_shell_horizon_label": label,
        "horizon_binary_established": horizon_binary(label),
        "horizon_ordered": horizon_order(label),
        "high_horizon_span": safe_float(raw["high_horizon_span"]),
        "high_retention_rate": safe_float(raw["high_retention_rate"]),
        "last12_high_rate": safe_float(raw["last12_high_rate"]),
        "tail_mean_far_shell_share": safe_float(raw["tail_mean_far_shell_share"]),
        "tail_mean_weighted_mean_distance": safe_float(raw["tail_mean_weighted_mean_distance"]),
        "split_count": int(split_count),
        "merge_count": int(merge_count),
        "birth_count": int(birth_count),
        "death_count": int(death_count),
        "compress_count": int(compress_count),
        "churn_event_count": int(churn),
        "max_component_count": int(max_components),
        "max_total_defect_mass": int(max_mass),
        "mean_total_defect_mass": mean_mass,
        "final_total_defect_mass": int(final_mass),
        "post_first_split_dual_duration": int(post_dual) if post_dual >= 0 else 0,
        "first_split_step": int(first_split) if first_split >= 0 else -1,
        "first_birth_step": int(first_birth) if first_birth >= 0 else -1,
    }

    denom = max(1.0, step_budget)
    target_denom = max(1.0, float(target))
    row.update(
        {
            "churn_per_step": churn / denom,
            "split_per_step": split_count / denom,
            "birth_death_per_step": (birth_count + death_count) / denom,
            "merge_per_step": merge_count / denom,
            "compress_per_step": compress_count / denom,
            "max_component_count_per_target": max_components / target_denom,
            "max_total_defect_mass_fraction": max_mass / target_denom,
            "mean_total_defect_mass_fraction": mean_mass / target_denom,
            "final_total_defect_mass_fraction": final_mass / target_denom,
            "post_split_dual_fraction": max(0.0, post_dual) / denom,
            "first_split_earliness": clamp01(1.0 - first_split / denom) if first_split >= 0 else 0.0,
            "first_birth_earliness": clamp01(1.0 - first_birth / denom) if first_birth >= 0 else 0.0,
            "fragmentation_pressure": (split_count + birth_count) / denom,
            "merge_pressure": (merge_count + death_count) / denom,
        }
    )
    return row


def load_runs() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for source in INPUT_SOURCES:
        path = source["path"]
        if not path.exists():
            raise FileNotFoundError(f"Missing v15cy input: {path}")
        for raw in read_csv(path):
            rows.append(
                enriched_row(
                    raw,
                    lab=str(source["lab"]),
                    source_scope=str(source["source_scope"]),
                )
            )
    return rows


def normalized_values(rows: Sequence[Mapping[str, Any]], key: str) -> Dict[int, float]:
    vals = [safe_float(row[key]) for row in rows]
    finite = [x for x in vals if math.isfinite(x)]
    if not finite:
        return {idx: 0.0 for idx, _ in enumerate(rows)}
    lo, hi = min(finite), max(finite)
    if hi <= lo:
        return {idx: 0.5 for idx, _ in enumerate(rows)}
    return {
        idx: (safe_float(row[key]) - lo) / (hi - lo)
        if math.isfinite(safe_float(row[key]))
        else 0.0
        for idx, row in enumerate(rows)
    }


def add_intensity_scores(rows: List[Dict[str, Any]]) -> None:
    normalized = {key: normalized_values(rows, key) for key in INDEX_FEATURES}
    for idx, row in enumerate(rows):
        parts = [normalized[key][idx] for key in INDEX_FEATURES]
        row["genealogy_intensity_index"] = sum(parts) / len(parts)
        for key, value in zip(INDEX_FEATURES, parts):
            row[f"index_component_{key}"] = value


def pairwise_auc(rows: Sequence[Mapping[str, Any]], metric: str) -> float:
    pos = [safe_float(row[metric]) for row in rows if int(row["horizon_binary_established"]) == 1]
    neg = [safe_float(row[metric]) for row in rows if int(row["horizon_binary_established"]) == 0]
    pos = [x for x in pos if math.isfinite(x)]
    neg = [x for x in neg if math.isfinite(x)]
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


def rankdata(values: Sequence[float]) -> List[float]:
    pairs = sorted((value, idx) for idx, value in enumerate(values))
    ranks = [0.0] * len(values)
    i = 0
    while i < len(pairs):
        j = i + 1
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for _, idx in pairs[i:j]:
            ranks[idx] = avg_rank
        i = j
    return ranks


def pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return float("nan")
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return float("nan")
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / math.sqrt(vx * vy)


def spearman_metric(rows: Sequence[Mapping[str, Any]], metric: str, target_key: str) -> float:
    pairs = [
        (safe_float(row[metric]), safe_float(row[target_key]))
        for row in rows
        if math.isfinite(safe_float(row[metric])) and math.isfinite(safe_float(row[target_key]))
    ]
    if len(pairs) < 3:
        return float("nan")
    xs = rankdata([x for x, _ in pairs])
    ys = rankdata([y for _, y in pairs])
    return pearson(xs, ys)


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for scope_name, predicate in SCOPES:
        group = [row for row in rows if predicate(row)]
        n_pos = sum(1 for row in group if int(row["horizon_binary_established"]) == 1)
        n_neg = sum(1 for row in group if int(row["horizon_binary_established"]) == 0)
        for metric in EVALUATED_METRICS:
            pos_vals = [safe_float(row[metric]) for row in group if int(row["horizon_binary_established"]) == 1]
            neg_vals = [safe_float(row[metric]) for row in group if int(row["horizon_binary_established"]) == 0]
            mean_pos = mean_defined(pos_vals)
            mean_neg = mean_defined(neg_vals)
            out.append(
                {
                    "scope": scope_name,
                    "metric": metric,
                    "n_runs": len(group),
                    "n_established": n_pos,
                    "n_non_established": n_neg,
                    "mean_metric_established": mean_pos,
                    "mean_metric_non_established": mean_neg,
                    "mean_delta_established_minus_non": mean_pos - mean_neg if math.isfinite(mean_pos) and math.isfinite(mean_neg) else float("nan"),
                    "binary_pairwise_auc": pairwise_auc(group, metric),
                    "spearman_vs_horizon_span": spearman_metric(group, metric, "high_horizon_span"),
                    "spearman_vs_ordered_label": spearman_metric(group, metric, "horizon_ordered"),
                }
            )
    return out


def scope_summary_rows(rows: Sequence[Mapping[str, Any]], metric_scores: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    score_by_scope_metric = {(str(row["scope"]), str(row["metric"])): row for row in metric_scores}
    for scope_name, predicate in SCOPES:
        group = [row for row in rows if predicate(row)]
        patterns = Counter(str(row["genealogy_pattern"]) for row in group)
        established = [row for row in group if int(row["horizon_binary_established"]) == 1]
        non = [row for row in group if int(row["horizon_binary_established"]) == 0]
        score = score_by_scope_metric[(scope_name, "genealogy_intensity_index")]
        out.append(
            {
                "scope": scope_name,
                "n_runs": len(group),
                "n_established": len(established),
                "n_non_established": len(non),
                "established_rate": len(established) / max(1, len(group)),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "genealogy_patterns": ";".join(f"{key}:{value}" for key, value in sorted(patterns.items())),
                "intensity_auc": safe_float(score["binary_pairwise_auc"]),
                "intensity_spearman_span": safe_float(score["spearman_vs_horizon_span"]),
                "mean_intensity_established": safe_float(score["mean_metric_established"]),
                "mean_intensity_non_established": safe_float(score["mean_metric_non_established"]),
                "mean_churn_established": mean_defined(safe_float(row["churn_event_count"]) for row in established),
                "mean_churn_non_established": mean_defined(safe_float(row["churn_event_count"]) for row in non),
                "mean_max_mass_established": mean_defined(safe_float(row["max_total_defect_mass"]) for row in established),
                "mean_max_mass_non_established": mean_defined(safe_float(row["max_total_defect_mass"]) for row in non),
            }
        )
    return out


def top_metric_rows(metric_scores: Sequence[Mapping[str, Any]], *, limit: int = 5) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    scopes = sorted({str(row["scope"]) for row in metric_scores})
    for scope in scopes:
        rows = [row for row in metric_scores if str(row["scope"]) == scope]
        rows.sort(
            key=lambda row: (
                safe_float(row["binary_pairwise_auc"], -1.0),
                safe_float(row["spearman_vs_horizon_span"], -1.0),
                abs(safe_float(row["mean_delta_established_minus_non"], 0.0)),
            ),
            reverse=True,
        )
        for rank, row in enumerate(rows[:limit], start=1):
            out.append({"scope": scope, "rank": rank, **dict(row)})
    return out


def diagnosis_rows(
    *,
    rows: Sequence[Mapping[str, Any]],
    scope_summary: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    by_scope = {str(row["scope"]): row for row in scope_summary}
    score = {(str(row["scope"]), str(row["metric"])): row for row in metric_scores}
    required_labs = {str(source["lab"]) for source in INPUT_SOURCES}
    observed_labs = {str(row["lab"]) for row in rows}
    inputs_clean = required_labs.issubset(observed_labs)
    all_auc = safe_float(by_scope["all_runs"]["intensity_auc"])
    p1_auc = safe_float(by_scope["p1_1024_all"]["intensity_auc"])
    p1_holdout_auc = safe_float(by_scope["p1_1024_holdout_only"]["intensity_auc"])
    p1_span = safe_float(by_scope["p1_1024_all"]["intensity_spearman_span"])
    top_p1 = max(
        [row for row in metric_scores if str(row["scope"]) == "p1_1024_all"],
        key=lambda row: (safe_float(row["binary_pairwise_auc"], -1.0), safe_float(row["spearman_vs_horizon_span"], -1.0)),
    )

    if p1_auc >= 0.75 and p1_holdout_auc >= 0.75 and all_auc >= 0.75:
        status = "continuous_genealogy_intensity_promising_small_n"
        note = (
            f"Intensity AUC er {fmt(all_auc)} globalt, {fmt(p1_auc)} for p1/1024 og "
            f"{fmt(p1_holdout_auc)} i holdout-only. Dette er lovende, men post-hoc og liten n."
        )
        next_step = "pre_register_continuous_intensity_holdout"
        next_note = (
            "Frys intensity-score/top-metrikker og test paa nye runs foer scorevekter eller observabler justeres videre."
        )
    elif p1_auc >= 0.75 and p1_holdout_auc >= 0.75 and all_auc < 0.75:
        status = "local_p1_1024_intensity_promising_not_global"
        note = (
            f"Intensity AUC er {fmt(p1_auc)} for p1/1024 og {fmt(p1_holdout_auc)} i holdout-only, "
            f"men bare {fmt(all_auc)} globalt. Dette er en lokal selector-kandidat, ikke en generell genealogy-lov."
        )
        next_step = "pre_register_p1_1024_intensity_holdout"
        next_note = (
            "Frys intensity-score og test paa nye p1/1024-runs eller ny growth_seed foer bredere placement-tolkning."
        )
    elif p1_auc >= 0.75:
        status = "p1_1024_intensity_partial"
        note = (
            f"Intensity AUC er {fmt(p1_auc)} for p1/1024, men holdout-only/global stotte er svakere "
            f"({fmt(p1_holdout_auc)} / {fmt(all_auc)})."
        )
        next_step = "refine_intensity_or_phase_coupling"
        next_note = "Neste steg bor se paa event-timing mot band-entry foer flere brede runs."
    elif all_auc >= 0.75:
        status = "global_intensity_promising"
        note = f"Intensity AUC er {fmt(all_auc)} globalt; dette er uventet sterkt og bor holdout-testes."
        next_step = "pre_register_global_intensity_holdout"
        next_note = "Frys score og test paa friske target/placement-cases."
    else:
        status = "continuous_genealogy_intensity_not_supported"
        note = f"Intensity AUC er {fmt(all_auc)} globalt og {fmt(p1_auc)} for p1/1024; ikke nok som selector."
        next_step = "build_genealogy_band_phase_coupling"
        next_note = "Neste observabel bor koble event-pulser til far-shell band-entry i tid."

    return [
        {
            "diagnostic_family": "input_control",
            "status": "clean" if inputs_clean else "missing_inputs",
            "note": f"Leste labs {sorted(observed_labs)} fra eksisterende CSV-er; ingen ny dynamikk er kjoert.",
        },
        {
            "diagnostic_family": "coarse_label_result",
            "status": "coarse_event_labels_not_enough",
            "note": "v15cx svekket birth_death_churn/split_fragment som kategorisk selector; v15cy tester derfor kontinuerlige genealogy-features.",
        },
        {
            "diagnostic_family": "continuous_intensity_axis",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "best_p1_1024_metric",
            "status": str(top_p1["metric"]),
            "note": (
                f"Beste p1/1024-metrikk etter AUC er {top_p1['metric']} med AUC "
                f"{fmt(top_p1['binary_pairwise_auc'])} og Spearman mot horizon-span {fmt(top_p1['spearman_vs_horizon_span'])}."
            ),
        },
        {"diagnostic_family": "next_step", "status": next_step, "note": next_note},
    ]


def build_report(
    *,
    run_rows: Sequence[Mapping[str, Any]],
    scope_summary: Sequence[Mapping[str, Any]],
    top_metrics: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cy: continuous genealogy intensity synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en synteserunde uten ny dynamikk. Den leser v15cw/v15cx-run-tabeller og tester om kontinuerlig genealogy-intensitet forklarer far-shell horizon bedre enn grove event-chain labels.")
    lines.append("Intensity-scoren bruker bare genealogy/event/mass-felter; horizon-label og horizon-span brukes bare som downstream evaluering.")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append("| lab | scope | path |")
    lines.append("| --- | --- | --- |")
    for source in INPUT_SOURCES:
        lines.append(f"| {source['lab']} | {source['source_scope']} | `{source['path']}` |")
    lines.append("")
    lines.append("## Per-run score")
    lines.append("")
    lines.append("| lab | target | placement | seed | horizon | pattern | intensity | churn/step | max mass frac | dual frac |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in run_rows:
        lines.append(
            f"| {row['lab']} | {int(row['target_nodes'])} | p{int(row['placement'])} | {int(row['seed_delta'])} | {row['far_shell_horizon_label']} | {row['genealogy_pattern']} | {fmt(row['genealogy_intensity_index'])} | {fmt(row['churn_per_step'])} | {fmt(row['max_total_defect_mass_fraction'])} | {fmt(row['post_split_dual_fraction'])} |"
        )
    lines.append("")
    lines.append("## Scope summary")
    lines.append("")
    lines.append("| scope | n | est rate | intensity AUC | span rho | mean int est | mean int non | patterns |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in scope_summary:
        lines.append(
            f"| {row['scope']} | {int(row['n_runs'])} | {fmt(row['established_rate'])} | {fmt(row['intensity_auc'])} | {fmt(row['intensity_spearman_span'])} | {fmt(row['mean_intensity_established'])} | {fmt(row['mean_intensity_non_established'])} | {row['genealogy_patterns']} |"
        )
    lines.append("")
    lines.append("## Top metrics")
    lines.append("")
    lines.append("| scope | rank | metric | AUC | span rho | delta |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in top_metrics:
        if int(row["rank"]) <= 3:
            lines.append(
                f"| {row['scope']} | {int(row['rank'])} | {row['metric']} | {fmt(row['binary_pairwise_auc'])} | {fmt(row['spearman_vs_horizon_span'])} | {fmt(row['mean_delta_established_minus_non'])} |"
            )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er ikke en partikkel-, Lorentz-, invariant- eller entanglement-paastand.")
    lines.append("- En positiv intensity-score betyr bare at noen genealogy-intensitetsmaal predikerer horizon bedre enn grove labels i dette lokale datasettet.")
    lines.append("- Hvis neste holdout feiler, maa genealogy nedgraderes fra selector til diagnostikk og vi bor teste timing/phase-coupling mot band-entry.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cy", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Dette er en syntese av eksisterende v15cw/v15cx-resultater, ikke ny dynamikk.")
    lines.append("- Ikke oppgrader intensity-score til global invariant, Lorentz-likhet, partikler eller entanglement.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cy",
        "",
        "Denne runden spurte om mengden uro i skadehistorien er viktigere enn navnet vi gav typen uro.",
        "",
        f"- Kontinuerlig intensitet: `{diag['continuous_intensity_axis']['status']}`.",
        f"- Beste lokale maal: `{diag['best_p1_1024_metric']['status']}`.",
        "",
        "Det betyr ikke at vi har funnet en fysisk lov. Det betyr at neste test bor fryse en konkret score og se om den forutsier hvilke runs som faar lang hale.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cy continuous genealogy intensity synthesis.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cy_continuous_genealogy_intensity_runs.csv")
    p.add_argument("--out-metrics-csv", type=str, default="Documentation/v15cy_continuous_genealogy_intensity_metric_scores.csv")
    p.add_argument("--out-scope-csv", type=str, default="Documentation/v15cy_continuous_genealogy_intensity_scope_summary.csv")
    p.add_argument("--out-top-csv", type=str, default="Documentation/v15cy_continuous_genealogy_intensity_top_metrics.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cy_continuous_genealogy_intensity_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cy_continuous_genealogy_intensity_synthesis.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cy_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cy.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = load_runs()
    add_intensity_scores(run_rows)
    metric_scores = metric_score_rows(run_rows)
    scope_summary = scope_summary_rows(run_rows, metric_scores)
    top_metrics = top_metric_rows(metric_scores)
    diagnosis = diagnosis_rows(rows=run_rows, scope_summary=scope_summary, metric_scores=metric_scores)

    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_metrics_csv, metric_scores)
    write_csv(args.out_scope_csv, scope_summary)
    write_csv(args.out_top_csv, top_metrics)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            run_rows=run_rows,
            scope_summary=scope_summary,
            top_metrics=top_metrics,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
