#!/usr/bin/env python3
"""v0.11b narrow bridge-corridor resolution.

This script verifies the live local frontier state from on-disk v0.11 outputs,
then runs a tighter candidate family around the bridge corridor:

- band_zero_del as control,
- bridge_0025_0000 as the raw bridge anchor,
- swap-tilted bridge variants as focused-score candidates,
- nearby p_triad perturbations at p_del = 0.

It reports raw vs focused winners separately and allows an unresolved outcome.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e


def named_candidate(name: str, p_swap: float, p_triad: float, p_del: float = 0.0) -> v09.ScaleCandidate:
    return v09.ScaleCandidate(name, 0.02, 0.00, p_swap, p_triad, p_del)


def bridge_candidates() -> List[v09.ScaleCandidate]:
    return [
        named_candidate("band_zero_del", 0.0200, 0.0000),
        named_candidate("bridge_0015_0000", 0.0200, 0.0015),
        named_candidate("bridge_0025_0000", 0.0200, 0.0025),
        named_candidate("bridge_0035_0000", 0.0200, 0.0035),
        named_candidate("bridge_0025_0000_swap0225", 0.0225, 0.0025),
        named_candidate("bridge_0025_0000_swap025", 0.0250, 0.0025),
    ]


def candidate_lookup(candidates: Sequence[v09.ScaleCandidate]) -> Mapping[str, v09.ScaleCandidate]:
    return {cand.name: cand for cand in candidates}


def read_csv_rows(path: str | Path) -> List[Dict[str, Any]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v10e.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v10e.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v10e.write_csv(path, rows)


def verify_working_hypothesis() -> Dict[str, Any]:
    final_rows = read_csv_rows("Documentation/v11_mid_focus_frontier_resolution_final_candidate_summary.csv")
    pair_rows = read_csv_rows("Documentation/v11_mid_focus_frontier_resolution_final_pairwise.csv")
    row_by_name = {str(row["candidate_name"]): row for row in final_rows}
    pair_lookup = {
        (str(row["candidate_a"]), str(row["candidate_b"])): safe_float(row["prob_a_gt_b_mean_composite"])
        for row in pair_rows
    }

    raw = max(final_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    focused = max(final_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    bridge_beats_band = pair_lookup.get(("bridge_0025_0000", "band_zero_del"), float("nan"))
    bridge_beats_swap = pair_lookup.get(("bridge_0025_0000", "bridge_0025_0000_swap025"), float("nan"))

    supported = (
        str(raw["candidate_name"]) == "bridge_0025_0000"
        and str(focused["candidate_name"]) == "bridge_0025_0000_swap025"
        and bridge_beats_band >= 0.5
        and bridge_beats_swap >= 0.5
    )
    return {
        "supported": int(bool(supported)),
        "raw_winner": str(raw["candidate_name"]),
        "focused_winner": str(focused["candidate_name"]),
        "p_bridge_gt_band": bridge_beats_band,
        "p_bridge_gt_swap": bridge_beats_swap,
        "note": (
            "On-disk v0.11 files support the bridge-corridor reading."
            if supported
            else "On-disk v0.11 files do not fully support the bridge-corridor reading."
        ),
        "band_mean_composite": safe_float(row_by_name.get("band_zero_del", {}).get("mean_composite")),
        "bridge_mean_composite": safe_float(row_by_name.get("bridge_0025_0000", {}).get("mean_composite")),
        "swap_mean_composite": safe_float(row_by_name.get("bridge_0025_0000_swap025", {}).get("mean_composite")),
    }


def candidate_rows_from_group_rows(
    candidates: Sequence[v09.ScaleCandidate],
    group_rows: Sequence[Dict[str, Any]],
    ci_rows: Dict[str, Dict[str, float]],
    top_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    top_lookup = {str(row["candidate_name"]): row for row in top_rows}
    rows: List[Dict[str, Any]] = []
    for cand in candidates:
        row = v10e.point_candidate_summary(cand.name, group_rows)
        row.update(ci_rows[cand.name])
        row["top_prob_mean_composite"] = top_lookup[cand.name]["top_prob_mean_composite"]
        rows.append(row)
    v10e.add_focused_score(rows)
    rows.sort(key=lambda row: safe_float(row["focused_score"], -1.0), reverse=True)
    return rows


def pair_lookup(pair_rows: Sequence[Dict[str, Any]]) -> Dict[Tuple[str, str], float]:
    return {
        (str(row["candidate_a"]), str(row["candidate_b"])): safe_float(row["prob_a_gt_b_mean_composite"])
        for row in pair_rows
    }


def finalist_names_from_broad_rows(candidate_rows: Sequence[Dict[str, Any]]) -> List[str]:
    raw_winner = max(candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))["candidate_name"]
    focused_winner = max(candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))["candidate_name"]
    wanted = [
        "band_zero_del",
        "bridge_0025_0000",
        "bridge_0025_0000_swap025",
        str(raw_winner),
        str(focused_winner),
    ]
    seen: set[str] = set()
    return [name for name in wanted if not (name in seen or seen.add(name))]


def credibility_note(raw_row: Dict[str, Any], focused_row: Dict[str, Any], final_pair_rows: Sequence[Dict[str, Any]]) -> Dict[str, str]:
    raw_name = str(raw_row["candidate_name"])
    focused_name = str(focused_row["candidate_name"])
    if raw_name == focused_name:
        return {
            "status": "resolved_same_winner",
            "note": (
                f"Focused-vinneren `{focused_name}` er også råvinner; den interne raw-vs-focused-spenningen for denne kandidaten "
                "ser derfor ut til a vaere lukket."
            ),
        }

    lookup = pair_lookup(final_pair_rows)
    prob_focused_gt_raw = lookup.get((focused_name, raw_name), float("nan"))
    prob_raw_gt_focused = lookup.get((raw_name, focused_name), float("nan"))
    raw_ci = safe_float(raw_row.get("ci_low_mean_composite"))
    focused_ci = safe_float(focused_row.get("ci_low_mean_composite"))

    if prob_focused_gt_raw < 0.35 and focused_ci < raw_ci:
        return {
            "status": "focused_not_operational",
            "note": (
                f"Focused-vinneren `{focused_name}` er ikke operativt troverdig som standardkandidat i denne runden: "
                f"P({focused_name} > {raw_name}) = {prob_focused_gt_raw:.3f}, og CI-low er svakere."
            ),
        }
    if 0.35 <= prob_focused_gt_raw <= 0.65:
        return {
            "status": "unresolved",
            "note": (
                f"Spenningen mellom `{raw_name}` og `{focused_name}` er fortsatt uavklart: "
                f"P({focused_name} > {raw_name}) = {prob_focused_gt_raw:.3f}."
            ),
        }
    if prob_focused_gt_raw > 0.65:
        return {
            "status": "focused_still_credible",
            "note": (
                f"Focused-vinneren `{focused_name}` er fortsatt operativt troverdig i denne runden: "
                f"P({focused_name} > {raw_name}) = {prob_focused_gt_raw:.3f}, "
                f"mot P({raw_name} > {focused_name}) = {prob_raw_gt_focused:.3f}."
            ),
        }
    return {
        "status": "focused_secondary",
        "note": f"`{focused_name}` ser mest ut som en focused-/regulariseringskontroll, ikke som ny standardkandidat.",
    }


def strongest_challenger(final_candidate_rows: Sequence[Dict[str, Any]], raw_name: str) -> Dict[str, Any]:
    challengers = [row for row in final_candidate_rows if str(row["candidate_name"]) != raw_name]
    return max(
        challengers,
        key=lambda row: (
            safe_float(row.get("top_prob_mean_composite"), -1.0),
            safe_float(row.get("mean_composite"), -1.0),
            safe_float(row.get("ci_low_mean_composite"), -1.0),
        ),
    )


def resolution_note(
    raw_row: Dict[str, Any],
    challenger_row: Dict[str, Any],
    final_pair_rows: Sequence[Dict[str, Any]],
) -> Dict[str, str]:
    raw_name = str(raw_row["candidate_name"])
    challenger_name = str(challenger_row["candidate_name"])
    lookup = pair_lookup(final_pair_rows)
    prob_raw_gt = lookup.get((raw_name, challenger_name), float("nan"))
    prob_challenger_gt = lookup.get((challenger_name, raw_name), float("nan"))
    raw_top = safe_float(raw_row.get("top_prob_mean_composite"))
    challenger_top = safe_float(challenger_row.get("top_prob_mean_composite"))
    raw_ci = safe_float(raw_row.get("ci_low_mean_composite"))
    challenger_ci = safe_float(challenger_row.get("ci_low_mean_composite"))

    if prob_raw_gt >= 0.65 and raw_top >= challenger_top + 0.10 and raw_ci >= challenger_ci:
        return {
            "status": "resolved",
            "note": (
                f"`{raw_name}` ser ut til a vaere reelt foran `{challenger_name}`: "
                f"P({raw_name} > {challenger_name}) = {prob_raw_gt:.3f}, "
                f"top_prob = {raw_top:.3f} mot {challenger_top:.3f}."
            ),
        }
    return {
        "status": "unresolved",
        "note": (
            f"Bro-korridoren er fortsatt uavklart mellom `{raw_name}` og `{challenger_name}`: "
            f"P({raw_name} > {challenger_name}) = {prob_raw_gt:.3f}, "
            f"P({challenger_name} > {raw_name}) = {prob_challenger_gt:.3f}, "
            f"CI-low = {raw_ci:.3f} mot {challenger_ci:.3f}, "
            f"top_prob = {raw_top:.3f} mot {challenger_top:.3f}."
        ),
    }


def pair_matrix_markdown(finalist_names: Sequence[str], final_pair_rows: Sequence[Dict[str, Any]]) -> List[str]:
    lookup = pair_lookup(final_pair_rows)
    lines = ["| a \\\\ b | " + " | ".join(finalist_names) + " |", "| --- | " + " | ".join(["---"] * len(finalist_names)) + " |"]
    for a in finalist_names:
        cells: List[str] = []
        for b in finalist_names:
            if a == b:
                cells.append("—")
            else:
                cells.append(f"{lookup.get((a, b), float('nan')):.3f}")
        lines.append("| " + a + " | " + " | ".join(cells) + " |")
    return lines


def build_markdown(
    hypothesis: Dict[str, Any],
    target_summary: Sequence[Dict[str, Any]],
    broad_candidate_rows: Sequence[Dict[str, Any]],
    final_candidate_rows: Sequence[Dict[str, Any]],
    final_pair_rows: Sequence[Dict[str, Any]],
    credibility: Dict[str, str],
    resolution: Dict[str, str],
) -> str:
    raw = max(final_candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    focused = max(final_candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    challenger = strongest_challenger(final_candidate_rows, str(raw["candidate_name"]))
    finalists = [str(row["candidate_name"]) for row in final_candidate_rows]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.11b: bridge-corridor resolution")
    lines.append("")
    lines.append("## Repo-verifisert arbeidshypotese")
    lines.append("")
    lines.append(f"- {hypothesis['note']}")
    lines.append(f"- Tidligere lokal råvinner: `{hypothesis['raw_winner']}`.")
    lines.append(f"- Tidligere lokal focused-vinner: `{hypothesis['focused_winner']}`.")
    lines.append(
        f"- Pairwise fra v0.11 mid focus: `P(bridge_0025_0000 > band_zero_del) = {safe_float(hypothesis['p_bridge_gt_band']):.3f}`, "
        f"`P(bridge_0025_0000 > bridge_0025_0000_swap025) = {safe_float(hypothesis['p_bridge_gt_swap']):.3f}`."
    )
    lines.append("")
    lines.append("## Eksperimentdesign")
    lines.append("")
    lines.append("Denne runden bruker et smalt, lokalt bridge-grid med `p_del = 0` overalt.")
    lines.append("Kandidatene varierer bare `p_triad` rundt `0.0025` og `p_swap` rundt `0.020-0.025`.")
    lines.append("`band_zero_del` beholdes som kontroll, ikke som forhåndsantatt vinner.")
    lines.append("")
    lines.append("## Realiserte startstørrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | {safe_float(row['q10_initial_nodes']):.1f} | "
            f"{safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | "
            f"{safe_float(row['mean_initial_tokens']):.1f} | {safe_float(row['mean_initial_beta1']):.1f} | {safe_float(row['mean_initial_triangles']):.1f} |"
        )
    lines.append("")
    lines.append("Generator-lesning: dette er metodisk input, ikke dynamisk resultat. Hvis `separated_from_prev` faller, er det et generatorproblem.")
    lines.append("")
    lines.append("## Broad-runde")
    lines.append("")
    lines.append("| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(broad_candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['focused_score']):.3f} | {safe_float(row['mean_composite']):.3f} | "
            f"{safe_float(row['ci_low_mean_composite']):.3f} | {safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} | "
            f"{safe_float(row['linear_margin']):.3f} | {safe_float(row['quasi_large']):.3f} |"
        )
    lines.append("")
    lines.append("## Finalister")
    lines.append("")
    lines.append("| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(final_candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['focused_score']):.3f} | {safe_float(row['mean_composite']):.3f} | "
            f"{safe_float(row['ci_low_mean_composite']):.3f} | {safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} | "
            f"{safe_float(row['linear_margin']):.3f} | {safe_float(row['quasi_large']):.3f} |"
        )
    lines.append("")
    lines.append("## Pairwise-matrise blant finalistene")
    lines.append("")
    lines.extend(pair_matrix_markdown(finalists, final_pair_rows))
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(f"- Råvinner: `{raw['candidate_name']}`.")
    lines.append(f"- Focused-vinner: `{focused['candidate_name']}`.")
    lines.append(f"- {credibility['note']}")
    lines.append(f"- {resolution['note']}")
    lines.append("")
    lines.append("## Svar pa arbeidsfragene")
    lines.append("")
    if resolution["status"] == "resolved":
        lines.append(f"1. Beste operative default er forelopig `{raw['candidate_name']}`.")
    else:
        lines.append(
            f"1. Beste operative default er ikke rent avgjort; `{raw['candidate_name']}` leder pa mean_composite, "
            f"men `{challenger['candidate_name']}` henger fortsatt tett pa."
        )
    if credibility["status"] in {"focused_not_operational", "focused_secondary"}:
        lines.append(f"2. `{focused['candidate_name']}` har ikke lenger en meningsfull separat fordel utover scoring-profilen.")
        lines.append("3. Den fordelen ser ut til a vaere focused/regularisert, ikke ra-dynamisk.")
    elif credibility["status"] == "resolved_same_winner":
        lines.append(f"2. `{focused['candidate_name']}` har fordel, men det er samme kandidat som ravinneren.")
        lines.append("3. Dermed er det ikke lenger en egen raw-vs-focused-spenning for denne kandidaten.")
    else:
        lines.append(f"2. `{focused['candidate_name']}` beholder en viss fordel, men ikke nok til a bli automatisk default.")
        lines.append("3. Fordelen er fortsatt blandet og bor ikke overtolkes som ren dynamikk.")
    band_row = next(row for row in final_candidate_rows if row["candidate_name"] == "band_zero_del")
    if str(band_row["candidate_name"]) == str(challenger["candidate_name"]):
        lines.append("4. `band_zero_del` er ikke bare kontroll i denne runden; den er fortsatt en reell utfordrer.")
    else:
        lines.append("4. `band_zero_del` fungerer i hovedsak som kontroll i denne runden.")
    lines.append("")
    lines.append("## Hva som er hva")
    lines.append("")
    lines.append("- Algebraiske identiteter: ingen nye påstander her; denne runden dreier seg ikke om eksakte invariants.")
    lines.append("- Generatorartefakter: vurderes via realiserte startstørrelser og `separated_from_prev`.")
    lines.append("- Scoringartefakter: focused-score kan løfte kandidater som ikke vinner rå pairwise.")
    lines.append("- Dynamiske resultater: `mean_composite`, `CI low` og pairwise-sannsynligheter i finalen er de operative størrelsene.")
    lines.append("")
    if resolution["status"] == "unresolved":
        lines.append("## Operativ dom")
        lines.append("")
        lines.append(
            f"Denne bridge-korridoren er fortsatt uavklart. Hold bade `{raw['candidate_name']}` og "
            f"`{challenger['candidate_name']}` åpne videre."
        )
    else:
        lines.append("## Operativ dom")
        lines.append("")
        lines.append(f"Bruk `{raw['candidate_name']}` som standardkandidat videre.")
        if credibility["status"] != "resolved_same_winner":
            lines.append(f"Hold `{focused['candidate_name']}` som focused-/diagnostisk kontroll.")
    lines.append("")
    return "\n".join(lines)


def build_lay_markdown(raw: Dict[str, Any], focused: Dict[str, Any], credibility: Dict[str, str], resolution: Dict[str, str], challenger: Dict[str, Any]) -> str:
    if resolution["status"] == "unresolved":
        first_line = (
            f"Vi har ikke helt avgjort kampen mellom `{raw['candidate_name']}` og `{challenger['candidate_name']}` ennå."
        )
    else:
        first_line = f"Den beste kandidaten i denne runden er `{raw['candidate_name']}`."
    return "\n".join(
        [
            "# v0.11b for ikke-spesialister",
            "",
            first_line,
            f"Modellen som ser best ut pa focused-score er `{focused['candidate_name']}`.",
            "",
            credibility["note"],
            resolution["note"],
            "",
            "Kort sagt: vi skiller na mellom hvem som ser best ut pa ren dynamikk, og hvem som bare scorer pent i en mer regularisert lesning.",
            "",
        ]
    )


def build_recommendation(
    raw: Dict[str, Any],
    focused: Dict[str, Any],
    credibility: Dict[str, str],
    resolution: Dict[str, str],
    challenger: Dict[str, Any],
) -> str:
    lines = ["# v0.11b operativ anbefaling", ""]
    if resolution["status"] == "unresolved":
        lines.append(
            f"Hold bade `{raw['candidate_name']}` og `{challenger['candidate_name']}` apne videre; "
            "den smale bridge-korridoren er fortsatt ikke rent avgjort."
        )
    else:
        lines.append(f"Bruk `{raw['candidate_name']}` som operativ standardkandidat i neste runde.")
        if credibility["status"] != "resolved_same_winner":
            lines.append(f"Behold `{focused['candidate_name']}` som focused-/diagnostisk kontroll.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.11b bridge corridor resolution")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=2)
    ap.add_argument("--run-seeds-broad", type=int, default=2)
    ap.add_argument("--run-seeds-final", type=int, default=4)
    ap.add_argument("--bootstrap-reps", type=int, default=80)
    ap.add_argument("--output-prefix", default="Documentation/v11b")
    ap.add_argument("--report-md", default="Documentation/v11b_bridge_resolution.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_11b.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_11b_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    hypothesis = verify_working_hypothesis()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidates = bridge_candidates()
    candidates_by_name = candidate_lookup(candidates)

    growth_seeds = [15001 + 23 * i for i in range(args.growth_seeds)]
    broad_offsets = [4101 + 31 * i for i in range(args.run_seeds_broad)]
    final_offsets = [4101 + 31 * i for i in range(args.run_seeds_final)]

    print(
        f"[v11b] regime={regime.name} targets={targets} candidates={[cand.name for cand in candidates]} "
        f"growth={len(growth_seeds)} broad={len(broad_offsets)} final={len(final_offsets)}"
    )
    print("[v11b] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    print("[v11b] bases done")

    print("[v11b] broad scan runs...")
    broad_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, broad_offsets, regime.name)
    broad_group_rows = v10e.summarize_groups(candidates, ensembles, broad_run_rows)
    print(f"[v11b] broad runs done: {len(broad_run_rows)} rows")
    print("[v11b] broad bootstrap...")
    broad_ci_rows, broad_pair_rows, broad_top_rows = v10e.bootstrap_joint(
        candidates,
        ensembles,
        broad_run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=43111,
    )
    broad_candidate_rows = candidate_rows_from_group_rows(candidates, broad_group_rows, broad_ci_rows, broad_top_rows)

    finalist_names = finalist_names_from_broad_rows(broad_candidate_rows)
    finalists = [candidates_by_name[name] for name in finalist_names]
    print(f"[v11b] finalists: {finalist_names}")

    final_run_rows = [row for row in broad_run_rows if str(row["candidate_name"]) in finalist_names]
    extra_offsets = [off for off in final_offsets if off not in broad_offsets]
    if extra_offsets:
        print("[v11b] finalist extra runs...")
        final_run_rows.extend(v10e.collect_run_rows(finalists, ensembles, base_states, growth_seeds, extra_offsets, regime.name))
    final_group_rows = v10e.summarize_groups(finalists, ensembles, final_run_rows)
    print(f"[v11b] finalist rows now: {len(final_run_rows)}")
    print("[v11b] finalist bootstrap...")
    final_ci_rows, final_pair_rows, final_top_rows = v10e.bootstrap_joint(
        finalists,
        ensembles,
        final_run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=43221,
    )
    final_candidate_rows = candidate_rows_from_group_rows(finalists, final_group_rows, final_ci_rows, final_top_rows)
    raw_row = max(final_candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    focused_row = max(final_candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    challenger_row = strongest_challenger(final_candidate_rows, str(raw_row["candidate_name"]))
    credibility = credibility_note(raw_row, focused_row, final_pair_rows)
    resolution = resolution_note(raw_row, challenger_row, final_pair_rows)

    print("[v11b] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_bridge_resolution_base_rows.csv", base_rows)
    write_csv(f"{prefix}_bridge_resolution_broad_candidate_summary.csv", broad_candidate_rows)
    write_csv(f"{prefix}_bridge_resolution_broad_pairwise.csv", broad_pair_rows)
    write_csv(f"{prefix}_bridge_resolution_final_candidate_summary.csv", final_candidate_rows)
    write_csv(f"{prefix}_bridge_resolution_final_pairwise.csv", final_pair_rows)
    write_csv(f"{prefix}_bridge_resolution_hypothesis_check.csv", [hypothesis])

    for path, content in [
        (args.report_md, build_markdown(hypothesis, target_summary, broad_candidate_rows, final_candidate_rows, final_pair_rows, credibility, resolution)),
        (args.lay_md, build_lay_markdown(raw_row, focused_row, credibility, resolution, challenger_row)),
        (args.recommendation_md, build_recommendation(raw_row, focused_row, credibility, resolution, challenger_row)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v11b] done")


if __name__ == "__main__":
    main()
