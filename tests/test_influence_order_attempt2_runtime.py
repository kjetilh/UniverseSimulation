import unittest
from Tools import influence_order_attempt2 as amended
from Tools import influence_order_lab as lab

class AmendmentRuntime(unittest.TestCase):
    def test_seed_reads_exact_host_and_writes_mark_only(self):
        v7,a,b,ac=lab.runtime()
        state=a.nx_to_state(lab.substrate_graph('ring',1),[3,9])
        adapter=lab.MarkAdapter(ac.LocalSeedClockAdapter(),.25,'mark')
        manager=v7.PairManager(next_node_id=1024,next_token_id=2)
        params=a.anchor_params()
        for descriptor,expected_reads in [(('seed_tid',0),{'token:0','node:3'}),(('seed',9),{'node:9'})]:
            concrete=b.materialize_event('seed',descriptor,manager)
            lr,lw=a.action_access(state,concrete)
            reads,writes=amended.amended_kernel_access(state,concrete,'M','mark',lr,lw)
            host=3 if descriptor[0]=='seed_tid' else 9
            self.assertEqual(reads,expected_reads)
            self.assertEqual(writes,{f'mark:{host}'})
            edges=state.g.edge_set(); positions=dict(state.token_pos)
            before_nodes=state.g.num_nodes()
            adapter.apply_descriptor(state,'seed',descriptor,params,manager)
            self.assertEqual(state.g.edge_set(),edges)
            self.assertEqual(state.g.num_nodes(),before_nodes)
            self.assertEqual(state.token_pos,positions)
            self.assertEqual(adapter.marks[host],1)

if __name__=='__main__': unittest.main()
