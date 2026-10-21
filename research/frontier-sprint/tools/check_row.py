"""Verify one pinned local shortlist witness and report its current comparison.

The comparison count is not certified by the witness unless counts match.
No writes, network requests, search imports, or accepted-frontier changes.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['v','k','t']:p.add_argument('--'+key,type=int,required=True)
    p.add_argument('--direct',action='store_true',help='use original containment verifier')
    p.add_argument('--proposal',action='store_true',help='bind to the unaccepted proposal table')
    a=p.parse_args();package=Path(__file__).resolve().parents[1];root=package.parents[1]
    rows=json.loads((package/('proposal-records.json' if a.proposal else 'data/shortlist.json')).read_text())
    row=next(r for r in rows if [r[n] for n in ['v','k','t']]==[a.v,a.k,a.t])
    if a.proposal:
        row=dict(row,local_witness=row['witness'],local_witness_sha256=row['sha256'],local_witness_blocks=row['blocks'],
                 current_source='https://coveringrepository.com/download_archive_vkt.aspx',current_audited_on=row['current_audit_date'])
    f=root/row['local_witness']
    if hashlib.sha256(f.read_bytes()).hexdigest()!=row['local_witness_sha256']:raise ValueError('witness hash mismatch')
    if a.direct:
        spec=importlib.util.spec_from_file_location('verifier',root/'covering/verify.py');name='verify'
    else:
        spec=importlib.util.spec_from_file_location('verifier',package.parent/'initial-sweep/tools/verify_rank.py');name='verify_rank'
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    start=time.perf_counter();result=getattr(module,name)(json.loads(f.read_text()),(a.v,a.k,a.t),row['local_witness_blocks'])
    result.update(witness=str(f),witness_sha256=row['local_witness_sha256'],current_published_upper=row['current_published_upper'],
                  current_source=row['current_source'],audit_date=row['current_audited_on'],seconds=time.perf_counter()-start,
                  comparison=('matches-published-count' if result['blocks']==row['current_published_upper'] else
                              'worse-than-published-count' if result['blocks']>row['current_published_upper'] else
                              'below-audited-count-novelty-review-required'),separate_author_review=False)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
