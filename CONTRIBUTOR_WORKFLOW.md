# Contributor workflow — 21 October 2026

Start with `python3 tools/pick_task.py`. The active catalogue is
`discover/active-catalog.json`; the original catalogue stays in the frozen sprint.
Two search-ready cells have complete, verified local witnesses: (48,9,3) with 272
blocks and (90,12,3) with 678. These are upper bounds, not proved equalities.
Target at most 271 or 677 respectively. Both proposals await scientific acceptance.

```sh
python3 research/frontier-sprint/tools/check_row.py --v 48 --k 9 --t 3 --proposal --direct
python3 research/frontier-sprint/tools/check_row.py --v 90 --k 12 --t 3 --proposal --direct
```

The public [ordinary-count export](https://coveringrepository.com/download_archive_vkt.aspx)
viewed on 21 October still lists 273 and 679. This is a source-relative comparison,
not a complete novelty or propagation audit. The historical commands deliberately
report their original 20 October audit date.

Six other shortlisted cells have weaker archive warm starts than their published
counts. They receive explicit witness-retrieval tasks, not routine search traffic.
Retrieve one current witness, verify coverage and attribution, and trace its parent
recipe before opening that cell to donors. A precise access blocker is a valid
handoff. Preserve Wynand van Staden's authorship of the weighted-search method.

For search, register the input hash and disjoint deletion clusters before a
20-minute capped experiment. Keep UNKNOWN and unsuccessful attempts. Consult the
existing ledger; the closed 3-for-2/4-for-3 neighborhoods are not fresh work.
Automatic propagation is a consequence of its source result, not multiple discoveries.

`python3 -m covering.reproduce` checks the original five-row record.
`python3 tools/replay_frontier_sprint.py` replays the sprint in a temporary copy
with hash-bound original documents. Its original manifest and verifier are unchanged;
current launch documentation is not substituted into historical evidence.

## Session receipt and review

Record the base commit, selected task and seed, input and output hashes, commands,
budget and elapsed time, successful and failed attempts, verification output,
and what remains unresolved. Check the live Handoffs Discussion before claiming
work. Post or open a focused PR only within the contributor's authorization.
A task draw is advisory; it does not reserve work.

A useful outcome can be a new witness, an independently checked result, a
source-backed correction, or a reproducible blocked handoff. Repeating a known
positive control is onboarding evidence. Review records must distinguish code
replay, independent implementation, scientific review and maintainer acceptance.

For the next monitored cohort, record cold-start orientation time, first useful
artifact, reviewer minutes, acceptance latency, duplicate work and unsuccessful
sessions. Later sessions inherit every known valid result. A lack of improvements
is evidence to revise the task pool, not a reason to reset it to weaker baselines.
