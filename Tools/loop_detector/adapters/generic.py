"""Define the adapter interface and the generic no-rounds adapter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Round:
    """One repository round with optional outcome and gate measurements."""

    label: str
    outcome: float | None
    gate_count: int | None
    source: str


class Adapter:
    """Base class for repository-specific round adapters."""

    name: str

    def rounds(self, repo: Path) -> list[Round]:
        """Return measured rounds from ``repo``.

        Args:
            repo: Repository root to inspect without modifying it.

        Returns:
            Rounds discovered by the adapter.

        Raises:
            NotImplementedError: Always, unless a subclass implements the method.
        """

        raise NotImplementedError


class GenericAdapter(Adapter):
    """Adapter for repositories without a known outcome data source."""

    name: str = "generic"

    def rounds(self, repo: Path) -> list[Round]:
        """Return no rounds because a generic repo has no defined outcome.

        Args:
            repo: Repository root, unused by the generic adapter.

        Returns:
            An empty list, representing the valid no-adapter-data outcome.
        """

        return []
