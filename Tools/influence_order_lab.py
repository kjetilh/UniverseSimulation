#!/usr/bin/env python3
"""WP-F2: frozen substrate calibration; no modification of v7/v16 modules.

Dynamics uses Python >=3.12 and the installed pure-Python NetworkX. Analysis
uses the installed Python 3.11/NumPy environment (no dependency installation).
Run --help for the deliberately separate preregistration, pilot and batch steps.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import dataclasses
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DOC = ROOT / 'Documentation/Program'
LOG = ROOT / '.program_logs'
ANALYSIS_PYTHON = '/opt/homebrew/bin/python3.11'
FROZEN = DOC / 'WP-F2_frozen.json'
SUBSTRATES = ('ring', 'lat2', 'lat3', 'rrg')


def heartbeat(message, package='WP-F2'):
    LOG.mkdir(exist_ok=True)
    line = f'{datetime.now(timezone.utc).isoformat()} {message}'
    with (LOG / f'{package}.heartbeat').open('a') as handle:
        handle.write(line + '\n')
    print(line, flush=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(path):
    with Path(path).open(newline='') as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f'empty evidence: {path}')
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def runtime():
    import relational_universe_local_max_coupling_lab as v7
    import relational_universe_v16a_disjoint_event_commutation_gate as v16a
    import relational_universe_v16b_intrinsic_event_dag_gate as v16b
    import relational_universe_v16ac_local_seed_adapter_gate as v16ac
    return v7, v16a, v16b, v16ac


def freeze(seed_policy):
    if FROZEN.exists():
        raise ValueError('refusing to overwrite preregistration')
    v7, a, b, ac = runtime()
    _, valid, rate = b.source_contract_rows()
    assert valid
    sources = [str(Path(m.__file__).relative_to(ROOT)) for m in (v7, a, b, ac)]
    sources += [
        'relational_universe_v15_defect_lifetime_lab.py',
        'relational_universe_v09_scale_and_natural_ensembles.py',
        'Documentation/v16b_run_summary.csv', 'Documentation/v16b_pre_registration.csv',
        'Documentation/v16ac_target_summary.csv',
        'Documentation/Program/WP-F2_influence_order_calibration.md',
        'Tools/influence_order_lab.py',
    ]
    summary = read_csv(ROOT / 'Documentation/v16b_run_summary.csv')
    seeds = [r for r in summary if r['arm'] == 'exposure_matched_local'
             and int(r['run_offset']) in (41011, 41047)]
    assignments = []
    for mode, substrate, row in itertools.product(('R', 'M'), SUBSTRATES, seeds):
        assignments.append(dict(mode=mode, substrate=substrate,
            seed=int(row['run_seed']), initial_tokens=int(row['initial_tokens']),
            growth_seed=int(row['growth_seed']), run_offset=int(row['run_offset'])))
    spec = dict(fingerprint='influence-order-geometry-calibration',
        prepared_at=datetime.now(timezone.utc).isoformat(),
        source_revision=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
        source_hashes={p: sha(ROOT / p) for p in sources},
        params=dataclasses.asdict(a.anchor_params()), v16b_frozen_spec=b.frozen_spec(rate),
        params_provenance='v16b.run -> v16a.anchor_params; frozen_spec does not contain Params',
        arm='exposure_matched_local', local_rate=rate, assignments=assignments,
        steps_requested=16384, runtime_ceiling_seconds=10800,
        runtime_policy='one complete lat3/R pilot at 16384; 32*pilot seconds; halve once to 8192 if >10800',
        pilot_assignment=next(r for r in assignments if r['substrate']=='lat3'),
        epsilon=0.25, M_seed_policy=seed_policy,
        M_move_weighting='multiply each move weight by 1+epsilon*mark[destination]; renormalize within each token, retaining 1/K token mass',
        M_structural_action='move token to descriptor u, increment mark[v], preserve all edges and nodes',
        legacy_order='unchanged v16a.action_access on the same sampled descriptors; descriptive projection, includes counterfactual structural writes in M',
        kernel_order='union legacy action reads with node/adj at v and neighbors, incident edges; M mark reads on closed 2-hop ball; actual M writes',
        metric_R='snapshot immediately before events 0,512,...; distance at later event snapshot; absent/disconnected node pairs reported as undefined',
        tau_grid='powers of 2 in physical Gillespie time, 1 <= tau <= total_time/4',
        eligible_events='event time >= total_time/2, for both V and R',
        alpha_fit='unweighted OLS log(median V) vs log(tau), median V >= 8, at least 2 points',
        gamma_fit='unweighted OLS log(pairwise R90) vs log(tau), all positive finite R, at least 2 points',
        percentile='linear interpolation at (n-1)*q',
        bootstrap='exact enumeration of all 4^4 history resamples, percentile 95% CI of median, no event bootstrap',
        gate=dict(order=list(SUBSTRATES), separation='strictly disjoint adjacent 95% alpha intervals',
                  gamma_max_range=0.10, missing_fit='not evaluable, never a pass'),
        drift='symmetric edge difference/frozen initial E; also removed initial edges/E, added edges/E, ever changed original edges/E',
        WP_F0_metrics='exact transitive reduction links/event, Theta=r*(n-1)/(h-1), r/r_floor, inclusive max interval/N',
        claim_limit='finite calibration only; a failed gate cannot prove failure at all N/T or for every rule')
    FROZEN.write_text(json.dumps(spec, indent=2, sort_keys=True)+'\n')
    heartbeat(f'preregistered sha256={sha(FROZEN)} steps=16384 histories=32 seed_policy={seed_policy}')
    (DOC/'WP-F2_report.md').write_text('# WP-F2 rapport\n\nStatus: forhåndsregistrert; ingen måletall ennå.\n\n'
        f'Frosset spesifikasjon: `WP-F2_frozen.json`, SHA-256 `{sha(FROZEN)}`.\n'
        'Kjøretidsanslaget skrives etter én komplett pilothistorie, før batchstart.\n')


def load_spec():
    spec = json.loads(FROZEN.read_text())
    for path, expected in spec['source_hashes'].items():
        if sha(ROOT/path) != expected:
            raise ValueError(f'frozen source changed: {path}')
    resolution = DOC / 'WP-F2_M_seed_resolution.json'
    if spec['M_seed_policy'] == 'pending' and resolution.exists():
        amendment = json.loads(resolution.read_text())
        assert amendment['frozen_sha256'] == sha(FROZEN)
        assert amendment['policy'] in ('mark', 'unchanged')
        spec['M_seed_policy'] = amendment['policy']
    return spec


def substrate_graph(name, seed):
    import networkx as nx
    if name == 'ring':
        return nx.cycle_graph(1024)
    if name == 'lat2':
        return nx.convert_node_labels_to_integers(nx.grid_graph((32,32), periodic=True))
    if name == 'lat3':
        return nx.convert_node_labels_to_integers(nx.grid_graph((10,10,10), periodic=True))
    return nx.random_regular_graph(3, 1024, seed=seed)


class MarkAdapter:
    """Explicit calibration adapter, using v7 descriptor support unchanged."""
    def __init__(self, base, epsilon, seed_policy):
        self.base, self.epsilon, self.seed_policy = base, epsilon, seed_policy
        self.marks = Counter()

    def family_rates(self, state, params):
        return self.base.family_rates(state, params)

    def family_kernel(self, state, family, params):
        kernel = self.base.family_kernel(state, family, params)
        if family != 'token':
            return kernel
        # Evaluate the declared mark ball even though only neighboring marks
        # enter move weights. The expanded order is an over-approximation.
        for v in state.token_pos.values():
            ball = {v} | state.g.neighbors(v)
            for u in state.g.neighbors(v):
                ball.update(state.g.neighbors(u))
            for u in ball:
                self.marks[u]
        original_mass, new_mass = Counter(), Counter()
        adjusted = {}
        for desc, probability in kernel.items():
            original_mass[desc[1]] += probability
            weight = 1+self.epsilon*self.marks[desc[3]] if desc[0]=='move' else 1.0
            adjusted[desc] = probability*weight
            new_mass[desc[1]] += adjusted[desc]
        return {d: p*original_mass[d[1]]/new_mass[d[1]] for d,p in adjusted.items()}

    def apply_descriptor(self, state, family, desc, params, manager):
        if family == 'token' and desc[0] in ('delete','triad','swap'):
            assert state.token_pos[desc[1]] == desc[2] and state.g.has_edge(desc[2],desc[3])
            state.token_pos[desc[1]] = desc[3]
            self.marks[desc[2]] += 1
            return {'event':desc[0]}
        if family == 'seed' and self.seed_policy == 'mark':
            host = state.token_pos[desc[1]] if desc[0]=='seed_tid' else desc[1]
            self.marks[host] += 1
            # Preserve allocator progression, but no new graph node is created.
            new_node = manager.next_node_id
            manager.next_node_id += 1
            return {'event':'seed','new_node':new_node}
        return self.base.apply_descriptor(state, family, desc, params, manager)


def event_location(state, concrete):
    desc = concrete.descriptor
    if concrete.family == 'token':
        return int(desc[1]), int(desc[2])
    if str(desc[0]).endswith('_tid'):
        return int(desc[1]), int(state.token_pos[desc[1]])
    return -1, int(desc[1])


def kernel_access(state, concrete, mode, seed_policy, legacy_reads, legacy_writes):
    reads, writes = set(legacy_reads), set(legacy_writes)
    token, v = event_location(state, concrete)
    if concrete.family == 'token':
        neighbors = set(state.g.neighbors(v))
        for u in {v} | neighbors:
            reads.update((f'node:{u}',f'adj:{u}'))
        for u in neighbors:
            reads.add(f'edge:{min(v,u)}:{max(v,u)}')
        if mode == 'M':
            ball = {v} | neighbors
            for u in neighbors:
                ball.update(state.g.neighbors(u))
            reads.update(f'mark:{u}' for u in ball)
            if concrete.kind in ('delete','triad','swap'):
                writes = {f'mark:{v}', f'token:{token}'}
    if mode == 'M' and concrete.kind=='seed' and seed_policy=='mark':
        writes = {f'mark:{v}'}
    return reads, writes


def file_prefix(assignment, pilot=False):
    return f"WP-F2_{'pilot_' if pilot else ''}{assignment['mode']}_{assignment['substrate']}_{assignment['seed']}"


def run_history(spec, assignment, steps, pilot=False):
    v7, a, b, ac = runtime()
    start = time.monotonic()
    name = file_prefix(assignment, pilot)
    if (DOC/f'{name}_summary.csv').exists():
        raise ValueError(f'refusing duplicate run: {name}')
    mode = assignment['mode']
    if mode == 'M' and spec['M_seed_policy'] == 'pending':
        raise ValueError('M seed semantics require user resolution before execution')
    graph = substrate_graph(assignment['substrate'], assignment['seed']+901)
    state = a.nx_to_state(graph, random.Random(assignment['seed']+902).choices(sorted(graph), k=assignment['initial_tokens']))
    initial_edges = state.g.edge_set()
    params = v7.Params(**spec['params'])
    base = ac.LocalSeedClockAdapter(spec['local_rate'])
    adapter = MarkAdapter(base,spec['epsilon'],spec['M_seed_policy']) if mode=='M' else base
    manager = v7.PairManager(next_node_id=max(state.g.nodes())+1, next_token_id=state.token_count())
    dags = {'legacy':b.DependencyDAG(), 'kernel':b.DependencyDAG()}
    rng = random.Random(assignment['seed'])
    events, snapshots = [], []
    touched_initial = set()
    snapshot = 0
    heartbeat(f'{name} start steps={steps}')
    for step in range(steps):
        if step % 512 == 0 and (mode=='R' or step==0 or spec['M_seed_policy']=='unchanged'):
            snapshot = step
            snapshots.extend(dict(snapshot=step,u=u,v=v) for u,v in sorted(state.g.edge_set()))
        family, total_rate = b.choose_family(adapter.family_rates(state,params),rng)
        assert total_rate > 0
        dt = rng.expovariate(total_rate)
        state.t += dt
        desc = tuple(v7.sample_from_dist(adapter.family_kernel(state,family,params),rng))
        concrete = b.materialize_event(family,desc,manager)
        token, node = event_location(state,concrete)
        legacy_reads,legacy_writes = a.action_access(state,concrete)
        reads,writes = kernel_access(state,concrete,mode,spec['M_seed_policy'],legacy_reads,legacy_writes)
        dags['legacy'].add(legacy_reads,legacy_writes)
        dags['kernel'].add(reads,writes)
        before = state.g.edge_set() if concrete.kind in ('swap','delete','triad','seed') else None
        context = adapter.apply_descriptor(state,family,desc,params,manager)
        assert context['event']==concrete.kind
        if before is not None:
            touched_initial.update((before ^ state.g.edge_set()) & initial_edges)
        events.append(dict(event_id=step,time=state.t,dt=dt,token=token,node=node,family=family,
            descriptor=json.dumps(desc),event_type=concrete.kind,snapshot=snapshot,
            reads=';'.join(sorted(reads)),writes=';'.join(sorted(writes)),
            legacy_reads=';'.join(sorted(legacy_reads)),legacy_writes=';'.join(sorted(legacy_writes)),
            parents=';'.join(map(str,sorted(dags['kernel'].predecessors[-1]))),
            legacy_parents=';'.join(map(str,sorted(dags['legacy'].predecessors[-1])))))
        if (step+1)%512 == 0:
            heartbeat(f'{name} dynamics {step+1}/{steps} elapsed_s={time.monotonic()-start:.3f} tokens={state.token_count()}')
    final_edges = state.g.edge_set()
    if mode=='M' and spec['M_seed_policy']=='mark':
        assert initial_edges == final_edges and state.g.num_nodes()==len(graph)
    write_csv(DOC/f'{name}_events.csv',events)
    write_csv(DOC/f'{name}_snapshots.csv',snapshots)
    counts = Counter(row['event_type'] for row in events)
    metadata = dict(**assignment,steps=steps,total_time=state.t,
        initial_nodes=len(graph), final_nodes=state.g.num_nodes(), final_tokens=state.token_count(),
        initial_edges=len(initial_edges),final_edges=len(final_edges),
        edge_drift=len(initial_edges^final_edges)/len(initial_edges),
        removed_initial_fraction=len(initial_edges-final_edges)/len(initial_edges),
        added_edge_fraction=len(final_edges-initial_edges)/len(initial_edges),
        ever_changed_initial_fraction=len(touched_initial)/len(initial_edges),
        dynamics_seconds=time.monotonic()-start, frozen_sha256=sha(FROZEN),
        **{f'{kind}_events':counts[kind] for kind in b.EVENT_TYPES})
    (DOC/f'{name}_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    heartbeat(f'{name} analysis_start')
    subprocess.run([ANALYSIS_PYTHON,str(Path(__file__)), '--analyze',name], check=True,
                   env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'})
    elapsed = time.monotonic()-start
    heartbeat(f'{name} complete elapsed_s={elapsed:.3f}')
    return elapsed


def poset_metrics(parents):
    n = len(parents)
    ancestors, depths = [], []
    descendants = [0]*n
    for v, ps in enumerate(parents):
        bits, depth = 0, 0
        for p in ps:
            assert 0 <= p < v
            bits |= ancestors[p] | (1<<p)
            depth = max(depth,depths[p]+1)
        ancestors.append(bits)
        depths.append(depth)
    has_children = set()
    for v in range(n-1,-1,-1):
        for p in parents[v]:
            descendants[p] |= descendants[v] | (1<<v)
            has_children.add(p)
    links = 0
    for ps in parents:
        shadow = 0
        for p in ps:
            shadow |= ancestors[p]
        links += sum(not (shadow>>p)&1 for p in ps)
    # Inclusive intervals are monotone under extending either endpoint.
    # Therefore the exact maximum is attained between a root and a sink.
    roots = [v for v,ps in enumerate(parents) if not ps]
    sinks = [v for v in range(n) if v not in has_children]
    max_interval = 1 if n else 0
    for p in roots:
        for q in sinks:
            if (ancestors[q]>>p)&1:
                max_interval = max(max_interval,(descendants[p]&ancestors[q]).bit_count()+2)
    comparable = sum(x.bit_count() for x in ancestors)
    h = max(depths)+1
    return ancestors, dict(links_per_event=links/n, theta=2*comparable/(n*(h-1)) if h>1 else math.nan,
        r_over_floor=comparable/sum(depths) if sum(depths) else math.nan,
        max_interval_frac=max_interval/n, comparable_pairs=comparable, height=h,
        raw_edges_per_event=sum(map(len,parents))/n)


def fit(xs,ys,minimum=0):
    points = [(math.log(x),math.log(y)) for x,y in zip(xs,ys) if math.isfinite(y) and y>0 and y>=minimum]
    if len(points)<2:
        return math.nan,len(points)
    x,y = zip(*points)
    mx,my = sum(x)/len(x),sum(y)/len(y)
    return sum((a-mx)*(b-my) for a,b in points)/sum((a-mx)**2 for a in x),len(points)


def analyze(name):
    import numpy as np
    import networkx as nx
    start=time.monotonic()
    events=read_csv(DOC/f'{name}_events.csv')
    metadata=json.loads((DOC/f'{name}_metadata.json').read_text())
    n=len(events)
    times=np.array([float(e['time']) for e in events])
    nodes=np.array([int(e['node']) for e in events])
    tokens=np.array([int(e['token']) for e in events])
    snapshots={}
    for row in read_csv(DOC/f'{name}_snapshots.csv'):
        snapshots.setdefault(int(row['snapshot']),nx.Graph()).add_edge(int(row['u']),int(row['v']))
    tau=[]
    value=1
    while value<=times[-1]/4:
        tau.append(value)
        value*=2
    eligible=np.flatnonzero(times>=times[-1]/2)
    distance_cache={}
    rows,curves=[],[]
    for order,field in (('kernel','parents'),('legacy','legacy_parents')):
        parents=[[int(p) for p in e[field].split(';') if p] for e in events]
        ancestors,metrics=poset_metrics(parents)
        volume=[[] for _ in tau]
        histograms=[Counter() for _ in tau]
        undefined=[0 for _ in tau]
        pair_counts=[0 for _ in tau]
        current_snapshot=None
        for ei,e in enumerate(eligible):
            snapshot=int(events[e]['snapshot'])
            if current_snapshot != snapshot:
                distance_cache.clear()
                current_snapshot=snapshot
            node=int(nodes[e])
            key=(snapshot,node)
            if key not in distance_cache:
                g=snapshots[snapshot]
                distance_cache[key]=dict(nx.single_source_shortest_path_length(g,node)) if node in g else {}
            distances=distance_cache[key]
            indices=np.flatnonzero(np.unpackbits(np.frombuffer(ancestors[e].to_bytes((n+7)//8,'little'),dtype=np.uint8),bitorder='little')[:n])
            if len(indices):
                lag=times[e]-times[indices]
                dist=np.array([distances.get(int(v),-1) for v in nodes[indices]],dtype=np.int32)
            for ti,t in enumerate(tau):
                if len(indices):
                    selected=dist[lag<=t]
                else:
                    selected=np.empty(0,dtype=np.int32)
                volume[ti].append(len(selected))
                pair_counts[ti]+=len(selected)
                undefined[ti]+=int(np.sum(selected<0))
                vals,counts=np.unique(selected[selected>=0],return_counts=True)
                histograms[ti].update({int(v):int(c) for v,c in zip(vals,counts)})
            if ei%2048==0:
                heartbeat(f'{name} {order} observables {ei}/{len(eligible)}')
        medians=[float(np.median(v)) if v else math.nan for v in volume]
        radii=[]
        for hist in histograms:
            count=sum(hist.values())
            if not count:
                radii.append(math.nan)
                continue
            pos=(count-1)*0.9
            targets=(math.floor(pos),math.ceil(pos))
            selected=[]
            for target in targets:
                cumulative=0
                for distance,count_at in sorted(hist.items()):
                    cumulative+=count_at
                    if cumulative>target:
                        selected.append(distance)
                        break
            radii.append(selected[0]+(pos-targets[0])*(selected[1]-selected[0]))
        alpha,na=fit(tau,medians,8)
        gamma,ng=fit(tau,radii)
        edges=sum(map(len,parents))
        cross=sum(tokens[p]!=tokens[e] for e,ps in enumerate(parents) for p in ps)
        rows.append(dict(**metadata,order=order,**metrics,alpha=alpha,alpha_fit_points=na,
            gamma=gamma,gamma_fit_points=ng,cross_token_fraction=cross/edges if edges else math.nan,
            cross_token_edges=cross,dag_edges=edges,eligible_events=len(eligible),
            analysis_seconds=time.monotonic()-start))
        curves.extend(dict(order=order,tau=t,V_median=v,R90=r,pair_count=c,undefined_distance_pairs=u,
                           finite_distance_pairs=c-u) for t,v,r,c,u in zip(tau,medians,radii,pair_counts,undefined))
    write_csv(DOC/f'{name}_summary.csv',rows)
    write_csv(DOC/f'{name}_curves.csv',curves)


def bootstrap(values):
    import statistics
    if not all(math.isfinite(v) for v in values):
        return (math.nan,math.nan,math.nan)
    distribution=sorted(statistics.median(sample) for sample in itertools.product(values,repeat=len(values)))
    def quantile(q):
        pos=(len(distribution)-1)*q
        low=math.floor(pos)
        high=math.ceil(pos)
        return distribution[low]+(pos-low)*(distribution[high]-distribution[low])
    return statistics.median(values),quantile(.025),quantile(.975)


def aggregate(spec):
    rows=[]
    for assignment in spec['assignments']:
        path=DOC/f'{file_prefix(assignment)}_summary.csv'
        if path.exists():
            rows.extend(read_csv(path))
    if rows:
        write_csv(DOC/'WP-F2_per_history.csv',rows)
    aggregates=[]
    for mode,order,substrate in itertools.product(('M','R'),('kernel','legacy'),SUBSTRATES):
        group=[r for r in rows if (r['mode'],r['order'],r['substrate'])==(mode,order,substrate)]
        if not group:
            continue
        row=dict(mode=mode,order=order,substrate=substrate,histories=len(group))
        for metric in ('alpha','gamma','cross_token_fraction','links_per_event','theta','r_over_floor','max_interval_frac','edge_drift'):
            center,low,high=bootstrap([float(r[metric]) for r in group])
            row.update({metric:center,f'{metric}_ci_low':low,f'{metric}_ci_high':high})
        aggregates.append(row)
    if aggregates:
        write_csv(DOC/'WP-F2_aggregate.csv',aggregates)
    gates=[]
    for mode,order in itertools.product(('M','R'),('kernel','legacy')):
        group=[next((r for r in aggregates if (r['mode'],r['order'],r['substrate'])==(mode,order,s)),None) for s in SUBSTRATES]
        complete=all(r and r['histories']==4 for r in group)
        valid=complete and all(math.isfinite(r['alpha']) and math.isfinite(r['gamma']) for r in group)
        ordering=valid and all(a['alpha']<b['alpha'] for a,b in zip(group,group[1:]))
        separation=valid and all(a['alpha_ci_high']<b['alpha_ci_low'] for a,b in zip(group,group[1:]))
        mechanism=valid and max(r['gamma'] for r in group[:3])-min(r['gamma'] for r in group[:3])<=.10
        gates.append(dict(mode=mode,order=order,complete=bool(complete),evaluable=bool(valid),
            ordering=bool(ordering),separation=bool(separation),mechanism=bool(mechanism),
            passed=bool(ordering and separation and mechanism)))
    write_csv(DOC/'WP-F2_gates.csv',gates)
    status='målinger fullført' if len(rows)==64 else f'under kjøring ({len(rows)//2}/32 historier)'
    lines=['# WP-F2 rapport','',f'Status: {status}. Codex måler; G1-verifikasjon hos spesifikasjonsforfatter gjenstår.','',
        '## Frosne parametre og metode','',f'`WP-F2_frozen.json` SHA-256: `{sha(FROZEN)}`.',
        'Params er hentet fra `v16b.run → v16a.anchor_params`, fordi `frozen_spec` ikke inneholder Params. '
        'Alle terskler, seed og operasjonelle estimatorvalg ble frosset før piloten.',
        f'Modus M seed-policy: `{spec["M_seed_policy"]}`. Legacy er uendret v16a-projeksjon av de samme deskriptorene; '
        'i M inkluderer den deklarerte grafskrivinger som mark-adapteren ikke utfører. '
        'Kernel-ordenen bruker adapterens faktiske skrivesett. DAG.add er uendret.',
        'Tau måles i Gillespie-tid, ikke hendelsesnummer. R bruker alle forfarpar til samme sene hendelsesutvalg som V. '
        'R-avstander hentes fra siste 512-stegs øyeblikksgraf; manglende noder/frakoblede par telles separat. '
        'Bootstrap er eksakt over de 256 trekkene av fire historier, ikke over hendelser.',
        'Markvekter normaliseres innen hvert token, slik at tokenklokkene ikke endres. '
        'RRG er en tilfeldig regulær kontroll; ingen enkelt realisasjon sertifiseres som uendeligdimensjonal.',
        '', '## Kjøretid','']
    estimate=DOC/'WP-F2_runtime_estimate.json'
    if estimate.exists():
        lines += ['```json',estimate.read_text().strip(),'```']
    lines += ['', '## Målte tall','', '|modus|orden|underlag|n|α [95% KI]|γ [95% KI]|tverrbinding|kantdrift|',
        '|---|---|---|---|---|---|---|---|']
    for r in aggregates:
        lines.append(f'|{r["mode"]}|{r["order"]}|{r["substrate"]}|{r["histories"]}|'
            f'{r["alpha"]:.4f} [{r["alpha_ci_low"]:.4f}, {r["alpha_ci_high"]:.4f}]|'
            f'{r["gamma"]:.4f} [{r["gamma_ci_low"]:.4f}, {r["gamma_ci_high"]:.4f}]|'
            f'{r["cross_token_fraction"]:.4f}|{r["edge_drift"]:.4f}|')
    lines += ['', 'De fire WP-F0-tallene med KI er bevart i `WP-F2_aggregate.csv`; per-historie-tall '
        'står i `WP-F2_per_history.csv`. Hendelseslogger og øyeblikksgrafer er separate CSV-er per historie.',
        '', '## Uendrede terskler','', '|modus|orden|evaluerbar|rekkefølge|separasjon|mekanisme|F2|',
        '|---|---|---|---|---|---|---|']
    for r in gates:
        lines.append('|'+ '|'.join(str(r[k]) for k in ('mode','order','evaluable','ordering','separation','mechanism','passed'))+'|')
    lines += ['', '## Utfall, begrensninger og neste beslutning','']
    m=next(r for r in gates if r['mode']=='M' and r['order']=='kernel')
    r=next(r for r in gates if r['mode']=='R' and r['order']=='kernel')
    if len(rows)<64:
        lines += ['G4 og lesning G er ennå ikke avgjort. Ingen WP-F3 er kjørt.']
    elif not m['evaluable']:
        lines += ['F2-M kan ikke evalueres med det frosne vinduet: minst én eksponent mangler tilstrekkelige punkter. '
                  'Dette er en målebegrensning, ikke dokumentasjon på at geometri mangler. Lesning G er uavklart.']
    elif not m['passed']:
        lines += ['G4: M består ikke. Ordenen dokumenterer ikke dimensjon under denne frosne kalibreringen. '
                  'Den positive F2-påstanden om lesning G faller ved dette N/T; det følger ikke at alle '
                  'størrelser eller hele regelfamilien mangler geometri. WP-H er den separate grafavlesningen.']
    elif r['passed']:
        lines += ['G4: M og R består; uttrekket er geometribevarende etter disse finite tersklene. '
                  'Lesning G står for kalibreringen; WP-F3 kan spesifiseres, men er ikke kjørt.']
    else:
        lines += ['G4: M består, R består ikke. Kalibreringsadapteren virker, mens reell regel ikke er kvalifisert '
                  'ved dette N/T. En høyere redigeringsrate eller lengre historie kan ikke godkjennes fra '
                  'tverrbindingsandel alene; dette krever en ny forhåndsregistrering. Lesning G er bare betinget støttet.']
    lines += ['', '## Blokkert / gjenstående','',
        'Commit og uavhengig G1-kontroll er ikke bekreftet i denne automatisk genererte rapporten. '
        'Ingen push, publisering eller RAG-sync inngår, i henhold til denne arbeidsordren. '
        'Ingen fysikkpåstander. Fire historier gir grov usikkerhetsoppløsning. '
        'Avvik fra WP-F0 ved 8× kjørelengde er observasjoner, ikke automatisk kodefeil.', '']
    (DOC/'WP-F2_report.md').write_text('\n'.join(lines))


def pilot():
    spec=load_spec()
    elapsed=run_history(spec,spec['pilot_assignment'],16384,True)
    projected=32*elapsed
    steps=8192 if projected>10800 else 16384
    estimate=dict(pilot_seconds=elapsed, projected_32_histories_seconds=projected,
        projected_hours=projected/3600, selected_steps=steps,
        estimated_selected_seconds=projected*(steps/16384),
        caveat='single lat3/R history; mode, token growth, analysis and machine load may change runtime')
    (DOC/'WP-F2_runtime_estimate.json').write_text(json.dumps(estimate,indent=2)+'\n')
    heartbeat(f'RUNTIME_ESTIMATE before_all_histories pilot_seconds={elapsed:.3f} '
              f'projected_total_hours={projected/3600:.3f} selected_steps={steps} '
              f'estimated_selected_hours={estimate["estimated_selected_seconds"]/3600:.3f}')
    aggregate(spec)


def batch():
    spec=load_spec()
    estimate=json.loads((DOC/'WP-F2_runtime_estimate.json').read_text())
    assert 'RUNTIME_ESTIMATE before_all_histories' in (LOG/'WP-F2.heartbeat').read_text()
    steps=estimate['selected_steps']
    heartbeat(f'BATCH_START histories=32 steps={steps}')
    for assignment in spec['assignments']:
        name=file_prefix(assignment)
        if (DOC/f'{name}_summary.csv').exists():
            heartbeat(f'{name} verified_completed_resume')
            continue
        run_history(spec,assignment,steps)
        aggregate(spec)
    heartbeat('MEASUREMENTS_COMPLETE histories=32 awaiting_verification_and_commit')


def self_test():
    # Independent exhaustive tiny-poset check, including singleton intervals.
    for n in range(1,6):
        possible=[(p,c) for c in range(n) for p in range(c)]
        for mask in range(1<<len(possible)):
            parents=[[] for _ in range(n)]
            for k,(p,c) in enumerate(possible):
                if mask>>k&1:
                    parents[c].append(p)
            anc,metrics=poset_metrics(parents)
            expected=1
            for p in range(n):
                for c in range(p+1,n):
                    if anc[c]>>p&1:
                        expected=max(expected,2+sum(bool(anc[c]>>v&1 and anc[v]>>p&1) for v in range(p+1,c)))
            assert abs(metrics['max_interval_frac']-expected/n)<1e-12
    slope, count = fit([1,2,4],[8,16,32],8)
    assert abs(slope-1.0)<1e-12 and count==3
    assert bootstrap([1.,1.,1.,1.])==(1.,1.,1.)
    heartbeat('SELF_TEST_PASS exhaustive_posets_n_le_5 interval_identity_and_estimators')


def main():
    parser=argparse.ArgumentParser(__doc__)
    parser.add_argument('--freeze',choices=('mark','unchanged','pending'))
    parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--batch',action='store_true')
    parser.add_argument('--analyze')
    parser.add_argument('--aggregate',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    if args.freeze: freeze(args.freeze)
    elif args.pilot: pilot()
    elif args.batch: batch()
    elif args.analyze: analyze(args.analyze)
    elif args.aggregate: aggregate(load_spec())
    elif args.self_test: self_test()
    else: parser.error('choose one operation')


if __name__=='__main__':
    main()
