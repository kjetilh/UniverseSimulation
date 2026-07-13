#!/usr/bin/env python3
"""v16aa seed-clock architecture gate after the v16a locality failure.

No new dynamics are run here. Existing v15dx event timelines are used to
reconstruct continuous-time token exposure. Candidate seed clocks are then
checked for exact locality, relabel covariance, and first-order rate shock.
Any fitted local rate remains a candidate for a fresh holdout, not validation.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

try:
    import networkx as nx
except ImportError as exc:  # pragma: no cover
    raise SystemExit("v16aa requires networkx") from exc

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
V15DX_EVENTS = DOC / "v15dx_event_log.csv"
V15DY_RUNS = DOC / "v15dy_run_summary.csv"
ANCHOR = "band_zero_del"
TOLERANCE = 1.0e-12
AGGREGATE_RATIO_RANGE = (0.90, 1.10)
PER_RUN_RATIO_RANGE = (0.75, 1.25)

RunKey = Tuple[int, int, int, str]


@dataclass(frozen=True)
class Candidate:
    name: str
    mode: str
    global_rate: float
    local_rate: float
    calibration: str
    retains_node_growth: int
    whole_system_intrinsic_eligible: int


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    records = list(rows)
    if not records:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: List[str] = []
    for row in records:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
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


def initial_tokens_by_growth_seed() -> Dict[int, int]:
    values: Dict[int, set[int]] = defaultdict(set)
    for row in read_csv(V15DY_RUNS):
        values[int(row["growth_seed"])].add(int(row["initial_tokens"]))
    out: Dict[int, int] = {}
    for seed, observed in values.items():
        if len(observed) != 1:
            raise ValueError(f"non-unique initial token count for growth_seed={seed}: {sorted(observed)}")
        out[seed] = next(iter(observed))
    return out


def reconstruct_trajectories() -> List[Dict[str, Any]]:
    initial_tokens = initial_tokens_by_growth_seed()
    grouped: Dict[RunKey, List[Dict[str, str]]] = defaultdict(list)
    for row in read_csv(V15DX_EVENTS):
        if row["regime"] != ANCHOR:
            continue
        key = (int(row["growth_seed"]), int(row["placement"]), int(row["seed_delta"]), row["branch"])
        grouped[key].append(row)
    rows: List[Dict[str, Any]] = []
    for key, events in sorted(grouped.items()):
        growth_seed, placement, seed_delta, branch = key
        if growth_seed not in initial_tokens:
            raise ValueError(f"missing initial token count for growth_seed={growth_seed}")
        events.sort(key=lambda row: int(row["step"]))
        token_count = initial_tokens[growth_seed]
        total_time = 0.0
        token_time = 0.0
        observed_seed_count = 0
        observed_birth_count = 0
        for event in events:
            dt = float(event["dt"])
            total_time += dt
            token_time += token_count * dt
            kind = event["event_type"]
            observed_seed_count += int(kind == "seed")
            observed_birth_count += int(kind == "birth")
            if kind == "birth":
                token_count += 1
            elif kind == "death":
                token_count -= 1
        rows.append({
            "growth_seed": growth_seed,
            "placement": placement,
            "seed_delta": seed_delta,
            "branch": branch,
            "n_events": len(events),
            "initial_tokens": initial_tokens[growth_seed],
            "final_tokens_reconstructed": token_count,
            "total_time": total_time,
            "token_time_integral": token_time,
            "time_weighted_mean_tokens": token_time / total_time,
            "observed_seed_count": observed_seed_count,
            "observed_birth_count": observed_birth_count,
        })
    return rows


def build_candidates(trajectories: Sequence[Mapping[str, Any]], r_seed: float) -> Tuple[List[Candidate], float, float]:
    total_time = sum(float(row["total_time"]) for row in trajectories)
    token_time = sum(float(row["token_time_integral"]) for row in trajectories)
    effective_tokens = token_time / total_time
    initial_reference = statistics.median(float(row["initial_tokens"]) for row in trajectories)
    return [
        Candidate("current_global", "global", r_seed, 0.0, "current_anchor", 1, 0),
        Candidate("naive_local_per_token", "local", 0.0, r_seed, "reuse_global_rate_as_per_token_rate", 1, 1),
        Candidate("initial_median_local", "local", 0.0, r_seed / initial_reference, f"fixed_initial_Kref={initial_reference:g}", 1, 1),
        Candidate("exposure_matched_local", "local", 0.0, r_seed / effective_tokens, f"fit_v15dx_time_weighted_K={effective_tokens:.12g}", 1, 1),
        Candidate("preparation_only", "frozen", 0.0, 0.0, "r_seed_zero_during_observation", 0, 1),
        Candidate("explicit_global_background", "global", r_seed, 0.0, "current_anchor_but_excluded_from_intrinsic_event_system", 1, 0),
    ], effective_tokens, initial_reference


def expected_seed_exposure(candidate: Candidate, trajectory: Mapping[str, Any]) -> float:
    if candidate.mode == "global":
        return candidate.global_rate * float(trajectory["total_time"])
    if candidate.mode == "local":
        return candidate.local_rate * float(trajectory["token_time_integral"])
    return 0.0


def trajectory_exposure_rows(
    trajectories: Sequence[Mapping[str, Any]],
    candidates: Sequence[Candidate],
    r_seed: float,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for trajectory in trajectories:
        baseline = r_seed * float(trajectory["total_time"])
        for candidate in candidates:
            expected = expected_seed_exposure(candidate, trajectory)
            rows.append({
                **dict(trajectory),
                "candidate": candidate.name,
                "mode": candidate.mode,
                "local_rate_per_host": candidate.local_rate,
                "expected_seed_exposure": expected,
                "baseline_expected_seed_exposure": baseline,
                "exposure_ratio_vs_current": expected / baseline if baseline else float("nan"),
            })
    return rows


def nx_to_state(graph: nx.Graph, token_nodes: Sequence[int]) -> v7.State:
    out = v7.UGraph()
    for node in graph.nodes():
        out.add_node(int(node))
    for left, right in graph.edges():
        out.add_edge(int(left), int(right))
    return v7.State(out, {tid: int(node) for tid, node in enumerate(token_nodes)}, 0.0)


def seed_intensities(state: v7.State, candidate: Candidate) -> Dict[Tuple[Any, ...], float]:
    kernel = v7.local_seed_kernel(state)
    if candidate.mode == "global":
        return {descriptor: candidate.global_rate * probability for descriptor, probability in kernel.items()}
    if candidate.mode == "local":
        return {descriptor: candidate.local_rate for descriptor in kernel}
    return {descriptor: 0.0 for descriptor in kernel}


def remote_context_rows(candidates: Sequence[Candidate]) -> List[Dict[str, Any]]:
    token_base = nx_to_state(nx.path_graph(4), (0,))
    token_remote = nx_to_state(nx.path_graph(4), (0, 3))
    node_base = nx_to_state(nx.path_graph(4), ())
    node_remote = nx_to_state(nx.path_graph(5), ())
    contexts = (
        ("token_host", token_base, token_remote, ("seed_tid", 0)),
        ("node_host_no_tokens", node_base, node_remote, ("seed_node", 0)),
    )
    rows: List[Dict[str, Any]] = []
    for candidate in candidates:
        for context, base, remote, descriptor in contexts:
            base_intensity = seed_intensities(base, candidate).get(descriptor, 0.0)
            remote_intensity = seed_intensities(remote, candidate).get(descriptor, 0.0)
            difference = abs(base_intensity - remote_intensity)
            rows.append({
                "candidate": candidate.name,
                "context": context,
                "descriptor": repr(descriptor),
                "base_intensity": base_intensity,
                "remote_intensity": remote_intensity,
                "absolute_difference": difference,
                "remote_invariant": int(difference <= TOLERANCE),
                "bounded_local": int(candidate.mode in {"local", "frozen"}),
            })
    return rows


def relabel_state(state: v7.State, mapping: Mapping[int, int]) -> v7.State:
    graph = v7.UGraph()
    for node in state.g.nodes():
        graph.add_node(mapping[int(node)])
    for left, right in state.g.edge_set():
        graph.add_edge(mapping[int(left)], mapping[int(right)])
    return v7.State(graph, {int(tid): mapping[int(node)] for tid, node in state.token_pos.items()}, 0.0)


def map_seed_descriptor(descriptor: Tuple[Any, ...], mapping: Mapping[int, int]) -> Tuple[Any, ...]:
    if descriptor[0] == "seed_node":
        return descriptor[0], mapping[int(descriptor[1])]
    return descriptor


def relabel_audit_rows(candidates: Sequence[Candidate]) -> Tuple[List[Dict[str, Any]], int]:
    stats: Dict[str, Dict[str, float]] = defaultdict(lambda: {"trials": 0.0, "max_error": 0.0, "failures": 0.0})
    graph_count = 0
    for graph in nx.graph_atlas_g():
        if not (4 <= graph.number_of_nodes() <= 7) or not nx.is_connected(graph):
            continue
        graph_count += 1
        nodes = sorted(int(node) for node in graph.nodes())
        mapping = dict(zip(nodes, reversed([50_000 + index for index in range(len(nodes))])))
        for state in (nx_to_state(graph, (nodes[0],)), nx_to_state(graph, ())):
            transported_state = relabel_state(state, mapping)
            for candidate in candidates:
                original = seed_intensities(state, candidate)
                transported = {map_seed_descriptor(descriptor, mapping): value for descriptor, value in original.items()}
                relabelled = seed_intensities(transported_state, candidate)
                keys = set(transported).union(relabelled)
                error = max((abs(transported.get(key, 0.0) - relabelled.get(key, 0.0)) for key in keys), default=0.0)
                stats[candidate.name]["trials"] += 1.0
                stats[candidate.name]["max_error"] = max(stats[candidate.name]["max_error"], error)
                stats[candidate.name]["failures"] += float(error > TOLERANCE)
    rows = [{
        "candidate": candidate.name,
        "graph_count": graph_count,
        "trials": int(stats[candidate.name]["trials"]),
        "max_abs_error": stats[candidate.name]["max_error"],
        "failures": int(stats[candidate.name]["failures"]),
        "relabel_pass": int(stats[candidate.name]["failures"] == 0),
    } for candidate in candidates]
    return rows, graph_count


def candidate_rows(
    candidates: Sequence[Candidate],
    exposure_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    relabel_lookup = {str(row["candidate"]): row for row in relabel_rows}
    baseline_total = sum(float(row["baseline_expected_seed_exposure"]) for row in exposure_rows if row["candidate"] == candidates[0].name)
    rows: List[Dict[str, Any]] = []
    for candidate in candidates:
        subset = [row for row in exposure_rows if row["candidate"] == candidate.name]
        expected_total = sum(float(row["expected_seed_exposure"]) for row in subset)
        ratios = [float(row["exposure_ratio_vs_current"]) for row in subset]
        bounded = int(candidate.mode in {"local", "frozen"})
        aggregate_ratio = expected_total / baseline_total
        ratio_pass = (
            AGGREGATE_RATIO_RANGE[0] <= aggregate_ratio <= AGGREGATE_RATIO_RANGE[1]
            and min(ratios) >= PER_RUN_RATIO_RANGE[0]
            and max(ratios) <= PER_RUN_RATIO_RANGE[1]
        )
        relabel_pass = int(relabel_lookup[candidate.name]["relabel_pass"])
        selection_pass = int(bounded and candidate.retains_node_growth and candidate.whole_system_intrinsic_eligible and relabel_pass and ratio_pass)
        rows.append({
            "candidate": candidate.name,
            "mode": candidate.mode,
            "global_rate": candidate.global_rate,
            "local_rate_per_host": candidate.local_rate,
            "calibration": candidate.calibration,
            "bounded_local": bounded,
            "hidden_global_population_dependency": int(candidate.mode == "global"),
            "retains_node_growth": candidate.retains_node_growth,
            "whole_system_intrinsic_eligible": candidate.whole_system_intrinsic_eligible,
            "relabel_pass": relabel_pass,
            "expected_seed_exposure_total": expected_total,
            "aggregate_ratio_vs_current": aggregate_ratio,
            "min_run_ratio_vs_current": min(ratios),
            "median_run_ratio_vs_current": statistics.median(ratios),
            "max_run_ratio_vs_current": max(ratios),
            "rate_shock_control_pass": int(ratio_pass),
            "selection_pass": selection_pass,
            "evidence_status": "fit_candidate_requires_fresh_holdout" if selection_pass else "architecture_control_or_rejected_candidate",
        })
    return rows


def claim_rows(selected: str, observed_seeds: int, baseline_expected: float) -> List[Dict[str, Any]]:
    return [
        {"claim_id": "C1", "statement": "The v15dx timelines permit exact reconstruction of continuous-time token exposure.", "status": "supported", "evidence": "v16aa_trajectory_exposure.csv", "scope_limit": "anchor runs only; initial K imported from matching v15dy bases"},
        {"claim_id": "C2", "statement": "A fixed per-host seed rate removes the remote population dependency and preserves relabel covariance.", "status": "supported", "evidence": "v16aa_remote_context_audit.csv;v16aa_relabel_audit.csv", "scope_limit": "seed scheduler architecture, not full dynamics"},
        {"claim_id": "C3", "statement": f"{selected} is dynamically validated.", "status": "unsupported", "evidence": "candidate fitted on v15dx exposure", "scope_limit": "requires fresh holdout"},
        {"claim_id": "C4", "statement": "The current observed seed count is compatible with the reconstructed global-clock exposure.", "status": "descriptive_support", "evidence": f"observed={observed_seeds};baseline_expected={baseline_expected:.12g}", "scope_limit": "not a formal Poisson goodness-of-fit test"},
        {"claim_id": "C5", "statement": "v16b intrinsic event-DAG work may begin now.", "status": "unsupported", "evidence": "v16aa selects only a fitted candidate", "scope_limit": "fresh scheduler holdout and v16a locality rerun required first"},
    ]


def build_report(
    trajectories: Sequence[Mapping[str, Any]],
    candidate_comparison: Sequence[Mapping[str, Any]],
    remote_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    effective_tokens: float,
    initial_reference: float,
    selected: Mapping[str, Any],
    observed_seeds: int,
    baseline_expected: float,
) -> str:
    lines = [
        "# UniverseSimulation v16aa: seed-clock architecture gate",
        "",
        "Dato: 2026-07-12",
        "",
        "## Konklusjon",
        "",
        f"Gaten velger `{selected['candidate']}` med fast lokal per-host-rate `{fmt(selected['local_rate_per_host'], 12)}` som kandidat for en fresh dynamisk holdout.",
        "",
        "Dette er ikke en ny anchor og ikke dynamisk validering. Raten er fittet til eksisterende v15dx token-time exposure for aa bevare seed-budsjettet i foerste orden. Kandidaten maa fryses og testes paa fresh growth seeds foer den kan erstatte dagens globale klokke.",
        "",
        "## Rekonstruksjon",
        "",
        f"- Anchor-runs: `{len(trajectories)}`.",
        f"- Observerte events: `{sum(int(row['n_events']) for row in trajectories)}`.",
        f"- Observerte seed-events: `{observed_seeds}`.",
        f"- Rekonstruert total kontinuerlig tid: `{fmt(sum(float(row['total_time']) for row in trajectories))}`.",
        f"- Rekonstruert token-time integral: `{fmt(sum(float(row['token_time_integral']) for row in trajectories))}`.",
        f"- Time-weighted effektivt tokenantall: `{fmt(effective_tokens)}`.",
        f"- Median initial K: `{fmt(initial_reference)}`.",
        f"- Forventet global-clock seed exposure: `{fmt(baseline_expected)}` mot `{observed_seeds}` observerte seeds.",
        "",
        "Tokenantallet rekonstrueres foer hvert logget `dt`; birth oeker K etter intervallet og death reduserer K. Dermed kan en kontrafaktisk fast lokal hazard beregnes som `rho_seed * integral K(t) dt` uten aa finne paa nye dynamiske resultater.",
        "",
        "## Kandidater",
        "",
    ]
    lines.extend(table(candidate_comparison, ("candidate", "local_rate_per_host", "bounded_local", "retains_node_growth", "aggregate_ratio_vs_current", "min_run_ratio_vs_current", "max_run_ratio_vs_current", "selection_pass", "evidence_status")))
    lines.extend([
        "",
        "Den naive lokale kandidaten gjenbruker `0.04` som rate per token og gir derfor en omtrent K-ganger stoerre seed-exposure. Initial-K-kalibreringen undervurderer at K vokser kraftig under runnet. Exposure-matching bruker i stedet en fast rate bestemt av time-weighted K; den er lokal etter fit fordi raten ikke leser K under dynamikken.",
        "",
        "`preparation_only` er en viktig kontroll, men kan ikke vaere hovedkandidat dersom fysisk nodevekst skal beholdes. `explicit_global_background` er koherent bare for en betinget lokal subdynamikk; den gir ikke whole-system intrinsic causality.",
        "",
        "## Remote-context gate",
        "",
    ])
    lines.extend(table(remote_rows, ("candidate", "context", "base_intensity", "remote_intensity", "absolute_difference", "remote_invariant", "bounded_local")))
    lines.extend(["", "## Relabel gate", ""])
    lines.extend(table(relabel_rows, ("candidate", "graph_count", "trials", "max_abs_error", "failures", "relabel_pass")))
    lines.extend(["", "## Gate-evaluering", ""])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Evidensstatus",
        "",
        "- Lokaliteten og relabel-egenskapen til en fast per-host-rate er eksakte arkitekturfakta.",
        "- Ratevalget er fittet paa v15dx og har ingen fresh evidens.",
        "- Exposure-ratio er en foersteordens kontrafaktisk beregning paa eksisterende trajectories; den inkluderer ikke feedback fra ekstra seed-noder til senere birth/move/swap-hazards.",
        "- Resultatet sier ingenting direkte om Lorentz-likhet, spacetime eller universell geometri.",
        "",
        "## Neste gate",
        "",
        "Kjoer en fresh, matched scheduler-holdout paa growth seeds som ikke inngikk i fittet:",
        "",
        "- current_global som baseline",
        "- preparation_only som mekanismekontroll",
        f"- `{selected['candidate']}` med frosset `rho_seed={fmt(selected['local_rate_per_host'], 12)}`",
        "- separate RNG/ID-allokatorer og samme eventbudsjett",
        "- primaert seed-exposure, nodevekst, tokenvekst, total tid og family-rate shock",
        "- ingen refit etter fresh resultater",
        "",
        "Bare dersom den lokale kandidaten unngaar katastrofal vekst og holder seed-/family-budsjettet innen frosne toleranser, rerunnes v16a-locality-gaten og v16b event-DAG kan vurderes.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="v16aa seed-clock architecture gate")
    parser.add_argument("--r-seed", type=float, default=0.04)
    args = parser.parse_args()
    trajectories = reconstruct_trajectories()
    candidates, effective_tokens, initial_reference = build_candidates(trajectories, args.r_seed)
    exposure_rows = trajectory_exposure_rows(trajectories, candidates, args.r_seed)
    remote_rows = remote_context_rows(candidates)
    relabel_rows, graph_count = relabel_audit_rows(candidates)
    comparison = candidate_rows(candidates, exposure_rows, relabel_rows)
    selected_rows = [row for row in comparison if int(row["selection_pass"])]
    if len(selected_rows) != 1:
        raise RuntimeError(f"expected exactly one selected candidate, got {[row['candidate'] for row in selected_rows]}")
    selected = selected_rows[0]

    observed_seeds = sum(int(row["observed_seed_count"]) for row in trajectories)
    total_time = sum(float(row["total_time"]) for row in trajectories)
    token_time = sum(float(row["token_time_integral"]) for row in trajectories)
    baseline_expected = args.r_seed * total_time
    reconstruction_ratio = observed_seeds / baseline_expected
    selected_remote = [row for row in remote_rows if row["candidate"] == selected["candidate"]]
    selected_relabel = next(row for row in relabel_rows if row["candidate"] == selected["candidate"])
    gate_rows = [
        {"gate": "input_integrity", "status": "pass" if len(trajectories) == 24 and sum(int(row["n_events"]) for row in trajectories) == 81936 else "fail", "observed": f"runs={len(trajectories)};events={sum(int(row['n_events']) for row in trajectories)}", "required": "runs=24;events=81936", "decision": "continue"},
        {"gate": "global_clock_reconstruction", "status": "pass" if 0.5 <= reconstruction_ratio <= 1.5 else "fail", "observed": reconstruction_ratio, "required": "observed/expected in [0.5,1.5]", "decision": "continue"},
        {"gate": "selected_remote_invariance", "status": "pass" if all(int(row["remote_invariant"]) for row in selected_remote) else "fail", "observed": max(float(row["absolute_difference"]) for row in selected_remote), "required": f"<={TOLERANCE}", "decision": "continue"},
        {"gate": "selected_relabel_covariance", "status": "pass" if int(selected_relabel["relabel_pass"]) else "fail", "observed": selected_relabel["max_abs_error"], "required": f"<={TOLERANCE}", "decision": "continue"},
        {"gate": "unique_architecture_candidate", "status": "pass", "observed": selected["candidate"], "required": "exactly one", "decision": "freeze_for_fresh_holdout"},
        {"gate": "fresh_validation", "status": "not_run", "observed": "none", "required": "fresh growth seeds; no refit", "decision": "do_not_start_v16b"},
        {"gate": "v16aa_overall", "status": "candidate_selected_not_validated", "observed": selected["candidate"], "required": "fresh holdout before architecture adoption", "decision": "run_fresh_seed_clock_holdout"},
    ]

    target_rows = [{
        "purpose_ref": PURPOSE_REF,
        "source_event_file": str(V15DX_EVENTS),
        "source_initial_token_file": str(V15DY_RUNS),
        "anchor_runs": len(trajectories),
        "anchor_events": sum(int(row["n_events"]) for row in trajectories),
        "observed_seed_events": observed_seeds,
        "total_time": total_time,
        "token_time_integral": token_time,
        "effective_tokens": effective_tokens,
        "initial_reference_tokens": initial_reference,
        "selected_candidate": selected["candidate"],
        "selected_local_rate": selected["local_rate_per_host"],
        "fresh_dynamics_runs": 0,
        "relabel_graphs": graph_count,
    }]

    DOC.mkdir(exist_ok=True)
    write_csv(DOC / "v16aa_trajectory_exposure.csv", exposure_rows)
    write_csv(DOC / "v16aa_candidate_comparison.csv", comparison)
    write_csv(DOC / "v16aa_remote_context_audit.csv", remote_rows)
    write_csv(DOC / "v16aa_relabel_audit.csv", relabel_rows)
    write_csv(DOC / "v16aa_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16aa_target_summary.csv", target_rows)
    write_csv(DOC / "v16aa_claim_ledger.csv", claim_rows(str(selected["candidate"]), observed_seeds, baseline_expected))
    report = build_report(trajectories, comparison, remote_rows, relabel_rows, gate_rows, effective_tokens, initial_reference, selected, observed_seeds, baseline_expected)
    (DOC / "v16aa_seed_clock_architecture_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16aa",
        "",
        "Status: `candidate_selected_not_validated`.",
        "",
        f"- Frys `exposure_matched_local` med `rho_seed={fmt(selected['local_rate_per_host'], 12)}`.",
        "- Behold `current_global` som baseline og `preparation_only` som mekanismekontroll.",
        "- Kjoer en fresh matched scheduler-holdout uten refit.",
        "- Ikke endre core anchor eller start v16b event-DAG foer holdouten og ny locality-gate passerer.",
        "- Ikke les den in-sample exposure-matchen som dynamisk eller fysisk validering.",
        "",
    ])
    (DOC / "v0_16aa_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16aa for ikke-spesialister",
        "",
        "Den gamle seed-klokken velger ett sted i hele grafen og fordeler en fast total rate mellom alle tokens. Derfor avhenger en lokal hendelse av hvor mange tokens som finnes langt borte.",
        "",
        "Vi fant en fast rate per token som er genuint lokal og som, beregnet paa gamle tidsforloep, ville gitt omtrent samme totale antall seed-hendelser. Men raten er tilpasset gamle data og maa testes paa nye grafer foer den kan tas i bruk.",
        "",
        "Neste test sammenligner den gamle globale klokken, ingen seed-hendelser etter preparering, og den nye lokale kandidaten paa helt nye startgrafer.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16aa.md").write_text(lay, encoding="utf-8")
    print(f"[v16aa] runs={len(trajectories)} events={sum(int(row['n_events']) for row in trajectories)}")
    print(f"[v16aa] effective_K={effective_tokens:.12f} selected={selected['candidate']} rho={float(selected['local_rate_per_host']):.12f}")
    print("[v16aa] status=candidate_selected_not_validated fresh_runs=0")


if __name__ == "__main__":
    main()
