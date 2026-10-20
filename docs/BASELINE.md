# Seeded baseline

The generator builds all candidate k-blocks and subset incidence masks. At each step
it selects a maximum uncovered-gain block with uniformly seeded random tie breaking.
After coverage, it visits selected blocks in a seeded shuffled order and removes
redundant ones. Eight restarts use a single `random.Random(20261020)` per instance;
ties among equally short results are resolved lexicographically. Instances run
independently with the same specified seed. Deterministic iteration order does not
depend on set hashing. This is a small reference baseline, not a competitive
annealing implementation or a claim about the greedy heuristic's limit.

```sh
python3 -m covering.baseline --seed 20261020 --restarts 8 --output-dir scratch/baseline
```

| Instance | Candidate blocks | Required subsets | Best of 8 | Archive | Difference |
|---|---:|---:|---:|---:|---:|
| (7,3,2) | 35 | 21 | 7 | 7 | 0 |
| (14,5,3) | 2,002 | 364 | 51 | 43 | +8 |
| (15,5,3) | 3,003 | 455 | 64 | 55 | +9 |
| (16,5,3) | 4,368 | 560 | 77 | 65 | +12 |
| (13,6,3) | 1,716 | 286 | 24 | 21 | +3 |

All output witnesses are in `witnesses/baseline/`; `summary.json` records the Python
version, seed, restart counts, per-restart sizes, and independent check status.
The complete run was repeated and witness bytes compared; see
`results/baseline-determinism.txt`. No record improved. Starting repair search from
the archive is more informative than celebrating improvements over this baseline.
The built-in pool limits prevent accidental enumeration of a very large instance.
No wall-time performance claim is made; other workload on the machine was not
controlled and this is not a benchmark harness.
