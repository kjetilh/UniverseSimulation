"""Independent read-only UC3R verification from archived successful edits.

Independent two-pass reconstruction; compares traces to published CSV, without RNG or kernel imports.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


BASE = Path(__file__).resolve().parents[1] / "Documentation/Program"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(name):
    return json.loads((BASE / name).read_text())


def csv_groups(name):
    groups = defaultdict(list)
    with (BASE / name).open(newline="") as source:
        for row in csv.DictReader(source):
            groups[row["run_id"]].append(row)
    return groups


def ordered(a, b, birth):
    assert a != b
    return (min(a, b), max(a, b), birth)


def link(graph, a, b, birth):
    assert b not in graph[a] and a not in graph[b] and a != b
    graph[a][b] = graph[b][a] = birth


def unlink(graph, a, b):
    left = graph[a].pop(b)
    right = graph[b].pop(a)
    assert left == right


def component(graph, origin):
    pending = [origin]
    known = {origin}
    while pending:
        found = graph[pending.pop()].keys() - known
        known.update(found)
        pending.extend(found)
    return known


def instances(graph, nodes):
    return frozenset((a, b, birth) for a in nodes for b, birth in graph[a].items()
                     if b in nodes and a < b)


def prune(graph, nodes):
    current = set(nodes)
    while True:
        leaves = {p for p in current if len(graph[p].keys() & current) <= 1}
        if not leaves:
            return current
        current.difference_update(leaves)


def inspect_tag(run, unit, trace):
    # Two passes over independently materialized component-local histories.
    best = None
    loss = None
    for local_index, step in enumerate(trace):
        if best is None or step["K"] > trace[best]["K"]:
            best = local_index
        elif trace[best]["K"] >= 4 and 2 * step["K"] <= trace[best]["K"]:
            loss = local_index
            break
    peak = trace[best] if best is not None and trace[best]["K"] >= 4 else None
    row = dict(run=run, tag=unit, seen=len(trace), peak=peak["tick"] if peak else None,
               Kpeak=peak["K"] if peak else None, peak_edges=sorted(peak["core"]) if peak else [],
               loss=None, Kloss=None, cause=None, split=None, remnants=[], follow=[], buds=[],
               growths=[], joint=None)
    if loss is None:
        return row
    event = trace[loss]
    remnants = peak["core"] & event["edges"]
    row.update(loss=event["tick"], Kloss=event["K"], cause=event["kind"], split=event["split"],
               remnants=sorted(remnants))
    first_hit = None
    for event in trace[loss+1:loss+17]:
        tick, size = event["tick"], event["K"]
        row["follow"].append([tick, size])
        if event["kind"] == "bud":
            hit = event["chosen"] in remnants
            if hit and first_hit is None:
                first_hit = tick
            row["buds"].append(dict(tick=tick, K=size, source=event["src"], anchor=event["anchor"],
                                    birth=event["chosen"][2], hits=hit,
                                    numerator=len(event["incident"] & remnants), degree=len(event["incident"])))
        if size >= row["Kloss"] + 2:
            row["growths"].append(tick)
            if first_hit is not None and row["joint"] is None:
                row["joint"] = [first_hit, tick]
    return row


def world(start, events, archive, observation, frames):
    run = start["run_id"]
    graph = {p: {} for p in start["nodes"]}
    for a, b in start["edges"]:
        link(graph, a, b, 0)
    assert component(graph, start["nodes"][0]) == set(graph)
    assert len(start["edges"]) + 1 == start["n"] and not prune(graph, set(graph))
    hosts = start["unit_hosts"].copy()
    traces = [[] for _ in hosts]
    frame_by_tag_local = {(int(f["unit_index"]), int(f["local_tick"])): f for f in frames}
    verified_frames = 0
    for tag in range(len(hosts)):
        zero = frame_by_tag_local[tag, 0]
        assert (int(zero["core_nodes"]), int(zero["core_edges"]), int(zero["global_tick"]),
                int(zero["N"]), int(zero["E"])) == (0, 0, 0, start["n"], start["n"] - 1)
        verified_frames += 1
    tick = 0
    next_id = start["next_node_id"]
    kinds = Counter()
    split_count = 0
    for attempt, row in enumerate(events, 1):
        src, strand = int(row["source"]), int(row["unit_index"])
        assert attempt == int(row["attempt"]) and src == hosts[strand]
        kind = row["kind"]
        if row["changed"] == "False":
            kinds["blocked_"+kind] += 1
            assert int(row["tick"]) == tick
            continue
        assert row["changed"] == "True"
        tick += 1
        assert tick == int(row["tick"])
        kinds[kind] += 1
        tgt = int(row["target"])
        old = component(graph, src)
        seen_by = [i for i, p in enumerate(hosts) if p in old]
        event = dict(tick=tick, kind=kind, src=src)
        if kind == "slide":
            carried = int(row["carried"])
            assert tgt in graph[src]
            unlink(graph, src, carried)
            link(graph, tgt, carried, tick)
        elif kind == "collapse":
            carried = int(row["carried"])
            assert int(row["removed"]) == src and hosts.count(src) == 1
            assert set(graph[src]) == {tgt, carried} and carried in graph[tgt]
            unlink(graph, src, tgt)
            unlink(graph, src, carried)
            del graph[src]
        elif kind == "bud":
            anchor = int(row["carried"])
            assert int(row["born"]) == tgt == next_id and tgt not in graph
            next_id += 1
            incident = frozenset(ordered(src, p, born) for p, born in graph[src].items())
            event.update(anchor=anchor, chosen=ordered(src, anchor, graph[src][anchor]), incident=incident)
            graph[tgt] = {}
            link(graph, src, tgt, tick)
            link(graph, anchor, tgt, tick)
        else:
            assert kind == "cut"
            unlink(graph, src, tgt)
        hosts[strand] = tgt
        part = component(graph, tgt)
        split = kind == "cut" and src not in part
        assert split == (row["component_split"] == "True")
        split_count += split
        event["split"] = split
        groups = [part, old-part] if split else [part]
        for group in groups:
            core = prune(graph, group)
            size, edges, core_edges = len(core), instances(graph, group), instances(graph, core)
            point = dict(event, K=size, core=core_edges, edges=edges)
            for i in seen_by:
                if hosts[i] in group:
                    traces[i].append(point)
                    f = frame_by_tag_local.get((i, len(traces[i])))
                    if f:
                        assert (int(f["core_nodes"]), int(f["core_edges"]), int(f["global_tick"]),
                                int(f["N"]), int(f["E"]), int(f["attempt"])) == (
                                    size, len(core_edges), tick, len(group), len(edges), attempt)
                        verified_frames += 1
    assert verified_frames == len(frames)
    for i,t in enumerate(traces):
        assert len(t) == observation["per_unit"][i]["component_exposures"]
    for name, val in kinds.items():
        assert val == int(archive[name])
    assert split_count == int(archive["component_splits"]) and tick == int(archive["ticks"])
    assert len(events) == int(archive["attempts"]) and len(graph) == int(archive["final_N"])
    assert not any(graph[p] for p in hosts) and archive["stop"] == "activity_absorbed"
    edges = sorted((a,b) for a in graph for b in graph[a] if a < b)
    assert len(edges) == int(archive["final_E"])
    snapshot = (tuple(sorted(graph)), tuple(edges), tuple(hosts), tick, len(events), next_id)
    state_digest = hashlib.sha256(repr(snapshot).encode()).hexdigest()
    assert state_digest == archive["final_state_sha256"]
    return ([inspect_tag(run, i, t) for i, t in enumerate(traces)],
            dict(run=run, initial_n=start["n"], attempts=len(events), changes=tick,
                 frames=verified_frames, state_sha256=state_digest))


def verify(out):
    if not __debug__:
        raise RuntimeError("Do not use -O: independent checks must be active")
    index = read_json("UC3_candidate.json")
    assert sha(BASE/"UC3_candidate.json") == "2b34ca0e00ad384ad0cf2b92c4d6de56f57b2c36a9dd9fa3c331df5d7a500bcf"
    assert sha(BASE/"UC3R_protocol.md") == "19c56981a886d8ef5d502f8af095b8b9f1e70f22560ddd50b827ac0bbadd6ede"
    for name, digest in index["evidence_sha256"].items():
        assert sha(BASE/name) == digest
    events = csv_groups("UC3_candidate_events.csv")
    frames = csv_groups("UC3_candidate_frames.csv")
    archive = csv_groups("UC3_candidate_summary.csv")
    observations = {r["run_id"]:r for r in read_json("UC3_candidate_observations.json")}
    def product(name):
        with (out/name).open(newline="") as stream:
            return list(csv.DictReader(stream))
    rows = product("UC3R_tags.csv")
    tags = {(r["run_id"], int(r["unit_index"])):r for r in rows}
    assert len(rows) == len(tags)
    bs = product("UC3R_buds.csv")
    buds = {(r["run_id"],int(r["unit_index"]),int(r["tick"])):r for r in bs}
    assert len(bs) == len(buds)
    tally = Counter()
    hits = set()
    post = set()
    for start in read_json("UC3_candidate_initial.json"):
        run = start["run_id"]
        tracks, meta = world(start, events[run], archive[run][0], observations[run], frames[run])
        tally.update(worlds=1,frames=meta["frames"], attempts=meta["attempts"], changes=meta["changes"])
        for t in tracks:
            row = tags.pop((run,t["tag"]))
            tally["tags"] += 1
            assert t["seen"] == int(row["seen_edits"])
            if t["peak"] is None:
                assert int(row["peak_core"]) < 4 and row["stage"] == "no_peak"
            else:
                assert (int(row["peak_tick"]),int(row["peak_core"])) == (t["peak"],t["Kpeak"])
                assert json.loads(row["peak_instances"]) == [list(e) for e in t["peak_edges"]]
            assert (row["loss_tick"] or None) == (str(t["loss"]) if t["loss"] else None)
            assert (row["loss_kind"] or None) == t["cause"]
            assert (row["loss_split"] == "True") == bool(t["split"])
            if t["loss"]:
                assert int(row["loss_core"]) == t["Kloss"]
            assert json.loads(row["retained_instances"]) == [list(e) for e in t["remnants"]]
            assert int(row["followup_edits"]) == len(t["follow"])
            hit = joint = new_hit = new_joint = None
            for b in t["buds"]:
                actual = buds.pop((run,t["tag"],b["tick"]))
                tally["bud_observations"] += 1
                for field, key in (("source","source"),("anchor","anchor"),("edge_birth_tick","birth"),
                                   ("incident_R","numerator"),("degree","degree"),("core_after","K")):
                    assert int(actual[field]) == b[key]
                assert (actual["hit"] == "True") == b["hits"]
                if b["hits"]:
                    hit = hit or b["tick"]
                    hits.add((run,b["tick"]))
                    if b["birth"] > 0:
                        new_hit = new_hit or b["tick"]
                        post.add((run,b["tick"]))
            if t["joint"]:
                joint = t["joint"][1]
            if new_hit:
                new_joint = next((g for g in t["growths"] if g>=new_hit),None)
            for field, value in (("first_hit_tick",hit),("post_initial_hit_tick",new_hit),
                                 ("growth_tick",next(iter(t["growths"]),None)),
                                 ("joint_growth_tick",joint),("post_initial_joint_growth_tick",new_joint)):
                assert row[field] == ("" if value is None else str(value))
    assert not tags and not buds
    record=json.loads((out/"UC3R_result.json").read_text())
    assert sorted(hits)==list(map(tuple,record["hit_events"]))
    assert sorted(post)==list(map(tuple,record["post_initial_hit_events"]))
    for name,digest in record["output_sha256"].items():
        assert sha(out/name)==digest
    return dict(tally, distinct_hits=len(hits), distinct_post_initial_hits=len(post))


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=BASE,help="Existing UC3R product directory to verify")
    print(json.dumps(verify(parser.parse_args().out),sort_keys=True))
