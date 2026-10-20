"""Add explicit archive attribution to repair envelopes; never change block arrays.

Preserve the raw engine envelope hash in the trial record. The research engine's
initial save used a generic greedy tag even for a supplied archive incumbent.
"""
import hashlib
import json
from pathlib import Path
from sweep import PACKAGE


def normalize_record(result):
    if result.get('provenance_normalized'):return result
    path=PACKAGE/result['witness'];raw=path.read_bytes();w=json.loads(raw)
    before=json.dumps(w['blocks'],separators=(',',':'))
    provenance=w.setdefault('provenance',{})
    provenance['engine_reported_method']=provenance['method']
    provenance['method']='archive-seeded-delete-repair-v1'
    provenance['outcome']='unchanged archive incumbent' if result['blocks']==result['initial_blocks'] else 'smaller verified construction'
    provenance['source_input_sha256']=result['input_sha256']
    provenance['attribution']='Daniel M. Gordon, LJCR v1.2, and original contributors in data/instances.json'
    provenance['source_data_license']='CC-BY-4.0'
    path.write_text(json.dumps(w,separators=(',',':'))+'\n')
    assert json.dumps(json.loads(path.read_text())['blocks'],separators=(',',':'))==before
    result['raw_engine_witness_sha256']=hashlib.sha256(raw).hexdigest()
    result['witness_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    result['provenance_normalized']=True
    return result


def main():
    path=PACKAGE/'results/repair.jsonl'
    rows=[normalize_record(json.loads(line)) for line in path.read_text().splitlines()]
    tmp=path.with_suffix('.tmp');tmp.write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in rows));tmp.replace(path)
    print(f'Normalized {len(rows)} trial envelopes; all block arrays preserved')


if __name__=='__main__':main()
