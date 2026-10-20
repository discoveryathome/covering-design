"""Bind a JSON witness to an independently checked native matrix representation."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def check_native(witness_path, executable, matrix_path, expected=None, expected_blocks=None):
    raw=Path(witness_path).read_bytes();w=json.loads(raw)
    v,k,t=(w[n] for n in ('v','k','t'))
    if any(type(x) is not int for x in (v,k,t)) or not 1<=t<=k<=v:raise ValueError('invalid JSON parameters')
    if expected is not None and (v,k,t)!=tuple(expected):raise ValueError('JSON instance mismatch')
    blocks=w['blocks']
    if not isinstance(blocks,list) or any(not isinstance(b,list) or any(type(x) is not int for x in b) for b in blocks):
        raise ValueError('JSON blocks must be integer lists')
    if expected_blocks is not None and len(blocks)!=expected_blocks:raise ValueError('JSON count mismatch')
    matrix_path=Path(matrix_path);matrix_path.parent.mkdir(parents=True,exist_ok=True)
    matrix_path.write_text('\n'.join(' '.join(map(str,b)) for b in blocks)+'\n')
    command=[str(Path(executable).resolve()),str(v),str(k),str(t),str(len(blocks)),str(matrix_path)]
    result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode:raise ValueError(result.stderr.strip())
    checked=json.loads(result.stdout)
    if any(checked[n]!=w[n] for n in ('v','k','t')) or checked['blocks']!=len(blocks) or not checked['valid']:
        raise ValueError('native result identity mismatch')
    return {**checked,'witness_sha256':hashlib.sha256(raw).hexdigest(),'matrix_sha256':hashlib.sha256(matrix_path.read_bytes()).hexdigest(),'command':command}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witness',type=Path)
    p.add_argument('--checker',type=Path,required=True);p.add_argument('--matrix',type=Path,required=True)
    p.add_argument('--instance',nargs=3,type=int);p.add_argument('--blocks',type=int);a=p.parse_args()
    print(json.dumps(check_native(a.witness,a.checker,a.matrix,a.instance,a.blocks),sort_keys=True))


if __name__=='__main__':main()
