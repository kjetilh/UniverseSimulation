"""Quasi-invariant analysis utilities for feature-lab trajectories."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

from .features import max_abs_identity_residuals


@dataclass(frozen=True)
class ScaleStat:
    """Descriptive statistics for a feature's scale."""

    feature: str
    mean: float
    std: float
    minimum: float
    maximum: float


@dataclass(frozen=True)
class DriftStat:
    """Linear drift estimate for one feature."""

    feature: str
    slope: float
    mean: float
    std: float
    rel_slope_per_mean: float


@dataclass(frozen=True)
class SVDCandidate:
    """One near-null direction from an SVD analysis."""

    rank: int
    coefficients: tuple[tuple[str, float], ...]
    standardized: bool
    increment_variance: float
    time_slope: float


@dataclass(frozen=True)
class SVDResult:
    """SVD output for one matrix."""

    matrix_label: str
    singular_values: tuple[float, ...]
    candidates: tuple[SVDCandidate, ...]
    standardized: bool


@dataclass(frozen=True)
class TrajectorySummary:
    """Basic facts extracted from a trajectory CSV."""

    row_count: int
    t_start: float
    t_end: float
    constant_features: tuple[str, ...]
    identity_max_abs: Dict[str, float]


@dataclass(frozen=True)
class AnalysisReport:
    """Structured result from a quasi-invariant analysis."""

    source_csv: str
    feature_names: tuple[str, ...]
    feature_basis: str
    analysis_mode: str
    summary: TrajectorySummary
    scale_stats: tuple[ScaleStat, ...]
    drift_stats: tuple[DriftStat, ...]
    svd_results: tuple[SVDResult, ...]
    notes: tuple[str, ...]


def load_csv_rows(csv_path: str) -> List[Dict[str, float]]:
    """Load a trajectory CSV as numeric rows."""
    path = Path(csv_path)
    rows: List[Dict[str, float]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            numeric: Dict[str, float] = {}
            for key, value in row.items():
                if key == "event":
                    continue
                if value is None or value == "":
                    continue
                numeric[key] = float(value)
            rows.append(numeric)
    return rows


def constant_features(rows: Sequence[Mapping[str, float]], feature_names: Sequence[str]) -> List[str]:
    """Return feature names that are exactly constant in the loaded rows."""
    constants: List[str] = []
    for feature in feature_names:
        values = [float(row[feature]) for row in rows if feature in row]
        if values and max(values) == min(values):
            constants.append(feature)
    return constants


def _try_import_numpy():
    try:
        import numpy as np  # type: ignore
    except Exception:
        return None
    return np


def analyze_csv(
    csv_path: str,
    feature_names: Sequence[str],
    feature_basis: str,
    analysis_mode: str = "both",
    top_k: int = 3,
) -> AnalysisReport:
    """Analyze a trajectory CSV in raw and/or standardized modes."""
    rows = load_csv_rows(csv_path)
    if not rows:
        raise ValueError(f"No rows found in trajectory CSV: {csv_path}")

    summary = TrajectorySummary(
        row_count=len(rows),
        t_start=float(rows[0].get("t", 0.0)),
        t_end=float(rows[-1].get("t", 0.0)),
        constant_features=tuple(constant_features(rows, feature_names)),
        identity_max_abs=max_abs_identity_residuals(rows),
    )

    np = _try_import_numpy()
    if np is None:
        return AnalysisReport(
            source_csv=csv_path,
            feature_names=tuple(feature_names),
            feature_basis=feature_basis,
            analysis_mode=analysis_mode,
            summary=summary,
            scale_stats=tuple(),
            drift_stats=tuple(),
            svd_results=tuple(),
            notes=("Numpy kunne ikke importeres; quasi-invariantanalyse ble hoppet over.",),
        )

    if len(rows) < 3:
        return AnalysisReport(
            source_csv=csv_path,
            feature_names=tuple(feature_names),
            feature_basis=feature_basis,
            analysis_mode=analysis_mode,
            summary=summary,
            scale_stats=tuple(),
            drift_stats=tuple(),
            svd_results=tuple(),
            notes=("For fa loggede rader til SVD-basert quasi-invariantanalyse.",),
        )

    t = np.array([float(row["t"]) for row in rows], dtype=float)
    features_matrix = np.array([[float(row[name]) for name in feature_names] for row in rows], dtype=float)
    delta = features_matrix[1:] - features_matrix[:-1]
    dt = (t[1:] - t[:-1]).reshape(-1, 1)
    dt[dt == 0.0] = 1.0
    rates = delta / dt

    mean = np.mean(features_matrix, axis=0)
    std = np.std(features_matrix, axis=0)
    std_safe = np.where(std > 1e-12, std, 1.0)
    standardized = (features_matrix - mean) / std_safe
    standardized_delta = standardized[1:] - standardized[:-1]
    standardized_rates = standardized_delta / dt

    scale_stats = tuple(
        ScaleStat(
            feature=name,
            mean=float(np.mean(features_matrix[:, idx])),
            std=float(np.std(features_matrix[:, idx])),
            minimum=float(np.min(features_matrix[:, idx])),
            maximum=float(np.max(features_matrix[:, idx])),
        )
        for idx, name in enumerate(feature_names)
    )

    A = np.column_stack([t, np.ones_like(t)])
    drift_stats = []
    for idx, name in enumerate(feature_names):
        q = features_matrix[:, idx]
        sol, *_ = np.linalg.lstsq(A, q, rcond=None)
        slope = float(sol[0])
        mean_value = float(np.mean(q))
        std_value = float(np.std(q))
        rel = slope / mean_value if abs(mean_value) > 1e-12 else float("nan")
        drift_stats.append(
            DriftStat(
                feature=name,
                slope=slope,
                mean=mean_value,
                std=std_value,
                rel_slope_per_mean=rel,
            )
        )

    def build_svd_result(
        matrix,
        trajectory_matrix,
        label: str,
        standardized_mode: bool,
    ) -> SVDResult:
        _, singular_values, vt = np.linalg.svd(matrix, full_matrices=False)
        candidates: List[SVDCandidate] = []
        for rank in range(1, min(top_k, vt.shape[0]) + 1):
            direction = vt[-rank]
            q = trajectory_matrix @ direction
            dq = q[1:] - q[:-1]
            sol, *_ = np.linalg.lstsq(A, q, rcond=None)
            coefficients = tuple(
                (name, float(coef))
                for coef, name in zip(direction, feature_names)
                if abs(float(coef)) >= 0.08
            )
            candidates.append(
                SVDCandidate(
                    rank=rank,
                    coefficients=coefficients,
                    standardized=standardized_mode,
                    increment_variance=float(np.var(dq)),
                    time_slope=float(sol[0]),
                )
            )
        return SVDResult(
            matrix_label=label,
            singular_values=tuple(float(value) for value in singular_values),
            candidates=tuple(candidates),
            standardized=standardized_mode,
        )

    results: List[SVDResult] = []
    if analysis_mode in {"raw", "both"}:
        results.append(build_svd_result(delta, features_matrix, "Minste endring i rå inkrementer ΔF", False))
        results.append(build_svd_result(rates, features_matrix, "Minste endring i rå hastigheter ΔF/Δt", False))
    if analysis_mode in {"standardized", "both"}:
        results.append(build_svd_result(standardized_delta, standardized, "Minste endring i standardiserte inkrementer Δz(F)", True))
        results.append(build_svd_result(standardized_rates, standardized, "Minste endring i standardiserte hastigheter Δz(F)/Δt", True))

    notes = [
        "Rå analyse er sensitiv for absolutte skalaer og store variasjoner.",
        "Standardisert analyse tester om de samme kandidatene overlever når alle features z-skaleres.",
    ]
    if feature_basis == "reduced":
        notes.append(
            "Redusert basis fjerner `beta1` og `deg_sq_sum` for å kvotientere ut de mest opplagte algebraiske redundansene."
        )

    return AnalysisReport(
        source_csv=csv_path,
        feature_names=tuple(feature_names),
        feature_basis=feature_basis,
        analysis_mode=analysis_mode,
        summary=summary,
        scale_stats=scale_stats,
        drift_stats=tuple(drift_stats),
        svd_results=tuple(results),
        notes=tuple(notes),
    )
