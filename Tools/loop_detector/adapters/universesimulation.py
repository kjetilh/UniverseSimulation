"""Read loop-detector rounds from UniverseSimulation gate evaluations."""

from __future__ import annotations

import csv
from pathlib import Path
import re

from .generic import Adapter, Round


_VERSION_RE: re.Pattern[str] = re.compile(
    r"^(v(?P<number>\d+)(?P<suffix>[a-z]*))_", re.IGNORECASE
)
_RATIO_RE: re.Pattern[str] = re.compile(
    r"ratio=(?P<low>[+-]?(?:\d+(?:\.\d*)?|\.\d+))"
    r"-(?P<high>[+-]?(?:\d+(?:\.\d*)?|\.\d+))",
    re.IGNORECASE,
)


def _suffix_number(suffix: str) -> int:
    """Return a bijective base-26 number for an alphabetic suffix."""

    value = 0
    for character in suffix.lower():
        value = value * 26 + (ord(character) - ord("a") + 1)
    return value


def _version_sort_key(token: str) -> tuple[int, int]:
    """Return a natural numeric and alphabetic sorting key for a version token."""

    match = _VERSION_RE.match(f"{token}_")
    if match is None:
        raise ValueError(f"invalid version token: {token}")
    return int(match.group("number")), _suffix_number(match.group("suffix"))


def _label_from_path(path: Path) -> str:
    """Extract the leading version token from a gate-evaluation path."""

    match = _VERSION_RE.match(path.name)
    if match is None:
        raise ValueError(f"gate evaluation lacks a version token: {path}")
    return match.group(1).lower()


def _read_round(path: Path) -> Round:
    """Read one gate-evaluation CSV file into a measured round."""

    gate_count = 0
    outcome: float | None = None
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        normalized_header = [column.strip().lower() for column in header]
        status_index = (
            normalized_header.index("status") if "status" in normalized_header else None
        )
        observed_index = (
            normalized_header.index("observed")
            if "observed" in normalized_header
            else None
        )
        for row in reader:
            if not row:
                continue
            if not row[0].strip().endswith("_overall"):
                gate_count += 1

            if status_index is None or observed_index is None:
                continue
            status = row[status_index].strip().lower()
            if outcome is None and status == "fail":
                ratio_match = _RATIO_RE.search(row[observed_index])
                if ratio_match is not None:
                    low = float(ratio_match.group("low"))
                    high = float(ratio_match.group("high"))
                    outcome = (low + high) / 2

    label = _label_from_path(path)
    return Round(label=label, outcome=outcome, gate_count=gate_count, source=str(path))


class UniverseSimulationAdapter(Adapter):
    """Adapter backed by UniverseSimulation gate-evaluation CSV files."""

    name: str = "universesimulation"

    def rounds(self, repo: Path) -> list[Round]:
        """Return naturally sorted gate-evaluation rounds from ``repo``.

        Args:
            repo: UniverseSimulation repository root to inspect.

        Returns:
            Rounds parsed from ``Documentation/v*_gate_evaluation.csv``.
        """

        paths = (repo / "Documentation").glob("v*_gate_evaluation.csv")
        rounds = [_read_round(path) for path in paths]
        return sorted(rounds, key=lambda round_: _version_sort_key(round_.label))
