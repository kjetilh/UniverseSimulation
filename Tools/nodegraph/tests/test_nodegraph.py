#!/usr/bin/env python3
"""Tests for Tools/nodegraph. Run with pytest, or directly with python3."""
from __future__ import annotations

import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "arena"))

import compile_c  # noqa: E402
import compile_py  # noqa: E402
import core  # noqa: E402
import library  # noqa: E402
import observable_purpose as OP  # noqa: E402
from core import BOOL, REAL, VEC, Builder, Composite, parse  # noqa: E402
from purpose import PurposeContract, Reference  # noqa: E402

REG = library.REGISTRY
SIG = (("v", VEC), ("w", VEC), ("x", REAL), ("y", REAL), ("p", BOOL))


# ------------------------------------------------------------------ typing
def test_declared_types_are_enforced():
    for bad in ("mean(x)", "add(v, 1)", "ifelse(x, 1, 2)", "corr(v, x)"):
        try:
            parse(REG, SIG, bad)
        except core.TypeError_:
            continue
        raise AssertionError(f"{bad!r} should not type-check")


def test_arity_is_enforced():
    try:
        parse(REG, SIG, "add(x)")
    except core.TypeError_ as e:
        assert "declares 2 input" in str(e)
        return
    raise AssertionError("wrong arity should not type-check")


def test_unknown_name_becomes_input_error():
    try:
        parse(REG, SIG, "notachannel")
    except core.TypeError_ as e:
        assert "signature" in str(e)
        return
    raise AssertionError("unknown input should be rejected")


# ------------------------------------------------------- structure sharing
def test_hash_consing_shares_subexpressions():
    g = parse(REG, SIG, "add(mean(v), mean(v))")
    assert g.size == 3, g.size  # v, mean(v), add -- mean(v) exists once
    b = Builder(REG, SIG)
    i = b.apply("mean", b.input("v"))
    assert b.apply("mean", b.input("v")) == i


def test_key_is_structural_identity():
    a = parse(REG, SIG, "div(std(v), mean(v))")
    b = parse(REG, SIG, "div(std(v), mean(v))")
    c = parse(REG, SIG, "div(mean(v), std(v))")
    assert a.key() == b.key() and a.key() != c.key()


def test_parse_roundtrip():
    for e in ("div(sub(topmean(v), median(v)), add(std(zscore(vlog1p(w))), 1.5))",
              "ifelse(gt(mean(v), x), sum(w), y)",
              "corr(sortdesc(v), norm1(w))"):
        g = parse(REG, SIG, e)
        assert parse(REG, SIG, g.to_expr()).key() == g.key()


# ------------------------------------------------------------- composites
def test_composite_is_a_node_and_inlines_to_the_same_value():
    reg = library.Registry()
    for name, op in REG.ops.items():
        reg.ops[name] = op
    body = parse(reg, (("v", VEC),), "div(std(v), add(mean(v), 1))")
    reg.add_composite(Composite("cv1", body))
    outer = parse(reg, SIG, "add(cv1(v), cv1(w))")
    env = {"v": [1.0, 2.0, 5.0, 9.0], "w": [3.0, 3.0, 4.0], "x": 1.0, "y": 2.0, "p": True}
    direct = parse(reg, SIG, "add(div(std(v), add(mean(v), 1)), div(std(w), add(mean(w), 1)))")
    assert abs(outer.evaluate(env) - direct.evaluate(env)) < 1e-12
    assert core.inline(outer).key() == direct.key()


# ------------------------------------------------------ backend conformance
def _sig_for(op):
    names = []
    sig = []
    for k, t in enumerate(op.inputs):
        n = f"a{k}"
        names.append(n)
        sig.append((n, t))
    return tuple(sig), names


def test_every_library_op_has_a_conformant_c_implementation():
    failures = []
    for name, op in sorted(REG.ops.items()):
        sig, names = _sig_for(op)
        if op.output == VEC:
            # wrap so the graph returns a scalar the C entry point can hand back
            inner = f"{name}(" + ", ".join(names) + ")"
            expr = f"add(add(sum({inner}), count({inner})), std({inner}))"
        else:
            expr = f"{name}(" + ", ".join(names) + ")"
        g = parse(REG, sig, expr)
        try:
            c = compile_c.compile_graph(g)
            rep = compile_c.conformance(g, c, trials=250, seed=7 + len(name))
            if not rep["passed"]:
                failures.append((name, rep))
        except Exception as e:  # pragma: no cover
            failures.append((name, repr(e)))
    assert not failures, failures


def test_python_codegen_matches_the_interpreter():
    rng = random.Random(3)
    for e in ("div(sub(topmean(v), median(v)), add(entropy(norm1(w)), 1))",
              "ifelse(lt(gini(v), 0.5), skew(w), cv(v))",
              "corr(vsq(v), diff(w))"):
        g = parse(REG, SIG, e)
        f = compile_py.compile_graph(g)
        for _ in range(50):
            env = compile_c.random_env(SIG, rng)
            a, b = g.evaluate(env), f(**env)
            assert abs(float(a) - float(b)) < 1e-12, (e, env, a, b)


def test_uncompilable_graph_is_reported_not_silently_wrong():
    g = parse(REG, SIG, "norm1(v)")
    try:
        compile_c.to_source(g)
    except compile_c.NotCompilable as e:
        assert "vec" in str(e)
        return
    raise AssertionError("a vec-valued graph must be refused by the C backend")


# ---------------------------------------------------------------- totality
def test_no_node_returns_nan_or_raises_on_degenerate_input():
    rng = random.Random(11)
    for name, op in sorted(REG.ops.items()):
        sig, names = _sig_for(op)
        g = parse(REG, sig, f"{name}(" + ", ".join(names) + ")")
        for env in ({n: ([] if t == VEC else (False if t == BOOL else 0.0))
                     for n, t in sig},
                    {n: ([0.0] * 3 if t == VEC else (True if t == BOOL else 0.0))
                     for n, t in sig},
                    {n: ([1e308, -1e308] if t == VEC else (True if t == BOOL else 1e308))
                     for n, t in sig}):
            v = g.evaluate(env)
            xs = v if isinstance(v, list) else [v]
            for x in xs:
                x = 1.0 if x is True else (0.0 if x is False else float(x))
                assert not math.isnan(x) and not math.isinf(x), (name, env, v)


# ------------------------------------------------------------ the contract
def _contract(null, pos, min_sep=2.0):
    return PurposeContract(
        id="t", statement="t", signature=SIG, output_type=REAL,
        score=lambda g: 1.0, holdout=lambda g: 1.0,
        null_reference=Reference("null", null, "m", "s"),
        positive_reference=Reference("positive", pos, "m", "s"),
        min_separation=min_sep,
    )


def test_contract_refuses_without_a_measured_null():
    v = _contract(None, 10.0).admissibility()
    assert not v and "null reference not measured" in v.reasons[0]


def test_contract_refuses_without_a_measured_positive():
    v = _contract(1.0, None).admissibility()
    assert not v and "positive reference not measured" in v.reasons[0]


def test_contract_refuses_when_it_cannot_separate_its_own_references():
    v = _contract(1.0, 1.5).admissibility()
    assert not v and "not measurable" in v.reasons[0]


def test_admissible_contract_gates_on_the_measured_null():
    c = _contract(2.0, 20.0)
    assert c.admissibility() and c.gate_threshold() == 2.0
    r = c.evaluate(parse(REG, SIG, "mean(v)"))
    assert r["admissible"] and r["gate_threshold"] == 2.0


# ------------------------------------------------------------- the statistic
def test_score_is_sign_symmetric_and_zero_on_no_signal():
    d = [0.3, -0.1, 0.9, 0.4, -0.2, 0.7, 0.1, 0.5]
    assert abs(OP.paired_score(d) - OP.paired_score([-x for x in d])) < 1e-12
    assert OP.paired_score([0.0] * 8) == 0.0


def test_winsorising_commutes_with_sign_flipping():
    """The fast null path depends on this; if it ever stops holding, the numpy
    and pure-python nulls silently diverge."""
    rng = random.Random(5)
    for _ in range(200):
        n = rng.choice([6, 9, 24])
        d = [rng.gauss(0.4, 1.0) * rng.choice([1, 1, 30]) for _ in range(n)]
        signs = [rng.choice([-1.0, 1.0]) for _ in range(n)]
        a = OP.paired_score([x * s for x, s in zip(d, signs)])
        c = OP.quantile([abs(x) for x in d], 0.90)
        dc = [max(-c, min(c, x)) for x in d]
        b = OP.paired_score([x * s for x, s in zip(dc, signs)])
        assert abs(a - b) < 1e-9, (d, signs, a, b)


def test_numpy_and_pure_python_nulls_agree():
    rng = random.Random(17)
    ds = [[rng.gauss(0.2, 1.0) for _ in range(24)] for _ in range(40)]
    a = OP.null_references(ds, reps=4000, seed=99)
    b = OP.null_references_np(ds, reps=4000, seed=99)
    for k in ("null_single_p95", "null_search_p95"):
        assert abs(a[k] - b[k]) < 0.35 * max(1.0, a[k]), (k, a[k], b[k])


# --------------------------------------------------------------- regression
def test_recorded_result_reproduces_from_the_cached_substrate():
    exp_path = os.path.join(ROOT, "_cache", "experiment.json")
    if not os.path.exists(exp_path):
        return
    with open(exp_path) as f:
        exp = json.load(f)
    g = parse(REG, OP.CHANNELS, exp["search_run"]["winner_expr"])
    w = OP.load("weak")
    for split, key in (("train", "winner_train_score"), ("holdout", "winner_holdout_score")):
        s = OP.paired_score(OP.deltas(g, OP.pairs(w, split)))
        assert abs(s - exp["search_run"][key]) < 1e-9, (split, s, exp["search_run"][key])


if __name__ == "__main__":
    fns = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    bad = 0
    for n, f in fns:
        try:
            f()
            print(f"  ok   {n}")
        except Exception as e:
            bad += 1
            print(f"  FAIL {n}: {e}")
    print(f"\n{len(fns)-bad}/{len(fns)} passed")
    raise SystemExit(1 if bad else 0)
