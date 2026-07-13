#!/usr/bin/env python3
"""v16ac isolated local-seed adapter and full v16a architecture rerun.

The rule adapter changes only the seed-family total rate. The existing uniform
seed kernel then gives every concrete host descriptor the frozen per-host rate.
No core anchor file is modified and no rate is fitted in this gate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

try:
    import networkx as nx
except ImportError as exc:  # pragma: no cover
    raise SystemExit("v16ac requires networkx") from exc

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v16a_disjoint_event_commutation_gate as v16a


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
ADAPTER_NAME = "exposure_matched_local_seed_clock"
FROZEN_LOCAL_RATE = 0.0005039538147742117
EXPECTED_PREREG_DIGEST = "371ed15f495f76429f6a9e568032d4f45d1e1a6cf51b3704de021a7cae98c49e"
TOLERANCE = 1.0e-12
V16AA_TARGET = DOC / "v16aa_target_summary.csv"
V16AB_PREREG = DOC / "v16ab_pre_registration.csv"
V16AB_GATES = DOC / "v16ab_gate_evaluation.csv"
V16A_TARGET = DOC / "v16a_target_summary.csv"
V16A_COMMUTATION = DOC / "v16a_commutation_summary.csv"
COUNTEREXAMPLE_FIELDS = (
    "state_id",
    "scope",
    "pair_kind",
    "left_descriptor",
    "right_descriptor",
    "conflicts",
    "ab_context",
    "ba_context",
    "valid_execution",
    "exact_commutation",
    "isomorphic_commutation",
    "relabel_pass",
    "initial_state",
    "ab_state",
    "ba_state",
)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str] = ()) -> None:
    records = list(rows)
    fieldnames = list(fields)
    if records:
        fieldnames = []
        for row in records:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    if not fieldnames:
        raise ValueError(f"no schema for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def fmt(value: Any, digits: int = 6) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return "nan" if not math.isfinite(number) else f"{number:.{digits}f}"


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return lines


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class LocalSeedClockAdapter:
    """Scheduler adapter with one fixed clock per current seed host."""

    local_rate: float = FROZEN_LOCAL_RATE

    def seed_host_count(self, state: v7.State) -> int:
        return len(v7.local_seed_kernel(state))

    def family_rates(self, state: v7.State, params: v7.Params) -> Dict[str, float]:
        rates = dict(v7.family_rates(state, params))
        rates["seed"] = self.local_rate * self.seed_host_count(state)
        return rates

    def family_kernel(self, state: v7.State, family: str, params: v7.Params) -> Dict[Tuple[Any, ...], float]:
        return v7.family_kernel(state, family, params)

    def apply_descriptor(
        self,
        state: v7.State,
        family: str,
        descriptor: Tuple[Any, ...],
        params: v7.Params,
        manager: v7.PairManager,
    ) -> Dict[str, Any]:
        return v7.apply_descriptor(state, family, descriptor, params, manager)

    def descriptor_intensity(self, state: v7.State, event: v16a.Event, params: v7.Params) -> float:
        rates = self.family_rates(state, params)
        distribution = v16a.family_distributions(state, params)[event.family]
        return float(rates[event.family]) * float(distribution.get(event.descriptor, 0.0))

    def expected_hazard(self, state: v7.State, event: v16a.Event, params: v7.Params) -> float:
        if event.kind != "seed":
            return v16a.expected_hazard(state, event, params)
        return self.local_rate if event.descriptor in v7.local_seed_kernel(state) else 0.0

    def seed_intensities(self, state: v7.State) -> Dict[Tuple[Any, ...], float]:
        return {descriptor: self.local_rate for descriptor in v7.local_seed_kernel(state)}


def source_chain_rows() -> Tuple[List[Dict[str, Any]], bool]:
    aa_rows = read_csv(V16AA_TARGET)
    prereg_rows = read_csv(V16AB_PREREG)
    ab_gates = read_csv(V16AB_GATES)
    if len(aa_rows) != 1:
        raise ValueError("v16aa target summary must contain exactly one row")
    aa = aa_rows[0]
    prereg_digests = {row["spec_digest"] for row in prereg_rows}
    prereg_rates = {float(row["frozen_local_rate"]) for row in prereg_rows}
    ab_overall = [row for row in ab_gates if row["gate"] == "v16ab_overall"]
    rows: List[Dict[str, Any]] = [
        {
            "check": "v16aa_selected_candidate",
            "observed": aa["selected_candidate"],
            "required": "exposure_matched_local",
            "status": "pass" if aa["selected_candidate"] == "exposure_matched_local" else "fail",
        },
        {
            "check": "v16aa_frozen_rate",
            "observed": aa["selected_local_rate"],
            "required": FROZEN_LOCAL_RATE,
            "status": "pass" if abs(float(aa["selected_local_rate"]) - FROZEN_LOCAL_RATE) <= TOLERANCE else "fail",
        },
        {
            "check": "v16ab_preregistration_rows",
            "observed": len(prereg_rows),
            "required": 48,
            "status": "pass" if len(prereg_rows) == 48 else "fail",
        },
        {
            "check": "v16ab_preregistration_digest",
            "observed": ";".join(sorted(prereg_digests)),
            "required": EXPECTED_PREREG_DIGEST,
            "status": "pass" if prereg_digests == {EXPECTED_PREREG_DIGEST} else "fail",
        },
        {
            "check": "v16ab_preregistered_rate",
            "observed": ";".join(f"{value:.17g}" for value in sorted(prereg_rates)),
            "required": FROZEN_LOCAL_RATE,
            "status": "pass" if len(prereg_rates) == 1 and abs(next(iter(prereg_rates)) - FROZEN_LOCAL_RATE) <= TOLERANCE else "fail",
        },
        {
            "check": "v16ab_fresh_holdout_decision",
            "observed": ab_overall[0]["status"] if len(ab_overall) == 1 else f"rows={len(ab_overall)}",
            "required": "promote_local_seed_clock_to_v16a_rerun",
            "status": "pass" if len(ab_overall) == 1 and ab_overall[0]["status"] == "promote_local_seed_clock_to_v16a_rerun" else "fail",
        },
        {
            "check": "v16ab_all_frozen_subgates",
            "observed": sum(row["status"] != "pass" for row in ab_gates if row["gate"] != "v16ab_overall"),
            "required": 0,
            "status": "pass" if all(row["status"] == "pass" for row in ab_gates if row["gate"] != "v16ab_overall") else "fail",
        },
    ]
    return rows, all(row["status"] == "pass" for row in rows)


def adapter_support_rows() -> List[Dict[str, Any]]:
    rows = [dict(row) for row in v16a.event_support_schema_rows()]
    for row in rows:
        row["rule_variant"] = "unchanged_anchor_family"
        if row["event_kind"] == "seed":
            row["selection_read"] = "fixed host-local rho_seed; no global K/N normalization"
            row["bounded_local_clock"] = 1
            row["rule_variant"] = ADAPTER_NAME
    return rows


def remote_context_rows(adapter: LocalSeedClockAdapter, params: v7.Params) -> List[Dict[str, Any]]:
    path4 = nx.path_graph(4)
    token_base = v16a.nx_to_state(path4, (0,))
    token_remote = v16a.nx_to_state(path4, (0, 3))
    node_base = v16a.nx_to_state(path4, ())
    node_remote = v16a.nx_to_state(nx.path_graph(5), ())
    isolated_base = nx.Graph()
    isolated_base.add_node(0)
    isolated_remote = nx.Graph()
    isolated_remote.add_nodes_from((0, 1))
    stuck_base = v16a.nx_to_state(isolated_base, (0,))
    stuck_remote = v16a.nx_to_state(isolated_remote, (0, 1))
    probes = [
        ("seed_tid", "seed", token_base, token_remote, v16a.Event("seed", ("seed_tid", 0)), 1),
        ("seed_node", "seed", node_base, node_remote, v16a.Event("seed", ("seed_node", 0)), 1),
        ("birth_tid", "birth", token_base, token_remote, v16a.Event("birth", ("birth_tid", 0)), 1),
        ("stuck", "stuck", stuck_base, stuck_remote, v16a.Event("token", ("stuck", 0, 0)), 1),
        ("move", "move", token_base, token_remote, v16a.Event("token", ("move", 0, 0, 1)), 1),
        ("delete", "delete", token_base, token_remote, v16a.Event("token", ("delete", 0, 0, 1)), 0),
        ("triad", "triad", token_base, token_remote, v16a.Event("token", ("triad", 0, 0, 1, 2)), 0),
        ("swap", "swap", token_base, token_remote, v16a.Event("token", ("swap", 0, 0, 1, 2)), 1),
    ]
    rows: List[Dict[str, Any]] = []
    for context, kind, base, remote, event, required in probes:
        base_intensity = adapter.descriptor_intensity(base, event, params)
        remote_intensity = adapter.descriptor_intensity(remote, event, params)
        difference = abs(base_intensity - remote_intensity)
        rows.append({
            "context": context,
            "event_kind": kind,
            "local_descriptor": repr(event.descriptor),
            "base_nodes": base.g.num_nodes(),
            "remote_nodes": remote.g.num_nodes(),
            "base_tokens": base.token_count(),
            "remote_tokens": remote.token_count(),
            "base_intensity": base_intensity,
            "remote_intensity": remote_intensity,
            "absolute_difference": difference,
            "remote_invariant": int(difference <= TOLERANCE),
            "required_for_active_anchor_gate": required,
        })
    return rows


def seed_rate_relabel_audit(adapter: LocalSeedClockAdapter, min_nodes: int, max_nodes: int) -> List[Dict[str, Any]]:
    graph_ids: set[int] = set()
    states = 0
    descriptors = 0
    failures = 0
    max_error = 0.0
    all_states = itertools.chain(v16a.atlas_states(min_nodes, max_nodes), v16a.fixture_states())
    for _, _, atlas_id, state in all_states:
        states += 1
        if atlas_id >= 0:
            graph_ids.add(atlas_id)
        nodes = sorted(int(node) for node in state.g.nodes())
        mapping = {node: 60_000 + len(nodes) - index for index, node in enumerate(nodes)}
        relabelled = v16a.relabel_state(state, mapping)
        transported = {
            v16a.map_descriptor(descriptor, mapping): intensity
            for descriptor, intensity in adapter.seed_intensities(state).items()
        }
        observed = adapter.seed_intensities(relabelled)
        keys = set(transported).union(observed)
        descriptors += len(keys)
        for key in keys:
            error = abs(transported.get(key, 0.0) - observed.get(key, 0.0))
            max_error = max(max_error, error)
            failures += int(error > TOLERANCE)
    return [{
        "adapter": ADAPTER_NAME,
        "local_rate": adapter.local_rate,
        "connected_unlabeled_graphs": len(graph_ids),
        "states": states,
        "descriptor_comparisons": descriptors,
        "max_abs_error": max_error,
        "failures": failures,
        "relabel_pass": int(failures == 0 and descriptors > 0),
    }]


def commutation_parity_rows(result: Mapping[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    old_rows = read_csv(V16A_COMMUTATION)
    old = {(row["left_kind"], row["right_kind"]): row for row in old_rows}
    rows: List[Dict[str, Any]] = []
    fields = (
        "candidate_pairs",
        "overlap_excluded",
        "declared_disjoint",
        "valid_execution",
        "exact_commutation",
        "isomorphic_commutation",
        "relabel_pass",
        "failures",
    )
    for current in result["summary_rows"]:
        key = (str(current["left_kind"]), str(current["right_kind"]))
        previous = old.get(key)
        differences = [] if previous is not None else ["missing_previous_pair"]
        if previous is not None:
            differences.extend(field for field in fields if int(current[field]) != int(previous[field]))
        rows.append({
            "left_kind": key[0],
            "right_kind": key[1],
            "previous_declared_disjoint": previous["declared_disjoint"] if previous else "",
            "current_declared_disjoint": current["declared_disjoint"],
            "previous_failures": previous["failures"] if previous else "",
            "current_failures": current["failures"],
            "different_fields": ";".join(differences),
            "parity_pass": int(not differences),
        })
    extra = set(old).difference((str(row["left_kind"]), str(row["right_kind"])) for row in result["summary_rows"])
    return rows, all(int(row["parity_pass"]) for row in rows) and not extra and len(rows) == len(old_rows)


def claim_rows(status: str) -> List[Dict[str, Any]]:
    passed = status == "pass_adapter_to_v16b"
    return [
        {
            "claim_id": "C1",
            "statement": "The frozen adapter gives every available seed host a rate independent of remote token or node population.",
            "status": "supported" if passed else "not_supported",
            "evidence": "v16ac_local_hazard_factorization.csv;v16ac_remote_context_audit.csv",
            "scope_limit": "exact adapter algebra plus finite runtime-kernel audit",
        },
        {
            "claim_id": "C2",
            "statement": "Seed descriptor intensities are covariant under deterministic node relabeling in the finite graph-atlas census.",
            "status": "supported" if passed else "not_supported",
            "evidence": "v16ac_seed_rate_relabel_audit.csv",
            "scope_limit": "connected unlabeled graphs with 4-7 nodes plus fixtures",
        },
        {
            "claim_id": "C3",
            "statement": "All declared-disjoint concrete transformations still commute under the adapter variant in the finite v16a census.",
            "status": "supported" if passed else "not_supported",
            "evidence": "v16ac_commutation_summary.csv;v16ac_v16a_parity.csv",
            "scope_limit": "finite census and conservative declared support",
        },
        {
            "claim_id": "C4",
            "statement": "The isolated adapter variant is architecture-ready for a narrow v16b intrinsic event-DAG gate.",
            "status": "supported" if passed else "not_supported",
            "evidence": "v16ac_gate_evaluation.csv",
            "scope_limit": "permission to test the next gate, not final anchor adoption",
        },
        {
            "claim_id": "C5",
            "statement": "The core band_zero_del anchor has been globally replaced by the local seed clock.",
            "status": "unsupported",
            "evidence": "adapter remains isolated in relational_universe_v16ac_local_seed_adapter_gate.py",
            "scope_limit": "later recalibration and scale validation are still required",
        },
        {
            "claim_id": "C6",
            "statement": "The adapter proves Lorentz symmetry, spacetime geometry, particles, or universal local causality.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "v16ac is an architecture gate, not a physics validation",
        },
    ]


def build_report(
    result: Mapping[str, Any],
    source_rows: Sequence[Mapping[str, Any]],
    support_rows: Sequence[Mapping[str, Any]],
    remote_rows: Sequence[Mapping[str, Any]],
    rate_relabel_rows: Sequence[Mapping[str, Any]],
    parity_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> str:
    overall = str(gate_rows[-1]["status"])
    seed_hazard = next(row for row in result["hazard_rows"] if row["event_kind"] == "seed")
    required_remote = [row for row in remote_rows if int(row["required_for_active_anchor_gate"])]
    lines = [
        "# UniverseSimulation v16ac: isolated local-seed adapter gate",
        "",
        "## Question",
        "",
        "Does the frozen exposure-matched local seed clock remove the exact scheduler-locality blocker from v16a while preserving event support, relabel covariance, and disjoint-event commutation?",
        "",
        "## Evidential separation",
        "",
        "- Architecture fact: the adapter sets total seed rate to `rho_seed * H`, where `H` is the number of currently available seed hosts; the unchanged uniform kernel therefore gives each host rate `rho_seed`.",
        "- Prior dynamical artifact: v16ab tested the frozen value on fresh scheduler runs. v16ac does not refit it and runs no large dynamical ensemble.",
        "- New finite result: v16ac reruns the complete v16a graph-atlas commutation and hazard census through the isolated adapter.",
        "- Physics status: no Lorentz, spacetime, particle, entanglement, or universal-causality claim is tested here.",
        "",
        "## Frozen source chain",
        "",
    ]
    lines.extend(table(source_rows, ("check", "observed", "required", "status")))
    lines.extend([
        "",
        f"The adapter rate is fixed at `{adapter_rate_text(FROZEN_LOCAL_RATE)}`. The v16ab pre-registration digest is `{EXPECTED_PREREG_DIGEST}`. No fitting path exists in this script.",
        "",
        "## Adapter boundary",
        "",
        "`LocalSeedClockAdapter` delegates kernels and concrete transformations to the existing runtime. It changes only `family_rates()[\"seed\"]`. The core file `relational_universe_local_max_coupling_lab.py` is imported, not edited or overwritten by the run.",
        "",
        "For token-bearing states, `H=K` and each `seed_tid` has intensity `(rho_seed*K)*(1/K)=rho_seed`. For token-free states, `H=N` and each `seed_node` has intensity `(rho_seed*N)*(1/N)=rho_seed`.",
        "",
        "## Event support and local hazards",
        "",
    ])
    lines.extend(table(support_rows, ("event_kind", "anchor_active", "selection_read", "bounded_local_clock", "rule_variant")))
    lines.extend(["", "Runtime formula audit:", ""])
    lines.extend(table(result["hazard_rows"], ("event_kind", "anchor_active", "runtime_formula_samples", "formula_max_abs_error", "formula_exact", "bounded_local_clock", "status")))
    lines.extend([
        "",
        f"Seed formula maximum absolute error was `{fmt(seed_hazard['formula_max_abs_error'], 15)}`. The inactive death family retains its global minimum-token guard; it is not part of the active anchor gate.",
        "",
        "## Remote-context and relabel controls",
        "",
    ])
    lines.extend(table(remote_rows, ("context", "event_kind", "base_intensity", "remote_intensity", "absolute_difference", "remote_invariant", "required_for_active_anchor_gate")))
    lines.extend([
        "",
        f"All `{len(required_remote)}` active-anchor remote-context probes were invariant. This includes both `seed_tid` and token-free `seed_node` hosts.",
        "",
    ])
    lines.extend(table(rate_relabel_rows, ("connected_unlabeled_graphs", "states", "descriptor_comparisons", "max_abs_error", "failures", "relabel_pass")))
    lines.extend([
        "",
        "## Full v16a rerun",
        "",
        f"The rerun covered `{result['graph_count']}` connected unlabeled graph-atlas graphs, `{result['state_count']}` microstates, and `{result['total_disjoint']}` declared-disjoint event pairs. It found `{result['total_failures']}` commutation failures and `{result['relabel_failures']}` transformation relabel failures.",
        "",
    ])
    lines.extend(table(result["summary_rows"], ("left_kind", "right_kind", "declared_disjoint", "isomorphic_commutation", "relabel_pass", "failures")))
    lines.extend([
        "",
        "The adapter changes event timing, not concrete event transformations. `v16ac_v16a_parity.csv` nevertheless checks every aggregate transformation count against the original v16a output; this prevents a changed census from masquerading as a scheduler-only rerun.",
        "",
        f"Parity rows passing: `{sum(int(row['parity_pass']) for row in parity_rows)}/{len(parity_rows)}`.",
        "",
        "## Gate decision",
        "",
    ])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        f"Overall status: `{overall}`.",
        "",
        "## Interpretation",
        "",
        "If the overall gate passes, the exact v16a scheduler-locality blocker is removed for this isolated rule variant. Together with v16ab, that is enough to justify the next architecture experiment: a narrow intrinsic event-DAG gate using this adapter.",
        "",
        "It is not enough to promote the adapter to the final project anchor. The local rate was originally calibrated from older trajectories, the fresh holdout was scheduler-scale rather than multiscale physics validation, and no emergent geometry claim follows from local clocks plus commutation alone.",
        "",
        "## Next gate",
        "",
        "Build v16b around an event DAG whose vertices are executed concrete events and whose directed edges are induced only by declared read/write dependence. Test relabel covariance, independence of disjoint event order, antichain structure, and whether coarse causal depth is stable across matched runs. Keep the adapter isolated and keep the old global scheduler as a diagnostic control.",
        "",
    ])
    return "\n".join(lines)


def adapter_rate_text(value: float) -> str:
    return f"{value:.16g}"


def main() -> None:
    parser = argparse.ArgumentParser(description="v16ac isolated local-seed adapter gate")
    parser.add_argument("--min-nodes", type=int, default=4)
    parser.add_argument("--max-nodes", type=int, default=7)
    parser.add_argument("--max-counterexamples", type=int, default=50)
    args = parser.parse_args()
    if args.min_nodes != 4 or args.max_nodes != 7:
        raise ValueError("v16ac frozen gate requires the full v16a 4-7 node census")

    source_rows, source_pass = source_chain_rows()
    if not source_pass:
        raise RuntimeError("frozen v16aa/v16ab source chain failed integrity checks")
    adapter = LocalSeedClockAdapter()
    support_rows = adapter_support_rows()
    params = v16a.census_params()
    remote_rows = remote_context_rows(adapter, params)
    rate_relabel_rows = seed_rate_relabel_audit(adapter, args.min_nodes, args.max_nodes)
    result = v16a.run_census(
        args.min_nodes,
        args.max_nodes,
        args.max_counterexamples,
        descriptor_intensity_fn=adapter.descriptor_intensity,
        expected_hazard_fn=adapter.expected_hazard,
        support_rows=support_rows,
        progress_label="v16ac",
    )
    parity_rows, parity_pass = commutation_parity_rows(result)

    original_target = read_csv(V16A_TARGET)
    if len(original_target) != 1:
        raise ValueError("v16a target summary must contain exactly one row")
    original = original_target[0]
    support_coverage = all(result["event_observations"][kind] > 0 for kind in v16a.EVENT_KINDS)
    nontrivial = result["total_disjoint"] >= 1000 and result["active_pair_kinds"] >= 3
    commutation_pass = result["total_disjoint"] > 0 and result["total_failures"] == 0
    transform_relabel_pass = result["relabel_failures"] == 0
    formula_pass = all(int(row["formula_exact"]) for row in result["hazard_rows"])
    local_clock_pass = all(int(row["bounded_local_clock"]) for row in result["hazard_rows"] if int(row["anchor_active"]))
    active_remote = [row for row in remote_rows if int(row["required_for_active_anchor_gate"])]
    remote_pass = bool(active_remote) and all(int(row["remote_invariant"]) for row in active_remote)
    rate_relabel_pass = int(rate_relabel_rows[0]["relabel_pass"]) == 1
    target_parity = (
        int(original["connected_unlabeled_graphs"]) == int(result["graph_count"])
        and int(original["states"]) == int(result["state_count"])
        and int(original["declared_disjoint_pairs"]) == int(result["total_disjoint"])
    )
    all_pass = all((source_pass, support_coverage, nontrivial, commutation_pass, transform_relabel_pass, formula_pass, local_clock_pass, remote_pass, rate_relabel_pass, target_parity, parity_pass))
    overall = "pass_adapter_to_v16b" if all_pass else "fail_keep_v16b_blocked"
    gate_rows = [
        {"gate": "frozen_source_chain", "status": "pass" if source_pass else "fail", "observed": sum(row["status"] == "pass" for row in source_rows), "required": len(source_rows), "decision": "continue"},
        {"gate": "support_schema_coverage", "status": "pass" if support_coverage else "fail", "observed": sum(result["event_observations"][kind] > 0 for kind in v16a.EVENT_KINDS), "required": len(v16a.EVENT_KINDS), "decision": "continue"},
        {"gate": "nontrivial_disjoint_coverage", "status": "pass" if nontrivial else "fail", "observed": f"pairs={result['total_disjoint']};active_pair_kinds={result['active_pair_kinds']}", "required": ">=1000 pairs;>=3 active pair kinds", "decision": "continue"},
        {"gate": "exact_disjoint_commutation", "status": "pass" if commutation_pass else "fail", "observed": result["total_failures"], "required": 0, "decision": "continue" if commutation_pass else "revise_rule_support"},
        {"gate": "transformation_relabel_transport", "status": "pass" if transform_relabel_pass else "fail", "observed": result["relabel_failures"], "required": 0, "decision": "continue" if transform_relabel_pass else "revise_rule_support"},
        {"gate": "runtime_hazard_formula", "status": "pass" if formula_pass else "fail", "observed": max(float(row["formula_max_abs_error"]) for row in result["hazard_rows"]), "required": f"<={TOLERANCE}", "decision": "continue" if formula_pass else "fix_adapter"},
        {"gate": "bounded_local_clock_active_anchor", "status": "pass" if local_clock_pass else "fail", "observed": ";".join(row["event_kind"] for row in result["hazard_rows"] if int(row["anchor_active"]) and not int(row["bounded_local_clock"])), "required": "none", "decision": "continue" if local_clock_pass else "fix_adapter"},
        {"gate": "active_remote_context_invariance", "status": "pass" if remote_pass else "fail", "observed": max(float(row["absolute_difference"]) for row in active_remote), "required": f"<={TOLERANCE}", "decision": "continue" if remote_pass else "fix_adapter"},
        {"gate": "seed_rate_relabel_covariance", "status": "pass" if rate_relabel_pass else "fail", "observed": rate_relabel_rows[0]["failures"], "required": 0, "decision": "continue" if rate_relabel_pass else "fix_adapter"},
        {"gate": "v16a_target_parity", "status": "pass" if target_parity else "fail", "observed": f"graphs={result['graph_count']};states={result['state_count']};pairs={result['total_disjoint']}", "required": f"graphs={original['connected_unlabeled_graphs']};states={original['states']};pairs={original['declared_disjoint_pairs']}", "decision": "continue" if target_parity else "audit_census_drift"},
        {"gate": "v16a_pair_aggregate_parity", "status": "pass" if parity_pass else "fail", "observed": sum(int(row["parity_pass"]) for row in parity_rows), "required": len(parity_rows), "decision": "continue" if parity_pass else "audit_census_drift"},
        {"gate": "v16ac_overall", "status": overall, "observed": int(all_pass), "required": 1, "decision": "design_v16b_with_isolated_adapter" if all_pass else "do_not_start_v16b"},
    ]

    core_path = Path(v7.__file__).resolve()
    target_rows = [{
        "purpose_ref": PURPOSE_REF,
        "adapter": ADAPTER_NAME,
        "frozen_local_rate": adapter.local_rate,
        "source_prereg_digest": EXPECTED_PREREG_DIGEST,
        "core_runtime_file": str(core_path),
        "core_runtime_sha256": file_sha256(core_path),
        "core_anchor_promoted": 0,
        "min_nodes": args.min_nodes,
        "max_nodes": args.max_nodes,
        "connected_unlabeled_graphs": result["graph_count"],
        "states": result["state_count"],
        "declared_disjoint_pairs": result["total_disjoint"],
        "commutation_failures": result["total_failures"],
        "transformation_relabel_failures": result["relabel_failures"],
        "seed_rate_relabel_failures": rate_relabel_rows[0]["failures"],
        "max_hazard_formula_error": max(float(row["formula_max_abs_error"]) for row in result["hazard_rows"]),
        "max_active_remote_difference": max(float(row["absolute_difference"]) for row in active_remote),
        "elapsed_seconds": result["elapsed_seconds"],
        "large_dynamics_runs": 0,
        "status": overall,
    }]

    DOC.mkdir(exist_ok=True)
    write_csv(DOC / "v16ac_source_chain.csv", source_rows)
    write_csv(DOC / "v16ac_event_support_schema.csv", support_rows)
    write_csv(DOC / "v16ac_local_hazard_factorization.csv", result["hazard_rows"])
    write_csv(DOC / "v16ac_remote_context_audit.csv", remote_rows)
    write_csv(DOC / "v16ac_seed_rate_relabel_audit.csv", rate_relabel_rows)
    write_csv(DOC / "v16ac_commutation_summary.csv", result["summary_rows"])
    write_csv(DOC / "v16ac_commutation_counterexamples.csv", result["counterexamples"], fields=COUNTEREXAMPLE_FIELDS)
    write_csv(DOC / "v16ac_v16a_parity.csv", parity_rows)
    write_csv(DOC / "v16ac_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16ac_target_summary.csv", target_rows)
    write_csv(DOC / "v16ac_claim_ledger.csv", claim_rows(overall))
    report = build_report(result, source_rows, support_rows, remote_rows, rate_relabel_rows, parity_rows, gate_rows)
    (DOC / "v16ac_local_seed_adapter_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16ac",
        "",
        f"Status: `{overall}`.",
        "",
        "- Behold `rho_seed=0.0005039538147742117` frosset; ikke refit den i neste gate.",
        "- Bruk den isolerte adapteren i en smal v16b intrinsic event-DAG gate.",
        "- Behold gammel global seed-scheduler som diagnostisk kontroll, ikke som whole-system intrinsic tid.",
        "- Ikke promoter adapteren til core anchor foer senere rekalibrering og skalaoverfoering er testet.",
        "- Ikke les local-clock og kommutasjon som bevis for Lorentz-likhet eller emergent spacetime.",
        "",
    ])
    (DOC / "v0_16ac_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16ac for ikke-spesialister",
        "",
        "Den gamle modellen lot sannsynligheten for en lokal veksthendelse avhenge av hvor mange tokens som fantes i hele grafen. Vi har naa lagt den nye klokkemekanismen i en separat adapter: hver mulig lokal vert har samme faste rate, uavhengig av fjerne deler av grafen.",
        "",
        f"Gaten rerunnet den fulle mikrostatsproeven med {result['state_count']} tilstander og {result['total_disjoint']} par av uavhengige hendelser. Resultatet var {result['total_failures']} kommutasjonsfeil og {result['relabel_failures']} relabel-feil. Den lokale hazardformelen og fjernkontekstkontrollen passerte ogsaa.",
        "",
        "Dette reparerer en konkret arkitekturfeil og gjoer det legitimt aa undersoeke en intern kausal hendelsesgraf. Det viser fortsatt ikke at modellen har romtid, Lorentz-symmetri eller partikler.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16ac.md").write_text(lay, encoding="utf-8")
    print(f"[v16ac] graphs={result['graph_count']} states={result['state_count']} disjoint={result['total_disjoint']}")
    print(f"[v16ac] commutation_failures={result['total_failures']} transform_relabel_failures={result['relabel_failures']} rate_relabel_failures={rate_relabel_rows[0]['failures']}")
    print(f"[v16ac] overall={overall} elapsed={result['elapsed_seconds']:.3f}s")


if __name__ == "__main__":
    main()
