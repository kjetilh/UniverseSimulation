#!/usr/bin/env python3
"""v0.15dv distributionally relabel-invariant add_chord constructor.

No-new-dynamics instrumentation step after v15du.

The legacy add_chord constructor selects the first valid chord after sorting
integer node ids. v15du showed that this does not transport covariantly under
pure node-id relabelling. This module leaves the legacy constructor unchanged
for historical reproducibility and defines a new experimental constructor:

- select the token identified by placement,
- enumerate every valid local chord rooted at that token node,
- sample uniformly from that finite candidate set,
- fall back to the union of all token-rooted candidates only when the selected
  token has no candidate.

The required symmetry is distributional covariance. The same raw RNG draw is
not expected to select transported candidates after an arbitrary relabelling,
because list order is representation-dependent; the probability measure over
transported candidates must be identical.
"""
from __future__ import annotations

import argparse
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn
import relational_universe_v15du_relabel_symmetry_gate as v15du


DOC = Path("Documentation")

TARGET_NODES = v15du.TARGET_NODES
PERTURBATION = v15du.PERTURBATION
PLACEMENTS = v15du.PLACEMENTS
GROWTH_SEEDS = v15du.GROWTH_SEEDS
RELABEL_SEEDS = v15du.RELABEL_SEEDS
SAMPLE_SEEDS = (19211, 19249, 19289, 19319, 19373, 19403, 19441, 19483)
TOLERANCE = 1.0e-12

Chord = Tuple[int, int, int]


def safe_float(value: Any, default: float = float("nan")) -> float:
    return v15dn.safe_float(value, default)


def safe_int(value: Any, default: int = 0) -> int:
    return v15dn.safe_int(value, default)


def safe_div(numerator: float, denominator: float) -> float:
    if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator == 0.0:
        return float("nan")
    return numerator / denominator


def fmt(value: Any, digits: int = 3) -> str:
    return v15dn.fmt(value, digits=digits)


def mean_defined(values: Iterable[Any]) -> float:
    return v15dn.mean_defined(values)


def median_defined(values: Iterable[Any]) -> float:
    return v15dn.median_defined(values)


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dn.write_csv(Path(path), rows)


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    return v15du.table(rows, fields)


def selected_token_id(state: Any, placement: int) -> int:
    token_ids = state.sorted_token_ids()
    if not token_ids:
        raise ValueError("add_chord requires at least one token")
    return int(token_ids[int(placement) % len(token_ids)])


def chord_candidates_from_root(state: Any, root: int) -> List[Chord]:
    root = int(root)
    if root not in state.g.adj:
        return []
    candidates: set[Chord] = set()
    for bridge in state.g.neighbors(root):
        for target in state.g.neighbors(int(bridge)):
            target = int(target)
            if target != root and not state.g.has_edge(root, target):
                candidates.add((root, int(bridge), target))
    return sorted(candidates)


def enumerate_chord_candidates(state: Any, placement: int) -> Tuple[List[Chord], str, int]:
    token_id = selected_token_id(state, placement)
    selected_root = int(state.token_pos[token_id])
    candidates = chord_candidates_from_root(state, selected_root)
    if candidates:
        return candidates, "selected_token_root", token_id

    fallback: set[Chord] = set()
    for candidate_token_id in state.sorted_token_ids():
        root = int(state.token_pos[candidate_token_id])
        fallback.update(chord_candidates_from_root(state, root))
    if fallback:
        return sorted(fallback), "all_token_roots_fallback", token_id
    raise ValueError("Could not construct any token-rooted add_chord candidate")


def chord_distribution(state: Any, placement: int) -> Tuple[Dict[Chord, float], str, int]:
    candidates, scope, token_id = enumerate_chord_candidates(state, placement)
    probability = 1.0 / len(candidates)
    return {candidate: probability for candidate in candidates}, scope, token_id


def sample_uniform_chord_candidate(state: Any, placement: int, rng: random.Random) -> Tuple[Chord, Dict[str, Any]]:
    candidates, scope, token_id = enumerate_chord_candidates(state, placement)
    candidate = candidates[rng.randrange(len(candidates))]
    return candidate, {
        "candidate_scope": scope,
        "selected_token_id": token_id,
        "candidate_count": len(candidates),
        "selection_policy": "uniform_over_valid_token_rooted_chords",
    }


def apply_uniform_chord(
    state: Any,
    *,
    placement: int,
    rng: random.Random,
) -> Dict[str, Any]:
    (source, bridge, target), metadata = sample_uniform_chord_candidate(state, placement, rng)
    state.g.add_edge(source, target)
    return {
        "type": "local_chord_uniform_token_rooted",
        "support": sorted({source, bridge, target}),
        "ordered_candidate": (source, bridge, target),
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": +1},
        **metadata,
    }


def map_chord(chord: Chord, mapping: Mapping[int, int]) -> Chord:
    return tuple(mapping[int(node)] for node in chord)  # type: ignore[return-value]


def transported_distribution(
    distribution: Mapping[Chord, float],
    mapping: Mapping[int, int],
) -> Dict[Chord, float]:
    return {map_chord(chord, mapping): float(probability) for chord, probability in distribution.items()}


def distribution_max_error(left: Mapping[Chord, float], right: Mapping[Chord, float]) -> float:
    keys = set(left).union(right)
    return max((abs(float(left.get(key, 0.0)) - float(right.get(key, 0.0))) for key in keys), default=0.0)


def context_rows(base_states: Mapping[int, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        state = base_states[growth_seed]
        for placement in PLACEMENTS:
            distribution, scope, token_id = chord_distribution(state, placement)
            legacy = v08b.find_chord_candidate(state, center_token_index=placement)
            sampled = [sample_uniform_chord_candidate(state, placement, random.Random(seed))[0] for seed in SAMPLE_SEEDS]
            endpoint_degree_sums = [state.g.degree(source) + state.g.degree(target) for source, _, target in distribution]
            bridge_degrees = [state.g.degree(bridge) for _, bridge, _ in distribution]
            rows.append(
                {
                    "target_nodes": TARGET_NODES,
                    "growth_seed": growth_seed,
                    "placement": placement,
                    "selected_token_id": token_id,
                    "selected_token_node": int(state.token_pos[token_id]),
                    "candidate_scope": scope,
                    "candidate_count": len(distribution),
                    "candidate_entropy_bits": math.log2(len(distribution)),
                    "legacy_candidate": v15du.candidate_text(legacy),
                    "legacy_candidate_in_distribution": int(legacy in distribution),
                    "sampled_unique_candidate_count": len(set(sampled)),
                    "sampled_candidate_fraction": safe_div(len(set(sampled)), len(distribution)),
                    "min_endpoint_degree_sum": min(endpoint_degree_sums),
                    "median_endpoint_degree_sum": median_defined(endpoint_degree_sums),
                    "max_endpoint_degree_sum": max(endpoint_degree_sums),
                    "min_bridge_degree": min(bridge_degrees),
                    "median_bridge_degree": median_defined(bridge_degrees),
                    "max_bridge_degree": max(bridge_degrees),
                }
            )
    return rows


def relabel_trial_rows(base_states: Mapping[int, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        state = base_states[growth_seed]
        for placement in PLACEMENTS:
            original_distribution, original_scope, token_id = chord_distribution(state, placement)
            for relabel_seed in RELABEL_SEEDS:
                mapping = v15du.relabel_mapping(
                    state.g.nodes(),
                    growth_seed * 100_000 + placement * 1_000 + relabel_seed,
                )
                relabelled = v15du.relabel_state(state, mapping)
                relabelled_distribution, relabelled_scope, relabelled_token_id = chord_distribution(relabelled, placement)
                transported = transported_distribution(original_distribution, mapping)
                max_error = distribution_max_error(transported, relabelled_distribution)
                rows.append(
                    {
                        "target_nodes": TARGET_NODES,
                        "growth_seed": growth_seed,
                        "placement": placement,
                        "relabel_seed": relabel_seed,
                        "selected_token_id": token_id,
                        "relabelled_selected_token_id": relabelled_token_id,
                        "candidate_scope": original_scope,
                        "relabelled_candidate_scope": relabelled_scope,
                        "candidate_count": len(original_distribution),
                        "relabelled_candidate_count": len(relabelled_distribution),
                        "transported_candidate_set_equal": int(set(transported) == set(relabelled_distribution)),
                        "candidate_probability_max_error": max_error,
                        "distributionally_relabel_equivariant": int(max_error <= TOLERANCE),
                    }
                )
    return rows


def summary_rows(contexts: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_placement: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in contexts:
        by_placement[safe_int(row["placement"])].append(row)
    out: List[Dict[str, Any]] = []
    for placement, rows in sorted(by_placement.items()):
        out.append(
            {
                "placement": placement,
                "n_growth_seeds": len(rows),
                "selected_token_root_fraction": mean_defined(int(row["candidate_scope"] == "selected_token_root") for row in rows),
                "min_candidate_count": min(safe_int(row["candidate_count"]) for row in rows),
                "median_candidate_count": median_defined(row["candidate_count"] for row in rows),
                "max_candidate_count": max(safe_int(row["candidate_count"]) for row in rows),
                "legacy_candidate_coverage": mean_defined(row["legacy_candidate_in_distribution"] for row in rows),
                "median_candidate_entropy_bits": median_defined(row["candidate_entropy_bits"] for row in rows),
                "median_sampled_candidate_fraction": median_defined(row["sampled_candidate_fraction"] for row in rows),
            }
        )
    return out


def evaluation_rows(
    trials: Sequence[Mapping[str, Any]],
    contexts: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    covariance_rate = mean_defined(row["distributionally_relabel_equivariant"] for row in trials)
    candidate_set_rate = mean_defined(row["transported_candidate_set_equal"] for row in trials)
    selected_root_rate = mean_defined(int(row["candidate_scope"] == "selected_token_root") for row in contexts)
    legacy_coverage = mean_defined(row["legacy_candidate_in_distribution"] for row in contexts)
    if covariance_rate == 1.0 and candidate_set_rate == 1.0:
        diagnosis = "distributionally_relabel_invariant_constructor_ready"
        next_step = "small_constructor_by_coupling_factorial_holdout"
    else:
        diagnosis = "constructor_distributional_covariance_failed"
        next_step = "fix_candidate_enumeration_before_new_dynamics"
    return [
        {
            "key": "scope",
            "value": "no_new_dynamics_constructor_instrumentation",
            "evidence": f"growth_seeds={len(GROWTH_SEEDS)}; placements={len(PLACEMENTS)}; relabel_trials={len(trials)}",
        },
        {
            "key": "distributional_relabel_equivariance",
            "value": fmt(covariance_rate),
            "evidence": f"candidate probability tolerance={TOLERANCE:.1e}",
        },
        {
            "key": "transported_candidate_set_equality",
            "value": fmt(candidate_set_rate),
            "evidence": "all transported valid chords must equal the relabelled valid-chord set",
        },
        {
            "key": "selected_token_root_coverage",
            "value": fmt(selected_root_rate),
            "evidence": "fallback is reported, not hidden",
        },
        {
            "key": "legacy_candidate_coverage",
            "value": fmt(legacy_coverage),
            "evidence": "legacy first-sorted candidate is contained in the uniform candidate distribution",
        },
        {
            "key": "diagnosis",
            "value": diagnosis,
            "evidence": "instrumentation readiness only; no dynamic effect has been measured",
        },
        {
            "key": "next_step",
            "value": next_step,
            "evidence": "factor constructor policy and stochastic coupling before interpreting damage observables",
        },
    ]


def render_report(
    *,
    summaries: Sequence[Mapping[str, Any]],
    evaluation: Sequence[Mapping[str, Any]],
) -> str:
    by_key = {str(row["key"]): row for row in evaluation}
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dv: relabel-invariant chord-constructor")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er instrumenteringssteget som v15du krevde. Ingen ny defect-dynamikk kjoeres.")
    lines.append("Legacy `add_chord` endres ikke; tidligere resultater forblir reproducerbare. Den nye helperen definerer en uniform sannsynlighetsfordeling over alle gyldige token-rooted lokale chords.")
    lines.append("")
    lines.append("Symmetrien som kreves er distributional covariance:")
    lines.append("")
    lines.append("`P(phi(c) | phi(G), p) = P(c | G, p)`")
    lines.append("")
    lines.append("for enhver node-ommerking `phi`, candidate chord `c` og placement `p`. Samme RNG-tall trenger ikke gi pathwise transport etter at list order endres.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- target: `{TARGET_NODES}`")
    lines.append(f"- growth seeds: `{';'.join(str(seed) for seed in GROWTH_SEEDS)}`")
    lines.append(f"- placements: `{';'.join(f'p{placement}' for placement in PLACEMENTS)}`")
    lines.append(f"- relabel trials: `{len(GROWTH_SEEDS) * len(PLACEMENTS) * len(RELABEL_SEEDS)}`")
    lines.append("- primary gate: exact transported candidate-set equality and probability max error <= `1e-12`")
    lines.append("")
    lines.append("## Candidate landscape")
    lines.append("")
    lines.extend(
        table(
            summaries,
            (
                "placement",
                "n_growth_seeds",
                "selected_token_root_fraction",
                "min_candidate_count",
                "median_candidate_count",
                "max_candidate_count",
                "legacy_candidate_coverage",
                "median_candidate_entropy_bits",
            ),
        )
    )
    lines.append("")
    lines.append("Candidate-count og entropy viser hvor mye skjult constructor-valg legacy first-sorted policy kollapset til ett punkt. Dette er generatorhygiene, ikke fysikk.")
    lines.append("")
    lines.append("## Evaluation")
    lines.append("")
    lines.extend(table(evaluation[1:], ("key", "value", "evidence")))
    lines.append("")
    lines.append("## Beslutning")
    lines.append("")
    lines.append(f"- diagnosis: `{by_key['diagnosis']['value']}`")
    lines.append(f"- next_step: `{by_key['next_step']['value']}`")
    lines.append("- claim ceiling: `distributionally relabel-invariant perturbation instrumentation`")
    lines.append("")
    lines.append("Den neste dynamiske testen boer vaere en liten `constructor x coupling`-faktorial:")
    lines.append("")
    lines.append("- constructor: legacy first-sorted vs uniform relabel-invariant")
    lines.append("- coupling: maximal vs rank")
    lines.append("- primary products: marginal branch-observables og continuous horizon, ikke bare coarse active labels")
    lines.append("- stopp hvis constructor eller coupling endrer majority outcome systematisk")
    lines.append("")
    lines.append("Selv full stabilitet i en slik faktorial oppgraderer bare det lokale response-signalet. Lorentz, global invariant, universality og en universe-builder claim krever senere, separate gater.")
    lines.append("")
    return "\n".join(lines)


def render_operational(evaluation: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): row for row in evaluation}
    return "\n".join(
        [
            "# Operativ anbefaling v0.15dv",
            "",
            f"- `distributional_relabel_equivariance`: `{by_key['distributional_relabel_equivariance']['value']}`.",
            f"- `transported_candidate_set_equality`: `{by_key['transported_candidate_set_equality']['value']}`.",
            f"- `selected_token_root_coverage`: `{by_key['selected_token_root_coverage']['value']}`.",
            f"- `diagnosis`: `{by_key['diagnosis']['value']}`.",
            f"- `next_step`: `{by_key['next_step']['value']}`.",
            "",
            "Legacy constructor beholdes som historisk kontroll, ikke som standard for nye symmetry-sensitive claims.",
            "Ingen dynamisk effekt er validert av denne instrumenteringsrunden.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-report", default=str(DOC / "v15dv_relabel_invariant_chord_constructor.md"))
    parser.add_argument("--out-context-csv", default=str(DOC / "v15dv_chord_candidate_contexts.csv"))
    parser.add_argument("--out-trials-csv", default=str(DOC / "v15dv_chord_distribution_relabel_trials.csv"))
    parser.add_argument("--out-summary-csv", default=str(DOC / "v15dv_chord_candidate_summary.csv"))
    parser.add_argument("--out-evaluation-csv", default=str(DOC / "v15dv_chord_constructor_evaluation.csv"))
    parser.add_argument("--out-operational", default=str(DOC / "v0_15dv_operativ_anbefaling.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_states = v15du.build_bases()
    contexts = context_rows(base_states)
    trials = relabel_trial_rows(base_states)
    summaries = summary_rows(contexts)
    evaluation = evaluation_rows(trials, contexts)

    write_csv(args.out_context_csv, contexts)
    write_csv(args.out_trials_csv, trials)
    write_csv(args.out_summary_csv, summaries)
    write_csv(args.out_evaluation_csv, evaluation)
    Path(args.out_report).write_text(render_report(summaries=summaries, evaluation=evaluation), encoding="utf-8")
    Path(args.out_operational).write_text(render_operational(evaluation), encoding="utf-8")

    for row in evaluation:
        print(f"{row['key']}: {row['value']} ({row['evidence']})")


if __name__ == "__main__":
    main()
