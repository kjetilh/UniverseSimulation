#!/usr/bin/env python3
"""Post-run audit of the sole failed v16z representation subcheck.

The formal v16z gate compared raw kernel dictionaries whose SlotClass keys are
expected to change under semantic relabeling. This audit leaves the frozen gate
untouched and compares the induced concrete 2x2 move sets instead.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16w_global_null_qualification_gate as v16w
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16y_reversible_global_measure_gate as v16y
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
AUDIT_CSV = DOC / "v16z_postrun_representation_audit.csv"
AUDIT_MD = DOC / "v16z_postrun_representation_audit.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def move_signature(
    kernel: v16y.ChainKernel,
    selected: frozenset[v16x.Edge],
) -> tuple[tuple[tuple[v16x.Edge, ...], tuple[v16x.Edge, ...]], ...]:
    return tuple((move.remove, move.add) for move in v16y.neighbor_moves(kernel, selected))


def verify_formal_products() -> str:
    prereg = v16i.read_csv(v16z.PRE_REGISTRATION)
    if len(prereg) != 1:
        raise ValueError("v16z preregistration row count failed")
    if prereg[0]["script_sha256"] != file_sha256(v16z.SCRIPT):
        raise ValueError("v16z frozen script hash changed")
    if prereg[0]["source_chain_sha256"] != file_sha256(v16z.SOURCE_CHAIN):
        raise ValueError("v16z frozen source-chain hash changed")
    v16z.verify_frozen_sources()

    cycles = v16i.read_csv(v16z.CYCLE_DECOMPOSITION)
    reversibility = v16i.read_csv(v16z.REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(v16z.REPRESENTATION_AUDIT)
    bridges = v16i.read_csv(v16z.BRIDGE_SUMMARY)
    trace = v16i.read_csv(v16z.BRIDGE_TRACE)
    summaries = v16i.read_csv(v16z.SOURCE_SUMMARY)
    gates = v16i.read_csv(v16z.GATE_EVALUATION)
    claims = v16i.read_csv(v16z.CLAIM_LEDGER)
    if not cycles or len(reversibility) != 6 or len(representations) != 6:
        raise ValueError("v16z formal cycle products are incomplete")
    if len(bridges) != 6 or len(summaries) != 6 or len(claims) != 5:
        raise ValueError("v16z formal bridge products are incomplete")
    if len(trace) != sum(int(row["bridge_steps"]) for row in bridges):
        raise ValueError("v16z formal bridge trace is incomplete")
    if not all(int(row["whole_cycle_reversibility_pass"]) for row in reversibility):
        raise ValueError("v16z formal whole-cycle replay failed")
    if not all(int(row["bridge_integrity_pass"]) for row in bridges):
        raise ValueError("v16z formal bridge replay failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16z_overall")
    if overall != "v16z_cycle_representation_not_qualified":
        raise ValueError("v16z formal status changed before post-run audit")
    exclusion = next(row for row in gates if row["gate"] == "effect_blind_integrity")
    if exclusion["observed"] != "spectrum=0;effect=0":
        raise ValueError("v16z formal effect exclusion failed")
    return overall


def audit_rows() -> list[Dict[str, Any]]:
    formal = {
        (int(row["growth_seed"]), int(row["run_offset"])): row
        for row in v16i.read_csv(v16z.REPRESENTATION_AUDIT)
    }
    rows: list[Dict[str, Any]] = []
    for dag, metadata in v16z.load_runs():
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        right = v16z.random_cost_start(dag, space)
        reversed_space = v16x.StateSpace(
            arm=space.arm,
            candidates=tuple(reversed(space.candidates)),
            source_edges=space.source_edges,
            slot_by_edge=space.slot_by_edge,
            parent_demands=space.parent_demands,
            slot_demands=space.slot_demands,
            edge_count=space.edge_count,
        )
        relabeled_metadata = v16w.relabel_metadata(
            metadata, v16i.stable_seed("v16z", "semantic_relabel", *dag.key)
        )
        relabeled_space = v16x.build_state_space(dag, relabeled_metadata, v16x.COARSE_ARM)
        relabeled_right = v16z.random_cost_start(dag, relabeled_space)

        original_kernel = v16y.build_kernel(space)
        reversed_kernel = v16y.build_kernel(reversed_space)
        relabeled_kernel = v16y.build_kernel(relabeled_space)
        raw_key_equality = (
            original_kernel.candidate_parents_by_slot
            == relabeled_kernel.candidate_parents_by_slot
        )
        source_moves = move_signature(original_kernel, space.source_edges)
        right_moves = move_signature(original_kernel, right)
        source_covariance = (
            source_moves
            == move_signature(reversed_kernel, space.source_edges)
            == move_signature(relabeled_kernel, relabeled_space.source_edges)
        )
        right_covariance = (
            right_moves
            == move_signature(reversed_kernel, right)
            == move_signature(relabeled_kernel, relabeled_right)
        )
        formal_row = formal[(dag.growth_seed, dag.run_offset)]
        corrected_pass = all((
            int(formal_row["exact_replay_pass"]),
            int(formal_row["candidate_order_covariance_pass"]),
            int(formal_row["candidate_set_covariance_pass"]),
            int(formal_row["start_pair_covariance_pass"]),
            int(formal_row["semantic_relabel_covariance_pass"]),
            source_covariance,
            right_covariance,
        ))
        rows.append({
            **dag.prefix,
            "formal_raw_kernel_key_equality_pass": int(raw_key_equality),
            "source_start_move_count": len(source_moves),
            "random_start_move_count": len(right_moves),
            "source_start_move_set_covariance_pass": int(source_covariance),
            "random_start_move_set_covariance_pass": int(right_covariance),
            "formal_cycle_signature_covariance_pass": formal_row["semantic_relabel_covariance_pass"],
            "corrected_edge_move_representation_pass": int(corrected_pass),
            "formal_gate_retroactively_changed": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def run() -> None:
    formal_status = verify_formal_products()
    rows = audit_rows()
    v16i.write_csv(AUDIT_CSV, rows)
    passed = sum(int(row["corrected_edge_move_representation_pass"]) for row in rows)
    raw = sum(int(row["formal_raw_kernel_key_equality_pass"]) for row in rows)
    AUDIT_MD.write_text(
        "# v16z post-run representation audit\n\n"
        f"Formal frozen status remains `{formal_status}`. This post-run audit does not rewrite the preregistered gate.\n\n"
        f"The formal raw dictionary-key comparison passed `{raw}/6`. Semantic relabeling changes `SlotClass` keys, so raw key equality is not a covariance test. The concrete valid 2x2 move sets at both frozen starts passed candidate-order and semantic-relabel covariance on `{passed}/6` sources.\n\n"
        "This diagnoses the sole formal representation failure as a comparison artifact. It supports using edge-level move-set covariance in the next proposal qualification, but it does not retroactively turn v16z into a preregistered pass. The bounded bridge result remains `0/6` exact paths with all six failures unresolved, and no spectrum or observed-effect statistic was computed.\n",
        encoding="utf-8",
    )
    print(f"[v16z-postrun] corrected edge-move covariance pass={passed}/6 raw={raw}/6")


def verify_outputs() -> None:
    formal_status = verify_formal_products()
    rows = v16i.read_csv(AUDIT_CSV)
    if len(rows) != 6:
        raise ValueError("v16z post-run audit row count failed")
    if not all(int(row["corrected_edge_move_representation_pass"]) for row in rows):
        raise ValueError("v16z corrected edge-move covariance failed")
    if any(int(row["formal_gate_retroactively_changed"]) for row in rows):
        raise ValueError("v16z formal gate was retroactively changed")
    if formal_status != "v16z_cycle_representation_not_qualified":
        raise ValueError("v16z formal status was not preserved")
    if not AUDIT_MD.exists() or not AUDIT_MD.read_text(encoding="utf-8").strip():
        raise ValueError("v16z post-run report missing")
    print("[v16z-postrun] output verification pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16z post-run representation audit")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
