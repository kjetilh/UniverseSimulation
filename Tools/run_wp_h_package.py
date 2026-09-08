#!/usr/bin/env python3
"""Operational WP-H runner: frozen scientific code, timing, ordered execution."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from Tools import state_graph_dimension_lab as h
from Tools import influence_order_lab as lab


def replay():
    spec=h.load_spec()
    gates=lab.read_csv(h.DOC/'WP-F2_attempt2_gates.csv')
    assert len(gates)==4 and all(g['complete']=='True' for g in gates)
    assert not (h.DOC/'WP-H_replay_audit.csv').exists(), 'refusing duplicate replay'
    rows=lab.read_csv(h.DOC/'attempt_ledger.csv')
    for row in rows:
        if row['fingerprint']==spec['fingerprint']:
            row.update(attempts=1,last_outcome='replay_started_after_F2_attempt2_gates',escalated='no',
                       note='WP-H attempt 1; frozen source hashes checked. F2 R then M then gates completed before replay. No new dynamics beyond exact v16b replay.')
    lab.write_csv(h.DOC/'attempt_ledger.csv',rows)
    # Estimate from measured F2 dynamics; estimate includes explicit unknown base-build overhead.
    f2=[json.loads(p.read_text())['dynamics_seconds'] for p in h.DOC.glob('WP-F2_R_*_metadata.json')]
    estimate=dict(timestamp=datetime.now(timezone.utc).isoformat(),basis='measured sixteen F2 R 8192-step dynamics scaled to twelve 2048-step replays',
        replay_estimated_seconds=sum(f2)/16*12/4,
        caveat='different substrates/token growth and building original bases; forecast only, not an H measurement')
    (h.DOC/'WP-H_runtime_estimate.json').write_text(json.dumps(estimate,indent=2)+'\n')
    h.beat('RUNTIME_ESTIMATE before_full_H_replay '+json.dumps(estimate))
    h.replay()
    h.beat('REPLAY_VERIFIED analysis_is_next')


def analyze():
    import networkx as nx
    h.load_spec()
    assert not (h.DOC/'WP-H_observables.csv').exists(), 'refusing duplicate analysis'
    audit=lab.read_csv(h.DOC/'WP-H_replay_audit.csv')[0]
    graph=nx.Graph()
    for e in lab.read_csv(h.DOC/f'WP-H_{audit["history"]}_edges.csv'):
        graph.add_edge(int(e['u']),int(e['v']))
    start=time.monotonic()
    summary,balls,walks=h.measure(graph,h.load_spec()['seed']+900,'timing_pilot')
    elapsed=time.monotonic()-start
    lab.write_csv(h.DOC/'WP-H_timing_pilot_observables.csv',[summary])
    lab.write_csv(h.DOC/'WP-H_timing_pilot_balls.csv',balls)
    lab.write_csv(h.DOC/'WP-H_timing_pilot_returns.csv',walks)
    path=h.DOC/'WP-H_runtime_estimate.json'
    estimate=json.loads(path.read_text())
    estimate.update(analysis_pilot_seconds=elapsed,analysis_144_graph_estimate_seconds=144*elapsed,
        analysis_caveat='one universe graph; rewiring and positive graph costs differ; pilot excluded from all gate aggregates',
        pilot_graph_sha256=lab.sha(h.DOC/f'WP-H_{audit["history"]}_edges.csv'))
    path.write_text(json.dumps(estimate,indent=2)+'\n')
    h.beat(f'RUNTIME_ESTIMATE before_all_H_measurements pilot_seconds={elapsed:.6f} graphs=144 projected_seconds={144*elapsed:.6f}')
    start=time.monotonic()
    h.analyze()
    (h.DOC/'WP-H_analysis_runtime.json').write_text(json.dumps(dict(seconds=time.monotonic()-start),indent=2)+'\n')

if __name__=='__main__':
    if sys.argv[1:] == ['--replay']: replay()
    elif sys.argv[1:] == ['--analyze']: analyze()
    else: raise SystemExit('choose --replay or --analyze')
