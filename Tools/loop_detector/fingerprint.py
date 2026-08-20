"""Create identity-stripped fingerprints for loop-detector observations."""

from __future__ import annotations

from collections.abc import Iterable
import re
import string


_IDENTITY_PATTERNS = (
    # Dates precede the general hexadecimal identifier pattern for clarity.
    r"(?<![A-Za-z0-9])\d{8}T\d{6}Z(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])\d{4}-\d{2}-\d{2}(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])\d{8}(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])v(?:\d+_)?\d+[a-z]*(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])retry[-_]?\d+(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])(?:final|gen)[-_]?\d+(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])(?:attempt|forsok|forsøk)[-_]?\d+(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9])[0-9a-f]{7,}(?![A-Za-z0-9])",
    r"\(\s*#?\d+\s*\)",
    r"(?<![A-Za-z0-9])(?:andre|tredje|fjerde|second|third)(?![A-Za-z0-9])",
)
_IDENTITY_RE = re.compile("|".join(f"(?:{pattern})" for pattern in _IDENTITY_PATTERNS), re.IGNORECASE)
_WHITESPACE_RE = re.compile(r"\s+")
_EDGE_SEPARATORS = string.whitespace + string.punctuation


def normalize(text: str) -> str:
    """Return a lowercase fingerprint with attempt identities removed.

    Version, retry, generation, attempt, date, hexadecimal identifier,
    parenthesized sequence, and ordinal tokens are removed. Remaining
    whitespace is collapsed and punctuation at both ends is stripped.

    Args:
        text: Observation, commit subject, or filename to fingerprint.

    Returns:
        The identity-stripped normalized fingerprint.
    """

    without_identities = _IDENTITY_RE.sub(" ", text).lower()
    collapsed = _WHITESPACE_RE.sub(" ", without_identities).strip()
    return collapsed.strip(_EDGE_SEPARATORS).strip()


def group(items: Iterable[str]) -> dict[str, list[str]]:
    """Group original strings by their normalized fingerprint.

    Args:
        items: Strings to fingerprint and group.

    Returns:
        A mapping from each normalized fingerprint to originals in input order.
    """

    grouped: dict[str, list[str]] = {}
    for item in items:
        grouped.setdefault(normalize(item), []).append(item)
    return grouped
