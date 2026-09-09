"""Generate a small, explicit provenance index, not a graph database or inference.

Only sources named by the JSON manifest are read; no repository scan occurs.
The caller declares every status and relation. Hashing establishes which file
bytes were indexed, not whether a scientific claim is true. Anchors are retained
as citation hints but are not checked for existence within the source file.

Manifest: {"nodes": [{"id", "kind", "status", "source", "anchor"?}],
           "edges": [{"source", "target", "relation"}],
           "schema_version"?: 1, "title"?: "..."}.
Source paths must be canonical repository-relative POSIX file paths.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date as calendar_date
import hashlib
import io
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re


KINDS = frozenset({"user_rule", "protocol", "code", "test", "report", "result",
                   "data", "limitation"})
STATUSES = frozenset({"planned", "measured", "verified", "blocked", "superseded",
                     "rejected"})
RELATIONS = frozenset({"specifies", "implements", "tests", "measures", "reports",
                      "derived_from", "supports", "contradicts", "calibrates",
                      "documents", "limited_by", "assumes", "executed_with"})
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]*\Z")


def _text(value: object, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not value and not allow_empty):
        raise ValueError(f"{label} must be a {'possibly empty ' if allow_empty else ''}string")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{label} must not contain control characters")
    return value


def _fields(value: object, required: set[str], optional: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    if not required <= value.keys() or value.keys() - required - optional:
        raise ValueError(f"{label} has missing or unknown fields")
    return value


def _source(root: Path, value: object) -> tuple[str, Path]:
    source = _text(value, "node source")
    path = PurePosixPath(source)
    if (path.is_absolute() or PureWindowsPath(source).drive or "\\" in source
            or any(part in {"", ".", ".."} for part in source.split("/"))
            or path.as_posix() != source):
        raise ValueError(f"source must be a canonical relative path: {source!r}")
    try:
        resolved = (root / source).resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ValueError(f"source is missing or resolves outside root: {source!r}") from exc
    if not resolved.is_file():
        raise ValueError(f"source is not a file: {source!r}")
    return source, resolved


def _csv(columns: tuple[str, ...], rows: list[dict]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _cell(value: str) -> str:
    """Keep manifest text literal in a Markdown table, without active links/HTML."""
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("\\", "&#92;").replace("|", "&#124;").replace("`", "&#96;")
            .replace("[", "&#91;").replace("]", "&#93;").replace("*", "&#42;")
            .replace("_", "&#95;"))


def build(manifest: dict, root: Path | str, date: str) -> dict[str, str]:
    """Return markdown, nodes_csv and edges_csv with deterministic ordering.

    `date` is an explicit YYYY-MM-DD assertion by the caller, never wall-clock
    time. No input files are modified. Output nodes include full-file SHA-256.
    """
    manifest = _fields(manifest, {"nodes", "edges"}, {"schema_version", "title"}, "manifest")
    version = manifest.get("schema_version", 1)
    if type(version) is not int or version != 1:
        raise ValueError("schema_version must be integer 1")
    title = _text(manifest.get("title", "Research provenance index"), "title")
    date = _text(date, "date")
    try:
        if calendar_date.fromisoformat(date).isoformat() != date:
            raise ValueError("noncanonical date")
    except ValueError as exc:
        raise ValueError("date must be a valid YYYY-MM-DD") from exc
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    if not isinstance(manifest["nodes"], list) or not manifest["nodes"]:
        raise ValueError("nodes must be a nonempty list")
    if not isinstance(manifest["edges"], list):
        raise ValueError("edges must be a list")
    nodes: dict[str, dict] = {}
    hashes: dict[Path, str] = {}
    for item in manifest["nodes"]:
        item = _fields(item, {"id", "kind", "status", "source"}, {"anchor"}, "node")
        node_id = _text(item["id"], "node id")
        if not ID_PATTERN.fullmatch(node_id):
            raise ValueError(f"invalid node id: {node_id!r}")
        if node_id in nodes:
            raise ValueError(f"duplicate node id: {node_id!r}")
        kind, status = _text(item["kind"], "node kind"), _text(item["status"], "node status")
        if kind not in KINDS or status not in STATUSES:
            raise ValueError(f"unknown node kind or status: {node_id!r}")
        source, resolved = _source(root, item["source"])
        anchor = _text(item.get("anchor", ""), "anchor", allow_empty=True)
        if resolved not in hashes:
            hashes[resolved] = hashlib.sha256(resolved.read_bytes()).hexdigest()
        nodes[node_id] = {"id": node_id, "kind": kind, "status": status,
                          "source": source, "anchor": anchor,
                          "sha256": hashes[resolved], "date": date}
    edges = []
    seen = set()
    for item in manifest["edges"]:
        item = _fields(item, {"source", "target", "relation"}, set(), "edge")
        source, target = _text(item["source"], "edge source"), _text(item["target"], "edge target")
        relation = _text(item["relation"], "edge relation")
        if source not in nodes or target not in nodes:
            raise ValueError(f"edge endpoint missing: {source!r} -> {target!r}")
        if relation not in RELATIONS:
            raise ValueError(f"unknown edge relation: {relation!r}")
        key = source, relation, target
        if key in seen:
            raise ValueError(f"duplicate edge: {key!r}")
        seen.add(key)
        edges.append({"source": source, "target": target, "relation": relation,
                      "source_sha256": nodes[source]["sha256"],
                      "target_sha256": nodes[target]["sha256"],
                      "source_status": nodes[source]["status"],
                      "target_status": nodes[target]["status"], "date": date})
    ordered_nodes = [nodes[node_id] for node_id in sorted(nodes)]
    edges.sort(key=lambda item: (item["source"], item["relation"], item["target"]))
    lines = [f"# {_cell(title)}", "", f"Declared as-of date: {date}.", "",
             "This is an explicit file-based index, not a graph database or an inference engine. "
             "Statuses and relations are declarations from the manifest, not verified scientific "
             "conclusions. SHA-256 identifies whole-file source bytes; anchors are unverified "
             "citation hints. Only listed sources were read.", "", "## Nodes", "",
             "| ID | Kind | Status | Repository-relative source | Anchor | SHA-256 |",
             "| --- | --- | --- | --- | --- | --- |"]
    for node in ordered_nodes:
        lines.append("| " + " | ".join(_cell(node[key]) for key in
                                       ("id", "kind", "status", "source", "anchor", "sha256")) + " |")
    lines.extend(["", "## Declared edges", "", "| Source | Relation | Target |", "| --- | --- | --- |"])
    for edge in edges:
        lines.append("| " + " | ".join(_cell(edge[key]) for key in ("source", "relation", "target")) + " |")
    return {"markdown": "\n".join(lines) + "\n",
            "nodes_csv": _csv(("id", "kind", "status", "source", "anchor", "sha256", "date"), ordered_nodes),
            "edges_csv": _csv(("source", "target", "relation", "source_sha256", "target_sha256",
                               "source_status", "target_status", "date"), edges)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--date", required=True, help="Explicit as-of date, YYYY-MM-DD")
    parser.add_argument("--out", required=True, type=Path, help="Output filename prefix")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        artifacts = build(manifest, args.root, args.date)
        paths = {"markdown": Path(str(args.out) + ".md"),
                 "nodes_csv": Path(str(args.out) + "_nodes.csv"),
                 "edges_csv": Path(str(args.out) + "_edges.csv")}
        root = args.root.resolve(strict=True)
        protected = {args.manifest.resolve(strict=True)}
        protected.update(_source(root, node["source"])[1] for node in manifest["nodes"])
        if any(path.resolve() in protected
               or (path.exists() and any(path.samefile(source) for source in protected))
               for path in paths.values()):
            raise ValueError("output must not overwrite the manifest or any indexed source")
        destinations = list(paths.values())
        if any(left.resolve() == right.resolve()
               or (left.exists() and right.exists() and left.samefile(right))
               for index, left in enumerate(destinations) for right in destinations[index + 1:]):
            raise ValueError("output paths must identify distinct files")
        for key, path in paths.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(artifacts[key], encoding="utf-8", newline="\n")
    except (OSError, RuntimeError, ValueError) as exc:
        parser.exit(2, f"provenance error: {exc}\n")


if __name__ == "__main__":
    main()
