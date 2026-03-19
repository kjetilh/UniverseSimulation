#!/usr/bin/env python3
"""v0.11e deeper binary resolution after the split v11d frontier.

This follow-up does not reopen the broader local triad axis. It uses the
resolved-to-unresolved transition in v11d as ground truth and spends more of
the runtime budget on the narrow operational contest:

- band_zero_del
- bridge_00075_0000

The purpose is to decide whether the slight raw/CI edge for band_zero_del or
the slight pairwise/focused edge for bridge_00075_0000 is the more stable
reading under deeper replication, while keeping the model and score machinery
fixed.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v11c_binary_bridge_vs_band as v11c
import relational_universe_v11d_local_triad_refinement as v11d


def binary_candidates() -> List[Any]:
    return [
        v11d.named_candidate("band_zero_del", 0.0000),
        v11d.named_candidate("bridge_00075_0000", 0.00075),
    ]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v11d.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v11d.write_csv(path, rows)


def verify_v11d_state() -> Dict[str, Any]:
    candidate_rows = v11c.read_csv_rows("Documentation/v11d_local_triad_refinement_candidate_summary.csv")
    pair_rows = v11c.read_csv_rows("Documentation/v11d_local_triad_refinement_pairwise.csv")
    target_rows = v11c.read_csv_rows("Documentation/v11d_local_triad_refinement_target_summary.csv")
    pair_lookup = v11c.pair_lookup(pair_rows)

    raw = max(candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    ci_low = max(candidate_rows, key=lambda row: safe_float(row["ci_low_mean_composite"], -1.0))
    pairwise = max(candidate_rows, key=lambda row: safe_float(row["pairwise_mean_win_prob"], -1.0))
    focused = max(candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    size_clean = int(all(int(row["separated_from_prev"]) == 1 for row in target_rows))
    supported = int(
        str(raw["candidate_name"]) == "band_zero_del"
        and str(ci_low["candidate_name"]) == "band_zero_del"
        and str(pairwise["candidate_name"]) == "bridge_00075_0000"
        and str(focused["candidate_name"]) == "bridge_00075_0000"
        and bool(size_clean)
    )
    return {
        "supported": supported,
        "raw_winner": str(raw["candidate_name"]),
        "ci_low_winner": str(ci_low["candidate_name"]),
        "pairwise_winner": str(pairwise["candidate_name"]),
        "focused_winner": str(focused["candidate_name"]),
        "size_clean": size_clean,
        "p_bridge0075_gt_band": pair_lookup.get(("bridge_00075_0000", "band_zero_del"), float("nan")),
        "p_band_gt_bridge0075": pair_lookup.get(("band_zero_del", "bridge_00075_0000"), float("nan")),
        "note": (
            "On-disk v11d files support a narrow unresolved split between band_zero_del and bridge_00075_0000."
            if supported
            else "On-disk v11d files do not cleanly support the expected band-vs-bridge0075 split."
        ),
    }


def resolution_verdict(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]], target_summary: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    raw = max(candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    ci_low = max(candidate_rows, key=lambda row: safe_float(row["ci_low_mean_composite"], -1.0))
    pairwise = max(candidate_rows, key=lambda row: safe_float(row["pairwise_mean_win_prob"], -1.0))
    focused = max(candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    raw_name = str(raw["candidate_name"])
    ci_name = str(ci_low["candidate_name"])
    pair_name = str(pairwise["candidate_name"])
    focused_name = str(focused["candidate_name"])
    lookup = v11c.pair_lookup(pair_rows)
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)

    if not size_clean:
        status = "unresolved"
        note = "Target summary viser ikke ren separasjon av startstorrelser; dette ma tolkes som generatoradvarsel."
    else:
        other = "bridge_00075_0000" if raw_name == "band_zero_del" else "band_zero_del"
        p_raw_gt_other = lookup.get((raw_name, other), float("nan"))
        p_other_gt_raw = lookup.get((other, raw_name), float("nan"))
        if raw_name == ci_name == pair_name and p_raw_gt_other >= 0.65:
            status = "resolved"
            note = f"`{raw_name}` vinner raw, CI-low og pairwise med tydelig margin mot `{other}`."
        else:
            status = "unresolved"
            note = (
                f"Raw/CI peker mot `{raw_name}`, pairwise peker mot `{pair_name}`, "
                f"og duellen er fortsatt for tett: P({raw_name} > {other}) = {p_raw_gt_other:.3f}, "
                f"P({other} > {raw_name}) = {p_other_gt_raw:.3f}."
            )
    return {
        "status": status,
        "raw_winner": raw_name,
        "ci_low_winner": ci_name,
        "pairwise_winner": pair_name,
        "focused_winner": focused_name,
        "focused_split": int(focused_name != raw_name),
        "size_clean": int(bool(size_clean)),
        "p_band_gt_bridge0075": lookup.get(("band_zero_del", "bridge_00075_0000"), float("nan")),
        "p_bridge0075_gt_band": lookup.get(("bridge_00075_0000", "band_zero_del"), float("nan")),
        "note": note,
    }


def build_markdown(
    hypothesis: Mapping[str, Any],
    target_summary: Sequence[Dict[str, Any]],
    candidate_rows: Sequence[Dict[str, Any]],
    pair_rows: Sequence[Dict[str, Any]],
    verdict: Mapping[str, Any],
) -> str:
    row_by_name = {str(row["candidate_name"]): row for row in candidate_rows}
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.11e: band_zero_del vs bridge_00075_0000")
    lines.append("")
    lines.append("## Repo-verifisert utgangspunkt")
    lines.append("")
    lines.append(f"- {hypothesis['note']}")
    lines.append(f"- v11d raw-vinner: `{hypothesis['raw_winner']}`.")
    lines.append(f"- v11d CI-low-vinner: `{hypothesis['ci_low_winner']}`.")
    lines.append(f"- v11d pairwise-vinner: `{hypothesis['pairwise_winner']}`.")
    lines.append(f"- v11d focused-vinner: `{hypothesis['focused_winner']}`.")
    lines.append(
        f"- v11d head-to-head: `P(bridge_00075_0000 > band_zero_del) = {safe_float(hypothesis['p_bridge0075_gt_band']):.3f}`, "
        f"`P(band_zero_del > bridge_00075_0000) = {safe_float(hypothesis['p_band_gt_bridge0075']):.3f}`."
    )
    lines.append("")
    lines.append("## Eksperimentdesign")
    lines.append("")
    lines.append("Denne runden holder modellen og scoringen fast og bruker mer replikeringsbudsjett pa den smale binare duellen.")
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
    lines.append("## Kandidatsammendrag")
    lines.append("")
    lines.append("| candidate | focused_score | mean_composite | CI low | top_prob | pairwise_mean | pairwise_min | alpha_large | alpha_jump |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for name in ["band_zero_del", "bridge_00075_0000"]:
        row = row_by_name[name]
        lines.append(
            f"| {name} | {safe_float(row['focused_score']):.3f} | {safe_float(row['mean_composite']):.3f} | "
            f"{safe_float(row['ci_low_mean_composite']):.3f} | {safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{safe_float(row['pairwise_mean_win_prob']):.3f} | {safe_float(row['pairwise_min_win_prob']):.3f} | "
            f"{safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} |"
        )
    lines.append("")
    lines.append("## Pairwise")
    lines.append("")
    lines.append("| a | b | P(a > b) |")
    lines.append("| --- | --- | --- |")
    for row in pair_rows:
        lines.append(f"| {row['candidate_a']} | {row['candidate_b']} | {safe_float(row['prob_a_gt_b_mean_composite']):.3f} |")
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    lines.append(f"1. Høyest raw `mean_composite`: `{verdict['raw_winner']}`.")
    lines.append(f"2. Sterkest `CI low`: `{verdict['ci_low_winner']}`.")
    lines.append(f"3. Sterkest pairwise-bootstrap: `{verdict['pairwise_winner']}`.")
    lines.append(f"4. Beste focused/local score: `{verdict['focused_winner']}`.")
    lines.append(f"5. Status: `{verdict['status']}`.")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(f"- {verdict['note']}")
    if int(verdict["focused_split"]):
        lines.append("- Focused-score og operativ frontier peker ikke samme vei i denne duellen.")
    else:
        lines.append("- Focused-score er ikke separat fra den operative lesningen i denne runden.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_markdown(verdict: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# v0.11e for ikke-spesialister",
            "",
            str(verdict["note"]),
            "",
            "Kort sagt: vi tester bare hvem som faktisk holder best stand mellom den ra band-kandidaten og den smale bridge-utfordreren.",
            "",
        ]
    )


def build_recommendation(verdict: Mapping[str, Any]) -> str:
    lines = ["# v0.11e operativ anbefaling", ""]
    if str(verdict["status"]) == "resolved":
        lines.append(f"Bruk `{verdict['raw_winner']}` som operativ standardkandidat videre.")
    else:
        lines.append("Hold bade `band_zero_del` og `bridge_00075_0000` apne videre; den dype binare duellen er fortsatt ikke helt ren.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.11e band-vs-bridge0075 resolution")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds", type=int, default=8)
    ap.add_argument("--bootstrap-reps", type=int, default=320)
    ap.add_argument("--output-prefix", default="Documentation/v11e")
    ap.add_argument("--report-md", default="Documentation/v11e_band_vs_bridge0075.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_11e.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_11e_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    hypothesis = verify_v11d_state()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidates = binary_candidates()
    growth_seeds = [21001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [7101 + 29 * i for i in range(args.run_seeds)]

    print(
        f"[v11e] regime={regime.name} targets={targets} candidates={[cand.name for cand in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)}"
    )
    print("[v11e] verifying live v11d state...")
    print(f"[v11e] {hypothesis['note']}")
    print("[v11e] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    print("[v11e] bases done")

    print("[v11e] collecting run rows...")
    run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    group_rows = v10e.summarize_groups(candidates, ensembles, run_rows)
    print(f"[v11e] runs done: {len(run_rows)} rows")
    print("[v11e] bootstrap...")
    ci_rows, pair_rows, top_rows = v10e.bootstrap_joint(
        candidates,
        ensembles,
        run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=77331,
    )
    candidate_rows = v11c.candidate_rows_from_group_rows(candidates, group_rows, ci_rows, top_rows)
    v11d.add_pairwise_scores(candidate_rows, pair_rows)
    verdict = resolution_verdict(candidate_rows, pair_rows, target_summary)

    print("[v11e] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_band_vs_bridge0075_base_rows.csv", base_rows)
    write_csv(f"{prefix}_band_vs_bridge0075_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_band_vs_bridge0075_candidate_summary.csv", candidate_rows)
    write_csv(f"{prefix}_band_vs_bridge0075_pairwise.csv", list(pair_rows))
    write_csv(f"{prefix}_band_vs_bridge0075_hypothesis_check.csv", [hypothesis])
    write_csv(f"{prefix}_band_vs_bridge0075_verdict.csv", [verdict])

    for path, content in [
        (args.report_md, build_markdown(hypothesis, target_summary, candidate_rows, pair_rows, verdict)),
        (args.lay_md, build_lay_markdown(verdict)),
        (args.recommendation_md, build_recommendation(verdict)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v11e] done")


if __name__ == "__main__":
    main()
