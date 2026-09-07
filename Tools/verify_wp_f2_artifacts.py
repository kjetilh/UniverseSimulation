#!/usr/bin/env python3
"""Read-only audit of completed WP-F2 serialized artifacts (no fresh dynamics)."""
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from Tools.influence_order_lab import DOC,FROZEN,sha,read_csv,write_csv,load_spec,runtime,heartbeat


def main():
    load_spec()
    v7,a,b,ac=runtime()
    rows=[]
    for path in sorted(DOC.glob('WP-F2_*_summary.csv')):
        name=path.name.removesuffix('_summary.csv')
        event_path=DOC/f'{name}_events.csv'
        if not event_path.exists(): continue
        events=read_csv(event_path)
        summary=read_csv(path)
        metadata=json.loads((DOC/f'{name}_metadata.json').read_text())
        assert len(events)==metadata['steps']
        assert metadata['frozen_sha256']==sha(FROZEN)
        times=[float(e['time']) for e in events]
        assert all(t>0 for t in times)
        assert all(x<y for x,y in zip(times,times[1:]))
        assert abs(sum(float(e['dt']) for e in events)-times[-1])<1e-10
        for order,rfield,wfield,pfield in [('kernel','reads','writes','parents'),
                                         ('legacy','legacy_reads','legacy_writes','legacy_parents')]:
            dag=b.DependencyDAG()
            for i,e in enumerate(events):
                assert int(e['event_id'])==i
                reads=set(filter(None,e[rfield].split(';')))
                writes=set(filter(None,e[wfield].split(';')))
                observed=dag.add(reads,writes)
                assert set(observed)==set(int(p) for p in e[pfield].split(';') if p)
            row=next(r for r in summary if r['order']==order)
            analysis=dag.analyze()
            assert analysis['n_events']==len(events)
            assert int(row['dag_edges'])==analysis['edge_count']
            assert int(row['height'])==analysis['causal_depth']
            assert int(row['comparable_pairs'])==analysis['comparable_pairs']
            assert analysis['edge_witness_errors']==0
        snapshots=read_csv(DOC/f'{name}_snapshots.csv')
        snapshot_ids={int(s['snapshot']) for s in snapshots}
        assert all(int(e['snapshot']) in snapshot_ids for e in events)
        for e in events:
            s=int(e['snapshot'])
            assert s%512==0 and s<=int(e['event_id'])
            if metadata['mode']=='R': assert int(e['event_id'])-s<512
        curves=read_csv(DOC/f'{name}_curves.csv')
        for c in curves:
            assert int(c['pair_count'])==int(c['finite_distance_pairs'])+int(c['undefined_distance_pairs'])
        artifacts=[path,event_path,DOC/f'{name}_metadata.json',DOC/f'{name}_snapshots.csv',DOC/f'{name}_curves.csv']
        rows.append(dict(history=name,events=len(events),dag_resource_roundtrip=True,
            original_DAG_analysis_match=True,clock_sum_match=True,snapshot_contract=True,
            hashes=json.dumps({p.name:sha(p) for p in artifacts},sort_keys=True)))
        heartbeat(f'verify {name} PASS')
    assert rows, 'no completed artifacts'
    write_csv(DOC/'WP-F2_verification.csv',rows)
    print('Verified',len(rows),'completed histories, including separately labeled pilot')


if __name__=='__main__': main()
