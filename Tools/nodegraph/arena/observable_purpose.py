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

CACHE = os.path.join(HERE, "..", "_cache")

CHANNELS: Tuple[Tuple[str, str], ...] = (
    ("n", REAL), ("m", REAL), ("beta1", REAL),
    ("deg", VEC), ("tri", VEC), ("clus", VEC),
    ("b1", VEC), ("b2", VEC), ("b3", VEC),
    ("comp", VEC), ("tokdeg", VEC), ("edeg_a", VEC), ("edeg_b", VEC),
)

SCORE_CAP = 50.0
EPS = 1e-12


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


def _median(x: Sequence[float]) -> float:
    y = sorted(x)
    n = len(y)
    if n == 0:
        return 0.0
    return y[n // 2] if n % 2 else 0.5 * (y[n // 2 - 1] + y[n // 2])


def paired_score(d: Sequence[float]) -> float:
    if not d:
        return 0.0
    n = len(d)
    c = quantile([abs(x) for x in d], 0.90)
    if c <= 0.0:
        return 0.0
    dd = [max(-c, min(c, x)) for x in d]
    mean = sum(dd) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in dd) / n)
    return min(abs(mean) * math.sqrt(n) / (sd + EPS), SCORE_CAP)


def permuted_scores(d: Sequence[float], reps: int, rng: random.Random) -> List[float]:
    out = []
    for _ in range(reps):
        flipped = [x if rng.random() < 0.5 else -x for x in d]
        out.append(paired_score(flipped))
    return out


def quantile(xs: Sequence[float], q: float) -> float:
    y = sorted(xs)
    if not y:
        return 0.0
    k = int(math.floor(q * (len(y) - 1) + 0.5))
    return y[max(0, min(len(y) - 1, k))]


def null_references(all_deltas: Sequence[Sequence[float]], reps: int = 2000,
                    seed: int = 20260908) -> Dict[str, float]:
    """Two measured nulls, for the two different decisions being made.

    null_single  -- the 95th percentile score of ONE pre-specified observable
                    under label permutation. This is the gate for the holdout,
                    where exactly one winner is evaluated.
    null_search  -- the 95th percentile of the MAXIMUM score over the whole
                    candidate set under label permutation. This is the gate for
                    selection, where thousands of candidates are examined and
                    the best one is kept.
    """
    rng = random.Random(seed)
    singles: List[float] = []
    maxima: List[float] = []
    for _ in range(reps):
        signs = None
        best = 0.0
        for k, d in enumerate(all_deltas):
            if signs is None or len(signs) != len(d):
                signs = [1.0 if rng.random() < 0.5 else -1.0 for _ in d]
            s = paired_score([x * y for x, y in zip(d, signs)])
            if k == 0:
                singles.append(s)
            best = max(best, s)
        maxima.append(best)
    return {
        "null_single_p95": quantile(singles, 0.95),
        "null_search_p95": quantile(maxima, 0.95),
        "reps": reps,
    }


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


# ---------------------------------------------------------------- fast nulls
def null_references_np(all_deltas, reps: int = 2000, seed: int = 20260908) -> Dict[str, float]:
    """Same two nulls as null_references, computed with numpy when available.

    The speedup rests on an exact algebraic fact rather than an approximation:
    the winsorising threshold is a quantile of |d|, and flipping signs does not
    change |d|. So the clipped matrix can be formed ONCE and every permutation
    is a pure sign multiplication. Pure-Python and numpy paths therefore compute
    the same numbers, which tests/test_nodegraph.py checks.
    """
    try:
        import numpy as np
    except Exception:
        return null_references(all_deltas, reps=reps, seed=seed)

    lens = {len(d) for d in all_deltas}
    if len(lens) != 1:
        return null_references(all_deltas, reps=reps, seed=seed)
    n = lens.pop()
    D = np.asarray(all_deltas, dtype=float)
    A = np.abs(D)
    k = int(math.floor(0.90 * (n - 1) + 0.5))
    c = np.sort(A, axis=1)[:, max(0, min(n - 1, k))]
    dead = c <= 0.0
    c_safe = np.where(dead, 1.0, c)
    Dc = np.clip(D, -c_safe[:, None], c_safe[:, None])

    rng = np.random.default_rng(seed)
    singles = np.empty(reps)
    maxima = np.empty(reps)
    chunk = max(1, min(reps, int(4e7 // max(1, D.size))))
    done = 0
    while done < reps:
        b = min(chunk, reps - done)
        S = rng.choice(np.array([-1.0, 1.0]), size=(b, n))
        P = Dc[None, :, :] * S[:, None, :]
        mean = P.mean(axis=2)
        sd = P.std(axis=2)
        sc = np.minimum(np.abs(mean) * math.sqrt(n) / (sd + EPS), SCORE_CAP)
        sc[:, dead] = 0.0
        singles[done:done + b] = sc[:, 0]
        maxima[done:done + b] = sc.max(axis=1)
        done += b
    return {
        "null_single_p95": float(np.quantile(singles, 0.95, method="nearest")),
        "null_search_p95": float(np.quantile(maxima, 0.95, method="nearest")),
        "reps": reps,
        "backend": "numpy",
    }


# --------------------------------------------------- transform-invariant test
def sign_test(d: Sequence[float]) -> Dict[str, float]:
    """Exact two-sided sign test on the paired differences.

    This is here because of what section 4.3 of the assessment found: every
    monotone transform of a positive observable has the SAME sign vector, so the
    winsorised studentized statistic can rise a long way -- 2.64 to 3.44 on the
    holdout -- while the directional evidence is bit-for-bit unchanged. An
    expression space is full of monotone transforms, so a search will climb that
    direction by default. Reporting this number next to the weighted one is what
    stops a reparameterisation from being read as a finding.
    """
    pos = sum(1 for x in d if x > 0)
    n = sum(1 for x in d if x != 0)
    if n == 0:
        return {"positive": 0, "n": 0, "p": 1.0, "signs": ()}
    tail = min(pos, n - pos)
    c = 0
    for k in range(tail + 1):
        c += math.comb(n, k)
    return {
        "positive": pos, "n": n,
        "p": min(1.0, 2.0 * c / (2 ** n)),
        "signs": tuple(1 if x > 0 else (-1 if x < 0 else 0) for x in d),
    }
