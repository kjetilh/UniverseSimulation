#!/usr/bin/env python3
"""v0.15co configuration heuristic assessment.

This is not a new dynamical lab. It is a repo-grounded decision layer that asks:

can physics-inspired desiderata such as Lorentz-likeness, quasi-invariants,
global rules, and entanglement be translated into practical heuristics for
choosing the next configurations?

The answer is intentionally conservative. These words are allowed to guide
search only after being translated into local observables already present in
the repo. The script writes explicit CSV and Markdown artifacts so later labs
can use the heuristic without quietly upgrading analogies into evidence.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


DOC_DIR = Path("Documentation")

REPORT_PATH = DOC_DIR / "v15co_configuration_heuristic_assessment.md"
AXES_PATH = DOC_DIR / "v15co_configuration_heuristic_axes.csv"
RULES_PATH = DOC_DIR / "v15co_configuration_candidate_rules.csv"
DECISION_PATH = DOC_DIR / "v15co_configuration_decision_table.csv"
ANCHORS_PATH = DOC_DIR / "v15co_configuration_physics_anchor_notes.csv"
OPERATIVE_PATH = DOC_DIR / "v0_15co_operativ_anbefaling.md"
NON_SPECIALIST_PATH = DOC_DIR / "relasjonell_universgraf_for_ikke_spesialister_v0_15co.md"


REQUIRED_EVIDENCE_FILES = [
    "Documentation/v11e_band_vs_bridge0075.md",
    "Documentation/v12_geometry_invariant_lab.md",
    "Documentation/v14_lorentz_diagnostics.md",
    "Documentation/v14b_lorentz_placement_diagnostics.md",
    "Documentation/v14c_local_isotropy_diagnostics.md",
    "Documentation/v15b_add_chord_collision_lab.md",
    "Documentation/v15g_collision_genealogy_lab.md",
    "Documentation/v15bl_conditional_quasi_invariant_lab.md",
    "Documentation/v15cl_target768_inner_gate_global_budget_lab.md",
    "Documentation/v15cm_target768_local_trigger_lab.md",
    "Documentation/v15cn_p2_horizon_scale_holdout_lab.md",
    "Documentation/v0_15cn_operativ_anbefaling.md",
]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def md_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def require_evidence_files() -> None:
    missing = [path for path in REQUIRED_EVIDENCE_FILES if not Path(path).exists()]
    if missing:
        formatted = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(f"Missing required evidence files:\n{formatted}")


def physics_anchor_notes() -> List[Dict[str, Any]]:
    return [
        {
            "anchor": "Relativity / Lorentz-like behavior",
            "external_source": "Einstein 1905, On the Electrodynamics of Moving Bodies",
            "url": "https://en.wikisource.org/wiki/On_the_Electrodynamics_of_Moving_Bodies_(1920_edition)",
            "usable_repo_translation": "frame/mode/placement robustness of propagation observables",
            "strict_caveat": "repo does not have coordinates, clocks, metric tensor, or demonstrated invariant signal speed",
        },
        {
            "anchor": "Symmetry -> conservation / invariant laws",
            "external_source": "Noether 1918, Invariante Variationsprobleme",
            "url": "https://eudml.org/doc/59024",
            "usable_repo_translation": "look for quantities with low drift that also predict or compress dynamics across families",
            "strict_caveat": "zero drift in nodes/beta1 is not a law unless it survives off-regime and has a derivation",
        },
        {
            "anchor": "Gauge/symmetry interpretation of conservation",
            "external_source": "Stanford Encyclopedia of Philosophy, Gauge Theories in Physics, section on Noether theorem",
            "url": "https://plato.stanford.edu/entries/gauge-theories/",
            "usable_repo_translation": "treat invariance claims as requiring both formal structure and empirical/dynamical relevance",
            "strict_caveat": "current repo has graph dynamics, not a Lagrangian field theory",
        },
        {
            "anchor": "Entanglement / nonseparability",
            "external_source": "Bell 1964, On the Einstein Podolsky Rosen paradox",
            "url": "https://journals.aps.org/ppf/abstract/10.1103/PhysicsPhysiqueFizika.1.195",
            "usable_repo_translation": "only a weak proxy is available: non-superposition of paired local defects versus matched single controls",
            "strict_caveat": "collision non-superposition is not quantum entanglement; there is no Bell test, Hilbert space, or measurement-setting formalism here",
        },
    ]


def heuristic_axes() -> List[Dict[str, Any]]:
    return [
        {
            "axis_id": "A0_artifact_hygiene",
            "physics_inspiration": "none; experimental hygiene",
            "repo_proxy": "separated start sizes, requested perturbation matching, clean controls/order checks",
            "current_status": "mandatory_clean_gate",
            "selector_role": "hard_gate",
            "priority": "must_pass",
            "confidence": "high",
            "evidence_files": "v11e, v14, v15b, v15bl, v15cn",
            "allowed_decision_use": "reject candidates that fail hygiene before interpreting any physics-like signal",
            "do_not_read_as": "positive physics evidence",
        },
        {
            "axis_id": "A1_defect_nonseparability",
            "physics_inspiration": "interaction / nonseparability, not entanglement",
            "repo_proxy": "pair-run damage not equal to union of matched single-run controls; genealogy event chains",
            "current_status": "strongest_active_signal_but_mesoscale",
            "selector_role": "positive_search_axis",
            "priority": "high",
            "confidence": "medium_high",
            "evidence_files": "v15b, v15g, later v15 defect chain",
            "allowed_decision_use": "prefer configurations where local defects persist and interact nontrivially under matched controls",
            "do_not_read_as": "particles, quantum entanglement, or universal field interaction",
        },
        {
            "axis_id": "A2_conditional_quasi_invariant",
            "physics_inspiration": "invariants / conserved quantities",
            "repo_proxy": "low relative drift of non-trivial metrics after conditioning on carrier/family",
            "current_status": "weak_to_moderate_positive_selector",
            "selector_role": "secondary_positive_axis",
            "priority": "medium",
            "confidence": "medium",
            "evidence_files": "v12, v13b-v13n, v15bl",
            "allowed_decision_use": "prefer followups where spectral drift remains low after family conditioning and helps compress outcomes",
            "do_not_read_as": "global law or Noether-style conservation",
        },
        {
            "axis_id": "A3_lorentz_like",
            "physics_inspiration": "Lorentz invariance / relativity",
            "repo_proxy": "mode- and placement-robust propagation/front-speed diagnostics with clean controls",
            "current_status": "not_yet",
            "selector_role": "negative_filter_or_diagnostic_only",
            "priority": "medium_low",
            "confidence": "medium_high_negative",
            "evidence_files": "v14, v14b, v14c",
            "allowed_decision_use": "penalize candidates whose signals are dominated by mode/placement sensitivity; do not select positives from Lorentz score alone",
            "do_not_read_as": "spacetime, universal light cone, or metric emergence",
        },
        {
            "axis_id": "A4_global_rules",
            "physics_inspiration": "global constraints / conservation-like regulation",
            "repo_proxy": "budget coupling, shell redistribution, stability of global quantities under local perturbations",
            "current_status": "not_yet",
            "selector_role": "instrumentation_axis",
            "priority": "medium_low",
            "confidence": "medium_negative",
            "evidence_files": "v15cl, v15cm, v15cn",
            "allowed_decision_use": "track as diagnostics while testing scale/budget; do not use as positive selector yet",
            "do_not_read_as": "global invariant or law",
        },
        {
            "axis_id": "A5_scale_robustness",
            "physics_inspiration": "universality / continuum-ish robustness",
            "repo_proxy": "same qualitative observable survives target scale changes under appropriate budget normalization",
            "current_status": "unresolved_budget_caveat",
            "selector_role": "holdout_gate",
            "priority": "high_for_claims",
            "confidence": "medium",
            "evidence_files": "v15cn",
            "allowed_decision_use": "keep target-768 p2 as live but require budget-scaled 1024 or intermediate scale before stronger claims",
            "do_not_read_as": "failure of all scale behavior, because v15cn used same absolute budget",
        },
        {
            "axis_id": "A6_local_isotropy_geometry",
            "physics_inspiration": "spatial isotropy / emergent geometry",
            "repo_proxy": "placement variation explained by local support geometry or disappears under controls",
            "current_status": "not_explained",
            "selector_role": "risk_penalty",
            "priority": "medium",
            "confidence": "medium",
            "evidence_files": "v14b, v14c",
            "allowed_decision_use": "prefer candidates whose signal is not only a hidden placement artifact",
            "do_not_read_as": "isotropic geometry",
        },
    ]


def candidate_rules() -> List[Dict[str, Any]]:
    return [
        {
            "rule_id": "R0",
            "rule_name": "hygiene_before_physics",
            "rule_type": "hard_gate",
            "if_condition": "start sizes not separated, requested perturbation mismatch, dirty controls, or unexplained order effects",
            "then_decision": "reject or rerun before interpretation",
            "reason": "generator/scoring artifacts can mimic every higher-level property",
            "evidence_basis": "general project rule plus v11e/v14/v15 controls",
        },
        {
            "rule_id": "R1",
            "rule_name": "nonseparability_is_search_signal",
            "rule_type": "positive_prioritization",
            "if_condition": "local defect persistence plus pair-vs-single non-superposition under matched controls",
            "then_decision": "prioritize as defect/interaction candidate",
            "reason": "this is the clearest current local interaction signal",
            "evidence_basis": "v15b, v15g",
        },
        {
            "rule_id": "R2",
            "rule_name": "conditioned_invariant_before_global_invariant",
            "rule_type": "positive_but_capped",
            "if_condition": "non-trivial drift metric is low only inside a family/carrier condition",
            "then_decision": "use as local carrier heuristic; require cross-family and scale holdout before law language",
            "reason": "v15bl shows sharpening after conditioning, not a global invariant",
            "evidence_basis": "v12, v15bl",
        },
        {
            "rule_id": "R3",
            "rule_name": "lorentz_not_positive_selector_yet",
            "rule_type": "negative_filter",
            "if_condition": "front-speed/propagation differs by perturbation mode or placement",
            "then_decision": "do not upgrade to Lorentz-like; use as anisotropy diagnostic",
            "reason": "v14-v14c keep Lorentz in not_yet state",
            "evidence_basis": "v14, v14b, v14c",
        },
        {
            "rule_id": "R4",
            "rule_name": "global_rule_language_requires_derivation_or_holdout",
            "rule_type": "language_guardrail",
            "if_condition": "global budget or zero-drift metric looks stable without derivation and off-regime support",
            "then_decision": "report as diagnostic or sanity metric only",
            "reason": "v13b broke some zero-drift readings; v15cl did not support global-budget explanation",
            "evidence_basis": "v13b, v15cl",
        },
        {
            "rule_id": "R5",
            "rule_name": "scale_before_universe_like_claim",
            "rule_type": "claim_gate",
            "if_condition": "signal is target-specific under same absolute budget",
            "then_decision": "keep as live pocket but run budget-scaled or intermediate-scale holdout before stronger interpretation",
            "reason": "v15cn keeps target-768 alive but target-1024 unsupported under same absolute budget",
            "evidence_basis": "v15cn",
        },
    ]


def decision_table() -> List[Dict[str, Any]]:
    return [
        {
            "candidate_direction": "target768_p2_horizon_local_swap",
            "artifact_gate": "pass_existing",
            "defect_nonseparability": "promising_indirect",
            "conditional_quasi_invariant": "possibly_relevant",
            "lorentz_like": "not_claimed",
            "global_rules": "not_supported",
            "scale_status": "live_but_target_specific_under_current_budget",
            "decision": "retain_as_contrast_anchor_not_final_target",
            "next_use": "compare against target1024 scaled-budget or intermediate target",
        },
        {
            "candidate_direction": "target768_p2_horizon_add_chord",
            "artifact_gate": "pass_existing",
            "defect_nonseparability": "strong_historical_family",
            "conditional_quasi_invariant": "cycle_band_p2_spectral_sharpening",
            "lorentz_like": "not_claimed",
            "global_rules": "not_supported",
            "scale_status": "weaker_than_local_swap_at_768_and_not_supported_at_1024",
            "decision": "retain_as_carrier_contrast",
            "next_use": "do not overfit; use beside local_swap to test carrier dependence",
        },
        {
            "candidate_direction": "target1024_p2_same_absolute_budget",
            "artifact_gate": "pass_existing",
            "defect_nonseparability": "not_established_in_this_observable",
            "conditional_quasi_invariant": "not_tested_here",
            "lorentz_like": "not_claimed",
            "global_rules": "not_supported",
            "scale_status": "negative_under_same_absolute_budget",
            "decision": "do_not_discard_until_budget_scaled",
            "next_use": "run scaled-budget 1024 or one intermediate scale",
        },
        {
            "candidate_direction": "lorentz_front_speed_as_selector",
            "artifact_gate": "controls_partly_clean",
            "defect_nonseparability": "orthogonal",
            "conditional_quasi_invariant": "orthogonal",
            "lorentz_like": "not_yet_mode_and_placement_sensitive",
            "global_rules": "not_relevant",
            "scale_status": "not_primary",
            "decision": "do_not_use_as_positive_selector",
            "next_use": "keep as diagnostic after stronger mesoscale signal appears",
        },
        {
            "candidate_direction": "entanglement_like_wording",
            "artifact_gate": "not_a_repo_observable",
            "defect_nonseparability": "weak_proxy_only",
            "conditional_quasi_invariant": "not_sufficient",
            "lorentz_like": "not_sufficient",
            "global_rules": "not_sufficient",
            "scale_status": "not_sufficient",
            "decision": "forbidden_as_claim",
            "next_use": "rename to pair_non_superposition unless a formal Bell-like measurement framework exists",
        },
    ]


def report_markdown(
    axes: Sequence[Mapping[str, Any]],
    rules: Sequence[Mapping[str, Any]],
    decisions: Sequence[Mapping[str, Any]],
    anchors: Sequence[Mapping[str, Any]],
) -> str:
    return f"""# Relasjonell universgraf v0.15co: configuration heuristic assessment

## Formal

Denne runden kjorer ingen ny universdynamikk. Den svarer paa et metodisk spoersmaal:

Kan egenskaper vi kjenner fra vaart univers, som Lorentz-likhet, invarianter, globale regler og entanglement, brukes som heuristikk for valg av konfigurasjoner i repoet?

Kort svar: ja, men bare som en svak og falsifiserbar prioriteringsheuristikk etter oversettelse til repo-observabler. Ordene kan ikke brukes direkte som konklusjoner.

## Verified current state

- `band_zero_del` er fortsatt arbeidsregime fra `v11e`; dette er regimevalg, ikke fysikkbevis.
- Lorentz-/spacetime-sporet er fortsatt `not_yet`: `v14`, `v14b` og `v14c` viser rene nok kontroller til aa ta signalet alvorlig, men fortsatt mode-dependence, placement-sensitivity og uavklart lokal anisotropi.
- Defect-/interaction-sporet er fortsatt den sterkeste positive retningen: `v15b` viser ikke-triviell pair-vs-single non-superposition, og `v15g` viser delvis strukturerte genealogy/event-chain-moenstre.
- Quasi-invariant-sporet er interessant, men betinget: `v12`/`v13` peker paa spektral relativ drift som beste ikke-trivielle kandidat, mens `v15bl` skjerper dette etter carrier/family-conditioning. Dette er ikke en global lov.
- Global-budget/global-regel-spraak skal holdes nede: `v15cl` finner ikke ren inner-gate eller global-budget-kobling.
- Skala er fortsatt en hard sperre for store paastander: `v15cn` holder target-768 p2-lommen live, men target 1024 stoetter ikke p2 under samme absolute step budget.

## Heuristic axes

{md_table(axes, ["axis_id", "current_status", "selector_role", "priority", "confidence"])}

## Candidate rules

{md_table(rules, ["rule_id", "rule_name", "rule_type", "then_decision"])}

## Decision table

{md_table(decisions, ["candidate_direction", "decision", "next_use"])}

## Physics anchors and repo translations

{md_table(anchors, ["anchor", "external_source", "url", "usable_repo_translation", "strict_caveat"])}

## Interpretation

Det er mulig aa lage en heuristikk, men bare hvis vi skiller mellom inspirasjon og evidens:

- Lorentz-likhet er forelopig en negativ filter-/diagnostikkakse, ikke en positiv selector.
- Invariant-spraak er forelopig en conditional quasi-invariant-akse: spektral drift kan prioritere carrier/family-runder, men ikke etablere globale lover.
- Globale regler maa behandles som instrumentering, ikke som konklusjon, inntil en observabel overlever skala, carrier og kontrollfamilier.
- Entanglement er ikke en tillatt paastand i dagens repo. Den naermeste repo-lokale proxyen er pair non-superposition under matched single controls.
- Defect non-superposition og genealogy er den beste positive signalaksen akkurat naa, men den sier "real mesoscale interaction", ikke "partikkel".

## Next natural step

Neste dynamiske steg boer vaere en liten scale/budget-runde, ikke et nytt bredt soek:

`target1024_scaled_budget_p2_horizon` eller ett mellomtarget mellom `768` og `1024`.

Grunnen er at `v15cn` gir den viktigste claim-gaten: hvis p2 bare finnes ved target 768 under dagens absolutte budsjett, kan vi ikke bruke den som universe-like selector. Hvis den kommer tilbake ved skalanormalisert budsjett eller mellomskala, blir p2-lommen mye mer interessant som testbenk for conditional quasi-invariant og defect-interaction observabler.

## Evidence discipline

Denne rapporten introduserer ingen nye runtime-resultater. CSV-ene er syntese-/beslutningstabeller basert paa eksisterende repo-filer og eksterne begrepsankere. De skal ikke leses som maalinger fra en ny simulering.
"""


def operative_markdown() -> str:
    return """# Operativ anbefaling v0.15co

- `configuration_heuristic`: `possible_but_weak` fordi univers-inspirerte egenskaper kan oversettes til repo-observabler, men bare som falsifiserbare prioriteringsregler.
- `hard_gate`: `artifact_hygiene_first` fordi startstorrelse, requested perturbation, controls og order-sensitivitet maa vaere rene foer noen fysikk-lignende lesning.
- `best_positive_axis`: `defect_nonseparability_and_genealogy` fordi pair-vs-single non-superposition og event-chain observabler er sterkere repo-signaler enn Lorentz-/global-rule-sporet akkurat naa.
- `conditional_invariant_axis`: `spectral_candidate_capped` fordi spektral relativ drift er interessant etter conditioning, men fortsatt ikke global invariant.
- `lorentz_axis`: `diagnostic_only_not_selector` fordi Lorentz-sporet fortsatt er mode-/placement-sensitivt og lokal anisotropi ikke er ryddet bort.
- `entanglement_axis`: `proxy_only` fordi repoet bare har pair non-superposition, ikke Bell-/Hilbert-/measurement-formalisme.
- `scale_gate`: `target1024_budget_extension_or_intermediate_scale` fordi v15cn holder target-768 p2 live, men target 1024 stoetter ikke p2 under samme absolute budsjett.
- `next_step`: `target1024_scaled_budget_p2_horizon_or_intermediate_target` fordi dette er den minste testen som kan avgjoere om p2-lommen er en target-768/budget-lomme eller en bedre konfigurasjonsselector.

- Ikke bruk denne runden som fysikkpaastand. Den er en beslutningspolicy for hva som boer testes videre.
"""


def non_specialist_markdown() -> str:
    return """# Relasjonell universgraf v0.15co for ikke-spesialister

Denne runden handler ikke om aa finne en ny effekt i simulasjonen. Den handler om aa velge bedre hva vi skal lete etter.

Sporsmaalet var: kan vi bruke ting vi kjenner fra fysisk virkelighet som peilemerker? For eksempel at lover ofte henger sammen med symmetrier, at relativitet krever robuste signaler uavhengig av observasjonsmaate, og at kvantefysikk har ikke-separerbare sammenhenger.

Svaret er ja, men med en streng begrensning: ordene fra fysikk kan bare brukes som inspirasjon. For aa telle i dette prosjektet maa de oversettes til noe vi faktisk kan maale i grafdynamikken.

Den beste positive retningen akkurat naa er ikke Lorentz-likhet. Det er lokale defects som varer lenge og som interagerer paa en maate som ikke bare er summen av to separate defects. Det er interessant, men det er ikke det samme som partikler.

Invarianter er ogsaa interessante, spesielt spektrale maal som driver mindre enn andre maal innen visse familier. Men de er forelopig betingede og lokale. Det er for tidlig aa kalle dem lover.

Lorentz-likhet er forelopig mest nyttig som en test vi ikke bestaar: hvis et signal endrer seg mye med perturbasjonstype eller plassering, skal vi ikke kalle det spacetime-likt.

Neste riktige steg er derfor aa teste skala og budsjett. Vi har en lovende p2-lomme ved target 768, men den dukket ikke opp ved target 1024 med samme tidsbudsjett. Det kan bety at effekten er lokal for 768, eller bare at 1024 trenger mer tid. Det maa avklares foer vi kan bruke denne lommen som et godt kompass videre.
"""


def run() -> Dict[str, Path]:
    require_evidence_files()
    anchors = physics_anchor_notes()
    axes = heuristic_axes()
    rules = candidate_rules()
    decisions = decision_table()

    write_csv(ANCHORS_PATH, anchors)
    write_csv(AXES_PATH, axes)
    write_csv(RULES_PATH, rules)
    write_csv(DECISION_PATH, decisions)

    REPORT_PATH.write_text(report_markdown(axes, rules, decisions, anchors), encoding="utf-8")
    OPERATIVE_PATH.write_text(operative_markdown(), encoding="utf-8")
    NON_SPECIALIST_PATH.write_text(non_specialist_markdown(), encoding="utf-8")

    return {
        "report": REPORT_PATH,
        "axes": AXES_PATH,
        "rules": RULES_PATH,
        "decision": DECISION_PATH,
        "anchors": ANCHORS_PATH,
        "operative": OPERATIVE_PATH,
        "non_specialist": NON_SPECIALIST_PATH,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="validate evidence files without writing outputs")
    args = parser.parse_args()

    require_evidence_files()
    if args.dry_run:
        print("v15co evidence files present; dry run wrote nothing.")
        return

    outputs = run()
    for key, path in outputs.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
