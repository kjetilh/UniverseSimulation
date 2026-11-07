"""Prospective paired UC3G experiment. Screen, calibrate, then open natural continuations."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import csv
from dataclasses import asdict, astuple
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import local_growth_candidate as kernel
from Tools.local_growth_observer import _region
from Tools.observe_uc3_remnants import Point, Trace, edge
from Tools.run_local_growth_candidate import initialize, partition_map
from Tools.uc3g_followup import follow
from Tools.uc3g_match import find_match

PROG = ROOT / "Documentation/Program"
ARMS = ("preserved", "rewired")
REPS = 32
SIZES = (32, 96)
WORLDS = 64
SOURCES = (
    "Documentation/Program/UC3G_protocol.md", "Tools/run_uc3g.py",
    "Tools/uc3g_followup.py", "Tools/uc3g_match.py", "Tools/local_growth_candidate.py",
    "Tools/local_change_candidate.py", "Tools/local_growth_observer.py",
    "Tools/run_local_growth_candidate.py", "Tools/run_local_change_candidate.py",
    "Tools/observe_uc3_remnants.py",
)


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump_state(state):
    nodes, edges, units, ticks, attempts, next_id = kernel.state_snapshot(state)
    return dict(nodes=nodes, edges=edges, units=units, ticks=ticks, attempts=attempts,
                next_node_id=next_id)


def restore(data):
    state = kernel.make_state(data["nodes"], data["edges"], data["units"], data["next_node_id"])
    state.ticks, state.attempts = data["ticks"], data["attempts"]
    return state


def update_births(births, event, tick):
    v, u, a = event.source, event.target, event.carried
    if event.kind == "slide":
        del births[edge(v, a)]
        births[edge(u, a)] = tick
    elif event.kind == "bud":
        births[edge(v, u)] = births[edge(a, u)] = tick
    elif event.kind == "collapse":
        del births[edge(v, u)], births[edge(v, a)]
    else:
        del births[edge(v, u)]


def screen(job):
    n, rep = job
    world, seed = f"g{n}-{rep:02d}", 202611070000 + 1000*n + rep
    state, rng, initial = initialize(dict(run_id=world, role="candidate", n=n, seed=seed, units=n//4))
    initial_sha = sha(compact(initial).encode())
    parts = partition_map(state)
    births = dict.fromkeys(kernel.edge_set(state), 0)
    traces = [Trace() for _ in state.units]
    transcript = hashlib.sha256()
    pair = None
    losses = nonempty = 0
    while True:
        if not any(t.loss is None and state.adjacency[u] for t, u in zip(traces, state.units)):
            stop = "no_remaining_active_tag"
            break
        if state.attempts >= 16384 or state.ticks >= 4096 or len(state.adjacency) >= 1024:
            stop = "prefix_safety_cap"
            break
        event = kernel.attempt_step(state, rng)
        transcript.update((compact(astuple(event)) + "\n").encode())
        if not event.changed:
            continue
        origin = parts[event.source]
        parts = partition_map(state)
        update_births(births, event, state.ticks)
        views = {}
        for tag, trace in enumerate(traces):
            host = state.units[tag]
            # The moving unit may occupy a newborn vertex absent from the old partition.
            if trace.loss is not None or (tag != event.unit_index and host not in origin):
                continue
            nodes = parts[host]
            if nodes not in views:
                region = _region(state.adjacency, nodes)
                edges = frozenset((a, b, births[a, b]) for a, b in region["core_edges"])
                views[nodes] = (len(region["core_nodes"]), edges)
            k, edges = views[nodes]
            split = event.kind == "cut" and len(nodes) < len(origin)
            point = Point(state.ticks, trace.clock + 1, k)
            trace.observe(point, nodes, edges, births, event, split, {})
            if trace.loss is None:
                continue
            losses += 1
            nonempty += bool(trace.retained)
            match = find_match(state, tag, trace.retained)
            if match is None:
                continue
            preserved, rewired, audit = match
            pair = dict(world=world, seed=seed, n=n, tag=tag, loss_state=dump_state(state),
                        loss=asdict(point), loss_event=asdict(event), split=split, peak=asdict(trace.peak),
                        peak_instances=sorted(trace.peak_edges), retained=sorted(trace.retained), match=audit,
                        start_hashes={arm: sha(compact(dump_state(branch)).encode()) for arm, branch
                                      in zip(ARMS, (preserved, rewired))})
            break
        if pair:
            stop = "matched"
            break
    row = dict(world=world, n=n, seed=seed, prefix_stop=stop, attempts=state.attempts,
               ticks=state.ticks, examined_first_losses=losses, nonempty_examined=nonempty,
               initial_sha256=initial_sha, prefix_events_sha256=transcript.hexdigest())
    return row, pair


def continuation_seed(world, arm, mode, rep):
    return int(sha(f"UC3G/{world}/{arm}/{mode}/{rep}".encode())[:16], 16)


def evaluate(job):
    pair, modes = job
    rows = []
    for arm in ARMS:
        state = restore(pair["loss_state"])
        setup = pair["match"][arm + "_event"]
        kernel.apply_event(state, setup["unit_index"], "slide", setup["target"], setup["carried"])
        if pair["start_hashes"][arm] != sha(compact(dump_state(state)).encode()):
            raise RuntimeError("Start reconstruction failed")
        for mode in modes:
            for rep in range(REPS):
                seed = continuation_seed(pair["world"], arm, mode, rep)
                result = follow(state, pair["tag"], seed, mode, setup)
                if result["k_start"] != pair["loss"]["core"]:
                    raise RuntimeError("Baseline core mismatch")
                rows.append(dict(world=pair["world"], n=pair["n"], arm=arm, mode=mode, rep=rep,
                                 seed=seed, **result))
    return rows


def check_manifest(pairs, modes, rows):
    expected = {(p["world"], arm, mode, rep) for p in pairs for arm in ARMS
                for mode in modes for rep in range(REPS)}
    observed = {(r["world"], r["arm"], r["mode"], r["rep"]) for r in rows}
    if observed != expected or len(rows) != len(expected):
        raise RuntimeError("Missing, duplicated or unexpected continuation")


def calibrate(rows):
    reference = {}
    for arm in ARMS:
        reference[arm] = {}
        for mode in ("null", "positive"):
            group = [r for r in rows if r["arm"] == arm and r["mode"] == mode]
            reference[arm][mode] = dict(total=len(group), hits=sum(r["success"] for r in group),
                                        censored=sum(r["censored"] for r in group))
    return reference


def sign_test(positive, negative):
    n = positive + negative
    return sum(math.comb(n, k) for k in range(positive, n+1)) / 2**n


def summarize(rows, reference_ok):
    eligible = [row for row in rows if row["prefix_stop"] == "matched"]
    diffs = [[(r["preserved_hits"] - r["rewired_hits"])/REPS for r in eligible if r["n"] == size]
             for size in SIZES]
    all_d = [v for group in diffs for v in group]
    n = len(all_d)
    pos, neg = sum(v > 0 for v in all_d), sum(v < 0 for v in all_d)
    p = sign_test(pos, neg)
    ci = None
    if n:
        rng = random.Random(2026110701)
        boot = sorted(sum(sum(rng.choices(group, k=len(group))) for group in diffs if group)/n
                      for _ in range(20000))
        # Empirical inverse CDF (nearest rank).
        ci = [boot[499], boot[19499]]
    contrasts = {}
    for key, subset in [("all", eligible)] + [(str(k), [r for r in eligible if r["n"] == k]) for k in SIZES]:
        den = REPS * len(subset)
        hits = {a: sum(r[a + "_hits"] for r in subset) for a in ARMS}
        contrasts[key] = dict(worlds=len(subset), denominator_per_arm=den, hits=hits,
                              difference=(hits["preserved"]-hits["rewired"])/den if den else None)
    censored = sum(r["natural_censored"] for r in eligible)
    if not reference_ok or n < 24 or censored:
        verdict = "instrumentation_or_coverage_limited"
    elif ci[0] > 0 and p <= 0.05:
        verdict = "preserved_advantage_in_matched_worlds"
    else:
        verdict = "preserved_advantage_not_demonstrated"
    return dict(verdict=verdict, contrasts=contrasts, interval_95=ci, positive=pos, tied=n-pos-neg,
                negative=neg, one_sided_sign_p=p, natural_censored=censored)


def write_csv(path, rows):
    with path.open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(out, workers):
    out.mkdir(parents=True, exist_ok=True)
    if any(out.glob("UC3G_*")):
        raise ValueError("Output directory already contains UC3G artifacts")
    with ProcessPoolExecutor(max_workers=workers) as pool:
        screened = list(pool.map(screen, [(n, i) for n in SIZES for i in range(WORLDS)]))
        worlds = [w for w, _ in screened]
        pairs = [p for _, p in screened if p is not None]
        (out / "UC3G_pairs.jsonl").write_text("".join(compact(p)+"\n" for p in pairs))
        print(f"screened {len(worlds)}, matched {len(pairs)}", flush=True)
        controls = [r for batch in pool.map(evaluate, [(p, ("null", "positive")) for p in pairs]) for r in batch]
        check_manifest(pairs, ("null", "positive"), controls)
        reference = calibrate(controls)
        denominator = len(pairs)*REPS
        reference_ok = denominator > 0 and all(
            v["total"] == denominator and v["hits"] == (denominator if m == "positive" else 0) and not v["censored"]
            for arm in reference.values() for m, v in arm.items())
        print(f"same-arm references passed: {reference_ok}", flush=True)
        natural = []
        if reference_ok:
            natural = [r for batch in pool.map(evaluate, [(p, ("natural",)) for p in pairs]) for r in batch]
            check_manifest(pairs, ("natural",), natural)
    counts = Counter((r["world"], r["arm"]) for r in natural if r["success"])
    censored = Counter(r["world"] for r in natural if r["censored"])
    for row in worlds:
        measured = reference_ok and row["prefix_stop"] == "matched"
        for arm in ARMS:
            row[arm+"_hits"] = counts[row["world"], arm] if measured else None
        row["natural_censored"] = censored[row["world"]] if measured else None
    write_csv(out/"UC3G_worlds.csv", worlds)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td)/"followups.csv"
        if controls or natural:
            write_csv(path, controls + natural)
        else:
            path.write_text("world,n,arm,mode,rep,seed,success,first_hit,exposure,attempts,stop,k_start,k_final,censored,trace_sha256\n")
        (out/"UC3G_followups.csv.gz").write_bytes(gzip.compress(path.read_bytes(), compresslevel=6, mtime=0))
    analysis = summarize(worlds, True) if reference_ok else {"verdict": "instrumentation_or_coverage_limited"}
    result = dict(round="UC3G", world_count=len(worlds), matched_count=len(pairs), reps_per_arm=REPS,
                  reference=reference, reference_pass=reference_ok, analysis=analysis,
                  prefix_stops=dict(Counter(r["prefix_stop"] for r in worlds)),
                  followup_stops={m:dict(Counter(r["stop"] for r in controls + natural if r["mode"] == m))
                                  for m in ("null","positive","natural")},
                  source_sha256={s:sha((ROOT/s).read_bytes()) for s in SOURCES},
                  evidence_sha256={p.name:sha(p.read_bytes()) for p in sorted(out.glob("UC3G_*"))})
    (out/"UC3G_result.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(compact(analysis), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    run(args.out, args.workers)
