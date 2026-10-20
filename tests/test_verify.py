import copy
import json
import unittest
from itertools import combinations
from pathlib import Path
from covering.verify import Invalid, verify
from covering.bounds import lower_bounds
from covering.records import check_row, rows

ROOT = Path(__file__).resolve().parents[1]


class VerifierTests(unittest.TestCase):
    def setUp(self):
        self.fano = json.loads((ROOT/'witnesses/fano.json').read_text())

    def test_fano_and_optimality(self):
        r = verify(self.fano, (7,3,2), 7)
        self.assertEqual((r['covered'],r['required']), (21,21))
        self.assertEqual(lower_bounds(7,3,2)['schonheim'],7)

    def test_invalid_fixtures(self):
        for path in (ROOT/'tests/fixtures').glob('*.json'):
            with self.subTest(path=path.name), self.assertRaises(Invalid):
                verify(json.loads(path.read_text()))

    def test_instance_and_count_are_checked(self):
        for args in [((8,3,2),7), ((7,3,2),6)]:
            with self.assertRaises(Invalid):
                verify(self.fano,*args)

    def test_wrong_types_and_parameters(self):
        for field,value in [('v',True),('k',3.0),('t',0),('v',2),('blocks',None)]:
            w=copy.deepcopy(self.fano);w[field]=value
            with self.subTest(field=field,value=value), self.assertRaises(Invalid):
                verify(w)
        for w in [None,{},[],{'v':7,'k':3}]:
            with self.assertRaises(Invalid): verify(w)

    def test_relabeling_and_block_order_invariance(self):
        w=copy.deepcopy(self.fano)
        w['blocks']=[list(reversed([8-x for x in b])) for b in reversed(w['blocks'])]
        self.assertEqual(verify(w)['covered'],21)

    def test_all_subfamilies_against_incidence_oracle(self):
        # Exhaust all 2^10 families on (5,3,2). Oracle enumerates pairs per block;
        # production verifier enumerates universe pairs and checks containment.
        blocks=list(combinations(range(1,6),3))
        for mask in range(1<<len(blocks)):
            chosen=[list(b) for i,b in enumerate(blocks) if mask>>i&1]
            pairs={p for b in chosen for p in combinations(b,2)}
            if len(pairs)==10:
                self.assertTrue(verify(dict(v=5,k=3,t=2,blocks=chosen))['valid'])
            else:
                with self.assertRaises(Invalid):
                    verify(dict(v=5,k=3,t=2,blocks=chosen))

    def test_edge_instances(self):
        for v,k,t,blocks in [(4,4,4,[[1,2,3,4]]),(4,2,1,[[1,2],[3,4]]),
                              (4,2,2,[list(b) for b in combinations(range(1,5),2)])]:
            self.assertTrue(verify(dict(v=v,k=k,t=t,blocks=blocks))['valid'])

    def test_record_binding_mutations(self):
        row=rows()[1]
        for key,value in [('blocks',row['blocks']-1),('v',row['v']+1),
                          ('witness_sha256','0'*64),('lower_bound',row['lower_bound']+1)]:
            changed=dict(row);changed[key]=value
            with self.subTest(field=key), self.assertRaises(Invalid):
                check_row(changed)


if __name__=='__main__': unittest.main()
