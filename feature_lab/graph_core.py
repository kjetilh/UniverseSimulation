"""Core graph and state primitives for the feature lab."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, List, Optional, Set


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

    def edge_list(self) -> List[tuple[int, int]]:
        return sorted((min(a, b), max(a, b)) for a, neighbors in self.adj.items() for b in neighbors if a < b)

    def random_node(self, rng: random.Random) -> Optional[int]:
        nodes = self.nodes()
        return rng.choice(nodes) if nodes else None

    def random_neighbor(self, node: int, rng: random.Random) -> Optional[int]:
        neighbors = list(self.neighbors(node))
        return rng.choice(neighbors) if neighbors else None

    def prune_isolated(self) -> List[int]:
        """Remove isolated nodes and return their ids."""
        removed: List[int] = []
        for node in list(self.adj.keys()):
            if not self.adj[node]:
                self.remove_node(node)
                removed.append(node)
        return removed


@dataclass
class State:
    """Simulation state for the relational universe toy model."""

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
    """Create a connected seed graph with tokens placed on the cycle."""
    g = UGraph()
    cycle_size = max(2, initial_cycle)
    for node in range(cycle_size):
        g.add_edge(node, (node + 1) % cycle_size)
    tokens = [rng.randrange(cycle_size) for _ in range(max(1, initial_tokens))]
    return State(g=g, tokens=tokens, t=0.0, next_node_id=cycle_size)


def count_components(g: UGraph) -> int:
    """Return the number of connected components."""
    nodes = g.nodes()
    if not nodes:
        return 0

    seen: Set[int] = set()
    count = 0
    for start in nodes:
        if start in seen:
            continue
        count += 1
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for neighbor in g.neighbors(node):
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return count


def beta1_cycle_rank(g: UGraph) -> int:
    """Return the first Betti number for the current graph."""
    return g.num_edges() - g.num_nodes() + count_components(g)


def is_bridge(g: UGraph, a: int, b: int, bfs_cap: Optional[int] = None) -> bool:
    """Return True if removing edge (a, b) disconnects the graph."""
    if not g.has_edge(a, b):
        return False

    queue = [a]
    seen = {a}
    explored = 0
    while queue:
        node = queue.pop()
        explored += 1
        if bfs_cap is not None and explored > bfs_cap:
            return False
        for neighbor in g.neighbors(node):
            if (node == a and neighbor == b) or (node == b and neighbor == a):
                continue
            if neighbor == b:
                return False
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return True


def common_neighbors_count(g: UGraph, a: int, b: int) -> int:
    """Return the number of common neighbors shared by a and b."""
    if a not in g.adj or b not in g.adj:
        return 0
    if len(g.adj[a]) < len(g.adj[b]):
        return sum(neighbor in g.adj[b] for neighbor in g.adj[a])
    return sum(neighbor in g.adj[a] for neighbor in g.adj[b])
