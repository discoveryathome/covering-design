"""Seeded random-tie greedy set cover with reverse redundant-block deletion.

The generator uses bit masks; the verifier separately checks set containment.
This is a replication baseline, with no claim to record-quality performance.
"""
import argparse
import json
import random
from itertools import combinations
from math import comb
from pathlib import Path
from .verify import parameters


def greedy(v, k, t, seed=0, restarts=8):
    parameters(v,k,t)
    if type(restarts) is not int or restarts < 1:
        raise ValueError('restarts must be positive')
    if comb(v,k) > 200_000 or comb(v,t) > 20_000:
        raise ValueError('baseline limit: <=200000 candidates and <=20000 required subsets')
    subsets = {s: i for i, s in enumerate(combinations(range(1,v+1),t))}
    candidates = list(combinations(range(1,v+1),k))
    masks = [sum(1 << subsets[s] for s in combinations(b,t)) for b in candidates]
    full = (1 << len(subsets)) - 1
    rng, best, sizes = random.Random(seed), None, []
    for _ in range(restarts):
        uncovered, chosen = full, []
        while uncovered:
            best_gain, ties = -1, []
            for i, mask in enumerate(masks):
                gain = (mask & uncovered).bit_count()
                if gain > best_gain:
                    best_gain, ties = gain, [i]
                elif gain == best_gain:
                    ties.append(i)
            i = rng.choice(ties)
            chosen.append(i)
            uncovered &= ~masks[i]
        order = chosen[:]
        rng.shuffle(order)
        for i in order:
            union = 0
            for j in chosen:
                if j != i:
                    union |= masks[j]
            if union == full:
                chosen.remove(i)
        blocks = sorted(candidates[i] for i in chosen)
        sizes.append(len(blocks))
        if best is None or (len(blocks), blocks) < (len(best), best):
            best = blocks
    return {'v':v, 'k':k, 't':t, 'blocks':[list(b) for b in best],
            'provenance':{'method':'random-tie-greedy+redundancy-deletion-v1',
                          'seed':seed, 'restarts':restarts, 'restart_sizes':sizes}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--instance', nargs=3, type=int, required=True)
    p.add_argument('--seed', type=int, default=20261020)
    p.add_argument('--restarts', type=int, default=8)
    p.add_argument('--output', type=Path, required=True)
    a=p.parse_args()
    w=greedy(*a.instance,a.seed,a.restarts)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(w,indent=2)+'\n')
    print(json.dumps({'instance':a.instance,'blocks':len(w['blocks']),'output':str(a.output)}))


if __name__ == '__main__':
    main()
