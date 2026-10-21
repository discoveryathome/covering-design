# Prioritized live-frontier shortlist

These eight counts agree between the [successor's ordinary-covering export](https://coveringrepository.com/download_archive_vkt.aspx)
(accessed 20 October 2026) and van Staden's
[pinned October 19 ledger](https://github.com/WynandVStaden/covering-design-records/blob/970a68752d01ca5aa04129bebbb92e1b268c947e/RECORDS.md).
The incumbent method is **weighted point-swap local search with block shrinking
(wls2)** in all eight cases. These are direct source-covering improvements, rather
than merely new arithmetic consequences of old sources. Automatic descendants
should receive dependency credit and should not inflate the number of discoveries.

The order favors cheap exact verification, recent demonstrated movement and
available warm starts. It is a research-priority judgment, not evidence that another
improvement exists. Published lower bounds may leave considerable gaps even when
the incumbent is very difficult to beat. The incumbent has already been optimized
by the method we are calibrating; its past yield is not our expected future yield.

**Local proposals improve two rows:** (48,9,3) now has 272 blocks and (90,12,3)
has 678, versus published 273 and 679. Separate review remains pending. New
searches must beat **272 and 678**, respectively. `research_upper_to_beat` in
the JSON work table is the smaller of the published count and local witness count.

| Priority | Cell | Current upper | Lower: replayed / archive reported | Required subsets | Specific alternative attack |
|---|---|---:|---:|---:|---|
| 1 | (48,9,3) | 273 | 224 / 224 | 17,296 | Start from the local 272 proposal, target <=271; cluster blocks sharing private triples and repair several blocks jointly. Weighted one-point moves provide diversification. |
| 2 | (70,12,3) | 337 | 257 / 275 | 54,740 | Compare incidence profiles across distinct near-incumbents; repair clusters of private triples, rather than uniformly sampling deletion sets. First obtain or reproduce the 337-block witness. |
| 3 | (90,12,3) | 679 | 548 / 563 | 117,480 | Start from the local 678 proposal, target <=677; multi-block repair of high-overlap regions with survivor blocks fixed. Avoid enumerating all C(90,12) candidate blocks. |
| 4 | (48,11,3) | 142 | 127 / 127 | 17,296 | Compact source cover, only 15 blocks above the replayed bound. Test degree-aware joint repairs; first acquire the current witness, because the included archive cover has 150 blocks. |
| 5 | (54,13,4) | 666 | 536 / 536 | 316,251 | A recently improved t=4 source; use private-quadruple clusters and exact replacement, rather than a full candidate pool. Current witness must be obtained; archive warm start has 746 blocks. |
| 6 | (52,9,3) | 339 | 295 / 295 | 22,100 | Relatively small residual gap and fast checking; compare several nonisomorphic complete covers before launching exact repairs. Current witness missing locally; archive has 345. |
| 7 | (57,12,3) | 175 | 148 / 148 | 29,260 | Recent multi-block reduction suggests testing transitions between local minima using block-intersection clusters. Current witness missing locally; archive has 185. |
| 8 | (35,18,6) | 207 | 121 / 125 | 1,623,160 | Higher-risk control for complement/incidence structure: store complements of 18-blocks as 17-sets, and repair uncovered 6-sets with lazy constraints. Start with a tiny restricted neighborhood; full enumeration of k-blocks is unsuitable. Archive warm start has 223. |

The replayed bounds use integer-only Schönheim iteration, with the counting proof
already supplied in `../../docs/LOWER_BOUNDS.md`. For example,
L(v,k,t)=ceil(v/k L(v-1,k-1,t-1)), with L(v,k,0)=1. The archived lower columns
275,563,125 are stronger than that direct iteration; their original proof or
subparameter trace was not completed here. They remain **reported bounds**, not
newly proved bounds or optimum values. No claim is made that this audit found the
strongest lower bound in all literature.

`data/shortlist.json` binds every cell to its source, comparison count, local
witness, witness hash and check command. The three search targets have locally
generated near/current-incumbent witnesses; all eight archive warm starts were
exactly checked. A local witness with more blocks does **not** certify the
published smaller upper bound. Five unexercised successor witnesses and the still
unreproduced 337-block (70,12,3) cover are an onboarding limitation. Resolve these
six before assigning their search cards as current-incumbent starts.

## Verification cost

Every candidate is checked exactly, never by sampling. A rank-based checker marks
each t-subset of each block, requiring B*C(k,t) insertions and C(v,t) bytes plus
small bookkeeping. At the published counts the eight respective insertion counts
are 22,932; 74,140; 149,380; 23,430; 476,190; 28,476; 38,500; and 3,842,748.
These figures make seconds-scale checking plausible on an ordinary laptop; they
are operation counts, not measured timing promises. Our first three final witnesses
actually checked in approximately 0.01,0.04,0.12 seconds respectively under shared
load. The original direct-containment verifier is a slower second algorithm and
is retained for cross-checks. The higher-t cell has the most expensive verification
here, still far below a 30–60 minute donated session.

## Demoted small cells

(13,6,3), (16,7,3), and (18,9,3) remain legitimate mathematical questions, with
current published upper counts 21,24,16 confirmed in the public form. They are
**not recommended first-donor search targets** after this sprint. Their supplied
incumbents admit no strict 3-for-2 repair; see the complete censuses and separate
enumeration checks. The first also underwent a complete 4-for-3 census. These
results bind particular witnesses, not all nonisomorphic incumbents and not the
unrestricted covering numbers. Do not repeat the same neighborhoods under new
seeds, relabelings or block orders and call that new work.
