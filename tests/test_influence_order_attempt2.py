import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from Tools import influence_order_attempt2 as a2
from Tools import influence_order_lab as lab

class AmendmentMeasurements(unittest.TestCase):
    def test_exact_pairs_and_fit_window(self):
        import numpy as np
        import networkx as nx
        n=256
        events=[dict(event_id=i,time=i+1,dt=1,token=i%2,node=i%8,snapshot=0,
                     parents=str(i-1) if i else '',legacy_parents=str(i-1) if i else '') for i in range(n)]
        with tempfile.TemporaryDirectory() as d:
            doc=Path(d)
            lab.write_csv(doc/'test_events.csv',events)
            lab.write_csv(doc/'test_snapshots.csv',[dict(snapshot=0,u=u,v=v) for u,v in nx.cycle_graph(8).edges()])
            (doc/'test_metadata.json').write_text(json.dumps(dict(steps=n)))
            frozen=doc/'frozen.json'; frozen.write_text('{}')
            with patch.object(a2,'DOC',doc),patch.object(a2,'FROZEN2',frozen),patch.object(lab,'heartbeat',lambda *a:None):
                a2.analyze('test')
            curves=lab.read_csv(doc/'test_attempt2_curves.csv')
            for row in curves:
                tau=float(row['tau'])
                volumes=[]; distances=[]
                for e in range(n):
                    if e+1<n/2: continue
                    selected=[a for a in range(e) if e-a<=tau]
                    volumes.append(len(selected))
                    distances.extend(min(abs(e%8-a%8),8-abs(e%8-a%8)) for a in selected)
                self.assertEqual(float(row['V_median']),np.median(volumes))
                self.assertEqual(int(row['pair_count']),len(distances))
                self.assertEqual(int(row['distance_sum']),sum(distances))
                self.assertEqual(int(row['undefined_distance_pairs']),0)
                if distances:
                    self.assertAlmostEqual(float(row['R_mean']),np.mean(distances))
                    self.assertAlmostEqual(float(row['R90']),np.quantile(distances,.9))
                else: self.assertTrue(math.isnan(float(row['R_mean'])))
            for row in lab.read_csv(doc/'test_attempt2_summary.csv'):
                pts=[c for c in curves if c['order']==row['order'] and c['fit_window']=='True']
                expected=lab.fit([float(c['tau']) for c in pts],[float(c['V_median']) for c in pts])[0]
                self.assertAlmostEqual(float(row['alpha']),expected)
                self.assertEqual(int(row['alpha_fit_points']),len(pts))

    def test_six_points_and_no_late_window_leak(self):
        tau=[1,2,3,4,5,6,7]
        self.assertTrue(math.isnan(a2.fit_window(tau,[8]*7,[8]*7,20)[0]))
        self.assertEqual(a2.fit_window(tau,[8]*7,[8]*7,24),(0.,6))
        self.assertTrue(math.isnan(a2.fit_window(tau,[7]*7,[8]*7,100)[0]))
        grid=a2.tau_grid(128)
        self.assertEqual((grid[0],grid[-1]),(.25,64))
        self.assertTrue(all(abs(b/a-2**.25)<1e-14 for a,b in zip(grid,grid[1:])))

if __name__=='__main__': unittest.main()
