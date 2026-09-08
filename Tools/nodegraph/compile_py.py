#!/usr/bin/env python3
"""compile_py.py -- graph -> straight-line Python closure.

The cheapest backend. It removes the interpreter's per-node dispatch by
emitting SSA assignments over the op implementations directly. Shared
subexpressions are computed once, which is what hash-consing bought.
"""
from __future__ import annotations

from typing import Callable, Dict, List

from core import Graph, inline


def to_source(graph: Graph, fname: str = "compiled") -> str:
    g = inline(graph)
    order = g.reachable()
    args = ", ".join(name for name, _ in g.signature)
    lines = [f"def {fname}({args}):"]
    for i in order:
        nd = g.nodes[i]
        if nd.kind == "input":
            lines.append(f"    t{i} = {nd.payload}")
        elif nd.kind == "const":
            lines.append(f"    t{i} = {nd.payload!r}")
        else:
            call = ", ".join(f"t{a}" for a in nd.args)
            lines.append(f"    t{i} = _op_{_sym(nd.payload)}({call})")
    lines.append(f"    return t{g.root}")
    return "\n".join(lines)


def _sym(name: str) -> str:
    return name.replace(".", "_")


def compile_graph(graph: Graph) -> Callable:
    g = inline(graph)
    ns: Dict[str, object] = {}
    for i in g.reachable():
        nd = g.nodes[i]
        if nd.kind == "op":
            ns[f"_op_{_sym(nd.payload)}"] = g.registry.ops[nd.payload].py
    src = to_source(g)
    exec(compile(src, "<nodegraph>", "exec"), ns)
    fn = ns["compiled"]
    fn.source = src  # type: ignore[attr-defined]
    return fn
