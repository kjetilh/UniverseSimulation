#!/usr/bin/env python3
"""Audit residual-component geometry around v16x high-inclusion edges."""
from __future__ import annotations

import networkx as nx

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x


OUTPUT = v16x.DOC / "v16x_postrun_top_edge_component_audit.csv"


def run() -> None:
    v16x.verify_outputs()
    concentration = {
        (int(row["growth_seed"]), int(row["run_offset"])): row
        for row in v16i.read_csv(v16x.DOC / "v16x_postrun_combined_seed_concentration.csv")
    }
    rows = []
    for dag, metadata in v16x.load_runs():
        source = concentration[(dag.growth_seed, dag.run_offset)]
        edge = (int(source["top_parent_event_id"]), int(source["top_child_event_id"]))
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        residual = v16x.residual_graph(space, space.source_edges)
        components = list(nx.strongly_connected_components(residual))
        labels = {
            node: index
            for index, component in enumerate(components)
            for node in component
        }
        left = v16x.parent_node(edge[0])
        right = v16x.slot_node(space.slot_by_edge[edge])
        if labels[left] != labels[right]:
            raise ValueError("reported top edge is not globally variable")
        component = components[labels[left]]
        internal = [
            candidate for candidate in space.candidates
            if v16x.parent_node(candidate[0]) in component
            and v16x.slot_node(space.slot_by_edge[candidate]) in component
        ]
        internal_source = [candidate for candidate in internal if candidate in space.source_edges]
        path = nx.shortest_path(residual, source=left, target=right)
        witness = v16x.alternating_cycle_witness(space, residual, edge)
        changed = len(space.source_edges - witness)
        rows.append({
            **dag.prefix,
            "top_parent_event_id": edge[0],
            "top_child_event_id": edge[1],
            "combined_inclusion_count": int(source["combined_inclusion_count"]),
            "combined_trial_count": int(source["combined_trial_count"]),
            "combined_inclusion_rate": float(source["combined_inclusion_rate"]),
            "residual_scc_node_count": len(component),
            "residual_scc_parent_count": sum(node[0] == "parent" for node in component),
            "residual_scc_slot_count": sum(node[0] == "slot" for node in component),
            "residual_scc_candidate_edge_count": len(internal),
            "residual_scc_source_edge_count": len(internal_source),
            "residual_scc_candidate_surplus": len(internal) - len(internal_source),
            "shortest_alternating_return_path_edge_count": len(path) - 1,
            "witness_changed_source_edge_count": changed,
            "witness_changed_edge_fraction": changed / space.edge_count,
            "witness_removes_top_edge_pass": int(edge not in witness),
            "witness_assignment_integrity_pass": int(v16x.assignment_integrity(space, witness)),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    v16i.write_csv(OUTPUT, rows)
    print(f"[v16x-component] complete rows={len(rows)}")


def verify_outputs() -> None:
    rows = v16i.read_csv(OUTPUT)
    if len(rows) != 6:
        raise ValueError("v16x component audit row count failed")
    if not all(
        int(row["witness_removes_top_edge_pass"])
        and int(row["witness_assignment_integrity_pass"])
        and row["source_spectrum_computed"] == "0"
        and row["observed_effect_computed"] == "0"
        for row in rows
    ):
        raise ValueError("v16x component witness integrity failed")
    print("[v16x-component] output verification pass")


if __name__ == "__main__":
    run()
    verify_outputs()
