# Handoff: review two live-frontier proposals

The sprint recommends **LAUNCH for scientific fit on the larger t=3 track**.
This is a recommendation, not permission to publish, open intake or replace
accepted records. Maintainer, license, review capacity and publication remain pending.

Two local proposals beat the published counts audited on 20 October 2026:

| Instance | Proposed | Published comparison | Locally reproduced lower | Witness |
|---|---:|---:|---:|---|
| (48,9,3) | 272 | 273 | 224 | `witnesses/proposed-48-9-3-272.json` |
| (90,12,3) | 678 | 679 | 548 | `witnesses/proposed-90-12-3-678.json` |

Both passed direct containment, Python rank and freshly compiled native checkers.
No separate contributor has reviewed them. Fresh public export checks still showed
273 and 679 after discovery; the pinned October 19 source ledger agrees. Treat
novelty as relative to those audited published sources, with review-time refresh
required. Do not call either an unconditional world record or a proved optimum.

Run from the repository root:

```sh
python3 -m covering.reproduce
python3 research/frontier-sprint/tools/replay.py
python3 research/frontier-sprint/tools/check_row.py --v 48 --k 9 --t 3 --proposal --direct
python3 research/frontier-sprint/tools/check_row.py --v 90 --k 12 --t 3 --proposal --direct
```

`proposed-frontier.json` is a valid separate Discovery record-table descriptor,
with per-instance witnesses and `check_row` commands. `discover/frontier.json`,
`data/records.json`, original verifier/tests and all historical research are unchanged.
The original five-row table remains the accepted table. No remote action occurred.

The weighted experiment used the published wls2 implementation at
`WynandVStaden/covering-design-records@970a68752d01ca5aa04129bebbb92e1b268c947e`,
compiled with `-DCHECK`, following source inspection. Give its author credit for
the method and preserve the included MIT notice; this grants no license for
original pilot material. Three targets received 360+720 seconds each, fixed seeds
and saved traces. Final counts: (48,9,3)272; (70,12,3)338 versus published337;
(90,12,3)678. All complete outputs, not just the best ones, were exactly checked.

The three prior large proposals are historical-only gains: the successor now
lists (92,7,4)129738, (75,10,5)166568, and (81,11,5)148485. The last is exactly
our earlier two-point recipe with a newer parent. Their old witnesses remain valid.

Exact repair also supplied useful negatives: all 3914 three-for-two neighborhoods
across the three small incumbent witnesses are excluded. All 5985 four-for-three
neighborhoods of the supplied (13,6,3) cover were independently enumerated too;
any <=20-block cover must retain at most 16 blocks of that particular incumbent.
These exclusions do not prove a global bound or exclude paths through equal-size
covers. Sampled six-for-five UNKNOWNs remain unresolved. Consult the ledger before
choosing another seed or scope; closed neighborhoods are not fresh donor tasks.

The eight-cell shortlist is source-pinned, with verified archive warm starts for
all eight. Six cells still lack current-count witnesses. Assign search only after
that gate is resolved. Local targets to beat are now 272 and 678 for the two
proposals, even before acceptance; do not rediscover them. Catalogue revision2 has
five tasks covering structured search, relevant lower-bound tracing, current-witness
and propagation audits, and independent verification. A real random picker smoke
test is saved in `checks/catalog-picker.txt`; it is a suggestion, not a reservation.

Next reviewer: independently inspect the two complete block families, exercise
negative controls, refresh successor/literature comparisons and check the source
attribution. The follow-on eight-session evaluation and honest A/B/C/D accounting
are in `LAUNCH_READINESS.md`. No numerical donor success-rate promise is justified
by this selected sample. Verification is inexpensive; target selection and novelty
provenance deserve the most attention.

New work remains in the local working tree; the base commit and artifact hashes
pin the review state. `artifacts.sha256.json` binds the package and relevant root documents.
`checks/` contains replay, controls, native/containment outputs and expected
Discovery validation failure for missing maintainer consent. The quick replay
checks bindings; the longer independent neighborhood enumeration commands are in
`METHODS.md`. No UNSAT proof-kernel or separate-review certification is claimed.

```discover
{
  "v": 0,
  "kind": "handoff",
  "task": "verify-frontier-candidate",
  "scope": "Review two exact source-cover proposals below audited current counts; preserve all accepted records and LOCAL scope.",
  "base": "56a58d459f9d560e92995b14cd2141bdc18ea417",
  "posted_at": "2026-10-20T07:02:18.338653+00:00",
  "evidence_level": "local-only",
  "priority_revision": 2,
  "request": {
    "question": "Can a different reviewer validate both proposed witnesses, refresh novelty and propagation comparisons, and check attribution before any acceptance decision?",
    "first_step": "python3 research/frontier-sprint/tools/check_row.py --v 48 --k 9 --t 3 --proposal --direct",
    "success_test": "Two exact checks agree on each hash-bound witness, invalid controls fail, and dated source comparisons still exceed 272 and 678; record separate reviewer identity and actual review scope without assuming acceptance.",
    "track": "independent-verification",
    "est_minutes": 45
  }
}
```
