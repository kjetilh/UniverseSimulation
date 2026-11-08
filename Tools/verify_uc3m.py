"""Replay UC3M loss checkpoints, compare both exact transition laws, and audit cycle times."""
import argparse
import ast
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
import csv
import gzip
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from Tools import local_growth_candidate as law
from Tools.verify_uc3g import replay_loss, project, core, component, one_step, check_witness, pack, sha, compact
from Tools.run_uc3g import summarize


def crossings(history):
    """Independent offline first passage scan of recorded core sizes."""
    marks=[]
    begin=0
    for stage in range(5):
        for t in range(begin+1,len(history)):
            previous=history[begin:t]
            if stage==0:
                gain=history[t]-history[0]
            elif stage%2:
                gain=max(previous)-history[t]
            else:
                gain=history[t]-min(previous)
            if gain>=2:
                marks.append((t,history[t]))
                begin=t
                break
        else:
            break
    return marks


def verify_world(job):
    row,pair,rows=job
    checkpoint=replay_loss(row,pair)
    if not pair:
        assert not rows
        return 0
    audit=pair["match"]
    actor,x,y,a,b=audit["spec"]
    tag=pair["tag"]
    nodes=component(checkpoint.adjacency,checkpoint.units[tag])
    g=set(map(tuple,audit["block"]))
    retained={tuple(z[:2]) for z in pair["retained"]}
    adj=defaultdict(set)
    for u,v in retained:
        adj[u].add(v)
        adj[v].add(u)
    block_nodes=component(adj,x)
    assert len(g)>=4 and g=={e for e in retained if e[0] in block_nodes}
    branches={}
    choices=0
    for arm in ("preserved","rewired"):
        st=law.clone_state(checkpoint)
        if arm=="preserved":
            law.apply_event(st,actor,"bud",y)
            law.apply_event(st,actor,"collapse",x)
        else:
            law.apply_event(st,actor,"slide",y,a)
            law.apply_event(st,actor,"slide",x,b)
        assert len(g-law.edge_set(st))==(0 if arm=="preserved" else 2)
        assert st.units==checkpoint.units and sha(compact(pack(st)).encode())==pair["start_hashes"][arm]
        options,count=one_step(st,tag)
        assert compact(options)==compact(audit["opportunities"])
        choices+=count
        branches[arm]=st
    check_witness(list(branches.values()),tag,audit["nonisomorphism"],nodes)
    assert len(rows)==192
    null_cache={}
    for r in rows:
        arm,mode=r["arm"],r["mode"]
        seed=int(sha(f'UC3M/{r["world"]}/{arm}/{mode}/{r["rep"]}'.encode())[:16],16)
        assert seed==int(r["seed"])
        n=int(r["attempts"])
        if mode=="null" and arm in null_cache:
            assert null_cache[arm]==(n,r["marks"],r["exposure"],r["k_final"],r["stop"])
            continue
        rng=random.Random(seed)
        st,f,ids=project(law.clone_state(branches[arm]),tag,list(range(len(checkpoint.units))))
        history=[len(core(st.adjacency,st.adjacency))]
        parents=[]
        for _ in range(n):
            t=len(history)-1
            if mode=="null":
                e=law.apply_event(st,ids.index(actor),"slide",x if t%2 else y,a if arm=="preserved" else b)
            elif mode=="positive" and t%4<2:
                u=st.units[f]
                parents.append(u)
                e=law.apply_event(st,f,"bud",rng.choice(sorted(st.adjacency[u])))
            elif mode=="positive":
                e=law.apply_event(st,f,"collapse",parents.pop())
            else:
                e=law.attempt_step(st,rng)
            if e.changed:
                st,f,ids=project(st,f,ids)
                history.append(len(core(st.adjacency,st.adjacency)))
        marks=crossings(history)
        assert marks==ast.literal_eval(r["marks"]) and len(history)-1==int(r["exposure"])
        hit=len(marks)==5
        assert hit==(r["success"]=="True") and history[-1]==int(r["k_final"])
        assert r["stop"]==("hit" if hit else "window" if len(history)==97 else "absorbed" if not st.adjacency[st.units[f]] else "attempt_cap")
        if hit:
            assert marks[-1][0]==len(history)-1
        if mode=="null":
            null_cache[arm]=(n,r["marks"],r["exposure"],r["k_final"],r["stop"])
    return choices


def verify(out):
    data=json.loads((out/'UC3M_result.json').read_bytes())
    for root,hashes in ((out,data['evidence_sha256']),(ROOT,data['source_sha256'])):
        for name,digest in hashes.items():
            assert sha((root/name).read_bytes())==digest
    worlds=list(csv.DictReader((out/'UC3M_worlds.csv').open()))
    pairs={p['world']:p for p in map(json.loads,(out/'UC3M_pairs.jsonl').read_text().splitlines())}
    rows=defaultdict(list)
    with gzip.open(out/'UC3M_followups.csv.gz','rt') as f:
        for r in csv.DictReader(f):
            rows[r['world']].append(r)
    assert len(worlds)==len({int(r['seed']) for r in worlds})==512
    assert set(rows)==set(pairs)
    for world in worlds:
        world['n']=int(world['n'])
        records=rows.get(world['world'],[])
        if records:
            assert len({(r['mode'],r['arm'],r['rep']) for r in records})==192
            for arm in ('preserved','rewired'):
                for mode in ('null','positive','natural'):
                    group=[r for r in records if (r['arm'],r['mode'])==(arm,mode)]
                    assert {int(r['rep']) for r in group}==set(range(32))
                    hits=sum(r['success']=='True' for r in group)
                    if mode=='natural':
                        assert hits==int(world[arm+'_hits'])
                        world[arm+'_hits']=hits
                    else:
                        assert hits==(32 if mode=='positive' else 0)
            world['natural_censored']=int(world['natural_censored'])
            assert world['natural_censored']==sum(r['censored']=='True' for r in records if r['mode']=='natural')
    assert summarize(worlds,True)==data['analysis']
    with ProcessPoolExecutor(max_workers=6) as pool:
        counts=list(pool.map(verify_world,[(w,pairs.get(w['world']),rows.get(w['world'],[])) for w in worlds]))
    print(json.dumps(dict(prefixes=len(worlds),pairs=len(pairs),rows=sum(map(len,rows.values())),legal_moves=sum(counts),verified=True)))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    verify(parser.parse_args().out)
