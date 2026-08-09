"""Regression test: R_slide must preserve the cyclomatic number.

The research report claims beta_1 = |E| - |V| + C is an exact invariant under
{R_seed, R_slide}. On a *simple* graph the reference rewire move was doing
remove_edge(v,u) then add_edge(v,w); because add_edge is idempotent, an edge
was silently lost whenever (v,w) already existed, collapsing cyclic graphs to a
spanning tree (beta_1 -> 0). The DPO rule R_slide carries a negative
application condition (a,c) not in E that forbids exactly this collision.

This test drives the actual simulator with only R_seed + R_slide active
(p_triad = p_delete = 0) and asserts that beta_1 = |E| - |V| + C stays constant.
It FAILS on the pre-fix code and PASSES once the NAC is enforced.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import relational_universe_sim as sim


def _components(g) -> int:
    """Number of connected components of the current graph."""
    seen = set()
    comps = 0
    for start in g.nodes():
        if start in seen:
            continue
        comps += 1
        stack = [start]
        seen.add(start)
        while stack:
            v = stack.pop()
            for w in g.neighbors(v):
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return comps


def _beta1(g) -> int:
    return g.num_edges() - g.num_nodes() + _components(g)


def _run_seed_slide_only(steps: int, seed: int):
    import random

    random.seed(seed)
    params = sim.Params(
        r_token=1.0,
        r_seed=1.0,
        p_delete_traversed_edge=0.0,   # R_tri,open OFF
        p_triadic_closure=0.0,         # R_tri,close OFF
        p_local_rewire=1.0,            # R_slide ON
        r_token_birth=0.0,
        r_token_death=0.0,
    )
    state = sim.init_state(n0=30, m0=60, tokens0=10)
    beta_start = _beta1(state.g)
    trace = [beta_start]
    for i in range(steps):
        sim.gillespie_step(state, params)
        if i % 200 == 0:
            trace.append(_beta1(state.g))
    trace.append(_beta1(state.g))
    return beta_start, trace


def test_slide_preserves_cyclomatic_number():
    """beta_1 = |E| - |V| + C must be invariant under {R_seed, R_slide}."""
    for seed in (1, 7, 42):
        beta_start, trace = _run_seed_slide_only(steps=6000, seed=seed)
        assert beta_start > 0, "initial graph must contain cycles for the test to bite"
        assert all(b == beta_start for b in trace), (
            f"beta_1 drifted under seed+slide (seed={seed}): "
            f"start={beta_start}, trace={trace}"
        )
