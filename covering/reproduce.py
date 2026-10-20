"""Offline full replay of local record evidence and verifier controls."""
import json
import hashlib
import subprocess
import sys
from .records import ROOT, rows, check_row
from .verify import verify


def main():
    frontier=json.loads((ROOT/'discover/frontier.json').read_text())
    for artifact in frontier['artifacts']:
        p=(ROOT/artifact['path']).resolve()
        if not p.is_relative_to(ROOT) or hashlib.sha256(p.read_bytes()).hexdigest()!=artifact['sha256']:
            raise ValueError(f"artifact hash mismatch: {artifact['path']}")
    subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True)
    summary=json.loads((ROOT/'witnesses/baseline/summary.json').read_text())['results']
    for row in rows():
        print(json.dumps(check_row(row),sort_keys=True),flush=True)
        p=ROOT/'witnesses/baseline'/f"{row['v']}-{row['k']}-{row['t']}.json"
        w=json.loads(p.read_text())
        result=verify(w,(row['v'],row['k'],row['t']))
        s=next(x for x in summary if (x['v'],x['k'],x['t'])==(row['v'],row['k'],row['t']))
        if result['blocks']!=s['blocks']:
            raise ValueError('baseline summary disagrees with witness')
    print('PASS: 5 record witnesses, 5 baseline witnesses, Fano optimum, and verifier controls',flush=True)


if __name__=='__main__': main()
