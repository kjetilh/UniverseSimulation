"""Evaluate the loop detector's seven signatures."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
import fnmatch
import os
from pathlib import Path
import re
from statistics import median

from . import fingerprint
from .adapters.generic import Round
from .gitlog import Commit, classify


_MAX_EVIDENCE: int = 20
_EXCLUDED_DIRECTORIES: frozenset[str] = frozenset(
    {".git", "__pycache__", ".codex_pydeps", ".build"}
)
_S4_GLOBS: tuple[str, ...] = (
    "*verify*.py",
    "*gate*.py",
    "*check*.sh",
    "*deploy*.sh",
    "*release*.sh",
    "*cutover*",
)
_SYS_EXIT_RE: re.Pattern[str] = re.compile(
    r"\bsys\.exit\(\s*(?P<argument>[^)]*)\)", re.DOTALL
)
_SHELL_DIE_RE: re.Pattern[str] = re.compile(r"\bdie\b")
_DEFAULT_STALL_PHRASES: tuple[str, ...] = (
    "remain closed",
    "remains closed",
    "stays closed",
    "deferred",
    "out of scope for this round",
    "not attempted",
    "holdes lukket",
    "utsatt",
)


@dataclass
class SignatureResult:
    """Result of evaluating one loop-detector signature."""

    code: str
    name: str
    fired: bool
    observed: str
    threshold: str
    evidence: list[str]

    def __post_init__(self) -> None:
        """Enforce the specification's maximum evidence length."""

        self.evidence = self.evidence[:_MAX_EVIDENCE]


def _outcome_window(rounds: list[Round]) -> tuple[float, float, float] | None:
    """Return median, minimum, and maximum when a round window is stalled."""

    if len(rounds) < 3 or any(round_.outcome is None for round_ in rounds):
        return None
    outcomes: list[float] = [
        round_.outcome for round_ in rounds if round_.outcome is not None
    ]
    midpoint = float(median(outcomes))
    tolerance = abs(midpoint) * 0.05
    if all(abs(outcome - midpoint) <= tolerance for outcome in outcomes):
        return midpoint, min(outcomes), max(outcomes)
    return None


def _longest_round_window(
    rounds: list[Round], *, require_nondecreasing_gates: bool
) -> tuple[list[Round], tuple[float, float, float]] | None:
    """Return the longest consecutive window satisfying outcome/gate rules."""

    best: tuple[list[Round], tuple[float, float, float]] | None = None
    for start in range(len(rounds)):
        for end in range(start + 3, len(rounds) + 1):
            window = rounds[start:end]
            outcome_summary = _outcome_window(window)
            if outcome_summary is None:
                continue
            if require_nondecreasing_gates:
                gates = [round_.gate_count for round_ in window]
                if any(gate is None for gate in gates):
                    continue
                measured_gates = [gate for gate in gates if gate is not None]
                if any(
                    later < earlier
                    for earlier, later in zip(measured_gates, measured_gates[1:])
                ):
                    continue
            if best is None or len(window) > len(best[0]):
                best = window, outcome_summary
    return best


def _round_evidence(rounds: Iterable[Round]) -> list[str]:
    """Return distinct round sources, falling back to labels when necessary."""

    return list(dict.fromkeys(round_.source or round_.label for round_ in rounds))


def s1_stalled_outcome(rounds: Iterable[Round]) -> SignatureResult:
    """Detect three or more consecutive outcomes within five percent of median."""

    round_list = list(rounds)
    if not round_list:
        return SignatureResult(
            code="S1",
            name="Stalled outcome",
            fired=False,
            observed="no adapter",
            threshold="at least 3 consecutive outcomes within +/-5% of their median",
            evidence=[],
        )

    match = _longest_round_window(
        round_list, require_nondecreasing_gates=False
    )
    if match is None:
        measured = sum(round_.outcome is not None for round_ in round_list)
        observed = (
            f"no qualifying window; {measured} measured outcomes "
            f"across {len(round_list)} rounds"
        )
        evidence: list[str] = []
    else:
        window, (midpoint, low, high) = match
        observed = (
            f"{len(window)} consecutive rounds {window[0].label}..{window[-1].label}; "
            f"median={midpoint:g}, range={low:g}..{high:g}"
        )
        evidence = _round_evidence(window)

    return SignatureResult(
        code="S1",
        name="Stalled outcome",
        fired=match is not None,
        observed=observed,
        threshold="at least 3 consecutive outcomes within +/-5% of their median",
        evidence=evidence,
    )


def _distinct_groups(items: Iterable[str]) -> dict[str, list[str]]:
    """Group strings by fingerprint while retaining distinct originals only."""

    grouped: dict[str, list[str]] = fingerprint.group(items)
    return {
        key: list(dict.fromkeys(originals)) for key, originals in grouped.items()
    }


def _display_key(key: str) -> str:
    """Return an explicit printable label for a normalized fingerprint."""

    return key if key else "<empty>"


def s2_repeated_attempt_identity(
    commits: Iterable[Commit], doc_paths: Iterable[str | Path]
) -> SignatureResult:
    """Detect repeated identities in commit subjects and document filenames.

    Commit subjects and document basenames are grouped separately using the
    shared identity-stripping fingerprint. A group qualifies when at least
    three distinct originals have the same normalized key. Document contents
    are never opened.

    Args:
        commits: Commits whose subjects and hashes should be inspected.
        doc_paths: Document paths; only each path's basename is used.

    Returns:
        S2's firing state, ten largest groups, threshold, and bounded evidence.
    """

    commit_list: list[Commit] = list(commits)
    document_names: list[str] = [Path(path).name for path in doc_paths]
    commit_groups: dict[str, list[str]] = _distinct_groups(
        commit.subject for commit in commit_list
    )
    document_groups: dict[str, list[str]] = _distinct_groups(document_names)

    ranked_groups: list[tuple[str, str, list[str]]] = []
    ranked_groups.extend(
        ("commits", key, originals) for key, originals in commit_groups.items()
    )
    ranked_groups.extend(
        ("docs", key, originals) for key, originals in document_groups.items()
    )
    ranked_groups.sort(key=lambda item: (-len(item[2]), item[0], item[1]))

    qualifying_groups: list[tuple[str, str, list[str]]] = [
        item for item in ranked_groups if len(item[2]) >= 3
    ]
    observed: str = "; ".join(
        f"{source}:{_display_key(key)}={len(originals)}"
        for source, key, originals in ranked_groups[:10]
    )
    if not observed:
        observed = "no groups"

    subject_hashes: dict[str, list[str]] = {}
    for commit in commit_list:
        subject_hashes.setdefault(commit.subject, []).append(commit.sha)

    evidence: list[str] = []
    for source, _key, originals in qualifying_groups:
        for original in originals:
            if source == "commits":
                evidence.append(f"commit:{subject_hashes[original][0]}")
            else:
                evidence.append(f"doc:{original}")
            if len(evidence) == _MAX_EVIDENCE:
                break
        if len(evidence) == _MAX_EVIDENCE:
            break

    return SignatureResult(
        code="S2",
        name="Repeated attempt identity",
        fired=bool(qualifying_groups),
        observed=observed,
        threshold="at least 3 distinct originals with one normalized key",
        evidence=evidence,
    )


def s3_growing_gates_stalled_outcome(
    rounds: Iterable[Round],
) -> SignatureResult:
    """Detect nondecreasing gate counts over the same stalled-outcome rounds."""

    round_list = list(rounds)
    if not round_list:
        return SignatureResult(
            code="S3",
            name="Growing gates with stalled outcome",
            fired=False,
            observed="no adapter",
            threshold=(
                "nondecreasing gate count across at least 3 consecutive rounds "
                "that also satisfy S1"
            ),
            evidence=[],
        )

    match = _longest_round_window(round_list, require_nondecreasing_gates=True)
    if match is None:
        measured = sum(
            round_.outcome is not None and round_.gate_count is not None
            for round_ in round_list
        )
        observed = (
            f"no qualifying joint window; {measured} rounds have both measurements"
        )
        evidence: list[str] = []
    else:
        window, (midpoint, low, high) = match
        gates = [round_.gate_count for round_ in window]
        observed = (
            f"{len(window)} consecutive rounds {window[0].label}..{window[-1].label}; "
            f"gates={','.join(str(gate) for gate in gates)}; "
            f"outcome median={midpoint:g}, range={low:g}..{high:g}"
        )
        evidence = _round_evidence(window)

    return SignatureResult(
        code="S3",
        name="Growing gates with stalled outcome",
        fired=match is not None,
        observed=observed,
        threshold=(
            "nondecreasing gate count across at least 3 consecutive rounds "
            "that also satisfy S1"
        ),
        evidence=evidence,
    )


def _candidate_paths(repo: Path, globs: Iterable[str]) -> list[Path]:
    """Return matching files while pruning excluded directories in place."""

    patterns: tuple[str, ...] = tuple(globs)
    candidates: list[Path] = []
    for root, directories, filenames in os.walk(repo):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in _EXCLUDED_DIRECTORIES
        )
        for filename in sorted(filenames):
            if any(fnmatch.fnmatchcase(filename, pattern) for pattern in patterns):
                candidates.append(Path(root) / filename)
    return sorted(candidates, key=lambda path: path.relative_to(repo).as_posix())


def _has_nonzero_sys_exit(source: str) -> bool:
    """Return whether Python source calls ``sys.exit`` with a non-null value."""

    for match in _SYS_EXIT_RE.finditer(source):
        argument: str = match.group("argument").strip()
        if argument and argument not in {"0", "None"}:
            return True
    return False


def _python_can_fail(source: str) -> bool:
    """Return whether source contains any specified Python failure mechanism."""

    return (
        source.count("assert ") > 0
        or source.count("raise ") > 0
        or _has_nonzero_sys_exit(source)
    )


def _shell_can_fail(source: str) -> bool:
    """Return whether source contains a specified shell failure mechanism."""

    has_fail_fast: bool = "set -e" in source or "set -Eeuo" in source
    has_explicit_failure: bool = "exit 1" in source or bool(
        _SHELL_DIE_RE.search(source)
    )
    return has_fail_fast or has_explicit_failure


def s4_unfailable_verification(
    repo: Path, extra_globs: Iterable[str] | None = None
) -> SignatureResult:
    """Detect verification candidates without a specified failure mechanism.

    Python candidates require an ``assert ``, ``raise ``, or non-null
    ``sys.exit`` argument. Other candidates are treated as shell scripts and
    require either fail-fast shell options or an explicit ``exit 1``/``die``.
    Only candidate files are read, and excluded directories are not traversed.

    Args:
        repo: Repository root to traverse without modifying it.
        extra_globs: Optional filename globs added to the standard candidates.

    Returns:
        S4's firing state, candidate counts, threshold, and flagged paths.
    """

    patterns: tuple[str, ...] = _S4_GLOBS + tuple(extra_globs or ())
    candidates: list[Path] = _candidate_paths(repo, patterns)
    flagged: list[str] = []
    for path in candidates:
        source: str = path.read_text(encoding="utf-8", errors="replace")
        can_fail: bool = (
            _python_can_fail(source) if path.suffix == ".py" else _shell_can_fail(source)
        )
        if not can_fail:
            flagged.append(path.relative_to(repo).as_posix())

    return SignatureResult(
        code="S4",
        name="Unfailable verification",
        fired=bool(flagged),
        observed=f"{len(flagged)} flagged of {len(candidates)} candidates",
        threshold="at least 1 flagged candidate file",
        evidence=flagged,
    )


def s5_parked_main_question(
    doc_paths: Iterable[str | Path],
    stall_phrases: Iterable[str] | None = None,
) -> SignatureResult:
    """Detect a stall phrase repeated through at least three ordered documents.

    Documents are ordered by filename and modification time, as the generic
    proxy for successive rounds required by the specification. Each phrase is
    counted at most once per document.
    """

    phrases = tuple(
        dict.fromkeys(
            phrase.strip().casefold()
            for phrase in (
                _DEFAULT_STALL_PHRASES
                if stall_phrases is None
                else tuple(stall_phrases)
            )
            if phrase.strip()
        )
    )
    paths = sorted(
        dict.fromkeys(Path(path) for path in doc_paths),
        key=lambda path: (path.name.casefold(), path.stat().st_mtime_ns, path.as_posix()),
    )
    matches: dict[str, list[Path]] = {phrase: [] for phrase in phrases}
    for path in paths:
        source = path.read_text(encoding="utf-8", errors="replace").casefold()
        for phrase in phrases:
            if phrase in source:
                matches[phrase].append(path)

    ranked = sorted(matches.items(), key=lambda item: (-len(item[1]), item[0]))
    qualifying = [(phrase, found) for phrase, found in ranked if len(found) >= 3]
    nonempty = [(phrase, found) for phrase, found in ranked if found]
    observed = "; ".join(
        f"{phrase}={len(found)}" for phrase, found in nonempty
    ) or "no stall phrases found"
    evidence: list[str] = []
    for phrase, found in qualifying:
        evidence.extend(f"{phrase}:{path.as_posix()}" for path in found)

    return SignatureResult(
        code="S5",
        name="Parked main question",
        fired=bool(qualifying),
        observed=observed,
        threshold="same stall phrase in at least 3 ordered round documents",
        evidence=evidence,
    )


@dataclass
class _MonthlyChange:
    """Aggregated Git measurements for one calendar month."""

    doc_files_changed: int = 0
    code_lines_changed: int = 0
    lines_added: int = 0


def _month_key(value: date) -> tuple[int, int]:
    return value.year, value.month


def _month_label(month: tuple[int, int]) -> str:
    return f"{month[0]:04d}-{month[1]:02d}"


def _next_month(month: tuple[int, int]) -> tuple[int, int]:
    year, number = month
    return (year + 1, 1) if number == 12 else (year, number + 1)


def _calendar_months(
    first: tuple[int, int], last: tuple[int, int]
) -> list[tuple[int, int]]:
    months: list[tuple[int, int]] = []
    current = first
    while current <= last:
        months.append(current)
        current = _next_month(current)
    return months


def _monthly_changes(
    commits: Iterable[Commit], docs_dirs: Iterable[str]
) -> tuple[list[Commit], dict[tuple[int, int], _MonthlyChange]]:
    """Aggregate documentation, code, and addition counts by month."""

    commit_list = list(commits)
    document_directories = list(docs_dirs)
    monthly: dict[tuple[int, int], _MonthlyChange] = {}
    for commit in commit_list:
        totals = monthly.setdefault(_month_key(commit.date), _MonthlyChange())
        for change in commit.files:
            category = classify(change.path, document_directories)
            if category == "doc":
                totals.doc_files_changed += 1
            elif category == "code":
                totals.code_lines_changed += change.added + change.deleted
            totals.lines_added += change.added
    return commit_list, monthly


def s6_documentation_outpaces_code(
    commits: Iterable[Commit], docs_dirs: Iterable[str]
) -> SignatureResult:
    """Detect three months where changed doc files exceed changed code lines."""

    document_directories = list(docs_dirs)
    commit_list, monthly = _monthly_changes(commits, document_directories)
    qualifying = [
        month
        for month, totals in sorted(monthly.items())
        if totals.doc_files_changed > totals.code_lines_changed
    ]
    observed = "; ".join(
        (
            f"{_month_label(month)}:docs={totals.doc_files_changed},"
            f"code_lines={totals.code_lines_changed},"
            f"ratio={totals.doc_files_changed / max(1, totals.code_lines_changed):g}"
        )
        for month, totals in sorted(monthly.items())
    ) or "no commit data"

    qualifying_set = set(qualifying)
    evidence: list[str] = []
    for commit in sorted(commit_list, key=lambda item: (item.date, item.sha)):
        if _month_key(commit.date) not in qualifying_set:
            continue
        for change in commit.files:
            if classify(change.path, document_directories) == "doc":
                evidence.append(f"{commit.sha}:{change.path}")

    return SignatureResult(
        code="S6",
        name="Documentation outpaces code",
        fired=len(qualifying) >= 3,
        observed=observed,
        threshold="doc files changed > code lines changed in at least 3 months",
        evidence=evidence,
    )


def _longest_growth_streak(
    monthly: dict[tuple[int, int], _MonthlyChange]
) -> list[tuple[tuple[int, int], int]]:
    """Return the longest strictly growing cumulative-additions month streak."""

    if not monthly:
        return []
    months = _calendar_months(min(monthly), max(monthly))
    cumulative = 0
    series: list[tuple[tuple[int, int], int]] = []
    for month in months:
        cumulative += monthly.get(month, _MonthlyChange()).lines_added
        series.append((month, cumulative))

    best: list[tuple[tuple[int, int], int]] = []
    current: list[tuple[tuple[int, int], int]] = []
    for point in series:
        if not current or point[1] > current[-1][1]:
            current.append(point)
        else:
            if len(current) > len(best):
                best = current
            current = [point]
    if len(current) > len(best):
        best = current
    return best


def s7_resource_growth_without_outcome_change(
    commits: Iterable[Commit],
    s1_result: SignatureResult,
    s2_result: SignatureResult,
) -> SignatureResult:
    """Detect sustained cumulative additions coupled to no outcome movement."""

    commit_list, monthly = _monthly_changes(commits, ())
    streak = _longest_growth_streak(monthly)
    has_adapter = s1_result.observed != "no adapter"
    no_outcome_movement = s1_result.fired if has_adapter else s2_result.fired
    coupling = "S1 fired" if has_adapter else "no adapter; S2 fired"
    if not no_outcome_movement:
        coupling = "S1 did not fire" if has_adapter else "no adapter; S2 did not fire"

    if streak:
        growth = ",".join(
            f"{_month_label(month)}={total}" for month, total in streak
        )
        observed = f"longest growth streak {len(streak)} months ({growth}); {coupling}"
    else:
        observed = f"no monthly additions; {coupling}"

    streak_months = {month for month, _total in streak}
    evidence: list[str] = []
    for commit in sorted(commit_list, key=lambda item: (item.date, item.sha)):
        if _month_key(commit.date) not in streak_months:
            continue
        for change in commit.files:
            if change.added > 0:
                evidence.append(f"{commit.sha}:{change.path}:+{change.added}")

    return SignatureResult(
        code="S7",
        name="Resource growth without outcome change",
        fired=len(streak) >= 3 and no_outcome_movement,
        observed=observed,
        threshold=(
            "strictly growing cumulative additions in at least 3 consecutive "
            "months, with S1 fired or (without adapter) S2 fired"
        ),
        evidence=evidence,
    )
