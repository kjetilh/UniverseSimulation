#!/usr/bin/env python3
"""v0.11d local triad refinement around the live v11c frontier.

This is a narrow follow-up to v0.11c. It keeps the model class and the scoring
machinery fixed, and only refines the local p_triad axis at

- p_swap = 0.02
- p_del = 0.0

The goal is to test whether bridge_0010_0000 is a real local optimum, or
whether it is only the best point on a still-too-coarse local grid.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v11c_binary_bridge_vs_band as v11c


FIXED_P_SWAP = 0.02
FIXED_P_DEL = 0.0


def named_candidate(name: str, p_triad: float) -> v09.ScaleCandidate:
    return v09.ScaleCandidate(name, 0.02, 0.00, FIXED_P_SWAP, p_triad, FIXED_P_DEL)


def local_refinement_candidates(include_diagnostic_0020: bool = False) -> List[v09.ScaleCandidate]:
    candidates = [
        named_candidate("band_zero_del", 0.0000),
        named_candidate("bridge_0005_0000", 0.0005),
        named_candidate("bridge_00075_0000", 0.00075),
        named_candidate("bridge_0010_0000", 0.0010),
        named_candidate("bridge_00125_0000", 0.00125),
        named_candidate("bridge_0015_0000", 0.0015),
    ]
    if include_diagnostic_0020:
        candidates.append(named_candidate("bridge_0020_0000", 0.0020))
    return candidates


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v11c.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v11c.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v11c.write_csv(path, rows)


def add_pairwise_scores(candidate_rows: List[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> None:
    v11c.add_pairwise_scores(candidate_rows, pair_rows)


def verify_live_state() -> Dict[str, Any]:
    candidate_rows = v11c.read_csv_rows("Documentation/v11c_binary_bridge_vs_band_candidate_summary.csv")
    pair_rows = v11c.read_csv_rows("Documentation/v11c_binary_bridge_vs_band_pairwise.csv")
    target_rows = v11c.read_csv_rows("Documentation/v11c_binary_bridge_vs_band_target_summary.csv")
    row_by_name = {str(row["candidate_name"]): row for row in candidate_rows}
    pair_lookup = v11c.pair_lookup(pair_rows)

    raw = max(candidate_rows, key=lambda row: safe_float(row["mean_composite"], -1.0))
    ci_low = max(candidate_rows, key=lambda row: safe_float(row["ci_low_mean_composite"], -1.0))
    pairwise = max(candidate_rows, key=lambda row: safe_float(row["pairwise_mean_win_prob"], -1.0))
    focused = max(candidate_rows, key=lambda row: safe_float(row["focused_score"], -1.0))
    size_clean = int(all(int(row["separated_from_prev"]) == 1 for row in target_rows))
    supported = int(
        str(raw["candidate_name"]) == "bridge_0010_0000"
        and str(ci_low["candidate_name"]) == "bridge_0010_0000"
        and str(pairwise["candidate_name"]) == "bridge_0010_0000"
        and str(focused["candidate_name"]) == "band_zero_del"
        and bool(size_clean)
    )
    return {
        "supported": supported,
        "raw_winner": str(raw["candidate_name"]),
        "ci_low_winner": str(ci_low["candidate_name"]),
        "pairwise_winner": str(pairwise["candidate_name"]),
        "focused_winner": str(focused["candidate_name"]),
        "size_clean": size_clean,
        "p_bridge0010_gt_band": pair_lookup.get(("bridge_0010_0000", "band_zero_del"), float("nan")),
        "p_band_gt_bridge0010": pair_lookup.get(("band_zero_del", "bridge_0010_0000"), float("nan")),
        "bridge_mean_composite": safe_float(row_by_name["bridge_0010_0000"]["mean_composite"]),
        "band_mean_composite": safe_float(row_by_name["band_zero_del"]["mean_composite"]),
        "note": (
            "On-disk v11c files support bridge_0010_0000 as the live operational frontier winner."
            if supported
            else "On-disk v11c files do not fully support the expected live frontier summary."
        ),
    }


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


def strongest_bridge_neighbor(candidate_rows: Sequence[Dict[str, Any]], leader_name: str) -> Dict[str, Any] | None:
    bridges = [
        row
        for row in candidate_rows
        if str(row["candidate_name"]).startswith("bridge_") and str(row["candidate_name"]) != leader_name
    ]
    if not bridges:
        return None
    return max(
        bridges,
        key=lambda row: (
            safe_float(row.get("pairwise_mean_win_prob"), -1.0),
            safe_float(row.get("ci_low_mean_composite"), -1.0),
            safe_float(row.get("mean_composite"), -1.0),
        ),
    )


def resolution_verdict(
    candidate_rows: Sequence[Dict[str, Any]],
    pair_rows: Sequence[Dict[str, Any]],
    target_summary: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
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

    band_name = "band_zero_del"
    local_bridge_core = {"bridge_00075_0000", "bridge_0010_0000", "bridge_00125_0000"}
    strongest_other = strongest_challenger(candidate_rows, raw_name)
    strongest_neighbor = strongest_bridge_neighbor(candidate_rows, raw_name)
    prob_raw_gt_band = lookup.get((raw_name, band_name), float("nan")) if raw_name != band_name else float("nan")
    prob_band_gt_raw = lookup.get((band_name, raw_name), float("nan")) if raw_name != band_name else float("nan")
    prob_raw_gt_neighbor = (
        lookup.get((raw_name, str(strongest_neighbor["candidate_name"])), float("nan")) if strongest_neighbor else float("nan")
    )
    prob_neighbor_gt_raw = (
        lookup.get((str(strongest_neighbor["candidate_name"]), raw_name), float("nan")) if strongest_neighbor else float("nan")
    )

    same_operational = raw_name == ci_name == pair_name
    if not size_clean:
        status = "unresolved"
        note = "Target summary viser ikke ren separasjon av startstorrelser; dette ma behandles som generatoradvarsel, ikke ny fysikk."
    elif raw_name == band_name and ci_name == band_name and pair_name == band_name:
        status = "frontier_revised"
        note = "`band_zero_del` tok tilbake raw, CI-low og pairwise under ren size-separasjon. Frontieren ma revideres."
    elif (
        same_operational
        and raw_name in local_bridge_core | {"bridge_0005_0000", "bridge_0015_0000", "bridge_0020_0000"}
        and prob_raw_gt_band == prob_raw_gt_band
        and prob_raw_gt_neighbor == prob_raw_gt_neighbor
        and prob_raw_gt_band >= 0.65
        and prob_raw_gt_neighbor >= 0.65
    ):
        status = "robust_local_optimum"
        note = (
            f"`{raw_name}` topper raw, CI-low og pairwise, og slar bade `{band_name}` og narmeste bridge-utfordrer "
            f"med tydelig pairwise-margin."
        )
    elif (
        raw_name in local_bridge_core
        and ci_name in local_bridge_core
        and pair_name in local_bridge_core
        and prob_raw_gt_band == prob_raw_gt_band
        and prob_raw_gt_band >= 0.65
    ):
        status = "local_plateau"
        note = (
            "Band taper fortsatt operativt, men de naermeste bridge-punktene er for tette til at repoet stotter ett helt rent lokalt optimum ennå."
        )
    else:
        status = "unresolved"
        note = (
            "Raw, CI-low, pairwise og/eller generator-kontroll gir ikke et rent nok bilde til a kalle dette et robust lokalt optimum."
        )

    return {
        "status": status,
        "raw_winner": raw_name,
        "ci_low_winner": ci_name,
        "pairwise_winner": pair_name,
        "focused_winner": focused_name,
        "focused_split": int(focused_name != raw_name),
        "size_clean": int(bool(size_clean)),
        "strongest_other": str(strongest_other["candidate_name"]),
        "strongest_bridge_neighbor": str(strongest_neighbor["candidate_name"]) if strongest_neighbor else "",
        "p_raw_gt_band": prob_raw_gt_band,
        "p_band_gt_raw": prob_band_gt_raw,
        "p_raw_gt_neighbor": prob_raw_gt_neighbor,
        "p_neighbor_gt_raw": prob_neighbor_gt_raw,
        "note": note,
    }


def pair_matrix_markdown(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> List[str]:
    return v11c.pair_matrix_markdown(candidate_rows, pair_rows)


def build_markdown(
    hypothesis: Mapping[str, Any],
    target_summary: Sequence[Dict[str, Any]],
    candidate_rows: Sequence[Dict[str, Any]],
    pair_rows: Sequence[Dict[str, Any]],
    verdict: Mapping[str, Any],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.11d: lokal triad-raffinement rundt bridge_0010_0000")
    lines.append("")
    lines.append("## Repo-verifisert utgangspunkt")
    lines.append("")
    lines.append(f"- {hypothesis['note']}")
    lines.append(f"- v11c raw-vinner: `{hypothesis['raw_winner']}`.")
    lines.append(f"- v11c CI-low-vinner: `{hypothesis['ci_low_winner']}`.")
    lines.append(f"- v11c pairwise-vinner: `{hypothesis['pairwise_winner']}`.")
    lines.append(f"- v11c focused-vinner: `{hypothesis['focused_winner']}`.")
    lines.append(
        f"- Pairwise i v11c: `P(bridge_0010_0000 > band_zero_del) = {safe_float(hypothesis['p_bridge0010_gt_band']):.3f}`, "
        f"`P(band_zero_del > bridge_0010_0000) = {safe_float(hypothesis['p_band_gt_bridge0010']):.3f}`."
    )
    lines.append("")
    lines.append("## Eksperimentdesign")
    lines.append("")
    lines.append(
        "Denne runden holder modellen fast og raffinerer bare den lokale `p_triad`-aksen ved fast "
        f"`p_swap = {FIXED_P_SWAP:.2f}` og `p_del = {FIXED_P_DEL:.1f}`."
    )
    lines.append("Kandidatsettet er smalt for a bruke budsjettet pa diskriminering, ikke pa bredde.")
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
    lines.append("Generator-lesning: hvis disse startnivåene ikke separerer, er frontier-lesningen metodisk skjør.")
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
        lines.append(
            f"- Focused-score peker fortsatt mot `{verdict['focused_winner']}`, men det avgjor ikke frontier alene hvis raw/CI/pairwise peker et annet sted."
        )
    else:
        lines.append("- Focused-score er ikke separat fra den operative vinnerlesningen i denne runden.")
    lines.append("")
    lines.append("## Hva som er hva")
    lines.append("")
    lines.append("- Algebraiske identiteter: ikke det som avgjor frontieren her.")
    lines.append("- Generatorartefakter: vurderes via target summary; hvis separasjonen bryter sammen, ma frontier-tolkningen holdes tilbake.")
    lines.append("- Scoringartefakter: focused-score holdes separat fra raw/CI/pairwise og kan ikke alene avgjore standardkandidat.")
    lines.append("- Dynamiske resultater: raw score, CI-low og pairwise under ren size-separasjon er den operative kjernen.")
    lines.append("")
    lines.append("## Operativ dom")
    lines.append("")
    if verdict["status"] == "robust_local_optimum":
        lines.append(f"Bruk `{verdict['raw_winner']}` som operativ standardkandidat videre.")
    elif verdict["status"] == "local_plateau":
        lines.append(
            f"Hold `{verdict['raw_winner']}` og de naermeste bridge-naboene apne videre; repoet stotter et lokalt plateau mer enn ett helt rent optimum."
        )
    elif verdict["status"] == "frontier_revised":
        lines.append("Frontieren ma revideres; band-kandidaten tok tilbake den operative ledelsen under ren size-separasjon.")
    else:
        lines.append(
            "Hold frontier-lesningen apen videre; metrikken eller generator-kontrollen er fortsatt for splittet til a kalle dette avgjort."
        )
    lines.append("")
    return "\n".join(lines)


def build_lay_markdown(verdict: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# v0.11d for ikke-spesialister",
            "",
            str(verdict["note"]),
            "",
            "Kort sagt: denne runden er laget for a se om den naavaerende beste bridge-kandidaten fortsatt er best nar vi zoomer inn lokalt, "
            "uten a endre selve modellen.",
            "",
        ]
    )


def build_recommendation(verdict: Mapping[str, Any]) -> str:
    lines = ["# v0.11d operativ anbefaling", ""]
    status = str(verdict["status"])
    if status == "robust_local_optimum":
        lines.append(f"Bruk `{verdict['raw_winner']}` som operativ standardkandidat i neste runde.")
    elif status == "local_plateau":
        lines.append(
            f"Hold `{verdict['raw_winner']}` som ledende kandidat, men la de naermeste bridge-nabopunktene bli med videre som lokal optimum-kontroll."
        )
    elif status == "frontier_revised":
        lines.append("Revider frontier; band-kandidaten tok tilbake den operative ledelsen.")
    else:
        lines.append("Hold baade den ledende bridge-kandidaten og kontrollsporet apne; repoet stotter fortsatt ikke en helt ren enkeltvinner.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.11d local triad refinement")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--bootstrap-reps", type=int, default=180)
    ap.add_argument("--include-diagnostic-0020", action="store_true")
    ap.add_argument("--output-prefix", default="Documentation/v11d")
    ap.add_argument("--report-md", default="Documentation/v11d_local_triad_refinement.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_11d.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_11d_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    hypothesis = verify_live_state()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidates = local_refinement_candidates(include_diagnostic_0020=bool(args.include_diagnostic_0020))
    growth_seeds = [19001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [6101 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v11d] regime={regime.name} targets={targets} candidates={[cand.name for cand in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)}"
    )
    print("[v11d] verifying live v11c state...")
    print(f"[v11d] {hypothesis['note']}")
    print("[v11d] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    print("[v11d] bases done")

    print("[v11d] collecting run rows...")
    run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    group_rows = v10e.summarize_groups(candidates, ensembles, run_rows)
    print(f"[v11d] runs done: {len(run_rows)} rows")
    print("[v11d] bootstrap...")
    ci_rows, pair_rows, top_rows = v10e.bootstrap_joint(
        candidates,
        ensembles,
        run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=66131,
    )
    candidate_rows = v11c.candidate_rows_from_group_rows(candidates, group_rows, ci_rows, top_rows)
    add_pairwise_scores(candidate_rows, pair_rows)
    verdict = resolution_verdict(candidate_rows, pair_rows, target_summary)

    print("[v11d] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_local_triad_refinement_base_rows.csv", base_rows)
    write_csv(f"{prefix}_local_triad_refinement_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_local_triad_refinement_candidate_summary.csv", candidate_rows)
    write_csv(f"{prefix}_local_triad_refinement_pairwise.csv", list(pair_rows))
    write_csv(f"{prefix}_local_triad_refinement_hypothesis_check.csv", [hypothesis])
    write_csv(f"{prefix}_local_triad_refinement_verdict.csv", [verdict])

    for path, content in [
        (args.report_md, build_markdown(hypothesis, target_summary, candidate_rows, pair_rows, verdict)),
        (args.lay_md, build_lay_markdown(verdict)),
        (args.recommendation_md, build_recommendation(verdict)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v11d] done")


if __name__ == "__main__":
    main()
