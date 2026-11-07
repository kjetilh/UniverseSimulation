from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from scripts.sync_orchestrator import (
    _http_json_request,
    collect_source_files,
    load_config,
)


def _git(release: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(release), *args])


def _tracked_files(release: Path, revision: str) -> dict[str, bytes]:
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision):
        raise ValueError("Expected the full Git commit hash.")
    if _git(release, "rev-parse", "--show-toplevel").decode().strip() != str(release):
        raise ValueError("The release must be the Git worktree root.")
    if _git(release, "rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("Release HEAD differs from the requested revision.")
    if _git(release, "status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("The release worktree must be clean.")
    tracked = {}
    for record in _git(release, "ls-tree", "-rz", revision).split(b"\0"):
        if record:
            metadata, name = record.split(b"\t", 1)
            mode, kind, oid = metadata.split()
            if kind == b"blob" and mode in (b"100644", b"100755"):
                tracked[os.fsdecode(name)] = oid
    return tracked


def _release_digest(release: Path, path: Path, tracked: dict[str, bytes]) -> str:
    rel = path.relative_to(release).as_posix()
    if path.resolve(strict=True) != path or rel not in tracked:
        raise ValueError(f"Expected a tracked regular release file: {rel}")
    raw = path.read_bytes()
    oid = tracked[rel]
    git_hash = hashlib.new("sha1" if len(oid) == 40 else "sha256")
    git_hash.update(f"blob {len(raw)}\0".encode())
    git_hash.update(raw)
    if git_hash.hexdigest().encode() != oid:
        raise ValueError(f"Release bytes differ from the commit: {rel}")
    return hashlib.sha256(raw).hexdigest()


def run_revalidation(
    config_path: Path, release: Path, revision: str, *, plan_only: bool = False
) -> dict:
    """Verify the pinned source and complete mirror inventory before sending one batch."""
    release = release.resolve(strict=True)
    tracked = _tracked_files(release, revision)
    config_path = config_path.absolute()
    config_sha256 = _release_digest(release, config_path, tracked)
    config = load_config(config_path, repo_override=release)
    settings = config.settings
    files = []
    counts = {}
    digests = {}
    mirror_paths = set()
    for source in config.sources:
        selected = collect_source_files(source)
        if not selected:
            raise ValueError(f"No files selected for {source.name}.")
        prefix = Path(settings.ingest_live_subdir) / source.target_subdir
        target = settings.ingest_root / prefix
        if target.resolve(strict=True) != target:
            raise ValueError(f"Mirror directory traverses a symlink: {prefix}")
        actual = set()
        for path in target.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Symlink in the source mirror: {path}")
            if path.is_file():
                actual.add(path.relative_to(target).as_posix())
        if actual != set(selected):
            raise ValueError(f"Mirror inventory differs for {source.name}.")
        counts[source.name] = len(selected)
        for rel in selected:
            path = source.repo_path / rel
            source_path = path.relative_to(release).as_posix()
            if source_path not in digests:
                digests[source_path] = _release_digest(release, path, tracked)
            digest = digests[source_path]
            if hashlib.sha256((target / rel).read_bytes()).hexdigest() != digest:
                raise ValueError(f"Mirror bytes differ from the commit: {prefix / rel}")
            mirror_path = (prefix / rel).as_posix()
            if mirror_path in mirror_paths:
                raise ValueError(f"Duplicate mirror path: {mirror_path}")
            mirror_paths.add(mirror_path)
            files.append({"path": mirror_path, "source_path": source_path,
                          "raw_sha256": digest, "source_type": source.source_type})

    payload = {"source_revision": revision, "files": files}
    result = {
        "plan_only": plan_only, "source_revision": revision,
        "config_sha256": config_sha256,
        "manifest_sha256": hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_counts": counts, "mirror_count": len(files), "source_file_count": len(digests),
    }
    if plan_only:
        return {**result, "ok": True, "manifest": files}

    key = os.environ.get(settings.admin_api_key_env, "").strip()
    if not key:
        raise ValueError(f"Missing admin credential: {settings.admin_api_key_env}")
    status, response = _http_json_request(
        method="POST", url=settings.admin_base_url + "/v1/admin/revalidate",
        timeout_sec=settings.request_timeout_sec, headers={"X-API-Key": key}, payload=payload,
    )
    summary = response.get("summary") if isinstance(response, dict) else None
    ok = (
        status == 200 and isinstance(summary, dict) and response.get("ok") is True
        and summary.get("source_revision") == revision
        and summary.get("verified_files") == len(files)
        and summary.get("verified_docs") == len(digests)
    )
    return {**result, "ok": ok, "http_status": status, "response": response}


def main() -> None:
    parser = argparse.ArgumentParser(description="Revalidate indexed sources against a committed release.")
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--config", type=Path, required=True, help="Tracked config in this release.")
    parser.add_argument("--plan-only", action="store_true", help="Verify sources/mirrors and print the manifest.")
    args = parser.parse_args()
    try:
        result = run_revalidation(args.config, args.release, args.revision, plan_only=args.plan_only)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
