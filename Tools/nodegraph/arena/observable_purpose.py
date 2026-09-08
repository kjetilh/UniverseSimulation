#!/usr/bin/env python3
"""
observable_purpose.py -- the purpose the search is pointed at, in this arena.

The purpose, in words:

    Find a scalar observable of a final simulation graph whose PAIRED response
    to a change in the rewrite rule is larger than what the same search
    procedure achieves when the arm labels carry no information, and which
    keeps that response on seeds never used to select it.

Why this purpose and not a prettier one: it is the quantity the v17 series
needed and did not have. v17 gated on a ratio whose variance was 99.8% explained
by which start pair was drawn and 0.1% by the kernel arm it was meant to test
(v17_program_closure.md, section 2). The statistic below is paired -- both arm
levels share a start state -- so start-family variance cancels by construction
rather than by hope, and the null is measured rather than assumed.

Statistic (fixed before any candidate was scored):
    d_s   = O(hi_s) - O(lo_s)                              for each start seed s
    d~    = d clipped symmetrically at the 90th percentile of |d|
    score = |mean(d~)| * sqrt(n) / (sd(d~) + eps)          capped at 50

It is a paired studentized mean on winsorised differences. The sqrt(n) is
deliberate: an effect size alone has almost no power against a small but
perfectly consistent response, which is the alternative that matters here. The
symmetric clipping keeps one exploding pair from carrying the whole statistic
and is sign-symmetric, so the permutation null stays exact. The absolute scale
of the number is meaningless and is never used -- every score is read against a
permutation null measured on the same pairs.

Permuting the arm labels within a pair is exactly flipping the sign of d_s, so
the null distribution is obtained from the same d vectors at no extra cost, and
the max-over-candidates null controls the multiple-comparison problem that a
search over thousands of expressions otherwise creates.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
from typing import Dict, List, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from core import REAL, VEC, Graph  # noqa: E402
from stats import (  # noqa: E402  re-exported: the arena is one caller, not the owner
    EPS, SCORE_CAP, _median, null_references, null_references_np,
    paired_score, permuted_scores, quantile, sign_test,
)

CACHE = os.path.join(HERE, "..", "_cache")

CHANNELS: Tuple[Tuple[str, str], ...] = (
    ("n", REAL), ("m", REAL), ("beta1", REAL),
    ("deg", VEC), ("tri", VEC), ("clus", VEC),
    ("b1", VEC), ("b2", VEC), ("b3", VEC),
    ("comp", VEC), ("tokdeg", VEC), ("edeg_a", VEC), ("edeg_b", VEC),
)



def load(arm: str) -> dict:
    """Substrates are committed gzipped; a plain .json wins if it is present,
    so a freshly generated one is picked up without an extra step."""
    base = os.path.join(CACHE, f"substrate_{arm}.json")
    if os.path.exists(base):
        with open(base) as f:
            return json.load(f)
    import gzip
    with gzip.open(base + ".gz", "rt") as f:
        return json.load(f)


def pairs(data: dict, split: str) -> List[Tuple[Dict, Dict]]:
    """(lo_env, hi_env) per start seed, in seed order."""
    by: Dict[int, Dict[str, Dict]] = {}
    for r in data["records"]:
        if r["split"] != split:
            continue
        by.setdefault(r["start_seed"], {})[r["level"]] = r["channels"]
    out = []
    for s in sorted(by):
        d = by[s]
        if "lo" in d and "hi" in d:
            out.append((d["lo"], d["hi"]))
    return out


def deltas(graph: Graph, prs: Sequence[Tuple[Dict, Dict]]) -> List[float]:
    out = []
    for lo, hi in prs:
        a = graph.evaluate(hi)
        b = graph.evaluate(lo)
        a = 1.0 if a is True else (0.0 if a is False else float(a))
        b = 1.0 if b is True else (0.0 if b is False else float(b))
        v = a - b
        out.append(0.0 if (math.isnan(v) or math.isinf(v)) else v)
    return out


BASELINES = {
    "n": "n",
    "m": "m",
    "beta1": "beta1",
    "mean_deg": "mean(deg)",
    "mean_clus": "mean(clus)",
    "mean_tri": "mean(tri)",
    "max_deg": "vmax(deg)",
    "mean_b2": "mean(b2)",
    "edge_density": "div(m, n)",
    "assortativity": "corr(edeg_a, edeg_b)",
}

