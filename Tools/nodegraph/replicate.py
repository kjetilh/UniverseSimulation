#!/usr/bin/env python3
"""
replicate.py -- evaluate the ONE pre-registered winner on fresh seeds.

Selection happened in run_experiment.py and is finished. Nothing here searches,
re-ranks or re-tunes; the expression is read from the experiment record and the
only new information is a set of start seeds that did not exist when it was
chosen. This is the repo's own fresh-seed standard applied to an observable
instead of to a mechanism.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "arena"))

import core, library  # noqa: E402
import observable_purpose as OP  # noqa: E402

REG = library.REGISTRY


def perm_p(d, observed, reps=20000, seed=13):
    rng = random.Random(seed)
    ge = sum(1 for s in OP.permuted_scores(d, reps, rng) if s >= observed - 1e-12)
    return (ge + 1.0) / (reps + 1.0)


def report(name, expr, prs, reps=20000):
    g = core.parse(REG, OP.CHANNELS, expr)
    d = OP.deltas(g, prs)
    s = OP.paired_score(d)
    return {
        "name": name, "expr": expr, "score": s,
        "permutation_p": perm_p(d, s, reps),
        "n_pairs": len(prs), "median_delta": OP._median(d),
        "sign_positive": sum(1 for x in d if x > 0), 
    }


def main():
    with open(os.path.join(HERE, "_cache", "experiment.json")) as f:
        exp = json.load(f)
    winner = exp["search_run"]["winner_expr"]

    rep = OP.load("weak_rep")
    prs = OP.pairs(rep, "train")
    base = OP.load("weak")

    out = {"winner_expr": winner, "replication_seeds": sorted(
        {r["start_seed"] for r in rep["records"]}), "rows": []}

    sets = [("selection(train)", OP.pairs(base, "train")),
            ("holdout", OP.pairs(base, "holdout")),
            ("replication(fresh)", prs)]

    for split, ps in sets:
        row = report(f"WINNER @ {split}", winner, ps)
        out["rows"].append(row)
    for name, expr in OP.BASELINES.items():
        out["rows"].append(report(f"{name} @ replication", expr, prs))

    # is the winner just a monotone re-spelling of beta1?
    gw = core.parse(REG, OP.CHANNELS, winner)
    gb = core.parse(REG, OP.CHANNELS, "beta1")
    xs, ys = [], []
    for lo, hi in prs:
        for env in (lo, hi):
            xs.append(float(gw.evaluate(env)))
            ys.append(float(gb.evaluate(env)))
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy) if sx > 0 and sy > 0 else 0.0
    rx = sorted(range(n), key=lambda i: xs[i])
    ry = sorted(range(n), key=lambda i: ys[i])
    rank_x = [0] * n
    rank_y = [0] * n
    for k, i in enumerate(rx):
        rank_x[i] = k
    for k, i in enumerate(ry):
        rank_y[i] = k
    mrx = mry = (n - 1) / 2
    srx = math.sqrt(sum((v - mrx) ** 2 for v in rank_x))
    sry = math.sqrt(sum((v - mry) ** 2 for v in rank_y))
    rho = sum((a - mrx) * (b - mry) for a, b in zip(rank_x, rank_y)) / (srx * sry)
    out["winner_vs_beta1"] = {"pearson_r": r, "spearman_rho": rho,
                              "note": "computed on the replication set only"}

    with open(os.path.join(HERE, "_cache", "replication.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(f"winner: {winner}\n")
    print(f"{'':34s}{'score':>8s}{'perm p':>10s}{'signs+':>8s}{'n':>4s}")
    for row in out["rows"]:
        print(f"{row['name']:34s}{row['score']:8.3f}{row['permutation_p']:10.4f}"
              f"{row['sign_positive']:8d}{row['n_pairs']:4d}")
    print(f"\nwinner vs beta1 on replication: pearson={r:.4f} spearman={rho:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
