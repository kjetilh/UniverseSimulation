#!/usr/bin/env python3
"""
minimal_purpose.py -- the smallest complete use of this framework.

Copy this file, replace the five marked blocks, and you have pointed the search
at a new problem. Nothing here touches the simulator; the data is synthetic and
the effect is planted, so you can see the machinery answer correctly on a
question whose answer is already known.

The planted effect is a small change in the SHAPE of x's upper tail. On top of
it sits a per-pair random rescaling of the whole sample, which is much larger
than the effect. So every observable that carries the scale -- mean, q90, max --
is swamped, and only a scale-invariant shape statistic can see the planting.
That is deliberate: it is the case where the obvious hand-picked observable
fails and the search has to earn its keep. The nuisance channel `n` is identical
in both arms and must score like noise.

Run:  python3 examples/minimal_purpose.py
"""
from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import compile_c, core, library, stats  # noqa: E402
from core import BOOL, REAL, VEC  # noqa: E402
from purpose import PurposeContract, Reference  # noqa: E402
from search import Enumerator  # noqa: E402

REG = library.REGISTRY

# ---- 1. CHANNELS: what a candidate is allowed to look at --------------------
CHANNELS = (("x", VEC), ("n", REAL))


# ---- 2. DATA: paired samples. Both arms share a seed, so the nuisance -------
#        variation between seeds cancels in the difference.
def make_pairs(seeds, stretch: float):
    out = []
    for s in seeds:
        rng = random.Random(s)
        base = sorted(rng.lognormvariate(0.0, 0.8) for _ in range(120))
        cut = int(0.85 * len(base))
        lo = list(base)
        hi = base[:cut] + [v * stretch for v in base[cut:]]
        # the nuisance: a common rescaling of one arm, far larger than the
        # effect and with a random sign. Anything that carries scale drowns.
        scale = rng.uniform(0.75, 1.35)
        hi = [v * scale for v in hi]
        rng.shuffle(lo)
        rng.shuffle(hi)
        out.append(({"x": lo, "n": float(len(lo))}, {"x": hi, "n": float(len(hi))}))
    return out


TRAIN = make_pairs(range(100, 124), stretch=1.035)    # the real, subtle arm
HOLDOUT = make_pairs(range(900, 924), stretch=1.035)  # never used to select
STRONG = make_pairs(range(500, 512), stretch=1.60)    # positive reference arm


# ---- 3. STATISTIC: reused as-is from stats.py; do not invent a new one ------
def deltas(graph, prs):
    out = []
    for lo, hi in prs:
        a, b = graph.evaluate(hi), graph.evaluate(lo)
        out.append(float(a) - float(b))
    return out


def main() -> int:
    probes = [e for pr in TRAIN[:3] for e in pr]
    cands = Enumerator(REG, CHANNELS, probes,
                       max_per_type={REAL: 2500, VEC: 60, BOOL: 40}
                       ).enumerate(depth=2)[REAL]
    rows = [(c, deltas(c.graph, TRAIN)) for c in cands]
    rows = [(c, d, stats.paired_score(d)) for c, d in rows]

    # ---- 4. REFERENCES: both MEASURED, never assumed -----------------------
    nulls = stats.null_references_np([r[1] for r in rows], reps=2000)
    strong = max(stats.paired_score(deltas(c.graph, STRONG)) for c, _, _ in rows)

    contract = PurposeContract(
        id="tail_effect_demo",
        statement="Find an observable of x whose paired response to the arm "
                  "beats what the same search achieves on permuted labels, and "
                  "keeps it on seeds it was not selected on.",
        signature=CHANNELS, output_type=REAL,
        score=lambda g: stats.paired_score(deltas(g, TRAIN)),
        holdout=lambda g: stats.paired_score(deltas(g, HOLDOUT)),
        null_reference=Reference("null", nulls["null_search_p95"],
                                 "95th pct of max score over the candidate set "
                                 "under arm-label permutation", "this file"),
        positive_reference=Reference("positive", strong,
                                     "best score of the same search on an arm "
                                     "where the effect is 1.80x", "this file"),
    )
    # ---- 5. INVARIANT COMPANION: catches a monotone re-spelling ------------
    contract.invariant = lambda g: (
        lambda r: (r["p"], r["signs"])
    )(stats.sign_test(deltas(g, HOLDOUT)))
    contract.reference_graph = core.parse(REG, CHANNELS, "q90(x)")

    v = contract.admissibility()
    print(f"contract admissible : {bool(v)}  (positive {strong:.2f} / null "
          f"{nulls['null_search_p95']:.2f} = {v.separation:.1f}x)")
    if not v:
        for r in v.reasons:
            print("  refused:", r)
        return 1

    rows.sort(key=lambda r: (-r[2], r[0].cost))
    winner = rows[0][0].graph
    res = contract.evaluate(winner)

    print(f"candidates          : {len(rows)}")
    print(f"winner              : {res['expr']}")
    print(f"train {res['selection_score']:7.3f}  vs selection gate "
          f"{res['gate_threshold']:.3f}  -> "
          f"{'PASS' if res['passes_selection'] else 'FAIL'}")
    hn = stats.quantile(stats.permuted_scores(deltas(winner, HOLDOUT), 2000,
                                              random.Random(1)), 0.95)
    print(f"holdout {res['holdout_score']:5.3f}  vs holdout gate  {hn:.3f}  -> "
          f"{'PASS' if res['holdout_score'] > hn else 'FAIL'}")
    print(f"sign-test p         : {res['invariant_p']:.5f}  "
          f"(reference q90(x): {res['reference_invariant_p']:.5f})")
    print(f"transform_only      : {res['transform_only']}"
          + ("   <- same sign vector as the reference: no new direction, "
             "only reweighting" if res["transform_only"] else ""))

    print("\nsanity, on the holdout:")
    for name, e in (("scale-carrying", "q90(x)"), ("blunt", "mean(x)"),
                    ("shape, invariant", "entropy(x)"), ("nuisance", "n")):
        g = core.parse(REG, CHANNELS, e)
        print(f"  {name:15s} {e:10s} {stats.paired_score(deltas(g, HOLDOUT)):6.3f}")

    c = compile_c.certify(winner)
    print(f"\nC backend certified : {c.conformance['failures']} disagreements "
          f"in {c.conformance['trials']} random trials")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
