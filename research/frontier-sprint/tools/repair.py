"""Exact incumbent neighborhoods: exhaustive 3-for-2 and seeded larger Z3 repairs.

The 3-for-2 solver exploits containment: after choosing one replacement,
all residual holes fit in one k-block iff their union has at most k points.
Z3 encodes replacement blocks directly as point-membership Booleans.
Neither UNSAT nor a completed census is a global lower bound.
"""
import argparse
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import random
import time


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def exact_two(holes, v, k):
    """Return <=2 blocks covering all holes, or None; complete, no time cap."""
    if not holes:
        return []
    # Every feasible pair has a member containing the first hole.
    pivot = holes[0]
    rest = [p for p in range(1, v + 1) if p not in pivot]
    for extra in it.combinations(rest, k - len(pivot)):
        a = pivot | frozenset(extra)
        union = frozenset().union(*(h for h in holes if not h <= a))
        if len(union) <= k:
            b = set(union)
            for p in range(1, v + 1):
                if len(b) == k:
                    break
                b.add(p)
            return [sorted(a), sorted(b)] if union else [sorted(a)]
    return None


def holes_after(subsets, owners, removed):
    mask = sum(1 << i for i in removed)
    return [h for h, own in zip(subsets, owners) if not own & ~mask]


def sat_repair(holes, v, k, q, timeout_ms, seed):
    import z3
    s = z3.Solver()
    s.set(timeout=timeout_ms, random_seed=seed)
    x = [[z3.Bool(f'x_{j}_{p}') for p in range(1,v+1)] for j in range(q)]
    for row in x:
        s.add(z3.PbEq([(a, 1) for a in row], k))
    for h in holes:
        s.add(z3.Or([z3.And([x[j][p-1] for p in sorted(h)]) for j in range(q)]))
    # Block permutation symmetry only; numeric Boolean masks ordered increasingly.
    codes = [z3.Sum([z3.If(a, 1 << p, 0) for p, a in enumerate(row)]) for row in x]
    for a,b in zip(codes,codes[1:]):
        s.add(a < b)
    status = s.check()
    blocks = None
    if status == z3.sat:
        m = s.model()
        blocks = [[p+1 for p,a in enumerate(row) if z3.is_true(m.eval(a))] for row in x]
    return str(status), blocks, s.reason_unknown() if status == z3.unknown else None


def run(a):
    witness = json.loads(a.input.read_text())
    v,k,t = [witness[n] for n in ('v','k','t')]
    incumbent = [frozenset(b) for b in witness['blocks']]
    subsets = [frozenset(h) for h in it.combinations(range(1,v+1),t)]
    owners = [sum(1 << i for i,b in enumerate(incumbent) if h <= b) for h in subsets]
    if not all(owners):
        raise ValueError('incumbent has uncovered subsets')
    seed = int(hashlib.sha256(f'{a.seed}:{v},{k},{t}'.encode()).hexdigest()[:8],16)
    rng = random.Random(seed)
    deletions = list(it.combinations(range(len(incumbent)), a.remove))
    if a.remove != 3:
        rng.shuffle(deletions)
        if a.trials:
            deletions = deletions[:a.trials]
    output = dict(instance=[v,k,t], incumbent_blocks=len(incumbent), input=str(a.input),
                  input_sha256=digest(a.input), seed=a.seed, derived_seed=seed,
                  remove=a.remove, replace_at_most=a.remove-1, timeout_ms=a.timeout_ms,
                  planned=len(deletions), total_deletion_sets=math.comb(len(incumbent),a.remove),
                  method='exact-containment-two' if a.remove==3 else 'z3-point-membership', trials=[])
    start = time.perf_counter()
    for n,removed in enumerate(deletions):
        holes = holes_after(subsets,owners,removed)
        tick = time.perf_counter()
        if a.remove==3:
            replacement = exact_two(holes,v,k)
            status, reason = ('sat' if replacement is not None else 'unsat'), None
        else:
            status,replacement,reason = sat_repair(holes,v,k,a.remove-1,a.timeout_ms,(seed+n)&0x7fffffff)
        row = dict(removed=list(removed), holes=len(holes),status=status,seconds=time.perf_counter()-tick)
        if reason: row['reason']=reason
        if replacement is not None:
            row['replacement']=replacement
            kept=[sorted(b) for i,b in enumerate(incumbent) if i not in removed]
            # Empty/redundant additions are unnecessary: output a simple family.
            candidate=dict(v=v,k=k,t=t,blocks=[list(b) for b in sorted(set(tuple(b) for b in kept+replacement))])
            path=a.output.parent.parent/'witnesses'/f'candidate-{v}-{k}-{t}-r{a.remove}-{n}.json'
            path.write_text(json.dumps(candidate,indent=2)+'\n')
            row['candidate']=str(path)
        output['trials'].append(row)
        if n%50==0: print(json.dumps(dict(instance=[v,k,t],remove=a.remove,done=n+1,planned=len(deletions),status=status)),flush=True)
    output['seconds']=time.perf_counter()-start
    output['counts']={s:sum(r['status']==s for r in output['trials']) for s in ['sat','unsat','unknown']}
    import z3
    output['z3_version']=z3.get_version_string()
    a.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='trials'}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--seed',required=True);p.add_argument('--remove',type=int,choices=[3,4,5,6],default=3)
    p.add_argument('--trials',type=int,default=32,help='0: complete deletion census')
    p.add_argument('--timeout-ms',type=int,default=5000)
    a=p.parse_args()
    if a.output.exists(): p.error('refusing to overwrite existing results')
    if a.trials < 0 or a.timeout_ms <= 0: p.error('invalid budget')
    run(a)
