"""Materialize a two-point covering construction and independently verify its parents and result."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from check_native import check_native


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('parent_a',type=Path);p.add_argument('parent_b',type=Path)
    p.add_argument('--checker',type=Path,required=True);p.add_argument('--scratch',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    p.add_argument('--archive-upper',type=int,required=True);a=p.parse_args()
    start=time.monotonic();pa=json.loads(a.parent_a.read_text());pb=json.loads(a.parent_b.read_text());a.scratch.mkdir(parents=True,exist_ok=True)
    if (pa['v'],pa['k']-2,pa['t']-1)!=(pb['v'],pb['k'],pb['t']):raise ValueError('incompatible parents')
    ca=check_native(a.parent_a,a.checker,a.scratch/'parent-a.txt');print('parent A verified',ca,flush=True)
    cb=check_native(a.parent_b,a.checker,a.scratch/'parent-b.txt');print('parent B verified',cb,flush=True)
    v=pa['v']+2;blocks=pa['blocks']+[b+[v-1,v] for b in pb['blocks']]
    provenance={'method':'two-point-combination','parents':[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in (a.parent_a,a.parent_b)],
      'attribution':'Derived from Daniel M. Gordon LJCR v1.2 and original contributors; source counts in data/archive-counts.json.',
      'source_data_license':'CC-BY-4.0','modification':'Parent A unchanged; append both new points to every block of parent B. No claim of current novelty.'}
    w={'v':v,'k':pa['k'],'t':pa['t'],'blocks':blocks,'provenance':provenance}
    a.output.write_text(json.dumps(w,separators=(',',':'))+'\n')
    checked=check_native(a.output,a.checker,a.scratch/'result.txt',(v,pa['k'],pa['t']),len(blocks))
    if len(blocks)>=a.archive_upper:raise ValueError('result does not improve provided archive count')
    report={'parents':[ca,cb],'result':checked,'archive_upper':a.archive_upper,'improvement':a.archive_upper-len(blocks),
      'wall_seconds_including_verification':time.monotonic()-start,'status':'author-checked archive improvement; current record status unconfirmed'}
    a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)


if __name__=='__main__':main()
