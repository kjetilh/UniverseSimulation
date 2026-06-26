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


def write_manifest_files(out_dir: Path, manifest: list[dict[str, Any]], generated_at: str) -> None:
    payload = {
        "generated_at": generated_at,
        "source_repository": str(ROOT),
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


def write_site(out_dir: Path, manifest: list[dict[str, Any]], generated_at: str) -> None:
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "site.css").write_text(css(), encoding="utf-8")
    (out_dir / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    seed_rows = csv_rows(out_dir / "data" / "latest_taxonomy" / "v15dq_active_set_taxonomy_seed_summary.csv")
    class_rows = csv_rows(out_dir / "data" / "latest_taxonomy" / "v15dq_active_set_taxonomy_class_summary.csv")
    diagnosis_rows = csv_rows(out_dir / "data" / "latest_taxonomy" / "v15dq_active_set_taxonomy_diagnosis.csv")
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
    <div class="eyebrow">Public research archive - generated {html.escape(generated_at)}</div>
    <h1>Emergent Universe Simulation</h1>
    <p class="lead">A public, evidence-led archive for a research program exploring whether local stochastic graph dynamics can produce stable structure, defect interactions and eventually stronger candidates for emergent geometry. The current result is deliberately modest: local structure and defect response are real enough to study, while Lorentz-like behavior and universal invariants remain <code>not_yet</code>.</p>
  </header>
  <main>
    <section class="grid">
      <div class="card"><div class="metric">band_zero_del</div><p class="muted">Current operational growth regime, retained after the v11e frontier duel.</p></div>
      <div class="card"><div class="metric">not_yet</div><p class="muted">Current status for Lorentz-like behavior: controls improved, but propagation remains mode-dependent and placement-sensitive.</p></div>
      <div class="card"><div class="metric">4 classes</div><p class="muted">Current add_chord active-set taxonomy across six 1024-scale seeds.</p></div>
    </section>

    <section>
      <h2>Scientific status</h2>
      <p>The project studies evolving relational graphs under local stochastic update rules. The working discipline is to separate algebraic/formal claims, generator artifacts, scoring artifacts and actual dynamical outcomes. Heuristic collision labels are not treated as particles, and long-lived local persistence is not treated as universal emergent spacetime.</p>
      <p>The current strongest empirical thread is the defect/response track, especially <code>add_chord</code> behavior. Recent pre-registered holdouts rejected a simple two-type active-set guard and forced a wider taxonomy.</p>
      <p class="warning">Interpretation boundary: the public data support a program of local defect and response-landscape analysis. They do not establish Lorentz invariance, quantum entanglement, particle species or a completed universe model.</p>
    </section>

    <section>
      <h2>Current active-set taxonomy</h2>
      {table_html(seed_rows, ["growth_seed", "landscape_class", "active_placements", "p0_established_rate", "p1_established_rate", "p2_established_rate"])}
      {table_html(class_rows, ["landscape_class", "n_seeds", "growth_seeds", "old_v15do_type_space", "median_p0_established_rate", "median_p1_established_rate", "median_p2_established_rate"])}
    </section>

    <section>
      <h2>Methods</h2>
      <p>The experiments use generated graph ensembles, matched controls, perturbation probes, defect genealogy/event logs, pre-run morphology features and pre-registered holdouts. The public archive includes both reports and machine-readable CSV artifacts so claims can be checked against the originating data.</p>
      <p>Important methodological safeguards include: target-size separation checks, requested perturbation matching, matched single-run controls for collision analysis, explicit distinction between pre-run observables and post-hoc diagnostics, and no refitting after failed holdouts.</p>
    </section>

    <section>
      <h2>RAG and corpus status</h2>
      <p>The repository contains a UniverseSimulation-specific FastAPI/pgvector RAG service with cases for project status, tools, argumentation and prompts. This public release publishes the RAG corpus plan and status documents, but does not expose the dynamic RAG service as a public API. That is intentional: the static archive is safer and easier to cite; a public RAG endpoint should come later only with authentication, rate limits, corpus freshness checks and citation auditing.</p>
    </section>

    <section>
      <h2>Machine-readable diagnosis</h2>
      {table_html(diagnosis_rows, ["diagnostic_family", "status", "note"])}
    </section>

    <section>
      <h2>Downloadable archive</h2>
      <p>Use <a href="data/manifest.json">manifest.json</a> or <a href="data/manifest.csv">manifest.csv</a> for checksums, source paths and artifact descriptions.</p>
      {''.join(artifact_items)}
    </section>
  </main>
  <footer>
    <p>Generated from the local UniverseSimulation repository. The archive is provided for inspection, replication and critique. Cite artifact filenames and SHA-256 hashes when discussing specific rows or reports.</p>
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
    manifest = copy_data(out_dir)
    write_manifest_files(out_dir, manifest, generated_at)
    write_site(out_dir, manifest, generated_at)


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
