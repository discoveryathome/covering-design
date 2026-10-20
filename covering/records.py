"""Check each independent (v,k,t) record and its locally stored witness."""
import argparse
import hashlib
import json
from pathlib import Path
from .verify import Invalid, verify
from .bounds import lower_bounds

ROOT=Path(__file__).resolve().parents[1]


def rows():
    data=json.loads((ROOT/'data/records.json').read_text())
    for row in data:
        if any(type(row[n]) is not int for n in ('v','k','t','blocks','lower_bound')):
            raise Invalid('record parameters and counts must be integers')
    keys=[(r['v'],r['k'],r['t']) for r in data]
    if len(keys)!=len(set(keys)):
        raise Invalid('duplicate instance key in record table')
    return data


def check_row(row):
    instance=tuple(row[n] for n in ('v','k','t'))
    witness=(ROOT/row['witness']).resolve()
    if not witness.is_relative_to(ROOT):
        raise Invalid('witness must remain inside repository')
    raw=witness.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row['witness_sha256']:
        raise Invalid('witness hash mismatch')
    result=verify(json.loads(raw),instance,row['blocks'])
    bound=lower_bounds(*instance)['schonheim']
    if row['lower_bound']!=bound or row['blocks']<bound:
        raise Invalid('record disagrees with recomputed Schonheim lower bound')
    result['lower_bound']=bound
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['check_row','check_all','bounds','audit'])
    p.add_argument('--v',type=int);p.add_argument('--k',type=int);p.add_argument('--t',type=int)
    a=p.parse_args()
    try:
        rs=rows()
        if a.command=='check_row':
            selected=[r for r in rs if (r['v'],r['k'],r['t'])==(a.v,a.k,a.t)]
            if len(selected)!=1: raise Invalid('unknown or ambiguous instance')
            print(json.dumps(check_row(selected[0]),sort_keys=True))
        elif a.command=='check_all':
            for r in rs: print(json.dumps(check_row(r),sort_keys=True))
            print(f'PASS: {len(rs)} independent records verified')
        elif a.command=='bounds':
            for r in rs:
                b=lower_bounds(r['v'],r['k'],r['t'])
                print(json.dumps({'instance':[r['v'],r['k'],r['t']],**b,
                    'archive_reported_lower_bound':r['archive_lower_bound']}))
        else:
            archive=json.loads((ROOT/'data/ljcr-selected.json').read_text())['records']
            for r in rs:
                key=f"C({r['v']},{r['k']},{r['t']})"
                old=archive[key]
                if old['size']!=r['archive_upper_bound'] or old['low_bd']!=r['archive_lower_bound']:
                    raise Invalid(f'archive metadata mismatch: {key}')
                check_row(r)
                if r['v'] != 7:
                    original=json.loads((ROOT/'data/ljcr-blocks-selected.json').read_text())['records'][key]
                    witness=json.loads((ROOT/r['witness']).read_text())
                    if original!=witness['blocks']:
                        raise Invalid(f'archive block array mismatch: {key}')
                print(f"{key}: archive {old['low_bd']}..{old['size']}; local {r['blocks']} blocks; successor confirmation pending")
    except (Invalid,OSError,ValueError,KeyError,TypeError) as e:
        p.exit(1,f'INVALID: {e}\n')


if __name__=='__main__': main()
