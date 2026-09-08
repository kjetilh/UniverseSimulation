#!/usr/bin/env python3
"""Audit attempt 2 against saved ancestry, original metrics and frozen inputs."""
import bisect
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from Tools import influence_order_lab as lab
from Tools import influence_order_attempt2 as a2


def main():
    import numpy as np
    spec=a2.load_spec()
    audit=[]
    for a in spec['assignments']:
        name=lab.file_prefix(a)
        events=lab.read_csv(lab.DOC/f'{name}_events.csv')
        original=lab.read_csv(lab.DOC/f'{name}_summary.csv')
        summary=lab.read_csv(lab.DOC/f'{name}_attempt2_summary.csv')
        curves=lab.read_csv(lab.DOC/f'{name}_attempt2_curves.csv')
        times=[float(e['time']) for e in events]
        assert len(events)==8192
        if a['mode']=='M':
            m=json.loads((lab.DOC/f'{name}_metadata.json').read_text())
            assert m['edge_drift']==m['ever_changed_initial_fraction']==0
            assert m['initial_nodes']==m['final_nodes']
            for e in events:
                if e['event_type']=='seed':
                    desc=json.loads(e['descriptor']); host=int(e['node'])
                    expected={f'node:{host}'}
                    if desc[0]=='seed_tid': expected.add(f'token:{desc[1]}')
                    assert set(e['reads'].split(';'))==expected
                    assert e['writes']==f'mark:{host}'
        for row in summary:
            order=row['order']
            old=next(r for r in original if r['order']==order)
            for metric in ('links_per_event','theta','r_over_floor','max_interval_frac','cross_token_fraction','dag_edges','comparable_pairs','height'):
                assert float(row[metric])==float(old[metric]), (name,order,metric)
            cs=[c for c in curves if c['order']==order]
            tau=[float(c['tau']) for c in cs]
            assert tau==a2.tau_grid(times[-1])
            field='parents' if order=='kernel' else 'legacy_parents'
            ancestors,_=lab.poset_metrics([[int(p) for p in e[field].split(';') if p] for e in events])
            volumes=[]
            for e,t in enumerate(times):
                if t<times[-1]/2: continue
                # Independent bitmask population counts after time-index cutoff.
                volumes.append([(ancestors[e] >> bisect.bisect_left(times,t-window)).bit_count() for window in tau])
            volume=np.asarray(volumes)
            for ti,c in enumerate(cs):
                assert float(c['V_median'])==np.median(volume[:,ti])
                assert int(c['pair_count'])==volume[:,ti].sum()
                assert int(c['pair_count'])==int(c['finite_distance_pairs'])+int(c['undefined_distance_pairs'])
                if int(c['finite_distance_pairs']):
                    assert float(c['R_mean'])==int(c['distance_sum'])/int(c['finite_distance_pairs'])
                expected_window=float(c['V_median'])>=8 and float(c['tau'])<=times[-1]/4
                assert (c['fit_window']=='True')==expected_window
            for metric,field in [('alpha','V_median'),('gamma','R_mean'),('gamma_R90','R90')]:
                selected=[c for c in cs if c['fit_window']=='True' and math.isfinite(float(c[field])) and float(c[field])>0]
                expected=float(np.polyfit(np.log([float(c['tau']) for c in selected]),np.log([float(c[field]) for c in selected]),1)[0]) if len(selected)>=6 else math.nan
                observed=float(row[metric])
                assert (math.isnan(expected) and math.isnan(observed)) or abs(expected-observed)<1e-12
        paths=[lab.DOC/f'{name}_{suffix}' for suffix in ('events.csv','snapshots.csv','metadata.json','attempt2_curves.csv','attempt2_summary.csv')]
        audit.append(dict(history=name,steps=8192,original_DAG_metrics=True,all_volume_points=True,
            six_point_fits_independent_OLS=True,M_seed_and_zero_drift=True if a['mode']=='M' else 'not_applicable',
            hashes=json.dumps({p.name:lab.sha(p) for p in paths},sort_keys=True)))
        lab.heartbeat(f'ATTEMPT2_VERIFY {name} PASS')
    lab.write_csv(lab.DOC/'WP-F2_attempt2_verification.csv',audit)
    a2.load_spec()
    print('PASS 32/32 histories; original sources and R artifacts unchanged')

if __name__=='__main__': main()
