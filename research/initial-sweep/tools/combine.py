"""Combine a (v-1,k,t) cover and a (v-1,k-1,t-1) cover with a new point.

Reverify both parents and the full result using an independent exact rank checker.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path
from verify_rank import verify_rank


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('parent_a',type=Path);p.add_argument('parent_b',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    start=time.monotonic();pa=json.loads(a.parent_a.read_text());pb=json.loads(a.parent_b.read_text())
    if (pa['v'],pa['k']-1,pa['t']-1)!=(pb['v'],pb['k'],pb['t']):raise ValueError('incompatible parents')
    ca=verify_rank(pa);print('parent A verified',ca,flush=True);cb=verify_rank(pb);print('parent B verified',cb,flush=True)
    v=pa['v']+1
    blocks=pa['blocks']+[b+[v] for b in pb['blocks']]
    provenance={'method':'one-point-combination','parents':[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in (a.parent_a,a.parent_b)],
      'attribution':'Derived from Daniel M. Gordon LJCR v1.2 and original contributors; source histories in data/closure-metadata.json.',
      'source_data_license':'CC-BY-4.0','modification':'Parent A unchanged; append the new point to every block of parent B. No independent novelty claim.'}
    w={'v':v,'k':pa['k'],'t':pa['t'],'blocks':blocks,'provenance':provenance}
    check=verify_rank(w);a.output.write_text(json.dumps(w,separators=(',',':'))+'\n')
    report={'parents':[ca,cb],'result':check,'witness_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'wall_seconds_including_verification':time.monotonic()-start,'status':'author-checked construction; current record status unconfirmed'}
    a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)


if __name__=='__main__':main()
