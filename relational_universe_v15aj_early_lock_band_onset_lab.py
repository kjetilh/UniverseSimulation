#!/usr/bin/env python3
"""v0.15aj early-lock band onset lab for add_chord recurrence band.

This round follows v15ai. v15ai showed that the robust `early_fragment_lock`
main family is much better described by coarse fragment-load bands
(`low`/`mid`/`high`) than by exact shell-component counts.

The next narrow question is:

when do runs actually settle into those band structures, and which runs remain
in broader three-band churn instead of latching into a stable ladder?

This round runs no new simulations. It analyzes the real v15ai snapshot data.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
IN_RUNS = DOC / "v15ai_early_lock_band_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15ai_early_lock_band_target_summary.csv"

TARGET = 48
BAND_ORDER = {"low": 0, "mid": 1, "high": 2}
SOURCE_ORDER = {"anchor_main_family": 0, "holdout_revert": 1, "combined": 2}
MIN_SUFFIX_SNAPSHOTS = 24


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
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def structured_suffix(
    bands: Sequence[str],
    *,
    min_suffix_snapshots: int,
) -> Tuple[int | None, str, str]:
    n = len(bands)
    required_len = max(min_suffix_snapshots, n // 3)
    for start in range(n):
        suffix = bands[start:]
        if len(suffix) < required_len:
            break
        uniq = sorted(set(suffix), key=lambda x: BAND_ORDER[x])
        if len(uniq) == 1:
            return start, "single", uniq[0]
        if len(uniq) == 2 and abs(BAND_ORDER[uniq[0]] - BAND_ORDER[uniq[1]]) == 1:
            return start, "adjacent", f"{uniq[0]}-{uniq[1]}"
    return None, "none", "none"


def onset_label(
    *,
    onset_start_index: int | None,
    onset_kind: str,
    onset_signature: str,
    n_snapshots: int,
) -> str:
    if onset_kind == "none" or onset_start_index is None:
        return "persistent_three_band_churn"
    onset_frac = onset_start_index / max(1, n_snapshots)
    if onset_start_index == 0:
        phase = "immediate"
    elif onset_frac <= 0.40:
        phase = "mid_tail"
    else:
        phase = "late_tail"
    suffix = "lock" if onset_kind == "single" else "ladder"
    return f"{phase}_{onset_signature}_{suffix}"


def onset_family(label: str) -> str:
    if label == "persistent_three_band_churn":
        return "persistent_three_band_churn"
    if label.startswith("immediate_"):
        return "immediate_structured_onset"
    if label.startswith("mid_tail_") or label.startswith("late_tail_"):
        return "delayed_structured_onset"
    return "other"


def analyze_runs(
    *,
    run_rows_in: Sequence[Mapping[str, str]],
    snapshot_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    by_run: Dict[Tuple[str, int], List[Dict[str, str]]] = defaultdict(list)
    run_lookup: Dict[Tuple[str, int], Dict[str, str]] = {}

    for row in run_rows_in:
        key = (str(row["source_group"]), int(row["run_seed"]))
        run_lookup[key] = dict(row)
    for row in snapshot_rows_in:
        key = (str(row["source_group"]), int(row["run_seed"]))
        by_run[key].append(dict(row))

    out: List[Dict[str, Any]] = []
    for key in sorted(by_run, key=lambda x: (SOURCE_ORDER.get(x[0], 99), x[1])):
        source_group, run_seed = key
        run_row = run_lookup[key]
        snapshots = sorted(by_run[key], key=lambda row: int(row["step"]))
        bands = [str(row["shell_count_band"]) for row in snapshots]
        steps = [int(row["step"]) for row in snapshots]
        onset_start_index, onset_kind, onset_signature = structured_suffix(
            bands,
            min_suffix_snapshots=MIN_SUFFIX_SNAPSHOTS,
        )
        label = onset_label(
            onset_start_index=onset_start_index,
            onset_kind=onset_kind,
            onset_signature=onset_signature,
            n_snapshots=len(bands),
        )
        if onset_start_index is None:
            onset_step = -1
            onset_frac = float("nan")
            post_switch_count = -1
            post_band_span = 3
            suffix_snapshot_count = 0
        else:
            onset_step = steps[onset_start_index]
            onset_frac = onset_start_index / max(1, len(bands))
            post_switch_count = sum(1 for a, b in zip(bands[onset_start_index:], bands[onset_start_index + 1:]) if a != b)
            post_band_span = max(BAND_ORDER[b] for b in bands[onset_start_index:]) - min(BAND_ORDER[b] for b in bands[onset_start_index:])
            suffix_snapshot_count = len(bands) - onset_start_index

        pre_bands = bands[:onset_start_index] if onset_start_index not in (None, 0) else []
        pre_switch_count = sum(1 for a, b in zip(pre_bands, pre_bands[1:]) if a != b) if pre_bands else 0
        pre_unique_band_count = len(set(pre_bands)) if pre_bands else 0
        post_counter = Counter(bands[onset_start_index:]) if onset_start_index is not None else Counter()
        post_dominant_band = (
            max(post_counter.items(), key=lambda item: (item[1], -BAND_ORDER[item[0]]))[0]
            if post_counter
            else "none"
        )
        post_dominant_share = (
            post_counter[post_dominant_band] / max(1, sum(post_counter.values()))
            if post_counter
            else float("nan")
        )

        out.append(
            {
                "source_group": source_group,
                "placement": int(run_row["placement"]),
                "anchor_seed_delta": int(run_row["anchor_seed_delta"]),
                "holdout_seed_delta": int(run_row["holdout_seed_delta"]),
                "run_seed": int(run_row["run_seed"]),
                "support_signature": str(run_row["support_signature"]),
                "band_lock_label": str(run_row["band_lock_label"]),
                "dominant_band": str(run_row["dominant_band"]),
                "dominant_band_share": safe_float(run_row["dominant_band_share"]),
                "top2_band_share": safe_float(run_row["top2_band_share"]),
                "onset_kind": onset_kind,
                "onset_signature": onset_signature,
                "onset_label": label,
                "onset_family": onset_family(label),
                "onset_snapshot_index": int(onset_start_index) if onset_start_index is not None else -1,
                "onset_step": int(onset_step),
                "onset_fraction": safe_float(onset_frac),
                "suffix_snapshot_count": int(suffix_snapshot_count),
                "pre_unique_band_count": int(pre_unique_band_count),
                "pre_switch_count": int(pre_switch_count),
                "post_switch_count": int(post_switch_count),
                "post_band_span": int(post_band_span),
                "post_dominant_band": post_dominant_band,
                "post_dominant_share": safe_float(post_dominant_share),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def add_group(group_type: str, group_value: str, group_rows: Sequence[Mapping[str, Any]]) -> None:
        if not group_rows:
            return
        out.append(
            {
                "group_type": group_type,
                "group_value": group_value,
                "n_runs": len(group_rows),
                "structured_onset_rate": mean_defined(
                    1.0 if str(row["onset_family"]) != "persistent_three_band_churn" else 0.0
                    for row in group_rows
                ),
                "immediate_structured_rate": mean_defined(
                    1.0 if str(row["onset_family"]) == "immediate_structured_onset" else 0.0
                    for row in group_rows
                ),
                "delayed_structured_rate": mean_defined(
                    1.0 if str(row["onset_family"]) == "delayed_structured_onset" else 0.0
                    for row in group_rows
                ),
                "persistent_three_band_churn_rate": mean_defined(
                    1.0 if str(row["onset_family"]) == "persistent_three_band_churn" else 0.0
                    for row in group_rows
                ),
                "immediate_low_mid_ladder_rate": mean_defined(
                    1.0 if str(row["onset_label"]) == "immediate_low-mid_ladder" else 0.0
                    for row in group_rows
                ),
                "delayed_mid_high_ladder_rate": mean_defined(
                    1.0 if str(row["onset_label"]) in {"mid_tail_mid-high_ladder", "late_tail_mid-high_ladder"} else 0.0
                    for row in group_rows
                ),
                "single_band_lock_rate": mean_defined(
                    1.0 if str(row["onset_kind"]) == "single" else 0.0
                    for row in group_rows
                ),
                "mean_onset_step": mean_defined(
                    safe_float(row["onset_step"]) for row in group_rows if int(row["onset_step"]) >= 0
                ),
                "mean_onset_fraction": mean_defined(
                    safe_float(row["onset_fraction"]) for row in group_rows if math.isfinite(safe_float(row["onset_fraction"]))
                ),
                "mean_pre_switch_count": mean_defined(safe_float(row["pre_switch_count"]) for row in group_rows),
                "mean_post_switch_count": mean_defined(
                    safe_float(row["post_switch_count"]) for row in group_rows if safe_float(row["post_switch_count"]) >= 0
                ),
                "mean_post_dominant_share": mean_defined(
                    safe_float(row["post_dominant_share"]) for row in group_rows if math.isfinite(safe_float(row["post_dominant_share"]))
                ),
            }
        )

    add_group("source_group", "combined", rows)
    for source_group in ("anchor_main_family", "holdout_revert"):
        add_group("source_group", source_group, [row for row in rows if str(row["source_group"]) == source_group])
    for placement in sorted({int(row["placement"]) for row in rows}):
        add_group("placement", str(placement), [row for row in rows if int(row["placement"]) == placement])
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    analyzed_rows: Sequence[Mapping[str, Any]],
    aggregate_rows_in: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    structured_anchor = next(row for row in aggregate_rows_in if str(row["group_type"]) == "source_group" and str(row["group_value"]) == "anchor_main_family")
    structured_holdout = next(row for row in aggregate_rows_in if str(row["group_type"]) == "source_group" and str(row["group_value"]) == "holdout_revert")
    p0 = next(row for row in aggregate_rows_in if str(row["group_type"]) == "placement" and str(row["group_value"]) == "0")
    p1 = next(row for row in aggregate_rows_in if str(row["group_type"]) == "placement" and str(row["group_value"]) == "1")
    p2 = next(row for row in aggregate_rows_in if str(row["group_type"]) == "placement" and str(row["group_value"]) == "2")

    if (
        safe_float(structured_anchor["structured_onset_rate"]) >= 0.75
        and safe_float(structured_holdout["structured_onset_rate"]) >= 0.70
        and safe_float(p0["immediate_low_mid_ladder_rate"]) >= 0.75
        and safe_float(p2["delayed_mid_high_ladder_rate"]) >= 0.35
    ):
        status = "band_onset_structure_supported"
        note = "De fleste run finner en strukturert ladder-suffix, men onseten er ikke flat: placement 0 gaar oftest rett inn i `low-mid`, mens placement 2 oftere glir senere inn i `mid-high` eller blir igjen i bredere churn."
        next_step = "probe_band_entry_triggers"
        next_note = "Neste steg bor forklare hva i tidlig hale som avgjor om et run gaar direkte inn i `low-mid`, senere inn i `mid-high`, eller blir igjen i tre-band-churn."
    elif safe_float(structured_anchor["structured_onset_rate"]) >= 0.60:
        status = "band_onset_partly_supported"
        note = "Onset-observabelen gir mer struktur enn `v15ai` alene, men forskjellene mellom onset-typene er fortsatt ikke skarpe nok til en sterk onset-familie-lesning."
        next_step = "tighten_onset_thresholds"
        next_note = "Neste steg bor stramme onset-definisjonen eller legge inn en enkel tidlig-hale triggerobservabel."
    else:
        status = "band_onset_still_mixed"
        note = "Selv onset-observabelen klarer ikke a gi en ren struktur inne i hovedfamilien."
        next_step = "pivot_observable_again"
        next_note = "Neste steg bor bytte observabel igjen i stedet for a presse onset-lesningen hardere."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "band_onset_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "placement_skew",
            "status": "descriptive",
            "note": (
                f"`p0` har immediate low-mid-rate {fmt(p0['immediate_low_mid_ladder_rate'])}, "
                f"`p1` har delayed mid-high-rate {fmt(p1['delayed_mid_high_ladder_rate'])}, "
                f"og `p2` har delayed mid-high-rate {fmt(p2['delayed_mid_high_ladder_rate'])} med mer churn."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_rows: Sequence[Mapping[str, str]],
    aggregate_rows_in: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    source_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "source_group"]
    placement_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "placement"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15aj: early-lock band onset lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker `v15ai`-snapshottene til a finne nar run faktisk finner en strukturert `low-mid` eller `mid-high` ladder-suffix, og hvilke run som blir igjen i bredere tre-band-churn.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_rows:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Source groups")
    lines.append("")
    lines.append("| group | n | structured onset | immediate structured | delayed structured | three-band churn | immediate low-mid | delayed mid-high | onset step | post switches |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(source_rows, key=lambda r: SOURCE_ORDER.get(str(r["group_value"]), 99)):
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['structured_onset_rate'])} | {fmt(row['immediate_structured_rate'])} | {fmt(row['delayed_structured_rate'])} | {fmt(row['persistent_three_band_churn_rate'])} | {fmt(row['immediate_low_mid_ladder_rate'])} | {fmt(row['delayed_mid_high_ladder_rate'])} | {fmt(row['mean_onset_step'],1)} | {fmt(row['mean_post_switch_count'],1)} |"
        )
    lines.append("")
    lines.append("## Per placement")
    lines.append("")
    lines.append("| placement | n | structured | immediate low-mid | delayed mid-high | three-band churn | onset step | post dominant share |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(placement_rows, key=lambda r: int(r["group_value"])):
        lines.append(
            f"| {int(row['group_value'])} | {int(row['n_runs'])} | {fmt(row['structured_onset_rate'])} | {fmt(row['immediate_low_mid_ladder_rate'])} | {fmt(row['delayed_mid_high_ladder_rate'])} | {fmt(row['persistent_three_band_churn_rate'])} | {fmt(row['mean_onset_step'],1)} | {fmt(row['mean_post_dominant_share'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en smal observabelrunde inne i hovedfamilien, ikke en ny defect-scan.")
    lines.append("- En strukturert ladder-suffix betyr her at resten av halen holder seg innenfor ett band eller et naboband-par.")
    lines.append("- Hvis dette holder, peker neste steg mot lokale triggerforhold ved selve overgangen inn i `low-mid` eller `mid-high`.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15aj early-lock band onset lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15aj_early_lock_band_onset_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15aj_early_lock_band_onset_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15aj_early_lock_band_onset_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15aj_early_lock_band_onset_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15aj_early_lock_band_onset_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15aj_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15aj.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows_in = read_csv(IN_RUNS)
    snapshot_rows_in = read_csv(IN_SNAPSHOTS)
    target_rows = read_csv(IN_TARGET)

    analyzed_rows = analyze_runs(
        run_rows_in=run_rows_in,
        snapshot_rows_in=snapshot_rows_in,
    )
    aggregate = aggregate_rows(analyzed_rows)
    diagnosis = diagnosis_rows(
        target_rows=target_rows,
        analyzed_rows=analyzed_rows,
        aggregate_rows_in=aggregate,
    )
    report_md = build_report(
        target_rows=target_rows,
        aggregate_rows_in=aggregate,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15aj operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en onset-lesning av `v15ai`-bandene, ikke som en ny defect-familieinndeling.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15aj",
            "",
            "Forrige runde viste at hovedfamilien er lettere a lese som grove fragment-band enn som eksakt antall shell-biter.",
            "",
            "Denne runden ser derfor pa nar runene faktisk kommer inn i slike band, og om de holder seg der eller fortsetter a veksle mellom mange band.",
            "",
            "Målet er a finne ut om hovedfamilien vanligvis starter direkte i et enkelt bandmonster, eller om den ma bruke tid pa a stabilisere seg.",
        ]
    ) + "\n"

    write_csv(args.out_runs_csv, analyzed_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_rows)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
