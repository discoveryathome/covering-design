"""Exact independent coverage checker using colex ranks and a byte per required set.

No imports of search code, C++ subset IDs, or search incidence arrays. Sorted
1-based subset a_1<...<a_t has unique rank sum_i binomial(a_i-1,i) in
0..binomial(v,t)-1. Every required subset is checked through its unique rank.
"""
import argparse
import json
from itertools import combinations
from math import comb
from pathlib import Path


def verify_rank(witness, expected=None, expected_blocks=None):
    if not isinstance(witness,dict):raise ValueError('witness must be an object')
    v,k,t=(witness[n] for n in ('v','k','t'))
    if any(type(x) is not int for x in (v,k,t)) or not 1<=t<=k<=v:raise ValueError('bad parameters')
    if expected is not None and (v,k,t)!=tuple(expected):raise ValueError('instance mismatch')
    blocks=witness['blocks']
    if not isinstance(blocks,list):raise ValueError('blocks must be a list')
    if expected_blocks is not None and len(blocks)!=expected_blocks:raise ValueError('count mismatch')
    total=comb(v,t)
    if total>30_000_000:raise ValueError('checker allocation cap: thirty million required subsets')
    choose=[[comb(n,i) if n>=i else 0 for i in range(t+1)] for n in range(v)]
    covered=bytearray(total);seen=set()
    for b in blocks:
        if not isinstance(b,list) or len(b)!=k or any(type(x) is not int or not 1<=x<=v for x in b):
            raise ValueError('invalid block')
        canonical=tuple(sorted(b))
        if len(set(b))!=k or canonical in seen:raise ValueError('duplicate point or block')
        seen.add(canonical)
        for subset in combinations(canonical,t):
            rank=0
            for i,point in enumerate(subset,1):rank+=choose[point-1][i]
            covered[rank]=1
    missing=covered.count(0)
    if missing:raise ValueError(f'uncovered {missing}/{total}')
    return dict(valid=True,v=v,k=k,t=t,blocks=len(blocks),covered=total,required=total,uncovered=0)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witness',type=Path)
    p.add_argument('--instance',nargs=3,type=int);p.add_argument('--blocks',type=int);a=p.parse_args()
    try:r=verify_rank(json.loads(a.witness.read_text()),a.instance,a.blocks)
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(1,f'INVALID: {e}\n')
    print(json.dumps(r,sort_keys=True))


if __name__=='__main__':main()
