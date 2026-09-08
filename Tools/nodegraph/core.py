#!/usr/bin/env python3
"""
core.py -- typed node graphs.

A NODE is a function definition: a name, a declared tuple of input types, a
declared output type, and a semantics. A GRAPH is a hash-consed DAG of such
nodes over named inputs and constants. Nothing here knows about universes,
purposes or search; this file is the substrate everything else stands on.

Three properties are load-bearing downstream and are enforced here:

  1. Declared types.       A graph that type-checks cannot be applied to the
                           wrong channel. Ill-typed construction raises.
  2. Hash-consing.         Structurally identical subexpressions become the same
                           node, so the DAG shares work and `key()` is a
                           canonical identity usable for deduplication.
  3. One semantics.        `evaluate` is the reference. Every backend in
                           compile_*.py must agree with it on the conformance
                           harness or it is not certified. There is exactly one
                           definition of what a graph means.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

REAL = "real"
VEC = "vec"
BOOL = "bool"
TYPES = (REAL, VEC, BOOL)


class TypeError_(Exception):
    """Raised when a graph would be ill-typed. Deliberately not builtins.TypeError."""


@dataclass(frozen=True)
class Op:
    """A node definition: declared arity, input types, output type, semantics."""

    name: str
    inputs: Tuple[str, ...]
    output: str
    py: Callable[..., object]
    c_fn: Optional[str] = None   # name of the C runtime function, if compilable
    cost: float = 1.0            # nominal evaluation cost, used by the search
    doc: str = ""

    @property
    def arity(self) -> int:
        return len(self.inputs)


@dataclass(frozen=True)
class Node:
    kind: str                      # 'input' | 'const' | 'op'
    payload: object                # input name | constant value | op name
    args: Tuple[int, ...] = ()
    type: str = REAL


@dataclass
class Graph:
    """A hash-consed DAG. nodes[i].args always point to indices < i."""

    nodes: Tuple[Node, ...]
    root: int
    signature: Tuple[Tuple[str, str], ...]   # ((input_name, type), ...)
    registry: "Registry" = field(repr=False, default=None)

    @property
    def output_type(self) -> str:
        return self.nodes[self.root].type

    @property
    def size(self) -> int:
        """Number of nodes actually reachable from the root (shared once)."""
        return len(self.reachable())

    @property
    def depth(self) -> int:
        d = [0] * len(self.nodes)
        for i, nd in enumerate(self.nodes):
            d[i] = 0 if not nd.args else 1 + max(d[a] for a in nd.args)
        return d[self.root]

    def reachable(self) -> List[int]:
        seen = set()
        stack = [self.root]
        while stack:
            i = stack.pop()
            if i in seen:
                continue
            seen.add(i)
            stack.extend(self.nodes[i].args)
        return sorted(seen)

    def used_inputs(self) -> List[str]:
        return sorted(
            {self.nodes[i].payload for i in self.reachable() if self.nodes[i].kind == "input"}
        )

    def cost(self) -> float:
        total = 0.0
        for i in self.reachable():
            nd = self.nodes[i]
            if nd.kind == "op":
                total += self.registry.ops[nd.payload].cost
        return total

    # -- identity ---------------------------------------------------------
    def key(self) -> str:
        """Canonical structural identity. Equal keys == equal DAGs."""
        idx: Dict[int, int] = {}
        parts: List[str] = []

        def emit(i: int) -> int:
            if i in idx:
                return idx[i]
            nd = self.nodes[i]
            child = [emit(a) for a in nd.args]
            if nd.kind == "input":
                s = f"i:{nd.payload}"
            elif nd.kind == "const":
                s = f"c:{nd.payload!r}"
            else:
                s = f"{nd.payload}({','.join(map(str, child))})"
            j = len(parts)
            parts.append(s)
            idx[i] = j
            return j

        emit(self.root)
        return "|".join(parts)

    def to_expr(self) -> str:
        """Readable nested form. This is what a language model reads and writes."""

        def go(i: int) -> str:
            nd = self.nodes[i]
            if nd.kind == "input":
                return str(nd.payload)
            if nd.kind == "const":
                v = nd.payload
                return f"{v:g}" if isinstance(v, float) else str(v)
            return f"{nd.payload}(" + ", ".join(go(a) for a in nd.args) + ")"

        return go(self.root)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Graph[{self.output_type}]({self.to_expr()})"

    # -- evaluation -------------------------------------------------------
    def evaluate(self, env: Dict[str, object]) -> object:
        """Reference semantics. Every backend must reproduce exactly this."""
        vals: List[object] = [None] * len(self.nodes)
        for i in self.reachable():
            nd = self.nodes[i]
            if nd.kind == "input":
                if nd.payload not in env:
                    raise KeyError(f"missing input {nd.payload!r}")
                vals[i] = env[nd.payload]
            elif nd.kind == "const":
                vals[i] = nd.payload
            else:
                op = self.registry.ops[nd.payload]
                vals[i] = op.py(*(vals[a] for a in nd.args))
        return vals[self.root]


class Registry:
    """The library of node definitions, plus composites built from them."""

    def __init__(self) -> None:
        self.ops: Dict[str, Op] = {}
        self.composites: Dict[str, "Composite"] = {}

    def add(self, op: Op) -> Op:
        if op.name in self.ops:
            raise ValueError(f"duplicate op {op.name!r}")
        for t in op.inputs + (op.output,):
            if t not in TYPES:
                raise ValueError(f"unknown type {t!r} in op {op.name!r}")
        self.ops[op.name] = op
        return op

    def define(self, name: str, inputs: Sequence[str], output: str, c_fn=None, cost=1.0, doc=""):
        def deco(fn):
            self.add(Op(name, tuple(inputs), output, fn, c_fn, cost, doc))
            return fn

        return deco

    def by_output(self, t: str) -> List[Op]:
        return [o for o in self.ops.values() if o.output == t]

    def compilable(self) -> List[str]:
        return sorted(n for n, o in self.ops.items() if o.c_fn)

    def uncompilable(self) -> List[str]:
        return sorted(n for n, o in self.ops.items() if not o.c_fn)

    # -- composites -------------------------------------------------------
    def add_composite(self, comp: "Composite") -> Op:
        """Register a saved subgraph as a first-class node in the library."""
        if comp.name in self.ops:
            raise ValueError(f"duplicate op {comp.name!r}")
        types = tuple(t for _, t in comp.graph.signature)

        def run(*args, _c=comp):
            env = {nm: v for (nm, _t), v in zip(_c.graph.signature, args)}
            return _c.graph.evaluate(env)

        op = Op(
            name=comp.name,
            inputs=types,
            output=comp.graph.output_type,
            py=run,
            # a composite is compilable exactly when its body is
            c_fn=None,
            cost=comp.graph.cost(),
            doc=comp.doc or f"composite := {comp.graph.to_expr()}",
        )
        self.ops[comp.name] = op
        self.composites[comp.name] = comp
        return op


@dataclass
class Composite:
    """A named subgraph promoted to a node. Inlined by the compilers."""

    name: str
    graph: Graph
    doc: str = ""


class Builder:
    """Hash-consing graph builder. Type errors raise at construction time."""

    def __init__(self, registry: Registry, signature: Sequence[Tuple[str, str]]):
        self.registry = registry
        self.signature = tuple(signature)
        self.nodes: List[Node] = []
        self._index: Dict[Tuple, int] = {}
        self._sig = {n: t for n, t in self.signature}

    def _intern(self, node: Node) -> int:
        k = (node.kind, node.payload, node.args)
        if k in self._index:
            return self._index[k]
        self.nodes.append(node)
        i = len(self.nodes) - 1
        self._index[k] = i
        return i

    def input(self, name: str) -> int:
        if name not in self._sig:
            raise TypeError_(f"{name!r} is not in the signature {sorted(self._sig)}")
        return self._intern(Node("input", name, (), self._sig[name]))

    def const(self, value, type_: str = REAL) -> int:
        if type_ == REAL:
            value = float(value)
        elif type_ == BOOL:
            value = bool(value)
        return self._intern(Node("const", value, (), type_))

    def apply(self, op_name: str, *args: int) -> int:
        op = self.registry.ops.get(op_name)
        if op is None:
            raise TypeError_(f"unknown op {op_name!r}")
        if len(args) != op.arity:
            raise TypeError_(
                f"{op_name} declares {op.arity} input(s), got {len(args)}"
            )
        for k, (a, want) in enumerate(zip(args, op.inputs)):
            got = self.nodes[a].type
            if got != want:
                raise TypeError_(
                    f"{op_name} input {k} declares {want!r}, got {got!r} "
                    f"from {self._show(a)}"
                )
        return self._intern(Node("op", op_name, tuple(args), op.output))

    def _show(self, i: int) -> str:
        nd = self.nodes[i]
        return f"{nd.payload}" if nd.kind != "op" else f"{nd.payload}(...)"

    def finish(self, root: int) -> Graph:
        return Graph(tuple(self.nodes), root, self.signature, self.registry)


def parse(registry: Registry, signature: Sequence[Tuple[str, str]], text: str) -> Graph:
    """Parse the readable form back into a graph. Type-checks on the way in.

    This is the door a language model writes through: it emits text, the parser
    either produces a type-correct graph or reports precisely what is wrong.
    """
    b = Builder(registry, signature)
    pos = 0
    s = text.strip()

    def ws():
        nonlocal pos
        while pos < len(s) and s[pos].isspace():
            pos += 1

    def ident() -> str:
        nonlocal pos
        start = pos
        while pos < len(s) and (s[pos].isalnum() or s[pos] in "_."):
            pos += 1
        if start == pos:
            raise TypeError_(f"expected a name at offset {pos} in {text!r}")
        return s[start:pos]

    def expr() -> int:
        nonlocal pos
        ws()
        if pos < len(s) and (s[pos].isdigit() or s[pos] == "-"):
            start = pos
            pos += 1
            while pos < len(s) and (s[pos].isdigit() or s[pos] in ".eE+-"):
                pos += 1
            return b.const(float(s[start:pos]))
        name = ident()
        ws()
        if pos < len(s) and s[pos] == "(":
            pos += 1
            args: List[int] = []
            ws()
            if pos < len(s) and s[pos] == ")":
                pos += 1
            else:
                while True:
                    args.append(expr())
                    ws()
                    if pos < len(s) and s[pos] == ",":
                        pos += 1
                        continue
                    if pos < len(s) and s[pos] == ")":
                        pos += 1
                        break
                    raise TypeError_(f"expected ',' or ')' at offset {pos} in {text!r}")
            return b.apply(name, *args)
        if name in {"true", "false"}:
            return b.const(name == "true", BOOL)
        return b.input(name)

    root = expr()
    ws()
    if pos != len(s):
        raise TypeError_(f"trailing input at offset {pos} in {text!r}")
    return b.finish(root)


def inline(graph: Graph) -> Graph:
    """Expand every composite node into its body. Backends compile the result."""
    reg = graph.registry
    b = Builder(reg, graph.signature)
    memo: Dict[int, int] = {}

    def go(i: int) -> int:
        if i in memo:
            return memo[i]
        nd = graph.nodes[i]
        if nd.kind == "input":
            j = b.input(nd.payload)
        elif nd.kind == "const":
            j = b.const(nd.payload, nd.type)
        else:
            args = [go(a) for a in nd.args]
            comp = reg.composites.get(nd.payload)
            if comp is None:
                j = b.apply(nd.payload, *args)
            else:
                body = inline(comp.graph)
                sub: Dict[int, int] = {}
                bind = {nm: args[k] for k, (nm, _t) in enumerate(body.signature)}
                for bi in body.reachable():
                    bn = body.nodes[bi]
                    if bn.kind == "input":
                        sub[bi] = bind[bn.payload]
                    elif bn.kind == "const":
                        sub[bi] = b.const(bn.payload, bn.type)
                    else:
                        sub[bi] = b.apply(bn.payload, *(sub[a] for a in bn.args))
                j = sub[body.root]
        memo[i] = j
        return j

    return b.finish(go(graph.root))
