"""Single-hop, outcome-blind matching at a UC3R loss checkpoint."""
from collections import Counter, defaultdict, deque
from dataclasses import asdict
from itertools import product

from Tools import local_growth_candidate as law
from Tools.local_change_candidate import _moves_at
from Tools.local_growth_observer import _region


def component(adj, root):
    seen = {root}
    stack = [root]
    while stack:
        node = stack.pop()
        for neighbor in adj[node] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return seen


def _pair(a, b):
    return (min(a, b), max(a, b))


def _hist(values):
    return sorted(Counter(values).items())


def _core_depths(adj, nodes):
    core = _region(adj, nodes)["core_nodes"]
    depths = dict.fromkeys(core, 0)
    queue = deque(core)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in depths:
                depths[v] = depths[u] + 1
                queue.append(v)
    return len(core), depths


def _local_counts(state, nodes, size, depths):
    result = []
    adj = state.adjacency
    for i, u in enumerate(state.units):
        if u not in nodes:
            continue
        # A bud on a pruned branch retains the path back to the old core.
        # On a tree only the new triangle survives pruning.
        bud_sizes = [size + 1 + max(depths[u], depths[v]) if size else 3
                     for v in adj[u]]
        result.append(dict(unit=i, degree=len(adj[u]), slide_choices=len(_moves_at(state, u)),
                           collapse_choices=len(law._collapse_neighbors(state, u)),
                           bud_core=_hist(bud_sizes)))
    return result


def _full_opportunities(state, tag, nodes, size, counts):
    """Enumerate legal choices. A tree's slide and cut results have empty cores."""
    adj = state.adjacency
    tag_host = state.units[tag]
    rows = []
    cut_cache = {}
    for count in counts:
        i = count["unit"]
        u = state.units[i]
        if size == 0:
            slides = [(0, count["slide_choices"])] if count["slide_choices"] else []
            cuts = [((True, 0), len(adj[u]))] if adj[u] else []
            collapses = []
        else:
            slide_sizes = []
            for v, carried in _moves_at(state, u):
                adj[u].remove(carried)
                adj[carried].remove(u)
                adj[v].add(carried)
                adj[carried].add(v)
                try:
                    slide_sizes.append(len(_region(adj, nodes)["core_nodes"]))
                finally:
                    adj[v].remove(carried)
                    adj[carried].remove(v)
                    adj[u].add(carried)
                    adj[carried].add(u)
            slides = _hist(slide_sizes)
            collapse_neighbors = law._collapse_neighbors(state, u)
            collapses = []
            if collapse_neighbors:
                # Both choices remove the same vertex and keep its component connected.
                for v in collapse_neighbors:
                    adj[v].remove(u)
                try:
                    remaining = nodes - {u}
                    collapse_size = len(_region(adj, remaining)["core_nodes"])
                finally:
                    for v in collapse_neighbors:
                        adj[v].add(u)
                collapses = [(collapse_size, len(collapse_neighbors))]
            cut_outcomes = []
            for v in sorted(adj[u]):
                # Only the cut actor crosses the removed edge. If that actor is
                # our tag its descendant can be on the other side of a bridge.
                focal_after = v if i == tag else tag_host
                key = (_pair(u, v), focal_after)
                if key not in cut_cache:
                    adj[u].remove(v)
                    adj[v].remove(u)
                    try:
                        part = component(adj, focal_after)
                        cut_cache[key] = (len(part) < len(nodes), len(_region(adj, part)["core_nodes"]))
                    finally:
                        adj[u].add(v)
                        adj[v].add(u)
                cut_outcomes.append(cut_cache[key])
            cuts = _hist(cut_outcomes)
        rows.append(dict(**count, slide_core=slides, collapse_core=collapses, cut_split_core=cuts))
    return rows


def opportunity_signature(state, tag):
    """Per focal-component unit, count targets by class and exact one-step outcome."""
    nodes = component(state.adjacency, state.units[tag])
    size, depths = _core_depths(state.adjacency, nodes)
    counts = _local_counts(state, nodes, size, depths)
    return _full_opportunities(state, tag, nodes, size, counts)


def _wl_witness(left, right, tag, nodes):
    """Joint color refinement. Unequal histograms certify rooted non-isomorphism."""
    occupancy = Counter(left.units)
    initial = {u: (u == left.units[tag], occupancy[u]) for u in nodes}
    colors = [initial, initial]
    histograms = []
    for iteration in range(1, len(nodes) + 1):
        descriptions = [
            {u: (old[u], tuple(sorted(old[v] for v in state.adjacency[u]))) for u in nodes}
            for old, state in zip(colors, (left, right))]
        vocabulary = sorted(set(descriptions[0].values()) | set(descriptions[1].values()))
        indices = {value: i for i, value in enumerate(vocabulary)}
        refined = [{u: indices[d] for u, d in per_node.items()} for per_node in descriptions]
        histograms = [_hist(side.values()) for side in refined]
        if histograms[0] != histograms[1]:
            return dict(method="joint_color_refinement_tag_host_and_unit_multiplicity",
                        iteration=iteration, preserved=histograms[0], rewired=histograms[1])
        if len(vocabulary) == len(set(colors[0].values()) | set(colors[1].values())):
            break
        colors = refined
    return None


def find_match(state, tag, retained):
    """Return (preserved, rewired, audit) or None. The checkpoint is untouched.

    Retained entries can be undirected pairs or UC3R (a, b, birth_tick)
    triples. The caller identifies continuous survival at this specific loss.
    Each fork takes one equally probable legal slide of the same selected unit
    over the same pivot. Only which adjacent endpoint is carried differs.
    """
    remnant = {_pair(entry[0], entry[1]) for entry in retained}
    nodes = component(state.adjacency, state.units[tag])
    if not remnant:
        return None
    if any(a not in nodes or b not in state.adjacency[a] for a, b in remnant):
        raise ValueError("R must consist of edges surviving in the focal component")
    baseline = len(_region(state.adjacency, nodes)["core_nodes"])
    for actor, source in enumerate(state.units):
        if source not in nodes:
            continue
        by_target = defaultdict(list)
        for target, carried in _moves_at(state, source):
            by_target[target].append(carried)
        for target, alternatives in sorted(by_target.items()):
            preserving = [a for a in alternatives if _pair(source, a) not in remnant]
            rewiring = [a for a in alternatives if _pair(source, a) in remnant]
            if not preserving or not rewiring:
                continue
            cache = {}
            signatures = {}
            for p, r in product(preserving, rewiring):
                for carried in (p, r):
                    if carried in cache:
                        continue
                    after = law.clone_state(state)
                    event = law.apply_event(after, actor, "slide", target, carried)
                    if component(after.adjacency, after.units[tag]) != nodes:
                        raise ValueError("A legal slide changed the component partition")
                    size, depths = _core_depths(after.adjacency, nodes)
                    cache[carried] = (after, event, _local_counts(after, nodes, size, depths)
                                      if size == baseline else None)
                left, le, lc = cache[p]
                right, re, rc = cache[r]
                if lc is None or lc != rc:
                    continue
                witness = _wl_witness(left, right, tag, nodes)
                if not witness:
                    continue
                for carried in (p, r):
                    if carried not in signatures:
                        after, _, counts = cache[carried]
                        signatures[carried] = _full_opportunities(after, tag, nodes, baseline, counts)
                if signatures[p] != signatures[r]:
                    continue
                degrees = {u: len(left.adjacency[u]) for u in sorted(nodes)}
                if left.units != right.units or degrees != {u: len(right.adjacency[u]) for u in nodes}:
                    raise ValueError("Matched setup must preserve per-name degrees and unit hosts across arms")
                return left, right, dict(preserved_event=asdict(le), rewired_event=asdict(re),
                     setup_tick=left.ticks, setup_attempt=left.attempts, tag=tag,
                     loss_core=baseline, component_nodes=sorted(nodes), degrees=degrees,
                     unit_hosts=list(left.units), retained_count=len(remnant),
                     retained_after_preserved=len(remnant), retained_after_rewired=len(remnant) - 1,
                     opportunities=signatures[p], nonisomorphism=witness)
    return None
