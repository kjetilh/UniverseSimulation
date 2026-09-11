"""UC3 structural qualification only; no candidate/macropattern measurements."""
import copy
from itertools import combinations
import random
import unittest

from Tools import local_growth_candidate as model


def all_small_graphs():
    for n in range(1, 5):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            yield n, [e for i, e in enumerate(possible) if mask & (1 << i)]


def beta(state):
    return len(model.edge_set(state)) - len(state.adjacency) + len(model.component_partition(state))


def legal_requests(state, unit_index):
    source = state.units[unit_index]
    neighbors = sorted(state.adjacency[source])
    requests = [("slide", u, a) for u, a in model.admissible_moves(state, unit_index)]
    requests += [(kind, u, None) for kind in ("bud", "cut") for u in neighbors]
    if (len(neighbors) == 2 and neighbors[1] in state.adjacency[neighbors[0]]
            and state.units.count(source) == 1):
        requests += [("collapse", u, None) for u in neighbors]
    return requests


class Choices:
    def __init__(self, values):
        self.values, self.bounds = iter(values), []

    def randrange(self, upper):
        self.bounds.append(upper)
        value = next(self.values)
        assert 0 <= value < upper
        return value


class LocalGrowthTests(unittest.TestCase):
    def check_transition(self, before, state, event):
        model.validate_state(state)
        old_nodes, new_nodes = set(before.adjacency), set(state.adjacency)
        old_edges, new_edges = model.edge_set(before), model.edge_set(state)
        old_components = model.component_partition(before)
        new_components = model.component_partition(state)
        self.assertEqual(len(state.units), len(before.units))
        self.assertEqual(state.attempts, before.attempts + 1)
        for i, host in enumerate(state.units):
            self.assertIn(host, state.adjacency)
            if i != event.unit_index:
                self.assertEqual(host, before.units[i])
        if not event.changed:
            self.assertEqual(model.state_snapshot(state)[:4], model.state_snapshot(before)[:4])
            self.assertEqual(state.next_node_id, before.next_node_id)
            return
        self.assertEqual(state.ticks, before.ticks + 1)
        self.assertEqual(event.source, before.units[event.unit_index])
        self.assertEqual(state.units[event.unit_index], event.target)
        for component in new_components:
            # No event may join previously separate components.
            surviving = component & old_nodes
            if surviving:
                self.assertTrue(any(surviving <= c for c in old_components))
        if event.kind != "bud":
            self.assertIn(event.target, before.adjacency[event.source])
            self.assertEqual(state.next_node_id, before.next_node_id)
        else:
            self.assertEqual(event.born, before.next_node_id)
            self.assertEqual(state.next_node_id, before.next_node_id + 1)
        delta = (len(new_nodes)-len(old_nodes), len(new_edges)-len(old_edges),
                 len(new_components)-len(old_components), beta(state)-beta(before))
        if event.kind == "slide":
            self.assertEqual(delta, (0, 0, 0, 0))
            self.assertEqual(old_components, new_components)
            self.assertEqual(len(old_edges ^ new_edges), 2)
        elif event.kind == "bud":
            self.assertEqual(delta, (1, 2, 0, 1))
            self.assertEqual(new_nodes-old_nodes, {event.born})
            self.assertEqual(old_nodes-new_nodes, set())
            self.assertEqual(state.adjacency[event.born], {event.source, event.carried})
            self.assertIn(event.carried, before.adjacency[event.source])
            self.assertNotIn(event.target, old_nodes)
            self.assertTrue(old_edges <= new_edges)
        elif event.kind == "collapse":
            self.assertEqual(delta, (-1, -2, 0, -1))
            self.assertEqual(old_nodes-new_nodes, {event.source})
            self.assertEqual(event.removed, event.source)
            self.assertEqual(new_nodes-old_nodes, set())
            self.assertEqual(new_components, frozenset(c-{event.source} for c in old_components))
        elif event.kind == "cut":
            self.assertIn(delta, ((0, -1, 0, -1), (0, -1, 1, 0)))
            self.assertEqual(new_nodes, old_nodes)
            self.assertEqual(old_edges-new_edges, {tuple(sorted((event.source, event.target)))})
        self.assertEqual(len(new_edges)-2*len(new_nodes),
                         len(old_edges)-2*len(old_nodes)-(event.kind == "cut"))

    def test_exhaustive_graphs_positions_and_legal_events(self):
        positions = 0
        checked = dict.fromkeys(model.CLASSES, 0)
        for n, edges in all_small_graphs():
            for host in range(n):
                original = model.make_state(range(n), edges, [host])
                positions += 1
                for kind, target, carried in legal_requests(original, 0):
                    state = model.clone_state(original)
                    result = model.apply_event(state, 0, kind, target, carried)
                    checked[kind] += 1
                    self.check_transition(original, state, result)
                    if kind == "bud":
                        model.apply_event(state, 0, "collapse", host)
                        self.assertEqual(model.state_snapshot(state)[:3], model.state_snapshot(original)[:3])
                        self.assertEqual(state.next_node_id, original.next_node_id + 1)
        self.assertEqual(positions, 285)
        self.assertEqual(checked, {"slide": 198, "bud": 410, "collapse": 102, "cut": 410})

    def test_exhaustive_label_equivariance_up_to_fresh_name(self):
        names = [-8, 17, 3, 40]
        for n, edges in all_small_graphs():
            mapping = {i: names[i] for i in range(n)}
            for host in range(n):
                original = model.make_state(range(n), edges, [host])
                renamed = model.make_state(names[:n], [(mapping[a], mapping[b]) for a,b in edges], [mapping[host]])
                requests = legal_requests(original, 0)
                mapped_requests = {(k, mapping[u], None if a is None else mapping[a]) for k,u,a in requests}
                self.assertEqual(mapped_requests, set(legal_requests(renamed, 0)))
                # Equal class weights and corresponding choice counts give
                # equal probability to each mapped unit/class/target outcome.
                for kind, target, carried in requests:
                    left, right = model.clone_state(original), model.clone_state(renamed)
                    le = model.apply_event(left, 0, kind, target, carried)
                    re = model.apply_event(right, 0, kind, mapping[target], None if carried is None else mapping[carried])
                    extended = dict(mapping)
                    if le.born is not None:
                        extended[le.born] = re.born
                    self.assertEqual({extended[v]: {extended[w] for w in ns}
                                      for v,ns in left.adjacency.items()}, right.adjacency)
                    self.assertEqual([extended[v] for v in left.units], right.units)

    def test_birth_id_is_never_reused_after_collapse(self):
        state = model.make_state([0, 1], [(0, 1)], [0])
        first = model.apply_event(state, 0, "bud", 1)
        self.assertEqual((first.source, first.target, first.carried, first.born), (0, 2, 1, 2))
        model.apply_event(state, 0, "collapse", 0, 1)
        clone = model.clone_state(state)
        second = model.apply_event(clone, 0, "bud", 1)
        self.assertEqual(second.born, 3)
        self.assertEqual(state.next_node_id, 3)
        self.assertEqual(clone.next_node_id, 4)

    def test_blocked_classes_draw_no_target_and_do_not_resample(self):
        fixtures = [(model.make_state([0], [], [0]), slot) for slot in range(8)]
        # K2 slide/collapse block; bud and cut remain available.
        fixtures += [(model.make_state([0, 1], [(0, 1)], [0]), slot) for slot in (0, 1, 2, 3, 5, 6)]
        # A newborn triangular host necessarily blocks the old slide class.
        triangle = model.make_state(range(3), [(0, 1), (1, 2), (2, 0)], [0])
        fixtures += [(triangle, slot) for slot in range(4)]
        for original, slot in fixtures:
            state = model.clone_state(original)
            rng = Choices([0, slot])
            event = model.attempt_step(state, rng)
            self.assertFalse(event.changed)
            self.assertEqual(rng.bounds, [1, 8])
            self.check_transition(original, state, event)
        empty = model.make_state([], [], [])
        event = model.attempt_step(empty, Choices([]))
        self.assertEqual(event.reason, "no_units")
        self.assertEqual((empty.ticks, empty.attempts), (0, 1))

    def test_class_weights_and_target_choice_bounds(self):
        # A triangular host has bud/collapse/cut, and slide slots stay blocked.
        expected = ["slide"]*4 + ["bud", "collapse", "collapse", "cut"]
        original = model.make_state(range(3), [(0, 1), (1, 2), (2, 0)], [0, 1])
        for slot, kind in enumerate(expected):
            for neighbor_index in range(2):
                state = model.clone_state(original)
                rng = Choices([0, slot] + ([] if kind == "slide" else [neighbor_index]))
                event = model.attempt_step(state, rng)
                self.assertEqual(event.kind, kind)
                self.assertEqual(rng.bounds, [2, 8] + ([] if kind == "slide" else [2]))
                self.check_transition(original, state, event)
        isolated_unit = model.make_state(range(4), [(0, 1), (0, 2)], [0, 3])
        rng = Choices([1, 4])
        self.assertFalse(model.attempt_step(isolated_unit, rng).changed)
        self.assertEqual(rng.bounds, [2, 8])

    def test_unit_collision_prevents_collapse_without_losing_units(self):
        state = model.make_state(range(3), [(0, 1), (1, 2), (2, 0)], [0, 0])
        before = model.state_snapshot(state)
        with self.assertRaises(ValueError):
            model.apply_event(state, 0, "collapse", 1)
        self.assertEqual(model.state_snapshot(state), before)
        rng = Choices([1, 5])
        self.assertFalse(model.attempt_step(state, rng).changed)
        self.assertEqual(state.units, [0, 0])
        self.assertEqual((state.ticks, state.attempts), (0, 1))

    def test_cut_preserves_isolated_hosts_and_their_units(self):
        state = model.make_state([0, 1], [(0, 1)], [0, 1])
        result = model.apply_event(state, 0, "cut", 1)
        self.assertEqual(state.units, [1, 1])
        self.assertEqual(state.adjacency, {0: set(), 1: set()})
        self.assertEqual(result.target, 1)
        for slot in range(8):
            before = model.clone_state(state)
            result = model.attempt_step(state, Choices([0, slot]))
            self.assertFalse(result.changed)
            self.check_transition(before, state, result)

    def test_invalid_event_requests_are_transactional(self):
        original = model.make_state(range(4), [(0, 1), (0, 2)], [0])
        bad = [(0, "unknown", 1, None), (-1, "bud", 1, None),
               (True, "bud", 1, None), (0, "bud", None, None),
               (0, "bud", True, None), (0, "bud", 3, None),
               (0, "bud", 1, 2), (0, "cut", 1, 2),
               (0, "collapse", 1, None), (0, "slide", 1, None),
               (0, "slide", 1, 1), (0, "slide", 1, 3)]
        for request in bad:
            state = model.clone_state(original)
            before = model.state_snapshot(state)
            with self.assertRaises(ValueError):
                model.apply_event(state, *request)
            self.assertEqual(model.state_snapshot(state), before)
        triangle = model.make_state(range(3), [(0, 1), (1, 2), (2, 0)], [0])
        for carried in (0, 1, 9, False, "2"):
            before = model.state_snapshot(triangle)
            with self.assertRaises(ValueError):
                model.apply_event(triangle, 0, "collapse", 1, carried)
            self.assertEqual(model.state_snapshot(triangle), before)

    def test_invalid_weights_state_and_allocator_before_rng(self):
        original = model.make_state(range(3), [(0, 1), (0, 2)], [0])
        for weights in ((0,0,0,0), (4,1,2), (4,1,2,-1), (4,1,2,True), (4,1,2,0.5), None):
            state = model.clone_state(original)
            rng = random.Random(17)
            before, stream = model.state_snapshot(state), rng.getstate()
            with self.assertRaises(ValueError):
                model.attempt_step(state, rng, weights)
            self.assertEqual(model.state_snapshot(state), before)
            self.assertEqual(rng.getstate(), stream)
        for counter in (-1, 2, False, 3.5):
            state = model.clone_state(original)
            state.next_node_id = counter
            before, rng = copy.deepcopy(state), random.Random(19)
            stream = rng.getstate()
            with self.assertRaises(ValueError):
                model.attempt_step(state, rng)
            self.assertEqual(state, before)
            self.assertEqual(rng.getstate(), stream)
        with self.assertRaises(ValueError):
            model.make_state([0, 1], [(0, 1)], [0], next_node_id=1)

    def test_deterministic_replay_and_observer_noninterference(self):
        original = model.make_state(range(6), [(0,1),(1,2),(2,3),(3,0),(3,4),(4,5)], [0,3])
        left, right = model.clone_state(original), model.clone_state(original)
        lrng, rrng = random.Random(121), random.Random(121)
        global_stream = random.getstate()
        for _ in range(256):
            before, local_stream = model.state_snapshot(right), rrng.getstate()
            model.edge_set(right)
            model.component_partition(right)
            model.clone_state(right)
            self.assertEqual(before, model.state_snapshot(right))
            self.assertEqual(local_stream, rrng.getstate())
            self.assertEqual(model.attempt_step(left, lrng), model.attempt_step(right, rrng))
            self.assertEqual(model.state_snapshot(left), model.state_snapshot(right))
        self.assertEqual(random.getstate(), global_stream)

    def test_bounded_multicomponent_multiunit_stress_and_accounting(self):
        for seed in range(3100, 3104):
            rng = random.Random(seed)
            state = model.make_state(range(9), [(0,1),(1,2),(2,0),(3,4),(4,5),(5,6),(6,3)], [0,4,8,4])
            initial_balance = len(model.edge_set(state))-2*len(state.adjacency)
            allocated = set(state.adjacency)
            cuts = 0
            for _ in range(256):
                before = model.clone_state(state)
                event = model.attempt_step(state, rng)
                self.check_transition(before, state, event)
                if event.born is not None:
                    self.assertNotIn(event.born, allocated)
                    allocated.add(event.born)
                cuts += event.changed and event.kind == "cut"
                self.assertEqual(len(model.edge_set(state))-2*len(state.adjacency)+cuts, initial_balance)
                self.assertEqual(state.units[2], 8)


if __name__ == "__main__":
    unittest.main()
