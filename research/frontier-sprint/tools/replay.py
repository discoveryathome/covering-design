"""Offline, stdlib-only evidence binding and exact witness replay (no search).

Use check_neighborhoods.py separately for the longer finite-exclusion replay.
This script checks evidence bindings, not a formal UNSAT proof certificate.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import time


ROOT=Path(__file__).resolve().parents[3]
PACKAGE=ROOT/'research/frontier-sprint'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text())


def main():
    start=time.perf_counter()
    spec=importlib.util.spec_from_file_location('rank',ROOT/'research/initial-sweep/tools/verify_rank.py')
    rank=importlib.util.module_from_spec(spec);spec.loader.exec_module(rank)
    current={tuple(row[n] for n in ['v','k','t']):row['blocks'] for row in read(PACKAGE/'data/current-selected-counts.json')['rows']}
    checked=0
    for row in read(PACKAGE/'data/shortlist.json'):
        key=tuple(row[n] for n in ['v','k','t']);path=ROOT/row['local_witness']
        assert sha(path)==row['local_witness_sha256']
        assert current[key]==row['current_published_upper']
        rank.verify_rank(read(path),key,row['local_witness_blocks']);checked+=1
        lower=1
        v,k,t=key
        for j in range(t-1,-1,-1):lower=((v-j)*lower+k-j-1)//(k-j)
        assert lower==row['lower_bound_schonheim_proved_here']
    for path in (PACKAGE/'data').glob('archive-*.json'):
        if path.name=='archive-metadata-selected.json':continue
        rank.verify_rank(read(path));checked+=1
    weighted=[]
    for path in sorted((PACKAGE/'results').glob('wls-*/result.json')):
        r=read(path);key=tuple(r['instance'])
        assert sha(ROOT/r['input'])==r['input_sha256']
        assert sha(ROOT/r['best_witness'])==r['best_witness_sha256']
        assert r['comparison_upper']==current[key]
        rank.verify_rank(read(ROOT/r['best_witness']),key,r['best_blocks']);checked+=1
        complete=0
        for text in path.parent.glob('shrink_cover_*.txt'):
            blocks=[list(map(int,line.split())) for line in text.read_text().splitlines() if line.strip()]
            rank.verify_rank(dict(zip(['v','k','t'],key),blocks=blocks),key,len(blocks));complete+=1;checked+=1
        assert complete==r['complete_outputs_verified']
        assert r['delta_vs_published']==r['comparison_upper']-r['best_blocks']
        weighted.append(dict(instance=list(key),seed=r['seed'],blocks=r['best_blocks'],comparison=current[key]))
    for path in (PACKAGE/'results').glob('*-r*.json'):
        r=read(path)
        assert sha(ROOT/r['input'])==r['input_sha256']
        assert len(r['trials'])==r['planned']==len({tuple(row['removed']) for row in r['trials']})
        assert r['counts']=={s:sum(row['status']==s for row in r['trials']) for s in ['sat','unsat','unknown']}
    exclusion_rows=0
    for name in ['census-first-two.json','census-third.json','r4-complete-enumeration.json','r4-medium-enumeration.json']:
        for r in read(PACKAGE/'checks'/name):
            assert sha(ROOT/r['input'])==r['input_sha256']
            assert r['counts']['sat']==r['counts']['unknown']==0
            exclusion_rows+=r['checked']
    assert read(PACKAGE/'checks/controls-final.json')['all_agree']
    if (PACKAGE/'artifacts.sha256.json').exists():
        for name,value in read(PACKAGE/'artifacts.sha256.json').items():assert sha(ROOT/name)==value,name
    print(json.dumps(dict(valid=True,witness_checks=checked,weighted=weighted,finite_exclusion_decisions_bound=exclusion_rows,
                         seconds=time.perf_counter()-start,separate_author_review=False),sort_keys=True))


if __name__=='__main__': main()
