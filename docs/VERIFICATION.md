# Exact verifier contract

A witness is a JSON object with integer `v,k,t`, a list of integer lists `blocks`,
and optional ignored provenance. It must have 1<=t<=k<=v. Labels are 1..v;
booleans and floating-point values are rejected. Each block has exactly k distinct
points. Duplicate blocks are rejected; sorting of points or blocks is not required.
Ignoring provenance never lets it influence the mathematical check.

`covering/verify.py` validates structure, then enumerates every t-subset of the
universe and tests its containment in the family using frozensets. It performs
no sampling and uses no floating-point arithmetic. It imports no search or mask
code. Missing subsets report their exact number and the first example. A record
check additionally binds (v,k,t), block count, local path, SHA-256, and the exact
computed bound to its row. Bad inputs and false claims exit nonzero.

```sh
python3 -m covering.verify witnesses/fano.json --instance 7 3 2 --blocks 7
python3 -m covering.verify tests/fixtures/missing-block.json
python3 -m covering.records check_row --v 15 --k 5 --t 3
python3 -m unittest discover -s tests -v
```

The second command must fail. Fixtures also include a repeated point, wrong block
size, out-of-range label, duplicate block, and boolean label. Test code covers
instance/count mismatches and invariance under relabelling and ordering, plus
edge cases t=1, k=t, k=v. A separate incidence-union oracle exhausts all 1,024
families on (5,3,2) and compares every accept/reject decision with the verifier.

The generator builds subset-indexed integer masks; its internal score is never
accepted as a covering certificate. Every saved baseline is passed through the
independent containment checker. Determinism is checked by rerunning the eight
restarts with seed 20261020 and comparing witness bytes. Python version is recorded;
stdlib PRNG behavior is not promised across all future Python versions.

The full `reproduce` command verifies the record and baseline witnesses, tests,
and hashed frontier artifacts. It does not rerun research or prove a stronger
lower bound than the documented recurrence. Typical selected-row and full-check
runs finish in seconds; large future instances may not. This session is
**author-checked** only. Algorithmic independence from search is not independent
review by another contributor and is not formal verification of this Python code.
