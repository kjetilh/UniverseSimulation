"""Core graph primitives shared by the rule-delta lab and perturbation lab."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random
from typing import Dict, Iterable, List, Optional, Set


class UGraph:
    """Simple undirected graph with integer node ids."""

    def __init__(self) -> None:
        self.adj: Dict[int, Set[int]] = {}

    def copy(self) -> "UGraph":
        cloned = UGraph()
        cloned.adj = {node: set(neighbors) for node, neighbors in self.adj.items()}
        return cloned

    def add_node(self, node: int) -> None:
        if node not in self.adj:
            self.adj[node] = set()

    def add_edge(self, a: int, b: int) -> None:
        if a == b:
            return
        self.add_node(a)
        self.add_node(b)
        self.adj[a].add(b)
        self.adj[b].add(a)

    def has_edge(self, a: int, b: int) -> bool:
        return a in self.adj and b in self.adj[a]

    def remove_edge(self, a: int, b: int) -> None:
        if a in self.adj:
            self.adj[a].discard(b)
        if b in self.adj:
            self.adj[b].discard(a)

    def remove_node(self, node: int) -> None:
        if node not in self.adj:
            return
        for neighbor in list(self.adj[node]):
            self.adj[neighbor].discard(node)
        del self.adj[node]

    def neighbors(self, node: int) -> Set[int]:
        return self.adj.get(node, set())

    def degree(self, node: int) -> int:
        return len(self.neighbors(node))

    def nodes(self) -> List[int]:
        return list(self.adj.keys())

    def num_nodes(self) -> int:
        return len(self.adj)

    def num_edges(self) -> int:
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def prune_isolated(self) -> List[int]:
        removed: List[int] = []
        for node in list(self.adj.keys()):
            if not self.adj[node]:
                self.remove_node(node)
                removed.append(node)
        return removed


@dataclass
class State:
    """Simulation state for the relational-universe toy model."""

    g: UGraph
    tokens: List[int]
    t: float
    next_node_id: int

    def copy(self) -> "State":
        return State(
            g=self.g.copy(),
            tokens=list(self.tokens),
            t=self.t,
            next_node_id=self.next_node_id,
        )


def bootstrap(initial_cycle: int, initial_tokens: int, rng: random.Random) -> State:
    """Create a connected cycle with tokens placed on it."""

    graph = UGraph()
    cycle_size = max(2, initial_cycle)
    for node in range(cycle_size):
        graph.add_edge(node, (node + 1) % cycle_size)
    tokens = [rng.randrange(cycle_size) for _ in range(max(1, initial_tokens))]
    return State(g=graph, tokens=tokens, t=0.0, next_node_id=cycle_size)


def count_components(graph: UGraph) -> int:
    """Return the number of connected components."""

    nodes = graph.nodes()
    if not nodes:
        return 0

    seen: Set[int] = set()
    components = 0
    for start in nodes:
        if start in seen:
            continue
        components += 1
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for neighbor in graph.neighbors(node):
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return components


def beta1_cycle_rank(graph: UGraph) -> int:
    """Return the first Betti number of the graph."""

    return graph.num_edges() - graph.num_nodes() + count_components(graph)


def is_bridge(graph: UGraph, a: int, b: int, bfs_cap: Optional[int] = None) -> bool:
    """Return True iff removing edge (a, b) disconnects the graph."""

    if not graph.has_edge(a, b):
        return False

    stack = [a]
    seen = {a}
    explored = 0
    while stack:
        node = stack.pop()
        explored += 1
        if bfs_cap is not None and explored > bfs_cap:
            return False
        for neighbor in graph.neighbors(node):
            if (node == a and neighbor == b) or (node == b and neighbor == a):
                continue
            if neighbor == b:
                return False
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return True


def common_neighbors_count(graph: UGraph, a: int, b: int) -> int:
    """Return the number of shared neighbors between a and b."""

    if a not in graph.adj or b not in graph.adj:
        return 0
    if len(graph.adj[a]) < len(graph.adj[b]):
        return sum(neighbor in graph.adj[b] for neighbor in graph.adj[a])
    return sum(neighbor in graph.adj[a] for neighbor in graph.adj[b])


def multi_source_distances(
    graph: UGraph,
    sources: Iterable[int],
    max_radius: Optional[int] = None,
) -> Dict[int, int]:
    """Return shortest graph distances from a source set."""

    queue: deque[int] = deque()
    distances: Dict[int, int] = {}
    for source in sorted(set(sources)):
        if source in graph.adj:
            distances[source] = 0
            queue.append(source)

    while queue:
        node = queue.popleft()
        distance = distances[node]
        if max_radius is not None and distance >= max_radius:
            continue
        for neighbor in graph.neighbors(node):
            if neighbor not in distances:
                distances[neighbor] = distance + 1
                queue.append(neighbor)
    return distances

