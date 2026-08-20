"""Read and classify changes from a Git repository's commit history."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re


_RECORD_SEPARATOR = "\x1e"
_FIELD_SEPARATOR = "\x1f"
_LOG_FORMAT = (
    f"{_RECORD_SEPARATOR}%H{_FIELD_SEPARATOR}%ad{_FIELD_SEPARATOR}"
    f"%an{_FIELD_SEPARATOR}%s"
)
_DOC_EXTENSIONS = frozenset({".md", ".csv", ".txt", ".json"})
_CODE_EXTENSIONS = frozenset(
    {
        ".asm",
        ".bash",
        ".c",
        ".cc",
        ".clj",
        ".cljc",
        ".cljs",
        ".cpp",
        ".cs",
        ".css",
        ".cxx",
        ".dart",
        ".erl",
        ".ex",
        ".exs",
        ".fish",
        ".fs",
        ".fsi",
        ".fsx",
        ".go",
        ".gradle",
        ".groovy",
        ".h",
        ".hh",
        ".hpp",
        ".hrl",
        ".htm",
        ".html",
        ".hxx",
        ".ipynb",
        ".java",
        ".js",
        ".jsx",
        ".kt",
        ".kts",
        ".less",
        ".lua",
        ".m",
        ".mm",
        ".nim",
        ".php",
        ".pl",
        ".pm",
        ".proto",
        ".ps1",
        ".py",
        ".pyi",
        ".r",
        ".rb",
        ".rs",
        ".s",
        ".sass",
        ".scala",
        ".scss",
        ".sh",
        ".sol",
        ".sql",
        ".svelte",
        ".swift",
        ".ts",
        ".tsx",
        ".vb",
        ".vue",
        ".zsh",
        ".zig",
    }
)


class GitError(RuntimeError):
    """Raised when Git cannot provide a valid commit history."""


@dataclass
class FileChange:
    """Line-count information for one path changed by a commit."""

    path: str
    added: int
    deleted: int
    is_binary: bool


@dataclass
class Commit:
    """A commit and its per-file numstat changes."""

    sha: str
    date: date
    author: str
    subject: str
    files: list[FileChange]


def _parse_file_change(line: str) -> FileChange:
    parts = line.split("\t", 2)
    if len(parts) != 3 or not parts[2]:
        raise GitError(f"malformed git numstat line: {line!r}")

    added_text, deleted_text, path = parts
    if added_text == "-" and deleted_text == "-":
        return FileChange(path=path, added=0, deleted=0, is_binary=True)
    if added_text == "-" or deleted_text == "-":
        raise GitError(f"malformed git numstat counts: {line!r}")

    try:
        added = int(added_text)
        deleted = int(deleted_text)
    except ValueError as exc:
        raise GitError(f"malformed git numstat counts: {line!r}") from exc
    if added < 0 or deleted < 0:
        raise GitError(f"negative git numstat counts: {line!r}")
    return FileChange(path=path, added=added, deleted=deleted, is_binary=False)


def _parse_log(output: str) -> list[Commit]:
    commits: list[Commit] = []
    for raw_record in output.split(_RECORD_SEPARATOR):
        record = raw_record.strip("\r\n")
        if not record:
            continue

        header, separator, body = record.partition("\n")
        fields = header.rstrip("\r").split(_FIELD_SEPARATOR, 3)
        if len(fields) != 4:
            raise GitError(f"malformed git log header: {header!r}")

        sha, date_text, author, subject = fields
        if not sha:
            raise GitError("git log returned a commit without a SHA")
        try:
            commit_date = date.fromisoformat(date_text)
        except ValueError as exc:
            raise GitError(f"malformed git commit date: {date_text!r}") from exc

        files: list[FileChange] = []
        if separator:
            for raw_line in body.splitlines():
                line = raw_line.rstrip("\r")
                if line:
                    files.append(_parse_file_change(line))
        commits.append(
            Commit(
                sha=sha,
                date=commit_date,
                author=author,
                subject=subject,
                files=files,
            )
        )
    return commits


def read_commits(repo: Path, since: str | None = None) -> list[Commit]:
    """Return commits from ``repo``, newest first, including numstat changes.

    Raises:
        GitError: If Git is unavailable, the repository cannot be read, or Git
            returns output that does not match the requested format.
    """

    command = [
        "git",
        "-C",
        str(repo),
        "log",
        "--numstat",
        "--date=short",
        f"--format={_LOG_FORMAT}",
    ]
    if since is not None:
        command.append(f"--since={since}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            check=False,
        )
    except FileNotFoundError as exc:
        raise GitError("git executable was not found") from exc
    except OSError as exc:
        raise GitError(f"could not run git: {exc}") from exc

    if result.returncode != 0:
        detail = result.stderr.strip() or f"git exited with status {result.returncode}"
        raise GitError(detail)
    return _parse_log(result.stdout)


def _normalize_repo_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return re.sub(r"/+", "/", normalized).rstrip("/")


def classify(path: str, docs_dirs: list[str]) -> str:
    """Classify a repository-relative path according to specification S6."""

    normalized_path = _normalize_repo_path(path)
    suffix = Path(normalized_path).suffix.lower()
    for docs_dir in docs_dirs:
        normalized_docs_dir = _normalize_repo_path(docs_dir)
        under_docs_dir = normalized_docs_dir in {"", "."} or normalized_path.startswith(
            f"{normalized_docs_dir}/"
        )
        if under_docs_dir and suffix in _DOC_EXTENSIONS:
            return "doc"
    if suffix in _CODE_EXTENSIONS:
        return "code"
    return "other"
