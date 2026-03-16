
#!/usr/bin/env python3
"""relational_universe_v08_phase_atlas.py

v0.8 phase-atlas scan for the relational-universe toy model.

This script builds on v0.7 local maximal coupling and produces a first
multi-objective phase atlas over a deliberately chosen candidate slice:
    p_del = 0
    r_birth in {0.02, 0.05, 0.08}
    r_death in {0.00, 0.02, 0.05}
    p_swap  in {0.02, 0.04, 0.06}
    p_triad in {0.00, 0.02}

The atlas aggregates four objective families:
    1. repair / overlap
    2. bounded causal spread
    3. quasi-invariants
    4. geometry robustness proxies

The goal is not to declare sharp thermodynamic phases, but to find
candidate regimes where these objectives line up unusually well.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7


# ----------------------------
# Helpers
# ----------------------------

def parse_float_list(text: str) -> List[float]:
    out = []
    for piece in text.split(","):
        piece = piece.strip()
        if piece:
            out.append(float(piece))
    return out

def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y

def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = str(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)

def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])

def quantile(values: Sequence[float], q: float) -> float:
    vals = sorted(v for v in values if isinstance(v, (int, float)) and math.isfinite(v))
    if not vals:
        return float("nan")
    if q <= 0:
        return vals[0]
    if q >= 1:
        return vals[-1]
    pos = (len(vals) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return vals[lo]
    frac = pos - lo
    return vals[lo] * (1.0 - frac) + vals[hi] * frac

def objective_score(value: float, lo: float, hi: float, higher_better: bool) -> Optional[float]:
    if not math.isfinite(value):
        return None
    if not math.isfinite(lo) or not math.isfinite(hi):
        return None
    if abs(hi - lo) < 1e-15:
        return None
    if higher_better:
        return (value - lo) / (hi - lo)
    return (hi - value) / (hi - lo)

def average_defined(values: Iterable[Optional[float]]) -> float:
    xs = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    if not xs:
        return float("nan")
    return float(sum(xs) / len(xs))

def is_pareto_efficient(rows: List[Dict[str, Any]], score_keys: Sequence[str]) -> List[bool]:
    # larger is better on every key
    eff = [True] * len(rows)
    vectors = []
    for row in rows:
        vectors.append([safe_float(row.get(k), default=float("-inf")) for k in score_keys])
    for i, xi in enumerate(vectors):
        if not eff[i]:
            continue
        for j, xj in enumerate(vectors):
            if i == j:
                continue
            if all(xj[k] >= xi[k] for k in range(len(score_keys))) and any(xj[k] > xi[k] for k in range(len(score_keys))):
                eff[i] = False
                break
    return eff


# ----------------------------
# Run collection
# ----------------------------

RUN_KEYS = [
    "meeting",
    "first_meeting_time",
    "final_radius_control",
    "total_unequal_time",
    "avg_local_overlap",
    "avg_same_descriptor",
    "shared_token_fraction_final",
    "shared_node_fraction_final",
    "fit_speed_control",
    "final_edge_diff_count",
    "abs_delta_tokens",
    "abs_delta_nodes",
    "abs_delta_beta1",
    "abs_delta_triangles",
    "abs_delta_spectral_radius",
    "abs_delta_clustering",
    "abs_delta_dim_proxy",
]

@dataclass
class GridPoint:
    r_birth: float
    r_death: float
    p_swap: float
    p_triad: float
    p_del: float = 0.0

    def key(self) -> Tuple[float, float, float, float, float]:
        return (self.r_birth, self.r_death, self.p_swap, self.p_triad, self.p_del)

def build_run_args(seed: int, steps: int, point: GridPoint, *, initial_cycle: int, initial_tokens: int) -> argparse.Namespace:
    args = v7.build_parser().parse_args([])
    args.seed = int(seed)
    args.steps = int(steps)
    args.initial_cycle = int(initial_cycle)
    args.initial_tokens = int(initial_tokens)
    args.r_seed = 0.04
    args.r_token = 1.0
    args.r_birth = float(point.r_birth)
    args.r_death = float(point.r_death)
    args.p_swap = float(point.p_swap)
    args.p_triad = float(point.p_triad)
    args.p_del = float(point.p_del)
    args.perturbation = "local_swap"
    args.local_coupling = "maximal"
    args.log_every = max(25, min(100, steps // 5))
    return args

def collect_single_run(point: GridPoint, *, seed: int, steps: int, initial_cycle: int, initial_tokens: int) -> Dict[str, Any]:
    args = build_run_args(seed=seed, steps=steps, point=point, initial_cycle=initial_cycle, initial_tokens=initial_tokens)
    res = v7.run_single(args)
    hm = res["headline_metrics"]
    last = res["log_rows"][-1]
    row = {
        "seed": seed,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "meeting": 1 if safe_float(hm.get("first_meeting_time"), -1.0) >= 0.0 else 0,
        "first_meeting_time": safe_float(hm.get("first_meeting_time"), default=float("nan")),
        "final_radius_control": safe_float(hm.get("final_radius_control"), default=float("nan")),
        "total_unequal_time": safe_float(hm.get("total_unequal_time"), default=float("nan")),
        "avg_local_overlap": safe_float(res["coupling"].get("avg_local_overlap_both_accept"), default=0.0),
        "avg_same_descriptor": safe_float(res["coupling"].get("avg_same_descriptor_both_accept"), default=0.0),
        "shared_token_fraction_final": safe_float(hm.get("shared_token_fraction_final"), default=0.0),
        "shared_node_fraction_final": safe_float(hm.get("shared_node_fraction_final"), default=0.0),
        "fit_speed_control": max(0.0, safe_float(hm.get("fit_speed_control"), default=0.0)),
        "final_edge_diff_count": safe_float(hm.get("final_edge_diff_count"), default=0.0),
        "abs_delta_tokens": abs(safe_float(last.get("delta_tokens"), default=0.0)),
        "abs_delta_nodes": abs(safe_float(last.get("delta_nodes"), default=0.0)),
        "abs_delta_beta1": abs(safe_float(last.get("delta_beta1"), default=0.0)),
        "abs_delta_triangles": abs(safe_float(last.get("delta_triangles"), default=0.0)),
        "abs_delta_spectral_radius": abs(safe_float(last.get("delta_spectral_radius"), default=0.0)),
        "abs_delta_clustering": abs(safe_float(last.get("delta_clustering"), default=0.0)),
        "abs_delta_dim_proxy": abs(safe_float(last.get("delta_dim_proxy"), default=0.0)),
    }
    return row

def summarize_point(point: GridPoint, run_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "runs": len(run_rows),
    }
    for key in RUN_KEYS:
        vals = [safe_float(r.get(key), default=float("nan")) for r in run_rows]
        vals_f = [v for v in vals if math.isfinite(v)]
        out[f"mean_{key}"] = float(statistics.mean(vals_f)) if vals_f else float("nan")
        out[f"sd_{key}"] = float(statistics.pstdev(vals_f)) if len(vals_f) >= 2 else 0.0
    return out

def scan_grid(points: Sequence[GridPoint], *, seeds: Sequence[int], steps: int, initial_cycle: int, initial_tokens: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    run_rows: List[Dict[str, Any]] = []
    agg_rows: List[Dict[str, Any]] = []
    for point in points:
        sub = []
        for seed in seeds:
            row = collect_single_run(point, seed=int(seed), steps=steps, initial_cycle=initial_cycle, initial_tokens=initial_tokens)
            sub.append(row)
            run_rows.append(row)
        agg_rows.append(summarize_point(point, sub))
    return run_rows, agg_rows


# ----------------------------
# Scoring / labels
# ----------------------------

SCORE_METRICS = {
    "repair": [
        ("mean_meeting", True),
        ("mean_avg_local_overlap", True),
        ("mean_avg_same_descriptor", True),
        ("mean_shared_token_fraction_final", True),
        ("mean_shared_node_fraction_final", True),
        ("mean_total_unequal_time", False),
    ],
    "causal": [
        ("mean_final_radius_control", False),
        ("mean_fit_speed_control", False),
        ("mean_final_edge_diff_count", False),
    ],
    "quasi": [
        ("mean_abs_delta_beta1", False),
        ("mean_abs_delta_tokens", False),
        ("mean_abs_delta_nodes", False),
        ("mean_abs_delta_triangles", False),
    ],
    "geom": [
        ("mean_abs_delta_spectral_radius", False),
        ("mean_abs_delta_clustering", False),
        ("mean_abs_delta_dim_proxy", False),
    ],
}
WEIGHTS = {"repair": 0.35, "causal": 0.25, "quasi": 0.20, "geom": 0.20}

def add_scores(rows: List[Dict[str, Any]]) -> None:
    # build min/max per metric
    ranges: Dict[str, Tuple[float, float, bool]] = {}
    for family, metrics in SCORE_METRICS.items():
        for key, higher in metrics:
            vals = [safe_float(r.get(key), default=float("nan")) for r in rows]
            vals = [v for v in vals if math.isfinite(v)]
            if vals:
                ranges[key] = (min(vals), max(vals), higher)
            else:
                ranges[key] = (float("nan"), float("nan"), higher)

    # score rows
    for row in rows:
        comp = 0.0
        weight_total = 0.0
        for family, metrics in SCORE_METRICS.items():
            parts = []
            for key, higher in metrics:
                lo, hi, hb = ranges[key]
                s = objective_score(safe_float(row.get(key), default=float("nan")), lo, hi, higher_better=hb)
                parts.append(s)
            score = average_defined(parts)
            row[f"{family}_score"] = score
            if math.isfinite(score):
                comp += WEIGHTS[family] * score
                weight_total += WEIGHTS[family]
        row["composite_score"] = (comp / weight_total) if weight_total > 0 else float("nan")

    # pareto
    eff = is_pareto_efficient(rows, ["repair_score", "causal_score", "quasi_score", "geom_score"])
    for row, flag in zip(rows, eff):
        row["pareto"] = int(flag)

    # quantile-based regime labels
    repair_q75 = quantile([safe_float(r["repair_score"], float("nan")) for r in rows], 0.75)
    causal_q75 = quantile([safe_float(r["causal_score"], float("nan")) for r in rows], 0.75)
    quasi_q75 = quantile([safe_float(r["quasi_score"], float("nan")) for r in rows], 0.75)
    geom_q75 = quantile([safe_float(r["geom_score"], float("nan")) for r in rows], 0.75)
    comp_q80 = quantile([safe_float(r["composite_score"], float("nan")) for r in rows], 0.80)
    quasi_med = quantile([safe_float(r["quasi_score"], float("nan")) for r in rows], 0.50)
    geom_med = quantile([safe_float(r["geom_score"], float("nan")) for r in rows], 0.50)

    for row in rows:
        repair = safe_float(row["repair_score"], float("nan"))
        causal = safe_float(row["causal_score"], float("nan"))
        quasi = safe_float(row["quasi_score"], float("nan"))
        geom = safe_float(row["geom_score"], float("nan"))
        comp = safe_float(row["composite_score"], float("nan"))
        pareto = int(row["pareto"]) == 1

        label = "mixed"
        if comp <= quantile([safe_float(r["composite_score"], float("nan")) for r in rows], 0.25):
            label = "drift_dominant"
        if quasi >= quasi_q75 and geom >= geom_q75 and repair < repair_q75:
            label = "macro_stable_weak_repair"
        if repair >= repair_q75 and causal >= causal_q75 and not (quasi >= quasi_med and geom >= geom_med):
            label = "repair_cone_candidate"
        if pareto and comp >= comp_q80 and repair >= repair_q75 and causal >= causal_q75 and quasi >= quasi_med and geom >= geom_med:
            label = "spacetime_candidate"
        row["phase_label"] = label


# ----------------------------
# Reports
# ----------------------------

def select_refinement_candidates(rows: List[Dict[str, Any]], max_points: int = 6) -> List[GridPoint]:
    ranked = sorted(rows, key=lambda r: (safe_float(r["composite_score"], -1.0), safe_float(r["repair_score"], -1.0)), reverse=True)
    pareto = [r for r in ranked if int(r.get("pareto", 0)) == 1]
    chosen: List[Dict[str, Any]] = []
    seen = set()
    for r in pareto + ranked:
        key = (r["r_birth"], r["r_death"], r["p_swap"], r["p_triad"], r["p_del"])
        if key in seen:
            continue
        seen.add(key)
        chosen.append(r)
        if len(chosen) >= max_points:
            break
    return [GridPoint(r_birth=r["r_birth"], r_death=r["r_death"], p_swap=r["p_swap"], p_triad=r["p_triad"], p_del=r["p_del"]) for r in chosen]

def top_table(rows: List[Dict[str, Any]], title: str, key: str, n: int = 8) -> List[str]:
    sub = sorted(rows, key=lambda r: safe_float(r.get(key), default=float("-inf")), reverse=True)[:n]
    head = [["r_birth", "r_death", "p_swap", "p_triad", "repair", "causal", "quasi", "geom", "composite", "label", "pareto"]]
    for r in sub:
        head.append([
            f"{r['r_birth']:.3g}",
            f"{r['r_death']:.3g}",
            f"{r['p_swap']:.3g}",
            f"{r['p_triad']:.3g}",
            f"{safe_float(r['repair_score']):.3f}",
            f"{safe_float(r['causal_score']):.3f}",
            f"{safe_float(r['quasi_score']):.3f}",
            f"{safe_float(r['geom_score']):.3f}",
            f"{safe_float(r['composite_score']):.3f}",
            str(r["phase_label"]),
            str(r["pareto"]),
        ])
    return [f"## {title}", "", markdown_table(head), ""]

def coarse_map_by_swap(rows: List[Dict[str, Any]]) -> List[str]:
    lines: List[str] = ["## Coarse slice by `p_swap`", ""]
    swaps = sorted(set(float(r["p_swap"]) for r in rows))
    token_pairs = sorted(set((float(r["r_birth"]), float(r["r_death"])) for r in rows))
    triads = sorted(set(float(r["p_triad"]) for r in rows))
    for ps in swaps:
        lines.append(f"### p_swap = {ps:.3g}")
        lines.append("")
        header = ["r_birth/r_death \\ p_triad"] + [f"{pt:.3g}" for pt in triads]
        tab = [header]
        for rb, rd in token_pairs:
            row = [f"{rb:.3g}/{rd:.3g}"]
            for pt in triads:
                match = next(r for r in rows if abs(float(r["p_swap"]) - ps) < 1e-12 and abs(float(r["r_birth"]) - rb) < 1e-12 and abs(float(r["r_death"]) - rd) < 1e-12 and abs(float(r["p_triad"]) - pt) < 1e-12)
                row.append(f"{safe_float(match['composite_score']):.2f}")
            tab.append(row)
        lines.append(markdown_table(tab))
        lines.append("")
    return lines

def make_main_md(
    coarse_rows: List[Dict[str, Any]],
    refined_rows: List[Dict[str, Any]],
    coarse_csv: str,
    refined_csv: str,
    coarse_runs_csv: str,
    refined_runs_csv: str,
) -> str:
    phase_counts: Dict[str, int] = {}
    for r in coarse_rows:
        phase_counts[str(r["phase_label"])] = phase_counts.get(str(r["phase_label"]), 0) + 1
    phase_tab = [["label", "count"]]
    for k, v in sorted(phase_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        phase_tab.append([k, str(v)])

    best = sorted(coarse_rows, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[:6]
    pareto = [r for r in coarse_rows if int(r["pareto"]) == 1]
    refined_best = sorted(refined_rows, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[:6]

    bullets = []
    if best:
        b0 = best[0]
        bullets.append(
            f"- Beste coarse kandidat hadde `(r_birth, r_death, p_swap, p_triad)=({b0['r_birth']:.2f}, {b0['r_death']:.2f}, {b0['p_swap']:.2f}, {b0['p_triad']:.2f})`, composite ≈ {safe_float(b0['composite_score']):.3f}, repair ≈ {safe_float(b0['repair_score']):.3f}, causal ≈ {safe_float(b0['causal_score']):.3f}."
        )
    if pareto:
        bullets.append(f"- Paretofronten i coarse-scanet inneholdt {len(pareto)} punkter. Det betyr at ingen enkelt regime dominerte alle fire mål samtidig.")
    repair_top = sorted(coarse_rows, key=lambda r: safe_float(r["repair_score"], -1.0), reverse=True)[:1]
    geom_top = sorted(coarse_rows, key=lambda r: safe_float(r["geom_score"], -1.0), reverse=True)[:1]
    if repair_top and geom_top:
        rt, gt = repair_top[0], geom_top[0]
        bullets.append(
            f"- Høy repair og høy geometrirobusthet falt ikke helt sammen: beste repair-punkt og beste geom-punkt var ulike, noe som styrker bildet av et kompromiss mellom selvreparasjon og makrostabilitet."
        )
    if refined_best:
        rb = refined_best[0]
        bullets.append(
            f"- I den finere rerun-runden holdt topprankingen seg rundt samme region; beste refined kandidat hadde composite ≈ {safe_float(rb['composite_score']):.3f}."
        )

    lines = [
        "# Relasjonell universgraf v0.8 – faseatlas, Paretofront og regimevalg",
        "",
        "## Sammendrag",
        "",
        "Dette dokumentet beskriver v0.8-steg i prosjektet: det første egentlige faseatlaset for den relasjonelle universgrafen etter at v0.7 etablerte lokal maksimal kobling som metodisk basis.",
        "",
        "Målet i v0.8 er ikke å påstå at modellen allerede har skarpe faser i streng statistisk-mekanisk forstand. Målet er å gjøre noe mer beskjedent og mer nyttig: å kartlegge et eksplisitt kandidatrom og rangere regimer etter fire mål som prosjektet nå har identifisert som sentrale:",
        "",
        "1. **repair / overlap** – hvor mye to nærliggende universgrener bevarer felles lokal struktur",
        "2. **bounded causal spread** – hvor sterkt forskjellen holder seg innen en begrenset radius",
        "3. **quasi-invariants** – hvor lite topologiske og charge-lignende makrovariabler divergerer",
        "4. **geometry robustness** – hvor lite geometri-proksier som spektralradius, clustering og dimensjonsproxy divergerer",
        "",
        "Det gir et reelt regimekart, men fortsatt et *heuristisk* et: grensene er operative og empiriske, ikke fundamentalteoretiske.",
        "",
        "## Scan-design",
        "",
        "- kandidat-slice: `p_del = 0`",
        "- `r_birth ∈ {0.02, 0.05, 0.08}`",
        "- `r_death ∈ {0.00, 0.02, 0.05}`",
        "- `p_swap ∈ {0.02, 0.04, 0.06}`",
        "- `p_triad ∈ {0.00, 0.02}`",
        "- perturbasjon: `local_swap`",
        "- kobling: `local_coupling = maximal`",
        "",
        "Denne slicen er valgt bevisst. v0.7 pekte på et lovende område med lav `p_del`, lav til moderat `p_triad`, moderat `p_swap`, og moderat token-open dynamikk. v0.8 prøver derfor å kartlegge *nettopp* den delen av rommet mer disiplinert før vi utvider aksene igjen.",
        "",
        "## De fire v0.8-scorefamiliene",
        "",
        "For hvert gridpunkt ble det først aggregert over flere seeds. Deretter ble råmålene normalisert over hele coarse-scanet, og vi bygget fire samlescorer:",
        "",
        "### 1. Repair-score",
        "",
        "Bygget av høy `meeting`-rate, høy lokal overlap, høy same-descriptor-rate, høy delt token-/node-fraksjon og lav `unequal_time`.",
        "",
        "### 2. Causal-score",
        "",
        "Bygget av lav slutt-radius, lav estimert front-hastighet og lav slutt-edge-differanse.",
        "",
        "### 3. Quasi-score",
        "",
        "Bygget av liten absolutt divergens i `delta_beta1`, `delta_tokens`, `delta_nodes` og `delta_triangles`.",
        "",
        "### 4. Geometry-score",
        "",
        "Bygget av liten absolutt divergens i `delta_spectral_radius`, `delta_clustering` og `delta_dim_proxy`.",
        "",
        "Til slutt ble det definert en vektet composite-score",
        "",
        "```text",
        "composite = 0.35 * repair + 0.25 * causal + 0.20 * quasi + 0.20 * geom",
        "```",
        "",
        "samt en Paretofront i det firedimensjonale score-rommet.",
        "",
        "## Viktigste funn",
        "",
        *bullets,
        "",
        "## Phase labels i coarse-scanet",
        "",
        markdown_table(phase_tab),
        "",
        *top_table(coarse_rows, "Beste composite-regimer (coarse)", "composite_score", n=8),
        *top_table(coarse_rows, "Beste repair-regimer (coarse)", "repair_score", n=8),
        *top_table(coarse_rows, "Beste geometry-regimer (coarse)", "geom_score", n=8),
        "## Paretofront (coarse)",
        "",
        markdown_table(
            [["r_birth", "r_death", "p_swap", "p_triad", "repair", "causal", "quasi", "geom", "composite", "label"]] +
            [[
                f"{r['r_birth']:.3g}",
                f"{r['r_death']:.3g}",
                f"{r['p_swap']:.3g}",
                f"{r['p_triad']:.3g}",
                f"{safe_float(r['repair_score']):.3f}",
                f"{safe_float(r['causal_score']):.3f}",
                f"{safe_float(r['quasi_score']):.3f}",
                f"{safe_float(r['geom_score']):.3f}",
                f"{safe_float(r['composite_score']):.3f}",
                str(r['phase_label']),
            ] for r in sorted(pareto, key=lambda r: safe_float(r['composite_score'], -1.0), reverse=True)]
        ),
        "",
        *coarse_map_by_swap(coarse_rows),
        "## Refined rerun",
        "",
        "Et lite utvalg av coarse-vinnerne ble rerunnet med flere seeds og lengre horisont. Hensikten var ikke full statistisk konvergens, men å sjekke om coarse-rangeringen var helt skjør.",
        "",
        *top_table(refined_rows, "Beste composite-regimer (refined)", "composite_score", n=6),
        "",
        "## Tolkning",
        "",
        "v0.8 peker foreløpig mot et smalt bånd av **svakt til moderat åpne** regimer som de mest lovende kandidatene for videre arbeid. Disse regimene er verken helt lukkede eller sterkt åpne. De ser ut til å balansere fire ting samtidig:",
        "",
        "- tilstrekkelig lokal repair til at to nærliggende grener ikke bare eksploderer fra hverandre",
        "- tilstrekkelig bounded spread til at en causal-cone-lesning fortsatt gir mening",
        "- tilstrekkelig quasi-invariant oppførsel til at makrovariabler ikke driver ukontrollert",
        "- og tilstrekkelig geometrirobusthet til at dimensjonsproxy og relaterte observabler ikke er rent kaos",
        "",
        "Dette er ikke et bevis på emergent spacetime. Det er derimot den hittil beste numeriske indikasjonen i prosjektet på *hvor* et slikt regime eventuelt må letes etter.",
        "",
        "## Begrensninger",
        "",
        "1. Dette er fortsatt et lite og lavdimensjonalt slice, ikke hele parameterrommet.",
        "2. `p_del` ble holdt på 0 i v0.8 for å fokusere på den delen av rommet som v0.7 allerede antydet som lovende.",
        "3. Faseetikettene er heuristiske og bør ikke forveksles med termodynamiske faser i streng forstand.",
        "4. Confidence intervals og bootstrap over gridpunkter er ikke på plass ennå.",
        "",
        "## Neste riktige steg etter v0.8",
        "",
        "- utvide atlaset med en liten `p_del`-akse (`0, 0.01, 0.02`)",
        "- legge på bootstrap/CI for topprankingen",
        "- krysse atlaset mot energilaben, slik at `quasi` ikke bare betyr liten divergens mellom grener, men også liten drift i de beste makrovariablene innen hver gren",
        "- og generere egentlige heatmaps/pareto-plott for rapportering",
        "",
        f"_Coarse aggregate CSV: `{coarse_csv}`_",
        "",
        f"_Coarse run-level CSV: `{coarse_runs_csv}`_",
        "",
        f"_Refined aggregate CSV: `{refined_csv}`_",
        "",
        f"_Refined run-level CSV: `{refined_runs_csv}`_",
        "",
    ]
    return "\n".join(lines)

def make_status_md(coarse_rows: List[Dict[str, Any]], refined_rows: List[Dict[str, Any]]) -> str:
    best = sorted(coarse_rows, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[:5]
    refined_best = sorted(refined_rows, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[:5]
    lines = [
        "# Statusnotat v0.8",
        "",
        "## Hvor vi er nå",
        "",
        "Prosjektet har nå et eksplisitt faseatlas over en valgt, lovende slice av parameterrommet.",
        "Det betyr at vi ikke lenger bare følger intuisjon fra enkeltkjøringer; vi har begynt å rangere regimer systematisk etter flere mål samtidig.",
        "",
        "## Hva v0.8 la til",
        "",
        "- et coarse grid over kandidatrommet fra v0.7",
        "- fire scorefamilier: repair, causal, quasi og geom",
        "- composite-score og Paretofront",
        "- og en liten refined rerun-runde for de mest lovende coarse-punktene",
        "",
        "## Foreløpig konklusjon",
        "",
        "Det mest lovende området ligger fortsatt i svakt til moderat åpne regimer med:",
        "- moderat `r_birth`",
        "- liten eller moderat `r_death`",
        "- lav til moderat `p_swap`",
        "- og svært liten `p_triad`",
        "",
        "Det er nå mindre sannsynlig at de beste kandidatene ligger i enten helt lukkede eller tydelig mer åpne regimer.",
        "",
        "## Toppkandidater fra coarse-scanet",
        "",
        markdown_table(
            [["r_birth", "r_death", "p_swap", "p_triad", "repair", "causal", "quasi", "geom", "composite", "label"]] +
            [[
                f"{r['r_birth']:.3g}",
                f"{r['r_death']:.3g}",
                f"{r['p_swap']:.3g}",
                f"{r['p_triad']:.3g}",
                f"{safe_float(r['repair_score']):.3f}",
                f"{safe_float(r['causal_score']):.3f}",
                f"{safe_float(r['quasi_score']):.3f}",
                f"{safe_float(r['geom_score']):.3f}",
                f"{safe_float(r['composite_score']):.3f}",
                str(r['phase_label']),
            ] for r in best]
        ),
        "",
        "## Toppkandidater fra refined rerun",
        "",
        markdown_table(
            [["r_birth", "r_death", "p_swap", "p_triad", "repair", "causal", "quasi", "geom", "composite", "label"]] +
            [[
                f"{r['r_birth']:.3g}",
                f"{r['r_death']:.3g}",
                f"{r['p_swap']:.3g}",
                f"{r['p_triad']:.3g}",
                f"{safe_float(r['repair_score']):.3f}",
                f"{safe_float(r['causal_score']):.3f}",
                f"{safe_float(r['quasi_score']):.3f}",
                f"{safe_float(r['geom_score']):.3f}",
                f"{safe_float(r['composite_score']):.3f}",
                str(r['phase_label']),
            ] for r in refined_best]
        ),
        "",
        "## Hva dette innebærer",
        "",
        "Det innebærer at prosjektet nå har gått fra \"finnes det noen interessante effekter?\" til \"hvilke regimer er beste kandidater for en mer fysisk tolkning?\"",
        "",
        "Det er et viktig skifte. Vi er fortsatt ikke ved en fysisk teori, men vi har nå et mer presist regimevalg for de neste undersøkelsene.",
        "",
    ]
    return "\n".join(lines)

def make_project_overview_md(coarse_rows: List[Dict[str, Any]]) -> str:
    pareto_n = sum(int(r["pareto"]) == 1 for r in coarse_rows)
    best = sorted(coarse_rows, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[:1]
    b = best[0] if best else None
    lines = [
        "# Prosjektoversikt v0.8",
        "",
        "## Kort om prosjektet",
        "",
        "Prosjektet undersøker om en ekstremt enkel ontologi – noder, relasjoner, stokastiske lokale `units of action`, og ingen bakgrunn – kan gi opphav til noe som ligner spacetime, partikler, bevaringslover og begrenset kausal spredning.",
        "",
        "## Hvor vi er i den lange kjeden",
        "",
        "- v0.1–v0.2: minimal grafdynamikk og seeds",
        "- v0.2–v0.4: invariantanalyse og redusert basis",
        "- v0.5: perturbasjonslab for causal spread",
        "- v0.6: uniformisert kobling i åpne regimer",
        "- v0.7: lokal maksimal kobling og repair-diagnostikk",
        "- v0.8: faseatlas og Paretofront over kandidatrommet",
        "",
        "## Hovedpoeng i v0.8",
        "",
        f"- coarse-scanet identifiserte {pareto_n} Pareto-effisiente punkter i den valgte slicen",
        f"- beste coarse-kandidat lå ved omtrent `(r_birth, r_death, p_swap, p_triad)=({b['r_birth']:.2f}, {b['r_death']:.2f}, {b['p_swap']:.2f}, {b['p_triad']:.2f})`" if b else "- ingen coarse-vinner tilgjengelig",
        "- de mest lovende regimene er fortsatt svakt til moderat åpne",
        "- sterk åpning ser fortsatt ut til å koste for mye i quasi-invariant og geometrirobusthet",
        "",
        "## Hva vi har lært så langt",
        "",
        "1. Lokal maksimal kobling gjør en faktisk forskjell; noen tidligere divergenser var delvis måle-/koblingsartefakter.",
        "2. Helt åpne regimer er dårlige kandidater for ren causal-cone-lesning.",
        "3. Helt lukkede regimer er metodisk rene, men sannsynligvis for stive som kandidater til et realistisk spacetime-regime.",
        "4. Det mest interessante ser ut til å ligge mellom disse ytterpunktene.",
        "",
    ]
    return "\n".join(lines)

def make_lay_md(coarse_rows: List[Dict[str, Any]], refined_rows: List[Dict[str, Any]]) -> str:
    best = sorted(refined_rows if refined_rows else coarse_rows, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[:1]
    b = best[0] if best else None
    lines = [
        "# Relasjonell universgraf v0.8 – forklart uten fagspråk",
        "",
        "## Hva vi prøver å gjøre",
        "",
        "Tenk deg at universet ikke starter med rom, tid og partikler. Tenk i stedet at det bare finnes små biter av informasjon som kan koble seg til hverandre og endre koblingene sine.",
        "",
        "Prosjektet prøver å teste om noe som ligner vår verden kan vokse fram fra et slikt enkelt utgangspunkt.",
        "",
        "## Hva vi testet denne gangen",
        "",
        "Vi tok mange litt forskjellige versjoner av modellen og spurte fire spørsmål om hver av dem:",
        "",
        "1. **Kan modellen reparere små forskjeller?**",
        "   Hvis to nesten like universer starter med en liten forskjell, holder de seg da noenlunde like?",
        "",
        "2. **Sprer forskjellen seg sakte eller fort?**",
        "   Hvis forskjellen sprer seg med begrenset fart, ligner det mer på en verden med en slags kausal struktur.",
        "",
        "3. **Holder viktige størrelser seg stabile?**",
        "   Hvis alt driver vilt av gårde, er modellen dårlig som kandidat til fysikk.",
        "",
        "4. **Holder de grove 'geometri-målene' seg stabile?**",
        "   Vi brukte noen enkle mål som forteller om grafen fortsatt ser omtrent like rom-lignende ut.",
        "",
        "## Hva vi fant",
        "",
        "Vi fant at de beste kandidatene ikke ligger helt i den stive enden og heller ikke i den kaotiske enden.",
        "",
        "Det mest lovende området ligger midt imellom: modellen må være litt åpen og foranderlig, men ikke for åpen.",
        "",
        (f"Den beste kandidaten vi fant i denne runden lå omtrent ved `r_birth={b['r_birth']:.2f}`, `r_death={b['r_death']:.2f}`, `p_swap={b['p_swap']:.2f}`, `p_triad={b['p_triad']:.2f}`." if b else "Vi fant en liten gruppe lovende kandidater, ikke én eneste vinner."),
        "",
        "## Hva det betyr",
        "",
        "Det betyr ikke at vi har laget et nytt univers. Men det betyr at vi har blitt bedre til å finne hvilke versjoner av modellen som er verdt å undersøke videre.",
        "",
        "I vanlig språk: vi har gått fra å lete i mørket til å ha et første kart over hvor de interessante områdene faktisk ligger.",
        "",
        "## Hva som skjer videre",
        "",
        "Neste steg er å gjøre kartet finere, teste flere varianter og sjekke om de samme gode områdene også passer med energibevaring og mer stabile 'rom-lignende' strukturer.",
        "",
    ]
    return "\n".join(lines)

def make_codex_prompt_main() -> str:
    return """# Codex-prompt – v0.8 faseatlas og videreutvikling

Du arbeider i et forskningsprosjekt om en relasjonell universgraf. Prosjektet har nå nådd v0.8 og har følgende kodebase som utgangspunkt:

- `relational_universe_local_max_coupling_lab.py` (v0.7-kjernelab)
- `relational_universe_v08_phase_atlas.py` (v0.8 faseatlas)
- diverse CSV/Markdown-rapporter fra v0.7 og v0.8

## Kontekst
Modellen representerer universet som en dynamisk graf med:
- noder
- én relasjonstype (udirekte kanter)
- stokastiske lokale `units of action`
- ingen bakgrunnsgeometri
- spacetime, partikler og felter tolkes som emergente mønstre

v0.7 etablerte lokal maksimal kobling mellom to nærliggende universgrener.
v0.8 skanner et kandidatrom og rangerer regimer etter fire mål:
1. repair / overlap
2. bounded causal spread
3. quasi-invariants
4. geometry robustness

## Oppgave
Forbedre v0.8 uten å bryte den eksisterende semantikken.

### Krav
1. Bevar de eksisterende parameterne og filformatene så langt det er rimelig.
2. Legg til støtte for bootstrap confidence intervals for aggregate metrics per gridpunkt.
3. Legg til mulighet for finere scan i et lokalt nabolag rundt de beste coarse-punktene.
4. Legg til Pareto-rangering med eksport av frontier til egen CSV.
5. Ikke introduser skjulte globale koordinater eller ikke-lokale regler.
6. Dokumenter endringene i klar Markdown.

### Leveranser
- oppdatert Python-kode
- en kort README
- ett eksempel på kommandoer
- en Markdown-oppsummering av hva endringen metodisk betyr

### Viktig
- vær eksplisitt om hvilke deler som er eksakte og hvilke som er heuristiske
- ikke bland sammen 'geometrirobusthet' med ekte geometri; kall det fortsatt proxy eller robustness
- ikke påstå at en fasegrense er skarp hvis dataene bare støtter en crossover eller et heuristisk regimeskille
"""

def make_codex_prompt_plotting() -> str:
    return """# Codex-prompt – plotting og heatmaps for v0.8

Bruk `relational_universe_v08_phase_atlas.py` og de tilhørende CSV-filene til å lage en brukerorientert analysepakke.

## Oppgave
Lag et lite plotting-verktøy som:
1. leser coarse- og refined-CSV-ene
2. lager heatmaps for composite-score, repair-score, causal-score, quasi-score og geom-score
3. markerer Paretofront-punkter tydelig
4. genererer en Markdown-rapport som forklarer hvordan figurene skal tolkes

## Tekniske krav
- bruk kun Python-standardbibliotek + `matplotlib` + `numpy`
- ingen seaborn
- ingen subplots i samme figur; én figur per score
- filnavn skal være konsistente og lett gjenbrukbare
- rapporten skal være nøktern: skill klart mellom observasjon, tolkning og spekulasjon

## Viktige forklaringer i rapporten
- hvorfor dette ikke er et fullstendig fasekart over hele parameterrommet
- hvorfor `p_del = 0`-slicen ble brukt i v0.8
- hvorfor Paretofront er nyttig når flere mål konkurrerer
"""

def make_codex_prompt_pdel() -> str:
    return """# Codex-prompt – v0.8b med p_del-akse og finere lokal scan

Utvid v0.8-faseatlaset med en liten `p_del`-akse og en lokal refinementsløyfe.

## Oppgave
1. Start fra dagens coarse-vinnere i `relational_universe_v08_phase_atlas.py`.
2. Definer en lokal scan der:
   - `p_del ∈ {0.00, 0.01, 0.02}`
   - `p_triad` finjusteres i små steg rundt v0.8-vinnerne
   - `p_swap` finjusteres i små steg rundt v0.8-vinnerne
   - `r_birth` og `r_death` finjusteres i små steg rundt v0.8-vinnerne
3. Hold fortsatt `local_coupling = maximal`.
4. Rapporter om de lovende regimene er robuste når slettingsakse åpnes litt.

## Krav
- skill eksplisitt mellom coarse og local refinement
- legg inn enkel caching slik at tidligere kjørte gridpunkter ikke regnes om unødvendig
- eksporter både run-level og aggregate CSV
- skriv en Markdown-rapport som sier tydelig om v0.8-kandidatene overlever når `p_del` åpnes, eller om de kollapser
"""

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="v0.8 phase atlas for the relational universe model")
    p.add_argument("--out-prefix", type=str, default="v08_phase_atlas")
    p.add_argument("--steps-coarse", type=int, default=400)
    p.add_argument("--steps-refined", type=int, default=700)
    p.add_argument("--initial-cycle", type=int, default=8)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--coarse-seeds", type=str, default="100,101")
    p.add_argument("--refined-seeds", type=str, default="400,401,402,403")
    p.add_argument("--r-birth-grid", type=str, default="0.02,0.05,0.08")
    p.add_argument("--r-death-grid", type=str, default="0.00,0.02,0.05")
    p.add_argument("--p-swap-grid", type=str, default="0.02,0.04,0.06")
    p.add_argument("--p-triad-grid", type=str, default="0.00,0.02")
    p.add_argument("--p-del", type=float, default=0.0)
    p.add_argument("--max-refine-points", type=int, default=6)
    return p

def main() -> None:
    args = build_parser().parse_args()
    coarse_seeds = [int(x) for x in parse_float_list(args.coarse_seeds)]
    refined_seeds = [int(x) for x in parse_float_list(args.refined_seeds)]

    points = [
        GridPoint(r_birth=rb, r_death=rd, p_swap=ps, p_triad=pt, p_del=args.p_del)
        for rb, rd, ps, pt in itertools.product(
            parse_float_list(args.r_birth_grid),
            parse_float_list(args.r_death_grid),
            parse_float_list(args.p_swap_grid),
            parse_float_list(args.p_triad_grid),
        )
    ]

    coarse_runs, coarse_rows = scan_grid(
        points,
        seeds=coarse_seeds,
        steps=args.steps_coarse,
        initial_cycle=args.initial_cycle,
        initial_tokens=args.initial_tokens,
    )
    add_scores(coarse_rows)

    refine_points = select_refinement_candidates(coarse_rows, max_points=args.max_refine_points)
    refined_runs, refined_rows = scan_grid(
        refine_points,
        seeds=refined_seeds,
        steps=args.steps_refined,
        initial_cycle=args.initial_cycle,
        initial_tokens=args.initial_tokens,
    )
    add_scores(refined_rows)

    out_prefix = Path(args.out_prefix)
    coarse_runs_csv = str(out_prefix.with_name(out_prefix.name + "_coarse_runs.csv"))
    coarse_csv = str(out_prefix.with_name(out_prefix.name + "_coarse.csv"))
    refined_runs_csv = str(out_prefix.with_name(out_prefix.name + "_refined_runs.csv"))
    refined_csv = str(out_prefix.with_name(out_prefix.name + "_refined.csv"))
    main_md = str(out_prefix.with_name(out_prefix.name + "_summary.md"))
    status_md = str(out_prefix.with_name(out_prefix.name + "_status.md"))
    overview_md = str(out_prefix.with_name(out_prefix.name + "_overview.md"))
    lay_md = str(out_prefix.with_name(out_prefix.name + "_lay.md"))
    json_path = str(out_prefix.with_name(out_prefix.name + "_report.json"))

    write_csv(coarse_runs_csv, coarse_runs)
    write_csv(coarse_csv, coarse_rows)
    write_csv(refined_runs_csv, refined_runs)
    write_csv(refined_csv, refined_rows)

    Path(main_md).write_text(make_main_md(coarse_rows, refined_rows, coarse_csv, refined_csv, coarse_runs_csv, refined_runs_csv), encoding="utf-8")
    Path(status_md).write_text(make_status_md(coarse_rows, refined_rows), encoding="utf-8")
    Path(overview_md).write_text(make_project_overview_md(coarse_rows), encoding="utf-8")
    Path(lay_md).write_text(make_lay_md(coarse_rows, refined_rows), encoding="utf-8")
    Path(str(out_prefix.with_name("codex_prompt_v0_8_phaseatlas_og_videreutvikling.md"))).write_text(make_codex_prompt_main(), encoding="utf-8")
    Path(str(out_prefix.with_name("codex_prompt_v0_8_plotting_og_heatmaps.md"))).write_text(make_codex_prompt_plotting(), encoding="utf-8")
    Path(str(out_prefix.with_name("codex_prompt_v0_8b_pdel_og_lokal_refinement.md"))).write_text(make_codex_prompt_pdel(), encoding="utf-8")

    report = {
        "coarse_points": len(coarse_rows),
        "refined_points": len(refined_rows),
        "coarse_pareto_points": sum(int(r["pareto"]) == 1 for r in coarse_rows),
        "best_coarse": max(coarse_rows, key=lambda r: safe_float(r["composite_score"], -1.0)) if coarse_rows else None,
        "best_refined": max(refined_rows, key=lambda r: safe_float(r["composite_score"], -1.0)) if refined_rows else None,
        "files": {
            "coarse_runs_csv": coarse_runs_csv,
            "coarse_csv": coarse_csv,
            "refined_runs_csv": refined_runs_csv,
            "refined_csv": refined_csv,
            "summary_md": main_md,
            "status_md": status_md,
            "overview_md": overview_md,
            "lay_md": lay_md,
        },
    }
    Path(json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
