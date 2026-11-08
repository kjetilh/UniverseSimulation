"""Screen fresh UC3 worlds, measure both instrument references, then run natural continuations."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import gzip
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import run_uc3m
from Tools.run_uc3g import calibrate, check_manifest, compact, sha, summarize, write_csv
from Tools.uc3i_inheritance import common_cohort, follow

STEM = "UC3I_"
ARMS = run_uc3m.ARMS
REPS = run_uc3m.REPS


def screen(job):
    world, pair = run_uc3m.screen(job)
    if pair:
        pair["cohort"] = common_cohort(pair)
        if not pair["cohort"]:
            world["prefix_stop"] = "empty_common_cohort"
            pair = None
    return world, pair


def evaluate(job):
    pair, modes = job
    rows = []
    for arm in ARMS:
        for mode in modes:
            for rep in range(REPS):
                seed = int(sha(f"UC3I/{pair['world']}/{arm}/{mode}/{rep}".encode())[:16], 16)
                rows.append(dict(world=pair["world"], arm=arm, mode=mode, rep=rep, seed=seed,
                                 **follow(pair, arm, mode, seed)))
    return rows


def run(out, workers):
    out.mkdir(parents=True, exist_ok=True)
    if any(out.glob(STEM + "*")):
        raise FileExistsError("Expected a fresh output directory")
    jobs = [(n, i) for n in run_uc3m.SIZES for i in range(1000000, 1000256)]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        screened = list(pool.map(screen, jobs))
        worlds = [w for w, _ in screened]
        pairs = [p for _, p in screened if p]
        print(f"{len(worlds)} worlds, {len(pairs)} eligible", flush=True)
        (out/"UC3I_pairs.jsonl").write_text("".join(compact(p)+"\n" for p in pairs))
        def measure(modes):
            rows = [r for batch in pool.map(evaluate, [(p, modes) for p in pairs]) for r in batch]
            check_manifest(pairs, modes, rows)
            return rows
        controls = measure(("null", "positive"))
        reference_ok = bool(pairs) and all(r["complete"] and r["success"] == (r["mode"] == "positive")
                                           for r in controls)
        print(f"Reference gate {reference_ok}", flush=True)
        natural = measure(("natural",)) if reference_ok else []
    counts = Counter((r["world"], r["arm"]) for r in natural if r["success"])
    censored = Counter(r["world"] for r in natural if r["censored"])
    for w in worlds:
        measured = reference_ok and w["prefix_stop"] == "matched"
        for arm in ARMS:
            w[arm+"_hits"] = counts[w["world"], arm] if measured else None
        w["natural_censored"] = censored[w["world"]] if measured else None
    write_csv(out/"UC3I_worlds.csv", worlds)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td)/"rows.csv"
        if controls or natural:
            write_csv(path, controls + natural)
        else:
            path.write_text("world,arm,mode,rep,seed,success,complete,inherited,strict,marks,witnesses,exposure,attempts,stop,censored\n")
        (out/"UC3I_followups.csv.gz").write_bytes(gzip.compress(path.read_bytes(), mtime=0))
    details = {}
    for arm in ARMS:
        rows = [r for r in natural if r["arm"] == arm]
        details[arm] = dict(complete=sum(r["complete"] for r in rows),
                            strict=sum(bool(r["strict"]) for r in rows),
                            witnesses=dict(Counter(len(r["inherited"]) for r in rows if r["complete"])),
                            stops=dict(Counter(r["stop"] for r in rows)))
    sources = set(run_uc3m.SOURCES) | {"Tools/run_uc3i.py", "Tools/uc3i_inheritance.py", "Documentation/Program/UC3I_protocol.md"}
    result = dict(reference_pass=reference_ok, reference=calibrate(controls),
                  reference_cycles=dict(Counter(r["arm"]+"/"+r["mode"] for r in controls if r["complete"])),
                  world_count=len(worlds), matched_count=len(pairs),
                  prefix_stops=dict(Counter(w["prefix_stop"] for w in worlds)),
                  analysis=summarize(worlds, True) if reference_ok else {"verdict":"instrumentation_only"},
                  details=details, source_sha256={s:sha((ROOT/s).read_bytes()) for s in sorted(sources)},
                  evidence_sha256={p.name:sha(p.read_bytes()) for p in sorted(out.glob(STEM+"*"))})
    (out/"UC3I_result.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(compact(result["analysis"]), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    run(args.out, args.workers)
