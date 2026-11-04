"""UC3R: deterministic, first-episode observation of the archived UC3 edits."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import asdict, dataclass, field
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import local_growth_candidate as kernel
from Tools.local_growth_observer import _region

DATA = ROOT / "Documentation/Program"
MANIFEST_SHA = "2b34ca0e00ad384ad0cf2b92c4d6de56f57b2c36a9dd9fa3c331df5d7a500bcf"
PROTOCOL_SHA = "19c56981a886d8ef5d502f8af095b8b9f1e70f22560ddd50b827ac0bbadd6ede"
WINDOW = 16
STAGES = ("no_peak", "no_loss", "empty_R", "no_bud", "no_hit", "hit")


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return (a, b) if a < b else (b, a)


def compact(value):
    return json.dumps(value, separators=(",", ":"))


def partition(state):
    return {v: group for group in kernel.component_partition(state) for v in group}


@dataclass(frozen=True)
class Point:
    tick: int
    local_tick: int
    core: int


@dataclass
class Trace:
    clock: int = 0
    peak: Point = Point(0, 0, 0)
    peak_edges: frozenset = frozenset()
    loss: Point | None = None
    loss_kind: str | None = None
    loss_split: bool = False
    retained: frozenset = frozenset()
    followup: int = 0
    end_tick: int | None = None
    buds: list = field(default_factory=list)
    first_hit: dict | None = None
    post_initial_hit: dict | None = None
    growth: Point | None = None
    joint_growth: Point | None = None
    post_initial_joint_growth: Point | None = None

    def observe(self, point, component, core_edges, births, event, split, pre_incident):
        self.clock = point.local_tick
        if self.loss is None:
            if point.core > self.peak.core:
                self.peak = point
                self.peak_edges = core_edges
            elif self.peak.core >= 4 and 2 * point.core <= self.peak.core:
                self.loss, self.loss_kind, self.loss_split = point, event.kind, split
                self.retained = frozenset((a, b, birth) for a, b, birth in self.peak_edges
                                          if a in component and births.get((a, b)) == birth)
                self.end_tick = point.tick
            return
        if self.followup == WINDOW:
            return
        self.followup += 1
        self.end_tick = point.tick
        if event.kind == "bud":
            pair = edge(event.source, event.carried)
            anchor = (*pair, pre_incident[pair])
            eligible = sorted(inst for pair, birth in pre_incident.items()
                              if (inst := (*pair, birth)) in self.retained)
            bud = dict(tick=point.tick, local_tick=point.local_tick, followup_edit=self.followup,
                       actor_unit=event.unit_index, source=event.source, anchor=event.carried,
                       newborn=event.born, edge_birth_tick=anchor[2], core_after=point.core,
                       incident_R=len(eligible), degree=len(pre_incident),
                       eligible_instances=compact(eligible), hit=anchor in self.retained)
            self.buds.append(bud)
            if bud["hit"]:
                if self.first_hit is None:
                    self.first_hit = bud
                if anchor[2] > 0 and self.post_initial_hit is None:
                    self.post_initial_hit = bud
        if point.core >= self.loss.core + 2:
            if self.growth is None:
                self.growth = point
            if self.first_hit and self.joint_growth is None:
                self.joint_growth = point
            if self.post_initial_hit and self.post_initial_joint_growth is None:
                self.post_initial_joint_growth = point

    def stage(self):
        if self.peak.core < 4:
            return "no_peak"
        if self.loss is None:
            return "no_loss"
        if not self.retained:
            return "empty_R"
        if not self.buds:
            return "no_bud"
        return "hit" if self.first_hit else "no_hit"

    def row(self):
        row = dict(stage=self.stage(), seen_edits=self.clock, loss_kind=self.loss_kind,
                   loss_split=self.loss_split, peak_edges=len(self.peak_edges),
                   peak_instances=compact(sorted(self.peak_edges)), retained_edges=len(self.retained),
                   retained_instances=compact(sorted(self.retained)),
                   retained_post_initial=sum(b > 0 for _, _, b in self.retained),
                   followup_edits=self.followup, followup_end_tick=self.end_tick,
                   short_followup=self.loss is not None and self.followup < WINDOW,
                   bud_opportunities=len(self.buds), hit_buds=sum(b["hit"] for b in self.buds))
        for name in ("peak", "loss", "growth", "joint_growth", "post_initial_joint_growth"):
            point = getattr(self, name)
            for key in ("tick", "local_tick", "core"):
                row[f"{name}_{key}"] = getattr(point, key) if point else None
        for name in ("first_hit", "post_initial_hit"):
            hit = getattr(self, name)
            for key in ("tick", "local_tick", "source", "anchor", "edge_birth_tick", "core_after"):
                row[f"{name}_{key}"] = hit[key] if hit else None
        return row


class Replay:
    """A tree and deterministic kernel edits. step() takes the pre-event bud anchor."""
    def __init__(self, initial):
        self.run = initial["run_id"]
        self.n = len(initial["nodes"])
        self.state = kernel.make_state(initial["nodes"], initial["edges"], initial["unit_hosts"],
                                       initial.get("next_node_id"))
        self.parts = partition(self.state)
        self.births = dict.fromkeys(kernel.edge_set(self.state), 0)
        require(self.n > 0 and len(set(self.parts.values())) == 1 and len(self.births) == self.n - 1,
                f"{self.run}: initial graph must be a tree")
        self.traces = [Trace() for _ in self.state.units]
        self.buds = []
        self.last_split = False

    def step(self, unit_index, kind, target, carried=None):
        state = self.state
        source = state.units[unit_index]
        origin = self.parts[source]
        seen = [i for i, host in enumerate(state.units) if host in origin]
        pre_incident = {edge(source, v): self.births[edge(source, v)]
                        for v in state.adjacency[source]} if kind == "bud" else {}
        event = kernel.apply_event(state, unit_index, kind, target, carried)
        edges_after = kernel.edge_set(state)
        for pair in self.births.keys() - edges_after:
            del self.births[pair]
        for pair in edges_after - self.births.keys():
            self.births[pair] = state.ticks
        after = partition(state)
        self.last_split = len(set(after.values())) > len(set(self.parts.values()))
        self.parts = after
        views = {}
        for tag in seen:
            component = after[state.units[tag]]
            if component not in views:
                region = _region(state.adjacency, component)
                core_edges = frozenset((a, b, self.births[(a, b)]) for a, b in region["core_edges"])
                views[component] = len(region["core_nodes"]), core_edges
            size, core_edges = views[component]
            trace = self.traces[tag]
            point = Point(state.ticks, trace.clock + 1, size)
            old_count = len(trace.buds)
            trace.observe(point, component, core_edges, self.births, event, self.last_split, pre_incident)
            if len(trace.buds) > old_count:
                self.buds.append(dict(run_id=self.run, initial_nodes=self.n, unit_index=tag,
                                      peak_tick=trace.peak.tick, peak_core=trace.peak.core,
                                      loss_tick=trace.loss.tick, loss_core=trace.loss.core,
                                      attempt=state.attempts, **trace.buds[-1]))
        return event

    def tag_rows(self):
        return [dict(run_id=self.run, initial_nodes=self.n, unit_index=i, **t.row())
                for i, t in enumerate(self.traces)]


def audit_world(initial, events, summary, observation):
    replay = Replay(initial)
    state = replay.state
    counts = Counter()
    max_nodes, drift = replay.n, 0.0
    for row in events:
        index, source = int(row["unit_index"]), int(row["source"])
        kind = row["kind"]
        label = f"{replay.run} attempt {row['attempt']}"
        require(0 <= index < len(state.units) and source == state.units[index] and kind in kernel.CLASSES,
                f"{label}: source, unit or class")
        collapsible = {v for v in state.units if kernel._collapse_neighbors(state, v)}
        active = sum(bool(state.adjacency[v]) for v in state.units)
        require((active, len(collapsible)) == (int(row["active_units_before"]),
                                                int(row["collapsible_units_before"])), f"{label}: activity")
        drift += (active - 2 * len(collapsible)) / (8 * len(state.units))
        if row["changed"] == "True":
            payload = {k: int(row[k]) if row[k] else None for k in ("target", "carried", "born", "removed")}
            target = payload["carried"] if kind == "bud" else payload["target"]
            event = replay.step(index, kind, target, None if kind == "bud" else payload["carried"])
            require(all(str(value if value is not None else "") == row[key] for key, value in asdict(event).items()),
                    f"{label}: successful event mismatch")
            split = replay.last_split
            counts[kind] += 1
            counts["component_splits"] += split
            max_nodes = max(max_nodes, len(state.adjacency))
        else:
            require(row["changed"] == "False" and row["reason"] == "blocked"
                    and all(not row[k] for k in ("target", "carried", "born", "removed")), f"{label}: blocked fields")
            if kind == "slide":
                available = kernel.admissible_moves(state, index)
            elif kind == "collapse":
                available = source in collapsible
            else:
                available = state.adjacency[source]
            require(not available, f"{label}: selected class could execute")
            state.attempts += 1
            counts["blocked_" + kind] += 1
            split = False
        require((state.attempts, state.ticks, str(split)) ==
                (int(row["attempt"]), int(row["tick"]), row["component_split"]), f"{label}: clocks or split")
    nodes, edges, comps = len(state.adjacency), len(replay.births), len(set(replay.parts.values()))
    audit = {k: counts[k] for k in (*kernel.CLASSES, *("blocked_" + c for c in kernel.CLASSES), "component_splits")}
    clocks = [trace.clock for trace in replay.traces]
    require(clocks == [t["component_exposures"] for t in observation["per_unit"]], f"{replay.run}: tag clocks")
    final_hash = hashlib.sha256(repr(kernel.state_snapshot(state)).encode()).hexdigest()
    audit.update(attempts=state.attempts, ticks=state.ticks, max_N=max_nodes, final_N=nodes, final_E=edges,
                 final_C=comps, final_beta=edges - nodes + comps, final_units=len(state.units),
                 isolated_units=sum(not state.adjacency[v] for v in state.units), final_state_sha256=final_hash,
                 min_component_exposures=min(clocks), max_component_exposures=max(clocks),
                 integrated_expected_node_drift=drift)
    for key, value in audit.items():
        require(str(value) == summary[key], f"{replay.run}: summary mismatch on {key}")
    require(audit["isolated_units"] == len(state.units) and summary["stop"] == "activity_absorbed",
            f"{replay.run}: terminal condition")
    return replay, audit


def coverage(tags, buds):
    hits = [b for b in buds if b["hit"]]
    physical = lambda rows: sorted({(b["run_id"], b["tick"]) for b in rows})
    return dict(tags=len(tags), **{"stage_" + s: sum(t["stage"] == s for t in tags) for s in STAGES},
                tags_peak=sum(t["peak_core"] >= 4 for t in tags),
                tags_loss=sum(t["loss_tick"] is not None for t in tags),
                tags_retained=sum(t["retained_edges"] > 0 for t in tags),
                tags_retained_post_initial=sum(t["retained_post_initial"] > 0 for t in tags),
                tags_followup_bud=sum(t["bud_opportunities"] > 0 for t in tags),
                tags_zero_followup=sum(t["loss_tick"] is not None and t["followup_edits"] == 0 for t in tags),
                tags_short_followup=sum(t["short_followup"] for t in tags),
                tags_full_followup=sum(t["followup_edits"] == WINDOW for t in tags),
                tags_hit=sum(t["first_hit_tick"] is not None for t in tags),
                tags_post_initial_hit=sum(t["post_initial_hit_tick"] is not None for t in tags),
                tags_growth=sum(t["growth_tick"] is not None for t in tags),
                tags_joint=sum(t["joint_growth_tick"] is not None for t in tags),
                tags_post_initial_joint=sum(t["post_initial_joint_growth_tick"] is not None for t in tags),
                loss_split=sum(t["loss_split"] for t in tags),
                **{"loss_" + c: sum(t["loss_kind"] == c and not t["loss_split"] for t in tags)
                   for c in kernel.CLASSES},
                tag_buds=len(buds), tag_hits=len(hits), unique_buds=len(physical(buds)),
                unique_hits=len(physical(hits)),
                unique_post_initial_hits=len(physical(b for b in hits if b["edge_birth_tick"] > 0)))


def summarize(worlds):
    keys = list(coverage([], []))
    return dict(worlds=len(worlds), totals={k: sum(w[k] for w in worlds) for k in keys},
                worlds_with={k: sum(w[k] > 0 for w in worlds) for k in keys},
                conditional_O_minus_E_sign_worlds={s: sum(w["conditional_O_minus_E_sign"] == s for w in worlds)
                                                   for s in ("positive", "tied", "negative")})


def write_csv(path, rows, fields=None):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(name):
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def extract(out):
    manifest_path = DATA / "UC3_candidate.json"
    require(digest(manifest_path) == MANIFEST_SHA and digest(DATA / "UC3R_protocol.md") == PROTOCOL_SHA,
            "Archived manifest or observation protocol changed")
    manifest = json.loads(manifest_path.read_text())
    for name, sha in manifest["evidence_sha256"].items():
        require(digest(DATA / name) == sha, f"Evidence hash mismatch: {name}")
    for name, sha in manifest["source_sha256"].items():
        path = DATA / "UC3_preregistration.json" if name == "preregistration" else ROOT / name
        require(digest(path) == sha, f"Archived source hash mismatch: {name}")
    starts = json.loads((DATA / "UC3_candidate_initial.json").read_text())
    observations = {row["run_id"]: row for row in json.loads((DATA / "UC3_candidate_observations.json").read_text())}
    summaries = {row["run_id"]: row for row in read_csv("UC3_candidate_summary.csv")}
    events = defaultdict(list)
    for row in read_csv("UC3_candidate_events.csv"):
        events[row["run_id"]].append(row)
    ids = {s["run_id"] for s in starts}
    require(len(ids) == len(starts) == manifest["runs"] == 16 and ids == summaries.keys()
            and ids == observations.keys() and ids == events.keys(), "Incomplete candidate population")
    tags, buds, worlds = [], [], []
    for initial in starts:
        run = initial["run_id"]
        replay, audit = audit_world(initial, events[run], summaries[run], observations[run])
        rows = replay.tag_rows()
        tags.extend(rows)
        buds.extend(replay.buds)
        counts = coverage(rows, replay.buds)
        expected = sum((Fraction(b["incident_R"], b["degree"]) for b in replay.buds), Fraction(0))
        difference = counts["tag_hits"] - expected
        worlds.append(dict(run_id=run, initial_nodes=replay.n, attempts=audit["attempts"], ticks=audit["ticks"],
                           stop=summaries[run]["stop"], final_state_sha256=audit["final_state_sha256"], **counts,
                           conditional_expected_tag_hits=str(expected), conditional_O_minus_E=str(difference),
                           conditional_O_minus_E_sign="positive" if difference > 0 else "negative" if difference < 0 else "tied"))
    require(sum(w["attempts"] for w in worlds) == manifest["total_attempts"] and
            sum(w["ticks"] for w in worlds) == manifest["total_changes"], "Archive totals mismatch")
    hits = sorted({(b["run_id"], b["tick"]) for b in buds if b["hit"]})
    post_hits = sorted({(b["run_id"], b["tick"]) for b in buds if b["hit"] and b["edge_birth_tick"] > 0})
    witnesses = {}
    for name, key in (("hit", "first_hit_tick"), ("post_initial_hit", "post_initial_hit_tick"),
                      ("joint", "joint_growth_tick"), ("post_initial_joint", "post_initial_joint_growth_tick")):
        witnesses[name] = next((t for t in tags if t[key] is not None), None)
    result = dict(round="UC3R", design="post_hoc_descriptive", followup_seen_edits=WINDOW,
                  source_manifest_sha256=MANIFEST_SHA, protocol_sha256=PROTOCOL_SHA,
                  extractor_sha256=digest(Path(__file__)), evidence_sha256=manifest["evidence_sha256"],
                  archived_source_sha256=manifest["source_sha256"], attempts=manifest["total_attempts"],
                  ticks=manifest["total_changes"], **summarize(worlds),
                  by_initial_nodes={n: summarize([w for w in worlds if w["initial_nodes"] == n])
                                    for n in sorted({w["initial_nodes"] for w in worlds})},
                  hit_events=hits, post_initial_hit_events=post_hits, witnesses=witnesses)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "UC3R_worlds.csv", worlds)
    write_csv(out / "UC3R_tags.csv", tags)
    write_csv(out / "UC3R_buds.csv", buds, fields=(
        "run_id", "initial_nodes", "unit_index", "peak_tick", "peak_core", "loss_tick", "loss_core",
        "attempt", "tick", "local_tick", "followup_edit", "actor_unit", "source", "anchor", "newborn",
        "edge_birth_tick", "core_after", "incident_R", "degree", "eligible_instances", "hit"))
    result["output_sha256"] = {p: digest(out / p) for p in ("UC3R_worlds.csv", "UC3R_tags.csv", "UC3R_buds.csv")}
    (out / "UC3R_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    extract(parser.parse_args().out)
