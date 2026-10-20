"""Reproduce deterministic baseline artifacts; no changes to frontier records."""
import argparse
import json
import platform
from pathlib import Path
from .search import greedy
from .verify import verify
from .records import rows, ROOT


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed',type=int,default=20261020)
    p.add_argument('--restarts',type=int,default=8)
    p.add_argument('--output-dir',type=Path,default=Path('results/reproduced'))
    a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True)
    results=[]
    for r in rows():
        v,k,t=(r[n] for n in ('v','k','t'))
        w=greedy(v,k,t,a.seed,a.restarts)
        check=verify(w,(v,k,t))
        name=f'{v}-{k}-{t}.json'
        (a.output_dir/name).write_text(json.dumps(w,indent=2)+'\n')
        out={'v':v,'k':k,'t':t,'blocks':check['blocks'],
             'archive_upper_bound':r['archive_upper_bound'],
             'delta_to_archive':check['blocks']-r['archive_upper_bound'],
             'seed':a.seed,'restarts':a.restarts,'restart_sizes':w['provenance']['restart_sizes'],
             'verified':True,'witness':str(a.output_dir/name)}
        results.append(out)
        print(json.dumps(out,sort_keys=True),flush=True)
    (a.output_dir/'summary.json').write_text(json.dumps({'method':'random-tie-greedy+redundancy-deletion-v1',
        'python':platform.python_version(),'results':results},indent=2)+'\n')


if __name__=='__main__': main()
