"""Select and expose repository-specific loop-detector adapters."""

from __future__ import annotations

from pathlib import Path

from .generic import Adapter, GenericAdapter, Round
from .universesimulation import UniverseSimulationAdapter


def resolve_adapter(name: str, repo: Path) -> Adapter:
    """Return the requested adapter for ``repo``.

    Args:
        name: Adapter name: ``auto``, ``generic``, or ``universesimulation``.
        repo: Repository path used by automatic adapter selection.

    Returns:
        A repository adapter matching ``name`` and ``repo``.

    Raises:
        ValueError: If ``name`` does not identify a supported adapter.
    """

    resolved_name = name
    if resolved_name == "auto":
        resolved_name = (
            "universesimulation" if repo.name == "UniverseSimulation" else "generic"
        )

    if resolved_name == "generic":
        return GenericAdapter()
    if resolved_name == "universesimulation":
        return UniverseSimulationAdapter()
    raise ValueError(f"unknown adapter: {name}")


__all__ = [
    "Adapter",
    "GenericAdapter",
    "Round",
    "UniverseSimulationAdapter",
    "resolve_adapter",
]
