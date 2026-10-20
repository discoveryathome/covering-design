"""Reproducible bounded search driver; exact union check is independent of C++ scores."""
import argparse
import hashlib
import json
import math
import subprocess
import time
from itertools import combinations
from pathlib import Path

PACKAGE=Path(__file__).resolve().parents[1]


def verify_union(witness):
    v,k,t=(witness[n] for n in ('v','k','t'))
    if any(type(x) is not int for x in (v,k,t)) or not 1<=t<=k<=v:
        raise ValueError('invalid parameters')
    family=witness['blocks']
    if not isinstance(family,list):raise ValueError('blocks must be a list')
    seen=set();covered=set()
    for b in family:
        if not isinstance(b,list) or len(b)!=k or any(type(x) is not int or not 1<=x<=v for x in b):
            raise ValueError('invalid block')
        canonical=tuple(sorted(b))
        if len(set(b))!=k or canonical in seen:raise ValueError('duplicate point or block')
        seen.add(canonical);covered.update(combinations(canonical,t))
    if len(covered)!=math.comb(v,t):raise ValueError('incomplete coverage')
    return {'v':v,'k':k,'t':t,'blocks':len(family),'covered':len(covered),'required':math.comb(v,t),'valid':True}


def execute(engine,row,seed,restarts,seconds,out,initial='-',mode='greedy'):
    command=[str(engine),str(row['v']),str(row['k']),str(row['t']),str(seed),str(restarts),str(seconds),str(out),str(initial),mode]
    start=time.monotonic()
    proc=subprocess.run(command,capture_output=True,text=True,timeout=seconds+30)
    if proc.returncode:raise RuntimeError(proc.stderr)
    result=json.loads(proc.stdout)
    raw=out.read_bytes();w=json.loads(raw);check=verify_union(w)
    if any(check[n]!=row[n] for n in ('v','k','t')) or check['blocks']!=result['blocks']:
        raise ValueError('engine result and exact witness disagree')
    return {**result,'seed':str(seed),'command':command,'wall_seconds_including_check':time.monotonic()-start,
      'archive_upper':row['archive_upper'],'archive_reported_lower':row['archive_reported_lower'],
      'delta_to_archive':check['blocks']-row['archive_upper'],'witness':str(out.relative_to(PACKAGE)),
      'witness_sha256':hashlib.sha256(raw).hexdigest(),'coverage_check':check,
      'input_sha256':None if initial=='-' else hashlib.sha256(Path(initial).read_bytes()).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--stage',choices=['greedy','repair'],required=True)
    a=p.parse_args();engine=a.engine.resolve()
    experiment=json.loads((PACKAGE/'experiment.json').read_text());rows=json.loads((PACKAGE/'data/instances.json').read_text())
    budget=experiment['method_budget'];start=time.monotonic();path=PACKAGE/'results'/f'{a.stage}.jsonl'
    if path.exists():raise ValueError(f'refusing to overwrite {path}')
    selected=rows if a.stage=='greedy' else json.loads((PACKAGE/'data/repair-selection.json').read_text())
    trials=1 if a.stage=='greedy' else budget['repair_seed_count']
    global_seconds=budget['stage_1_global_seconds'] if a.stage=='greedy' else budget['repair_global_seconds']
    waiting=0.0
    with path.open('w') as f:
        for row in selected:
            for trial in range(trials):
                if time.monotonic()-start-waiting>=global_seconds:
                    print('GLOBAL BUDGET EXHAUSTED',flush=True);return
                key=f"{row['v']}-{row['k']}-{row['t']}"
                seed=int.from_bytes(hashlib.sha256(f"{experiment['seed']}:{a.stage}:{key}:{trial}".encode()).digest()[:8],'big')
                out=PACKAGE/'witnesses'/f'{a.stage}-{key}-{trial}.json'
                if a.stage=='greedy':
                    result=execute(engine,row,seed,budget['greedy_restarts_per_cell'],10,out)
                else:
                    initial=PACKAGE/row['initial_text']
                    wait_start=time.monotonic()
                    while not initial.exists():
                        if time.monotonic()-wait_start>600:raise RuntimeError('archive seed unavailable after ten minutes')
                        time.sleep(1)
                    waiting+=time.monotonic()-wait_start
                    seconds=budget['repair_seconds_per_trial']
                    result=execute(engine,row,seed,0,seconds,out,initial,'repair')
                result['trial']=trial
                f.write(json.dumps(result,sort_keys=True)+'\n');f.flush()
                print(f"{a.stage} {key} trial {trial}: {result['blocks']} vs archive {row['archive_upper']} ({result['delta_to_archive']:+d}); {result['seconds']:.2f}s",flush=True)
    print(f'COMPLETE {a.stage}: {len(selected)} cells x {trials} trials in {time.monotonic()-start:.2f}s',flush=True)


if __name__=='__main__':main()
