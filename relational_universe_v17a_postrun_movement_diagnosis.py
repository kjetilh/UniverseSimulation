#!/usr/bin/env python3
"""Post-run diagnosis of the frozen v17a finite-movement failure."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import statistics
from typing import Any, Dict, List

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
DIAGNOSIS_CSV = DOC / "v17a_postrun_movement_diagnosis.csv"
DIAGNOSIS_MD = DOC / "v17a_postrun_movement_diagnosis.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_formal_products() -> str:
    prereg = v16i.read_csv(v17a.PRE_REGISTRATION)
    if len(prereg) != 1:
        raise ValueError("v17a preregistration row count failed")
    if prereg[0]["script_sha256"] != file_sha256(v17a.SCRIPT):
        raise ValueError("v17a frozen script hash changed")
    if prereg[0]["source_chain_sha256"] != file_sha256(v17a.SOURCE_CHAIN):
        raise ValueError("v17a frozen source chain hash changed")
    v17a.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v17a.GATE_EVALUATION)
        if row["gate"] == "v17a_overall"
    )
    if overall != "v17a_cycle_proposal_finite_movement_not_qualified":
        raise ValueError("v17a post-run diagnosis requires the frozen movement failure")
    return overall


def metric_row(
    rows: List[Dict[str, str]],
    metric: str,
    threshold: float,
    comparison: str,
    interpretation: str,
) -> Dict[str, Any]:
    values = [float(row[metric]) for row in rows]
    if comparison == "at_least":
        passes = sum(value >= threshold for value in values)
        requirement = f">={threshold}"
    elif comparison == "at_most":
        passes = sum(value <= threshold for value in values)
        requirement = f"<={threshold}"
    else:
        raise ValueError("unknown threshold comparison")
    return {
        "stage": "v17a_postrun",
        "metric": metric,
        "minimum": min(values),
        "mean": statistics.mean(values),
        "maximum": max(values),
        "passing_chains": passes,
        "total_chains": len(values),
        "frozen_requirement": requirement,
        "metric_pass": int(passes == len(values)),
        "interpretation": interpretation,
    }


def diagnosis_rows() -> List[Dict[str, Any]]:
    rows = v16i.read_csv(v17a.TRANSITION_SUMMARY)
    if len(rows) != 24:
        raise ValueError("v17a transition summary is incomplete")
    return [
        metric_row(
            rows, "valid_proposals", v17a.MIN_VALID_PROPOSALS_PER_CHAIN, "at_least",
            "proposal construction reaches a valid closed cycle too infrequently",
        ),
        metric_row(
            rows, "accepted_cycles", v17a.MIN_ACCEPTED_CYCLES_PER_CHAIN, "at_least",
            "accepted movement is below the frozen floor on most chains",
        ),
        metric_row(
            rows, "accepted_long_cycles", v17a.MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN, "at_least",
            "length-three-or-greater movement is too sparse",
        ),
        metric_row(
            rows, "unique_state_count", v17a.MIN_UNIQUE_STATES_PER_CHAIN, "at_least",
            "all chains visit multiple distinct states",
        ),
        metric_row(
            rows, "final_start_changed_edge_fraction", v17a.MIN_FINAL_START_CHANGE, "at_least",
            "finite displacement remains below the frozen five-percent floor",
        ),
        metric_row(
            rows, "elapsed_seconds", v17a.MAX_CHAIN_SECONDS, "at_most",
            "runtime is not the qualification bottleneck",
        ),
    ]


def run() -> None:
    overall = verify_formal_products()
    rows = diagnosis_rows()
    v16i.write_csv(DIAGNOSIS_CSV, rows)
    by_metric = {row["metric"]: row for row in rows}
    DIAGNOSIS_MD.write_text(
        "# v17a post-run movement diagnosis\n\n"
        f"The frozen formal status remains `{overall}`. This audit does not relax thresholds or rerun the chains.\n\n"
        "Representation, exact reverse support, pathwise detailed balance and resource bounds passed in the formal gate. "
        f"All `24/24` chains also passed the unique-state floor, with "
        f"`{int(by_metric['unique_state_count']['minimum'])}-{int(by_metric['unique_state_count']['maximum'])}` visited states.\n\n"
        "Finite movement nevertheless failed for two coupled reasons. Valid proposals ranged from "
        f"`{int(by_metric['valid_proposals']['minimum'])}` to `{int(by_metric['valid_proposals']['maximum'])}` and passed the frozen floor on "
        f"`{int(by_metric['valid_proposals']['passing_chains'])}/24`. Accepted cycles passed on "
        f"`{int(by_metric['accepted_cycles']['passing_chains'])}/24`, accepted length-three-or-greater cycles on "
        f"`{int(by_metric['accepted_long_cycles']['passing_chains'])}/24`, and final five-percent displacement on "
        f"`{int(by_metric['final_start_changed_edge_fraction']['passing_chains'])}/24`. Observed final displacement was "
        f"`{by_metric['final_start_changed_edge_fraction']['minimum']:.6f}-{by_metric['final_start_changed_edge_fraction']['maximum']:.6f}`.\n\n"
        "The correct diagnosis is proposal inefficiency under the frozen finite budget, not a reversibility, representation or runtime failure. "
        "Do not advance to start/seed/time stability and do not merely lengthen the chains. The smallest next research gate is a residual-graph cycle constructor that raises valid-cycle yield while preserving distinguished reverse auxiliaries and exact proposal ratios; it must be qualified anew before any spectrum/effect test.\n",
        encoding="utf-8",
    )
    print("[v17a-postrun] movement diagnosis complete")


def verify_outputs() -> None:
    overall = verify_formal_products()
    rows = v16i.read_csv(DIAGNOSIS_CSV)
    if len(rows) != 6:
        raise ValueError("v17a post-run diagnosis row count failed")
    if next(row for row in rows if row["metric"] == "unique_state_count")["passing_chains"] != "24":
        raise ValueError("v17a unique-state diagnosis changed")
    if next(row for row in rows if row["metric"] == "final_start_changed_edge_fraction")["passing_chains"] != "0":
        raise ValueError("v17a displacement diagnosis changed")
    if overall not in DIAGNOSIS_MD.read_text(encoding="utf-8"):
        raise ValueError("v17a post-run report lost the frozen status")
    print("[v17a-postrun] output verification pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v17a post-run movement diagnosis")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
