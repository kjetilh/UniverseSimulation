#!/usr/bin/env python3
"""v0.12f budget-aware screening around band_zero_del.

This follows v0.12e. The question is no longer only whether a compact basis
can sort start states, but whether it can save expensive full-dynamics budget
in a realistic screening flow.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e


ANCHOR_REGIME = "band_zero_del"
TARGET_METRIC = "mean_final_radius_control"
BASIS_SPECS = [
    ("spectral_plus_dim", ("initial_spectral_per_sqrtN", "initial_dim_proxy")),
    ("spectral_only", ("initial_spectral_per_sqrtN",)),
    ("full_basis", tuple(v12.BASIS_FEATURES)),
]
DIAGNOSTIC_POLICIES = [
    "random_baseline",
    "oracle_actual",
]
REFERENCE_POLICY = "full_basis"
REFERENCE_BUDGET = 0.50


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def fixed_candidate():
    import relational_universe_v09_scale_and_natural_ensembles as v09

    return v09.ScaleCandidate(ANCHOR_REGIME, 0.02, 0.00, 0.02, 0.00, 0.00)


def score_rows(
    train_rows: Sequence[Dict[str, Any]],
    test_rows: Sequence[Dict[str, Any]],
    policy_name: str,
    features: Sequence[str],
    rng: random.Random,
) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []
    if policy_name == "random_baseline":
        for row in test_rows:
            out = dict(row)
            out["screen_score"] = rng.random()
            enriched.append(out)
        return enriched
    if policy_name == "oracle_actual":
        for row in test_rows:
            out = dict(row)
            out["screen_score"] = safe_float(row[TARGET_METRIC])
            enriched.append(out)
        return enriched

    intercept, weights = v12.fit_linear_regression(train_rows, features, TARGET_METRIC)
    for row in test_rows:
        out = dict(row)
        out["screen_score"] = v12.predict_row(row, features, intercept, weights)
        enriched.append(out)
    return enriched


def actual_top_rows(rows: Sequence[Dict[str, Any]], q: float = 0.25) -> List[Dict[str, Any]]:
    if not rows:
        return []
    top_n = max(1, int(math.ceil(len(rows) * q)))
    ranked = sorted(rows, key=lambda r: safe_float(r[TARGET_METRIC]), reverse=True)
    return ranked[:top_n]


def select_within_target(rows: Sequence[Dict[str, Any]], budget_frac: float) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    selected: List[Dict[str, Any]] = []
    for target in sorted(by_target):
        sub = sorted(by_target[target], key=lambda r: safe_float(r["screen_score"]), reverse=True)
        take = max(1, int(round(len(sub) * budget_frac)))
        take = min(len(sub), take)
        selected.extend(sub[:take])
    return selected


def select_global(rows: Sequence[Dict[str, Any]], budget_frac: float) -> List[Dict[str, Any]]:
    ranked = sorted(rows, key=lambda r: safe_float(r["screen_score"]), reverse=True)
    take = max(1, int(round(len(ranked) * budget_frac)))
    take = min(len(ranked), take)
    return ranked[:take]


def same_identity(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
    return (
        str(a["ensemble"]) == str(b["ensemble"])
        and int(a["target_nodes"]) == int(b["target_nodes"])
        and int(a["growth_seed"]) == int(b["growth_seed"])
    )


def selection_metrics(
    selected_rows: Sequence[Dict[str, Any]],
    all_rows: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    overall_mean = mean_defined(safe_float(r[TARGET_METRIC]) for r in all_rows)
    selected_mean = mean_defined(safe_float(r[TARGET_METRIC]) for r in selected_rows)
    selected_lift = (
        (selected_mean / overall_mean) - 1.0
        if math.isfinite(overall_mean) and abs(overall_mean) > 1e-12
        else float("nan")
    )

    actual_best = max(all_rows, key=lambda r: safe_float(r[TARGET_METRIC]))
    global_best_hit = 1.0 if any(same_identity(actual_best, row) for row in selected_rows) else 0.0

    actual_top = actual_top_rows(all_rows)
    global_top_hits = sum(
        1
        for top_row in actual_top
        if any(same_identity(top_row, row) for row in selected_rows)
    )
    global_top_recall = global_top_hits / len(actual_top) if actual_top else float("nan")

    by_target_all: Dict[int, List[Dict[str, Any]]] = {}
    by_target_sel: Dict[int, List[Dict[str, Any]]] = {}
    for row in all_rows:
        by_target_all.setdefault(int(row["target_nodes"]), []).append(dict(row))
    for row in selected_rows:
        by_target_sel.setdefault(int(row["target_nodes"]), []).append(dict(row))

    target_best_hits: List[float] = []
    target_top_recalls: List[float] = []
    target_lifts: List[float] = []
    for target in sorted(by_target_all):
        sub_all = by_target_all[target]
        sub_sel = by_target_sel.get(target, [])
        actual_best_target = max(sub_all, key=lambda r: safe_float(r[TARGET_METRIC]))
        target_best_hits.append(1.0 if any(same_identity(actual_best_target, row) for row in sub_sel) else 0.0)
        actual_top_target = actual_top_rows(sub_all)
        captured = sum(
            1
            for top_row in actual_top_target
            if any(same_identity(top_row, row) for row in sub_sel)
        )
        target_top_recalls.append(captured / len(actual_top_target) if actual_top_target else float("nan"))
        mean_all = mean_defined(safe_float(r[TARGET_METRIC]) for r in sub_all)
        mean_sel = mean_defined(safe_float(r[TARGET_METRIC]) for r in sub_sel)
        if math.isfinite(mean_all) and abs(mean_all) > 1e-12:
            target_lifts.append((mean_sel / mean_all) - 1.0)

    return {
        "selected_rows": len(selected_rows),
        "selected_mean_radius": selected_mean,
        "selected_lift_all": selected_lift,
        "global_best_hit": global_best_hit,
        "global_top_quartile_recall": global_top_recall,
        "within_target_best_hit": mean_defined(target_best_hits),
        "within_target_top_quartile_recall": mean_defined(target_top_recalls),
        "within_target_selected_lift": mean_defined(target_lifts),
    }


def budget_policy_rows(
    base_level_rows: Sequence[Dict[str, Any]],
    repeats: int,
    test_frac: float,
    seed: int,
    budgets: Sequence[float],
) -> List[Dict[str, Any]]:
    master_rng = random.Random(seed)
    rows: List[Dict[str, Any]] = []
    for split_id in range(1, repeats + 1):
        split_rng = random.Random(master_rng.randint(1, 10**9))
        train_idx, test_idx = v12e.stratified_holdout_indices(base_level_rows, split_rng, test_frac)
        train_rows = [dict(base_level_rows[i]) for i in train_idx]
        test_rows = [dict(base_level_rows[i]) for i in test_idx]

        for policy_name, features in BASIS_SPECS:
            scored = score_rows(train_rows, test_rows, policy_name, features, split_rng)
            for budget_frac in budgets:
                selected = select_within_target(scored, budget_frac)
                metrics = selection_metrics(selected, scored)
                rows.append(
                    {
                        "split_id": split_id,
                        "policy_name": policy_name,
                        "policy_type": "model",
                        "basis_features": "+".join(features),
                        "feature_count": len(features),
                        "budget_frac": budget_frac,
                        **metrics,
                    }
                )

        for policy_name in DIAGNOSTIC_POLICIES:
            scored = score_rows(train_rows, test_rows, policy_name, (), split_rng)
            for budget_frac in budgets:
                selected = select_within_target(scored, budget_frac)
                metrics = selection_metrics(selected, scored)
                rows.append(
                    {
                        "split_id": split_id,
                        "policy_name": policy_name,
                        "policy_type": "diagnostic",
                        "basis_features": "",
                        "feature_count": 0,
                        "budget_frac": budget_frac,
                        **metrics,
                    }
                )
    return rows


def aggregate_budget_rows(policy_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    keys = sorted({(str(r["policy_name"]), float(r["budget_frac"])) for r in policy_rows})
    for policy_name, budget_frac in keys:
        sub = [r for r in policy_rows if str(r["policy_name"]) == policy_name and abs(float(r["budget_frac"]) - budget_frac) <= 1e-12]
        out.append(
            {
                "policy_name": policy_name,
                "policy_type": sub[0]["policy_type"] if sub else "",
                "budget_frac": budget_frac,
                "feature_count": int(sub[0]["feature_count"]) if sub else 0,
                "mean_global_best_hit": mean_defined(safe_float(r["global_best_hit"]) for r in sub),
                "mean_global_top_quartile_recall": mean_defined(safe_float(r["global_top_quartile_recall"]) for r in sub),
                "mean_within_target_best_hit": mean_defined(safe_float(r["within_target_best_hit"]) for r in sub),
                "mean_within_target_top_quartile_recall": mean_defined(safe_float(r["within_target_top_quartile_recall"]) for r in sub),
                "mean_selected_lift_all": mean_defined(safe_float(r["selected_lift_all"]) for r in sub),
                "mean_within_target_selected_lift": mean_defined(safe_float(r["within_target_selected_lift"]) for r in sub),
            }
        )
    return out


def auc_from_budget_curve(rows: Sequence[Dict[str, Any]], metric_key: str) -> float:
    if len(rows) < 2:
        return float("nan")
    ordered = sorted(rows, key=lambda r: float(r["budget_frac"]))
    area = 0.0
    for left, right in zip(ordered[:-1], ordered[1:]):
        x0 = float(left["budget_frac"])
        x1 = float(right["budget_frac"])
        y0 = safe_float(left[metric_key])
        y1 = safe_float(right[metric_key])
        area += 0.5 * (y0 + y1) * (x1 - x0)
    width = float(ordered[-1]["budget_frac"]) - float(ordered[0]["budget_frac"])
    return (area / width) if width > 1e-12 else float("nan")


def min_budget_for_threshold(rows: Sequence[Dict[str, Any]], metric_key: str, threshold: float) -> float:
    ordered = sorted(rows, key=lambda r: float(r["budget_frac"]))
    for row in ordered:
        if safe_float(row[metric_key]) >= threshold:
            return float(row["budget_frac"])
    return float("nan")


def policy_summary_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ref_rows = [r for r in aggregate_rows if str(r["policy_name"]) == REFERENCE_POLICY]
    ref_row = next((r for r in ref_rows if abs(float(r["budget_frac"]) - REFERENCE_BUDGET) <= 1e-12), None)
    ref_hit = safe_float(ref_row["mean_within_target_best_hit"]) if ref_row else float("nan")
    ref_recall = safe_float(ref_row["mean_within_target_top_quartile_recall"]) if ref_row else float("nan")

    out: List[Dict[str, Any]] = []
    for policy_name in sorted({str(r["policy_name"]) for r in aggregate_rows}):
        sub = [r for r in aggregate_rows if str(r["policy_name"]) == policy_name]
        best_033 = min(sub, key=lambda r: abs(float(r["budget_frac"]) - (1.0 / 3.0)))
        best_050 = min(sub, key=lambda r: abs(float(r["budget_frac"]) - REFERENCE_BUDGET))
        out.append(
            {
                "policy_name": policy_name,
                "policy_type": sub[0]["policy_type"] if sub else "",
                "feature_count": int(sub[0]["feature_count"]) if sub else 0,
                "auc_within_target_best_hit": auc_from_budget_curve(sub, "mean_within_target_best_hit"),
                "auc_within_target_top_quartile_recall": auc_from_budget_curve(sub, "mean_within_target_top_quartile_recall"),
                "auc_within_target_selected_lift": auc_from_budget_curve(sub, "mean_within_target_selected_lift"),
                "budget_to_match_full_basis_hit50": min_budget_for_threshold(sub, "mean_within_target_best_hit", ref_hit),
                "budget_to_match_full_basis_recall50": min_budget_for_threshold(sub, "mean_within_target_top_quartile_recall", ref_recall),
                "mean_within_target_best_hit_at_033": safe_float(best_033["mean_within_target_best_hit"]),
                "mean_within_target_best_hit_at_050": safe_float(best_050["mean_within_target_best_hit"]),
                "mean_within_target_recall_at_050": safe_float(best_050["mean_within_target_top_quartile_recall"]),
            }
        )
    out.sort(
        key=lambda row: (
            safe_float(row["auc_within_target_best_hit"], -1e9),
            safe_float(row["auc_within_target_top_quartile_recall"], -1e9),
            safe_float(row["auc_within_target_selected_lift"], -1e9),
        ),
        reverse=True,
    )
    for idx, row in enumerate(out, start=1):
        row["rank"] = idx
    return out


def target_summary(base_rows: Sequence[Dict[str, Any]], base_level_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    base_lookup = {(int(r["target_nodes"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in base_level_rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    prev_q90 = None
    for target in sorted(by_target):
        sub = by_target[target]
        initial_nodes = [
            safe_float(base_lookup[(int(r["target_nodes"]), int(r["growth_seed"]))]["initial_nodes"])
            for r in sub
        ]
        actual_radius = [safe_float(r[TARGET_METRIC]) for r in sub]
        q10 = v10b.quantile(initial_nodes, 0.10)
        q90 = v10b.quantile(initial_nodes, 0.90)
        separated = 1 if prev_q90 is None or q10 > prev_q90 else 0
        out.append(
            {
                "target_nodes": target,
                "bases": len(sub),
                "mean_initial_nodes": mean_defined(initial_nodes),
                "q10_initial_nodes": q10,
                "q90_initial_nodes": q90,
                "mean_actual_radius": mean_defined(actual_radius),
                "sd_actual_radius": v12e.sd_or_zero(actual_radius),
                "separated_from_prev": separated,
            }
        )
        prev_q90 = q90
    return out


def build_report(
    target_rows: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    summary_rows: Sequence[Dict[str, Any]],
    *,
    base_count: int,
    run_count: int,
    repeats: int,
    test_frac: float,
    budgets: Sequence[float],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12f: budsjettstyrt screening av starttilstander")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om de enkle geometri-basisene fra v12e faktisk kan spare full simulasjonsbudsjett. Sporsmalet er ikke bare om de korrelerer med radius, men om de kan brukes til a velge hvilke baser vi faktisk bor bruke dyre dynamikk-kjoringer pa."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append(f"- Arbeidsregime: `{ANCHOR_REGIME}`.")
    lines.append(f"- Datasett: `{base_count}` starttilstander og `{run_count}` underliggende dynamikk-kjoringer.")
    lines.append(f"- Holdout-oppsett: `{repeats}` stratified split med testandel `{test_frac:.2f}` per størrelse.")
    lines.append(
        "- Budsjettstigen er innen størrelse: vi scorer alle kandidater billig, men kjører full dynamikk bare på toppfraksjonen innen hver størrelse."
    )
    lines.append(
        "- Dette holder size-effekten under kontroll. Hvis vi ikke gjør det, kan en policy se god ut bare fordi den foretrekker store ensembler."
    )
    lines.append(f"- Budsjettfraksjoner: {', '.join(f'{b:.3f}' for b in budgets)}.")
    lines.append("")
    lines.append("## Hvordan metricene leses")
    lines.append("")
    lines.append("- `within_target_best_hit`: hvor ofte policyen fanger den beste testbasen innen hver størrelse.")
    lines.append("- `within_target_top_quartile_recall`: hvor stor andel av de faktisk beste kvartil-basene som blir med videre innen hver størrelse.")
    lines.append("- `within_target_selected_lift`: hvor mye bedre de utvalgte basene er enn gjennomsnittet innen samme størrelse.")
    lines.append("- `auc_*`: samlet budsjettkurve-score over hele budsjettstigen. Hoy verdi betyr at policyen holder seg nyttig over mange budsjettvalg.")
    lines.append(
        f"- `budget_to_match_full_basis_*`: minste budsjett en policy trenger for a na samme nivaa som `{REFERENCE_POLICY}` ved budsjett `{REFERENCE_BUDGET:.2f}`."
    )
    lines.append("")
    lines.append("## Startstørrelser og etikettspenn")
    lines.append("")
    lines.append("| target | bases | mean_initial | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in target_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['bases'])} | {safe_float(row['mean_initial_nodes']):.1f} | "
            f"{safe_float(row['q10_initial_nodes']):.1f} | {safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | "
            f"{safe_float(row['mean_actual_radius']):.3f} | {safe_float(row['sd_actual_radius']):.3f} |"
        )
    lines.append("")
    lines.append("## Budsjettkurver")
    lines.append("")
    lines.append("| policy | budget | within_target_best_hit | within_target_top_quartile_recall | within_target_selected_lift |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['policy_name']} | {safe_float(row['budget_frac']):.3f} | {safe_float(row['mean_within_target_best_hit']):.3f} | "
            f"{safe_float(row['mean_within_target_top_quartile_recall']):.3f} | {safe_float(row['mean_within_target_selected_lift']):.3f} |"
        )
    lines.append("")
    lines.append("## Budsjett-effektivitet")
    lines.append("")
    lines.append("| rank | policy | auc_best_hit | auc_top_quartile_recall | auc_selected_lift | budget_to_match_full_basis_hit50 | budget_to_match_full_basis_recall50 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['policy_name']} | {safe_float(row['auc_within_target_best_hit']):.3f} | "
            f"{safe_float(row['auc_within_target_top_quartile_recall']):.3f} | {safe_float(row['auc_within_target_selected_lift']):.3f} | "
            f"{safe_float(row['budget_to_match_full_basis_hit50']):.3f} | {safe_float(row['budget_to_match_full_basis_recall50']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    if summary_rows:
        best = summary_rows[0]
        compact = next(
            (
                row
                for row in summary_rows
                if str(row["policy_type"]) == "model" and int(row["feature_count"]) <= 2
            ),
            None,
        )
        full_basis = next((row for row in summary_rows if str(row["policy_name"]) == "full_basis"), None)
        if full_basis is not None:
            lines.append(
                f"- Budsjett-benchmark i denne runden er `{full_basis['policy_name']}` med auc-best-hit `{safe_float(full_basis['auc_within_target_best_hit']):.3f}`."
            )
        if compact is not None:
            lines.append(
                f"- Beste kompakte policy er `{compact['policy_name']}` med auc-best-hit `{safe_float(compact['auc_within_target_best_hit']):.3f}` og budsjett for a matche `full_basis@0.50` lik `{safe_float(compact['budget_to_match_full_basis_hit50']):.3f}`."
            )
            if str(compact["policy_name"]) == "spectral_only":
                lines.append(
                    "- Dette reviderer den tidligere kompakte arbeidslesningen fra v12c-v12e: i selve budsjettpolicy-oppgaven er `spectral_only` na sterkere enn `spectral_plus_dim`."
                )
        if best is not None and compact is not None and str(best["policy_name"]) != str(compact["policy_name"]):
            lines.append(
                "- Dette betyr at repoet na skiller mellom beste screening-benchmark og beste lille arbeidsbasis ogsa i en eksplisitt budsjettpolicy."
            )
        random_policy = next((row for row in summary_rows if str(row["policy_name"]) == "random_baseline"), None)
        if compact is not None and random_policy is not None:
            lines.append(
                f"- Samtidig er gevinsten smal: `{compact['policy_name']}` ligger bare moderat foran `random_baseline` pa budsjettkurve-sammendraget (`{safe_float(compact['auc_within_target_best_hit']):.3f}` mot `{safe_float(random_policy['auc_within_target_best_hit']):.3f}`), sa hovedverdien ser ut til a ligge rundt middels budsjett heller enn som en sterk kurvevid separasjon."
            )
        lines.append(
            "- Denne runden ma leses som en offline beslutningsbenchmark. Den sier noe om mulig simuleringseffektivitet, ikke om ny grunnfysikk."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    full_basis = next((row for row in summary_rows if str(row["policy_name"]) == "full_basis"), None)
    compact = next(
        (
            row
            for row in summary_rows
            if str(row["policy_type"]) == "model" and int(row["feature_count"]) <= 2
        ),
        None,
    )
    return "\n".join(
        [
            "# v0.12f for ikke-spesialister",
            "",
            "Denne runden tester om vi kan spare mange dyre simulasjoner ved a bruke en enkel geometrioppskrift til a velge hvilke starttilstander som er verdt a folge opp.",
            "",
            f"- Beste fulle screeningbenchmark er `{full_basis['policy_name']}`." if full_basis else "- Ingen klar full benchmark.",
            f"- Beste lille arbeidsbasis er `{compact['policy_name']}`." if compact else "- Ingen klar kompakt basis.",
            "",
        ]
    )


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12f operativ anbefaling", ""]
    full_basis = next((row for row in summary_rows if str(row["policy_name"]) == "full_basis"), None)
    compact = next(
        (
            row
            for row in summary_rows
            if str(row["policy_type"]) == "model" and int(row["feature_count"]) <= 2
        ),
        None,
    )
    if full_basis is None or compact is None:
        lines.append("v12f ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append(
        f"Bruk `{full_basis['policy_name']}` som budsjettbenchmark og `{compact['policy_name']}` som kompakt arbeidspolicy. Hvis vi trenger den sterkeste offline screeningkurven, holder `full_basis` seg som referanse."
    )
    lines.append(
        f"Hvis vi trenger en enklere policy, er `{compact['policy_name']}` fortsatt den riktige lille kandidaten. Den ma leses mot budsjett-tallene: `budget_to_match_full_basis_hit50 = {safe_float(compact['budget_to_match_full_basis_hit50']):.3f}` og `budget_to_match_full_basis_recall50 = {safe_float(compact['budget_to_match_full_basis_recall50']):.3f}`."
    )
    lines.append(
        "Denne anbefalingen er bevisst forsiktig. `spectral_only` slar `spectral_plus_dim` i denne policy-oppgaven, men curve-wide ligger den fortsatt naert random-baseline og bor derfor behandles som en lovende, men ikke endelig screeningregel."
    )
    lines.append(
        "Neste naturlige steg er a teste denne kompakte policyen i en enda mer direkte kandidatpipeline: behold bare topp-fraksjonen og mael faktisk hvor mange oppfolgingskjoringer vi unngar ved samme eller nesten samme treffrate."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12f budget-aware screening")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=12)
    ap.add_argument("--run-seeds", type=int, default=6)
    ap.add_argument("--screening-repeats", type=int, default=60)
    ap.add_argument("--test-frac", type=float, default=0.50)
    ap.add_argument("--screening-seed", type=int, default=12061)
    ap.add_argument("--budgets", default="0.1666667,0.3333333,0.5,0.6666667,0.8333333")
    ap.add_argument("--output-prefix", default="Documentation/v12f_budget")
    ap.add_argument("--report-md", default="Documentation/v12f_budget_screening.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12f.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12f_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    budgets = [float(x) for x in args.budgets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidate = fixed_candidate()
    growth_seeds = [41001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [22101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12f] regime={regime.name} targets={targets} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12f] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    print("[v12f] bases done")

    print("[v12f] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows([candidate], ensembles, base_states, growth_seeds, run_offsets, regime.name)
    print(f"[v12f] runs done: {len(raw_run_rows)} rows")

    base_level = v12e.build_base_level_rows(base_rows, raw_run_rows)
    target_rows = target_summary(base_rows, base_level)
    policy_rows = budget_policy_rows(
        base_level,
        repeats=args.screening_repeats,
        test_frac=args.test_frac,
        seed=args.screening_seed,
        budgets=budgets,
    )
    aggregate_rows = aggregate_budget_rows(policy_rows)
    summary_rows = policy_summary_rows(aggregate_rows)

    prefix = args.output_prefix
    print("[v12f] writing outputs...")
    write_csv(f"{prefix}_base_rows.csv", base_level)
    write_csv(f"{prefix}_target_summary.csv", target_rows)
    write_csv(f"{prefix}_policy_rows.csv", policy_rows)
    write_csv(f"{prefix}_aggregate.csv", aggregate_rows)
    write_csv(f"{prefix}_summary.csv", summary_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                target_rows,
                aggregate_rows,
                summary_rows,
                base_count=len(base_level),
                run_count=len(raw_run_rows),
                repeats=args.screening_repeats,
                test_frac=args.test_frac,
                budgets=budgets,
            ),
        ),
        (args.lay_md, build_lay_summary(summary_rows)),
        (args.recommendation_md, build_recommendation(summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12f] done")


if __name__ == "__main__":
    main()
