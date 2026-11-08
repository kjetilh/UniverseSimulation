"""Prospective uninterrupted edge inheritance in the tagged UC3 descendant."""
import random

from Tools import local_growth_candidate as law
from Tools.local_growth_observer import _region
from Tools.uc3g_followup import _descendant
from Tools.uc3g_match import component
from Tools.uc3m_cycles import setup
from Tools.run_uc3g import restore


def common_cohort(pair):
    block = set(map(tuple, pair["match"]["block"]))
    for arm in ("preserved", "rewired"):
        state = setup(restore(pair["loss_state"]), pair["match"]["spec"], arm)
        nodes = component(state.adjacency, state.units[pair["tag"]])
        block.intersection_update(map(tuple, _region(state.adjacency, nodes)["core_edges"]))
    return [inst for inst in pair["retained"] if tuple(inst[:2]) in block]


def reference_step(local, tag, rng, mode, tick, rising, parents, landmarks):
    host = local.units[tag]
    if mode == "null" and tick < 6:
        if tick == 0:
            anchor = rng.choice(sorted(local.adjacency[host]))
            event = law.apply_event(local, tag, "bud", anchor)
            landmarks.extend((host, anchor, event.born))
            return event
        origin, anchor, daughter = landmarks
        kind, dest = (("cut", anchor), ("cut", origin), ("bud", daughter),
                      ("cut", origin), ("cut", daughter))[tick - 1]
        return law.apply_event(local, tag, kind, dest)
    if rising:
        parents.append(host)
        return law.apply_event(local, tag, "bud", rng.choice(sorted(local.adjacency[host])))
    return law.apply_event(local, tag, "collapse", parents.pop())


def follow(pair, arm, mode, seed):
    state = setup(restore(pair["loss_state"]), pair["match"]["spec"], arm)
    local, tag, _ = _descendant(state, pair["tag"])
    # Array indices refer to immutable triples recorded in the matched pair.
    cohort = [tuple(inst[:2]) for inst in pair["cohort"]]
    alive = set(range(len(cohort)))
    inherited = alive.copy()
    strict = alive.copy()
    rng = random.Random(seed)
    parents, landmarks, marks, witnesses = [], [], [], []
    start = extreme = k = pair["loss"]["core"]
    t = attempts = 0
    while t < 96 and attempts < 16384 and local.adjacency[local.units[tag]] and len(marks) < 5:
        rising = len(marks) % 2 == 0
        event = (law.attempt_step(local, rng) if mode == "natural" else
                 reference_step(local, tag, rng, mode, t, rising, parents, landmarks))
        attempts += 1
        if not event.changed:
            continue
        t += 1
        if event.kind == "cut":
            local, tag, _ = _descendant(local, tag)
        region = _region(local.adjacency, set(local.adjacency))
        edges = set(map(tuple, region["edges"]))
        alive = {i for i in alive if cohort[i] in edges}
        k = len(region["core_nodes"])
        if marks:
            extreme = min(extreme, k) if rising else max(extreme, k)
        if (k - extreme if rising else extreme - k) >= 2:
            core_edges = set(map(tuple, region["core_edges"]))
            present = {i for i in alive if cohort[i] in core_edges}
            witnesses.append(sorted(present))
            strict &= present
            if rising:
                inherited &= present
            marks.append((t, k))
            extreme = k
    complete = len(marks) == 5
    stop = ("complete" if complete else "window" if t == 96 else "absorbed"
            if not local.adjacency[local.units[tag]] else "attempt_cap")
    return dict(success=complete and bool(inherited), complete=complete,
                inherited=sorted(inherited) if complete else [], strict=sorted(strict) if complete else [],
                marks=marks, witnesses=witnesses, exposure=t, attempts=attempts, stop=stop,
                censored=stop=="attempt_cap")
