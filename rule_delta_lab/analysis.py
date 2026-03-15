"""Invariant analysis and Markdown reporting for the rule-delta lab."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Sequence

import numpy as np

from .features import CORE_FEATURES, MOTIF_FEATURES, REDUCED_FEATURES


RULESET_LIBRARY: Dict[str, List[str]] = {
    "closed_topological": ["seed", "swap"],
    "open_topological": ["seed", "triad", "delete", "swap"],
    "fully_open_linear": ["seed", "triad", "delete", "swap", "birth", "death"],
}


@dataclass(frozen=True)
class TheoremRow:
    """Exact, non-empirical statement about one primitive rule."""

    rule: str
    delta_core: Dict[str, float]
    delta_motif: Dict[str, float | None]
    note: str


def markdown_table(rows: Sequence[Sequence[str]]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    separator = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join([header, separator, body])


def core_delta_vector(delta_core: Dict[str, float]) -> np.ndarray:
    return np.array([float(delta_core.get(name, 0.0)) for name in CORE_FEATURES], dtype=float)


def nullspace_basis(matrix: np.ndarray, atol: float = 1e-10) -> np.ndarray:
    if matrix.size == 0:
        return np.eye(0)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int((singular_values > atol).sum())
    return vh[rank:].T


def format_nullspace_basis(basis: np.ndarray, feature_names: Sequence[str], tol: float = 1e-9) -> List[str]:
    if basis.size == 0 or basis.shape[1] == 0:
        return ["ingen"]
    rows = []
    for index in range(basis.shape[1]):
        column = basis[:, index]
        terms = [f"{column[i]:+.3f}·{feature_names[i]}" for i in range(len(feature_names)) if abs(column[i]) > tol]
        rows.append(" ".join(terms) if terms else "0")
    return rows


def invariant_classification_markdown(theorem_rows: Sequence[TheoremRow]) -> str:
    rows = [["regel", "Δtokens", "Δnodes", "Δcomponents", "Δbeta1", "merknad"]]
    for theorem in theorem_rows:
        rows.append(
            [
                theorem.rule,
                f"{theorem.delta_core.get('tokens', 0.0):.0f}",
                f"{theorem.delta_core.get('nodes', 0.0):.0f}",
                f"{theorem.delta_core.get('components', 0.0):.0f}",
                f"{theorem.delta_core.get('beta1', 0.0):.0f}",
                theorem.note,
            ]
        )

    lines = [
        "## Teorem og identiteter",
        "",
        "### Primitive regler og eksakte lineære inkrementer i kjernebasis",
        "",
        markdown_table(rows),
        "",
        "En lineær kombinasjon `I = c·F_core` er eksakt invariant dersom `ΔF_rule · c = 0` for alle regler i den valgte regelklassen.",
        "",
    ]

    theorem_lookup = {theorem.rule: theorem for theorem in theorem_rows}
    for label, rule_names in RULESET_LIBRARY.items():
        matrix = np.vstack([core_delta_vector(theorem_lookup[name].delta_core) for name in rule_names])
        basis = nullspace_basis(matrix)
        lines.extend(
            [
                f"### Regelsett: `{label}`",
                "",
                f"Regler: {', '.join(rule_names)}",
                "",
                f"Invariantrommets dimensjon: {basis.shape[1]}",
                "",
            ]
        )
        for pretty in format_nullspace_basis(basis, CORE_FEATURES):
            lines.append(f"- {pretty}")
        lines.append("")
    return "\n".join(lines)


def motif_formula_markdown() -> str:
    note_rows = [
        ["seed", "h", "0", "C(h,2)"],
        ["triad", "d_v + d_w", "c", "C(d_v,2) + C(d_w,2)"],
        ["delete", "-[(d_v-1)+(d_u-1)]", "-c", "-[C(d_v-1,2)+C(d_u-1,2)]"],
        ["swap", "-(d_u-1)+d_w", "-c_del + (c_add - 1)", "-C(d_u-1,2)+C(d_w,2)"],
    ]
    return "\n".join(
        [
            "### Eksakte motivformler",
            "",
            "Formlene under er lokale identiteter for dagens implementasjon. De er ikke numeriske estimater.",
            "",
            markdown_table([["regel", "Δwedges", "Δtriangles", "Δstar3"]] + note_rows),
            "",
            "Merk spesielt at `swap` gir `Δtriangles = -c_del + (c_add - 1)`. `-1`-leddet kommer av at den nye kanten `(source, target)` deler destinasjonsnoden som felles nabo før den gamle kanten fjernes.",
            "",
        ]
    )


def summarise_events(event_rows: Sequence[Dict[str, Any]]) -> str:
    counts: Dict[str, int] = {}
    for row in event_rows:
        event = str(row["event"])
        counts[event] = counts.get(event, 0) + 1
    rows = [["event", "count"]] + [[event, str(counts[event])] for event in sorted(counts)]
    return markdown_table(rows)


def mean_delta_tables(event_rows: Sequence[Dict[str, Any]]) -> tuple[str, str]:
    if not event_rows:
        return "", ""
    deltas = np.array([[float(row[f"d_{name}"]) for name in REDUCED_FEATURES] for row in event_rows], dtype=float)
    std = deltas.std(axis=0)
    std[std == 0.0] = 1.0
    grouped: Dict[str, List[int]] = {}
    for index, row in enumerate(event_rows):
        grouped.setdefault(str(row["event"]), []).append(index)

    raw_rows = [["event"] + REDUCED_FEATURES]
    z_rows = [["event"] + REDUCED_FEATURES]
    for event in sorted(grouped):
        indices = grouped[event]
        mean_raw = deltas[indices].mean(axis=0)
        mean_z = (deltas[indices] / std).mean(axis=0)
        raw_rows.append([event] + [f"{value:.4g}" for value in mean_raw])
        z_rows.append([event] + [f"{value:.4g}" for value in mean_z])
    return markdown_table(raw_rows), markdown_table(z_rows)


def empirical_rule_matrix(event_rows: Sequence[Dict[str, Any]], event_filter: Sequence[str]) -> np.ndarray:
    rows = []
    for event in event_filter:
        subset = [row for row in event_rows if row["event"] == event]
        if not subset:
            rows.append(np.zeros(len(CORE_FEATURES)))
            continue
        matrix = np.array([[float(row[f"d_{name}"]) for name in CORE_FEATURES] for row in subset], dtype=float)
        rows.append(matrix.mean(axis=0))
    return np.array(rows, dtype=float)


def contextual_formula_residuals(event_rows: Sequence[Dict[str, Any]]) -> str:
    rows = [["event", "feature", "n", "mean_abs_residual", "max_abs_residual"]]
    for event in ["seed", "triad", "delete", "swap"]:
        for feature in MOTIF_FEATURES:
            residuals = []
            for row in event_rows:
                if row["event"] != event:
                    continue
                predicted = row.get(f"pred_{feature}")
                if predicted in ("", None):
                    continue
                residuals.append(abs(float(row[f"d_{feature}"]) - float(predicted)))
            if residuals:
                rows.append(
                    [
                        event,
                        feature,
                        str(len(residuals)),
                        f"{float(np.mean(residuals)):.6g}",
                        f"{float(np.max(residuals)):.6g}",
                    ]
                )
            else:
                rows.append([event, feature, "0", "nan", "nan"])
    return markdown_table(rows)


def build_markdown_report(
    args: Any,
    event_rows: Sequence[Dict[str, Any]],
    csv_path: str,
    theorem_rows: Sequence[TheoremRow],
) -> str:
    raw_table, z_table = mean_delta_tables(event_rows)

    lines = [
        "# Rule-delta lab v0.4",
        "",
        "## Metode",
        "",
        "Denne rapporten skiller eksplisitt mellom:",
        "",
        "1. algebraiske identiteter i feature-rommet,",
        "2. eksakte lineære invariants som følger av primitive regler,",
        "3. og numeriske observasjoner i en konkret kjøring.",
        "",
        "## Kjøringsparametre",
        "",
        f"- steps: {args.steps}",
        f"- seed: {args.seed}",
        f"- r_seed: {args.r_seed}",
        f"- r_token: {args.r_token}",
        f"- r_birth: {args.r_birth}",
        f"- r_death: {args.r_death}",
        f"- p_triad: {args.p_triad}",
        f"- p_del: {args.p_del}",
        f"- p_swap: {args.p_swap}",
        f"- avoid_disconnect: {args.avoid_disconnect}",
        f"- relocate_tokens: {args.relocate_tokens}",
        "",
        "## Algebraiske identiteter",
        "",
        "- `beta1 = edges - nodes + components`",
        "- `deg_sq_sum = 2*wedges + 2*edges`",
        "",
        "Herfra følger at `edges` og `deg_sq_sum` ikke skal behandles som uavhengige dynamiske observabler i den reduserte basisen.",
        "",
        invariant_classification_markdown(theorem_rows),
        motif_formula_markdown(),
        "## Numeriske observasjoner",
        "",
        "### Hendelsesfordeling",
        "",
        summarise_events(event_rows),
        "",
        "### Empirisk middelmatrise i redusert basis",
        "",
        raw_table,
        "",
        "### Standardisert middelmatrise",
        "",
        "Denne tabellen er z-skalert per feature over hele hendelsesmatrisen. Den skal brukes til å kontrollere for rene skalaeffekter.",
        "",
        z_table,
        "",
    ]

    active_rules = [event for event in ["seed", "birth", "death", "triad", "delete", "swap"] if any(row["event"] == event for row in event_rows)]
    if active_rules:
        empirical = empirical_rule_matrix(event_rows, active_rules)
        basis = nullspace_basis(empirical)
        rows = [["regel"] + CORE_FEATURES]
        for event, vector in zip(active_rules, empirical):
            rows.append([event] + [f"{value:.4g}" for value in vector])
        lines.extend(
            [
                "### Empirisk kjernebasis for aktive regler",
                "",
                markdown_table(rows),
                "",
                "Empirisk nullromsbasis:",
                "",
            ]
        )
        for pretty in format_nullspace_basis(basis, CORE_FEATURES):
            lines.append(f"- {pretty}")
        lines.append("")

    lines.extend(
        [
            "### Residualtest for eksakte motivformler",
            "",
            contextual_formula_residuals(event_rows),
            "",
            "## Tolkning",
            "",
            "### Teorem/identitet",
            "",
            "- Redusert basis kvotienterer ut de to innebygde grafidentitetene.",
            "- Nullrommene i kjernebasis er eksakte utsagn om primitive regelklasser, ikke data-tilpassede observasjoner.",
            "",
            "### Numerisk observasjon",
            "",
            "- De empiriske middelmatrisene viser hvilke features som faktisk driver i denne konkrete parameterkonteksten.",
            "- Standardisert analyse skiller stor absolutt skala fra robust strukturell dominans.",
            "",
            "### Spekulativ fortolkning",
            "",
            "- `c4`, `spectral_radius`, `clustering` og `dim_proxy` er fortsatt regimevariabler. De kan bli quasi-invarianter i bestemte regimer, men det følger ikke av reglene alene.",
            "",
            "## Videre arbeid",
            "",
            "- Knytt regelobjektene til en eksplisitt perturbasjonslab med kopla kjøringer.",
            "- Mål causal-cone-lignende spredning i grafdistanse og hendelsestid.",
            "",
            f"_CSV med rå hendelsesdata: `{csv_path}`_",
            "",
        ]
    )
    return "\n".join(lines)
