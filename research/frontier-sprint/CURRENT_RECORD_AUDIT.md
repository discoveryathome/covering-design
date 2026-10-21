# Current-record audit — 20 October 2026 UTC

All three earlier witnesses are mathematically valid improvements of the frozen
La Jolla archive. **None improves the currently published successor count.**
Accepted pilot records and historical evidence have not been changed.

**New results from this follow-up:** weighted-search continuations produced
272 blocks for (48,9,3) and 678 for (90,12,3). Both passed the original
containment verifier, the separate Python rank checker and the native matrix
checker. The public export was queried again after discovery and still returned
273 and 679; the pinned October 19 ledger agrees. Exact-number literature searches
found no earlier 272 or 678 constructions, but absence from an index is not a
novelty proof. These are **proposed new best-known constructions relative to the
audited published frontier**, pending separate review. They are not accepted
frontier updates or unconditional world-record announcements. See
`proposal-records.json` and the exact witness checks.

| Cell | Frozen LJCR | Our earlier witness | Current published upper bound | Our excess over current |
|---|---:|---:|---:|---:|
| C(92,7,4) | 132,580 | 131,122 | 129,738 | 1,384 |
| C(75,10,5) | 166,799 | 166,692 | 166,568 | 124 |
| C(81,11,5) | 148,763 | 148,511 | 148,485 | 26 |

The current counts come from the [Covering Repository ordinary-covering export](https://coveringrepository.com/download_archive_vkt.aspx),
linked from its [download page](https://coveringrepository.com/download.aspx).
Selected numerical facts and source line numbers are saved in
`data/current-selected-counts.json`. This is a selected transcription from the web
tool's text/plain representation, not a hash-certified raw download of the complete
export. Direct urllib requests returned HTTP 403. The export contains **counts**,
not block witnesses or lower-bound proofs. Its values were checked against the
ordinary m=t rows; generalized lottery-covering records were excluded.

The public Chrome search form independently displayed:

* (75,10,5,5): 166,568; Evandro De Simone; 2 June 2026; no construction method
  supplied in the visible notes; [history identifier 114565](https://coveringrepository.com/history.aspx?id=114565).
* (81,11,5,5): 148,485; system-account construction; 18 September 2026;
  dynamic programming; [history identifier 114635](https://coveringrepository.com/history.aspx?id=114635),
  [free witness link](https://coveringrepository.com/download_system.aspx?id=220499).

These observations are also recorded in `experiment.json`. History pages were not
retrieved. A free-witness browser download timed out, and subsequent browser tabs
could no longer attach. No login, paid access, access-control bypass, or contact
with repository authors was attempted. Thus the **numeric novelty question is
resolved**, while independent validation and detailed attribution of the successor
witnesses remain unfinished. We do not claim to have checked their block arrays.

## Automatic propagation

For two new points, a (v-2,k,t) cover together with a (v-2,k-2,t-1) cover whose
blocks receive both new points gives a (v,k,t) cover. A required t-set either uses
no new point, or its old points extend to a (t-1)-set covered by the second source.
This is a standard synthesis from existing covers, consistent with the combination
methods in Gordon, Kuperberg and Patashnik, *New constructions for covering designs*,
[Section V](https://arxiv.org/html/math/9502238).

`data/current-parent-counts.json` records the corresponding current source counts:

| Derived cell | Current source arithmetic | Consequence |
|---|---|---|
| (81,11,5) | C(79,11,5) <=128,314; C(79,9,4) <=20,171; sum=148,485 | Exactly the displayed DP count. The first source improved by 26; our earlier recipe used 128,340. No new source construction arose here. |
| (75,10,5) | C(73,10,5) <=143,408; C(73,8,4) <=23,207; sum=166,615 | Even the same recipe with fresh parents already beats our 166,692. De Simone's published 166,568 is another 47 better; its method remains unspecified here. |
| (92,7,4) | One-point sum C(91,7,4)+C(91,6,3) <=123,257+6,764=130,021 | Our frozen-parent 131,122 is stale; the current displayed 129,738 is stronger still. Its precise recipe was not retrieved. |

These are conditional arithmetic audits of published parent counts, not newly
materialized successor witnesses. The earlier package retains full independent
coverage checks of its own parents and all three complete derived witnesses.

The repository's [automated-construction policy](https://coveringrepository.com/about_sums.aspx)
explicitly supports updating derived records when components improve. Its dates
are internally unusual: effective 11 August 2026, last updated 11 July 2026.
The policy also explains component-dependent free access and system attribution.
Therefore source optimization is the useful research action; routine descendants
must be recorded as consequences of that source result, not independent wins.

## Other sources and recent work

[Numaro report NUMARO-2026-006](https://numaro.tech/research/covering-designs-la-jolla-2026/)
(3 July 2026) already gives the same 131,122 construction. Its comparison is dated
and it disclaims current-record status; it does not establish novelty for our other
two witnesses. Its reported annealing/CP-SAT failures are further evidence against
starting donors with unstructured search on mature small cells.

A substantially newer primary source is Wynand van Staden's
[weighted-local-search project](https://github.com/WynandVStaden/covering-design-records),
pinned here to [970a68752d01ca5aa04129bebbb92e1b268c947e](https://github.com/WynandVStaden/covering-design-records/tree/970a68752d01ca5aa04129bebbb92e1b268c947e),
19 October 2026, 18:18:38 UTC. The pinned ledger reports 416 ordinary records and
75 generalized records. Only ordinary entries enter this audit. Indexed GitHub
pages showed older totals (185/401), so they were superseded by the pinned files.
The author's ledger and performance claims have not all been independently
audited. The eight selected ordinary counts agree with the successor export.
Code and provenance were read before sandboxed execution; the small MIT-licensed
search source and its license are retained in `tools/vendor/`. No external batch
script or external verifier was executed.

The older multilevel-search literature includes Dai, Li and Toulouse,
*A Cooperative Multilevel Tabu Search Algorithm for the Covering Design Problem*,
EA 2005, pp.119–130, [DOI 10.1007/11740698_11](https://doi.org/10.1007/11740698_11)
and the [author-hosted technical report](https://w1.cirrelt.ca/~toulouse/CD-BL-MT.pdf).
The latter's text extraction is damaged; no uninspected numerical table from it
was promoted to a bound. Horsley and Singh's [2017 lower-bound paper](https://arxiv.org/html/1706.06825v2)
is a proof-tracing lead; we have not assumed its hypotheses apply to every target.
Searches for recent ordinary-covering papers and the exact two large improvements
found no stronger source than the active export. This is not a comprehensive
literature-completeness proof.

## What a reviewer still needs

1. Reopen the public ordinary m=t table, date the observation and retain a permitted
   snapshot of each candidate's count, attribution, history and downloadable file.
2. Obtain the current block arrays, using the free link where supplied or another
   permission-compatible public source. For non-free witnesses, record the access
   limitation; do not substitute an old cover while labeling it the current witness.
3. Check every candidate against the latest export and relevant source publications
   again at review time. Verify complete coverage separately. For DP entries, pin
   the actual parent witnesses and recipe; an inferred numeric sum is insufficient.
4. Trace reported stronger lower bounds to their proofs. Upper-bound witnesses,
   repository lower columns, and locally replayed counting bounds are different
   evidence. No world-record or unrestricted optimality claim is made in this sprint.

For the 272 proposal specifically, elementary neighboring recipes do not explain
it: the current (48,8,3) cover has 349 blocks, the (49,9,3) cover has 309, and
deriving through a point of the (49,10,4) 1,793-block cover gives the ordinary
averaging bound floor(10*1,793/49)=365. One-point synthesis uses a (47,9,3)
253-block source plus a (47,8,2) source needing at least 42 blocks by counting,
so even that optimistic sum exceeds 272. Two-point synthesis similarly gives at
least 246+53=299 with the published (46,9,3) source. These are checks of specified
recipes, not an exhaustive audit of every algebraic or DP construction. The
272 witness itself was obtained by direct weighted search, not by propagating
an unchanged archive source.
