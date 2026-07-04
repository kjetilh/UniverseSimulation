#!/usr/bin/env python3
"""v0.15dq active-set taxonomy synthesis.

No-new-dynamics synthesis after v15dp.

Goal:
- stop treating the post-v15dp problem as another single frozen guard,
- combine v15dn and v15dp active-set landscapes,
- make the observed response taxonomy explicit,
- report tiny-sample pre-run contrasts only as descriptive leads.

This script reads existing CSV artifacts only. It does not run defect dynamics.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn


DOC = Path("Documentation")

TARGET_NODES = 1024
PLACEMENTS = (0, 1, 2)
ACTIVE_ESTABLISHED_RATE = 0.50

V15DN_PLACEMENT_CSV = DOC / "v15dn_multi_active_landscape_placement_rows.csv"
V15DP_PLACEMENT_CSV = DOC / "v15dp_active_set_type_guard_placement_summary.csv"
V15DP_MORPHOLOGY_CSV = DOC / "v15dp_active_set_type_guard_pre_run_morphology.csv"
V15DP_GUARD_EVAL_CSV = DOC / "v15dp_active_set_type_guard_evaluation.csv"

OLD_V15DO_TYPES = {"single_active_p1", "multi_active_p0_p2"}


def read_csv(path: Path) -> List[Dict[str, str]]:
    return v15dn.read_csv(path)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dn.write_csv(path, rows)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15dn.safe_float(x, default)


def safe_int(x: Any, default: int = 0) -> int:
    return v15dn.safe_int(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    return v15dn.fmt(x, digits=digits)


def mean_defined(values: Iterable[Any]) -> float:
    return v15dn.mean_defined(values)


def median_defined(values: Iterable[Any]) -> float:
    return v15dn.median_defined(values)


def format_set(values: Iterable[int]) -> str:
    vals = sorted(int(x) for x in values)
    return ";".join(f"p{x}" for x in vals) if vals else "none"


def parse_set(label: str) -> set[int]:
    if not label or label == "none":
        return set()
    out: set[int] = set()
    for part in label.split(";"):
        part = part.strip()
        if part.startswith("p"):
            out.add(int(part[1:]))
    return out


def landscape_class(active_set: Iterable[int]) -> str:
    active = sorted(int(x) for x in active_set)
    if not active:
        return "no_active"
    if len(active) == 1:
        return f"single_active_p{active[0]}"
    return "multi_active_" + "_".join(f"p{x}" for x in active)


def load_placement_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for raw in read_csv(V15DN_PLACEMENT_CSV):
        row: Dict[str, Any] = dict(raw)
        row["taxonomy_input_source"] = "v15dn"
        rows.append(normalize_placement_row(row))

    morphology_by_key = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"])): row
        for row in read_csv(V15DP_MORPHOLOGY_CSV)
    }
    for raw in read_csv(V15DP_PLACEMENT_CSV):
        row = dict(raw)
        seed = safe_int(row["growth_seed"])
        placement = safe_int(row["placement"])
        morph = morphology_by_key[(seed, placement)]
        row["source"] = "v15dp"
        row["target_nodes"] = TARGET_NODES
        row["profile_label"] = f"add_chord_p{placement}"
        row["taxonomy_input_source"] = "v15dp"
        for key, value in morph.items():
            row.setdefault(key, value)
        for metric in v15dn.MORPHOLOGY_METRICS:
            if metric not in row or row[metric] == "":
                row[metric] = morph.get(metric, "")
        rows.append(normalize_placement_row(row))
    return sorted(rows, key=lambda r: (safe_int(r["growth_seed"]), safe_int(r["placement"])))


def normalize_placement_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    placement = safe_int(out.get("placement"))
    out["target_nodes"] = safe_int(out.get("target_nodes", TARGET_NODES), TARGET_NODES)
    out["growth_seed"] = safe_int(out.get("growth_seed"))
    out["placement"] = placement
    out["profile_label"] = out.get("profile_label") or f"add_chord_p{placement}"
    out["active_placement"] = int(safe_float(out.get("active_placement")) >= 1.0)
    out["established_rate"] = safe_float(out.get("established_rate"))
    out["support_signature"] = v15dn.normalize_support_signature(out)
    if "median_w32_mean_boundary_per_mass" not in out:
        out["median_w32_mean_boundary_per_mass"] = out.get("median_boundary_mass", "")
    if "median_genealogy_intensity_index" not in out:
        out["median_genealogy_intensity_index"] = out.get("median_genealogy_intensity", "")
    return out


def seed_summary_rows(placement_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in placement_rows:
        grouped[safe_int(row["growth_seed"])].append(row)

    out: List[Dict[str, Any]] = []
    for seed, group in sorted(grouped.items()):
        active = {
            safe_int(row["placement"])
            for row in group
            if safe_int(row.get("active_placement")) == 1
        }
        rates = {safe_int(row["placement"]): safe_float(row["established_rate"]) for row in group}
        strongest = max(rates, key=lambda p: rates[p]) if rates else -1
        klass = landscape_class(active)
        out.append(
            {
                "growth_seed": seed,
                "source_inputs": ";".join(sorted(set(str(row.get("taxonomy_input_source", "")) for row in group))),
                "active_count": len(active),
                "active_placements": format_set(active),
                "landscape_class": klass,
                "covered_by_v15do_two_type_space": int(klass in OLD_V15DO_TYPES),
                "new_after_v15dp_type": int(klass not in OLD_V15DO_TYPES),
                "strongest_placement": f"p{strongest}" if strongest >= 0 else "none",
                "strongest_established_rate": rates.get(strongest, float("nan")),
                "p0_established_rate": rates.get(0, float("nan")),
                "p1_established_rate": rates.get(1, float("nan")),
                "p2_established_rate": rates.get(2, float("nan")),
                "placement_rates": ";".join(f"p{p}:{fmt(rates.get(p))}" for p in PLACEMENTS),
                "support_signatures": ";".join(
                    f"p{safe_int(row['placement'])}:{row['support_signature']}"
                    for row in sorted(group, key=lambda r: safe_int(r["placement"]))
                ),
            }
        )
    return out


def taxonomy_summary_rows(seed_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in seed_rows:
        grouped[str(row["landscape_class"])].append(row)

    out: List[Dict[str, Any]] = []
    for klass, group in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(
            {
                "landscape_class": klass,
                "n_seeds": len(group),
                "growth_seeds": ";".join(str(row["growth_seed"]) for row in group),
                "old_v15do_type_space": int(klass in OLD_V15DO_TYPES),
                "mean_active_count": mean_defined(row["active_count"] for row in group),
                "median_p0_established_rate": median_defined(row["p0_established_rate"] for row in group),
                "median_p1_established_rate": median_defined(row["p1_established_rate"] for row in group),
                "median_p2_established_rate": median_defined(row["p2_established_rate"] for row in group),
            }
        )
    return out


def seed_feature_rows(
    seed_rows: Sequence[Mapping[str, Any]],
    placement_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    seed_meta = {safe_int(row["growth_seed"]): row for row in seed_rows}
    grouped: Dict[int, Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in placement_rows:
        grouped[safe_int(row["growth_seed"])][safe_int(row["placement"])] = row

    out: List[Dict[str, Any]] = []
    for seed, placements in sorted(grouped.items()):
        meta = seed_meta[seed]
        row: Dict[str, Any] = {
            "growth_seed": seed,
            "landscape_class": meta["landscape_class"],
            "active_count": meta["active_count"],
            "active_placements": meta["active_placements"],
            "covered_by_v15do_two_type_space": meta["covered_by_v15do_two_type_space"],
            "p0_established_rate": meta["p0_established_rate"],
            "p1_established_rate": meta["p1_established_rate"],
            "p2_established_rate": meta["p2_established_rate"],
        }
        for metric in v15dn.MORPHOLOGY_METRICS:
            vals = {p: safe_float(placements.get(p, {}).get(metric)) for p in PLACEMENTS}
            if not any(math.isfinite(v) for v in vals.values()):
                continue
            for p in PLACEMENTS:
                row[f"{metric}_p{p}"] = vals[p]
            row[f"{metric}_p0_minus_p1"] = vals[0] - vals[1]
            row[f"{metric}_p2_minus_p1"] = vals[2] - vals[1]
            row[f"{metric}_p2_minus_p0"] = vals[2] - vals[0]
            row[f"{metric}_range"] = max(vals.values()) - min(vals.values())
        out.append(row)
    return out


def numeric_feature_names(seed_features: Sequence[Mapping[str, Any]]) -> List[str]:
    skip = {
        "growth_seed",
        "landscape_class",
        "active_placements",
        "active_count",
        "covered_by_v15do_two_type_space",
        "p0_established_rate",
        "p1_established_rate",
        "p2_established_rate",
    }
    names: List[str] = []
    for row in seed_features:
        for key, value in row.items():
            if key in skip or key in names:
                continue
            if math.isfinite(safe_float(value)):
                names.append(key)
    return names


def feature_metric_name(feature: str) -> str:
    for suffix in ("_p0_minus_p1", "_p2_minus_p1", "_p2_minus_p0", "_range", "_p0", "_p1", "_p2"):
        if feature.endswith(suffix):
            return feature[: -len(suffix)]
    return feature


def pairwise_type_contrast_rows(seed_features: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_type: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in seed_features:
        by_type[str(row["landscape_class"])].append(row)

    features = numeric_feature_names(seed_features)
    out: List[Dict[str, Any]] = []
    types = sorted(by_type)
    for i, left_type in enumerate(types):
        for right_type in types[i + 1:]:
            left_rows = by_type[left_type]
            right_rows = by_type[right_type]
            for feature in features:
                left_values = [safe_float(row.get(feature)) for row in left_rows]
                right_values = [safe_float(row.get(feature)) for row in right_rows]
                left_values = [x for x in left_values if math.isfinite(x)]
                right_values = [x for x in right_values if math.isfinite(x)]
                if not left_values or not right_values:
                    continue
                left_gt = min(left_values) > max(right_values)
                right_gt = min(right_values) > max(left_values)
                if left_gt:
                    direction = f"{left_type}_gt_{right_type}"
                    clean = 1
                elif right_gt:
                    direction = f"{right_type}_gt_{left_type}"
                    clean = 1
                else:
                    direction = "overlap"
                    clean = 0
                min_n = min(len(left_rows), len(right_rows))
                out.append(
                    {
                        "left_type": left_type,
                        "right_type": right_type,
                        "feature": feature,
                        "metric": feature_metric_name(feature),
                        "feature_family": v15dn.feature_family(feature_metric_name(feature)),
                        "left_n": len(left_rows),
                        "right_n": len(right_rows),
                        "evidence_strength": "repeated_pair_tiny" if min_n >= 2 else "singleton_descriptive_only",
                        "clean_current_sample": clean,
                        "direction": direction,
                        "left_min": min(left_values),
                        "left_median": median_defined(left_values),
                        "left_max": max(left_values),
                        "right_min": min(right_values),
                        "right_median": median_defined(right_values),
                        "right_max": max(right_values),
                    }
                )
    return sorted(
        out,
        key=lambda row: (
            -safe_int(row["clean_current_sample"]),
            str(row["evidence_strength"]) != "repeated_pair_tiny",
            str(row["left_type"]),
            str(row["right_type"]),
            str(row["feature_family"]),
            str(row["feature"]),
        ),
    )


def feature_family_summary_rows(pairwise_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in pairwise_rows:
        grouped[(str(row["feature_family"]), str(row["evidence_strength"]))].append(row)

    out: List[Dict[str, Any]] = []
    for (family, strength), group in sorted(grouped.items()):
        clean = [row for row in group if safe_int(row["clean_current_sample"]) == 1]
        out.append(
            {
                "feature_family": family,
                "evidence_strength": strength,
                "n_contrasts": len(group),
                "n_clean_current_sample": len(clean),
                "clean_rate": len(clean) / max(1, len(group)),
                "example_clean_features": ";".join(str(row["feature"]) for row in clean[:8]),
            }
        )
    return out


def diagnosis_rows(
    *,
    seed_rows: Sequence[Mapping[str, Any]],
    taxonomy_rows: Sequence[Mapping[str, Any]],
    pairwise_rows: Sequence[Mapping[str, Any]],
    guard_eval: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    class_counts = Counter(str(row["landscape_class"]) for row in seed_rows)
    old_covered = sum(safe_int(row["covered_by_v15do_two_type_space"]) for row in seed_rows)
    new_count = len(seed_rows) - old_covered
    repeated_classes = [
        row for row in taxonomy_rows
        if safe_int(row["n_seeds"]) >= 2
    ]
    singleton_classes = [
        row for row in taxonomy_rows
        if safe_int(row["n_seeds"]) == 1
    ]
    repeated_pair_clean = [
        row for row in pairwise_rows
        if str(row["evidence_strength"]) == "repeated_pair_tiny" and safe_int(row["clean_current_sample"]) == 1
    ]
    guard_status = next((row for row in guard_eval if row.get("key") == "guard_status"), {"value": "missing"})

    if new_count > 0:
        taxonomy_status = "expanded_beyond_v15do_two_type_space"
        next_status = "build_taxonomy_mapper_before_new_selector"
        next_note = (
            "Neste dynamiske budsjett bor brukes til aa kartlegge flere fresh seeds eller teste en taxonomy-mapper; "
            "ikke til aa refitte den gamle two-type-guarden."
        )
    else:
        taxonomy_status = "old_two_type_space_still_covers_all"
        next_status = "replicate_two_type_mapper"
        next_note = "Hvis alle seeds fortsatt var i gammelt type-rom, kunne en ny pre-registered mapper vaert neste steg."

    return [
        {
            "diagnostic_family": "input_scope",
            "status": "no_new_dynamics",
            "note": "v15dq leser v15dn og v15dp placement/morphology CSV-er; ingen nye defect-runs er kjoert.",
        },
        {
            "diagnostic_family": "taxonomy_scope",
            "status": taxonomy_status,
            "note": (
                f"Observed classes: {';'.join(f'{k}:{v}' for k, v in sorted(class_counts.items()))}. "
                f"Old v15do type-space covers {old_covered}/{len(seed_rows)} seeds; new classes cover {new_count}/{len(seed_rows)}."
            ),
        },
        {
            "diagnostic_family": "repetition_balance",
            "status": "mixed_repeated_and_singleton_classes",
            "note": (
                f"Repeated classes: {';'.join(str(row['landscape_class']) for row in repeated_classes)}. "
                f"Singleton classes: {';'.join(str(row['landscape_class']) for row in singleton_classes)}."
            ),
        },
        {
            "diagnostic_family": "v15dp_guard_reading",
            "status": str(guard_status["value"]),
            "note": "Frozen delta_return_t2 guard is retained only as a failed candidate, not refit.",
        },
        {
            "diagnostic_family": "pre_run_contrasts",
            "status": "descriptive_leads_only",
            "note": (
                f"Repeated-pair clean contrasts in current sample: {len(repeated_pair_clean)}. "
                "Because n is tiny and two classes are singletons, these are leads, not selector validation."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str], limit: int | None = None) -> List[str]:
    shown = list(rows[:limit] if limit is not None else rows)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in shown:
        vals = []
        for field in fields:
            val = row.get(field, "")
            vals.append(fmt(val) if isinstance(val, float) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def build_report(
    *,
    seed_rows: Sequence[Mapping[str, Any]],
    taxonomy_rows: Sequence[Mapping[str, Any]],
    family_rows: Sequence[Mapping[str, Any]],
    pairwise_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    repeated_pair_clean = [
        row for row in pairwise_rows
        if str(row["evidence_strength"]) == "repeated_pair_tiny" and safe_int(row["clean_current_sample"]) == 1
    ]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dq: active-set taxonomy synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en no-new-dynamics syntese etter v15dp.")
    lines.append("Den smarte endringen er aa slutte aa refitte en to-type guard naar holdouten viser nye responsklasser.")
    lines.append("I stedet samles eksisterende placement-landskap til en eksplisitt aktivt-sett-taksonomi.")
    lines.append("")
    lines.append("## Seed taxonomy")
    lines.append("")
    lines.extend(
        table(
            seed_rows,
            (
                "growth_seed",
                "landscape_class",
                "active_placements",
                "covered_by_v15do_two_type_space",
                "p0_established_rate",
                "p1_established_rate",
                "p2_established_rate",
                "support_signatures",
            ),
        )
    )
    lines.append("")
    lines.append("## Taxonomy summary")
    lines.append("")
    lines.extend(
        table(
            taxonomy_rows,
            (
                "landscape_class",
                "n_seeds",
                "growth_seeds",
                "old_v15do_type_space",
                "median_p0_established_rate",
                "median_p1_established_rate",
                "median_p2_established_rate",
            ),
        )
    )
    lines.append("")
    lines.append("## Pre-run contrast families")
    lines.append("")
    lines.extend(table(family_rows, ("feature_family", "evidence_strength", "n_contrasts", "n_clean_current_sample", "clean_rate", "example_clean_features")))
    lines.append("")
    lines.append("## Repeated-class descriptive contrasts")
    lines.append("")
    if repeated_pair_clean:
        lines.extend(
            table(
                repeated_pair_clean,
                (
                    "left_type",
                    "right_type",
                    "feature",
                    "feature_family",
                    "direction",
                    "left_median",
                    "right_median",
                ),
                limit=24,
            )
        )
    else:
        lines.append("No clean repeated-pair contrasts in this tiny sample.")
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- `none` og `single_active_p0` maa inn i type-rommet foer nye selector-claims.")
    lines.append("- Repeated classes (`single_active_p1`, `multi_active_p0_p2`) kan brukes til deskriptive contrasts, men ikke som validert lov.")
    lines.append("- Singleton classes er viktige som taxonomisk varsellampe, men kan ikke laere en robust mapper alene.")
    lines.append("- Ikke oppgrader dette til Lorentz-, invariant-, entanglement-, partikkel- eller universell geometri-evidens.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dq", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit v15do/v15dp-guarden.")
    lines.append("- Ikke tren selector paa singleton-klassene.")
    lines.append("- Neste dynamiske budsjett bor vaere taxonomy-mapping eller flere fresh seeds, ikke ny single-guard finpuss.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dq",
            "",
            "Denne runden kjoerte ikke nye simulasjoner. Den samlet resultatene vi allerede hadde for aa se hvilke respons-typer som faktisk finnes.",
            "",
            "Det smarte grepet er at naar en regel feiler fordi verden har flere typer enn regelen kjenner til, skal vi ikke justere regelen. Vi maa forst tegne kartet bedre.",
            "",
            f"- Hovedlesning: `{diag['taxonomy_scope']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er fortsatt lokal defect/response-kartlegging, ikke en paastand om ferdig fysikk.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dq active-set taxonomy synthesis.")
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dq_active_set_taxonomy_placement_rows.csv"))
    p.add_argument("--out-seed-csv", default=str(DOC / "v15dq_active_set_taxonomy_seed_summary.csv"))
    p.add_argument("--out-taxonomy-csv", default=str(DOC / "v15dq_active_set_taxonomy_class_summary.csv"))
    p.add_argument("--out-seed-features-csv", default=str(DOC / "v15dq_active_set_taxonomy_seed_features.csv"))
    p.add_argument("--out-pairwise-csv", default=str(DOC / "v15dq_active_set_taxonomy_pairwise_type_contrasts.csv"))
    p.add_argument("--out-family-csv", default=str(DOC / "v15dq_active_set_taxonomy_feature_family_summary.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dq_active_set_taxonomy_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dq_active_set_taxonomy_synthesis.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dq_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dq.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placement_rows = load_placement_rows()
    seed_rows = seed_summary_rows(placement_rows)
    taxonomy_rows = taxonomy_summary_rows(seed_rows)
    seed_features = seed_feature_rows(seed_rows, placement_rows)
    pairwise_rows = pairwise_type_contrast_rows(seed_features)
    family_rows = feature_family_summary_rows(pairwise_rows)
    guard_eval = read_csv(V15DP_GUARD_EVAL_CSV)
    diagnosis = diagnosis_rows(
        seed_rows=seed_rows,
        taxonomy_rows=taxonomy_rows,
        pairwise_rows=pairwise_rows,
        guard_eval=guard_eval,
    )

    write_csv(Path(args.out_placement_csv), placement_rows)
    write_csv(Path(args.out_seed_csv), seed_rows)
    write_csv(Path(args.out_taxonomy_csv), taxonomy_rows)
    write_csv(Path(args.out_seed_features_csv), seed_features)
    write_csv(Path(args.out_pairwise_csv), pairwise_rows)
    write_csv(Path(args.out_family_csv), family_rows)
    write_csv(Path(args.out_diagnosis_csv), diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            seed_rows=seed_rows,
            taxonomy_rows=taxonomy_rows,
            family_rows=family_rows,
            pairwise_rows=pairwise_rows,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")
    print(f"wrote {args.out_summary_md}")
    print(f"wrote {args.out_diagnosis_csv}")


if __name__ == "__main__":
    main()
