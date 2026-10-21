# Experiments and replay contract

Run commands from the pilot repository root. All new search outputs are local
proposals. Do not edit `discover/frontier.json` or the historical packages.

## Exact incumbent repair

`tools/repair.py` keeps the surviving incumbent blocks fixed. After deleting r
blocks, let H be the t-sets no longer covered by survivors. A repair needs at most
r-1 k-blocks covering H; no constraint on already-covered sets is necessary.

For r=3, every feasible pair has a block A containing the first hole. Enumerate
every k-set extending that hole. For each A, form the union U of points in all
holes not contained in A. A second block exists exactly when |U|<=k. Extending U
to size k yields a replacement. This is a complete finite 3-for-2 search, rather
than a random local-search failure. An empty residual needs no additional block.

For larger repairs the Z3 encoding has r-1 rows of v Boolean point memberships,
exactly k true values per row, and an OR of containment conditions per hole.
Increasing numeric block masks break only permutation symmetry between replacement
blocks. A solution using fewer blocks can be padded to distinct k-blocks, so this
does not lose an improvement. Saved candidates are deduplicated before independent
verification. Z3's [official Python API](https://z3prover.github.io/api/html/namespacez3py.html)
documents the pseudo-Boolean operations used here. Installed version: 5.1.0.

The master seed is `4ab3d4d0142a4bb506f6bea2245d1be4`, drawn with the OS random
generator. Per-cell seeds use the leading 32 bits of SHA256(master:triple).
Three complete 3-for-2 censuses, 32 sampled 4-for-3 repairs per cell, and 64 sampled
6-for-5 repairs per cell were run. After the small calibration, a complete 5,985-row
4-for-3 census was run for (13,6,3). Every row archives deletion indices, number
of holes, solver status, timing and any candidate; input witness hashes are fixed.
Each SMT call has a 5,000ms solver timeout. UNKNOWN remains unresolved.

Example (choose a new output filename for an intentional replay):

```sh
python3 research/frontier-sprint/tools/repair.py \
  research/initial-sweep/data/archive-13-6-3.json /path/to/new-results.json \
  --seed 4ab3d4d0142a4bb506f6bea2245d1be4 --remove 4 --trials 0 --timeout-ms 5000
```

The output's parent directory must have a sibling `witnesses/` directory if a
candidate is found. Supplied package structure already provides one. Replay in a
new copy or a workspace-scoped experiment directory; existing result files are
never overwritten.

## Separate neighborhood checker

`tools/check_neighborhoods.py` imports no search code. It enumerates all k-sets and
builds bitsets of which candidates cover each hole. To test two replacements, it
chooses one covering the first hole and intersects candidate-coverer bitsets for
every remaining hole. An empty intersection excludes that first choice. The
three-replacement checker branches once more and uses the two-replacement test.
Its holes are recomputed by direct containment in surviving blocks, independently
of the search's owner masks. Full 3-for-2 replays check the exact deletion-set
cardinality and uniqueness, binding the entire neighborhood to the witness hash.

```sh
python3 research/frontier-sprint/tools/check_neighborhoods.py \
  research/frontier-sprint/results/13-6-3-r3.json \
  --output /path/to/new-check.json
python3 research/frontier-sprint/tools/check_neighborhoods.py \
  research/frontier-sprint/results/13-6-3-r4-all.json \
  --larger-limit 5985 --enumerate-three --output /path/to/new-check.json
python3 research/frontier-sprint/tools/controls.py
```

Controls compare all 1,024 hole families on (5,3,2) with brute-force replacement
pairs/triples, and both SAT encodings against exact small cases with budgets 2,3,4.
There are positive and negative cases. The alternative all-k-set Z3 encoding
timed out on its six larger control replays; those UNKNOWNs establish no exclusion.
The combinatorial checker was therefore used for finite exclusions where practical.
These are separately implemented checks by the same authoring session. No
separate-contributor review or formal proof-kernel validation is asserted.

## Weighted-search frontier experiment

The audited October 2026 method at
[van Staden's pinned source](https://github.com/WynandVStaden/covering-design-records/tree/970a68752d01ca5aa04129bebbb92e1b268c947e)
uses persistent weights on uncovered t-sets, tabu point swaps, incremental move
scores, and repeated shrinking of complete covers. These features address the
unweighted fixed-size repair stagnation observed in the initial sweep. Its full
candidate block universe is implicit, making large-v t=3 cells tractable.
This sprint exercises that published method; it does not claim to invent it.

Only `wls2.cpp` is compiled, with its original MIT notice retained alongside it.
`-DCHECK` additionally recomputes coverage and incremental scores every 5,000 moves.
There are no network calls in this executable. Readable source inspection preceded
execution under the existing workspace OS sandbox.

```sh
clang++ -O3 -std=c++17 -DCHECK \
  research/frontier-sprint/tools/vendor/wls2.cpp -o /path/to/wls2-check
python3 research/frontier-sprint/tools/wls_trial.py /path/to/wls2-check \
  research/frontier-sprint/data/archive-48-9-3.json /path/to/new-trial \
  --seconds 360 --seed 287374570 --comparison 273
```

On macOS the actual runs wrapped commands in `sandbox-exec -f` with the existing
`session-covering-design/sandbox.sb`; compilation used a workspace TMPDIR. Adapt
this OS-level confinement to the donor host. Repository scripts do not grant
permission to broaden filesystem or network access.

Three targets received 360 seconds each from exactly verified archive witnesses,
then one fixed 720-second continuation from their own first-stage best witnesses.
The target/method change followed discovery of the new source and is explicitly an
adaptive second phase, not a prospectively randomized donor trial. Its seeds,
budgets and stopping rule were archived before reviewing continuation results.
The raw command arrays, executable hash, input/output hashes, all complete covers
and console logs are under `results/wls-*/`. Every complete saved cover passes the
separate rank checker. Wall-budgeted paths can differ across machines even with
fixed seeds. Preserve the exact output as evidence, not a promise of identical
heuristic trajectories. The three processes and checkers shared machine load;
their elapsed times are not controlled speed comparisons.

## Interpreting outcomes

A complete cover proves an upper bound, not novelty or optimality. A smaller cover
than the frozen archive can still be above, or equal to, the current successor.
The candidate must beat the smaller of the audited successor count and any stronger
published construction; then it needs a fresh literature/propagation review.
Finite neighborhood exclusions apply only to the supplied cover and exact move
radius. Timed-out or failed heuristic runs are bounded measurements, not proofs of
nonexistence. A sequence of equal-size moves followed by improvement, or a different
incumbent, lies outside a strict one-step deletion census.
