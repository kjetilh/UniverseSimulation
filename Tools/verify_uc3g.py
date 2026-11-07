"""Independently audit UC3G evidence using the actual UC3 transition dispatcher."""
import argparse
from collections import Counter, defaultdict, deque
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import local_growth_candidate as law
from Tools.run_local_growth_candidate import initialize


ARMS = ("preserved", "rewired")
MODES = ("null", "positive", "natural")
REPS = 32


def check(condition, message):
    if not condition:
        raise ValueError(message)


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pack(state):
    return dict(nodes=sorted(state.adjacency), edges=sorted(law.edge_set(state)), units=state.units,
                ticks=state.ticks, attempts=state.attempts, next_node_id=state.next_node_id)


def component(adj, host):
    todo = [host]
    found = {host}
    while todo:
        node = todo.pop()
        for v in adj[node]:
            if v not in found:
                found.add(v)
                todo.append(v)
    return found


def core(adj, nodes):
    deg = {v: len(adj[v]) for v in nodes}
    queue = deque(v for v in nodes if deg[v] < 2)
    while queue:
        v = queue.popleft()
        if v not in deg:
            continue
        del deg[v]
        for w in adj[v]:
            if w in deg:
                deg[w] -= 1
                if deg[w] == 1:
                    queue.append(w)
    return set(deg)


def replay_loss(row, pair):
    n, world, seed = int(row["n"]), row["world"], int(row["seed"])
    state, rng, initial = initialize(dict(run_id=world, role="candidate", n=n, seed=seed, units=n//4))
    check(sha(compact(initial).encode()) == row["initial_sha256"], f"{world}: initial state hash")
    if not pair:
        transcript = hashlib.sha256()
        while state.attempts < int(row["attempts"]):
            event = law.attempt_step(state, rng)
            transcript.update((compact(astuple(event)) + "\n").encode())
        check(state.ticks == int(row["ticks"]) and transcript.hexdigest() == row["prefix_events_sha256"],
              f"{world}: unmatched prefix transcript")
        return None
    tag = pair["tag"]
    edges = set(law.edge_set(state))
    births = dict.fromkeys(edges, 0)
    local = 0
    peak = {"tick": 0, "local_tick": 0, "core": 0}
    peak_instances = []
    stream = hashlib.sha256()
    event = None
    while state.attempts < int(row["attempts"]):
        before = component(state.adjacency, state.units[tag])
        event = law.attempt_step(state, rng)
        stream.update((compact(astuple(event)) + "\n").encode())
        if not event.changed:
            continue
        next_edges = set(law.edge_set(state))
        for e in edges - next_edges:
            del births[e]
        births.update(dict.fromkeys(next_edges - edges, state.ticks))
        edges = next_edges
        if event.source not in before:
            continue
        local += 1
        after = component(state.adjacency, state.units[tag])
        k = core(state.adjacency, after)
        point = dict(tick=state.ticks, local_tick=local, core=len(k))
        if len(k) > peak["core"]:
            peak = point
            peak_instances = sorted([a, b, births[a,b]] for a, b in edges if a in k and b in k)
        elif peak["core"] >= 4 and 2*len(k) <= peak["core"]:
            check(state.attempts == int(row["attempts"]) and point == pair["loss"], f"{world}: first focal loss")
            retained = [t for t in peak_instances if t[0] in after and births.get(tuple(t[:2])) == t[2]]
            check(retained == pair["retained"] and peak_instances == pair["peak_instances"]
                  and peak == pair["peak"], f"{world}: peak and uninterrupted source edge generations")
            check(pair["split"] == (event.kind == "cut" and before != after), f"{world}: split at loss")
            break
    check(event is not None and asdict(event) == pair["loss_event"] and compact(pack(state)) == compact(pair["loss_state"])
          and state.ticks == int(row["ticks"]) and stream.hexdigest() == row["prefix_events_sha256"]
          and state.attempts == int(row["attempts"]) and pair["loss"]["tick"] == state.ticks,
          f"{world}: prefix transcript or loss state")
    check(peak["core"] >= 4 and 2*len(core(state.adjacency, component(state.adjacency, state.units[tag]))) <= peak["core"],
          f"{world}: missing qualified loss")
    return state


def hist(values):
    return sorted(Counter(values).items())


def one_step(state, tag):
    """Try actual legal transitions on separate clones, including cut-actor traversal."""
    nodes = component(state.adjacency, state.units[tag])
    options = []
    enumerated = 0
    for i, u in enumerate(state.units):
        if u not in nodes:
            continue
        by_kind = {}
        for kind in law.CLASSES:
            if kind == "slide":
                # Independent proposal enumeration. The kernel makes the legality decision.
                choices = [(v, a) for v in state.adjacency[u] for a in state.adjacency[u] if a != v]
            else:
                choices = [(v, None) for v in state.adjacency[u]]
            values = []
            for dest, carried in choices:
                after = law.clone_state(state)
                try:
                    law.apply_event(after, i, kind, dest, carried)
                except ValueError:
                    if kind not in ("slide", "collapse"):
                        raise
                    continue
                part = component(after.adjacency, after.units[tag])
                k = len(core(after.adjacency, part))
                values.append((len(part) != len(nodes), k) if kind == "cut" else k)
                enumerated += 1
            by_kind[kind] = values
        options.append(dict(unit=i, degree=len(state.adjacency[u]),
                            slide_choices=len(by_kind["slide"]), collapse_choices=len(by_kind["collapse"]),
                            bud_core=hist(by_kind["bud"]), collapse_core=hist(by_kind["collapse"]),
                            slide_core=hist(by_kind["slide"]), cut_split_core=hist(by_kind["cut"])))
    return options, enumerated


def check_witness(states, tag, witness, nodes):
    colors = []
    for state in states:
        counts = Counter(state.units)
        colors.append({u: (u == state.units[tag], counts[u]) for u in nodes})
    for step in range(1, witness["iteration"] + 1):
        words = [{u: (side[u], tuple(sorted(side[v] for v in state.adjacency[u]))) for u in nodes}
                 for state, side in zip(states, colors)]
        lut = {w: i for i, w in enumerate(sorted(set(words[0].values()) | set(words[1].values())))}
        colors = [{u: lut[w] for u, w in table.items()} for table in words]
        a, b = [hist(side.values()) for side in colors]
        if a != b:
            check(step == witness["iteration"] and compact([a,b]) == compact([witness["preserved"], witness["rewired"]]),
                  "Incorrect rooted color-refinement witness")
            return
    raise ValueError("No certified topological difference")


def branch_audit(state, pair):
    tag, world, audit = pair["tag"], pair["world"], pair["match"]
    nodes = component(state.adjacency, state.units[tag])
    parts = law.component_partition(state)
    retained = {tuple(t[:2]) for t in pair["retained"]}
    branches = {}
    total = 0
    check(0 < len(retained) == audit["retained_count"] and audit["tag"] == tag and
          audit["loss_core"] == pair["loss"]["core"], f"{world}: remnant metadata")
    check(audit["preserved_event"]["carried"] != audit["rewired_event"]["carried"] and
          all(audit["preserved_event"][k] == audit["rewired_event"][k] for k in ("unit_index","source","target","kind")),
          f"{world}: setup did not use the same pivot")
    for arm in ARMS:
        ev = audit[arm+"_event"]
        branch = law.clone_state(state)
        event = law.apply_event(branch, ev["unit_index"], "slide", ev["target"], ev["carried"])
        check(asdict(event) == ev and branch.ticks == state.ticks + 1 and branch.attempts == state.attempts + 1
              and branch.ticks == audit["setup_tick"] and branch.attempts == audit["setup_attempt"]
              and branch.next_node_id == state.next_node_id, f"{world}: illegal or mis-timed setup")
        left = retained - set(law.edge_set(branch))
        removed = tuple(sorted((ev["source"], ev["carried"])))
        check(left == ({removed} if arm == "rewired" else set())
              and len(retained-left) == audit["retained_after_" + arm], f"{world}: setup changed wrong remnant")
        check(law.component_partition(branch) == parts and sorted(nodes) == audit["component_nodes"] and
              branch.units == audit["unit_hosts"] and {str(v):len(branch.adjacency[v]) for v in nodes} == audit["degrees"]
              and len(core(branch.adjacency, nodes)) == pair["loss"]["core"] and
              sha(compact(pack(branch)).encode()) == pair["start_hashes"][arm], f"{world}: state matching")
        options, count = one_step(branch, tag)
        total += count
        check(compact(options) == compact(audit["opportunities"]), f"{world}/{arm}: mismatch in one-step law")
        branches[arm] = branch
    check_witness(list(branches.values()), tag, audit["nonisomorphism"], nodes)
    return branches, total


def project(state, tag, original):
    members = component(state.adjacency, state.units[tag])
    if len(members) == len(state.adjacency):
        return state, tag, original
    ids = [i for i,u in enumerate(state.units) if u in members]
    local = law.make_state(members, [(u,v) for u in members for v in state.adjacency[u] if u<v],
                           [state.units[i] for i in ids], state.next_node_id)
    local.ticks, local.attempts = state.ticks, state.attempts
    return local, ids.index(tag), [original[i] for i in ids]


def trace_row(start, pair, row):
    world, arm, mode, rep = row["world"], row["arm"], row["mode"], int(row["rep"])
    seed = int(sha(f"UC3G/{world}/{arm}/{mode}/{rep}".encode())[:16],16)
    check(seed == int(row["seed"]), f"{world}: continuation seed")
    rng = random.Random(seed)
    state, tag, original = project(law.clone_state(start), pair["tag"], list(range(len(start.units))))
    setup = pair["match"][arm+"_event"]
    exposure = attempts = 0
    digest = hashlib.sha256()
    k0 = k = len(core(state.adjacency, state.adjacency))
    while k < k0+2 and exposure < 16 and state.adjacency[state.units[tag]] and attempts < 16384:
        if mode == "null":
            dest = setup["source"] if exposure % 2 == 0 else setup["target"]
            e = law.apply_event(state, original.index(setup["unit_index"]), "slide", dest, setup["carried"])
        elif mode == "positive" and exposure < 2:
            u = state.units[tag]
            e = law.apply_event(state, tag, "bud", rng.choice(sorted(state.adjacency[u])))
        else:
            e = law.attempt_step(state, rng)
        attempts += 1
        actor = original[e.unit_index]
        if e.changed:
            exposure += 1
            if e.kind == "cut":
                state, tag, original = project(state, tag, original)
            k = len(core(state.adjacency, state.adjacency))
        event_record = (attempts, exposure, e.changed, e.kind, actor, e.source, e.target,
                        e.carried, e.born, e.removed, e.reason, k)
        digest.update((compact(event_record) + "\n").encode())
    hit = k >= k0+2
    stop = ("hit" if hit else "window" if exposure == 16 else
            "absorbed" if not state.adjacency[state.units[tag]] else "attempt_cap")
    expected = dict(success=str(hit), first_hit=str(exposure) if hit else "", exposure=str(exposure),
                    attempts=str(attempts), stop=stop, k_start=str(k0), k_final=str(k),
                    censored=str(stop == "attempt_cap"), trace_sha256=digest.hexdigest())
    check(all(row[k] == v for k,v in expected.items()), f"{world}/{arm}/{mode}/{rep}: first hit, trace, or censoring")
    return (attempts, exposure)


def audit_world(args):
    row, pair, follows = args
    state = replay_loss(row, pair)
    if pair is None:
        check(not follows and row["prefix_stop"] != "matched", "Unmatched world has continuations")
        return (0,0,0)
    check(row["world"] == pair["world"] and int(row["seed"]) == pair["seed"] and
          int(row["n"]) == pair["n"] and row["prefix_stop"] == "matched", "Checkpoint identity")
    branches, count = branch_audit(state, pair)
    # Every null replicate uses exactly the same deterministic prescribed path.
    # Verify each independently seeded row and every byte of the shared trace.
    null_proof = {}
    attempts = successes = 0
    for item in follows:
        arm, mode, rep = item["arm"], item["mode"], int(item["rep"])
        if mode != "null" or arm not in null_proof:
            stats = trace_row(branches[arm], pair, item)
            if mode == "null":
                null_proof[arm] = (item, stats)
        else:
            prior, stats = null_proof[arm]
            keys = set(prior) - {"rep", "seed"}
            seed = int(sha(f"UC3G/{pair['world']}/{arm}/null/{rep}".encode())[:16], 16)
            check(all(prior[k] == item[k] for k in keys) and int(item["seed"]) == seed,
                  f"{pair['world']}: deterministic null row")
        attempts += stats[0]
        successes += stats[1]
    return count, attempts, successes


def verify_summary(worlds, pairs, result, followups):
    check(len(worlds) == result["world_count"] == 128 and result["matched_count"] == len(pairs)
          and result["reps_per_arm"] == REPS, "Population or replica count")
    check([w["world"] for w in worlds] == [f"g{n}-{i:02d}" for n in (32,96) for i in range(64)],
          "Population differs from the locked seed schedule")
    for w in worlds:
        n, rep = map(int, w["world"][1:].split("-"))
        check(int(w["n"]) == n and int(w["seed"]) == 202611070000 + 1000*n + rep
              and 0 <= int(w["nonempty_examined"]) <= int(w["examined_first_losses"]) <= n//4, "World metadata")
    check(set(pairs) == {w["world"] for w in worlds if w["prefix_stop"] == "matched"}
          and Counter(w["prefix_stop"] for w in worlds) == result["prefix_stops"], "Prefix stop coverage")
    check(set(followups) == set(pairs), "World membership in continuations")
    flat = [r for group in followups.values() for r in group]
    refs = {}
    for arm in ARMS:
        refs[arm] = {}
        for mode in ("null", "positive"):
            group = [r for r in flat if (r["mode"],r["arm"]) == (mode,arm)]
            refs[arm][mode] = dict(total=len(group), hits=sum(r["success"] == "True" for r in group),
                                   censored=sum(r["censored"] == "True" for r in group))
    measured = bool(pairs) and all(refs[a][m] == dict(total=len(pairs)*REPS, censored=0,
        hits=len(pairs)*REPS if m=="positive" else 0) for a in ARMS for m in ("positive","null"))
    check(result["reference"] == refs and result["reference_pass"] == measured, "Reference gates")
    modes = MODES if measured else MODES[:2]
    required = {(a,m,i) for a in ARMS for m in modes for i in range(REPS)}
    for world, rows in followups.items():
        check(len(rows) == len(required) and {(r["arm"],r["mode"],int(r["rep"])) for r in rows} == required
              and all(int(r["n"]) == pairs[world]["n"] for r in rows), f"{world}: replica membership")
    stops = {m: dict(Counter(r["stop"] for r in flat if r["mode"] == m)) for m in MODES}
    check(stops == result["followup_stops"], "Reported follow-up stops")
    if not measured:
        check(result["analysis"] == {"verdict":"instrumentation_or_coverage_limited"}
              and all(w[key] == "" for w in worlds for key in ("preserved_hits","rewired_hits","natural_censored")),
              "A natural analysis was reported from failed references")
        return
    strata = {32: [], 96: []}
    hits = defaultdict(Counter)
    censor_total = 0
    for w in worlds:
        world, n = w["world"], int(w["n"])
        if world not in pairs:
            check(all(w[k] == "" for k in ("preserved_hits","rewired_hits","natural_censored")),
                  "Unexpected natural counts on unmatched world")
            continue
        rows = [r for r in followups[world] if r["mode"] == "natural"]
        counts = {a: sum(r["success"] == "True" for r in rows if r["arm"] == a) for a in ARMS}
        censored = sum(r["censored"] == "True" for r in rows)
        check(all(counts[a] == int(w[a+"_hits"]) for a in ARMS) and censored == int(w["natural_censored"]),
              f"{world}: raw-to-world aggregation")
        hits[n].update(counts)
        hits["all"].update(counts)
        strata[n].append(counts["preserved"]-counts["rewired"])
        censor_total += censored
    contrasts = {}
    for group in (32,96,"all"):
        size = len(pairs) if group == "all" else len(strata[group])
        arm_hits = dict(hits[group])
        den = REPS*size
        contrasts[str(group)] = dict(worlds=size, hits={a:arm_hits.get(a,0) for a in ARMS}, denominator_per_arm=den,
                       difference=(arm_hits["preserved"]-arm_hits["rewired"])/den if den else None)
    diffs = strata[32] + strata[96]
    pos, neg = sum(d>0 for d in diffs), sum(d<0 for d in diffs)
    sign_p = sum(math.comb(pos+neg,k) for k in range(pos,pos+neg+1)) / (1 << (pos+neg))
    rng = random.Random(2026110701)
    boots = sorted((sum(sum(rng.choices(s,k=len(s))) for s in strata.values() if s)/(REPS*len(pairs)))
                   for _ in range(20000))
    ci = [boots[499],boots[19499]]
    verdict = "instrumentation_or_coverage_limited"
    if len(pairs) >= 24 and not censor_total:
        verdict = ("preserved_advantage_in_matched_worlds" if ci[0]>0 and sign_p<=0.05
                   else "preserved_advantage_not_demonstrated")
    check(result["analysis"] == dict(verdict=verdict, contrasts=contrasts, interval_95=ci, positive=pos,
            negative=neg, tied=len(pairs)-pos-neg, natural_censored=censor_total, one_sided_sign_p=sign_p),
          "Independent world-level statistics or gate differs")


def verify(out, workers):
    result = json.loads((out/"UC3G_result.json").read_text())
    evidence = {"UC3G_followups.csv.gz","UC3G_pairs.jsonl","UC3G_worlds.csv"}
    check(set(result["evidence_sha256"]) == evidence and result["round"] == "UC3G", "Evidence identity")
    for name, expected in result["evidence_sha256"].items():
        check(sha((out/name).read_bytes()) == expected, f"Evidence digest {name}")
    for name, expected in result["source_sha256"].items():
        check(sha((ROOT/name).read_bytes()) == expected, f"Source digest {name}")
    with (out/"UC3G_worlds.csv").open() as f:
        worlds = list(csv.DictReader(f))
    checkpoints = [json.loads(line) for line in (out/"UC3G_pairs.jsonl").read_text().splitlines()]
    pairs = {p["world"]:p for p in checkpoints}
    check(len(pairs) == len(checkpoints), "Duplicate matched checkpoint")
    follows = defaultdict(list)
    with gzip.open(out/"UC3G_followups.csv.gz","rt") as f:
        for row in csv.DictReader(f):
            follows[row["world"]].append(row)
    verify_summary(worlds, pairs, result, follows)
    jobs = [(w,pairs.get(w["world"]),follows.get(w["world"],[])) for w in worlds]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        totals = list(pool.map(audit_world, jobs))
    return dict(verified=True, seeded_prefixes=len(worlds), matched_checkpoints=len(pairs),
                matched_branch_states=2*len(pairs), legal_one_step_outcomes=sum(x[0] for x in totals),
                followup_rows=sum(map(len,follows.values())), verified_followup_attempts=sum(x[1] for x in totals),
                verified_followup_changes=sum(x[2] for x in totals),
                deterministic_null="one physical replay per world and arm, then seed and exact row comparison",
                analysis=result["analysis"], result_sha256=sha((out/"UC3G_result.json").read_bytes()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(verify(args.out, args.workers), indent=2, sort_keys=True))
