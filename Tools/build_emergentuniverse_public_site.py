#!/usr/bin/env python3
"""Build the public Emergent Universe static site bundle.

The bundle is intentionally static: it publishes scientific-style summaries and
downloadable evidence artifacts without exposing the local RAG service or admin
endpoints. The RAG corpus docs are included as public documentation, while the
dynamic RAG service remains a separate internal tool until it is hardened.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[1]


DATASET_SPECS: list[dict[str, str]] = [
    {
        "source": "PROJECT_CONTEXT_LIVE.md",
        "category": "project_context",
        "title": "Live project context",
        "description": "Current repo-loyal context and working conclusions.",
    },
    {
        "source": "PROJECT_HISTORY_INDEX.md",
        "category": "project_context",
        "title": "Project history index",
        "description": "Chronological index of experiment rounds and conclusions.",
    },
    {
        "source": "Documentation/EmergentUniverse_Public_Site_Runbook.md",
        "category": "project_context",
        "title": "Public site runbook",
        "description": "Build, deployment, verification, and RAG exposure boundary for the public site.",
    },
    {
        "source": "Documentation/grundig-research-rapport-16.md",
        "category": "theory",
        "title": "Formal research report",
        "description": "Conceptual and mathematical project report.",
    },
    {
        "source": "rag_service/docs/UNIVERSE_RAG_STATUS.md",
        "category": "rag_corpus",
        "title": "RAG status",
        "description": "Status of the project-specific RAG service and corpus.",
    },
    {
        "source": "rag_service/docs/RAG_SERVICE_API.md",
        "category": "rag_corpus",
        "title": "RAG service API and hardening",
        "description": "Research API, auth, rate-limit, citation-audit, and freshness-hardening notes.",
    },
    {
        "source": "rag_service/docs/UNIVERSE_ARGUMENTATION_MAP.md",
        "category": "rag_corpus",
        "title": "Argumentation map",
        "description": "Evidence-level map used to separate formalism, code, data and inference.",
    },
    {
        "source": "rag_service/docs/UNIVERSE_CORPUS_PLAN.md",
        "category": "rag_corpus",
        "title": "Corpus plan",
        "description": "RAG source-type and case plan.",
    },
    {
        "source": "rag_service/docs/UNIVERSE_TOOL_RUNBOOK.md",
        "category": "rag_corpus",
        "title": "Tool runbook",
        "description": "Operational notes for the simulator/RAG workflow.",
    },
    {
        "source": "rag_service/docs/UNIVERSE_DEEP_RESEARCH_PROMPT.md",
        "category": "rag_corpus",
        "title": "Deep research prompt",
        "description": "Model prompt for source-grounded project research.",
    },
    {
        "source": "Documentation/v11e_band_vs_bridge0075.md",
        "category": "frontier_regime",
        "title": "v11e operational regime report",
        "description": "Frontier duel establishing band_zero_del as operational regime.",
    },
    {
        "source": "Documentation/v11e_band_vs_bridge0075_candidate_summary.csv",
        "category": "frontier_regime",
        "title": "v11e candidate summary",
        "description": "Candidate-level score summary.",
    },
    {
        "source": "Documentation/v11e_band_vs_bridge0075_pairwise.csv",
        "category": "frontier_regime",
        "title": "v11e pairwise comparison",
        "description": "Pairwise comparison evidence for the operational regime.",
    },
    {
        "source": "Documentation/v11e_band_vs_bridge0075_verdict.csv",
        "category": "frontier_regime",
        "title": "v11e verdict",
        "description": "Machine-readable final verdict rows.",
    },
    {
        "source": "Documentation/v14_lorentz_diagnostics.md",
        "category": "lorentz_diagnostics",
        "title": "v14 Lorentz diagnostics",
        "description": "Lorentz-like propagation diagnostics and artifact controls.",
    },
    {
        "source": "Documentation/v14_lorentz_artifact_checks.csv",
        "category": "lorentz_diagnostics",
        "title": "v14 artifact checks",
        "description": "Artifact-control table for Lorentz diagnostics.",
    },
    {
        "source": "Documentation/v14_lorentz_pairwise_perturbation_summary.csv",
        "category": "lorentz_diagnostics",
        "title": "v14 perturbation pairwise summary",
        "description": "Pairwise perturbation comparison rows.",
    },
    {
        "source": "Documentation/v14b_lorentz_placement_diagnostics.md",
        "category": "lorentz_diagnostics",
        "title": "v14b placement diagnostics",
        "description": "Placement sensitivity analysis.",
    },
    {
        "source": "Documentation/v14b_lorentz_mode_vs_placement_diagnosis.csv",
        "category": "lorentz_diagnostics",
        "title": "v14b mode-vs-placement diagnosis",
        "description": "Machine-readable mode/placement diagnosis.",
    },
    {
        "source": "Documentation/v14c_local_isotropy_diagnostics.md",
        "category": "lorentz_diagnostics",
        "title": "v14c local isotropy diagnostics",
        "description": "Local anisotropy alternative analysis.",
    },
    {
        "source": "Documentation/v14c_local_isotropy_feature_signal_summary.csv",
        "category": "lorentz_diagnostics",
        "title": "v14c feature signal summary",
        "description": "Local support-geometry feature signal summary.",
    },
    {
        "source": "Documentation/v15_defect_lifetime_lab.md",
        "category": "defect_track",
        "title": "v15 defect lifetime lab",
        "description": "Initial defect lifetime experiment.",
    },
    {
        "source": "Documentation/v15_defect_lifetime_aggregate.csv",
        "category": "defect_track",
        "title": "v15 defect lifetime aggregate",
        "description": "Aggregate defect lifetime rows.",
    },
    {
        "source": "Documentation/v15b_add_chord_collision_lab.md",
        "category": "defect_track",
        "title": "v15b add_chord collision lab",
        "description": "Matched-control collision interaction report.",
    },
    {
        "source": "Documentation/v15b_add_chord_collision_interactions.csv",
        "category": "defect_track",
        "title": "v15b collision interactions",
        "description": "Pair-run interaction table.",
    },
    {
        "source": "Documentation/v15g_collision_genealogy_lab.md",
        "category": "defect_track",
        "title": "v15g collision genealogy lab",
        "description": "Genealogy-first collision observable report.",
    },
    {
        "source": "Documentation/v15g_collision_genealogy_event_aggregate.csv",
        "category": "defect_track",
        "title": "v15g genealogy event aggregate",
        "description": "Aggregate genealogy event rows.",
    },
    {
        "source": "Documentation/v15q_single_defect_recurrence_lab.md",
        "category": "defect_track",
        "title": "v15q single defect recurrence lab",
        "description": "Single-defect recurrence report.",
    },
    {
        "source": "Documentation/v15q_single_defect_recurrence_aggregate.csv",
        "category": "defect_track",
        "title": "v15q single defect recurrence aggregate",
        "description": "Aggregate recurrence rows.",
    },
    {
        "source": "Documentation/v15dg_boundary_mass_holdout.md",
        "category": "active_set_landscape",
        "title": "v15dg boundary/mass holdout",
        "description": "Fresh boundary/mass holdout report.",
    },
    {
        "source": "Documentation/v15dg_boundary_mass_metric_scores.csv",
        "category": "active_set_landscape",
        "title": "v15dg boundary/mass metric scores",
        "description": "Metric score rows.",
    },
    {
        "source": "Documentation/v15dh_boundary_mass_growth_seed_holdout.md",
        "category": "active_set_landscape",
        "title": "v15dh growth-seed holdout",
        "description": "Boundary/mass transfer holdout report.",
    },
    {
        "source": "Documentation/v15di_growth_seed_signature_synthesis.md",
        "category": "active_set_landscape",
        "title": "v15di growth-seed signature synthesis",
        "description": "Growth-seed-conditioned landscape synthesis.",
    },
    {
        "source": "Documentation/v15di_growth_seed_outcome_matrix.csv",
        "category": "active_set_landscape",
        "title": "v15di outcome matrix",
        "description": "Outcome matrix by growth seed and placement.",
    },
    {
        "source": "Documentation/v15dl_base_landscape_morphology_synthesis.md",
        "category": "active_set_landscape",
        "title": "v15dl morphology synthesis",
        "description": "Base landscape and morphology synthesis.",
    },
    {
        "source": "Documentation/v15dm_frozen_return_probability_holdout.md",
        "category": "active_set_landscape",
        "title": "v15dm frozen return-probability holdout",
        "description": "Fresh holdout of a frozen return-probability scout.",
    },
    {
        "source": "Documentation/v15dn_multi_active_landscape_synthesis.md",
        "category": "active_set_landscape",
        "title": "v15dn multi-active landscape synthesis",
        "description": "Multi-active active-set framing.",
    },
    {
        "source": "Documentation/v15dn_multi_active_landscape_seed_summary.csv",
        "category": "active_set_landscape",
        "title": "v15dn seed summary",
        "description": "Seed-level active-set summary.",
    },
    {
        "source": "Documentation/v15do_active_set_type_discriminator_synthesis.md",
        "category": "active_set_landscape",
        "title": "v15do type discriminator synthesis",
        "description": "Post-hoc type-discriminator synthesis and underdetermination diagnosis.",
    },
    {
        "source": "Documentation/v15do_active_set_type_diagnosis.csv",
        "category": "active_set_landscape",
        "title": "v15do diagnosis",
        "description": "Machine-readable v15do diagnosis.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_holdout.md",
        "category": "latest_holdout",
        "title": "v15dp type-guard holdout",
        "description": "Fresh two-seed holdout of the frozen v15do guard.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_seed_evaluation.csv",
        "category": "latest_holdout",
        "title": "v15dp seed evaluation",
        "description": "Seed-level guard evaluation.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_evaluation.csv",
        "category": "latest_holdout",
        "title": "v15dp aggregate evaluation",
        "description": "Aggregate guard-evaluation rows.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_placement_summary.csv",
        "category": "latest_holdout",
        "title": "v15dp placement summary",
        "description": "Placement-level holdout outcomes.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_pre_run_guard.csv",
        "category": "latest_holdout",
        "title": "v15dp pre-run guard",
        "description": "Pre-registered guard rows written before dynamics.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_component_trajectories.csv",
        "category": "latest_holdout_raw",
        "title": "v15dp component trajectories",
        "description": "Full component trajectory log from the latest holdout.",
    },
    {
        "source": "Documentation/v15dp_active_set_type_guard_event_log.csv",
        "category": "latest_holdout_raw",
        "title": "v15dp event log",
        "description": "Full genealogy/event log from the latest holdout.",
    },
    {
        "source": "Documentation/v15dq_active_set_taxonomy_synthesis.md",
        "category": "latest_taxonomy",
        "title": "v15dq taxonomy synthesis",
        "description": "No-new-dynamics active-set taxonomy synthesis.",
    },
    {
        "source": "Documentation/v15dq_active_set_taxonomy_seed_summary.csv",
        "category": "latest_taxonomy",
        "title": "v15dq seed summary",
        "description": "Seed-level taxonomy table.",
    },
    {
        "source": "Documentation/v15dq_active_set_taxonomy_class_summary.csv",
        "category": "latest_taxonomy",
        "title": "v15dq class summary",
        "description": "Class-level active-set taxonomy summary.",
    },
    {
        "source": "Documentation/v15dq_active_set_taxonomy_pairwise_type_contrasts.csv",
        "category": "latest_taxonomy",
        "title": "v15dq pairwise type contrasts",
        "description": "Leakage-guarded descriptive pre-run contrasts.",
    },
    {
        "source": "Documentation/v15dq_active_set_taxonomy_feature_family_summary.csv",
        "category": "latest_taxonomy",
        "title": "v15dq feature-family summary",
        "description": "Contrast counts by feature family.",
    },
    {
        "source": "Documentation/v15dq_active_set_taxonomy_diagnosis.csv",
        "category": "latest_taxonomy",
        "title": "v15dq diagnosis",
        "description": "Machine-readable taxonomy diagnosis.",
    },
    {
        "source": "Documentation/v16h_fresh_rate_logged_mechanism_holdout.md",
        "category": "causal_architecture",
        "title": "v16h fresh total-rate mechanism holdout",
        "description": "Fresh validation attributing the clock/depth relation to scheduler total rate.",
    },
    {
        "source": "Documentation/v16h_gate_evaluation.csv",
        "category": "causal_architecture",
        "title": "v16h gate evaluation",
        "description": "Machine-readable total-rate mechanism gates.",
    },
    {
        "source": "Documentation/v16i_causal_interval_abundance_gate.md",
        "category": "causal_architecture",
        "title": "v16i causal-interval abundance gate",
        "description": "Open causal-interval spectrum beyond the layer and indegree null.",
    },
    {
        "source": "Documentation/v16i_interval_run_summary.csv",
        "category": "causal_architecture",
        "title": "v16i interval run summary",
        "description": "Per-run v16i effect and interval summaries.",
    },
    {
        "source": "Documentation/v16i_gate_evaluation.csv",
        "category": "causal_architecture",
        "title": "v16i gate evaluation",
        "description": "Machine-readable v16i gate outcomes.",
    },
    {
        "source": "Documentation/v16j_interval_strict_null_gate.md",
        "category": "latest_causal_structure",
        "title": "v16j strict-null gate",
        "description": "Frozen strict-null analysis preserving degree, depth, order, and global age-bin structure.",
    },
    {
        "source": "Documentation/v16j_interpretation_audit.md",
        "category": "latest_causal_structure",
        "title": "v16j interpretation audit",
        "description": "Required decomposition of strict-null effect existence and magnitude transfer.",
    },
    {
        "source": "Documentation/v16j_interpretation_audit.csv",
        "category": "latest_causal_structure",
        "title": "v16j interpretation audit data",
        "description": "Machine-readable post-run semantic audit; not a replacement gate.",
    },
    {
        "source": "Documentation/v16j_strict_null_run_summary.csv",
        "category": "latest_causal_structure",
        "title": "v16j strict-null run summary",
        "description": "Per-run effect, p-value, and null-mixing summary.",
    },
    {
        "source": "Documentation/v16j_local_strict_null_gate.csv",
        "category": "latest_causal_structure",
        "title": "v16j local strict-null gate",
        "description": "Primary effect-existence gate for the local scheduler arm.",
    },
    {
        "source": "Documentation/v16j_calibration_transfer.csv",
        "category": "latest_causal_structure",
        "title": "v16j magnitude transfer",
        "description": "Frozen v16d-to-v16h effect-size transfer result.",
    },
    {
        "source": "Documentation/v16j_gate_evaluation.csv",
        "category": "latest_causal_structure",
        "title": "v16j frozen gate evaluation",
        "description": "Machine-readable preregistered composite gate outcomes.",
    },
    {
        "source": "Documentation/v16j_claim_ledger.csv",
        "category": "latest_causal_structure",
        "title": "v16j claim ledger",
        "description": "Claim boundaries generated by the frozen v16j gate.",
    },
    {
        "source": "Documentation/v16m_qualified_sampler_fresh_holdout.md",
        "category": "latest_causal_structure",
        "title": "v16m fresh strict-null holdout",
        "description": "Fresh-history replication under the qualified strict degree/depth/age null.",
    },
    {
        "source": "Documentation/v16m_effect_existence_gate.csv",
        "category": "latest_causal_structure",
        "title": "v16m effect gate",
        "description": "Machine-readable fresh strict-null replication gate.",
    },
    {
        "source": "Documentation/v16m_gate_evaluation.csv",
        "category": "latest_causal_structure",
        "title": "v16m gate evaluation",
        "description": "Fresh-history integrity, effect, longer-null and magnitude gates.",
    },
    {
        "source": "Documentation/v16q_event_footprint_null_calibration.md",
        "category": "latest_causal_structure",
        "title": "v16q footprint-null calibration",
        "description": "Effect-blind qualification of the coarse event-footprint sampler.",
    },
    {
        "source": "Documentation/v16q_sampler_qualification.csv",
        "category": "latest_causal_structure",
        "title": "v16q sampler qualification",
        "description": "Selected attempt ceiling and qualification status.",
    },
    {
        "source": "Documentation/v16q_gate_evaluation.csv",
        "category": "latest_causal_structure",
        "title": "v16q gate evaluation",
        "description": "Machine-readable effect-blind sampler gates.",
    },
    {
        "source": "Documentation/v16r_event_footprint_sensitivity_gate.md",
        "category": "latest_causal_structure",
        "title": "v16r footprint sensitivity gate",
        "description": "Posthoc same-history sensitivity under the qualified footprint null.",
    },
    {
        "source": "Documentation/v16r_effect_existence_gate.csv",
        "category": "latest_causal_structure",
        "title": "v16r posthoc effect gate",
        "description": "Aggregate same-history footprint-null sensitivity result.",
    },
    {
        "source": "Documentation/v16r_gate_evaluation.csv",
        "category": "latest_causal_structure",
        "title": "v16r gate evaluation",
        "description": "Integrity, persistence and independent-replication exclusion gates.",
    },
    {
        "source": "Documentation/v16s_fresh_event_footprint_holdout.md",
        "category": "latest_causal_structure",
        "title": "v16s fresh footprint-null holdout",
        "description": "Fresh-history replication with the footprint null selected before generation.",
    },
    {
        "source": "Documentation/v16s_event_footprint_run_summary.csv",
        "category": "latest_causal_structure",
        "title": "v16s per-run footprint results",
        "description": "Per-run effect, p-value, tail and integrity summaries.",
    },
    {
        "source": "Documentation/v16s_effect_existence_gate.csv",
        "category": "latest_causal_structure",
        "title": "v16s fresh effect gate",
        "description": "Primary fresh footprint-null replication result.",
    },
    {
        "source": "Documentation/v16s_longer_footprint_gate.csv",
        "category": "latest_causal_structure",
        "title": "v16s longer footprint gate",
        "description": "Longer-perturbation consistency result.",
    },
    {
        "source": "Documentation/v16s_anchor_comparison.csv",
        "category": "latest_causal_structure",
        "title": "v16s descriptive anchor comparison",
        "description": "Descriptive magnitude comparison with v16m and v16r; not a confirmatory gate.",
    },
    {
        "source": "Documentation/v16s_gate_evaluation.csv",
        "category": "latest_causal_structure",
        "title": "v16s gate evaluation",
        "description": "Machine-readable fresh-history and footprint-null gates.",
    },
    {
        "source": "Documentation/v16s_claim_ledger.csv",
        "category": "latest_causal_structure",
        "title": "v16s claim ledger",
        "description": "Current supported, unresolved and unsupported claim boundaries.",
    },
    {
        "source": "Documentation/v16o_v16s_direction_and_execution_report.md",
        "category": "latest_causal_structure",
        "title": "v16o-v16s direction and execution report",
        "description": "Adviser arguments, literature constraints, executed sequence and next recommendation.",
    },
    {
        "source": "Documentation/v16t_footprint_null_path_stability_gate.md",
        "category": "latest_causal_structure",
        "title": "v16t footprint-null path stability gate",
        "description": "Effect-blind null-center stability test across direct chain lengths and a staged path.",
    },
    {
        "source": "Documentation/v16t_null_protocol_summary.csv",
        "category": "latest_causal_structure",
        "title": "v16t null protocol summary",
        "description": "Per-source protocol centers, dispersion, edge-change and conflict-retention diagnostics.",
    },
    {
        "source": "Documentation/v16t_null_center_comparison.csv",
        "category": "latest_causal_structure",
        "title": "v16t null-center comparison",
        "description": "Frozen chain-length and path-segmentation center-shift ratios for all six source DAGs.",
    },
    {
        "source": "Documentation/v16t_footprint_perturbation_integrity.csv",
        "category": "latest_causal_structure",
        "title": "v16t perturbation integrity",
        "description": "Structural, completion, uniqueness and edge-change audits for all 384 null DAGs.",
    },
    {
        "source": "Documentation/v16t_null_spectrum_distribution.csv",
        "category": "latest_causal_structure",
        "title": "v16t null-spectrum distribution",
        "description": "Per-null spectra used only for effect-blind protocol-center stability comparisons.",
    },
    {
        "source": "Documentation/v16t_gate_evaluation.csv",
        "category": "latest_causal_structure",
        "title": "v16t gate evaluation",
        "description": "Machine-readable integrity, chain-length, path and spectrum-exclusion gates.",
    },
    {
        "source": "Documentation/v16t_claim_ledger.csv",
        "category": "latest_causal_structure",
        "title": "v16t claim ledger",
        "description": "Supported procedure-level claim and explicit unresolved sampler and physics claims.",
    },
    {
        "source": "Documentation/v16t_pre_registration.csv",
        "category": "latest_causal_structure",
        "title": "v16t preregistration",
        "description": "Frozen digest, source hashes, budgets and effect-blind exclusions.",
    },
    {
        "source": "Documentation/v16t_source_chain.csv",
        "category": "latest_causal_structure",
        "title": "v16t source chain",
        "description": "SHA-256 chain linking v16t to the frozen v16s histories and v16q sampler.",
    },
    {
        "source": "Documentation/v16t_next_direction_assessment.md",
        "category": "latest_causal_structure",
        "title": "v16t interpretation and next direction",
        "description": "Evidence boundary and corrected realized-effort stability recommendation.",
    },
    {
        "source": "Documentation/v16t_realized_effort_interpretation_audit.md",
        "category": "latest_causal_structure",
        "title": "v16t realized-effort interpretation audit",
        "description": "Post-run audit showing that nominal direct lengths were not separated and staged effort was unmatched.",
    },
    {
        "source": "Documentation/v16t_realized_effort_interpretation_audit.csv",
        "category": "latest_causal_structure",
        "title": "v16t realized-effort interpretation data",
        "description": "Machine-readable semantic correction that preserves the frozen gate while narrowing its claim.",
    },
    {
        "source": "Documentation/v0_16t_operativ_anbefaling.md",
        "category": "latest_causal_structure",
        "title": "v16t operational recommendation",
        "description": "Concise operational status and next-step boundary after the effect-blind stability gate.",
    },
    {
        "source": "Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_16t.md",
        "category": "latest_causal_structure",
        "title": "v16t non-specialist summary",
        "description": "Plain-language distinction between null-procedure stability and a physics result.",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def table_html(rows: Iterable[Mapping[str, Any]], columns: list[str]) -> str:
    header = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    body = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(col, '')))}</td>" for col in columns)
        body.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def grouped_manifest(manifest: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in manifest:
        grouped.setdefault(str(item["category"]), []).append(item)
    return grouped


def copy_data(out_dir: Path) -> list[dict[str, Any]]:
    data_dir = out_dir / "data"
    manifest: list[dict[str, Any]] = []
    for spec in DATASET_SPECS:
        source = ROOT / spec["source"]
        if not source.exists():
            raise FileNotFoundError(source)
        category = spec["category"]
        target_rel = Path("data") / category / source.name
        target = out_dir / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest.append(
            {
                "title": spec["title"],
                "description": spec["description"],
                "category": category,
                "source_path": spec["source"],
                "public_path": target_rel.as_posix(),
                "bytes": target.stat().st_size,
                "sha256": sha256_file(target),
            }
        )
    data_dir.mkdir(parents=True, exist_ok=True)
    return manifest


def git_revision() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def write_manifest_files(
    out_dir: Path,
    manifest: list[dict[str, Any]],
    generated_at: str,
    source_revision: str,
) -> None:
    payload = {
        "generated_at": generated_at,
        "source_repository": "https://github.com/kjetilh/UniverseSimulation",
        "source_revision": source_revision,
        "license_note": "Research data are published for inspection and reuse with attribution; interpretive claims remain provisional.",
        "artifacts": manifest,
    }
    (out_dir / "data" / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (out_dir / "data" / "manifest.csv").open("w", newline="", encoding="utf-8") as fh:
        fieldnames = ["category", "title", "description", "source_path", "public_path", "bytes", "sha256"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in manifest:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def css() -> str:
    return """
:root {
  color-scheme: light;
  --ink: #17211b;
  --muted: #5e6a61;
  --paper: #f7f4ed;
  --panel: #fffdf8;
  --line: #d8d0c2;
  --accent: #0e675e;
  --accent-2: #8b4b18;
  --code: #233b34;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background:
    radial-gradient(circle at 16% 4%, rgba(14, 103, 94, 0.12), transparent 34rem),
    linear-gradient(180deg, #fbfaf6 0%, var(--paper) 100%);
  color: var(--ink);
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.54;
}
main, header, footer { max-width: 1180px; margin: 0 auto; padding: 0 28px; }
header { padding-top: 58px; padding-bottom: 36px; }
.eyebrow {
  color: var(--accent);
  font: 700 12px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
h1 {
  max-width: 980px;
  margin: 16px 0 18px;
  font-size: clamp(38px, 6vw, 78px);
  line-height: 0.94;
  letter-spacing: -0.045em;
}
h2 {
  margin-top: 54px;
  font-size: clamp(26px, 3vw, 40px);
  line-height: 1.05;
  letter-spacing: -0.02em;
}
h3 { margin-top: 28px; font-size: 21px; }
p.lead { max-width: 880px; font-size: 21px; color: #29342e; }
.grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; margin: 28px 0; }
.card {
  background: rgba(255, 253, 248, 0.88);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 14px 30px rgba(42, 32, 18, 0.05);
}
.metric { font-size: 32px; line-height: 1; font-weight: 700; letter-spacing: -0.03em; }
.muted { color: var(--muted); }
.warning { border-left: 4px solid var(--accent-2); padding-left: 16px; color: #3e3228; }
a { color: var(--accent); text-decoration-thickness: 0.08em; text-underline-offset: 0.18em; }
table { width: 100%; border-collapse: collapse; margin: 18px 0 30px; font-size: 14px; background: var(--panel); }
th, td { border-bottom: 1px solid var(--line); padding: 10px 9px; text-align: left; vertical-align: top; }
th { font: 700 12px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
code { color: var(--code); background: rgba(14, 103, 94, 0.08); padding: 0.1em 0.32em; border-radius: 5px; }
.artifact-list { columns: 2; column-gap: 36px; padding-left: 0; list-style: none; }
.artifact-list li { break-inside: avoid; margin: 0 0 12px; }
.artifact-list small { display: block; color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
footer { padding-top: 42px; padding-bottom: 50px; color: var(--muted); font-size: 14px; }
@media (max-width: 820px) {
  .grid { grid-template-columns: 1fr; }
  .artifact-list { columns: 1; }
  main, header, footer { padding-left: 18px; padding-right: 18px; }
}
""".strip() + "\n"


def write_site(
    out_dir: Path,
    manifest: list[dict[str, Any]],
    generated_at: str,
    source_revision: str,
) -> None:
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "site.css").write_text(css(), encoding="utf-8")
    (out_dir / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    seed_rows = csv_rows(out_dir / "data" / "latest_taxonomy" / "v15dq_active_set_taxonomy_seed_summary.csv")
    class_rows = csv_rows(out_dir / "data" / "latest_taxonomy" / "v15dq_active_set_taxonomy_class_summary.csv")
    diagnosis_rows = csv_rows(out_dir / "data" / "latest_taxonomy" / "v15dq_active_set_taxonomy_diagnosis.csv")
    strict_local_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16j_local_strict_null_gate.csv")
    strict_transfer_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16j_calibration_transfer.csv")
    strict_gate_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16j_gate_evaluation.csv")
    interpretation_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16j_interpretation_audit.csv")
    footprint_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16s_effect_existence_gate.csv")
    footprint_longer_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16s_longer_footprint_gate.csv")
    footprint_gate_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16s_gate_evaluation.csv")
    footprint_claim_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16s_claim_ledger.csv")
    stability_gate_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16t_gate_evaluation.csv")
    stability_comparison_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16t_null_center_comparison.csv")
    stability_claim_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16t_claim_ledger.csv")
    stability_audit_rows = csv_rows(out_dir / "data" / "latest_causal_structure" / "v16t_realized_effort_interpretation_audit.csv")
    grouped = grouped_manifest(manifest)
    artifact_items = []
    for category, items in sorted(grouped.items()):
        artifact_items.append(f"<h3>{html.escape(category.replace('_', ' ').title())}</h3><ul class='artifact-list'>")
        for item in items:
            artifact_items.append(
                "<li>"
                f"<a href='{html.escape(item['public_path'])}'>{html.escape(item['title'])}</a>"
                f"<small>{html.escape(str(item['bytes']))} bytes - sha256 {html.escape(item['sha256'][:12])}...</small>"
                f"<span class='muted'>{html.escape(item['description'])}</span>"
                "</li>"
            )
        artifact_items.append("</ul>")

    index = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Emergent Universe Simulation - public research archive</title>
  <meta name="description" content="Public scientific archive for the UniverseSimulation research program: dynamic graph universes, Lorentz diagnostics, defect response and active-set taxonomy.">
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>
  <header>
    <div class="eyebrow">Public research archive - generated {html.escape(generated_at)} - revision {html.escape(source_revision[:12])}</div>
    <h1>Emergent Universe Simulation</h1>
    <p class="lead">A public, evidence-led archive testing whether local stochastic graph dynamics can produce robust higher-level law structure. The latest frozen gate found effect-blind null-center stability, but its realized-effort audit shows that direct chain lengths were not separated and staged effort was unmatched. The underlying signal remains a finite event-DAG spectrum contrast, not a spacetime claim.</p>
  </header>
  <main>
    <section class="grid">
      <div class="card"><div class="metric">band_zero_del</div><p class="muted">Current operational growth regime, retained after the v11e frontier duel.</p></div>
      <div class="card"><div class="metric">11.9993</div><p class="muted">v16s median JS effect ratio on six new footprint-null holdout histories.</p></div>
      <div class="card"><div class="metric">384 / 384</div><p class="muted">v16t effect-blind null perturbations passed structural and uniqueness checks.</p></div>
    </section>

    <section>
      <h2>Scientific status</h2>
      <p>The project studies evolving relational graphs under local stochastic update rules. The working discipline is to separate algebraic/formal claims, generator artifacts, scoring artifacts and actual dynamical outcomes. Heuristic collision labels are not treated as particles, and long-lived local persistence is not treated as universal emergent spacetime.</p>
      <p>The earlier defect/response track established nontrivial local interactions but not particles. The current architecture track records exact event dependencies. v16h retired a clock/depth common-geometry reading by validating scheduler total rate as the mechanism. v16i through v16m then isolated and freshly replicated an open causal-interval spectrum contrast under a strict degree/depth/age null.</p>
      <p>v16o showed that a concrete-resource-conflict edge-color null was structurally immobile. v16p and v16q replaced it with a coarser event-footprint rule and qualified that sampler without inspecting spectra. v16r retained the contrast posthoc, and v16s replicated it on six new histories with the footprint null selected before generation. The v16s median effect ratio was <code>11.999282</code>; all six primary runs had empirical <code>p = 1/33</code>.</p>
      <p>All v16s tail-mass deltas were negative. The result is therefore a full-spectrum contrast, not evidence for excess large intervals.</p>
      <p>v16t then tested the footprint-null procedure without computing any source spectrum or observed-effect metric. All frozen comparisons passed, but the required realized-effort audit found that direct short/reference/long averaged <code>993/1005/998</code> accepted swaps while staged averaged <code>2023</code>. The frozen pass is therefore a center-stability diagnostic; it does not separately establish chain-length or path-segmentation stability.</p>
      <p class="warning">Interpretation boundary: the public data support a program of local defect and response-landscape analysis. They do not establish Lorentz invariance, quantum entanglement, particle species or a completed universe model.</p>
    </section>

    <section>
      <h2>Current effect-blind footprint-null stability gate</h2>
      {table_html(stability_gate_rows, ["gate", "status", "observed", "required", "decision"])}
      <h3>Required realized-effort interpretation audit</h3>
      {table_html(stability_audit_rows, ["audit_item", "status", "observed", "required", "evidential_role"])}
      {table_html(stability_comparison_rows, ["growth_seed", "run_offset", "comparison", "center_jensen_shannon", "pooled_median_leave_one_out_js", "center_shift_ratio", "stability_pass"])}

      <h3>Prior v16s fresh effect gate</h3>
      {table_html(footprint_rows, ["stage", "n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass"])}
      {table_html(footprint_longer_rows, ["stage", "n_runs", "target_swap_multiplier", "median_js_effect_ratio", "positive_fraction", "longer_perturbation_consistency_pass"])}
      {table_html(footprint_gate_rows, ["gate", "status", "observed", "required", "decision"])}

      <h3>Earlier strict-null checkpoint</h3>
      {table_html(strict_local_rows, ["stage", "n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass"])}
      {table_html(strict_transfer_rows, ["source_stage", "holdout_stage", "source_median_js_effect_ratio", "holdout_median_js_effect_ratio", "holdout_over_source_ratio", "calibration_transfer_pass"])}
      {table_html(strict_gate_rows, ["gate", "status", "observed", "required", "decision"])}
    </section>

    <section>
      <h2>Earlier defect landscape checkpoint</h2>
      {table_html(seed_rows, ["growth_seed", "landscape_class", "active_placements", "p0_established_rate", "p1_established_rate", "p2_established_rate"])}
      {table_html(class_rows, ["landscape_class", "n_seeds", "growth_seeds", "old_v15do_type_space", "median_p0_established_rate", "median_p1_established_rate", "median_p2_established_rate"])}
    </section>

    <section>
      <h2>Methods</h2>
      <p>The experiments use generated graph ensembles, matched controls, perturbation probes, defect genealogy, exact event-DAG reconstruction, source hashing, preregistered holdouts and explicit structural nulls. Reports and machine-readable CSVs are published together so claims can be checked against their originating rows.</p>
      <p>v16j uses directed double-edge swaps that preserve event count, scheduler order, exact direct in/out-degree, exact causal depth and the global dyadic parent-age histogram. v16q adds source event family/write-namespace and target event family/read-namespace footprints. Every accepted holdout null had to be unique and change at least 10% of direct edges. Qualification establishes procedural completion and invariant preservation, not uniform or converged sampling.</p>
      <p>v16t compares only null ensembles. Its source spectra and observed/null effect statistics are excluded by preregistration, preventing the stability threshold or path selection from being tuned against the positive v16s result.</p>
    </section>

    <section>
      <h2>RAG and corpus status</h2>
      <p>The repository contains a UniverseSimulation-specific FastAPI/pgvector RAG service with separate status, experiment, tool, argumentation and prompt sources. This public host publishes the current corpus documents and evidence artifacts as static, checksum-addressed files. It does not expose dynamic RAG routes. Dynamic retrieval freshness must be verified separately with token scope, shared rate limits, citation audit and corpus-freshness metadata.</p>
    </section>

    <section>
      <h2>Current machine-readable claim ledger</h2>
      <p>The interpretation audit below supersedes the broad semantic reading of the frozen v16t claim row while preserving the preregistered machine result.</p>
      {table_html(stability_audit_rows, ["audit_item", "status", "observed", "required", "evidential_role"])}
      <h3>Frozen v16t claim ledger</h3>
      {table_html(stability_claim_rows, ["claim_id", "claim", "status", "evidence", "scope_limit"])}
      <h3>Prior v16s effect claim ledger</h3>
      {table_html(footprint_claim_rows, ["claim_id", "claim", "status", "evidence", "scope_limit"])}
      <h3>Earlier v16j interpretation audit</h3>
      {table_html(interpretation_rows, ["audit_item", "status", "observed", "required", "evidential_role"])}
    </section>

    <section>
      <h2>Downloadable archive</h2>
      <p>Use <a href="data/manifest.json">manifest.json</a> or <a href="data/manifest.csv">manifest.csv</a> for checksums, source paths and artifact descriptions.</p>
      {''.join(artifact_items)}
    </section>
  </main>
  <footer>
    <p>Generated from UniverseSimulation revision {html.escape(source_revision)}. The archive is provided for inspection, replication and critique. Cite artifact filenames, revision and SHA-256 hashes when discussing specific rows or reports.</p>
  </footer>
</body>
</html>
"""
    (out_dir / "index.html").write_text(index, encoding="utf-8")
    readme = f"""# Emergent Universe public archive

Generated: {generated_at}

This directory is a static public bundle for `emergentuniverse.haven.digipomps.org`.

The dynamic RAG service is not exposed here. The bundle includes selected RAG
corpus documents and research artifacts as static, citeable files.

See:

- `index.html`
- `data/manifest.json`
- `data/manifest.csv`
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def build(out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_revision = git_revision()
    manifest = copy_data(out_dir)
    write_manifest_files(out_dir, manifest, generated_at, source_revision)
    write_site(out_dir, manifest, generated_at, source_revision)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the static Emergent Universe public site.")
    parser.add_argument("--out", default="/tmp/emergentuniverse_public", help="Output directory for the generated static site.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out).resolve()
    build(out_dir)
    print(f"built {out_dir}")


if __name__ == "__main__":
    main()
