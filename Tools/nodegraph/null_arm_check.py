#!/usr/bin/env python3
"""
null_arm_check.py -- run the whole pipeline where there is nothing to find.

Both arm levels use the SAME parameter value; only the event stream differs,
exactly as it does in the real arm. So any candidate that clears the selection
gate here was manufactured by the pipeline -- by the pairing, the caching, the
substrate extraction or the loader -- and not by the world.

This is the check a permutation null cannot do. Permuting arm labels tests the
statistic on the differences it is handed; it cannot see a `pairs()` that hands
it the wrong differences in the first place. Fifteen lines and forty seconds,
and it is the only thing standing between "the statistic is calibrated" and
"the numbers mean anything".
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "arena"))

import core, library  # noqa: E402
import observable_purpose as OP  # noqa: E402
from run_experiment import run_arm  # noqa: E402

REG = library.REGISTRY


def main() -> int:
    r = run_arm("null", depth=3, n_probes=3, reps=2000, verbose=True, workers=4)

    print("\n== null arm ==", flush=True)
    print(f"arm            : {r['arm_field']} {r['levels']}  (identical levels)", flush=True)
    print(f"candidates     : {r['n_candidates']}", flush=True)
    print(f"winner         : {r['winner_expr']}", flush=True)
    print(f"train  {r['winner_train_score']:7.3f}  vs selection gate "
          f"{r['selection_gate_null_search_p95']:.3f}  -> "
          f"{'LEAK' if r['passes_selection'] else 'clean'}", flush=True)
    print(f"holdout{r['winner_holdout_score']:7.3f}  vs holdout gate  "
          f"{r['holdout_gate_null_p95']:.3f}  -> "
          f"{'LEAK' if r['passes_holdout'] else 'clean'}", flush=True)

    print("\nhand-picked baselines on the null arm (all should be noise):", flush=True)
    d = OP.load("null")
    for split in ("train", "holdout"):
        prs = OP.pairs(d, split)
        worst = max(
            (OP.paired_score(OP.deltas(core.parse(REG, OP.CHANNELS, e), prs)), n)
            for n, e in OP.BASELINES.items()
        )
        print(f"  {split:8s} worst of ten: {worst[1]} = {worst[0]:.3f}", flush=True)

    verdict = "CLEAN" if not (r["passes_selection"] or r["passes_holdout"]) else "LEAK"
    r["verdict"] = verdict
    with open(os.path.join(HERE, "_cache", "null_arm.json"), "w") as f:
        json.dump(r, f, indent=2)
    print(f"\nverdict: {verdict}", flush=True)
    return 0 if verdict == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
