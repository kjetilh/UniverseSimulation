#!/usr/bin/env python3
"""v0.15aa p0-vs-p1 case trigger holdout.

This round is the direct follow-up to v15z. It runs a very narrow holdout
around the three anchor case seeds from v15y/v15z to test whether the new
onset-trigger story has any local carry-over.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q
import relational_universe_v15z_case_trigger_explainer as v15z


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1)
HOLDOUT_MAP = {
    151: (139, 163),
    239: (227, 251),
    271: (259, 283),
}
FULL_STEPS = 2560
LOG_EVERY = 8

DOC = Path("Documentation")
V15W_SUPPORT = DOC / "v15w_add_chord_p0_p1_support_summary.csv"
V15Z_ROWS = DOC / "v15z_case_trigger_rows.csv"

OUT_TARGET = DOC / "v15aa_case_trigger_holdout_target_summary.csv"
OUT_RUNS = DOC / "v15aa_case_trigger_holdout_runs.csv"
OUT_SEGMENTS = DOC / "v15aa_case_trigger_holdout_segments.csv"
OUT_ROWS = DOC / "v15aa_case_trigger_holdout_rows.csv"
OUT_AGGR = DOC / "v15aa_case_trigger_holdout_aggregate.csv"
OUT_DIAG = DOC / "v15aa_case_trigger_holdout_diagnosis.csv"
OUT_REPORT = DOC / "v15aa_case_trigger_holdout.md"
OUT_RECO = DOC / "v0_15aa_operativ_anbefaling.md"
OUT_NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15aa.md"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def segment_bounds(log_rows: Sequence[Dict[str, Any]], first_exact_step: float) -> Tuple[int, int]:
    tail_start_idx = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    if not math.isfinite(first_exact_step) or first_exact_step < 0:
        return tail_start_idx, len(log_rows) - 1
    end_idx = len(log_rows) - 1
    for idx in range(tail_start_idx, len(log_rows)):
        if safe_float(log_rows[idx]["step"]) >= first_exact_step:
            end_idx = idx
            break
    return tail_start_idx, end_idx


def support_lookup() -> Sequence[Mapping[str, str]]:
    return read_csv(V15W_SUPPORT)


def expected_trigger_lookup() -> Dict[int, Mapping[str, str]]:
    return {int(row["seed_delta"]): row for row in read_csv(V15Z_ROWS)}


def run_rows(*, base_state: Any) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    run_rows_out: List[Dict[str, Any]] = []
    segment_rows_out: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for anchor_seed, holdouts in HOLDOUT_MAP.items():
        for holdout_seed in holdouts:
            for placement in PLACEMENTS:
                base_run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
                run_seed = int(base_run_seed + holdout_seed)
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
                first_exact = safe_float(metrics["first_exact_return_step"])
                start_idx, end_idx = segment_bounds(res["log_rows"], first_exact)
                seg_rows = res["log_rows"][start_idx : end_idx + 1]
                seg_sets = res["damaged_sets"][start_idx : end_idx + 1]
                prev_set = None
                for local_idx, (row, damaged) in enumerate(zip(seg_rows, seg_sets)):
                    adj = v15.jaccard(prev_set, damaged) if prev_set is not None else float("nan")
                    prev_set = damaged
                    segment_rows_out.append(
                        {
                            "anchor_seed_delta": int(anchor_seed),
                            "holdout_seed_delta": int(holdout_seed),
                            "placement": int(placement),
                            "run_seed": int(run_seed),
                            "segment_local_index": int(local_idx),
                            "step": int(row["step"]),
                            "damage_component_count": int(row["damage_component_count"]),
                            "largest_component_fraction": safe_float(row["largest_component_fraction"]),
                            "boundary_to_volume": safe_float(row["boundary_to_volume"]),
                            "radius_control": safe_float(row["radius_control"]),
                            "damaged_nodes_count": int(row["damaged_nodes_count"]),
                            "adjacent_jaccard": adj,
                        }
                    )
                info = dict(res["perturbation_info"])
                run_rows_out.append(
                    {
                        "anchor_seed_delta": int(anchor_seed),
                        "holdout_seed_delta": int(holdout_seed),
                        "placement": int(placement),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                        "support_signature": ",".join(str(x) for x in info.get("support", [])),
                        "full_label": v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), metrics),
                        "full_exact_return_rate": safe_float(metrics["exact_return_rate"]),
                        "first_exact_return_step": first_exact,
                        "segment_snapshot_count": len(seg_rows),
                        "mean_prelock_component_count": mean_defined(safe_float(r["damage_component_count"]) for r in seg_rows),
                        "mean_prelock_largest_fraction": mean_defined(safe_float(r["largest_component_fraction"]) for r in seg_rows),
                        "mean_prelock_boundary_to_volume": mean_defined(safe_float(r["boundary_to_volume"]) for r in seg_rows),
                        "mean_prelock_radius": mean_defined(
                            safe_float(r["radius_control"]) for r in seg_rows if safe_float(r["radius_control"]) >= 0
                        ),
                        "mean_prelock_damage_nodes": mean_defined(safe_float(r["damaged_nodes_count"]) for r in seg_rows),
                        "mean_prelock_adjacent_jaccard": mean_defined(
                            safe_float(r["adjacent_jaccard"])
                            for r in segment_rows_out
                            if int(r["anchor_seed_delta"]) == int(anchor_seed)
                            and int(r["holdout_seed_delta"]) == int(holdout_seed)
                            and int(r["placement"]) == int(placement)
                            and math.isfinite(safe_float(r["adjacent_jaccard"]))
                        ),
                    }
                )
    return run_rows_out, segment_rows_out


def first_segment_rows(rows: Sequence[Mapping[str, Any]]) -> Dict[Tuple[int, int, int], Mapping[str, Any]]:
    out: Dict[Tuple[int, int, int], Mapping[str, Any]] = {}
    for row in rows:
        if int(row["segment_local_index"]) != 0:
            continue
        key = (int(row["anchor_seed_delta"]), int(row["holdout_seed_delta"]), int(row["placement"]))
        out[key] = row
    return out


def holdout_case_rows(
    *,
    run_rows_in: Sequence[Mapping[str, Any]],
    segment_rows_in: Sequence[Mapping[str, Any]],
    expected_trigger_rows: Mapping[int, Mapping[str, str]],
    support_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    run_lookup = {
        (int(row["anchor_seed_delta"]), int(row["holdout_seed_delta"]), int(row["placement"])): row
        for row in run_rows_in
    }
    first_lookup = first_segment_rows(segment_rows_in)
    support_bias = v15z.support_bias_snapshot(support_rows_in)
    out: List[Dict[str, Any]] = []
    for anchor_seed, holdouts in HOLDOUT_MAP.items():
        expected = expected_trigger_rows[int(anchor_seed)]
        expected_label = str(expected["trigger_label"])
        for holdout_seed in holdouts:
            p0 = run_lookup[(anchor_seed, holdout_seed, 0)]
            p1 = run_lookup[(anchor_seed, holdout_seed, 1)]
            p0_first = first_lookup[(anchor_seed, holdout_seed, 0)]
            p1_first = first_lookup[(anchor_seed, holdout_seed, 1)]

            exact_gap = safe_float(p1["full_exact_return_rate"]) - safe_float(p0["full_exact_return_rate"])
            first_gap = safe_float(p1["first_exact_return_step"]) - safe_float(p0["first_exact_return_step"])
            first_component_gap = safe_float(p1_first["damage_component_count"]) - safe_float(p0_first["damage_component_count"])
            first_largest_gap = safe_float(p1_first["largest_component_fraction"]) - safe_float(p0_first["largest_component_fraction"])
            first_boundary_gap = safe_float(p1_first["boundary_to_volume"]) - safe_float(p0_first["boundary_to_volume"])
            first_radius_gap = safe_float(p1_first["radius_control"]) - safe_float(p0_first["radius_control"])
            first_damage_gap = safe_float(p1_first["damaged_nodes_count"]) - safe_float(p0_first["damaged_nodes_count"])
            mean_component_gap = safe_float(p1["mean_prelock_component_count"]) - safe_float(p0["mean_prelock_component_count"])
            mean_boundary_gap = safe_float(p1["mean_prelock_boundary_to_volume"]) - safe_float(p0["mean_prelock_boundary_to_volume"])
            mean_radius_gap = safe_float(p1["mean_prelock_radius"]) - safe_float(p0["mean_prelock_radius"])
            mean_damage_gap = safe_float(p1["mean_prelock_damage_nodes"]) - safe_float(p0["mean_prelock_damage_nodes"])
            mean_adj_gap = safe_float(p1["mean_prelock_adjacent_jaccard"]) - safe_float(p0["mean_prelock_adjacent_jaccard"])

            observed_trigger = v15z.classify_trigger(
                exact_gap=exact_gap,
                first_gap=first_gap,
                first_component_gap=first_component_gap,
                first_boundary_gap=first_boundary_gap,
                first_radius_gap=first_radius_gap,
                first_damage_gap=first_damage_gap,
                mean_component_gap=mean_component_gap,
            )
            if observed_trigger == expected_label:
                holdout_status = "trigger_matched"
            elif observed_trigger == "mixed_trigger":
                holdout_status = "mixed_holdout"
            else:
                holdout_status = "trigger_shifted"

            out.append(
                {
                    "anchor_seed_delta": int(anchor_seed),
                    "expected_trigger_label": expected_label,
                    "holdout_seed_delta": int(holdout_seed),
                    "holdout_offset_from_anchor": int(holdout_seed - anchor_seed),
                    "observed_trigger_label": observed_trigger,
                    "holdout_status": holdout_status,
                    "support_density_bias": "p1_denser_support",
                    "support_expansion_bias": "p0_wider_relative_expansion",
                    "p1_minus_p0_support_degree_gap": support_bias["p1_minus_p0_degree_gap"],
                    "p1_minus_p0_support_ball1_gap": support_bias["p1_minus_p0_ball1_gap"],
                    "p0_minus_p1_expansion_gap": support_bias["p0_minus_p1_expansion_gap"],
                    "p1_minus_p0_exact_gap": exact_gap,
                    "p1_minus_p0_first_gap": first_gap,
                    "first_component_gap": first_component_gap,
                    "first_largest_gap": first_largest_gap,
                    "first_boundary_gap": first_boundary_gap,
                    "first_radius_gap": first_radius_gap,
                    "first_damage_gap": first_damage_gap,
                    "mean_component_gap": mean_component_gap,
                    "mean_boundary_gap": mean_boundary_gap,
                    "mean_radius_gap": mean_radius_gap,
                    "mean_damage_gap": mean_damage_gap,
                    "mean_adjacent_jaccard_gap": mean_adj_gap,
                }
            )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for anchor_seed in sorted(HOLDOUT_MAP):
        grp = [row for row in rows if int(row["anchor_seed_delta"]) == int(anchor_seed)]
        matched = sum(1 for row in grp if str(row["holdout_status"]) == "trigger_matched")
        mixed = sum(1 for row in grp if str(row["holdout_status"]) == "mixed_holdout")
        shifted = sum(1 for row in grp if str(row["holdout_status"]) == "trigger_shifted")
        total = max(1, len(grp))
        if matched == total:
            family_status = "fully_supported"
        elif matched >= 1 and shifted == 0:
            family_status = "partly_supported"
        elif matched >= 1:
            family_status = "contested"
        else:
            family_status = "not_supported"
        out.append(
            {
                "anchor_seed_delta": int(anchor_seed),
                "expected_trigger_label": str(grp[0]["expected_trigger_label"]) if grp else "missing",
                "n_holdouts": len(grp),
                "trigger_match_rate": matched / total,
                "mixed_holdout_rate": mixed / total,
                "trigger_shift_rate": shifted / total,
                "mean_exact_gap": mean_defined(safe_float(row["p1_minus_p0_exact_gap"]) for row in grp),
                "mean_first_gap": mean_defined(safe_float(row["p1_minus_p0_first_gap"]) for row in grp),
                "mean_first_component_gap": mean_defined(safe_float(row["first_component_gap"]) for row in grp),
                "mean_first_boundary_gap": mean_defined(safe_float(row["first_boundary_gap"]) for row in grp),
                "family_status": family_status,
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, str]],
    run_rows_in: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    requested_match_clean = all(int(row["requested_match"]) == 1 for row in run_rows_in)
    fully_supported = sum(1 for row in aggregate if str(row["family_status"]) == "fully_supported")
    partly_supported = sum(1 for row in aggregate if str(row["family_status"]) == "partly_supported")
    contested = sum(1 for row in aggregate if str(row["family_status"]) == "contested")
    not_supported = sum(1 for row in aggregate if str(row["family_status"]) == "not_supported")

    if fully_supported >= 2 and not_supported == 0:
        status = "trigger_holdout_strong"
        note = "Minst to av de tre lokale trigger-familiene holder fullt i nærliggende holdouts, og ingen kollapser helt."
        next_step = "expand_tiny_holdout"
        next_note = "Neste steg kan være en liten utvidelse rundt den svakeste trigger-familien."
    elif fully_supported + partly_supported >= 2:
        status = "trigger_holdout_mixed_but_real"
        note = "Holdout-runden støtter at trigger-historien har lokal bæreevne, men ikke som ren lov på tvers av alle tre familier."
        next_step = "focus_weak_family"
        next_note = "Neste steg bør gå enda smalere på den trigger-familien som holder svakest."
    else:
        status = "trigger_holdout_not_yet"
        note = "Trigger-historien holder ikke rent nok i nærliggende seeds til å kalles stabil ennå."
        next_step = "stop_generalizing"
        next_note = "Neste steg bør være en ny observabel eller et annet defect-spørsmål, ikke mer trigger-generalisering."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean and requested_match_clean else "unclear",
            "note": "Startstørrelsene er rent separert og alle holdout-runene matcher ønsket add_chord-perturbasjon."
            if size_clean and requested_match_clean
            else "Enten størrelsesseparasjonen eller perturbasjonsmatchen er uklar i holdout-runden.",
        },
        {
            "diagnostic_family": "family_snapshot",
            "status": f"fully_supported={fully_supported};partly_supported={partly_supported};contested={contested};not_supported={not_supported}",
            "note": "Dette oppsummerer hvor mange av de tre lokale trigger-familiene som holder i de nærliggende holdout-seedene.",
        },
        {
            "diagnostic_family": "trigger_holdout_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15aa: p0-vs-p1 case trigger holdout")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden tester om de tre onset-triggerne fra `v15z` har lokal bæreevne i noen få nærliggende holdout-seeds.")
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Holdout rows")
    lines.append("")
    lines.append("| anchor | holdout | expected | observed | status | exact gap | first gap | first comp gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['anchor_seed_delta'])} | {int(row['holdout_seed_delta'])} | {row['expected_trigger_label']} | {row['observed_trigger_label']} | {row['holdout_status']} | {fmt(row['p1_minus_p0_exact_gap'])} | {fmt(row['p1_minus_p0_first_gap'],1)} | {fmt(row['first_component_gap'])} |"
        )
    lines.append("")
    lines.append("## Family aggregate")
    lines.append("")
    lines.append("| anchor | expected | match rate | mixed rate | shift rate | status |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['anchor_seed_delta'])} | {row['expected_trigger_label']} | {fmt(row['trigger_match_rate'])} | {fmt(row['mixed_holdout_rate'])} | {fmt(row['trigger_shift_rate'])} | {row['family_status']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Les denne runden som lokal trigger-holdout, ikke som bred generalisering.")
    lines.append("- Målet her er bare å se om `v15z`-forklaringen bærer litt utover de tre opprinnelige case-seedene.")
    lines.append("")
    return "\n".join(lines)


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# v0.15aa operativ anbefaling", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les denne runden som en smal holdout-test av `v15z`-triggerne, ikke som en ny p0-vs-p1-scan.")
    return "\n".join(lines) + "\n"


def build_nonspecialist(aggregate: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15aa for ikke-spesialister")
    lines.append("")
    lines.append("Her testet vi ikke mange nye tilfeller. Vi tok bare noen få små nabo-tilfeller rundt de tre `v15z`-eksemplene for å se om forklaringen holder litt utenfor originalcasene.")
    lines.append("")
    for row in aggregate:
        lines.append(
            f"- Anker `{int(row['anchor_seed_delta'])}` med forventet `{row['expected_trigger_label']}` fikk status `{row['family_status']}` og match-rate `{fmt(row['trigger_match_rate'])}`."
        )
    lines.append("")
    next_row = next((row for row in diagnosis if str(row["diagnostic_family"]) == "next_step"), None)
    if next_row is not None:
        lines.append(f"Neste naturlige steg er `{next_row['status']}`: {next_row['note']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]

    run_rows_out, segment_rows_out = run_rows(base_state=base_state)
    expected_trigger_rows = expected_trigger_lookup()
    support_rows_in = support_lookup()
    rows = holdout_case_rows(
        run_rows_in=run_rows_out,
        segment_rows_in=segment_rows_out,
        expected_trigger_rows=expected_trigger_rows,
        support_rows_in=support_rows_in,
    )
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows_in=run_rows_out,
        aggregate=aggregate,
    )

    write_csv(OUT_TARGET, target_summary)
    write_csv(OUT_RUNS, run_rows_out)
    write_csv(OUT_SEGMENTS, segment_rows_out)
    write_csv(OUT_ROWS, rows)
    write_csv(OUT_AGGR, aggregate)
    write_csv(OUT_DIAG, diagnosis)
    OUT_REPORT.write_text(
        build_report(
            target_summary=target_summary,
            rows=rows,
            aggregate=aggregate,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    OUT_RECO.write_text(build_recommendation(diagnosis), encoding="utf-8")
    OUT_NONSPECIALIST.write_text(build_nonspecialist(aggregate, diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
