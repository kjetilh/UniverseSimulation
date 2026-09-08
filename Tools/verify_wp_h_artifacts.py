#!/usr/bin/env python3
"""Independent saved-artifact checks for WP-H; no dynamics or threshold changes."""
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from Tools import state_graph_dimension_lab as h
from Tools.influence_order_lab import read_csv,write_csv,sha


def main():
    import numpy as np
    import networkx as nx
    spec=h.load_spec()
    summaries=read_csv(h.DOC/'WP-H_observables.csv')
    audits=read_csv(h.DOC/'WP-H_replay_audit.csv')
    gates=read_csv(h.DOC/'WP-H_gate_per_graph.csv')
    assert len(summaries)==144 and len(audits)==len(gates)==12
    verified=[]; references=[]
    for audit in audits:
        key=audit['history']
        path=h.DOC/f'WP-H_{key}_edges.csv'
        assert sha(path)==audit['edges_sha256']
        assert audit['all_descriptors_match']==audit['all_times_match']=='True'
        assert audit['final_nodes']==audit['expected_final_nodes']
        assert audit['final_tokens']==audit['expected_final_tokens']
        base=nx.read_edgelist(path,delimiter=',',comments='u,',nodetype=int)
        group=[r for r in summaries if r['history']==key]
        assert len(group)==12
        return_rows=read_csv(h.DOC/f'WP-H_{key}_returns.csv')
        ball_rows=read_csv(h.DOC/f'WP-H_{key}_balls.csv')
        returns={}; balls={}
        for r in return_rows: returns.setdefault(r['label'],{}).setdefault(int(r['root']),{})[int(r['t'])]=float(r['P'])
        for r in ball_rows: balls.setdefault(r['label'],{}).setdefault(int(r['root']),{})[int(r['r'])]=int(r['B'])
        for row in group:
            graph_path=h.DOC/f'WP-H_{row["label"]}_graph.csv'
            g=nx.read_edgelist(graph_path,delimiter=',',comments='u,',nodetype=int)
            assert len(g)==int(row['nodes'])==int(audit['final_nodes'])
            assert g.number_of_edges()==int(row['edges'])
            if row['kind']=='null': assert dict(g.degree())==dict(base.degree())
            if row['kind']=='universe': assert set(map(frozenset,g.edges()))==set(map(frozenset,base.edges()))
            roots=returns[row['label']]
            assert len(roots)==64
            exponents=[]
            for root,walk in roots.items():
                assert set(walk)==set(range(1,65))
                assert all(0<=p<=1 for p in walk.values())
                ts=list(range(4,65,2))
                exponents.append(-2*float(np.polyfit(np.log(ts),np.log([walk[t] for t in ts]),1)[0]))
                distances=nx.single_source_shortest_path_length(g,root,cutoff=10)
                assert balls[row['label']][root]=={r:sum(d<=r for d in distances.values()) for r in range(1,11)}
                if row['kind']=='ring':
                    for t,p in walk.items():
                        expected=0.0 if t%2 else math.comb(t,t//2)/2**t
                        assert abs(p-expected)<1e-12
            assert abs(float(row['ds_median'])-np.median(exponents))<1e-12
            volumes=np.mean([[balls[row['label']][root][r] for r in range(1,11)] for root in roots],axis=0)
            for field,rs in [('d_vol_3_6',list(range(3,7))),('d_vol_6_10',list(range(6,11)))]:
                expected=np.polyfit(np.log(rs),np.log([volumes[r-1] for r in rs]),1)[0]
                assert abs(float(row[field])-expected)<1e-12
            verified.append(dict(label=row['label'],kind=row['kind'],nodes=True,degree_sequence=True if row['kind']=='null' else 'not_applicable',
                all_64_root_ball_curves=True,saved_walk_OLS=True,ring_returns_analytic=True if row['kind']=='ring' else 'not_applicable',
                graph_sha256=sha(graph_path)))
        nulls=[float(r['ds_median']) for r in group if r['kind']=='null']
        low,high=np.quantile(nulls,[.025,.975])
        gate=next(g for g in gates if g['history']==key)
        assert abs(float(gate['null_ci_low'])-low)<1e-12 and abs(float(gate['null_ci_high'])-high)<1e-12
        for kind in ('universe','ring','lat2','lat2_rewired'):
            ds=float(next(r['ds_median'] for r in group if r['kind']==kind))
            refs=dict(history=key,kind=kind,ds_median=ds,null_low=float(low),null_high=float(high),below=ds<low,above=ds>high,
                sign_vs_null_median=int(ds>np.median(nulls))-int(ds<np.median(nulls)))
            references.append(refs)
            if kind=='universe':
                assert (gate['below']=='True')==bool(ds<low)
                assert (gate['above']=='True')==bool(ds>high)
        h.beat(f'ARTIFACT_VERIFY {key} PASS graphs=12')
    write_csv(h.DOC/'WP-H_verification.csv',verified)
    write_csv(h.DOC/'WP-H_reference_audit.csv',references)
    inventory=[dict(path=str(p.relative_to(h.ROOT)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(h.DOC.glob('WP-H_*.csv')) if p.name!='WP-H_artifact_hashes.csv']
    write_csv(h.DOC/'WP-H_artifact_hashes.csv',inventory)
    print('PASS 12 replay audits; 144 graphs; 9216 root volume/fit checks; reference separation and gate arithmetic')

if __name__=='__main__': main()
