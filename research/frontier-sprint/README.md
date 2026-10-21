# Follow-up sprint: live-frontier experiment

**Recommendation: LAUNCH for scientific fit, centered on larger t=3 source cells.**
Two proposed constructions beat the audited current published counts and are
exactly verifiable. Separate review, maintainer, original-material licensing and
publication remain pending. Nothing was published or accepted into the main table.

| Cell | Archive warm start | Six-minute result | Twelve-minute continuation | Audited published count | Classification |
|---|---:|---:|---:|---:|---|
| C(48,9,3) | 292 | 273 | **272** | 273 | Proposed A; separate review pending |
| C(70,12,3) | 352 | 340 | 338 | 337 | C: historical-only improvement |
| C(90,12,3) | 704 | 679 | **678** | 679 | Proposed A; separate review pending |

The search used Wynand van Staden's pinned October 2026 weighted point-swap and
shrink method, with its internal exact score checks enabled. This is a source
construction search, not automatic propagation or another generic greedy sweep.
The published method is credited; no new algorithm is claimed. Every complete
output was checked independently of the search. The proposal witnesses also pass
the original direct-containment verifier and the native matrix checker.

The three earlier large archive improvements are all stale relative to the current
successor: (92,7,4) now lists 129,738; (75,10,5) 166,568; (81,11,5) 148,485.
The last count is exactly the same two-point recipe using a fresher source.
Their original witnesses, source histories and exact checks remain intact.

## Deliverables

* [Current-record audit and citations](CURRENT_RECORD_AUDIT.md).
* [Eight prioritized live-frontier cells](SHORTLIST.md) and the hash-bound
  [work table](data/shortlist.json). `research_upper_to_beat` includes local
  proposals, preventing rediscovery of our own unaccepted candidates.
* [Methods and exact replay commands](METHODS.md), fixed seeds/budgets in
  [experiment.json](experiment.json), and [nonduplication ledger](experiment-ledger.json).
* [Launch-readiness assessment and donor-yield accounting](LAUNCH_READINESS.md).
* [Updated five-card catalogue](../../discover/catalog.json), revision 2.
* [Two-row proposed record table](proposal-records.json) and its Discovery
  [record-table descriptor](proposed-frontier.json). The accepted frontier is unchanged.

## Check the results locally

From the repository root, no network or solver is needed to verify stored covers:

```sh
python3 -m covering.reproduce
python3 research/frontier-sprint/tools/replay.py
python3 research/frontier-sprint/tools/check_row.py --v 48 --k 9 --t 3 --proposal --direct
python3 research/frontier-sprint/tools/check_row.py --v 90 --k 12 --t 3 --proposal --direct
```

The first command preserves the original Fano/negative tests and five accepted
archive rows. The second checks all new saved complete covers, input/output hashes,
source comparisons, bound arithmetic and finite-result evidence bindings. It does
not rerun heuristic search or assert that a solver's UNSAT status is a formal proof.
The last two commands bind the exact proposed table row, witness and count, then
run the original containment verifier. `--proposal` is essential to select the
proposed table rather than the larger research shortlist.

Longer independent finite-exclusion replays and new search commands are in
[METHODS.md](METHODS.md). Z3 is needed only for new constraint search and its
encoding controls; the combinatorial neighborhood replay uses the standard library.
The published weighted search needs a C++17 compiler; its original MIT license is
in `tools/vendor/LICENSE`, separate from this pilot's pending original license.

## Exact negative results

| Pinned incumbent | Complete 3-delete / <=2-add census | Additional 4-delete / <=3-add result |
|---|---:|---|
| (13,6,3), 21 blocks | 1,330 exclusions | All 5,985 exclusions, independently replayed by combinatorial enumeration |
| (16,7,3), 24 blocks | 2,024 exclusions | 32 sampled exclusions, independently replayed by enumeration |
| (18,9,3), 16 blocks | 560 exclusions | 32 sampled SMT UNSAT results; no successful second-encoding replay |

Thus any <=20-block (13,6,3) cover can retain at most **16 of the 21 blocks**
of this particular incumbent: retaining 17 would give a 4-for-3 repair. This is
a useful finite overlap restriction, not a global lower bound. Analogous 3-for-2
results force a 23-block (16,7,3) cover to share at most 20 blocks, and a 15-block
(18,9,3) cover to share at most 12. Different incumbents and paths through equal-size
covers remain open.

The 64 sampled 6-for-5 trials per cell returned respectively 64 UNSAT; 8 UNSAT and
56 UNKNOWN; and 64 UNKNOWN. UNKNOWN is not an exclusion. Full details, including
the unsuccessful alternative SAT replay, are preserved rather than hidden.

## Handoff rules

Start with [HANDOFF.md](HANDOFF.md). Do not count the two proposals again as new
discoveries, and do not call all intermediate complete covers discoveries. Inspect
the experiment ledger before selecting a new scope. Six shortlist cells still
need a current-count witness; their archive warm starts are verified but weaker.
All checks here were run by one authoring session using separate implementations;
no separate-contributor review is claimed. The Discovery validation's sole expected
failure remains the empty maintainer list. All work is LOCAL.
