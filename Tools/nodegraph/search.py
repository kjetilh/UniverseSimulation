#!/usr/bin/env python3
"""
search.py -- bottom-up typed enumeration with observational deduplication.

Candidates are built level by level from the library. Two candidates that
produce identical values on every probe environment are the same function as
far as this arena can tell, so only the cheaper one survives. That single rule
is what keeps a combinatorial space tractable: most of an expression space is
re-spellings of the same function.

`Proposer` is the seam. The enumerator below is deterministic and costs no
tokens, so a result obtained with it does not depend on any model being
available or on how a prompt was phrased. A language-model proposer implements
the same two methods and is scored by exactly the same contract; that is the
only fair way to find out whether the model actually adds anything.
"""
from __future__ import annotations

import hashlib
import itertools
import math
import random
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

from core import BOOL, REAL, VEC, Builder, Graph, Registry, parse


def fingerprint(graph: Graph, probes: Sequence[Dict[str, object]]) -> Optional[str]:
    """Observational identity on the probe set. None if the value is degenerate."""
    h = hashlib.blake2b(digest_size=16)
    seen_any = False
    for env in probes:
        try:
            v = graph.evaluate(env)
        except Exception:
            return None
        if isinstance(v, list):
            if len(v) > 64:
                v = v[:32] + v[-32:]
            h.update(b"V")
            for x in v:
                h.update(f"{float(x):.9g}|".encode())
        else:
            x = 1.0 if v is True else (0.0 if v is False else float(v))
            if math.isnan(x) or math.isinf(x):
                return None
            if abs(x) > 1e-12:
                seen_any = True
            h.update(f"R{x:.9g}|".encode())
    if graph.output_type == REAL and not seen_any:
        return None  # identically zero on the whole arena: carries no information
    return h.hexdigest()


@dataclass
class Candidate:
    graph: Graph
    fp: str
    cost: float


class Proposer:
    """Interface. Implement these two and the contract does the rest."""

    def propose(self, budget: int) -> Iterable[Graph]:
        raise NotImplementedError

    def observe(self, graph: Graph, result: dict) -> None:
        """Feedback hook. The enumerator ignores it; a model proposer would not."""


class Enumerator(Proposer):
    def __init__(
        self,
        registry: Registry,
        signature: Sequence[Tuple[str, str]],
        probes: Sequence[Dict[str, object]],
        consts: Sequence[float] = (1.0, 2.0, 0.5),
        max_per_type: Dict[str, int] = None,
        seed: int = 20260908,
        budget: int = 4000,
        probe_trunc: int = 48,
    ):
        self.reg = registry
        self.sig = tuple(signature)
        # Fingerprinting runs on truncated copies of the real environments:
        # cheap enough to do millions of times, and still the actual arena data,
        # so two candidates judged equivalent really are equivalent on it.
        self.probes = [
            {k: (list(v)[:probe_trunc] if isinstance(v, list) else v) for k, v in env.items()}
            for env in probes
        ]
        self.consts = list(consts)
        self.caps = max_per_type or {REAL: 9000, VEC: 130, BOOL: 60}
        self.budget = budget
        self.rng = random.Random(seed)

    def _mk(self, build) -> Optional[Candidate]:
        b = Builder(self.reg, self.sig)
        try:
            root = build(b)
        except Exception:
            return None
        g = b.finish(root)
        fp = fingerprint(g, self.probes)
        if fp is None:
            return None
        return Candidate(g, fp, g.cost() + 0.01 * g.size)

    # -- staged enumeration ------------------------------------------------
    # Blind level-by-level products explode: at depth 1 this library already
    # yields a few hundred vectors, and their cross product with every binary op
    # is millions of mostly-equivalent expressions. The staging below follows
    # the shape of the domain instead -- build vector pipelines, reduce them to
    # scalars, then do scalar algebra -- and samples inside each stage under an
    # explicit budget. It is a heuristic about search order, not about meaning:
    # nothing here can change what a graph computes.
    def _seed_pool(self, seen):
        base = {REAL: [], VEC: [], BOOL: []}
        for name, t in self.sig:
            c = self._mk(lambda b, n=name: b.input(n))
            if c and c.fp not in seen:
                seen[c.fp] = c
                base[t].append(c)
        for v in self.consts:
            c = self._mk(lambda b, x=v: b.const(x, REAL))
            if c and c.fp not in seen:
                seen[c.fp] = c
                base[REAL].append(c)
        return base

    def _apply_ops(self, ops, pools, seen, budget, require_new=None):
        out = []
        for op in ops:
            arg_pools = [pools[t] for t in op.inputs]
            if any(len(p) == 0 for p in arg_pools):
                continue
            sizes = [len(p) for p in arg_pools]
            total = 1
            for x in sizes:
                total *= x
            if total <= budget:
                combos = itertools.product(*arg_pools)
            else:
                combos = (
                    tuple(self.rng.choice(p) for p in arg_pools) for _ in range(budget)
                )
            for combo in combos:
                if require_new is not None and not any(id(c) in require_new for c in combo):
                    continue
                cand = self._build(op.name, combo)
                if cand is None or cand.fp in seen:
                    continue
                seen[cand.fp] = cand
                out.append(cand)
        return out

    def _trim(self, cands, cap):
        """Keep the cheapest half and a random sample of the rest, so the pool
        stays small without collapsing onto trivial expressions."""
        if len(cands) <= cap:
            return cands
        cands = sorted(cands, key=lambda c: c.cost)
        keep = cands[: cap // 2]
        rest = cands[cap // 2:]
        self.rng.shuffle(rest)
        return keep + rest[: cap - len(keep)]

    def enumerate(self, depth: int = 3, verbose: bool = False) -> Dict[str, List[Candidate]]:
        seen: Dict[str, Candidate] = {}
        pools = self._seed_pool(seen)
        vec_ops = [o for o in self.reg.ops.values() if o.output == VEC]
        red_ops = [o for o in self.reg.ops.values() if o.output == REAL and VEC in o.inputs]
        sca_ops = [o for o in self.reg.ops.values()
                   if o.output == REAL and o.inputs and VEC not in o.inputs]
        bool_ops = [o for o in self.reg.ops.values() if o.output == BOOL]
        sel_ops = [o for o in self.reg.ops.values() if o.output == REAL and BOOL in o.inputs]

        # stage 1: vector pipelines
        for k in range(max(1, depth - 1)):
            fresh = self._apply_ops(vec_ops, pools, seen, self.budget)
            fresh = self._trim(fresh, self.caps[VEC])
            pools[VEC] = self._trim(pools[VEC] + fresh, self.caps[VEC])
            if verbose:
                print(f"  vec stage {k+1}: +{len(fresh)} -> {len(pools[VEC])}", flush=True)

        # stage 2: reductions to scalars
        red = self._apply_ops(red_ops, pools, seen, self.budget)
        pools[REAL] = self._trim(pools[REAL] + red, self.caps[REAL])
        if verbose:
            print(f"  reductions: +{len(red)} -> {len(pools[REAL])}", flush=True)

        # stage 3: scalar algebra
        for k in range(max(1, depth - 1)):
            fresh = self._apply_ops(sca_ops, pools, seen, self.budget)
            fresh = self._trim(fresh, self.caps[REAL])
            pools[REAL] = self._trim(pools[REAL] + fresh, self.caps[REAL])
            if verbose:
                print(f"  scalar stage {k+1}: +{len(fresh)} -> {len(pools[REAL])}", flush=True)

        # stage 4: predicates and selection, so the space contains conditionals
        bl = self._apply_ops(bool_ops, pools, seen, min(self.budget, 400))
        pools[BOOL] = self._trim(pools[BOOL] + bl, self.caps[BOOL])
        sel = self._apply_ops(sel_ops, pools, seen, min(self.budget, 1500))
        pools[REAL] = self._trim(pools[REAL] + sel, self.caps[REAL])
        if verbose:
            print(f"  predicates: bool={len(pools[BOOL])} selected reals +{len(sel)} "
                  f"-> {len(pools[REAL])}", flush=True)
        return pools

    def _build(self, op_name: str, combo: Sequence[Candidate]) -> Optional[Candidate]:
        b = Builder(self.reg, self.sig)
        memo: Dict[int, int] = {}

        def graft(src: Graph, i: int, tag: int) -> int:
            k = (tag, i)
            if k in memo:
                return memo[k]
            nd = src.nodes[i]
            if nd.kind == "input":
                j = b.input(nd.payload)
            elif nd.kind == "const":
                j = b.const(nd.payload, nd.type)
            else:
                j = b.apply(nd.payload, *(graft(src, a, tag) for a in nd.args))
            memo[k] = j
            return j

        try:
            args = [graft(c.graph, c.graph.root, t) for t, c in enumerate(combo)]
            root = b.apply(op_name, *args)
        except Exception:
            return None
        g = b.finish(root)
        fp = fingerprint(g, self.probes)
        if fp is None:
            return None
        return Candidate(g, fp, g.cost() + 0.01 * g.size)

    def propose(self, budget: int, depth: int = 3, verbose: bool = False) -> List[Graph]:
        pool = self.enumerate(depth=depth, verbose=verbose)
        out = [c.graph for c in pool[REAL]]
        self.rng.shuffle(out)
        return out[:budget]
