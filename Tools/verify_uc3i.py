"""Replay UC3I using event-based death and birth stamps and offline 2-core crossings."""
import argparse
import ast
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
import csv
import gzip
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import local_growth_candidate as law
from Tools.run_uc3g import compact, sha, summarize
from Tools.uc3i_inheritance import reference_step
from Tools.uc3m_cycles import setup
from Tools.verify_uc3g import core, component, one_step, check_witness, pack, project, replay_loss
from Tools.verify_uc3m import crossings


def check_row(start, pair, row):
    seed = int(sha("/".join(("UC3I", row["world"], row["arm"], row["mode"], row["rep"])).encode())[:16], 16)
    assert seed == int(row["seed"])
    rng = random.Random(seed)
    state, tag, ids = project(law.clone_state(start), pair["tag"], list(range(len(start.units))))
    originals = [tuple(e) for e in pair["cohort"]]
    generations = {inst[:2]: inst[2] for inst in originals}
    history = [len(core(state.adjacency, state.adjacency))]
    snapshots, parents, landmarks = [], [], []
    recorded_marks = ast.literal_eval(row["marks"])
    for _ in range(int(row["attempts"])):
        t = len(history) - 1
        # Reference driver is shared. Audit all reported crossings offline below.
        rising = sum(mark[0] <= t for mark in recorded_marks) % 2 == 0
        event = (law.attempt_step(state, rng) if row["mode"] == "natural" else
                 reference_step(state, tag, rng, row["mode"], t, rising, parents, landmarks))
        if not event.changed:
            continue
        u, v, a = event.source, event.target, event.carried
        if event.kind == "cut":
            removed = [(u,v)]
        elif event.kind == "collapse":
            removed = [(u,v), (u,a)]
        elif event.kind == "slide":
            removed = [(u,a)]
        else:
            removed = []
        for edge in removed:
            generations.pop(tuple(sorted(edge)), None)
        state, tag, ids = project(state, tag, ids)
        if t == 5 and row["mode"] == "null":
            assert len(state.adjacency) == 2 and all(v >= start.next_node_id for v in state.adjacency)
        nodes = core(state.adjacency, state.adjacency)
        history.append(len(nodes))
        snapshots.append({i for i,(u,v,b) in enumerate(originals) if u in nodes and v in nodes
                          and v in state.adjacency[u] and generations.get((u,v)) == b})
    marks = crossings(history)
    assert marks == recorded_marks and int(row["exposure"]) == len(history)-1
    witnesses = [snapshots[t-1] for t,_ in marks]
    assert list(map(sorted, witnesses)) == ast.literal_eval(row["witnesses"])
    complete = len(marks) == 5
    inherited = set.intersection(*witnesses[::2]) if complete else set()
    strict = set.intersection(*witnesses) if complete else set()
    assert sorted(inherited) == ast.literal_eval(row["inherited"]) and sorted(strict) == ast.literal_eval(row["strict"])
    assert complete == (row["complete"] == "True") and bool(inherited) == (row["success"] == "True")
    stop = ("complete" if complete else "window" if len(history)==97 else
            "absorbed" if not state.adjacency[state.units[tag]] else "attempt_cap")
    assert row["stop"] == stop and (stop=="attempt_cap") == (row["censored"]=="True")
    if complete:
        assert marks[-1][0] == len(history)-1
    if row["mode"] != "natural":
        assert complete and bool(inherited) == (row["mode"] == "positive")


def verify_world(job):
    world, pair, rows = job
    initial = replay_loss(world, pair)
    if not pair:
        assert not rows
        return 0
    assert len(rows) == 192
    choices = 0
    group = set(map(tuple,pair["match"]["block"]))
    arms = {}
    for arm in ("preserved","rewired"):
        state = setup(initial,pair["match"]["spec"],arm)
        arms[arm] = state
        assert sha(compact(pack(state)).encode()) == pair["start_hashes"][arm]
        opts, num = one_step(state, pair["tag"])
        assert compact(opts) == compact(pair["match"]["opportunities"])
        choices += num
        nodes = core(state.adjacency, component(state.adjacency,state.units[pair["tag"]]))
        group &= {e for e in law.edge_set(state) if set(e) <= nodes}
    check_witness(list(arms.values()),pair["tag"],pair["match"]["nonisomorphism"],
                  component(initial.adjacency, initial.units[pair["tag"]]))
    assert pair["cohort"] and pair["cohort"] == [i for i in pair["retained"] if tuple(i[:2]) in group]
    for row in rows:
        check_row(arms[row["arm"]], pair, row)
    return choices


def verify(out):
    data = json.loads((out/"UC3I_result.json").read_text())
    for root, key in ((out,"evidence_sha256"),(ROOT,"source_sha256")):
        for name, digest in data[key].items():
            assert sha((root/name).read_bytes()) == digest
    worlds = list(csv.DictReader((out/"UC3I_worlds.csv").open()))
    pairs = {p["world"]:p for p in map(json.loads,(out/"UC3I_pairs.jsonl").read_text().splitlines())}
    by_world = defaultdict(list)
    with gzip.open(out/"UC3I_followups.csv.gz","rt") as f:
        for r in csv.DictReader(f):
            by_world[r["world"]].append(r)
    assert set(pairs) == set(by_world)
    schedule = [(n,i) for n in (32,96) for i in range(1000000,1000256)]
    assert len(worlds) == len(schedule)
    for w,(n,i) in zip(worlds,schedule):
        assert int(w["n"]) == n and int(w["seed"]) == 202611080000+1000*n+i and w["world"] == f"m{n}-{i:02d}"
        w["n"] = n
        if w["prefix_stop"] != "matched":
            assert w["world"] not in pairs
            continue
        rows = by_world[w["world"]]
        assert {(r["arm"],r["mode"],int(r["rep"])) for r in rows} == {
            (a,m,i) for a in ("preserved","rewired") for m in ("natural","positive","null") for i in range(32)}
        natural = [r for r in rows if r["mode"] == "natural"]
        for arm in ("preserved","rewired"):
            hits = sum(r["arm"]==arm and r["success"]=="True" for r in natural)
            assert hits == int(w[arm+"_hits"])
            w[arm+"_hits"] = hits
        w["natural_censored"] = int(w["natural_censored"])
        assert w["natural_censored"] == sum(r["censored"]=="True" for r in natural)
    assert data["reference_pass"] and summarize(worlds,True) == data["analysis"]
    jobs = [(w,pairs.get(w["world"]),by_world.get(w["world"],[])) for w in worlds]
    with ProcessPoolExecutor(max_workers=6) as pool:
        choices = sum(pool.map(verify_world,jobs))
    print(json.dumps(dict(verified=True,prefixes=len(worlds),pairs=len(pairs),
                          rows=sum(map(len,by_world.values())),one_step_transitions=choices)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    verify(parser.parse_args().out)
