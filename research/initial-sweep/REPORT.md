# Initial sweep: launch readiness assessment

**The sweep found accessible archive-maintenance improvements, but did not establish an easy supply of new public construction records.** Keep generic small-cell search off the inaugural project's easy-wins promise. Construction propagation and witness audits are more promising introductory work, subject to a current-record audit.

## Results

| Experiment | Scope | Outcome |
|---|---|---|
| Seeded incremental greedy | 184 open archive cells, 2,943 restarts | No archive match or improvement |
| Archive-seeded deletion/repair | 20 cells, three 20-second seeds each | No smaller valid construction |
| Redundant-block audit | All 20 selected archive witnesses | No redundant block removed |
| Elementary construction audit | All 9,482 archive count entries | Four one-point arithmetic leads; eight two-point leads, with overlap |
| Materialized construction follow-ups | Three independent cells | Three fully verified archive improvements; one known replication, two with current status unconfirmed |

The closest greedy ratio was 17 blocks against 16 for (18,9,3). The median greedy result was 24.55% above its reported archive incumbent. None of these finite failed searches proves a cell is impossible or generally hard. Only 20 archived small witnesses and six large source witnesses were rechecked; the complete block archive was not downloaded.

| Cell | Frozen LJCR count | Verified construction | Reduction | Public-result status |
|---|---:|---:|---:|---|
| C(92,7,4) | 132,580 | 131,122 | 1,458 | Known July 2026 result reproduced |
| C(75,10,5) | 166,799 | 166,692 | 107 | Current incumbent/novelty unconfirmed |
| C(81,11,5) | 148,763 | 148,511 | 252 | Current incumbent/novelty unconfirmed |

Each row has its own witness, hash, and check_row entry in proposal-records.json and proposed-frontier.json. These are upper bounds, not optima, and they do not replace the main pilot frontier. Lower-bound columns use the conservative exact Schonheim recurrence; no new lower bound is claimed.

## What produced progress

The one-point construction combines the archived covers on (91,7,4) and (91,6,3). The two-point construction combines (73,10,5) with (73,8,4), and (79,11,5) with (79,9,4). All parent and resulting coverages were verified exactly. The three resulting witnesses cover respectively 2,794,155, 17,259,390, and 25,621,596 required subsets.

These are applications of known constructions. The opportunity came from a stale derived entry after source improvements, rather than inventing a new method. Five other two-point arithmetic leads remain unmaterialized; their larger verification requirements and current-record status need work. They are not counted as verified wins or an assured contributor queue.

A literature check found [Numaro's July 3, 2026 report](https://numaro.tech/research/covering-designs-la-jolla-2026/) of the same four one-point results. C(92,7,4) is consequently a replication. That primary report is cited for prior disclosure, not treated as a blanket verification of its other objects or experiments. Correct m=t successor queries were inaccessible, so we cannot announce any current world record. See SOURCE_AUDIT.md.

## Launch recommendation

The proposed small-cell search lane still carries a substantial risk of early contributors hitting a wall. A 20-second trial is shorter than a full donation session, but the absence of wins across many cells and seeds does not support an easy-record-breaking promise. Longer budgets or materially stronger algorithms may help; this sweep did not test that claim.

A construction-and-audit lane is more credible. It provides concrete objects to rebuild, contradictions or stale dependency edges to trace, and exact per-cell outcomes. Before presenting it as a discovery queue, establish dated current incumbents and identify multiple still-unclaimed improvements. A finite set of already-known archive corrections should be labelled replication work.

For the next preparation round, first audit current status of (75,10,5) and (81,11,5), then examine the remaining two-point leads and compositional verification for large cases. Do not spend another round merely increasing the same greedy restart count or repeating these exact repair budgets. If current sources already subsume those leads, lower this pilot's inaugural priority for quick research wins.

## Reproducibility and scope

Read METHODS.md, experiment.json, and results/summary.json. Per-cell data are in results/screen.csv; complete command vectors and seeds are in greedy.jsonl and repair.jsonl. All best complete trial witnesses were checked with the independent tuple-union verifier. Rank-based Python and native C++ checkers validate large constructions; small exhaustive comparisons, Fano, negative fixtures, and a large missing-branch rejection are included.

Recheck stored evidence from the repository root with:

    python3 research/initial-sweep/tools/check_package.py all

For faster large-object checks, compile tools/verify_matrix.cpp and pass --native-checker PATH --matrix-dir scratch/sweep/matrices. No committed binary or network access is required. Wall-time-limited searches need not replay byte-identically on another machine; their saved witnesses and counts do. Timings were not controlled performance benchmarks.

This is author-checked, local-only work. No independent contributor or maintainer has reviewed it. Governance and original-material licensing remain pending; no external repository, push, post, or hub action was taken.

```discover
{
  "v": 0,
  "kind": "finding",
  "scope": "184-cell greedy sweep and 60 archive-repair trials: no search wins; three exact archive construction improvements, one prior replication and two with unconfirmed novelty.",
  "base": "99fd9f56ffc290da88636819f8fed35a19465688",
  "posted_at": "2026-10-20T05:36:13.183007+00:00",
  "evidence_level": "local-only",
  "seed": "dfd378b39a602458ed164ae0ef63400e"
}
```
