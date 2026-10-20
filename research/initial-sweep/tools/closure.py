"""Audit three elementary construction rules against pinned LJCR metadata.

This emits conditional arithmetic candidates, not verified witnesses or new records.
"""
import argparse
import json
from pathlib import Path


def closure(source):
    initial={tuple(map(int,key[2:-1].split(','))):r['size'] for key,r in source.items()}
    current=dict(initial);proofs={}
    for turn in range(20):
        changed=False
        for (v,k,t),old in sorted(current.items()):
            options=[]
            if (v-1,k,t) in current and (v-1,k-1,t-1) in current:
                options.append((current[v-1,k,t]+current[v-1,k-1,t-1],'one-point-combination',[(v-1,k,t),(v-1,k-1,t-1)]))
            if (v+1,k,t) in current:options.append((current[v+1,k,t],'delete-point-and-pad',[(v+1,k,t)]))
            if (v,k-1,t) in current:options.append((current[v,k-1,t],'enlarge-blocks',[(v,k-1,t)]))
            if options:
                new,rule,parents=min(options)
                if new<old:
                    current[v,k,t]=new;proofs[v,k,t]={'rule':rule,'parents':parents,'parent_bounds':[current[x] for x in parents]};changed=True
        if not changed:break
    candidates=[{'v':key[0],'k':key[1],'t':key[2],'archive_upper':initial[key],'derived_upper':n,
                'delta':n-initial[key],'proof':proofs[key],
                'status':'arithmetic construction candidate; witness and current-frontier audit required'}
                for key,n in current.items() if n<initial[key]]
    return {'rounds':turn+1,'source_cells':len(source),'rules':['one-point-combination','delete-point-and-pad','enlarge-blocks'],'candidates':candidates}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('metadata',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=closure(json.loads(a.metadata.read_text()));a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'source_cells':result['source_cells'],'arithmetic_candidates':len(result['candidates'])}))


if __name__=='__main__':main()
