"""Independent exact verifier: enumerate every required subset and test containment.

No import of the generator, incidence masks, heuristic scores, or external libraries.
Witness labels are integers 1..v. Duplicate blocks are rejected (simple families).
"""
import argparse
import json
from itertools import combinations
from math import comb
from pathlib import Path


class Invalid(ValueError):
    pass


def parameters(v, k, t):
    if any(type(x) is not int for x in (v, k, t)) or not 1 <= t <= k <= v:
        raise Invalid("require integer parameters 1 <= t <= k <= v")


def verify(witness, expected=None, expected_blocks=None):
    if not isinstance(witness, dict):
        raise Invalid("witness must be a JSON object")
    try:
        v, k, t = (witness[n] for n in ('v', 'k', 't'))
    except KeyError as e:
        raise Invalid(f"missing parameter {e}") from e
    parameters(v, k, t)
    if expected is not None and (v, k, t) != tuple(expected):
        raise Invalid("witness parameters do not match requested instance")
    blocks = witness.get('blocks')
    if not isinstance(blocks, list):
        raise Invalid("blocks must be a list")
    if expected_blocks is not None and (type(expected_blocks) is not int or len(blocks) != expected_blocks):
        raise Invalid("block count does not match claimed value")
    family, seen = [], set()
    for i, block in enumerate(blocks):
        if not isinstance(block, list) or len(block) != k:
            raise Invalid(f"block {i}: require exactly {k} entries")
        if any(type(x) is not int or not 1 <= x <= v for x in block):
            raise Invalid(f"block {i}: labels must be integers in 1..{v}")
        b = frozenset(block)
        if len(b) != k:
            raise Invalid(f"block {i}: repeated point")
        if b in seen:
            raise Invalid(f"block {i}: duplicate block")
        seen.add(b)
        family.append(b)
    covered, missing, first_missing = 0, 0, None
    for subset in combinations(range(1, v + 1), t):
        if any(frozenset(subset) <= b for b in family):
            covered += 1
        else:
            missing += 1
            if first_missing is None:
                first_missing = subset
    if missing:
        raise Invalid(f"uncovered {missing}/{comb(v,t)} subsets; first={first_missing}")
    return dict(valid=True, v=v, k=k, t=t, blocks=len(family), covered=covered,
                required=comb(v, t), uncovered=0)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('witness', type=Path)
    p.add_argument('--instance', nargs=3, type=int)
    p.add_argument('--blocks', type=int)
    a = p.parse_args()
    try:
        result = verify(json.loads(a.witness.read_text()), a.instance, a.blocks)
    except (Invalid, OSError, ValueError) as e:
        p.exit(1, f"INVALID: {e}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
