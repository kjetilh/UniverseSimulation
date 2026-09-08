#!/usr/bin/env python3
"""
demo_compile.py -- take the graph the search selected and lower it, without
changing what it means.

Three things are demonstrated on one real artefact:
  1. a found graph becomes a named COMPOSITE node and can be used as a node
  2. the composite is INLINED and lowered to C, and refuses to be handed back
     unless it agrees with the reference interpreter on random inputs
  3. the speedup is measured twice -- once end to end through the ctypes
     boundary, once with the input already on the C side -- because those are
     different numbers and only the second one is the compiler's doing.
"""
from __future__ import annotations

import ctypes
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "arena"))

import compile_c, compile_py, core, library  # noqa: E402
import observable_purpose as OP  # noqa: E402
from core import Composite  # noqa: E402

REG = library.REGISTRY


def bench(fn, n, *a, **kw):
    t = time.perf_counter()
    for _ in range(n):
        fn(*a, **kw)
    return time.perf_counter() - t


def main():
    with open(os.path.join(HERE, "_cache", "experiment.json")) as f:
        expr = json.load(f)["search_run"]["winner_expr"]
    print(f"selected graph: {expr}\n")

    g = core.parse(REG, OP.CHANNELS, expr)

    # 1. promote it to a node in the library
    REG.add_composite(Composite("found.arm_observable", g,
                                doc="observable selected by the depth-3 search"))
    op = REG.ops["found.arm_observable"]
    print(f"composite registered: {op.name}")
    print(f"  declares {len(op.inputs)} inputs {op.inputs} -> {op.output}")

    user = core.parse(
        REG, OP.CHANNELS,
        "div(found.arm_observable(" + ", ".join(n for n, _ in OP.CHANNELS) + "), add(m, 1))",
    )
    print(f"  used as a node: {user.to_expr()[:90]}...")
    flat = core.inline(user)
    print(f"  inlined: {flat.size} nodes, depth {flat.depth}\n")

    # 2. lower it, and refuse anything that disagrees with the reference
    cf = compile_c.certify(g)
    print(f"C backend certified: {cf.conformance}")
    pf = compile_py.compile_graph(g)

    rec = OP.load("weak")["records"]
    env = {k: rec[0]["channels"][k] for k, _t in OP.CHANNELS}
    big = dict(env)
    big["tokdeg"] = list(env["tokdeg"]) * 400
    ref, py, c = g.evaluate(big), pf(**big), cf(**big)
    print(f"values agree: ref={ref!r} py={py!r} c={c!r}  "
          f"max diff {max(abs(ref-py), abs(ref-c)):.3e}\n")

    N = 20000
    t_ref = bench(lambda: g.evaluate(big), N)
    t_py = bench(lambda: pf(**big), N)
    t_c = bench(lambda: cf(**big), N)

    # same C code, input already marshalled: this isolates the compiler's gain
    # from the cost of crossing the language boundary every call
    scratch = (ctypes.c_double * (1 << 20))()
    arrs, args = [], [scratch, ctypes.c_long(1 << 20)]
    for name, t in g.signature:
        v = big[name]
        if t == "vec":
            a = (ctypes.c_double * max(1, len(v)))(*[float(x) for x in v] or [0.0])
            arrs.append(a)
            args += [a, ctypes.c_int(len(v))]
        else:
            args.append(ctypes.c_double(float(v)))
    t_c_hot = bench(lambda: cf.fn(*args), N)

    print(f"{N} evaluations of the same graph on |tokdeg|={len(big['tokdeg'])}")
    print(f"  reference interpreter      {t_ref*1e6/N:9.2f} us/call   1.00x")
    print(f"  python codegen             {t_py*1e6/N:9.2f} us/call  {t_ref/t_py:5.2f}x")
    print(f"  C, marshalling every call  {t_c*1e6/N:9.2f} us/call  {t_ref/t_c:5.2f}x")
    print(f"  C, input already resident  {t_c_hot*1e6/N:9.2f} us/call  {t_ref/t_c_hot:5.2f}x")

    out = {
        "expr": expr,
        "conformance": cf.conformance,
        "us_per_call": {
            "interpreter": t_ref * 1e6 / N, "python_codegen": t_py * 1e6 / N,
            "c_marshalled": t_c * 1e6 / N, "c_resident": t_c_hot * 1e6 / N,
        },
        "speedup_vs_interpreter": {
            "python_codegen": t_ref / t_py, "c_marshalled": t_ref / t_c,
            "c_resident": t_ref / t_c_hot,
        },
        "input_size": len(big["tokdeg"]),
        "iterations": N,
    }
    with open(os.path.join(HERE, "_cache", "compile_bench.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nC source ({len(cf.source)} chars) at {cf.so_path[:-3]}.c")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
