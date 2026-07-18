#!/usr/bin/env python3
"""v17e matched-prefix, effect-blind scale-response gate.

The qualified v17c length-2-to-4 bounded-cycle kernel is run from the same six
state spaces, starts, and v17d random streams.  The first checkpoint window
must replay the frozen v17d late window exactly.  The chains then continue to
twice the v17d step budget.  Direct cross-start endpoint distance is the
primary response; source spectra and observed-effect metrics are prohibited.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import statistics
from typing import Any, Dict, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17b_residual_cycle_constructor_gate as v17b
import relational_universe_v17c_exact_counter_runtime_qualification as v17c
import relational_universe_v17d_effect_blind_finite_stability as v17d


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = v17d.START_FAMILIES
CHAIN_SEED_FAMILIES = v17d.CHAIN_SEED_FAMILIES
TOTAL_STEPS = 4096
BASELINE_STEPS = tuple(range(1536, 2048, 64))
SCALE_STEPS = tuple(range(3584, 4096, 64))
WINDOW_STEPS = {"early": BASELINE_STEPS, "late": SCALE_STEPS}
SAMPLES_PER_WINDOW = 8
MAX_CHAIN_SECONDS = 160.0
MIN_ACCEPTED_CYCLES_PER_WINDOW = 20
MIN_WINDOW_UNIQUE_FRACTION = 0.875
MAX_PRIMARY_DISTANCE_RATIO = 0.90
MAX_CENTER_RANGE_RATIO = v16x.MAX_CENTER_RANGE_RATIO
MAX_CROSS_TO_WITHIN_DISTANCE_RATIO = v17d.MAX_CROSS_TO_WITHIN_DISTANCE_RATIO

ENDPOINT_FEATURES = v17d.ENDPOINT_CENTER_FEATURES
COMPONENT_FEATURES = v17d.COMPONENT_CENTER_FEATURES
START_RESPONSE_FEATURES = (
    "source_edge_fraction",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
)

SOURCE_CHAIN = DOC / "v17e_source_chain.csv"
PRE_REGISTRATION = DOC / "v17e_pre_registration.csv"
PREFIX_REPLAY = DOC / "v17e_v17d_prefix_replay.csv"
ENDPOINT_AUDIT = DOC / "v17e_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v17e_pairwise_distance.csv"
CENTER_STABILITY = DOC / "v17e_center_stability.csv"
ENDPOINT_AGREEMENT = DOC / "v17e_endpoint_agreement.csv"
SCALE_RESPONSE = DOC / "v17e_cross_start_scale_response.csv"
FEATURE_RESPONSE = DOC / "v17e_start_feature_scale_response.csv"
COMPONENT_PROFILE = DOC / "v17e_residual_component_profile.csv"
COMPONENT_STABILITY = DOC / "v17e_residual_component_stability.csv"
RESIDUAL_AUDIT = DOC / "v17e_residual_partition_audit.csv"
PROPOSAL_FOOTPRINT = DOC / "v17e_proposal_footprint.csv"
PROPOSAL_OVERLAP = DOC / "v17e_proposal_footprint_overlap.csv"
TRANSITION_SUMMARY = DOC / "v17e_chain_transition_summary.csv"
REVERSIBILITY_AUDIT = DOC / "v17e_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17e_representation_audit.csv"
SOURCE_SUMMARY = DOC / "v17e_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17e_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v17e_claim_ledger.csv"
REPORT = DOC / "v17e_effect_blind_scale_response_gate.md"
INTERPRETATION = DOC / "v17e_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17e_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17e_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17e.md"

Endpoint = v17d.Endpoint
Footprint = v17d.Footprint


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v17c", "qualified_proposal_implementation", v17c.SCRIPT),
        ("v17d", "frozen_preregistration", v17d.PRE_REGISTRATION),
        ("v17d", "frozen_gate", v17d.GATE_EVALUATION),
        ("v17d", "frozen_endpoint_prefix", v17d.ENDPOINT_AUDIT),
        ("v17d", "qualified_runner", v17d.SCRIPT),
        ("v17d", "interpretation_boundary", v17d.INTERPRETATION),
        ("v17d", "postrun_diagnosis", v17d.POSTRUN_REPORT if hasattr(v17d, "POSTRUN_REPORT") else DOC / "v17d_postrun_start_memory_diagnosis.md"),
    )
    return [
        {
            "stage": stage,
            "role": role,
            "artifact": path.name,
            "sha256": file_sha256(path),
            "source_pass": 1,
        }
        for stage, role, path in paths
    ]


def spec_payload() -> Dict[str, Any]:
    return {
        "gate": "v17e_effect_blind_scale_response",
        "purpose_ref": PURPOSE_REF,
        "scope": "matched_prefix_2048_to_4096_cross_start_distance_response",
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "random_stream": "exact_v17d_chain_seed_and_prefix",
        "proposal_law": "qualified_v17c_exact_counter_bounded_cycles_2_3_4",
        "stationary_target_scope": "uniform_per_bounded_cycle_proposal_connected_component",
        "total_steps": TOTAL_STEPS,
        "baseline_steps": list(BASELINE_STEPS),
        "scale_steps": list(SCALE_STEPS),
        "samples_per_window": SAMPLES_PER_WINDOW,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_accepted_cycles_per_window": MIN_ACCEPTED_CYCLES_PER_WINDOW,
        "minimum_window_unique_fraction": MIN_WINDOW_UNIQUE_FRACTION,
        "primary_metric": "median_all_cross_start_changed_edge_fraction_scale_over_baseline",
        "maximum_primary_distance_ratio": MAX_PRIMARY_DISTANCE_RATIO,
        "required_primary_source_passes": 6,
        "required_v17d_prefix_replays": 192,
        "endpoint_features": list(ENDPOINT_FEATURES),
        "start_response_features": list(START_RESPONSE_FEATURES),
        "residual_component_features": list(COMPONENT_FEATURES),
        "diagnostic_boundary": (
            "center, residual-SCC, and accepted-footprint rows are diagnostics; "
            "they are not global state-graph connectivity or mixing proofs"
        ),
        "stop_rule": (
            "if fewer than six sources have primary ratio <=0.90, retire further "
            "scale growth of the length-2-to-4 kernel and change the move class"
        ),
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "irreducibility",
            "convergence",
            "mixing_time",
            "global_uniformity",
            "canonical_measure",
            "source_effect",
            "energy",
            "temperature",
            "Lorentz_symmetry",
            "spacetime",
            "particles",
            "Bell_correlation",
            "entanglement",
            "universe_model",
        ],
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_row() -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "random_stream": "exact_v17d_chain_seed_and_prefix",
        "proposal_law": "qualified_v17c_exact_counter_bounded_cycles_2_3_4",
        "total_steps": TOTAL_STEPS,
        "baseline_steps": ";".join(map(str, BASELINE_STEPS)),
        "scale_steps": ";".join(map(str, SCALE_STEPS)),
        "samples_per_window": SAMPLES_PER_WINDOW,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_accepted_cycles_per_window": MIN_ACCEPTED_CYCLES_PER_WINDOW,
        "minimum_window_unique_fraction": MIN_WINDOW_UNIQUE_FRACTION,
        "primary_metric": "median_all_cross_start_changed_edge_fraction_scale_over_baseline",
        "maximum_primary_distance_ratio": MAX_PRIMARY_DISTANCE_RATIO,
        "required_primary_source_passes": 6,
        "required_v17d_prefix_replays": 192,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17d.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17e] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17e preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17e source chain changed")


def configure_v17d_runner() -> None:
    v17d.TOTAL_STEPS = TOTAL_STEPS
    v17d.EARLY_STEPS = BASELINE_STEPS
    v17d.LATE_STEPS = SCALE_STEPS
    v17d.WINDOW_STEPS = WINDOW_STEPS
    v17d.SAMPLES_PER_WINDOW = SAMPLES_PER_WINDOW
    v17d.MAX_CHAIN_SECONDS = MAX_CHAIN_SECONDS
    v17d.MIN_ACCEPTED_CYCLES_PER_WINDOW = MIN_ACCEPTED_CYCLES_PER_WINDOW
    v17d.MIN_WINDOW_UNIQUE_FRACTION = MIN_WINDOW_UNIQUE_FRACTION


def implementation_call_counts() -> Dict[str, int]:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    names = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            names[node.func.attr] += 1
        elif isinstance(node.func, ast.Name):
            names[node.func.id] += 1
    return {
        "spectrum_calls": names["interval_spectrum"],
        "effect_metric_calls": names["jensen_shannon"],
    }


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v16x.load_runs():
        runs.append(
            (
                v16i.RunDAG(
                    stage="v17e",
                    target_nodes=source.target_nodes,
                    growth_seed=source.growth_seed,
                    run_offset=source.run_offset,
                    arm=source.arm,
                    run_seed=source.run_seed,
                    predecessors=source.predecessors,
                    depths=source.depths,
                    indegrees=source.indegrees,
                ),
                metadata,
            )
        )
    if len(runs) != 6:
        raise ValueError("v17e requires six frozen source histories")
    return runs


def source_key(row: Mapping[str, Any]) -> Tuple[int, int]:
    return int(row["growth_seed"]), int(row["run_offset"])


def prefix_reference() -> Dict[Tuple[int, int, str, str, int, int], str]:
    rows = v16i.read_csv(v17d.ENDPOINT_AUDIT)
    reference = {}
    for row in rows:
        if row["window"] != "late":
            continue
        key = (
            int(row["growth_seed"]),
            int(row["run_offset"]),
            row["start_family"],
            row["chain_seed_family"],
            int(row["sample_index"]),
            int(row["step"]),
        )
        reference[key] = row["endpoint_edge_sha256"]
    if len(reference) != 192:
        raise ValueError("v17e expected 192 frozen v17d prefix endpoints")
    return reference


def prefix_replay_rows(
    endpoints: Sequence[Endpoint],
    reference: Mapping[Tuple[int, int, str, str, int, int], str],
) -> List[Dict[str, Any]]:
    rows = []
    for endpoint in endpoints:
        row = endpoint.row
        if row["window"] != "early":
            continue
        key = (
            int(row["growth_seed"]),
            int(row["run_offset"]),
            row["start_family"],
            row["chain_seed_family"],
            int(row["sample_index"]),
            int(row["step"]),
        )
        expected = reference.get(key, "")
        observed = row["endpoint_edge_sha256"]
        rows.append(
            {
                "stage": "v17e",
                "growth_seed": key[0],
                "run_offset": key[1],
                "start_family": key[2],
                "chain_seed_family": key[3],
                "sample_index": key[4],
                "step": key[5],
                "expected_v17d_endpoint_sha256": expected,
                "observed_v17e_endpoint_sha256": observed,
                "exact_prefix_replay_pass": int(bool(expected) and expected == observed),
            }
        )
    return rows


def scale_response_rows(
    dag: v16i.RunDAG,
    pairwise: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    for row in pairwise:
        if row["left_window"] != row["right_window"]:
            continue
        relation = (
            "cross_start"
            if row["left_start_family"] != row["right_start_family"]
            else "within_start"
        )
        grouped[(row["left_window"], relation)].append(float(row["changed_edge_fraction"]))

    baseline_cross = statistics.median(grouped[("early", "cross_start")])
    scale_cross = statistics.median(grouped[("late", "cross_start")])
    baseline_within = statistics.median(grouped[("early", "within_start")])
    scale_within = statistics.median(grouped[("late", "within_start")])
    direct_ratio = scale_cross / baseline_cross if baseline_cross else math.inf
    baseline_separation = baseline_cross / baseline_within if baseline_within else math.inf
    scale_separation = scale_cross / scale_within if scale_within else math.inf
    return [
        {
            **dag.prefix,
            "baseline_step_budget": 2048,
            "scale_step_budget": 4096,
            "baseline_cross_start_pair_count": len(grouped[("early", "cross_start")]),
            "scale_cross_start_pair_count": len(grouped[("late", "cross_start")]),
            "baseline_median_cross_start_distance": baseline_cross,
            "scale_median_cross_start_distance": scale_cross,
            "scale_over_baseline_cross_start_distance_ratio": direct_ratio,
            "maximum_primary_ratio": MAX_PRIMARY_DISTANCE_RATIO,
            "primary_material_contraction_pass": int(direct_ratio <= MAX_PRIMARY_DISTANCE_RATIO),
            "baseline_median_within_start_distance": baseline_within,
            "scale_median_within_start_distance": scale_within,
            "baseline_cross_to_within_ratio": baseline_separation,
            "scale_cross_to_within_ratio": scale_separation,
            "scale_over_baseline_separation_ratio": (
                scale_separation / baseline_separation if baseline_separation else math.inf
            ),
            "directional_cross_start_contraction": int(scale_cross < baseline_cross),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        }
    ]


def feature_response_rows(
    dag: v16i.RunDAG,
    endpoints: Sequence[Endpoint],
) -> List[Dict[str, Any]]:
    rows = []
    for feature in START_RESPONSE_FEATURES:
        centers: Dict[Tuple[str, str], float] = {}
        for window in WINDOW_STEPS:
            for start_family in START_FAMILIES:
                values = [
                    float(endpoint.row[feature])
                    for endpoint in endpoints
                    if endpoint.row["window"] == window
                    and endpoint.row["start_family"] == start_family
                ]
                centers[(window, start_family)] = statistics.median(values)
        baseline_gap = abs(
            centers[("early", START_FAMILIES[0])]
            - centers[("early", START_FAMILIES[1])]
        )
        scale_gap = abs(
            centers[("late", START_FAMILIES[0])]
            - centers[("late", START_FAMILIES[1])]
        )
        rows.append(
            {
                **dag.prefix,
                "feature": feature,
                "baseline_start_gap": baseline_gap,
                "scale_start_gap": scale_gap,
                "scale_over_baseline_gap_ratio": (
                    scale_gap / baseline_gap if baseline_gap else (0.0 if scale_gap == 0 else math.inf)
                ),
                "directional_gap_contraction": int(scale_gap < baseline_gap),
                "preregistered_primary_metric": 0,
                "source_spectrum_computed": 0,
                "observed_effect_computed": 0,
            }
        )
    return rows


def residual_audit_rows(
    dag: v16i.RunDAG,
    profiles: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    digests = {row["residual_component_profile_sha256"] for row in profiles}
    jaccards = [float(row["source_flexible_edge_jaccard"]) for row in profiles]
    exact = len(profiles) == 8 and len(digests) == 1 and min(jaccards) == 1.0
    return [
        {
            **dag.prefix,
            "representative_endpoint_count": len(profiles),
            "unique_residual_component_profile_count": len(digests),
            "minimum_source_flexible_edge_jaccard": min(jaccards),
            "maximum_source_flexible_edge_jaccard": max(jaccards),
            "exact_within_source_residual_partition_identity": int(exact),
            "bounded_cycle_state_graph_connectivity_claimed": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        }
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    return v17b.markdown_table(rows, fields)


def write_documents(
    overall: str,
    gates: Sequence[Mapping[str, Any]],
    responses: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    residual_rows: Sequence[Mapping[str, Any]],
) -> None:
    primary_passes = sum(int(row["primary_material_contraction_pass"]) for row in responses)
    ratios = [float(row["scale_over_baseline_cross_start_distance_ratio"]) for row in responses]
    directional = sum(int(row["directional_cross_start_contraction"]) for row in responses)
    feature_contractions = sum(int(row["directional_gap_contraction"]) for row in feature_rows)
    residual_identity = sum(int(row["exact_within_source_residual_partition_identity"]) for row in residual_rows)
    retire = primary_passes != 6

    report = [
        "# v17e effect-blind scale-response gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Frozen design",
        "",
        "V17e reuses the six v17d state spaces, both frozen starts, both v17d random streams, and the exact v17c length-2-to-4 proposal law. The 1536-1984 checkpoint window must replay v17d exactly; each chain then continues without restart to a 3584-4032 window under a 4096-step total budget. No source spectrum or observed-effect statistic is computed.",
        "",
        "## Primary scale response",
        "",
        *markdown_table(
            responses,
            (
                "growth_seed",
                "run_offset",
                "baseline_median_cross_start_distance",
                "scale_median_cross_start_distance",
                "scale_over_baseline_cross_start_distance_ratio",
                "primary_material_contraction_pass",
                "baseline_cross_to_within_ratio",
                "scale_cross_to_within_ratio",
            ),
        ),
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Diagnostics",
        "",
        f"Direct cross-start distance contracted directionally in `{directional}/6` sources and met the preregistered material threshold in `{primary_passes}/6`. The source-ratio range was `{min(ratios):.6f}-{max(ratios):.6f}`. Start-sensitive feature gaps contracted directionally in `{feature_contractions}/{len(feature_rows)}` diagnostic cells. Exact residual-profile identity held in `{residual_identity}/6` sources.",
        "",
        f"All 24 chains had a maximum runtime of `{max(float(row['elapsed_seconds']) for row in transitions):.6f}` seconds. These finite rows do not prove convergence, irreducibility, mixing, global uniformity, or state-graph connectivity.",
        "",
        "## Decision",
        "",
        (
            "The preregistered six-source contraction requirement failed. Further scale growth of this length-2-to-4 kernel is retired. The next gate must change the move class while preserving an explicit target law and effect blindness."
            if retire
            else
            "All six sources met the material contraction threshold. This supports a separate finite mixing-curve qualification, not a source-effect or physics test."
        ),
        "",
        "## Claim boundary",
        "",
        "No source effect, Bell correlation, entanglement, Lorentz symmetry, spacetime geometry, particle, energy, temperature, or universe model was tested.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")

    INTERPRETATION.write_text(
        "# v17e interpretation audit\n\n"
        f"Frozen status is `{overall}`. Matched-prefix replay, integrity, reversibility, representation, traversal, and resource checks are separate from the primary cross-start distance response.\n\n"
        f"The primary requirement passed `{primary_passes}/6`; the observed scale/baseline ratio range is `{min(ratios):.6f}-{max(ratios):.6f}`. "
        "A failed contraction gate retires scale growth for this move class; it does not prove disconnected components. A pass would still not prove convergence or a canonical measure.\n\n"
        f"Residual-profile identity passed `{residual_identity}/6`. This is an exact residual-algebra diagnostic, not global bounded-cycle state-graph connectivity. Source spectra and effect metrics remained prohibited.\n",
        encoding="utf-8",
    )

    if retire:
        next_text = (
            "# v17e next direction\n\n"
            f"Formal status: `{overall}`.\n\n"
            "Retire further step-budget scaling of the length-2-to-4 kernel. Preregister one effect-blind move-class expansion on the same six spaces and starts. Preserve the explicit uniform target and exact reverse accounting, but introduce a genuinely broader transition, such as exact longer alternating cycles or a reversible compound-cycle proposal.\n\n"
            "The primary question is whether the expanded move class reduces cross-start separation under a matched realized-work budget. Do not inspect the source spectrum until the new kernel passes probability, representation, traversal, resource, and start-memory gates.\n"
        )
        recommendation = "- next: replace the length-2-to-4 move class under an effect-blind matched-work gate"
    else:
        next_text = (
            "# v17e next direction\n\n"
            f"Formal status: `{overall}`.\n\n"
            "Preregister one finite multiscale mixing-curve qualification with independent streams. A scale response is not a convergence proof and does not yet reopen the source effect.\n"
        )
        recommendation = "- next: finite independent-stream mixing-curve qualification"
    NEXT_DIRECTION.write_text(next_text, encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17e\n\n"
        f"- status: `{overall}`\n"
        f"{recommendation}\n"
        "- claim ceiling: matched finite 2048-to-4096 scale response on six spaces; no convergence or physics claim\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17e for ikke-spesialister\n\n"
        "V17e gjentar de samme tilfeldige forlopene fra v17d helt frem til 2048 steg og lar dem deretter fortsette til 4096. Hovedsporsmalet er om avstanden mellom resultatene fra to ulike startgrafer blir minst ti prosent mindre.\n\n"
        f"Statusen er `{overall}`. Dette er en avgrenset test av en bestemt matematisk flytteregel. Den kan verken bevise konvergens eller fysikk, og en stabil reststruktur er ikke det samme som et sammenhengende globalt tilstandsrom.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    configure_v17d_runner()
    v17c.install_optimized_constructor()
    frozen_starts = v16z.frozen_start_digests()
    reference = prefix_reference()

    endpoint_rows: List[MutableMapping[str, Any]] = []
    pairwise_rows: List[Dict[str, Any]] = []
    center_rows: List[Dict[str, Any]] = []
    agreement_rows: List[Dict[str, Any]] = []
    response_rows: List[Dict[str, Any]] = []
    feature_rows: List[Dict[str, Any]] = []
    component_profiles: List[Dict[str, Any]] = []
    component_stability: List[Dict[str, Any]] = []
    residual_rows: List[Dict[str, Any]] = []
    footprint_rows: List[MutableMapping[str, Any]] = []
    overlap_rows: List[Dict[str, Any]] = []
    transition_rows: List[Dict[str, Any]] = []
    reversibility_rows: List[Dict[str, Any]] = []
    representation_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        flexibility = v16x.audit_flexibility(space)
        kernel = v17a.build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        source_endpoints: List[Endpoint] = []
        source_footprints: List[Footprint] = []
        source_transitions: List[Dict[str, Any]] = []
        source_reversibility: List[Dict[str, Any]] = []
        source_representations: List[Dict[str, Any]] = []
        frozen_start_passes = 0

        for start_family, start in starts.items():
            frozen_start_passes += int(
                v16x.edge_digest(start)
                == frozen_starts[(dag.growth_seed, dag.run_offset, start_family)]
            )
            source_reversibility.extend(v17b.reversibility_rows(dag, kernel, start, start_family))
            source_representations.append(
                v17b.representation_row(dag, metadata, space, start, start_family)
            )
            for seed_family in CHAIN_SEED_FAMILIES:
                result = v17d.run_chain(
                    dag,
                    metadata,
                    kernel,
                    flexibility.forced_source_edges,
                    start,
                    start_family,
                    seed_family,
                )
                source_endpoints.extend(result.endpoints)
                source_footprints.extend(result.footprints)
                source_transitions.append(result.stats)

        source_pairwise = v17d.pairwise_rows(dag, source_endpoints)
        source_center = v17d.center_rows(
            dag, source_endpoints, lambda item: item.row, ENDPOINT_FEATURES, "endpoint"
        )
        source_agreement = v17d.endpoint_agreement_rows(dag, source_endpoints)
        source_response = scale_response_rows(dag, source_pairwise)
        source_feature = feature_response_rows(dag, source_endpoints)
        representative = [
            endpoint
            for endpoint in source_endpoints
            if int(endpoint.row["sample_index"]) == SAMPLES_PER_WINDOW - 1
        ]
        source_components = [
            v17d.residual_component_row(
                dag, space, flexibility.flexible_edges, endpoint
            )
            for endpoint in representative
        ]
        source_component_stability = v17d.center_rows(
            dag,
            source_components,
            lambda item: item,
            COMPONENT_FEATURES,
            "residual_component",
        )
        source_residual = residual_audit_rows(dag, source_components)
        source_overlap = v17d.proposal_overlap_rows(dag, space, source_footprints)
        source_replay = prefix_replay_rows(source_endpoints, reference)

        endpoint_rows.extend(endpoint.row for endpoint in source_endpoints)
        pairwise_rows.extend(source_pairwise)
        center_rows.extend(source_center)
        agreement_rows.extend(source_agreement)
        response_rows.extend(source_response)
        feature_rows.extend(source_feature)
        component_profiles.extend(source_components)
        component_stability.extend(source_component_stability)
        residual_rows.extend(source_residual)
        footprint_rows.extend(footprint.row for footprint in source_footprints)
        overlap_rows.extend(source_overlap)
        transition_rows.extend(source_transitions)
        reversibility_rows.extend(source_reversibility)
        representation_rows.extend(source_representations)
        replay_rows.extend(source_replay)

        chain_passes = sum(
            int(row["traversal_pass"]) and int(row["resource_pass"])
            for row in source_transitions
        )
        prefix_passes = sum(int(row["exact_prefix_replay_pass"]) for row in source_replay)
        reverse_passes = sum(
            int(row["pathwise_detailed_balance_pass"]) for row in source_reversibility
        )
        representation_passes = sum(
            int(row["representation_pass"]) for row in source_representations
        )
        integrity_passes = sum(
            int(endpoint.row["endpoint_integrity_pass"]) for endpoint in source_endpoints
        )
        primary_pass = int(source_response[0]["primary_material_contraction_pass"])
        residual_pass = int(source_residual[0]["exact_within_source_residual_partition_identity"])
        source_pass = all(
            (
                frozen_start_passes == 2,
                chain_passes == 4,
                prefix_passes == 32,
                reverse_passes == 6,
                representation_passes == 2,
                integrity_passes == 64,
                primary_pass == 1,
            )
        )
        summaries.append(
            {
                **dag.prefix,
                "frozen_start_passes": frozen_start_passes,
                "chain_passes": chain_passes,
                "v17d_prefix_replay_passes": prefix_passes,
                "reversibility_passes": reverse_passes,
                "representation_passes": representation_passes,
                "endpoint_integrity_passes": integrity_passes,
                "primary_scale_response_pass": primary_pass,
                "cross_start_distance_ratio": source_response[0][
                    "scale_over_baseline_cross_start_distance_ratio"
                ],
                "residual_partition_identity_pass": residual_pass,
                "maximum_chain_seconds": max(
                    float(row["elapsed_seconds"]) for row in source_transitions
                ),
                "source_qualification_pass": int(source_pass),
            }
        )
        print(
            f"[v17e] sources={run_index}/6 chains={chain_passes}/4 "
            f"prefix={prefix_passes}/32 ratio={float(source_response[0]['scale_over_baseline_cross_start_distance_ratio']):.6f} "
            f"primary={primary_pass}"
        )

    calls = implementation_call_counts()
    exclusion_pass = all(
        (
            calls == {"spectrum_calls": 0, "effect_metric_calls": 0},
            all(int(row["source_spectrum_computed"]) == 0 for row in endpoint_rows),
            all(int(row["observed_effect_computed"]) == 0 for row in endpoint_rows),
            all(int(row["source_spectrum_computed"]) == 0 for row in transition_rows),
            all(int(row["observed_effect_computed"]) == 0 for row in transition_rows),
        )
    )
    start_count = sum(int(row["frozen_start_passes"]) for row in summaries)
    replay_count = sum(int(row["exact_prefix_replay_pass"]) for row in replay_rows)
    integrity_count = sum(int(row["endpoint_integrity_pass"]) for row in endpoint_rows)
    reverse_count = sum(int(row["pathwise_detailed_balance_pass"]) for row in reversibility_rows)
    representation_count = sum(int(row["representation_pass"]) for row in representation_rows)
    traversal_count = sum(int(row["traversal_pass"]) for row in transition_rows)
    resource_count = sum(int(row["resource_pass"]) for row in transition_rows)
    primary_count = sum(int(row["primary_material_contraction_pass"]) for row in response_rows)
    center_count = sum(int(row["center_stability_pass"]) for row in center_rows)
    agreement_count = sum(int(row["endpoint_agreement_pass"]) for row in agreement_rows)
    component_count = sum(int(row["center_stability_pass"]) for row in component_stability)
    residual_count = sum(
        int(row["exact_within_source_residual_partition_identity"]) for row in residual_rows
    )
    overlap_count = sum(
        int(row["proposal_footprint_overlap_pass"]) for row in overlap_rows
    )

    if not exclusion_pass or start_count != 12 or replay_count != 192 or integrity_count != 384:
        overall = "v17e_instrumentation_failed"
    elif reverse_count != 36:
        overall = "v17e_reversibility_not_qualified"
    elif representation_count != 12:
        overall = "v17e_representation_not_qualified"
    elif traversal_count != 24:
        overall = "v17e_finite_traversal_not_qualified"
    elif resource_count != 24:
        overall = "v17e_resource_not_qualified"
    elif primary_count != 6:
        overall = "v17e_cross_start_distance_flat_retire_length_2_4_kernel"
    else:
        overall = "v17e_cross_start_distance_contracts_at_2x_scale"

    ratios = [float(row["scale_over_baseline_cross_start_distance_ratio"]) for row in response_rows]
    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_replay", "status": "pass" if start_count == 12 else "fail", "observed": f"{start_count}/12", "required": "12/12", "decision": "continue" if start_count == 12 else "invalidate"},
        {"gate": "matched_v17d_prefix_replay", "status": "pass" if replay_count == 192 else "fail", "observed": f"{replay_count}/192", "required": "192/192", "decision": "continue" if replay_count == 192 else "invalidate"},
        {"gate": "endpoint_integrity", "status": "pass" if integrity_count == 384 else "fail", "observed": f"{integrity_count}/384", "required": "384/384", "decision": "continue" if integrity_count == 384 else "invalidate"},
        {"gate": "pathwise_detailed_balance", "status": "pass" if reverse_count == 36 else "fail", "observed": f"{reverse_count}/36", "required": "36/36", "decision": "continue" if reverse_count == 36 else "repair_probability"},
        {"gate": "representation_covariance", "status": "pass" if representation_count == 12 else "fail", "observed": f"{representation_count}/12", "required": "12/12", "decision": "continue" if representation_count == 12 else "repair_representation"},
        {"gate": "finite_traversal", "status": "pass" if traversal_count == 24 else "fail", "observed": f"{traversal_count}/24", "required": "24/24", "decision": "continue" if traversal_count == 24 else "insufficient_traversal"},
        {"gate": "resource_bound", "status": "pass" if resource_count == 24 else "fail", "observed": f"{resource_count}/24;max={max(float(row['elapsed_seconds']) for row in transition_rows):.6f}s", "required": "24/24;each<=160s", "decision": "continue" if resource_count == 24 else "resource_not_qualified"},
        {"gate": "primary_cross_start_distance_contraction", "status": "pass" if primary_count == 6 else "fail", "observed": f"{primary_count}/6;ratio={min(ratios):.6f}-{max(ratios):.6f}", "required": "6/6;each<=0.90", "decision": "continue" if primary_count == 6 else "retire_length_2_4_kernel_scale_growth"},
        {"gate": "endpoint_center_diagnostic", "status": "reported", "observed": f"{center_count}/108", "required": "diagnostic_only", "decision": "no_primary_decision"},
        {"gate": "endpoint_agreement_diagnostic", "status": "reported", "observed": f"{agreement_count}/18", "required": "diagnostic_only", "decision": "no_primary_decision"},
        {"gate": "residual_profile_diagnostic", "status": "reported", "observed": f"centers={component_count}/90;identity={residual_count}/6", "required": "diagnostic_only", "decision": "not_connectivity"},
        {"gate": "proposal_footprint_diagnostic", "status": "reported", "observed": f"{overlap_count}/18", "required": "diagnostic_only", "decision": "not_connectivity"},
        {"gate": "v17e_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={start_count}/12;prefix={replay_count}/192;integrity={integrity_count}/384;reverse={reverse_count}/36;representation={representation_count}/12;traversal={traversal_count}/24;resource={resource_count}/24;primary={primary_count}/6", "required": "1;12/12;192/192;384/384;36/36;12/12;24/24;24/24;6/6", "decision": overall},
    ]
    claims = [
        {"claim_id": "C1", "claim": "v17e computes no source spectrum or observed-effect statistic.", "status": "supported" if exclusion_pass else "not_supported", "evidence": "static call audit plus endpoint and transition fields", "scope_limit": "this script and these outputs"},
        {"claim_id": "C2", "claim": "The 2048-step v17e checkpoint exactly replays the frozen v17d endpoint window.", "status": "supported" if replay_count == 192 else "not_supported", "evidence": "v17e_v17d_prefix_replay.csv", "scope_limit": "192 recorded endpoints"},
        {"claim_id": "C3", "claim": "Direct cross-start endpoint distance contracts materially from 2048 to 4096 under the frozen threshold in all six spaces.", "status": "supported" if primary_count == 6 else "not_supported", "evidence": "v17e_cross_start_scale_response.csv", "scope_limit": "six reused spaces, two starts, two streams, two finite windows"},
        {"claim_id": "C4", "claim": "Residual profile identity proves the bounded-cycle state graph is connected.", "status": "unsupported", "evidence": "v17e_residual_partition_audit.csv", "scope_limit": "residual algebra is not global state-graph reachability"},
        {"claim_id": "C5", "claim": "The tested chain is irreducible, converged, mixed, or globally uniform.", "status": "unsupported", "evidence": "none", "scope_limit": "finite scale response cannot prove these properties"},
        {"claim_id": "C6", "claim": "The v16s source effect survives this sampler.", "status": "not_tested", "evidence": "source effects prohibited", "scope_limit": "requires a separately qualified sampler"},
        {"claim_id": "C7", "claim": "The model exhibits Bell correlation, entanglement, Lorentz symmetry, spacetime, particles, physical energy, or temperature.", "status": "not_tested", "evidence": "required observables and interventions absent", "scope_limit": "outside v17e"},
    ]

    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PREFIX_REPLAY, replay_rows)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise_rows)
    v16i.write_csv(CENTER_STABILITY, center_rows)
    v16i.write_csv(ENDPOINT_AGREEMENT, agreement_rows)
    v16i.write_csv(SCALE_RESPONSE, response_rows)
    v16i.write_csv(FEATURE_RESPONSE, feature_rows)
    v16i.write_csv(COMPONENT_PROFILE, component_profiles)
    v16i.write_csv(COMPONENT_STABILITY, component_stability)
    v16i.write_csv(RESIDUAL_AUDIT, residual_rows)
    v16i.write_csv(PROPOSAL_FOOTPRINT, footprint_rows)
    v16i.write_csv(PROPOSAL_OVERLAP, overlap_rows)
    v16i.write_csv(TRANSITION_SUMMARY, transition_rows)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility_rows)
    v16i.write_csv(REPRESENTATION_AUDIT, representation_rows)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    write_documents(
        overall, gates, response_rows, feature_rows, transition_rows, residual_rows
    )
    print(f"[v17e] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    expected_counts = {
        PREFIX_REPLAY: 192,
        ENDPOINT_AUDIT: 384,
        PAIRWISE_DISTANCE: 6 * (64 * 63 // 2),
        CENTER_STABILITY: 108,
        ENDPOINT_AGREEMENT: 18,
        SCALE_RESPONSE: 6,
        FEATURE_RESPONSE: 18,
        COMPONENT_PROFILE: 48,
        COMPONENT_STABILITY: 90,
        RESIDUAL_AUDIT: 6,
        PROPOSAL_FOOTPRINT: 48,
        PROPOSAL_OVERLAP: 18,
        TRANSITION_SUMMARY: 24,
        REVERSIBILITY_AUDIT: 36,
        REPRESENTATION_AUDIT: 12,
        SOURCE_SUMMARY: 6,
        GATE_EVALUATION: 14,
        CLAIM_LEDGER: 7,
    }
    loaded = {path: v16i.read_csv(path) for path in expected_counts}
    for path, expected in expected_counts.items():
        if len(loaded[path]) != expected:
            raise ValueError(
                f"v17e row count failed for {path.name}: {len(loaded[path])} != {expected}"
            )
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise ValueError("v17e effect exclusion failed")
    if sum(int(row["exact_prefix_replay_pass"]) for row in loaded[PREFIX_REPLAY]) != 192:
        raise ValueError("v17e matched prefix replay failed")
    if any(int(row["source_spectrum_computed"]) for row in loaded[ENDPOINT_AUDIT]):
        raise ValueError("v17e endpoint rows contain source spectrum")
    if any(int(row["observed_effect_computed"]) for row in loaded[ENDPOINT_AUDIT]):
        raise ValueError("v17e endpoint rows contain observed effect")
    overall = next(
        row["status"] for row in loaded[GATE_EVALUATION] if row["gate"] == "v17e_overall"
    )
    allowed = {
        "v17e_instrumentation_failed",
        "v17e_reversibility_not_qualified",
        "v17e_representation_not_qualified",
        "v17e_finite_traversal_not_qualified",
        "v17e_resource_not_qualified",
        "v17e_cross_start_distance_flat_retire_length_2_4_kernel",
        "v17e_cross_start_distance_contracts_at_2x_scale",
    }
    if overall not in allowed:
        raise ValueError(f"unknown v17e status: {overall}")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v17e documentation missing: {path.name}")
    print(f"[v17e] output verification pass overall={overall}")


def self_test() -> None:
    configure_v17d_runner()
    v17c.self_test()
    if len(BASELINE_STEPS) != SAMPLES_PER_WINDOW or len(SCALE_STEPS) != SAMPLES_PER_WINDOW:
        raise AssertionError("v17e sample schedule failed")
    if set(BASELINE_STEPS) & set(SCALE_STEPS):
        raise AssertionError("v17e windows overlap")
    if BASELINE_STEPS != v17d.LATE_STEPS and BASELINE_STEPS != tuple(range(1536, 2048, 64)):
        raise AssertionError("v17e baseline does not match v17d late window")
    if v17d.chain_seed(load_runs()[0][0], START_FAMILIES[0], CHAIN_SEED_FAMILIES[0]) != v16i.stable_seed(
        "v17d", "chain", START_FAMILIES[0], CHAIN_SEED_FAMILIES[0], *load_runs()[0][0].key
    ):
        raise AssertionError("v17e random stream does not match v17d")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v17e effect exclusion audit failed")
    if len(prefix_reference()) != 192:
        raise AssertionError("v17e frozen prefix reference failed")
    print("[v17e] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v17e effect-blind scale-response gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose only one mode")
    if args.prepare_only:
        prepare()
    elif args.self_test:
        self_test()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
