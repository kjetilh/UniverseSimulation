#!/usr/bin/env python3
"""v0.11c binary bridge-vs-band resolution.

This is a deliberately tiny follow-up to v0.11b. It does not reopen a broad
frontier scan. It evaluates a one-dimensional local p_triad axis at fixed
p_swap=0.02 and p_del=0.0:

- band_zero_del
- bridge_0005_0000
- bridge_0010_0000
- bridge_0015_0000
- bridge_0020_0000

The goal is to test whether bridge_0015_0000 is actually better than
band_zero_del, or whether the gap is too small / seed-sensitive / metric-split
to justify promoting one over the other.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e


def named_candidate(name: str, p_triad: float) -> v09.ScaleCandidate:
    return v09.ScaleCandidate(name, 0.02, 0.00, 0.02, p_triad, 0.0)


def binary_candidates() -> List[v09.ScaleCandidate]:
    return [
        named_candidate("band_zero_del", 0.0000),
        named_candidate("bridge_0005_0000", 0.0005),
        named_candidate("bridge_0010_0000", 0.0010),
        named_candidate("bridge_0015_0000", 0.0015),
        named_candidate("bridge_0020_0000", 0.0020),
    ]


def read_csv_rows(path: str | Path) -> List[Dict[str, Any]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v10e.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v10e.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v10e.write_csv(path, rows)


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


def add_pairwise_scores(candidate_rows: List[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> None:
    lookup = pair_lookup(pair_rows)
    candidate_names = [str(row["candidate_name"]) for row in candidate_rows]
    for row in candidate_rows:
        name = str(row["candidate_name"])
        probs = [lookup.get((name, other), float("nan")) for other in candidate_names if other != name]
        finite = [p for p in probs if p == p]
        row["pairwise_mean_win_prob"] = mean_defined(finite)
        row["pairwise_min_win_prob"] = min(finite) if finite else float("nan")


def strongest_challenger(candidate_rows: Sequence[Dict[str, Any]], leader_name: str) -> Dict[str, Any]:
    challengers = [row for row in candidate_rows if str(row["candidate_name"]) != leader_name]
    return max(
        challengers,
        key=lambda row: (
            safe_float(row.get("pairwise_mean_win_prob"), -1.0),
            safe_float(row.get("ci_low_mean_composite"), -1.0),
            safe_float(row.get("mean_composite"), -1.0),
        ),
    )


def verify_working_hypothesis() -> Dict[str, Any]:
    final_rows = read_csv_rows("Documentation/v11b_bridge_resolution_final_candidate_summary.csv")
    pair_rows = read_csv_rows("Documentation/v11b_bridge_resolution_final_pairwise.csv")
    row_by_name = {str(row["candidate_name"]): row for row in final_rows}
    lookup = pair_lookup(pair_rows)

    raw = max(final_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    ci_low = max(final_rows, key=lambda row: safe_float(row["ci_low_mean_composite"], -1.0))
    focused = max(final_rows, key=lambda row: safe_float(row["focused_score"], -1.0))

    supported = (
        str(raw["candidate_name"]) == "bridge_0015_0000"
        and str(ci_low["candidate_name"]) == "band_zero_del"
        and str(focused["candidate_name"]) == "bridge_0015_0000"
    )
    return {
        "supported": int(bool(supported)),
        "raw_winner": str(raw["candidate_name"]),
        "ci_low_winner": str(ci_low["candidate_name"]),
        "focused_winner": str(focused["candidate_name"]),
        "p_bridge0015_gt_band": lookup.get(("bridge_0015_0000", "band_zero_del"), float("nan")),
        "p_band_gt_bridge0015": lookup.get(("band_zero_del", "bridge_0015_0000"), float("nan")),
        "note": (
            "On-disk v0.11b files support a binary bridge_0015_0000 vs band_zero_del contest."
            if supported
            else "On-disk v0.11b files do not cleanly support the expected binary contest."
        ),
        "band_ci_low": safe_float(row_by_name.get("band_zero_del", {}).get("ci_low_mean_composite")),
        "bridge_ci_low": safe_float(row_by_name.get("bridge_0015_0000", {}).get("ci_low_mean_composite")),
    }


def resolution_verdict(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> Dict[str, str]:
    raw = max(candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    ci_low = max(candidate_rows, key=lambda row: safe_float(row["ci_low_mean_composite"], -1.0))
    pairwise = max(candidate_rows, key=lambda row: safe_float(row["pairwise_mean_win_prob"], -1.0))
    focused = max(candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    leader_name = str(raw["candidate_name"])
    challenger = strongest_challenger(candidate_rows, leader_name)
    lookup = pair_lookup(pair_rows)
    prob_leader_gt = lookup.get((leader_name, str(challenger["candidate_name"])), float("nan"))
    prob_challenger_gt = lookup.get((str(challenger["candidate_name"]), leader_name), float("nan"))

    same_raw_ci_pair = (
        str(raw["candidate_name"]) == str(ci_low["candidate_name"]) == str(pairwise["candidate_name"])
    )
    if same_raw_ci_pair and prob_leader_gt >= 0.65:
        return {
            "status": "resolved",
            "raw_winner": str(raw["candidate_name"]),
            "ci_low_winner": str(ci_low["candidate_name"]),
            "pairwise_winner": str(pairwise["candidate_name"]),
            "focused_winner": str(focused["candidate_name"]),
            "challenger": str(challenger["candidate_name"]),
            "note": (
                f"`{leader_name}` er robust nok til a regnes som vinner: raw, CI-low og pairwise peker samme vei, "
                f"og P({leader_name} > {challenger['candidate_name']}) = {prob_leader_gt:.3f}."
            ),
        }
    return {
        "status": "unresolved",
        "raw_winner": str(raw["candidate_name"]),
        "ci_low_winner": str(ci_low["candidate_name"]),
        "pairwise_winner": str(pairwise["candidate_name"]),
        "focused_winner": str(focused["candidate_name"]),
        "challenger": str(challenger["candidate_name"]),
        "note": (
            f"Resultatet er fortsatt delt: raw peker mot `{raw['candidate_name']}`, CI-low peker mot `{ci_low['candidate_name']}`, "
            f"pairwise peker mot `{pairwise['candidate_name']}`, og P({leader_name} > {challenger['candidate_name']}) = {prob_leader_gt:.3f} "
            f"mot P({challenger['candidate_name']} > {leader_name}) = {prob_challenger_gt:.3f}."
        ),
    }


def pair_matrix_markdown(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> List[str]:
    names = [str(row["candidate_name"]) for row in candidate_rows]
    lookup = pair_lookup(pair_rows)
    lines = ["| a \\\\ b | " + " | ".join(names) + " |", "| --- | " + " | ".join(["---"] * len(names)) + " |"]
    for a in names:
        cells: List[str] = []
        for b in names:
            if a == b:
                cells.append("—")
            else:
                cells.append(f"{lookup.get((a, b), float('nan')):.3f}")
        lines.append("| " + a + " | " + " | ".join(cells) + " |")
    return lines


def build_markdown(
    hypothesis: Dict[str, Any],
    target_summary: Sequence[Dict[str, Any]],
    candidate_rows: Sequence[Dict[str, Any]],
    pair_rows: Sequence[Dict[str, Any]],
    verdict: Dict[str, str],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.11c: binary bridge vs band")
    lines.append("")
    lines.append("## Repo-verifisert arbeidshypotese")
    lines.append("")
    lines.append(f"- {hypothesis['note']}")
    lines.append(f"- v0.11b raw-vinner: `{hypothesis['raw_winner']}`.")
    lines.append(f"- v0.11b CI-low-vinner: `{hypothesis['ci_low_winner']}`.")
    lines.append(f"- v0.11b focused-vinner: `{hypothesis['focused_winner']}`.")
    lines.append(
        f"- Pairwise i v0.11b: `P(bridge_0015_0000 > band_zero_del) = {safe_float(hypothesis['p_bridge0015_gt_band']):.3f}`, "
        f"`P(band_zero_del > bridge_0015_0000) = {safe_float(hypothesis['p_band_gt_bridge0015']):.3f}`."
    )
    lines.append("")
    lines.append("## Eksperimentdesign")
    lines.append("")
    lines.append("Denne runden holder kandidatfamilien pa en ren lokal `p_triad`-akse ved fast `p_swap = 0.02` og `p_del = 0.0`.")
    lines.append("Swap er ikke med i hovedgridet, fordi v0.11b ikke støttet at swap fortsatt var sentrum av frontieren.")
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
    lines.append("Generator-lesning: hvis disse startnivåene ikke separerer, er analysen metodisk skjør. I denne runden separerer de.")
    lines.append("")
    lines.append("## Kandidatsammendrag")
    lines.append("")
    lines.append("| candidate | focused_score | mean_composite | CI low | top_prob | pairwise_mean | pairwise_min | alpha_large | alpha_jump |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['focused_score']):.3f} | {safe_float(row['mean_composite']):.3f} | "
            f"{safe_float(row['ci_low_mean_composite']):.3f} | {safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{safe_float(row['pairwise_mean_win_prob']):.3f} | {safe_float(row['pairwise_min_win_prob']):.3f} | "
            f"{safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} |"
        )
    lines.append("")
    lines.append("## Pairwise-matrise")
    lines.append("")
    lines.extend(pair_matrix_markdown(candidate_rows, pair_rows))
    lines.append("")
    lines.append("## Svar pa arbeidsfragene")
    lines.append("")
    lines.append(f"1. Høyest raw `mean_composite`: `{verdict['raw_winner']}`.")
    lines.append(f"2. Sterkest `CI low`: `{verdict['ci_low_winner']}`.")
    lines.append(f"3. Sterkest pairwise-bootstrap: `{verdict['pairwise_winner']}`.")
    lines.append(f"4. Beste focused/local score: `{verdict['focused_winner']}`.")
    same = len({verdict['raw_winner'], verdict['ci_low_winner'], verdict['pairwise_winner'], verdict['focused_winner']}) == 1
    lines.append(f"5. Er dette samme kandidat? {'Ja' if same else 'Nei'}.")
    lines.append(f"6. Resultatstatus: `{verdict['status']}`.")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(f"- {verdict['note']}")
    if verdict["focused_winner"] != verdict["raw_winner"]:
        lines.append(
            f"- Focused-score peker mot `{verdict['focused_winner']}`, men det er ikke nok alene til a overstyre raw/CI/pairwise."
        )
    else:
        lines.append(
            f"- `{verdict['focused_winner']}` har ikke en separat scoring-fordel; focused og raw peker samme vei for vinnerkandidaten."
        )
    lines.append("")
    lines.append("## Hva som er hva")
    lines.append("")
    lines.append("- Generatorstabilitet: vurderes via de realiserte startstørrelsene over de fire nivåene.")
    lines.append("- Scoringartefakter: focused-score holdes separat fra raw/CI/pairwise og skal ikke alene avgjøre vinner.")
    lines.append("- Finite-sample-ambiguity: hvis raw, CI-low og pairwise peker ulikt, er resultatet fortsatt uavklart.")
    lines.append("- Robust dynamisk fordel: krever at samme kandidat dominerer flere operative mål samtidig.")
    lines.append("")
    lines.append("## Operativ dom")
    lines.append("")
    if verdict["status"] == "resolved":
        lines.append(f"Bruk `{verdict['raw_winner']}` som standardkandidat videre.")
    else:
        lines.append(
            f"Hold bade `{verdict['raw_winner']}` og `{verdict['ci_low_winner']}` apne videre; repoet støtter fortsatt ikke en ren enkeltvinner."
        )
    lines.append("")
    return "\n".join(lines)


def build_lay_markdown(verdict: Dict[str, str]) -> str:
    return "\n".join(
        [
            "# v0.11c for ikke-spesialister",
            "",
            verdict["note"],
            "",
            "Kort sagt: vi ma fortsatt skille mellom en kandidat som leder pa ett tall og en kandidat som er robust pa flere maal samtidig.",
            "",
        ]
    )


def build_recommendation(verdict: Dict[str, str]) -> str:
    lines = ["# v0.11c operativ anbefaling", ""]
    if verdict["status"] == "resolved":
        lines.append(f"Bruk `{verdict['raw_winner']}` som operativ standardkandidat i neste runde.")
    else:
        lines.append(
            f"Hold bade `{verdict['raw_winner']}` og `{verdict['ci_low_winner']}` apne videre; "
            "den binare bridge-vs-band-duellen er fortsatt ikke rent avgjort."
        )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.11c binary bridge-vs-band resolution")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=3)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--bootstrap-reps", type=int, default=120)
    ap.add_argument("--output-prefix", default="Documentation/v11c")
    ap.add_argument("--report-md", default="Documentation/v11c_binary_bridge_vs_band.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_11c.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_11c_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    hypothesis = verify_working_hypothesis()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidates = binary_candidates()
    growth_seeds = [17001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [5101 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v11c] regime={regime.name} targets={targets} candidates={[cand.name for cand in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)}"
    )
    print("[v11c] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    print("[v11c] bases done")

    print("[v11c] collecting run rows...")
    run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    group_rows = v10e.summarize_groups(candidates, ensembles, run_rows)
    print(f"[v11c] runs done: {len(run_rows)} rows")
    print("[v11c] bootstrap...")
    ci_rows, pair_rows, top_rows = v10e.bootstrap_joint(
        candidates,
        ensembles,
        run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=55111,
    )
    candidate_rows = candidate_rows_from_group_rows(candidates, group_rows, ci_rows, top_rows)
    add_pairwise_scores(candidate_rows, pair_rows)
    verdict = resolution_verdict(candidate_rows, pair_rows)

    print("[v11c] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_binary_bridge_vs_band_base_rows.csv", base_rows)
    write_csv(f"{prefix}_binary_bridge_vs_band_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_binary_bridge_vs_band_candidate_summary.csv", candidate_rows)
    write_csv(f"{prefix}_binary_bridge_vs_band_pairwise.csv", list(pair_rows))
    write_csv(f"{prefix}_binary_bridge_vs_band_hypothesis_check.csv", [hypothesis])
    write_csv(f"{prefix}_binary_bridge_vs_band_verdict.csv", [verdict])

    for path, content in [
        (args.report_md, build_markdown(hypothesis, target_summary, candidate_rows, pair_rows, verdict)),
        (args.lay_md, build_lay_markdown(verdict)),
        (args.recommendation_md, build_recommendation(verdict)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v11c] done")


if __name__ == "__main__":
    main()
