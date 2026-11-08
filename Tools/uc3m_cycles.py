"""Connected remnant interventions and repeated tagged-core recovery."""
from collections import defaultdict
import random
from Tools import local_growth_candidate as law
from Tools.local_growth_observer import _region
from Tools.uc3g_followup import _descendant, _core_size
from Tools.uc3g_match import component, opportunity_signature, _wl_witness


def blocks(edges):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    left = set(adj)
    results = []
    while left:
        nodes = component(adj, min(left))
        results.append(sorted((u,v) for u in nodes for v in adj[u] if u < v))
        left -= nodes
    return sorted(results, key=lambda g: (-len(g), g))


def edge(a, b):
    return tuple(sorted((a,b)))


def setup(state, spec, arm):
    i, x, y, a, b = spec
    after = law.clone_state(state)
    if arm == "preserved":
        law.apply_event(after,i,"bud",y)
        law.apply_event(after,i,"collapse",x)
    else:
        law.apply_event(after,i,"slide",y,a)
        law.apply_event(after,i,"slide",x,b)
    return after


def find_match(state, tag, retained):
    nodes = component(state.adjacency,state.units[tag])
    size = len(_region(state.adjacency,nodes)["core_nodes"])
    signature = None
    for group in blocks({(a,b) for a,b,_ in retained}):
        if len(group)<4:
            break
        edges=set(group)
        for i,x in enumerate(state.units):
            for y in sorted(state.adjacency[x]):
                if edge(x,y) not in edges:
                    continue
                for a in sorted(state.adjacency[x]-state.adjacency[y]-{y}):
                    if edge(x,a) not in edges:
                        continue
                    middle=law.clone_state(state)
                    law.apply_event(middle,i,"slide",y,a)
                    if len(_region(middle.adjacency,nodes)["core_nodes"])!=size:
                        continue
                    for b in sorted(state.adjacency[y]-state.adjacency[x]-{x}):
                        if edge(y,b) not in edges:
                            continue
                        spec=(i,x,y,a,b)
                        right=setup(state,spec,"rewired")
                        if len(_region(right.adjacency,nodes)["core_nodes"])!=size:
                            continue
                        witness=_wl_witness(state,right,tag,nodes)
                        if not witness:
                            continue
                        if signature is None:
                            signature=opportunity_signature(state,tag)
                        if opportunity_signature(right,tag)!=signature:
                            continue
                        left=setup(state,spec,"preserved")
                        assert law.edge_set(left)==law.edge_set(state)
                        assert left.units==right.units==state.units
                        assert {v:len(s) for v,s in left.adjacency.items()}=={v:len(s) for v,s in right.adjacency.items()}
                        remaining=edges & law.edge_set(right)
                        assert len(remaining)==len(edges)-2
                        return left,right,dict(spec=spec,block=group,remaining_sizes=[len(g) for g in blocks(remaining)],
                                               nonisomorphism=witness,opportunities=signature)
    return None


def follow(state, tag, seed, mode, spec, arm):
    local,tag,indices=_descendant(law.clone_state(state),tag)
    i,x,y,a,b=spec
    actor=indices.index(i)
    rng=random.Random(seed)
    start=extreme=k=_core_size(local)
    marks=[]
    parents=[]
    t=attempts=0
    while t<96 and attempts<16384 and local.adjacency[local.units[tag]] and len(marks)<5:
        if mode=="null":
            event=law.apply_event(local,actor,"slide",y if t%2==0 else x,a if arm=="preserved" else b)
        elif mode=="positive":
            if t%4<2:
                u=local.units[tag]
                parents.append(u)
                event=law.apply_event(local,tag,"bud",rng.choice(sorted(local.adjacency[u])))
            else:
                event=law.apply_event(local,tag,"collapse",parents.pop())
        else:
            event=law.attempt_step(local,rng)
        attempts+=1
        if not event.changed:
            continue
        t+=1
        if event.kind=="cut":
            local,tag,_=_descendant(local,tag)
        k=_core_size(local)
        rising=len(marks)%2==0
        extreme=min(extreme,k) if rising and marks else max(extreme,k) if not rising else extreme
        if (k-extreme if rising else extreme-k)>=2:
            marks.append((t,k))
            extreme=k
    hit=len(marks)==5
    reason="hit" if hit else "window" if t==96 else "absorbed" if not local.adjacency[local.units[tag]] else "attempt_cap"
    return dict(success=hit,marks=str(marks),exposure=t,attempts=attempts,k_start=start,k_final=k,stop=reason,censored=reason=="attempt_cap")
