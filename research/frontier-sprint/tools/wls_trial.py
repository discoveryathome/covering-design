"""Bounded pinned weighted-search trial; independently check every saved cover.

Use a dedicated output directory. External executable must be run under the
workspace OS sandbox. No fetching, compiler invocation, or frontier mutation.
"""
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import re
import subprocess
import time


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('executable',type=Path);p.add_argument('input',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--seconds',type=int,default=360);p.add_argument('--seed',type=int,required=True)
    p.add_argument('--comparison',type=int,required=True)
    a=p.parse_args()
    if not 1<=a.seconds<=3600 or not 0<=a.seed<2**32 or a.comparison<=0:
        p.error('require 1..3600 seconds, uint32 seed and positive comparison')
    a.output.mkdir(exist_ok=False)
    spec=importlib.util.spec_from_file_location('rank',Path(__file__).resolve().parents[2]/'initial-sweep/tools/verify_rank.py')
    rank=importlib.util.module_from_spec(spec);spec.loader.exec_module(rank)
    w=json.loads(a.input.read_text());v,k,t=[w[n] for n in ['v','k','t']];b=len(w['blocks'])
    if not 1<=t<k<=25 or not k<=v<=99 or comb(v,t)>3_000_000:
        raise ValueError('weighted engine scope: t<k<=25, v<=99, at most three million required subsets')
    check_start=time.perf_counter();initial_check=rank.verify_rank(w,(v,k,t),b);check_seconds=time.perf_counter()-check_start
    initial=a.output/'start.txt';initial.write_text('\n'.join(' '.join(map(str,row)) for row in w['blocks'])+'\n')
    cmd=[str(a.executable.resolve()),str(v),str(k),str(t),str(b),str(a.seconds),str(a.seed),str(initial.resolve()),'7','0.05','1']
    begin=time.perf_counter()
    with (a.output/'console.txt').open('w') as log:
        run=subprocess.run(cmd,cwd=a.output,stdout=log,stderr=subprocess.STDOUT,timeout=a.seconds+90)
    if run.returncode:raise RuntimeError(f'engine exited {run.returncode}; see console')
    candidates=[]
    for path in a.output.glob('shrink_cover_*.txt'):
        rows=[list(map(int,line.split())) for line in path.read_text().splitlines() if line.strip()]
        candidate=dict(v=v,k=k,t=t,blocks=rows)
        start=time.perf_counter();checked=rank.verify_rank(candidate,(v,k,t),len(rows));elapsed=time.perf_counter()-start
        candidates.append((len(rows),path,candidate,checked,elapsed))
    assert candidates,'no valid complete output'
    _,best_path,best,best_check,best_check_seconds=min(candidates,key=lambda c:c[0])
    witness=a.output/'best.json';witness.write_text(json.dumps(best,indent=2)+'\n')
    result=dict(instance=[v,k,t],input=str(a.input),input_sha256=sha(a.input),initial_check=initial_check,
                input_verify_seconds=check_seconds,executable_sha256=sha(a.executable),command=cmd,
                seed=a.seed,budget_seconds=a.seconds,elapsed_seconds=time.perf_counter()-begin,
                comparison_upper=a.comparison,comparison_scope='Pinned van Staden 2026-10-19 published list; live-table reconfirmation required',
                best_blocks=len(best['blocks']),delta_vs_published=a.comparison-len(best['blocks']),
                best_witness=str(witness),best_witness_sha256=sha(witness),best_verify=best_check,
                best_verify_seconds=best_check_seconds,complete_outputs_verified=len(candidates),
                source='WynandVStaden/covering-design-records@970a68752d01ca5aa04129bebbb92e1b268c947e',
                accepted_frontier_changed=False)
    (a.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
