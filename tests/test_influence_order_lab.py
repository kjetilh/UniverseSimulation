"""Independent checks for the F2 estimators; run with installed Python 3.11."""
import csv
import json
import math
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from Tools import influence_order_lab as lab


class InfluenceMeasurements(unittest.TestCase):
    def test_random_posets_against_set_reference(self):
        rng=random.Random(9)
        for n in (1,2,7,16,35):
            for _ in range(8):
                parents=[[p for p in range(c) if rng.random()<.17] for c in range(n)]
                past=[]
                depth=[]
                for ps in parents:
                    ancestors=set(ps)
                    for p in ps: ancestors.update(past[p])
                    past.append(ancestors)
                    depth.append(max((depth[p]+1 for p in ps),default=0))
                expected_links=sum(not any(p in past[q] for q in ps if q!=p) for ps in parents for p in ps)
                max_interval=max([1]+[2+sum(p in past[v] for v in past[c]) for c in range(n) for p in past[c]])
                bits,metrics=lab.poset_metrics(parents)
                self.assertEqual([set(i for i in range(n) if b>>i&1) for b in bits],past)
                self.assertAlmostEqual(metrics['links_per_event'],expected_links/n)
                self.assertAlmostEqual(metrics['max_interval_frac'],max_interval/n)
                self.assertEqual(metrics['comparable_pairs'],sum(map(len,past)))

    def test_spatial_and_volume_curves_exact_chain(self):
        # Time = event id+1; node cycles on an eight-node ring. Fully known
        # ancestry: every earlier event. Compare every eligible pair directly.
        import numpy as np
        import networkx as nx
        n=128
        events=[dict(event_id=i,time=i+1,dt=1,token=i%2,node=i%8,snapshot=0,
                     parents=str(i-1) if i else '',legacy_parents=str(i-1) if i else '') for i in range(n)]
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)
            lab.write_csv(output/'test_events.csv',events)
            lab.write_csv(output/'test_snapshots.csv',[dict(snapshot=0,u=u,v=v) for u,v in nx.cycle_graph(8).edges()])
            (output/'test_metadata.json').write_text(json.dumps({'steps':n}))
            with patch.object(lab,'DOC',output),patch.object(lab,'heartbeat',lambda *args:None):
                lab.analyze('test')
            rows=lab.read_csv(output/'test_curves.csv')
            for row in rows:
                tau=float(row['tau'])
                volumes=[]
                distances=[]
                for e in range(n):
                    if e+1<n/2: continue
                    selected=[a for a in range(e) if e-a<=tau]
                    volumes.append(len(selected))
                    distances.extend(min(abs(e%8-a%8),8-abs(e%8-a%8)) for a in selected)
                self.assertEqual(float(row['V_median']),float(np.median(volumes)))
                self.assertEqual(float(row['R90']),float(np.quantile(distances,.9)))
                self.assertEqual(int(row['pair_count']),len(distances))
                self.assertEqual(int(row['undefined_distance_pairs']),0)
            summary=lab.read_csv(output/'test_summary.csv')
            self.assertTrue(all(abs(float(r['cross_token_fraction'])-1)<1e-12 for r in summary))

    def test_missing_fit_is_not_a_number(self):
        self.assertTrue(math.isnan(lab.fit([1],[8],8)[0]))
        self.assertTrue(all(math.isnan(x) for x in lab.bootstrap([1.,math.nan,2.,3.])))


if __name__=='__main__':
    unittest.main()
