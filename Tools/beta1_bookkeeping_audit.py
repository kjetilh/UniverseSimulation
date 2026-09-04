#!/usr/bin/env python3
"""Measure beta1 bookkeeping fidelity on the actual v15 start configurations.

This is an external audit.  It imports and calls the production constructors;
it deliberately does not repair or reimplement them.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import importlib
import json
import platform
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import networkx as nx

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15cz_pre_registered_continuous_intensity_holdout as v15cz
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15dk_pre_registered_support_rank_holdout as v15dk
import relational_universe_v15dr_active_set_taxonomy_mapper_holdout as v15dr


TARGET_MODULE = "relational_universe_local_max_coupling_lab"
CONSTRUCTORS: dict[str, Callable[..., dict[str, Any]]] = {
    "local_swap": v7.apply_local_swap_perturbation,
    "add_chord": v7.apply_chord_perturbation,
}
CSV_FIELDS = (
    "call_id",
    "constructor",
    "source_program",
    "source_declared_perturbations",
    "target_nodes",
    "growth_regime",
    "growth_seed",
    "center_token_index",
    "seed_delta",
    "schedule_repeat",
    "configuration_size",
    "tokens",
    "nodes_before",
    "edges_before",
    "components_before",
    "beta1_before",
    "nodes_after",
    "edges_after",
    "components_after",
    "beta1_after",
    "selected_v",
    "selected_u",
    "selected_w",
    "fallback_hit",
    "add_edge_noop",
    "recorded_delta_beta1",
    "actual_delta_beta1",
    "mismatch",
)


@dataclass(frozen=True)
class ScheduledCall:
    source_program: str
    source_declared_perturbations: tuple[str, ...]
    target_nodes: int
    growth_seed: int
    center_token_index: int
    seed_delta: int | None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def heartbeat(path: Path, status: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {status}\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tuple_value(module: Any, plural: str, singular: str) -> tuple[Any, ...] | None:
    value = getattr(module, plural, None)
    if value is None:
        value = getattr(module, singular, None)
    if value is None:
        return None
    if isinstance(value, (tuple, list, range, set, frozenset)):
        return tuple(value)
    return (value,)


def actual_schedule() -> list[ScheduledCall]:
    """Discover declared runnable v15 start configurations from the modules."""
    calls: list[ScheduledCall] = []
    for path in sorted(ROOT.glob("relational_universe_v15*.py")):
        module = importlib.import_module(path.stem)
        targets = tuple_value(module, "TARGETS", "TARGET_NODES")
        if targets is None:
            targets = tuple_value(module, "TARGETS", "TARGET")
        growth_seeds = tuple_value(module, "GROWTH_SEEDS", "GROWTH_SEED")
        placements = tuple_value(module, "PLACEMENTS", "PLACEMENT")
        perturbations = tuple_value(module, "PERTURBATIONS", "PERTURBATION")
        if not all(
            value is not None
            for value in (targets, growth_seeds, placements, perturbations)
        ):
            continue
        relevant_perturbations = tuple(
            sorted(
                {
                    str(value)
                    for value in perturbations or ()
                    if str(value) in CONSTRUCTORS
                }
            )
        )
        if not relevant_perturbations:
            continue
        seed_deltas: tuple[Any, ...] = (None,)
        for name in ("FRESH_SEED_DELTAS", "HOLDOUT_SEED_DELTAS", "SEED_DELTAS"):
            if hasattr(module, name):
                seed_deltas = tuple(getattr(module, name))
                break
        for target in targets or ():
            for growth_seed in growth_seeds or ():
                for placement in placements or ():
                    for seed_delta in seed_deltas:
                        calls.append(
                            ScheduledCall(
                                source_program=path.stem,
                                source_declared_perturbations=relevant_perturbations,
                                target_nodes=int(target),
                                growth_seed=int(growth_seed),
                                center_token_index=int(placement),
                                seed_delta=(
                                    None if seed_delta is None else int(seed_delta)
                                ),
                            )
                        )
    return calls


def validate_named_configuration_sources() -> None:
    observed = {
        "v15cz": (
            v15cz.TARGET_NODES,
            (v15cz.GROWTH_SEED,),
            (v15cz.PLACEMENT,),
            len(v15cz.HOLDOUT_SEED_DELTAS),
        ),
        "v15da": (
            v15da.TARGET_NODES,
            (v15da.GROWTH_SEED,),
            tuple(v15da.PLACEMENTS),
            len(v15da.FRESH_SEED_DELTAS),
        ),
        "v15dk": (
            v15dk.TARGET_NODES,
            (v15dk.GROWTH_SEED,),
            tuple(v15dk.PLACEMENTS),
            len(v15dk.FRESH_SEED_DELTAS),
        ),
        "v15dr": (
            v15dr.TARGET_NODES,
            tuple(v15dr.GROWTH_SEEDS),
            tuple(v15dr.PLACEMENTS),
            len(v15dr.FRESH_SEED_DELTAS),
        ),
    }
    expected = {
        "v15cz": (1024, (202,), (1,), 24),
        "v15da": (1024, (202,), (0, 1, 2), 12),
        "v15dk": (1024, (404,), (0, 1, 2), 8),
        "v15dr": (1024, (808, 909, 1001, 1103), (0, 1, 2), 4),
    }
    if observed != expected:
        raise RuntimeError(
            "Named v15 configuration sources changed; review sampling frame: "
            f"observed={observed!r}"
        )


def nx_beta1(g: v7.UGraph) -> tuple[int, int, int, int]:
    """Return N, E, C and beta1 from an independently constructed nx.Graph."""
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(g.nodes())
    nx_graph.add_edges_from(g.edge_set())
    nodes = nx_graph.number_of_nodes()
    edges = nx_graph.number_of_edges()
    components = nx.number_connected_components(nx_graph) if nodes else 0
    return nodes, edges, components, edges - nodes + components


def build_actual_bases(
    schedule: Sequence[ScheduledCall], heartbeat_path: Path
) -> tuple[dict[tuple[int, int], v7.State], list[dict[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    targets = sorted({row.target_nodes for row in schedule})
    ensembles = v15.deep_ensembles(targets)
    ensemble_by_target = {int(ensemble.target_nodes): ensemble for ensemble in ensembles}
    required_pairs = sorted(
        {(row.target_nodes, row.growth_seed) for row in schedule}
    )
    bases: dict[tuple[int, int], v7.State] = {}
    metadata: list[dict[str, Any]] = []
    for target, growth_seed in required_pairs:
        heartbeat(
            heartbeat_path,
            f"building-base target={target} growth_seed={growth_seed}",
        )
        ensemble = ensemble_by_target[target]
        states, rows = v10e.build_bases([ensemble], regime, [growth_seed])
        key = (target, growth_seed)
        state = states[(ensemble.name, growth_seed)]
        bases[key] = state
        source = rows[0]
        metadata.append(
            {
                "ensemble": ensemble.name,
                "burnin_label": ensemble.burnin_label,
                "target_nodes": key[0],
                "growth_seed": key[1],
                "realized_nodes": state.g.num_nodes(),
                "realized_edges": state.g.num_edges(),
                "realized_tokens": state.token_count(),
                "first_hit_step": source.get("first_hit_step", ""),
                "growth_steps_executed": source.get("growth_steps_executed", ""),
                "target_low": source.get("target_low", ""),
                "target_high": source.get("target_high", ""),
            }
        )
    return bases, metadata


def audit_one(
    base: v7.State,
    scheduled: ScheduledCall,
    constructor_name: str,
    repeat: int,
    call_id: int,
) -> dict[str, Any]:
    state = base.clone()
    before = nx_beta1(state.g)
    selection: dict[str, Any] = {}
    original_choose = v7.choose_center_token

    def instrumented_choose(
        measured_state: v7.State, center_token_index: int
    ) -> tuple[int, int, int]:
        v, u, w = original_choose(measured_state, center_token_index)
        primary = sorted(
            candidate
            for candidate in measured_state.g.neighbors(u)
            if candidate != v and not measured_state.g.has_edge(v, candidate)
        )
        selection.update(
            {
                "v": v,
                "u": u,
                "w": w,
                "fallback_hit": int(not primary),
                "add_edge_noop": int(measured_state.g.has_edge(v, w)),
            }
        )
        return v, u, w

    v7.choose_center_token = instrumented_choose
    try:
        info = CONSTRUCTORS[constructor_name](
            state, center_token_index=scheduled.center_token_index
        )
    finally:
        v7.choose_center_token = original_choose
    after = nx_beta1(state.g)
    recorded = int(info["delta_core"]["beta1"])
    actual = int(after[3] - before[3])
    if not selection:
        raise RuntimeError("Constructor did not invoke choose_center_token")
    return {
        "call_id": call_id,
        "constructor": constructor_name,
        "source_program": scheduled.source_program,
        "source_declared_perturbations": ";".join(
            scheduled.source_declared_perturbations
        ),
        "target_nodes": scheduled.target_nodes,
        "growth_regime": "fast_balanced",
        "growth_seed": scheduled.growth_seed,
        "center_token_index": scheduled.center_token_index,
        "seed_delta": "" if scheduled.seed_delta is None else scheduled.seed_delta,
        "schedule_repeat": repeat,
        "configuration_size": before[0],
        "tokens": state.token_count(),
        "nodes_before": before[0],
        "edges_before": before[1],
        "components_before": before[2],
        "beta1_before": before[3],
        "nodes_after": after[0],
        "edges_after": after[1],
        "components_after": after[2],
        "beta1_after": after[3],
        "selected_v": selection["v"],
        "selected_u": selection["u"],
        "selected_w": selection["w"],
        "fallback_hit": selection["fallback_hit"],
        "add_edge_noop": selection["add_edge_noop"],
        "recorded_delta_beta1": recorded,
        "actual_delta_beta1": actual,
        "mismatch": int(recorded != actual),
    }


def run_audit(
    bases: Mapping[tuple[int, int], v7.State],
    schedule: Sequence[ScheduledCall],
    repeats: int,
    heartbeat_path: Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    call_id = 0
    for constructor_name in CONSTRUCTORS:
        heartbeat(heartbeat_path, f"measuring constructor={constructor_name}")
        for repeat in range(1, repeats + 1):
            for scheduled in schedule:
                call_id += 1
                rows.append(
                    audit_one(
                        bases[(scheduled.target_nodes, scheduled.growth_seed)],
                        scheduled,
                        constructor_name,
                        repeat,
                        call_id,
                    )
                )
    counts = Counter(str(row["constructor"]) for row in rows)
    for name in CONSTRUCTORS:
        if counts[name] < 500:
            raise RuntimeError(f"Only {counts[name]} calls for {name}; at least 500 required")
    return rows


def local_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return imports


def import_inventory() -> tuple[list[str], list[str], dict[str, set[str]]]:
    paths = sorted(ROOT.glob("relational_universe_v15*.py"))
    all_local = {path.stem for path in ROOT.glob("*.py")}
    graph: dict[str, set[str]] = {}
    for path in ROOT.glob("*.py"):
        graph[path.stem] = local_imports(path).intersection(all_local)
    direct = sorted(path.name for path in paths if TARGET_MODULE in graph[path.stem])

    def reaches_target(module: str, active: set[str] | None = None) -> bool:
        active = set() if active is None else active
        if module in active:
            return False
        if TARGET_MODULE in graph.get(module, set()):
            return True
        return any(
            reaches_target(dependency, active | {module})
            for dependency in graph.get(module, set())
            if dependency != TARGET_MODULE
        )

    reachable = {path.name for path in paths if reaches_target(path.stem)}
    transitive_only = sorted(reachable.difference(direct))
    return direct, transitive_only, graph


def percent(numerator: int, denominator: int) -> str:
    return f"{100.0 * numerator / denominator:.6f}%" if denominator else "nan"


def aggregate(
    rows: Sequence[Mapping[str, Any]], keys: Sequence[str]
) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    result: list[dict[str, Any]] = []
    for key_values, group in sorted(grouped.items()):
        calls = len(group)
        fallback = sum(int(row["fallback_hit"]) for row in group)
        noop = sum(int(row["add_edge_noop"]) for row in group)
        mismatch = sum(int(row["mismatch"]) for row in group)
        result.append(
            {
                **dict(zip(keys, key_values)),
                "calls": calls,
                "fallback": fallback,
                "fallback_rate": percent(fallback, calls),
                "noop": noop,
                "noop_rate": percent(noop, calls),
                "mismatch": mismatch,
                "mismatch_rate": percent(mismatch, calls),
            }
        )
    return result


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> list[str]:
    output = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    output.extend(
        "| " + " | ".join(str(row.get(field, "")) for field in fields) + " |"
        for row in rows
    )
    return output


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    rows: Sequence[Mapping[str, Any]],
    schedule: Sequence[ScheduledCall],
    base_metadata: Sequence[Mapping[str, Any]],
    direct_imports: Sequence[str],
    transitive_imports: Sequence[str],
    repeats: int,
    source_hashes: Mapping[str, str],
) -> None:
    overall = aggregate(rows, ["constructor"])
    by_size = aggregate(rows, ["constructor", "configuration_size"])
    by_config = aggregate(
        rows,
        [
            "constructor",
            "source_program",
            "target_nodes",
            "growth_seed",
            "center_token_index",
        ],
    )
    all_imports = list(direct_imports) + list(transitive_imports)
    growth_spec = json.dumps(
        asdict(v10e.recommended_regime("fast_balanced")),
        indent=2,
        sort_keys=True,
    ).splitlines()
    lines = [
        "# Beta1 bookkeeping audit",
        "",
        f"Generated: `{utc_now()}`",
        "",
        "## Result",
        "",
        "This is a measurement of the two production perturbation constructors, not a repair.",
            "The measured claim is limited to the source-declared v15 configuration schedule below.",
        "It is not a physics claim and does not by itself invalidate v15.",
        "",
        *markdown_table(
            overall,
            [
                "constructor",
                "calls",
                "fallback",
                "fallback_rate",
                "noop",
                "noop_rate",
                "mismatch",
                "mismatch_rate",
            ],
        ),
        "",
        "A mismatch means recorded `delta_core.beta1` differed from actual `E - N + C`.",
        "Fallback and no-op are measured at constructor entry around the imported production",
        "`choose_center_token`; actual beta1 is recomputed independently with NetworkX before",
        "and after each call.",
        "",
        "## Preregistered outcome interpretation",
        "",
    ]
    mismatch_count = sum(int(row["mismatch"]) for row in rows)
    if mismatch_count:
        lines.extend(
            [
                f"The discrepancy rate is greater than zero ({mismatch_count}/{len(rows)} overall).",
                "The affected measured calls/configurations are reported below. This does not",
                "support the stronger conclusion that v15 as a whole is invalid.",
            ]
        )
    else:
        lines.extend(
            [
                "The discrepancy rate is approximately zero in this measured schedule; the",
                "tested v15 bookkeeping is cleared for this exact scope.",
            ]
        )
    lines.extend(
        [
            "",
            "## Actual v15 configuration schedule",
            "",
            "The tool imports every `relational_universe_v15*.py` module and reads its declared",
            "target(s), growth seed(s), placement(s), perturbation family and, where present,",
            "seed-delta schedule. This includes explicit validation of v15cz/v15da/v15dk/v15dr.",
            "All audited bases use the v15 deep ensemble and `fast_balanced` growth regime.",
            f"The source-declared schedule has {len(schedule)} configurations and is repeated",
            f"{repeats} time(s) for each constructor. Each constructor is tested on every start",
            "configuration even when its source module declared only one of the two families.",
            "Seed-delta affects the later run RNG, not the deterministic constructor on the base",
            "state; keeping every declared seed-delta preserves the program schedule's call weighting.",
            "",
            "Exact imported growth parameters:",
            "",
            "```json",
            *growth_spec,
            "```",
            "",
            *markdown_table(
                base_metadata,
                [
                    "ensemble",
                    "burnin_label",
                    "target_nodes",
                    "growth_seed",
                    "realized_nodes",
                    "realized_edges",
                    "realized_tokens",
                    "first_hit_step",
                    "growth_steps_executed",
                    "target_low",
                    "target_high",
                ],
            ),
            "",
            "## Distribution by realized configuration size",
            "",
            *markdown_table(
                by_size,
                [
                    "constructor",
                    "configuration_size",
                    "calls",
                    "fallback",
                    "fallback_rate",
                    "noop",
                    "noop_rate",
                    "mismatch",
                    "mismatch_rate",
                ],
            ),
            "",
            "## Distribution by source configuration",
            "",
            *markdown_table(
                by_config,
                [
                    "constructor",
                    "source_program",
                    "target_nodes",
                    "growth_seed",
                    "center_token_index",
                    "calls",
                    "fallback",
                    "fallback_rate",
                    "noop",
                    "noop_rate",
                    "mismatch",
                    "mismatch_rate",
                ],
            ),
            "",
            "## Import inventory",
            "",
            f"Among `relational_universe_v15*.py`, {len(direct_imports)} files import",
            f"`{TARGET_MODULE}` directly and {len(transitive_imports)} additional files reach it",
            f"transitively ({len(all_imports)} total). This is static module reachability, not proof",
            "that every module invokes both constructors on every control-flow path.",
            "",
            "### Direct imports",
            "",
            *[f"- `{name}`" for name in direct_imports],
            "",
            "### Transitive-only imports",
            "",
            *[f"- `{name}`" for name in transitive_imports],
            "",
            "## Reproducibility and source hashes",
            "",
            f"- Python: `{platform.python_version()}`",
            f"- NetworkX: `{nx.__version__}`",
            f"- Raw rows: `{len(rows)}`",
            *[f"- `{name}` SHA-256: `{digest}`" for name, digest in source_hashes.items()],
            "",
            "Run from repository root:",
            "",
            "```sh",
            "PYTHONPATH=.codex_pydeps python3 Tools/beta1_bookkeeping_audit.py",
            "```",
            "",
            "## Claim limits",
            "",
            "- Results cover v15 modules with a complete source-declared target/growth-seed/placement",
            "  configuration and at least one of the two audited perturbation families.",
            "- Declared seed-deltas can map to the same deterministic base-state constructor call;",
            "  frequencies are source-schedule-weighted, not a count of unique graph/locus pairs.",
            "- The audit measures initial perturbation bookkeeping, not later coupled dynamics.",
            "- Import reachability is a conservative dependency inventory, not runtime coverage.",
            "- No physics inference follows from this finite software audit.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--csv", default="Documentation/beta1_bookkeeping_audit.csv"
    )
    result.add_argument(
        "--report", default="Documentation/beta1_bookkeeping_audit.md"
    )
    result.add_argument(
        "--heartbeat", default=".program_logs/WP-A.heartbeat"
    )
    result.add_argument("--schedule-repeats", type=int, default=1)
    return result


def main() -> None:
    args = parser().parse_args()
    heartbeat_path = ROOT / args.heartbeat
    heartbeat(heartbeat_path, "audit-started")
    validate_named_configuration_sources()
    schedule = actual_schedule()
    if len(schedule) < 500:
        raise RuntimeError(
            f"Only {len(schedule)} source-declared configurations; at least 500 required"
        )
    bases, base_metadata = build_actual_bases(schedule, heartbeat_path)
    heartbeat(heartbeat_path, "base-build-complete")
    rows = run_audit(bases, schedule, args.schedule_repeats, heartbeat_path)
    heartbeat(heartbeat_path, "measurement-complete")
    direct, transitive, _ = import_inventory()
    source_names = ["relational_universe_local_max_coupling_lab.py"] + sorted(
        {f"{row.source_program}.py" for row in schedule}
    )
    source_hashes = {name: sha256(ROOT / name) for name in source_names}
    write_csv(ROOT / args.csv, rows)
    write_report(
        ROOT / args.report,
        rows,
        schedule,
        base_metadata,
        direct,
        transitive,
        args.schedule_repeats,
        source_hashes,
    )
    heartbeat(heartbeat_path, "outputs-written")
    for summary in aggregate(rows, ["constructor"]):
        print(
            f"{summary['constructor']}: calls={summary['calls']} "
            f"fallback={summary['fallback']} ({summary['fallback_rate']}) "
            f"noop={summary['noop']} ({summary['noop_rate']}) "
            f"mismatch={summary['mismatch']} ({summary['mismatch_rate']})"
        )
    print(
        f"imports: direct={len(direct)} transitive_only={len(transitive)} "
        f"total={len(direct) + len(transitive)}"
    )


if __name__ == "__main__":
    main()
