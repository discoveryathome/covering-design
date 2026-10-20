"""Small exact controls for the new engine and its independent sweep checker."""
import argparse
import json
import subprocess
import tempfile
from itertools import combinations
from pathlib import Path
from sweep import verify_union, PACKAGE

p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--scratch',type=Path,required=True)
a=p.parse_args();engine=a.engine.resolve();a.scratch.mkdir(parents=True,exist_ok=True)
# Exhaustive (5,3,2) oracle agrees with the existing direct-containment verifier.
import sys
sys.path.insert(0,str(PACKAGE.parents[1]))
from covering.verify import verify, Invalid
blocks=list(combinations(range(1,6),3))
for mask in range(1<<len(blocks)):
    w={'v':5,'k':3,'t':2,'blocks':[list(b) for i,b in enumerate(blocks) if mask>>i&1]}
    outcomes=[]
    for checker in [verify,verify_union]:
        try:checker(w);outcomes.append(True)
        except (ValueError,Invalid):outcomes.append(False)
    assert outcomes[0]==outcomes[1],mask
for path in (PACKAGE.parents[1]/'tests/fixtures').glob('*.json'):
    try:verify_union(json.loads(path.read_text()))
    except ValueError:pass
    else:raise AssertionError(path)
for v,k,t in [(7,3,2),(5,3,2),(4,4,4),(4,2,1)]:
    out=a.scratch/f'control-{v}-{k}-{t}.json'
    r=subprocess.run([str(engine),str(v),str(k),str(t),'123','16','2',str(out),'-','greedy'],capture_output=True,text=True,check=True)
    w=json.loads(out.read_text());result=verify(w,(v,k,t));assert result==verify_union(w)|{'uncovered':0}
    if (v,k,t)==(7,3,2):assert result['blocks']==7
# Known easy improvement: all ten triples can be reduced to a four-block (5,3,2) cover.
initial=a.scratch/'all-triples.txt';initial.write_text('\n'.join(' '.join(map(str,b)) for b in blocks)+'\n')
out=a.scratch/'repaired-five.json'
r=subprocess.run([str(engine),'5','3','2','123','0','0.5',str(out),str(initial),'repair'],capture_output=True,text=True,check=True)
result=json.loads(r.stdout);assert result['blocks']==4,result
verify(json.loads(out.read_text()),(5,3,2),4)
print('PASS: 1024 exhaustive checker comparisons, six negative fixtures, four engine controls, and known easy repair from 10 to 4 blocks')
