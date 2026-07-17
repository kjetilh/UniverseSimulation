#!/usr/bin/env python3
"""Post-run runtime diagnosis for the frozen v17b residual-cycle gate."""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v17b_residual_cycle_constructor_gate as v17b


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
DIAGNOSIS_CSV = DOC / "v17b_postrun_runtime_diagnosis.csv"
DIAGNOSIS_MD = DOC / "v17b_postrun_runtime_diagnosis.md"

ChainKey = Tuple[str, str, str, str]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = math.sqrt(
        sum((x - mean_x) ** 2 for x in xs)
        * sum((y - mean_y) ** 2 for y in ys)
    )
    return numerator / denominator if denominator else 0.0


def chain_key(row: Dict[str, str]) -> ChainKey:
    return (
        row["growth_seed"],
        row["run_offset"],
        row["start_family"],
        row["chain_seed_family"],
    )


def diagnosis_rows() -> List[Dict[str, Any]]:
    traces: Dict[ChainKey, List[Dict[str, str]]] = defaultdict(list)
    for row in v16i.read_csv(v17b.PROPOSAL_TRACE):
        traces[chain_key(row)].append(row)

    result = []
    for transition in v16i.read_csv(v17b.TRANSITION_SUMMARY):
        rows = traces[chain_key(transition)]
        valid_by_length: Counter[int] = Counter()
        completed_by_length: Counter[int] = Counter()
        max_completed_by_length: Counter[int] = Counter()
        for row in rows:
            completed = int(row["cycle_count_for_start"])
            if not completed:
                continue
            length = int(row["cycle_length_choice"])
            valid_by_length[length] += 1
            completed_by_length[length] += completed
            max_completed_by_length[length] = max(
                max_completed_by_length[length], completed
            )
        total_completed = sum(completed_by_length.values())
        result.append({
            "growth_seed": transition["growth_seed"],
            "run_offset": transition["run_offset"],
            "start_family": transition["start_family"],
            "chain_seed_family": transition["chain_seed_family"],
            "elapsed_seconds": transition["elapsed_seconds"],
            "resource_pass": transition["resource_pass"],
            "valid_proposals": transition["valid_proposals"],
            "accepted_cycles": transition["accepted_cycles"],
            "recorded_completion_count_sum": total_completed,
            "recorded_completion_count_length2": completed_by_length[2],
            "recorded_completion_count_length3": completed_by_length[3],
            "recorded_completion_count_length4": completed_by_length[4],
            "length4_completion_fraction": (
                completed_by_length[4] / total_completed
                if total_completed else 0.0
            ),
            "maximum_completion_count_length2": max_completed_by_length[2],
            "maximum_completion_count_length3": max_completed_by_length[3],
            "maximum_completion_count_length4": max_completed_by_length[4],
            "valid_length2": valid_by_length[2],
            "valid_length3": valid_by_length[3],
            "valid_length4": valid_by_length[4],
        })
    return result


def write_report(rows: Sequence[Dict[str, Any]]) -> None:
    elapsed = [float(row["elapsed_seconds"]) for row in rows]
    completions = [float(row["recorded_completion_count_sum"]) for row in rows]
    length4_total = sum(int(row["recorded_completion_count_length4"]) for row in rows)
    completion_total = sum(int(row["recorded_completion_count_sum"]) for row in rows)
    resource_passes = sum(int(row["resource_pass"]) for row in rows)
    slowest = max(rows, key=lambda row: float(row["elapsed_seconds"]))
    only_source_pass = [
        row for row in v16i.read_csv(v17b.SOURCE_SUMMARY)
        if int(row["source_qualification_pass"])
    ]

    report = f"""# v17b post-run runtime diagnosis

Status inherited from the frozen gate: `v17b_resource_not_qualified`.

## Measured result

- finite movement passed `24/24`
- matched valid-proposal improvement passed `24/24`
- median valid-proposal ratio versus v17a was `2.898276`
- resource bound passed only `{resource_passes}/24`
- runtime range was `{min(elapsed):.6f}` to `{max(elapsed):.6f}` seconds per chain
- only `{len(only_source_pass)}/6` source cells passed all four per-chain resource checks

The slowest chain was growth seed `{slowest['growth_seed']}`, run offset
`{slowest['run_offset']}`, start `{slowest['start_family']}`, seed family
`{slowest['chain_seed_family']}` at `{float(slowest['elapsed_seconds']):.6f}` seconds.

## Trace diagnosis

Recorded completed length-4 sequences account for
`{length4_total / completion_total:.6f}` of all recorded completion counts.
The Pearson correlation between per-chain runtime and the sum of recorded
completion counts is only `{pearson(completions, elapsed):.6f}`.

This weak correlation prevents treating the logged completion count as a
complete cost model. The trace records completed cycles, but not failed branch
visits or allocation cost. It is therefore evidence that length-4 enumeration
dominates the returned candidate mass, not proof that it alone explains runtime.

## Static implementation diagnosis

The frozen v17b implementation enumerates the forward cycle set once in
`propose_cycle()`, then enumerates the same forward set again in
`path_probability()`. It also materializes every completed cycle as a tuple
before sampling. Reverse probability legitimately requires a separate count in
the proposed state; the duplicate forward enumeration does not.

These are algorithmic costs, not dynamical effects. Optimizing them must leave
the exact auxiliary probability and reverse pairing unchanged.

## Next gate: v17c exact-counter runtime qualification

Freeze a new effect-blind gate with the same six spaces, starts, seeds, 512-step
budget, cycle lengths, laziness, movement floors, exact reverse auxiliary and
`<=60 s` resource threshold. Change only the constructor implementation:

1. compute the forward completion count once and reuse it in the auxiliary
   probability
2. replace full tuple materialization with exact completion counting plus
   uniform rank/reservoir sampling
3. add parity tests showing identical completion counts and proposal support
   against v17b on frozen witness states
4. retain exact `min(1,q_reverse/q_forward)` and full assignment-integrity checks
5. require resource pass `24/24` and movement pass `24/24`

Do not open source spectrum, observed effect, start/seed/time stability, Bell,
entanglement or Lorentz claims in v17c. If the exact optimized constructor still
misses the runtime bound, retire full bounded-cycle enumeration as the active
sampler path rather than relaxing the threshold.

## Evidence and claim limits

- v17b trace SHA-256: `{file_sha256(v17b.PROPOSAL_TRACE)}`
- v17b transition summary SHA-256: `{file_sha256(v17b.TRANSITION_SUMMARY)}`
- this is a disclosed post-run diagnosis, not a preregistered v17b endpoint
- no source spectrum or observed-effect statistic was computed
- no convergence, mixing, global irreducibility or physical claim follows
"""
    DIAGNOSIS_MD.write_text(report, encoding="utf-8")


def main() -> None:
    v17b.verify_outputs()
    rows = diagnosis_rows()
    if len(rows) != 24:
        raise ValueError("expected 24 v17b chains")
    v16i.write_csv(DIAGNOSIS_CSV, rows)
    write_report(rows)
    print(
        "[v17b-postrun] complete "
        f"resource={sum(int(row['resource_pass']) for row in rows)}/24"
    )


if __name__ == "__main__":
    main()
