# Experiment design and limits

The launch question is whether short contributor-sized experiments can produce
visible, valid improvements. We do not infer tractability from a gap alone.

## Greedy screen

Select every open cell in pinned LJCR v1.2 satisfying all of:

- at most 150,000 possible k-blocks;
- at most 50,000 required t-subsets;
- at most 5,000,000 block/subset incidence entries.

There are 184 such cells, spanning t=2..8. OS randomness produced the master seed
in experiment.json; that seed shuffles the screening order. SHA-256 derives each
method/instance/trial seed. The engine builds all incidences, maintains uncovered
gain buckets, chooses a seeded maximum-gain block, and deletes redundant blocks.
Sixteen restarts were requested per cell, with a ten-second per-cell check and a
180-second global stage cap. The per-cell cap is checked between restarts, so a
single restart may overrun it. All 184 cells finished; 183 completed all 16 restarts
and one completed 15, for 2,943 total. The stage took 143.82 wall seconds on this
machine; this is a bounded feasibility observation, not a controlled speed benchmark.

## Archive-seeded repair

Choose 20 screened cells whose archive counts are at most 1,000: the ten closest
greedy/archive ratios, followed by the ten largest archive upper/reported-lower
ratios among remaining cells. Numeric tie-breaks and exact chosen rows are saved
in data/repair-selection.json. This selection happened before the repair results.
It covers both nearly matched baselines and larger gaps; neither category is
assumed easy.

Each starts from its exact verified archive witness. Remove one block and search
at fixed size. A move samples replacement blocks containing an uncovered subset,
samples blocks to remove, scores exact coverage-defect changes, and uses tabu and
annealing acceptance to escape plateaux. Complete covers alone may replace the
saved incumbent. Success permits another block deletion within the same budget.
Three independent derived seeds get 20 wall seconds each. The search-time ceiling
is 1,260 seconds for 1,200 seconds of planned repair trials; input-download waits
are excluded from this allowance. Exact iteration counts, final valid
count, attempted target, and best invalid defect are recorded for every trial.
The defect metric must never be called a valid construction or lower bound.

## Construction propagation

A separate all-9,482-cell audit checks elementary constructions from Gordon,
Kuperberg, and Patashnik, *New constructions for covering designs*, Sections V
and VI.1 (https://arxiv.org/html/math/9502238). This was a follow-up lead discovered
after the greedy screen, rather than part of its predeclared success metric.

For the one-point construction, keep a (v-1,k,t) cover and append the new point to
each block of a (v-1,k-1,t-1) cover. Every required subset either avoids the new
point or contains it, so their union is a cover. The two-point variant combines
a (v-2,k,t) cover with a (v-2,k-2,t-1) cover whose blocks receive both new points;
subsets containing one or both new points are covered by the latter branch.

Arithmetic audits are conditional on source witnesses and current-record checks.
Materialized results have parent hashes, a complete resulting witness, and exact
coverage checks. Other arithmetic leads are not counted as verified improvements.
No improved numerical lower bound is claimed.

## Independent checking and resource scope

The search engine represents subsets with 64-bit masks and internal IDs. The
Python sweep checker enumerates combinations of sorted block labels into a set
of tuples. The original pilot checker separately tests set containment for every
required subset. For large proposed constructions, the Python and C++ rank checkers
map a subset a_1<...<a_t to sum_i binomial(a_i-1,i) and require every rank to be marked.
These implementations import no heuristic masks or incidence arrays.

The rank formula is bijective: subsets with maximum a_t=m have ranks starting at
binomial(m-1,t), followed by all ranks of their (t-1)-subsets on m-1 points.
Induction and Pascal's identity give precisely 0..binomial(v,t)-1. Thus a complete
marked byte array proves coverage, rather than sampling it. Structure, integer
labels, duplicate points/blocks, expected parameters, and claimed sizes are also
checked. Full proof formalization and separate-contributor review remain pending.

Wall-limited repairs can take different paths on a different machine because they
execute different numbers of moves. Seeds alone do not guarantee identical final
results for these timed trials. Included witnesses and their scores are exact and
can be replayed independently. Other machine workload was not controlled; do not
compare these timings as a performance benchmark. The sweep's finite failures
prove no impossibility and cannot assess every parameter region or search method.

Repair witness envelopes were normalized after the trials to state archive
attribution and whether the incumbent stayed unchanged. Raw engine envelope hashes
are retained; block arrays were not altered. Source snapshots named *-used-v1
preserve the executed engine and driver.
