"""One-pass exact redundant-block audit of the twenty selected archive witnesses."""
import hashlib
import json
import random
from collections import Counter
from itertools import combinations
from pathlib import Path
from sweep import PACKAGE, verify_union


def main():
    seed=json.loads((PACKAGE/'experiment.json').read_text())['seed'];results=[]
    for row in json.loads((PACKAGE/'data/repair-selection.json').read_text()):
        name=f"{row['v']}-{row['k']}-{row['t']}";path=PACKAGE/'data'/f'archive-{name}.json';w=json.loads(path.read_text())
        blocks=[tuple(sorted(b)) for b in w['blocks']];subsets=[list(combinations(b,w['t'])) for b in blocks]
        counts=Counter(s for group in subsets for s in group)
        order=list(range(len(blocks)));random.Random(f'{seed}:prune:{name}').shuffle(order);removed=set()
        for i in order:
            if all(counts[s]>1 for s in subsets[i]):
                removed.add(i)
                for s in subsets[i]:counts[s]-=1
        result={'v':w['v'],'k':w['k'],'t':w['t'],'archive_upper':len(blocks),'removed':len(removed),'blocks':len(blocks)-len(removed),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        if removed:
            candidate={**w,'blocks':[list(b) for i,b in enumerate(blocks) if i not in removed],
                       'provenance':{'method':'redundancy-audit','source':str(path.relative_to(PACKAGE)),'attribution':'Daniel M. Gordon, LJCR v1.2 and original contributors; CC BY 4.0 source data'}}
            verify_union(candidate);out=PACKAGE/'witnesses'/f'pruned-{name}.json';out.write_text(json.dumps(candidate,indent=2)+'\n');result['witness']=str(out.relative_to(PACKAGE))
        results.append(result)
    (PACKAGE/'results/redundancy-audit.json').write_text(json.dumps(results,indent=2)+'\n')
    print(f"Audited {len(results)} archive witnesses; {sum(r['removed']>0 for r in results)} improved by redundant-block deletion")


if __name__=='__main__':main()
