"""Exhaustive finite calibration of both neighborhood algorithms and SAT encoding."""
import importlib.util
import functools
import itertools as it
import json
from pathlib import Path


def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def main():
    repair=module('repair');check=module('check_neighborhoods')
    pool=list(it.combinations(range(1,6),3));pairs=list(it.combinations(range(1,6),2))
    blocks=[set(b) for b in pool]
    _,_,_,masks,lists,coverers=check.prepare(dict(v=5,k=3,t=2,blocks=[list(b) for b in pool]))
    all_masks=[sum(1 << i for i,h in enumerate(pairs) if set(h)<=b) for b in blocks]
    sats=0
    for holes in range(1<<len(pairs)):
        expected=any((a|b)&holes==holes for a in all_masks for b in all_masks)
        h=[frozenset(p) for i,p in enumerate(pairs) if holes>>i&1]
        answer=repair.exact_two(h,5,3)
        assert (answer is not None)==expected
        if answer is not None:
            assert all(any(set(p)<=set(b) for b in answer) for p in h)
            sats+=1
        assert check.two(holes,masks,lists,coverers)==expected
        expected_three=any(functools.reduce(int.__or__,c,0)&holes==holes for c in it.combinations(all_masks,3))
        assert check.three(holes,masks,lists,coverers)==expected_three
    # Known C(5,3,2)=4 control: full 10 pairs cannot fit in three blocks;
    # exhaustive enumeration provides the expected answer independently.
    full=(1<<len(pairs))-1
    for q in [2,3,4]:
        expected=any(functools.reduce(int.__or__,c,0)==full for c in it.combinations(all_masks,q))
        status,answer,reason=repair.sat_repair([frozenset(p) for p in pairs],5,3,q,30000,7)
        assert status==('sat' if expected else 'unsat'),(q,status,reason)
        assert check.selected_sat(full,q,masks,lists,30000)==status
        if answer is not None: assert all(any(set(h)<=set(b) for b in answer) for h in pairs)
    print(json.dumps(dict(all_hole_subfamilies=1024,two_block_sat=sats,two_block_unsat=1024-sats,
                         sat_encoding_budgets=[2,3,4],all_agree=True,separate_author_review=False)))


if __name__=='__main__': main()
