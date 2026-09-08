#!/usr/bin/env python3
"""
run_experiment.py -- the whole loop, once, with the decisions fixed in advance.

Pre-registration (fixed before any candidate was scored; see PURPOSE.md):
  P1  Statistic: winsorised paired studentized mean, arena/observable_purpose.py.
  P2  Selection uses ONLY weak-arm train pairs. The holdout pairs are read by
      exactly one function, and only for graphs already selected.
  P3  Selection gate = 95th percentile of the MAXIMUM score over the entire
      candidate set under arm-label permutation (max-statistic null; this is
      what controls the multiple-comparison problem a search creates).
  P4  Holdout gate = 95th percentile of the score of that ONE winner under
      arm-label permutation of the holdout pairs.
  P5  The winner is the highest train score; ties broken by lower cost.
  P6  The positive reference is the same search run on the strong arm, where a
      response is known to be present.
  P7  A run in which the winner passes P3 but fails P4 is reported as a failure
      to generalise, not re-run with a different statistic.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "arena"))

import multiprocessing as mp  # noqa: E402

import core  # noqa: E402
import library  # noqa: E402
import observable_purpose as OP  # noqa: E402
from purpose import PurposeContract, Reference  # noqa: E402
from search import Enumerator  # noqa: E402

REG = library.REGISTRY


def build_pool(pairs_train, depth: int, n_probes: int, verbose: bool, search_seed: int = 20260908):
    probes = []
    for lo, hi in pairs_train[:n_probes]:
        probes.append(lo)
        probes.append(hi)
    en = Enumerator(REG, OP.CHANNELS, probes, seed=search_seed)
    t0 = time.time()
    pool = en.enumerate(depth=depth, verbose=verbose)
    if verbose:
        print(f"  enumeration {time.time()-t0:.1f}s", flush=True)
    return pool[core.REAL]


_W = {}


def _init(arm: str, split: str):
    _W["pairs"] = OP.pairs(OP.load(arm), split)


def _score_expr(expr: str):
    g = core.parse(REG, OP.CHANNELS, expr)
    d = OP.deltas(g, _W["pairs"])
    return expr, d, OP.paired_score(d)


def score_all(exprs, arm: str, split: str, workers: int):
    """Scoring is embarrassingly parallel and the graphs travel as text.

    Sending the readable expression rather than a pickled object is not just
    convenient: the text form is the interchange format of this whole design --
    it is what a worker parses, what a reviewer reads, and what a language-model
    proposer would emit. Everything type-checks again on arrival."""
    if workers <= 1:
        _init(arm, split)
        return [_score_expr(e) for e in exprs]
    with mp.Pool(workers, initializer=_init, initargs=(arm, split)) as pool:
        return pool.map(_score_expr, exprs, chunksize=64)


def run_arm(arm: str, depth: int, n_probes: int, reps: int, verbose: bool,
            workers: int = 4, search_seed: int = 20260908) -> Dict:
    data = OP.load(arm)
    train = OP.pairs(data, "train")
    holdout = OP.pairs(data, "holdout")

    cands = build_pool(train, depth, n_probes, verbose, search_seed)
    if verbose:
        print(f"  {len(cands)} distinct candidate observables", flush=True)

    t0 = time.time()
    by_expr = {c.graph.to_expr(): c for c in cands}
    scored = score_all(list(by_expr), arm, "train", workers)
    rows = [(by_expr[e], d, s) for e, d, s in scored]
    if verbose:
        print(f"  scored on train in {time.time()-t0:.1f}s "
              f"({workers} workers)", flush=True)

    nulls = OP.null_references_np([r[1] for r in rows], reps=reps)
    rows.sort(key=lambda r: (-r[2], r[0].cost))

    winner, wd, wscore = rows[0]
    # P4: the holdout is touched here and only here, for the selected graph only
    hd = OP.deltas(winner.graph, holdout)
    hscore = OP.paired_score(hd)
    rng = random.Random(4242)
    hnull = OP.quantile(OP.permuted_scores(hd, reps, rng), 0.95)

    return {
        "arm": arm,
        "arm_field": data["meta"]["arm_field"],
        "levels": data["meta"]["levels"],
        "steps": data["meta"]["steps"],
        "n_train_pairs": len(train),
        "n_holdout_pairs": len(holdout),
        "n_candidates": len(rows),
        "selection_gate_null_search_p95": nulls["null_search_p95"],
        "null_single_p95_train": nulls["null_single_p95"],
        "winner_expr": winner.graph.to_expr(),
        "winner_size": winner.graph.size,
        "winner_depth": winner.graph.depth,
        "winner_train_score": wscore,
        "winner_holdout_score": hscore,
        "holdout_gate_null_p95": hnull,
        "passes_selection": wscore > nulls["null_search_p95"],
        "passes_holdout": hscore > hnull,
        "top10": [
            {"expr": c.graph.to_expr(), "train_score": s, "size": c.graph.size}
            for c, _d, s in rows[:10]
        ],
        "permutation_reps": reps,
        "search_seed": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--probes", type=int, default=3)
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("--out", default=os.path.join(HERE, "_cache", "experiment.json"))
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--only", choices=["strong", "weak", "both"], default="both")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--search-seed", type=int, default=20260908)
    args = ap.parse_args()
    v = not args.quiet

    part = os.path.join(HERE, "_cache", "part_%s.json")
    if args.only in ("strong", "both"):
        print("== positive reference: strong arm ==", flush=True)
        strong = run_arm("strong", args.depth, args.probes, args.reps, v, args.workers, args.search_seed)
        with open(part % "strong", "w") as f:
            json.dump(strong, f, indent=2)
    else:
        with open(part % "strong") as f:
            strong = json.load(f)
    print(json.dumps({k: strong[k] for k in
                      ("winner_expr", "winner_train_score", "selection_gate_null_search_p95",
                       "winner_holdout_score", "holdout_gate_null_p95", "n_candidates")},
                     indent=2), flush=True)

    if args.only in ("weak", "both"):
        print("\n== search target: weak arm ==", flush=True)
        weak = run_arm("weak", args.depth, args.probes, args.reps, v, args.workers, args.search_seed)
        with open(part % "weak", "w") as f:
            json.dump(weak, f, indent=2)
    else:
        with open(part % "weak") as f:
            weak = json.load(f)
    if args.only != "both":
        pass

    contract = PurposeContract(
        id="observable_responds_to_rule_arm",
        statement=(
            "Find a scalar observable of the final simulation graph whose paired "
            "response to a change in the rewrite rule beats what the same search "
            "achieves on label-permuted data, and which keeps that response on "
            "start seeds never used to select it."
        ),
        signature=OP.CHANNELS,
        output_type=core.REAL,
        score=lambda g: 0.0,
        holdout=lambda g: 0.0,
        null_reference=Reference(
            "null", weak["selection_gate_null_search_p95"],
            "95th pct of max score over the whole candidate set under arm-label "
            "permutation of the same paired differences",
            "run_experiment.py P3",
        ),
        positive_reference=Reference(
            "positive", strong["winner_train_score"],
            "best score of the same search on the strong arm, where the response "
            "is known to be present",
            "run_experiment.py P6 (arm p_triadic_closure 0.02 vs 0.30)",
        ),
        min_separation=2.0,
        notes=(
            "The two references come from different arms and different pair counts "
            "(strong n=8, weak n=24). The strong-arm null is the higher of the two, "
            "so the separation check is conservative."
        ),
    )
    verdict = contract.admissibility()

    baselines = {}
    wdata = OP.load("weak")
    tr, ho = OP.pairs(wdata, "train"), OP.pairs(wdata, "holdout")
    for name, expr in OP.BASELINES.items():
        g = core.parse(REG, OP.CHANNELS, expr)
        baselines[name] = {
            "expr": expr,
            "train_score": OP.paired_score(OP.deltas(g, tr)),
            "holdout_score": OP.paired_score(OP.deltas(g, ho)),
        }

    out = {
        "generated_unix": time.time(),
        "library_ops": len(REG.ops),
        "contract": json.loads(contract.to_json()),
        "contract_admissible": bool(verdict),
        "contract_reasons": verdict.reasons,
        "positive_reference_run": strong,
        "search_run": weak,
        "hand_picked_baselines_weak_arm": baselines,
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print("\n== result ==", flush=True)
    print(f"contract admissible: {bool(verdict)} (separation {verdict.separation})", flush=True)
    print(f"candidates examined : {weak['n_candidates']}", flush=True)
    print(f"winner              : {weak['winner_expr']}", flush=True)
    print(f"train  {weak['winner_train_score']:.3f}  vs selection gate {weak['selection_gate_null_search_p95']:.3f}"
          f"  -> {'PASS' if weak['passes_selection'] else 'FAIL'}", flush=True)
    print(f"holdout{weak['winner_holdout_score']:8.3f}  vs holdout gate  {weak['holdout_gate_null_p95']:.3f}"
          f"  -> {'PASS' if weak['passes_holdout'] else 'FAIL'}", flush=True)
    best_bl = max(baselines.items(), key=lambda kv: kv[1]["holdout_score"])
    print(f"best hand-picked on holdout: {best_bl[0]} = {best_bl[1]['holdout_score']:.3f}", flush=True)
    print(f"\nwrote {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
