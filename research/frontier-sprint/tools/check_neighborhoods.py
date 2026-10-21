"""Separate replay: enumerate ALL k-sets and intersect hole-coverer bitsets.

No search-module imports. Replays 3-for-2 decisions by a different algorithm;
--enumerate-three also checks 4-for-3 repairs combinatorially. Other larger
replays use a second Z3 encoding (one Boolean per k-set), not a proof kernel.
"""
import argparse
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import time


def prepare(w):
    v,k,t=(w[n] for n in ['v','k','t'])
    family=[set(b) for b in w['blocks']]
    universe=list(it.combinations(range(1,v+1),t))
    index={h:i for i,h in enumerate(universe)}
    pool=list(it.combinations(range(1,v+1),k))
    masks=[]; lists=[[] for _ in universe]
    for j,b in enumerate(pool):
        ids=[index[h] for h in it.combinations(b,t)]
        masks.append(sum(1 << i for i in ids))
        for i in ids: lists[i].append(j)
    coverers=[sum(1 << j for j in row) for row in lists]
    return family,universe,pool,masks,lists,coverers


def two(holes,masks,lists,coverers):
    if not holes: return True
    pivot=(holes & -holes).bit_length()-1
    for j in lists[pivot]:
        left=holes & ~masks[j]
        possible=-1
        while left:
            bit=left & -left
            possible &= coverers[bit.bit_length()-1]
            if not possible: break
            left ^= bit
        if possible: return True
    return False


def three(holes,masks,lists,coverers):
    if not holes: return True
    pivot=(holes & -holes).bit_length()-1
    remaining={holes & ~masks[j] for j in lists[pivot]}
    return any(two(left,masks,lists,coverers) for left in remaining)


def selected_sat(holes,q,masks,lists,timeout_ms):
    import z3
    if not holes: return 'sat'
    candidates=sorted({j for i in range(len(lists)) if holes>>i&1 for j in lists[i]})
    x={j:z3.Bool(f'b_{j}') for j in candidates}
    s=z3.Solver();s.set(timeout=timeout_ms,random_seed=0)
    s.add(z3.PbLe([(b,1) for b in x.values()],q))
    left=holes
    while left:
        bit=left & -left;i=bit.bit_length()-1
        s.add(z3.Or([x[j] for j in lists[i]]));left ^= bit
    return str(s.check())


def check(path,extra_limit=0,enumerate_three=False):
    r=json.loads(path.read_text());input_path=Path(r['input'])
    assert hashlib.sha256(input_path.read_bytes()).hexdigest()==r['input_sha256']
    w=json.loads(input_path.read_text());v,k,t=r['instance']
    assert [w[n] for n in ['v','k','t']]==r['instance']
    family,universe,pool,masks,lists,coverers=prepare(w)
    assert len(family)==r['incumbent_blocks']
    for b in w['blocks']:
        assert len(b)==k and len(set(b))==k and all(type(p) is int and 1<=p<=v for p in b)
    assert len({tuple(sorted(b)) for b in family})==len(family)
    assert all(any(set(h)<=b for b in family) for h in universe)
    deletion_rows=[tuple(row['removed']) for row in r['trials']]
    assert len(set(deletion_rows))==len(deletion_rows)==r['planned']
    if r['remove']==3:
        assert set(deletion_rows)==set(it.combinations(range(len(family)),3))
    start=time.perf_counter();counts={'sat':0,'unsat':0,'unknown':0};checked=0
    for row in r['trials']:
        removed=row['removed']
        assert len(set(removed))==r['remove'] and all(type(j) is int and 0<=j<len(family) for j in removed)
        kept=[b for j,b in enumerate(family) if j not in removed]
        holes=sum(1 << i for i,h in enumerate(universe) if not any(set(h)<=b for b in kept))
        assert holes.bit_count()==row['holes']
        if r['remove']==3:
            status='sat' if two(holes,masks,lists,coverers) else 'unsat'
        elif extra_limit and checked<extra_limit:
            if enumerate_three and r['remove']==4:
                status='sat' if three(holes,masks,lists,coverers) else 'unsat'
            else: status=selected_sat(holes,r['remove']-1,masks,lists,30000)
        else: continue
        counts[status]+=1;checked+=1
        if status!='unknown': assert status==row['status'],(path,removed,status,row['status'])
        if checked%100==0: print(json.dumps({'input':str(path),'checked':checked}),flush=True)
    result=dict(input=str(path),input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),instance=r['instance'],
                checked=checked,counts=counts,seconds=time.perf_counter()-start,
                algorithm='all-k-set-coverer-intersection' if r['remove']==3 else ('all-k-set-three-enumeration' if enumerate_three and r['remove']==4 else 'z3-all-k-set-selection'),
                separate_author_review=False)
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',nargs='+',type=Path)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--larger-limit',type=int,default=0)
    p.add_argument('--enumerate-three',action='store_true')
    a=p.parse_args()
    if a.output.exists(): p.error('refusing overwrite')
    a.output.write_text(json.dumps([check(path,a.larger_limit,a.enumerate_three) for path in a.results],indent=2)+'\n')
