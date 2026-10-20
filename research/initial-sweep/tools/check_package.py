"""Offline audit of search-trial witnesses and proposed per-instance records."""
import argparse
import hashlib
import json
from pathlib import Path
from sweep import verify_union, PACKAGE
from verify_rank import verify_rank
from check_native import check_native


def check_row(row, native_checker=None, matrix_dir=None):
    path=(PACKAGE/row['witness']).resolve()
    if not path.is_relative_to(PACKAGE):raise ValueError('witness outside package')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row['witness_sha256']:raise ValueError('hash mismatch')
    if native_checker:
        matrix=matrix_dir/f"{row['v']}-{row['k']}-{row['t']}.txt"
        result=check_native(path,native_checker,matrix,(row['v'],row['k'],row['t']),row['blocks'])
    else:
        result=verify_rank(json.loads(raw),(row['v'],row['k'],row['t']),row['blocks'])
    b=1
    for i in range(row['t']-1,-1,-1):b=((row['v']-i)*b+row['k']-i-1)//(row['k']-i)
    if b!=row['lower_bound']:raise ValueError('bound mismatch')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['all','check_row'])
    for name in ('v','k','t'):p.add_argument('--'+name,type=int)
    p.add_argument('--native-checker',type=Path)
    p.add_argument('--matrix-dir',type=Path)
    a=p.parse_args()
    if a.native_checker and not a.matrix_dir:p.error('--native-checker requires --matrix-dir')
    rows=json.loads((PACKAGE/'proposal-records.json').read_text())
    if a.command=='check_row':
        selected=[r for r in rows if (r['v'],r['k'],r['t'])==(a.v,a.k,a.t)]
        if len(selected)!=1:raise ValueError('unknown or ambiguous proposed instance')
        print(json.dumps(check_row(selected[0],a.native_checker,a.matrix_dir),sort_keys=True));return
    artifact_file=PACKAGE/'results/artifacts.json'
    if artifact_file.exists():
        for artifact in json.loads(artifact_file.read_text()):
            path=(PACKAGE/artifact['path']).resolve()
            if not path.is_relative_to(PACKAGE) or hashlib.sha256(path.read_bytes()).hexdigest()!=artifact['sha256']:
                raise ValueError(f"artifact mismatch: {artifact['path']}")
    counts=json.loads((PACKAGE/'data/archive-counts.json').read_text());total=0;wins=0
    for stage in ('greedy','repair'):
        path=PACKAGE/'results'/f'{stage}.jsonl'
        if not path.exists():continue
        for line in path.read_text().splitlines():
            r=json.loads(line);wpath=(PACKAGE/r['witness']).resolve()
            if not wpath.is_relative_to(PACKAGE):raise ValueError('trial path outside package')
            raw=wpath.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=r['witness_sha256']:raise ValueError('trial witness hash mismatch')
            w=json.loads(raw);check=verify_union(w)
            if any(check[n]!=r[n] for n in ('v','k','t','blocks')):raise ValueError('trial identity/count mismatch')
            source=counts[f"C({r['v']},{r['k']},{r['t']})"]
            if source['size']!=r['archive_upper']:raise ValueError('archive comparison mismatch')
            if r['delta_to_archive']!=r['blocks']-r['archive_upper']:raise ValueError('delta mismatch')
            wins+=r['delta_to_archive']<0;total+=1
    for row in rows:print(json.dumps(check_row(row,a.native_checker,a.matrix_dir),sort_keys=True))
    print(f'PASS: {total} exact trial witnesses; {wins} trial archive improvements; {len(rows)} verified proposed records; artifacts match')


if __name__=='__main__':main()
