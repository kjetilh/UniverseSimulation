"""Runtime contract tests; use Python >=3.12 and installed NetworkX path."""
from collections import Counter
import random
import unittest

from Tools.influence_order_lab import runtime, substrate_graph, MarkAdapter, kernel_access


class InfluenceRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v7,cls.a,cls.b,cls.ac=runtime()

    def test_known_substrate_degrees(self):
        import networkx as nx
        for name,n,degree in (('ring',1024,2),('lat2',1024,4),('lat3',1000,6),('rrg',1024,3)):
            graph=substrate_graph(name,11)
            self.assertEqual(len(graph),n)
            self.assertEqual(set(dict(graph.degree()).values()),{degree})
            self.assertTrue(nx.is_connected(graph))

    def test_mark_bias_and_exact_write_support(self):
        state=self.a.nx_to_state(substrate_graph('ring',1),[0,1])
        params=self.a.anchor_params()
        adapter=MarkAdapter(self.ac.LocalSeedClockAdapter(),.25,'mark')
        base=adapter.base.family_kernel(state,'token',params)
        observed=adapter.family_kernel(state,'token',params)
        for descriptor,probability in base.items():
            self.assertAlmostEqual(probability,observed[descriptor],places=14)
        adapter.marks[1]=4
        observed=adapter.family_kernel(state,'token',params)
        self.assertAlmostEqual(sum(observed.values()),1,places=14)
        self.assertAlmostEqual(observed[('move',0,0,1)]/observed[('move',0,0,1023)],2)
        masses=Counter()
        for descriptor,probability in observed.items(): masses[descriptor[1]]+=probability
        self.assertAlmostEqual(masses[0],.5)
        self.assertAlmostEqual(masses[1],.5)
        manager=self.v7.PairManager(next_node_id=1024,next_token_id=2)
        event=self.b.materialize_event('token',('swap',0,0,1,2),manager)
        oldr,oldw=self.a.action_access(state,event)
        reads,writes=kernel_access(state,event,'M','mark',oldr,oldw)
        self.assertTrue({'adj:1023','adj:1','node:0','edge:0:1','mark:1022','mark:2'}<=reads)
        self.assertEqual(writes,{'token:0','mark:0'})
        edges=state.g.edge_set()
        adapter.apply_descriptor(state,'token',event.descriptor,params,manager)
        self.assertEqual(state.g.edge_set(),edges)
        self.assertEqual(state.token_pos[0],1)
        self.assertEqual(adapter.marks[0],1)
        adapter.apply_descriptor(state,'seed',('seed_tid',0),params,manager)
        self.assertEqual(state.g.edge_set(),edges)
        self.assertEqual(adapter.marks[1],5)
        self.assertEqual(manager.next_node_id,1025)

    def test_R_trace_and_legacy_order_match_original_step(self):
        # Synthetic ring, not a universe history. Same RNG draws, unchanged
        # adapter, Params and original DAG.add for both copies.
        state=self.a.nx_to_state(substrate_graph('ring',3),[0,30,60,90])
        other=state.clone()
        params=self.a.anchor_params()
        adapter=self.ac.LocalSeedClockAdapter()
        rng=random.Random(201)
        rng_other=random.Random(201)
        manager=self.v7.PairManager(next_node_id=1024,next_token_id=4)
        manager_other=self.v7.PairManager(next_node_id=1024,next_token_id=4)
        legacy=self.b.DependencyDAG()
        reference=self.b.DependencyDAG()
        for i in range(192):
            family,rate=self.b.choose_family(adapter.family_rates(state,params),rng)
            family_other,rate_other=self.b.choose_family(adapter.family_rates(other,params),rng_other)
            dt=rng.expovariate(rate)
            dt_other=rng_other.expovariate(rate_other)
            self.assertEqual((family,rate,dt),(family_other,rate_other,dt_other))
            state.t+=dt
            other.t+=dt_other
            descriptor=self.v7.sample_from_dist(adapter.family_kernel(state,family,params),rng)
            desc_other=self.v7.sample_from_dist(adapter.family_kernel(other,family_other,params),rng_other)
            self.assertEqual(descriptor,desc_other)
            event=self.b.materialize_event(family,descriptor,manager)
            oldr,oldw=self.a.action_access(state,event)
            reads,writes=kernel_access(state,event,'R','pending',oldr,oldw)
            self.assertTrue(oldr<=reads)
            self.assertEqual(oldw,writes)
            legacy.add(oldr,oldw)
            reference.add(*self.a.action_access(other,event))
            adapter.apply_descriptor(state,family,descriptor,params,manager)
            adapter.apply_descriptor(other,family_other,desc_other,params,manager_other)
        self.assertTrue(self.v7.states_equal(state,other))
        self.assertEqual(legacy.predecessors,reference.predecessors)


if __name__=='__main__': unittest.main()
