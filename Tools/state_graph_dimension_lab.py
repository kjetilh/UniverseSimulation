#!/usr/bin/env python3
"""WP-H preregistered graph observables and exact v16b replay.

Replay with Python >=3.12 and existing NetworkX; analysis with the installed
Python 3.11 NumPy/SciPy/NetworkX environment. Does not modify v16 files.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from Tools.influence_order_lab import read_csv,write_csv,sha,fit,heartbeat,runtime
DOC=ROOT/'Documentation/Program'
FROZEN=DOC/'WP-H_frozen.json'


def beat(message):
    heartbeat(message,'WP-H')


def freeze():
    if FROZEN.exists():
        raise ValueError('refusing to overwrite preregistration')
    v7,a,b,ac=runtime()
    b.load_and_verify_preregistration()
    sources=sorted({str(Path(m.__file__).relative_to(ROOT)) for m in list(sys.modules.values())
        if getattr(m,'__file__',None) and str(m.__file__).startswith(str(ROOT))
        and str(m.__file__).endswith('.py')})
    sources += ['Documentation/v16b_run_summary.csv','Documentation/v16b_event_log.csv',
                'Documentation/v16b_pre_registration.csv','Tools/state_graph_dimension_lab.py']
    spec=dict(fingerprint='state-graph-dimension-vs-null',prepared_at=datetime.now(timezone.utc).isoformat(),
        source_hashes={p:sha(ROOT/p) for p in sources},
        assignments=read_csv(ROOT/'Documentation/v16b_run_summary.csv'),
        seed=2026090701, roots=64,null_replicates=8,swaps_per_edge=10,
        null='NetworkX double_edge_swap, simple graph, exactly 10*E successful swaps, max_tries=1000*E; disconnected outputs retained and disclosed',
        positive='ring and open near-square induced grid with exactly N nodes; third graph rewires exactly 2*floor(.1*E/2) distinct original edges via degree-preserving swaps',
        positive_drift='no previously added edge is selected; removed original fraction equals the preregistered even-integer rounding of 10%; actual drift reported',
        volumes='B(r) includes root; arithmetic mean over 64 fixed sampled roots; OLS log(mean B) vs log r on 3..6 and 6..10',
        spectral='exact transition propagation from 64 roots; ordinary non-lazy simple walk; mean return probability; OLS log P(t) vs log t on even t=4,6,...64; ds=-2*slope',
        spectral_reason='even times fixed before data to handle bipartite ring/grid zero odd returns; all t=1..64 saved; no stationary-floor subtraction',
        spectral_median='gate uses median of per-root d_s on the same even-time fit; aggregate-curve d_s also reported separately',
        distance='exact unordered all-node pairs; disconnected pairs assigned infinity; diameter infinity if disconnected; finite-pair median also saved',
        null_interval='linear percentile 2.5/97.5 of the eight null medians, no bootstrap of roots',
        threshold=dict(required_graphs=10,total_graphs=12,direction='same, above or below',boundary='strictly outside'),
        claim_limit='finite r<=10,t<=64 separation only; no proof of stable asymptotic dimension or uniform null mixing')
    FROZEN.write_text(json.dumps(spec,indent=2,sort_keys=True)+'\n')
    beat(f'preregistered sha256={sha(FROZEN)} execution_waits_for_WP_F2')
    (DOC/'WP-H_report.md').write_text('# WP-H rapport\n\nStatus: forberedt, ikke kjørt; WP-F2 må avsluttes først.\n\n'
        f'Frosset spesifikasjon SHA-256: `{sha(FROZEN)}`.\n'
        'Ingen kjøretidsmåling eller observerte tall ennå. Ingen konklusjon om lesning G.\n')


def load_spec():
    spec=json.loads(FROZEN.read_text())
    for p,digest in spec['source_hashes'].items():
        if sha(ROOT/p)!=digest:
            raise ValueError(f'frozen source changed: {p}')
    return spec


def history_id(row):
    return f"{row['growth_seed']}_{row['run_offset']}_{row['arm']}"


def replay():
    spec=load_spec()
    gates=read_csv(DOC/'WP-F2_gates.csv')
    assert all(r['complete']=='True' for r in gates), 'WP-F2 measurements must be complete first'
    v7,a,b,ac=runtime()
    assignments,rate,_=b.load_and_verify_preregistration()
    start=time.monotonic()
    beat('replay_start using_v16b_build_bases_and_identical_sampling_loop')
    bases,_=b.v10e.build_bases(b.v15.deep_ensembles([b.TARGET_NODES]),
                              b.v10e.recommended_regime('fast_balanced'),list(b.GROWTH_SEEDS))
    reference={}
    for event in read_csv(ROOT/'Documentation/v16b_event_log.csv'):
        reference.setdefault(history_id(event),[]).append(event)
    expected={history_id(row):row for row in spec['assignments']}
    adapter=ac.LocalSeedClockAdapter(rate)
    params=a.anchor_params()
    audits=[]
    for assignment in assignments:
        key=history_id(assignment)
        base=next(state for (name,seed),state in bases.items() if seed==int(assignment['growth_seed']))
        state=base.clone()
        assert state.g.num_nodes()==int(expected[key]['initial_nodes'])
        assert state.token_count()==int(expected[key]['initial_tokens'])
        rng=random.Random(int(assignment['run_seed']))
        next_node,next_token=b.v08b.next_ids_from_state(state)
        manager=v7.PairManager(next_node_id=next_node,next_token_id=next_token)
        total_time=0.0
        for i in range(b.STEPS):
            rates=v7.family_rates(state,params) if assignment['arm']=='current_global' else adapter.family_rates(state,params)
            family,total_rate=b.choose_family(rates,rng)
            dt=rng.expovariate(total_rate)
            total_time+=dt
            state.t+=dt
            desc=tuple(v7.sample_from_dist(adapter.family_kernel(state,family,params),rng))
            source=reference[key][i]
            assert family==source['family'] and desc==ast.literal_eval(source['descriptor']), (key,i,'descriptor mismatch')
            assert abs(total_time-float(source['time']))<1e-12 and abs(dt-float(source['dt']))<1e-12, (key,i,'clock mismatch')
            context=adapter.apply_descriptor(state,family,desc,params,manager)
            assert context['event']==source['event_type']
            if (i+1)%512==0:
                beat(f'{key} replay {i+1}/{b.STEPS}')
        assert state.g.num_nodes()==int(expected[key]['final_nodes'])
        assert state.token_count()==int(expected[key]['final_tokens'])
        path=DOC/f'WP-H_{key}_edges.csv'
        write_csv(path,[dict(u=u,v=v) for u,v in sorted(state.g.edge_set())])
        audits.append(dict(history=key,steps=b.STEPS,all_descriptors_match=True,all_times_match=True,
            initial_nodes=base.g.num_nodes(),initial_tokens=base.token_count(),
            final_nodes=state.g.num_nodes(),final_tokens=state.token_count(),
            expected_final_nodes=expected[key]['final_nodes'],expected_final_tokens=expected[key]['final_tokens'],
            edges_sha256=sha(path),elapsed_seconds=time.monotonic()-start))
        write_csv(DOC/'WP-H_replay_audit.csv',audits)
        beat(f'{key} replay_verified')
    (DOC/'WP-H_replay_runtime.json').write_text(json.dumps(dict(seconds=time.monotonic()-start),indent=2)+'\n')
    beat('replay_complete 12/12 event_and_clock_exact')


def measure(graph,seed,label):
    import networkx as nx
    import numpy as np
    from scipy.sparse import diags
    nodes=sorted(graph)
    rng=random.Random(seed)
    roots=rng.sample(nodes,min(64,len(nodes)))
    n=len(nodes)
    index={v:i for i,v in enumerate(nodes)}
    volumes=[]
    for root in roots:
        distances=nx.single_source_shortest_path_length(graph,root,cutoff=10)
        volumes.append([sum(d<=r for d in distances.values()) for r in range(1,11)])
    mean_volume=np.mean(volumes,axis=0)
    vol36,_=fit(range(3,7),mean_volume[2:6])
    vol610,_=fit(range(6,11),mean_volume[5:10])
    adjacency=nx.to_scipy_sparse_array(graph,nodelist=nodes,dtype=float,format='csr')
    degrees=np.array([graph.degree(v) for v in nodes],dtype=float)
    # Column-stochastic propagation of probability mass.
    inverse=np.divide(1.,degrees,out=np.zeros_like(degrees),where=degrees>0)
    transition=adjacency@diags(inverse)
    if np.any(degrees==0):
        transition=transition+diags((degrees==0).astype(float))
    mass=np.zeros((n,len(roots)))
    root_index=np.array([index[v] for v in roots])
    mass[root_index,np.arange(len(roots))]=1
    returns=[]
    for t in range(1,65):
        mass=transition@mass
        assert np.max(np.abs(mass.sum(axis=0)-1))<1e-11
        returns.append(mass[root_index,np.arange(len(roots))].copy())
    returns=np.array(returns)
    times=list(range(4,65,2))
    ds_roots=[-2*fit(times,[returns[t-1,k] for t in times])[0] for k in range(len(roots))]
    aggregate_ds=-2*fit(times,[np.mean(returns[t-1]) for t in times])[0]
    finite_distances=Counter()
    finite_pairs=0
    for u,distances in nx.all_pairs_shortest_path_length(graph):
        for v,d in distances.items():
            if v>u:
                finite_distances[d]+=1
                finite_pairs+=1
    pair_count=n*(n-1)//2
    disconnected=pair_count-finite_pairs
    def median_hist(hist):
        total=sum(hist.values())
        if not total: return math.nan
        targets=((total-1)//2,total//2)
        values=[]
        for target in targets:
            count=0
            for value,n_at in sorted(hist.items()):
                count+=n_at
                if count>target:
                    values.append(value)
                    break
        return sum(values)/2
    all_hist=dict(finite_distances)
    if disconnected: all_hist[math.inf]=disconnected
    summary=dict(label=label,nodes=n,edges=graph.number_of_edges(),components=nx.number_connected_components(graph),
        d_vol_3_6=vol36,d_vol_6_10=vol610,ds_median=float(np.median(ds_roots)),ds_mean_curve=aggregate_ds,
        diameter=math.inf if disconnected else max(finite_distances,default=0),
        median_distance=median_hist(all_hist),finite_pair_median=median_hist(finite_distances),
        disconnected_pairs=disconnected,roots=len(roots))
    raw=[dict(label=label,root=root,r=r,B=volumes[k][r-1]) for k,root in enumerate(roots) for r in range(1,11)]
    walks=[dict(label=label,root=root,t=t,P=float(returns[t-1,k]),ds_root=ds_roots[k])
           for k,root in enumerate(roots) for t in range(1,65)]
    return summary,raw,walks


def positive_grid(n):
    import networkx as nx
    width=math.isqrt(n)
    graph=nx.Graph()
    graph.add_nodes_from(range(n))
    for v in range(n):
        if v%width and v-1>=0: graph.add_edge(v,v-1)
        if v>=width: graph.add_edge(v,v-width)
    return graph


def rewire_positive(grid, seed):
    rng = random.Random(seed)
    graph = grid.copy()
    original = {tuple(sorted(e)) for e in grid.edges()}
    available = sorted(original)
    target = math.floor(.1 * len(original) / 2)
    completed = 0
    for _ in range(1000 * len(original)):
        if completed == target:
            break
        first, second = rng.sample(available, 2)
        a, b = first
        c, d = second if rng.random() < .5 else tuple(reversed(second))
        proposed = {tuple(sorted((a,c))), tuple(sorted((b,d)))}
        if len({a,b,c,d}) < 4 or proposed & original or any(graph.has_edge(*e) for e in proposed):
            continue
        graph.remove_edges_from((first, second))
        graph.add_edges_from(proposed)
        available.remove(first)
        available.remove(second)
        completed += 1
    assert completed == target, 'positive rewiring budget exhausted'
    assert dict(graph.degree()) == dict(grid.degree())
    final = {tuple(sorted(e)) for e in graph.edges()}
    assert len(original - final) == 2 * target
    return graph, target


def analyze():
    import numpy as np
    import networkx as nx
    spec=load_spec()
    audits=read_csv(DOC/'WP-H_replay_audit.csv')
    assert len(audits)==12
    all_rows,gate_rows=[],[]
    start=time.monotonic()
    for hi,audit in enumerate(audits):
        key=audit['history']
        graph=nx.Graph()
        for edge in read_csv(DOC/f'WP-H_{key}_edges.csv'):
            graph.add_edge(int(edge['u']),int(edge['v']))
        original_degrees=dict(graph.degree())
        variants=[('universe',graph,0)]
        for k in range(8):
            null=graph.copy()
            nx.double_edge_swap(null,nswap=10*null.number_of_edges(),max_tries=1000*null.number_of_edges(),
                                seed=spec['seed']+1000*hi+k)
            assert dict(null.degree())==original_degrees
            variants.append(('null',null,k))
        ring=nx.cycle_graph(len(graph))
        grid=positive_grid(len(graph))
        rewired,nswap=rewire_positive(grid,spec['seed']+1000*hi+800)
        variants.extend([('ring',ring,0),('lat2',grid,0),('lat2_rewired',rewired,0)])
        rows,balls,walks=[],[],[]
        for vi,(kind,g,replica) in enumerate(variants):
            label=f'{key}_{kind}_{replica}'
            measured,raw,returns=measure(g,spec['seed']+1000*hi+900,label)
            measured.update(history=key,kind=kind,replica=replica,
                            degree_sequence_preserved=(dict(g.degree())==original_degrees) if kind=='null' else '')
            if kind=='lat2_rewired':
                initial={tuple(sorted(e)) for e in grid.edges()}
                final={tuple(sorted(e)) for e in g.edges()}
                measured.update(positive_successful_swaps=nswap,removed_original_fraction=len(initial-final)/len(initial),
                                edge_symmetric_difference_fraction=len(initial^final)/len(initial))
            rows.append(measured)
            balls.extend(raw)
            walks.extend(returns)
            write_csv(DOC/f'WP-H_{label}_graph.csv',[dict(u=u,v=v) for u,v in sorted(g.edges())])
            beat(f'{label} measured {vi+1}/12 elapsed_s={time.monotonic()-start:.3f}')
        write_csv(DOC/f'WP-H_{key}_observables.csv',rows)
        write_csv(DOC/f'WP-H_{key}_balls.csv',balls)
        write_csv(DOC/f'WP-H_{key}_returns.csv',walks)
        all_rows.extend(rows)
        universe=next(r['ds_median'] for r in rows if r['kind']=='universe')
        null_ds=[r['ds_median'] for r in rows if r['kind']=='null']
        low,high=map(float,np.quantile(null_ds,[.025,.975]))
        gate_rows.append(dict(history=key,ds_median=universe,null_ci_low=low,null_ci_high=high,
                              below=universe<low,above=universe>high))
        write_csv(DOC/'WP-H_observables.csv',all_rows)
        write_csv(DOC/'WP-H_gate_per_graph.csv',gate_rows)
        report(gate_rows,all_rows,time.monotonic()-start)
    beat('MEASUREMENTS_COMPLETE awaiting_verification_and_commit')


def report(gates,rows,seconds):
    below=sum(r['below'] for r in gates)
    above=sum(r['above'] for r in gates)
    complete=len(gates)==12
    passed=complete and max(below,above)>=10
    lines=['# WP-H rapport','',f'Status: {len(gates)}/12 grafer målt; ingen fysikkpåstand.','',
        '## Frosset metode og kjøretid','',f'`WP-H_frozen.json` SHA-256: `{sha(FROZEN)}`.',
        f'Analyse så langt: {seconds:.3f} s. Replaytid står i `WP-H_replay_runtime.json`.',
        '64 rotnoder, r=1…10, lokal volumhelning på 3…6 og 6…10. Ikke-lat vandring: '
        'returnsannsynligheten regnes eksakt ved matrisepropagasjon; d_s tilpasses ved partall t=4…64. '
        'Partallsvalget ble frosset før måling på grunn av null retur ved odde tider på bipartitte positive kontroller. '
        'Ingen korreksjon for endelig graf eller stasjonært gulv. Gate bruker median over de 64 roteksponentene.',
        'Nullene har nøyaktig samme merkede gradsekvens etter 10E vellykkede byttinger. '
        'Åtte nullreplikater gir grov 95%-intervalloppløsning; uniform miksing er ikke dokumentert. '
        'Positivt 2D-gitter er åpent og nær kvadratisk med eksakt N; den omkoblede kontrollen '
        'omkobler 10% av distinkte opprinnelige kanter, avrundet ned til partall, med faktisk drift i rådata.',
        '', '## Replayintegritet','',
        'Alle 2048 deskriptorer og klokkeinkrementer per historie må samsvare med original v16b-logg. '
        'Initialt og endelig node-/tokenantall er kontrollert mot v16b_run_summary.csv; '
        'se `WP-H_replay_audit.csv`. Ingen ny dynamikk utover den samme replayen.',
        '', '## Forhåndsregistrert gate','',
        '|graf|median d_s|null 95% lav|null 95% høy|under|over|','|---|---|---|---|---|---|']
    for r in gates:
        lines.append(f'|{r["history"]}|{r["ds_median"]:.5f}|{r["null_ci_low"]:.5f}|{r["null_ci_high"]:.5f}|{r["below"]}|{r["above"]}|')
    lines += ['',f'Terskel: minst 10 av 12 i samme retning. Under: {below}/12; over: {above}/12. '
        f'Utfall: {"bestått" if passed else "ikke skilt" if complete else "ikke ferdig"}.',
        '', '## Begrensning, neste beslutning og lesning G','']
    if not complete:
        lines += ['Lesning G er uavklart mens kjøringen pågår.']
    elif passed:
        lines += ['Grafene skilles fra disse gradbevarende nullene på det frosne tidsvinduet. '
            'Lesning G får støtte fra grafavlesningen, men en stabil dimensjon over større skalaer er ikke etablert.']
    else:
        lines += ['G4: Ikke skilt etter den uendrede terskelen. Null-separert dimensjon er ikke dokumentert '
            'i denne grafavlesningen. Dette beviser ikke at gradsekvensen alene forklarer alle egenskaper. '
            'Lesning G står ikke dokumentert fra WP-H ved disse skalaene.']
    lines += ['', '## Blokkert / gjenstående','',
        'Commit og uavhengig G1-verifikasjon gjenstår til de er særskilt bekreftet. '
        'Ingen push/publisering/RAG-sync i denne arbeidsordren. Fullstendige observabler, '
        'ballvolumer, returkurver og alle grafrealisereringer er lagret som WP-H CSV-er.', '']
    (DOC/'WP-H_report.md').write_text('\n'.join(lines))


def self_test():
    import networkx as nx
    summary,balls,walks=measure(nx.cycle_graph(128),1,'test_ring')
    assert summary['diameter']==64
    assert summary['median_distance']==32
    assert all(row['B']==2*row['r']+1 for row in balls)
    for row in walks:
        if row['t']%2:
            assert row['P']==0
        else:
            t=row['t']
            assert abs(row['P']-math.comb(t,t//2)/2**t)<1e-12
    for n in (1000,1024,1025,1026,1027):
        grid=positive_grid(n)
        assert len(grid)==n and nx.is_connected(grid)
        rewired,swaps=rewire_positive(grid,1)
        assert dict(rewired.degree())==dict(grid.degree())
        original={tuple(sorted(e)) for e in grid.edges()}
        final={tuple(sorted(e)) for e in rewired.edges()}
        assert len(original-final)==2*swaps==2*math.floor(.1*len(original)/2)
    beat('SELF_TEST_PASS exact_ring_ball_distance_binomial_returns_and_positive_sizes')


def main():
    p=argparse.ArgumentParser(__doc__)
    for operation in ('freeze','replay','analyze','self-test'):
        p.add_argument('--'+operation,action='store_true')
    args=p.parse_args()
    if args.freeze: freeze()
    elif args.replay: replay()
    elif args.analyze: analyze()
    elif args.self_test: self_test()
    else: p.error('choose an operation')


if __name__=='__main__':
    main()
