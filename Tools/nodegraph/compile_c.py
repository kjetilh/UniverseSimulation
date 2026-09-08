#!/usr/bin/env python3
"""compile_c.py -- graph -> C, built with the system compiler, called via ctypes.

This backend exists to test one specific claim: that a graph that has been
found to work can be turned into a materially faster artefact WITHOUT changing
what it means. The second half of that sentence is the hard half, so nothing
here is trusted until `conformance` has compared the compiled artefact against
core.Graph.evaluate on random inputs. A backend that has not passed conformance
is reported as uncertified and must not be used.

Limits, stated rather than hidden:
  * output type must be real or bool (a vec-valued graph is not compiled)
  * every op on the reachable path must declare a C runtime function
  * the arena is sized from the input; deeper vec pipelines need a bigger one
"""
from __future__ import annotations

import ctypes
import hashlib
import os
import random
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from core import BOOL, REAL, VEC, Graph, inline
from library import c_runtime

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache", "cbuild")


class NotCompilable(Exception):
    pass


def to_source(graph: Graph) -> str:
    g = inline(graph)
    if g.output_type == VEC:
        raise NotCompilable("C backend returns a scalar; graph output type is 'vec'")

    bad = sorted(
        {
            g.nodes[i].payload
            for i in g.reachable()
            if g.nodes[i].kind == "op" and not g.registry.ops[g.nodes[i].payload].c_fn
        }
    )
    if bad:
        raise NotCompilable(f"no C runtime for ops: {', '.join(bad)}")

    params: List[str] = []
    for name, t in g.signature:
        if t == VEC:
            params.append(f"double* {name}_d, int {name}_n")
        else:
            params.append(f"double {name}")

    body: List[str] = []
    for i in g.reachable():
        nd = g.nodes[i]
        ct = "nv_vec" if nd.type == VEC else "double"
        if nd.kind == "input":
            if nd.type == VEC:
                body.append(f"  nv_vec t{i}; t{i}.d={nd.payload}_d; t{i}.n={nd.payload}_n;")
            else:
                body.append(f"  double t{i} = {nd.payload};")
        elif nd.kind == "const":
            v = float(nd.payload) if not isinstance(nd.payload, bool) else (1.0 if nd.payload else 0.0)
            body.append(f"  double t{i} = {v!r};")
        else:
            op = g.registry.ops[nd.payload]
            needs_arena = VEC in op.inputs or op.output == VEC
            call_args = ["ar"] if needs_arena else []
            for a in nd.args:
                call_args.append(f"t{a}")
            body.append(f"  {ct} t{i} = {op.c_fn}({', '.join(call_args)});")

    src = [c_runtime(), "", f"double nv_main(nv_arena* ar, {', '.join(params) or 'void'}) {{"]
    src.extend(body)
    src.append(f"  return t{g.root};")
    src.append("}")
    src.append(
        """
double nv_entry(double* scratch, long scratch_n, %s) {
  nv_arena ar; ar.buf=scratch; ar.used=0; ar.cap=scratch_n;
  return nv_main(&ar%s);
}
"""
        % (
            ", ".join(params) or "void",
            "".join(
                f", {n}_d, {n}_n" if t == VEC else f", {n}" for n, t in g.signature
            ),
        )
    )
    return "\n".join(src)


@dataclass
class CompiledC:
    fn: object
    signature: Tuple[Tuple[str, str], ...]
    so_path: str
    source: str
    certified: bool = False
    conformance: Optional[dict] = None

    def __call__(self, **env):
        scratch_n = 1 << 20
        scratch = (ctypes.c_double * scratch_n)()
        args = [scratch, ctypes.c_long(scratch_n)]
        keep = []
        for name, t in self.signature:
            v = env[name]
            if t == VEC:
                arr = (ctypes.c_double * max(1, len(v)))(*[float(x) for x in v] or [0.0])
                keep.append(arr)
                args.append(arr)
                args.append(ctypes.c_int(len(v)))
            else:
                args.append(ctypes.c_double(1.0 if v is True else (0.0 if v is False else float(v))))
        out = self.fn(*args)
        return bool(out) if _root_type(self) == BOOL else out


def _root_type(c: CompiledC) -> str:
    return getattr(c, "_root_type", REAL)


def compile_graph(graph: Graph, cc: str = "gcc", opt: str = "-O2") -> CompiledC:
    src = to_source(graph)
    os.makedirs(CACHE, exist_ok=True)
    h = hashlib.sha256((src + cc + opt).encode()).hexdigest()[:16]
    so = os.path.join(CACHE, f"nv_{h}.so")
    cpath = os.path.join(CACHE, f"nv_{h}.c")
    if not os.path.exists(so):
        with open(cpath, "w") as f:
            f.write(src)
        r = subprocess.run(
            [cc, opt, "-shared", "-fPIC", "-o", so, cpath, "-lm"],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            raise NotCompilable(f"{cc} failed:\n{r.stderr[:2000]}")
    lib = ctypes.CDLL(so)
    fn = lib.nv_entry
    argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_long]
    for _name, t in graph.signature:
        if t == VEC:
            argtypes += [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        else:
            argtypes.append(ctypes.c_double)
    fn.argtypes = argtypes
    fn.restype = ctypes.c_double
    out = CompiledC(fn, tuple(graph.signature), so, src)
    out._root_type = graph.output_type  # type: ignore[attr-defined]
    return out


# ------------------------------------------------------------------ conformance
def random_env(signature, rng: random.Random) -> Dict[str, object]:
    env: Dict[str, object] = {}
    for name, t in signature:
        if t == VEC:
            n = rng.choice([0, 1, 2, 3, 7, 33, 128])
            env[name] = [rng.choice([rng.uniform(-50, 50), rng.uniform(0, 3), 0.0]) for _ in range(n)]
        elif t == BOOL:
            env[name] = rng.random() < 0.5
        else:
            env[name] = rng.choice([rng.uniform(-50, 50), 0.0, rng.uniform(0, 1e6)])
    return env


def conformance(graph: Graph, backend, trials: int = 400, seed: int = 20260908,
                rtol: float = 1e-9, atol: float = 1e-9) -> dict:
    """Compare a backend against core.Graph.evaluate. This is the certificate."""
    rng = random.Random(seed)
    worst = 0.0
    worst_env = None
    fails = 0
    for _ in range(trials):
        env = random_env(graph.signature, rng)
        ref = graph.evaluate(env)
        got = backend(**env) if not callable(getattr(backend, "fn", None)) else backend(**env)
        rf = 1.0 if isinstance(ref, bool) and ref else (0.0 if isinstance(ref, bool) else float(ref))
        gf = 1.0 if isinstance(got, bool) and got else (0.0 if isinstance(got, bool) else float(got))
        err = abs(rf - gf)
        tol = atol + rtol * abs(rf)
        if err > tol:
            fails += 1
            if err > worst:
                worst, worst_env = err, env
    return {
        "trials": trials,
        "failures": fails,
        "worst_abs_error": worst,
        "passed": fails == 0,
        "rtol": rtol,
        "atol": atol,
        "worst_env_sizes": None if worst_env is None else
            {k: (len(v) if isinstance(v, list) else v) for k, v in worst_env.items()},
    }


def certify(graph: Graph, **kw) -> CompiledC:
    """Compile and refuse to hand back anything that disagrees with the reference."""
    c = compile_graph(graph, **kw)
    rep = conformance(graph, c)
    c.conformance = rep
    c.certified = rep["passed"]
    if not c.certified:
        raise AssertionError(f"C backend disagrees with reference semantics: {rep}")
    return c
