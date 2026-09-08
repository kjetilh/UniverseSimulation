#!/usr/bin/env python3
"""WP-F2 amendment 1. Original frozen lab and attempt-1 evidence stay unchanged."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import itertools
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import influence_order_lab as lab
DOC = lab.DOC
AMENDMENT = DOC/'WP-F2_amendment_1.md'
FROZEN2 = DOC/'WP-F2_attempt2_frozen.json'
ORIGINAL_ACCESS = lab.kernel_access


def amended_kernel_access(state, concrete, mode, seed_policy, legacy_reads, legacy_writes):
    if mode == 'M' and concrete.kind == 'seed' and seed_policy == 'mark':
        token, host = lab.event_location(state, concrete)
        reads = {f'node:{host}'}
        if concrete.descriptor[0] == 'seed_tid':
            reads.add(f'token:{token}')
        return reads, {f'mark:{host}'}
    return ORIGINAL_ACCESS(state, concrete, mode, seed_policy, legacy_reads, legacy_writes)


def tau_grid(total_time):
    # Integer powers avoid cumulative multiplication error at the upper bound.
    return [0.25 * 2**(k/4) for k in range(1+math.floor(4*math.log2((total_time/2)/.25)))] if total_time >= .5 else []


def fit_window(tau, volumes, observable, total_time):
    selected = [(t,y) for t,v,y in zip(tau,volumes,observable)
                if v >= 8 and t <= total_time/4 and math.isfinite(y) and y > 0]
    if len(selected) < 6:
        return math.nan, len(selected)
    return lab.fit(*zip(*selected))


def prepare():
    if FROZEN2.exists():
        raise ValueError('refusing to overwrite attempt-2 preregistration')
    spec = lab.load_spec()
    now = datetime.now(timezone.utc).isoformat()
    resolution = dict(policy='mark', frozen_sha256=lab.sha(lab.FROZEN),
        authority='WP-F2 amendment 1, spec author Claude; user requested execution',
        timestamp=now, amendment_sha256=lab.sha(AMENDMENT),
        wording='i modus M utføres `seed` som `mark:host` — ingen node, ingen kant. Lese-/skrivesett: leser `token:t` (ved `seed_tid`) og `node:host`, skriver `mark:host`.')
    resolution_path = DOC/'WP-F2_M_seed_resolution.json'
    assert not resolution_path.exists()
    resolution_path.write_text(json.dumps(resolution,ensure_ascii=False,indent=2)+'\n')
    preserved = {}
    for a in spec['assignments']:
        if a['mode'] != 'R': continue
        for suffix in ('events.csv','snapshots.csv','metadata.json','summary.csv','curves.csv'):
            p = DOC/f'{lab.file_prefix(a)}_{suffix}'
            preserved[str(p.relative_to(ROOT))] = lab.sha(p)
    # Historical report remains available in full, not rewritten as if it used the new estimator.
    for suffix in ('report.md','aggregate.csv','per_history.csv','gates.csv','verification.csv','threshold_audit.csv','unavailable_fits.csv'):
        src = DOC/f'WP-F2_{suffix}'
        dst = DOC/f'WP-F2_attempt1_{suffix}'
        assert not dst.exists()
        dst.write_bytes(src.read_bytes())
        preserved[str(dst.relative_to(ROOT))] = lab.sha(dst)
    frozen = dict(attempt=2,fingerprint=spec['fingerprint'],timestamp=now,
        original_frozen_sha256=lab.sha(lab.FROZEN),amendment_sha256=lab.sha(AMENDMENT),
        code_sha256=lab.sha(__file__),seed_resolution_sha256=lab.sha(resolution_path),
        tau_grid='0.25 * 2**(k/4), integer k >= 0, through T/2',
        fitting='both alpha and mean-distance gamma use median V>=8 AND tau<=T/4; >=6 finite positive points',
        R90='reported; diagnostic slope on the identical fit window, never used for gates',
        bootstrap=spec['bootstrap'],gate=spec['gate'],steps=8192,
        preserved_hashes=preserved,
        execution_order=['R reanalysis from saved parents/snapshots','M dynamics and same analysis','gates','WP-H'],
        reference_limit='known substrates are measured calibration references; failure to separate them does not qualify a geometry hypothesis gate')
    FROZEN2.write_text(json.dumps(frozen,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
    lab.heartbeat(f'ATTEMPT2_PREREGISTERED sha256={lab.sha(FROZEN2)} R_logs_preserved=16 steps_M=8192')
    rows = lab.read_csv(DOC/'attempt_ledger.csv')
    for row in rows:
        if row['fingerprint'] == spec['fingerprint']:
            row.update(attempts=2,last_outcome='attempt2_preregistered',escalated='no',
                note='WP-F2 amendment 1; same fingerprint G2. Attempt 1 unmeasurable grid, R16 retained; seed=mark authorized by amendment. Original evidence preserved in WP-F2_attempt1_*.')
    lab.write_csv(DOC/'attempt_ledger.csv',rows)
    report([])


def load_spec():
    spec = lab.load_spec()
    frozen = json.loads(FROZEN2.read_text())
    assert frozen['code_sha256'] == lab.sha(__file__)
    assert frozen['original_frozen_sha256'] == lab.sha(lab.FROZEN)
    assert frozen['amendment_sha256'] == lab.sha(AMENDMENT)
    assert frozen['seed_resolution_sha256'] == lab.sha(DOC/'WP-F2_M_seed_resolution.json')
    for p,digest in frozen['preserved_hashes'].items():
        assert lab.sha(ROOT/p) == digest, p
    assert spec['M_seed_policy']=='mark'
    return spec


def analyze(name):
    import numpy as np
    import networkx as nx
    start=time.monotonic()
    events=lab.read_csv(DOC/f'{name}_events.csv')
    metadata=json.loads((DOC/f'{name}_metadata.json').read_text())
    n=len(events)
    times=np.array([float(e['time']) for e in events])
    nodes=np.array([int(e['node']) for e in events])
    tokens=np.array([int(e['token']) for e in events])
    snapshots={}
    for row in lab.read_csv(DOC/f'{name}_snapshots.csv'):
        snapshots.setdefault(int(row['snapshot']),nx.Graph()).add_edge(int(row['u']),int(row['v']))
    tau=tau_grid(times[-1])
    eligible=np.flatnonzero(times>=times[-1]/2)
    rows,curves=[],[]
    for order,field in (('kernel','parents'),('legacy','legacy_parents')):
        parents=[[int(p) for p in e[field].split(';') if p] for e in events]
        ancestors,metrics=lab.poset_metrics(parents)
        volume=np.zeros((len(eligible),len(tau)),dtype=np.int32)
        histograms=[Counter() for _ in tau]
        undefined=np.zeros(len(tau),dtype=np.int64)
        current_snapshot=None
        distance_cache={}
        for ei,e in enumerate(eligible):
            snapshot=int(events[e]['snapshot'])
            if current_snapshot != snapshot:
                distance_cache.clear()
                current_snapshot=snapshot
            node=int(nodes[e])
            if node not in distance_cache:
                g=snapshots[snapshot]
                distance_cache[node]=dict(nx.single_source_shortest_path_length(g,node)) if node in g else {}
            distances=distance_cache[node]
            indices=np.flatnonzero(np.unpackbits(np.frombuffer(ancestors[e].to_bytes((n+7)//8,'little'),dtype=np.uint8),bitorder='little')[:n])
            if not len(indices): continue
            lag=times[e]-times[indices]
            dist=np.array([distances.get(int(v),-1) for v in nodes[indices]],dtype=np.int32)
            # Each ancestor enters at the first tau >= lag. Accumulate exact integer
            # distance histograms once, then prefix-sum across tau after all events.
            bins=np.searchsorted(tau,lag,side='left')
            valid=bins<len(tau)
            volume[ei]=np.cumsum(np.bincount(bins[valid],minlength=len(tau)))
            missing=valid & (dist<0)
            undefined += np.bincount(bins[missing],minlength=len(tau))
            good=valid & (dist>=0)
            pairs,counts=np.unique(np.column_stack((bins[good],dist[good])),axis=0,return_counts=True)
            for (ti,d),count in zip(pairs,counts):
                histograms[int(ti)][int(d)]+=int(count)
            if ei%2048==0:
                lab.heartbeat(f'{name} attempt2 {order} pairs {ei}/{len(eligible)}')
        medians=np.median(volume,axis=0)
        pair_counts=volume.sum(axis=0)
        undefined=np.cumsum(undefined)
        radii,means,sums=[],[],[]
        cumulative=Counter()
        for hist in histograms:
            cumulative.update(hist)
            count=sum(cumulative.values())
            distance_sum=sum(d*c for d,c in cumulative.items())
            sums.append(distance_sum)
            means.append(distance_sum/count if count else math.nan)
            if not count:
                radii.append(math.nan)
                continue
            pos=(count-1)*.9
            selected=[]
            for target in (math.floor(pos),math.ceil(pos)):
                c=0
                for distance,at in sorted(cumulative.items()):
                    c+=at
                    if c>target:
                        selected.append(distance)
                        break
            radii.append(selected[0]+(pos-math.floor(pos))*(selected[1]-selected[0]))
        alpha,na=fit_window(tau,medians,medians,times[-1])
        gamma,ng=fit_window(tau,medians,means,times[-1])
        gamma90,ng90=fit_window(tau,medians,radii,times[-1])
        edges=sum(map(len,parents))
        cross=sum(tokens[p]!=tokens[e] for e,ps in enumerate(parents) for p in ps)
        rows.append(dict(**metadata,attempt=2,attempt2_frozen_sha256=lab.sha(FROZEN2),order=order,**metrics,
            alpha=alpha,alpha_fit_points=na,gamma=gamma,gamma_fit_points=ng,
            gamma_R90=gamma90,gamma_R90_fit_points=ng90,
            cross_token_fraction=cross/edges if edges else math.nan,cross_token_edges=cross,dag_edges=edges,
            eligible_events=len(eligible),analysis_seconds=time.monotonic()-start))
        curves.extend(dict(order=order,tau=t,V_median=v,R90=r,R_mean=m,distance_sum=s,
            pair_count=int(c),undefined_distance_pairs=int(u),finite_distance_pairs=int(c-u),
            fit_window=bool(v>=8 and t<=times[-1]/4))
            for t,v,r,m,s,c,u in zip(tau,medians,radii,means,sums,pair_counts,undefined))
    lab.write_csv(DOC/f'{name}_attempt2_summary.csv',rows)
    lab.write_csv(DOC/f'{name}_attempt2_curves.csv',curves)
    lab.heartbeat(f'{name} ATTEMPT2_ANALYZED seconds={time.monotonic()-start:.3f}')


def aggregate(spec, evaluate=False):
    rows=[]
    for a in spec['assignments']:
        p=DOC/f'{lab.file_prefix(a)}_attempt2_summary.csv'
        if p.exists(): rows.extend(lab.read_csv(p))
    if rows: lab.write_csv(DOC/'WP-F2_attempt2_per_history.csv',rows)
    aggregates=[]
    for mode,order,substrate in itertools.product(('R','M'),('kernel','legacy'),lab.SUBSTRATES):
        group=[r for r in rows if (r['mode'],r['order'],r['substrate'])==(mode,order,substrate)]
        if not group: continue
        row=dict(mode=mode,order=order,substrate=substrate,histories=len(group))
        for metric in ('alpha','gamma','gamma_R90','cross_token_fraction','links_per_event','theta','r_over_floor','max_interval_frac','edge_drift'):
            center,low,high=lab.bootstrap([float(r[metric]) for r in group])
            row.update({metric:center,f'{metric}_ci_low':low,f'{metric}_ci_high':high})
        row['min_alpha_points']=min(int(r['alpha_fit_points']) for r in group)
        row['min_gamma_points']=min(int(r['gamma_fit_points']) for r in group)
        aggregates.append(row)
    if aggregates: lab.write_csv(DOC/'WP-F2_attempt2_aggregate.csv',aggregates)
    gates=[]
    if evaluate:
        assert len(rows)==64, 'R and M must both finish before gate evaluation'
        for mode,order in itertools.product(('R','M'),('kernel','legacy')):
            group=[next(r for r in aggregates if (r['mode'],r['order'],r['substrate'])==(mode,order,s)) for s in lab.SUBSTRATES]
            alpha_ok=all(math.isfinite(r['alpha']) for r in group)
            gamma_ok=all(math.isfinite(r['gamma']) for r in group[:3])
            ordering='pass' if alpha_ok and all(a['alpha']<b['alpha'] for a,b in zip(group,group[1:])) else 'fail' if alpha_ok else 'not_evaluable'
            separation='pass' if alpha_ok and all(a['alpha_ci_high']<b['alpha_ci_low'] for a,b in zip(group,group[1:])) else 'fail' if alpha_ok else 'not_evaluable'
            span=max(r['gamma'] for r in group[:3])-min(r['gamma'] for r in group[:3]) if gamma_ok else math.nan
            mechanism='pass' if gamma_ok and span<=spec['gate']['gamma_max_range'] else 'fail' if gamma_ok else 'not_evaluable'
            outcomes=(ordering,separation,mechanism)
            overall='pass' if all(v=='pass' for v in outcomes) else 'fail' if 'fail' in outcomes else 'not_evaluable'
            gates.append(dict(mode=mode,order=order,complete=True,evaluable=alpha_ok and gamma_ok,
                ordering=ordering,separation=separation,mechanism=mechanism,gamma_span=span,outcome=overall,
                passed=overall=='pass',adjacent_alpha_signs=';'.join(str(int(b['alpha']>a['alpha'])-int(b['alpha']<a['alpha'])) if alpha_ok else 'NA' for a,b in zip(group,group[1:]))))
        lab.write_csv(DOC/'WP-F2_gates.csv',gates)
        lab.write_csv(DOC/'WP-F2_attempt2_gates.csv',gates)
        lab.heartbeat('ATTEMPT2_GATES_EVALUATED thresholds_unchanged')
    report(aggregates,gates)
    return rows,aggregates,gates


def report(aggregates,gates=()):
    old=DOC/'WP-F2_attempt1_report.md'
    lines=['# WP-F2 rapport','', 'Forsøk 2 følger amendment 1. Forsøk 1 er bevart separat i sin helhet.', '',
        f'Original frys SHA-256: `{lab.sha(lab.FROZEN)}`.',f'Forsøk 2 frys SHA-256: `{lab.sha(FROZEN2)}`.','',
        'Metode: τ = 0,25·2^(k/4) til T/2; hendelser ved t≥T/2. Begge helninger bruker '
        'median V≥8 og τ≤T/4, minst seks punkter. γ bruker middelavstand; R90 og R90-γ rapporteres diagnostisk. '
        'KI er eksakt bootstrap over 256 trekk av fire historier. Udefinerte historier beholdes. '
        'Alle v7/v16-kilder og den opprinnelige laben er uendret. Separat wrapper erstatter bare M-seed-lese-/skrivesettet; '
        'M-dynamikken bruker den opprinnelige MarkAdapter med seed-policy mark. Ingen R-dynamikk kjøres.','']
    for mode in ('R','M'):
        group=[r for r in aggregates if r['mode']==mode]
        lines += [f'## Forsøk 2 — {mode}','']
        if not group:
            lines+=['Ikke analysert ennå.','']; continue
        lines += ['|orden|underlag|n|α [95% KI]|γ middel [95% KI]|γ R90|minste fit-punkter α/γ|',
                  '|---|---|---|---|---|---|---|']
        for r in group:
            lines.append(f'|{r["order"]}|{r["substrate"]}|{r["histories"]}|{r["alpha"]:.6f} [{r["alpha_ci_low"]:.6f}, {r["alpha_ci_high"]:.6f}]|{r["gamma"]:.6f} [{r["gamma_ci_low"]:.6f}, {r["gamma_ci_high"]:.6f}]|{r["gamma_R90"]:.6f}|{r["min_alpha_points"]}/{r["min_gamma_points"]}|')
        lines+=['','Alle kurver, parantall, avstandssummer, WP-F0-observabler, drift og tverrbindinger er lagret i forsøk 2-CSV-ene.','']
    lines+=['## Forsøk 1 — R (bevart)','',
            'Full original rapport: [WP-F2_attempt1_report.md](WP-F2_attempt1_report.md). Tallene under bruker det gamle gridet og γ på R90.','',
            '|orden|underlag|α|γ R90|','|---|---|---|---|']
    for r in lab.read_csv(DOC/'WP-F2_attempt1_aggregate.csv'):
        lines.append(f'|{r["order"]}|{r["substrate"]}|{float(r["alpha"]):.6f}|{float(r["gamma"]):.6f}|')
    lines+=['','## Uendrede porter / G4','']
    if not gates:
        lines+=['Gatene evalueres etter R og M, i bestilt rekkefølge.']
    else:
        lines+=['|modus|orden|rekkefølge|separasjon|γ-spenn|mekanisme|F2|','|---|---|---|---|---|---|---|']
        for g in gates:
            lines.append(f'|{g["mode"]}|{g["order"]}|{g["ordering"]}|{g["separation"]}|{g["gamma_span"]:.6f}|{g["mechanism"]}|{g["outcome"]}|')
        lines+=['','G4 og referansekvalifikasjon må leses sammen: ikke-evaluerbar α er manglende instrumentgrunnlag, '
            'ikke null eksponent eller et påvist fravær av geometri. De målte kalibreringsreferansene må skilles før '
            'endepunktet kan brukes som hypotesegate (AGENTS.md). Ingen terskel er endret. '
            'Naboforskjellenes fortegn står i gatefilen som transform-invariant rekkefølgekontroll. '
            'Fire historier gir grov KI-oppløsning; dette er en endelig kalibrering. Ingen WP-F3 kjøres.']
    lines+=['','## Status og avslutning','',
        'Målinger og integrasjon har separate statuser. Commit/push, offentlig arkiv, live-revisjon, RAG-sync og '
        'autentisert ferskhets-/sitasjonskontroll er ikke bekreftet. Ved faktisk .git-blokkering gjelder amendmentets stoppregel; integratoren committer. '
        'Uavhengig G1-kvittering gjenstår. Ingen fysikkpåstand.','']
    (DOC/'WP-F2_report.md').write_text('\n'.join(lines))


def reanalyze_R():
    spec=load_spec()
    start=time.monotonic()
    lab.heartbeat('ATTEMPT2_R_REANALYSIS_START saved_logs_only')
    for a in spec['assignments']:
        if a['mode']!='R': continue
        name=lab.file_prefix(a)
        assert not (DOC/f'{name}_attempt2_summary.csv').exists(), 'no duplicate analysis'
        analyze(name)
        aggregate(spec)
    (DOC/'WP-F2_attempt2_R_runtime.json').write_text(json.dumps(dict(seconds=time.monotonic()-start),indent=2)+'\n')
    load_spec()
    lab.heartbeat('ATTEMPT2_R_COMPLETE 16/16 saved_input_hashes_unchanged report_written')


def run_M():
    spec=load_spec()
    assert len(list(DOC.glob('WP-F2_R_*_attempt2_summary.csv')))==16
    start=time.monotonic()
    lab.heartbeat('ATTEMPT2_M_RUNTIME_ESTIMATE before_all_M_histories prior_R16_seconds=728.617 estimated_16M_seconds=1457.234 caveat=mark_kernel_and_machine_load estimate_not_measurement')
    lab.kernel_access=amended_kernel_access
    try:
        for a in spec['assignments']:
            if a['mode']!='M': continue
            name=lab.file_prefix(a)
            # Original run_history writes a diagnostic old-grid summary. The amended
            # result is separate and only the amended result reaches attempt-2 gates.
            lab.run_history(spec,a,8192)
            subprocess.run([lab.ANALYSIS_PYTHON,__file__,'--analyze',name],check=True,
                           env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'})
            aggregate(spec)
    finally:
        lab.kernel_access=ORIGINAL_ACCESS
    (DOC/'WP-F2_attempt2_M_runtime.json').write_text(json.dumps(dict(seconds=time.monotonic()-start),indent=2)+'\n')
    lab.heartbeat('ATTEMPT2_M_COMPLETE 16/16 report_written')


def main():
    p=argparse.ArgumentParser(__doc__)
    for flag in ('prepare','reanalyze-R','run-M','gates'):
        p.add_argument('--'+flag,action='store_true')
    p.add_argument('--analyze')
    args=p.parse_args()
    if args.prepare: prepare()
    elif args.reanalyze_R: reanalyze_R()
    elif args.run_M: run_M()
    elif args.gates: aggregate(load_spec(),True)
    elif args.analyze: load_spec(); analyze(args.analyze)
    else: p.error('choose operation')

if __name__=='__main__': main()
