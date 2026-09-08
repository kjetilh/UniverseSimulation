#!/usr/bin/env python3
"""
build_substrate.py -- generate cached "substrate channels" from relational_universe_sim runs.

Purpose (see Tools/nodegraph/PURPOSE.md, delformaal D4):
  Give the observable search a cheap, fixed input so that scoring a candidate
  observable costs milliseconds instead of a simulation run. Each run is reduced
  ONCE to a set of typed raw channels; the search then operates only on channels.

No physics claim is made here. This is instrumentation.

Design (paired):
  For every seed s and every arm level L, the START STATE is built from seed s
  (identical across levels) and the event stream from a level-dependent seed.
  This is a paired design: the arm contrast is within-start, so start-family
  variance -- the quantity that dominated the v17 series -- does not enter the
  paired statistic. The unpaired variance split is still recorded so the
  domination can be measured rather than assumed.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, REPO)

import relational_universe_sim as sim  # noqa: E402


MAX_SAMPLE = 300


def _sorted_nodes(g: "sim.UGraph") -> List[int]:
    return sorted(g.adj.keys())


def _sample(nodes: List[int], k: int, rng: random.Random) -> List[int]:
    if len(nodes) <= k:
        return nodes
    return rng.sample(nodes, k)


def _components(g: "sim.UGraph") -> List[int]:
    seen = set()
    sizes = []
    for v in _sorted_nodes(g):
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        size = 0
        while stack:
            x = stack.pop()
            size += 1
            for y in g.neighbors(x):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def extract_channels(g: "sim.UGraph", tokens: List[int], rng: random.Random) -> Dict[str, object]:
    nodes = _sorted_nodes(g)
    n = len(nodes)
    m = g.num_edges()

    deg = [float(g.degree(v)) for v in nodes]

    probe = _sample(nodes, MAX_SAMPLE, rng)
    tri: List[float] = []
    clus: List[float] = []
    for v in probe:
        ns = list(g.neighbors(v))
        k = len(ns)
        links = 0
        for i in range(k):
            na = g.neighbors(ns[i])
            for j in range(i + 1, k):
                if ns[j] in na:
                    links += 1
        tri.append(float(links))
        clus.append(0.0 if k < 2 else 2.0 * links / (k * (k - 1)))

    roots = _sample(nodes, min(60, MAX_SAMPLE), rng)
    b1: List[float] = []
    b2: List[float] = []
    b3: List[float] = []
    for r in roots:
        vol = sim.bfs_ball_volumes(g, r, 3)
        b1.append(float(vol[1]))
        b2.append(float(vol[2]))
        b3.append(float(vol[3]))

    comp = [float(x) for x in _components(g)]
    tokdeg = [float(g.degree(v)) for v in tokens if v in g.adj]
    if not tokdeg:
        tokdeg = [0.0]

    # edge-endpoint degree pairs, in a fixed order (assortativity substrate)
    edeg_a: List[float] = []
    edeg_b: List[float] = []
    for v in probe:
        for u in sorted(g.neighbors(v)):
            if u > v:
                edeg_a.append(float(g.degree(v)))
                edeg_b.append(float(g.degree(u)))
    if not edeg_a:
        edeg_a = [0.0]
        edeg_b = [0.0]

    return {
        "n": float(n),
        "m": float(m),
        "beta1": float(m - n + len(comp)),
        "deg": deg,
        "tri": tri,
        "clus": clus,
        "b1": b1,
        "b2": b2,
        "b3": b3,
        "comp": comp,
        "tokdeg": tokdeg,
        "edeg_a": edeg_a,
        "edeg_b": edeg_b,
    }


def one_run(start_seed: int, event_seed: int, steps: int, params: "sim.Params") -> Dict[str, object]:
    random.seed(start_seed)
    s = sim.init_state()
    random.seed(event_seed)
    for _ in range(steps):
        sim.gillespie_step(s, params)
    rng = random.Random(event_seed ^ 0x5DEECE66)
    ch = extract_channels(s.g, s.tokens, rng)
    ch["_events"] = s.event_count
    return ch


ARMS = {
    # strong arm: used ONLY to establish that the instrument responds at all
    # (positive reference). p_triadic_closure directly drives triangle creation.
    "strong": ("p_triadic_closure", 0.02, 0.30),
    # weak arm: the actual search target. p_local_rewire moves an edge endpoint
    # without changing |E|; its coarse signature is not obvious a priori.
    "weak": ("p_local_rewire", 0.03, 0.09),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=sorted(ARMS), required=True)
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--train-seeds", type=int, default=24)
    ap.add_argument("--holdout-seeds", type=int, default=24)
    ap.add_argument("--out", default=os.path.join(HERE, "..", "_cache"))
    ap.add_argument("--seed-base", type=int, default=0,
                    help="offset for start seeds; a non-zero value produces an "
                         "independent replication set")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    field, lo, hi = ARMS[args.arm]
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"substrate_{args.arm}{args.tag}.json")

    splits = {
        "train": [1000 + args.seed_base + i for i in range(args.train_seeds)],
        "holdout": [9000 + args.seed_base + i for i in range(args.holdout_seeds)],
    }

    records = []
    t0 = time.time()
    for split, seeds in splits.items():
        for s in seeds:
            for level_name, level_value in (("lo", lo), ("hi", hi)):
                p = sim.Params(**{field: level_value})
                ev = s * 7919 + (1 if level_name == "hi" else 0)
                ch = one_run(s, ev, args.steps, p)
                records.append(
                    {
                        "split": split,
                        "start_seed": s,
                        "event_seed": ev,
                        "level": level_name,
                        "arm_field": field,
                        "arm_value": level_value,
                        "channels": ch,
                    }
                )
                print(
                    f"[{time.time()-t0:7.1f}s] {args.arm} {split} seed={s} {level_name} "
                    f"n={ch['n']:.0f} m={ch['m']:.0f}",
                    flush=True,
                )

    meta = {
        "arm": args.arm,
        "arm_field": field,
        "levels": {"lo": lo, "hi": hi},
        "steps": args.steps,
        "sim_source": "relational_universe_sim.py",
        "generated_unix": time.time(),
        "n_records": len(records),
        "paired": True,
        "note": "instrumentation only; no physics claim",
    }
    with open(out_path, "w") as f:
        json.dump({"meta": meta, "records": records}, f)
    print(f"wrote {out_path} ({len(records)} records, {time.time()-t0:.1f}s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
