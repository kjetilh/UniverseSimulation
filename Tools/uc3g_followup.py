"""UC3G follow-up from a post-intervention state in the tagged component.

No historical edge information enters the observer or the transition kernel.
The gate is the first observed increase of at least two 2-core nodes.
"""
from __future__ import annotations

import hashlib
import json
import random

from Tools import local_growth_candidate as kernel
from Tools.local_growth_observer import _region


WINDOW = 16
ATTEMPT_CAP = 16384


def _descendant(state, tag):
    """Project to the tag's current component and retain local unit order."""
    component = {state.units[tag]}
    stack = list(component)
    while stack:
        for neighbor in state.adjacency[stack.pop()]:
            if neighbor not in component:
                component.add(neighbor)
                stack.append(neighbor)
    indices = [i for i, host in enumerate(state.units) if host in component]
    if len(component) == len(state.adjacency):
        return state, tag, indices
    local = kernel.GrowthState(
        {v: set(state.adjacency[v]) for v in component},
        [state.units[i] for i in indices],
        ticks=state.ticks,
        attempts=state.attempts,
        next_node_id=state.next_node_id,
    )
    return local, indices.index(tag), indices


def _core_size(state):
    return len(_region(state.adjacency, set(state.adjacency))["core_nodes"])


def follow(state, tag, seed, mode="natural", setup=None):
    """Observe up to 16 successful local changes; the setup slide is excluded.

    Removing outside-component draws exactly thins the uniform unit draw
    because UC3 cannot merge components or transmit effects between them.
    Birth names remain above existing names, preserving their local ordering.
    A split counts once and subsequent observations follow the tag's host.

    The null alternates the exact inverse and forward setup slides. The
    positive chooses a uniform adjacent anchor for each of up to two legal
    buds by the tag before resuming the normal law if still needed.
    """
    if mode not in ("natural", "null", "positive"):
        raise ValueError(f"unrecognized follow-up mode {mode!r}")
    if not isinstance(tag, int) or isinstance(tag, bool) or not 0 <= tag < len(state.units):
        raise ValueError("tag must index an existing unit")
    rng = random.Random(seed)
    local, tag, indices = _descendant(kernel.clone_state(state), tag)
    original_indices = indices
    trace = hashlib.sha256()
    if mode == "null":
        if not setup or setup["unit_index"] not in indices:
            raise ValueError("the null needs the setup actor in the tagged component")
        actor = indices.index(setup["unit_index"])
        if local.units[actor] != setup["target"]:
            raise ValueError("the null must start after the specified setup slide")
    start_core = current_core = _core_size(local)
    exposure = attempts = 0
    first_hit = None
    while True:
        if current_core >= start_core + 2:
            first_hit, stop = exposure, "hit"
            break
        if exposure == WINDOW:
            stop = "window"
            break
        if not local.adjacency[local.units[tag]]:
            stop = "absorbed"
            break
        if attempts == ATTEMPT_CAP:
            stop = "attempt_cap"
            break
        if mode == "null":
            destination = setup["source"] if exposure % 2 == 0 else setup["target"]
            event = kernel.apply_event(local, actor, "slide", destination, setup["carried"])
        elif mode == "positive" and exposure < 2:
            anchor = rng.choice(sorted(local.adjacency[local.units[tag]]))
            event = kernel.apply_event(local, tag, "bud", anchor)
        else:
            event = kernel.attempt_step(local, rng)
        attempts += 1
        original_actor = original_indices[event.unit_index]
        if event.changed:
            exposure += 1
            if event.kind == "cut":
                local, tag, selected = _descendant(local, tag)
                original_indices = [original_indices[i] for i in selected]
            current_core = _core_size(local)
        record = (attempts, exposure, event.changed, event.kind, original_actor,
                  event.source, event.target, event.carried, event.born, event.removed,
                  event.reason, current_core)
        trace.update((json.dumps(record, separators=(",", ":")) + "\n").encode("ascii"))
    return dict(success=first_hit is not None, first_hit=first_hit,
                exposure=exposure, attempts=attempts, stop=stop,
                k_start=start_core, k_final=current_core, censored=stop == "attempt_cap",
                trace_sha256=trace.hexdigest())
