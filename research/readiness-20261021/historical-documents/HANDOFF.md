# Local handoff

**Latest continuation:** [frontier-sprint handoff](research/frontier-sprint/HANDOFF.md)
supersedes the search priorities below. It contains two exactly verified proposed
improvements to the audited current frontier, eight live-source targets, completed
finite repair censuses and a LAUNCH recommendation for scientific fit. Accepted
records and governance remain unchanged; separate review is pending.

**Later evidence:** the [initial sweep](research/initial-sweep/REPORT.md) supersedes
the exploratory attack priorities below for launch planning. Original records and
governance status remain unchanged.

The pilot is ready for local review and bounded experiments. It is not ready for
donor intake or publication. Run `python3 -m covering.reproduce` from this directory.
Read `docs/LITERATURE.md` before treating any archive target as a current record.

| Priority | Cell | Concrete attack | Why it is useful | Principal limitation |
|---|---|---|---|---|
| 1 | (14,5,3) | Repair 43-block archive cover toward <=42; fixed seed and 10-minute experiment | 2,002 candidate blocks, six-block gap to reproduced bound | Generic greedy is still eight blocks worse; improvement is not assured |
| 2 | (16,5,3) | Repair or anneal from 65 toward <=64 | 4,368 candidates, four-block gap | Greedy's 77 is far above incumbent; first calibrate on archive |
| 3 | (15,5,3) | Find a 54-cover or build a proof-capable unrestricted exclusion model | One-block gap, 3,003 candidates; any 54-cover must have point degree 18 | Can be difficult; restricted or timed-out searches do not settle it |
| 4 | (13,6,3) | Trace the reported lower bound 20, then test a 20-block construction | Smallest research pool, 1,716 blocks; archive range 20..21 | Only lower bound 18 was proved/recomputed in this pilot |
| Control | (7,3,2) | Regression only | Seven Fano lines prove the optimum seven | No room for improvement |

The four catalogue tasks cover search, lower bounds, archive/current-record audits,
and independent verification. All first_step commands have been run; transcripts
are under `results/`. No task reservation, public claim, remote, push, or hub
application exists. The listed priority order is editorial judgment about short
experiments, not a randomized task draw or a tractability guarantee. Future task
picks must use executed randomness and save the seed.

The full record replay checks all stored witnesses and verifier controls. A repeated
seeded run produced byte-identical baseline witnesses. This is **author-checked**;
another contributor must still inspect both checker and mathematical lower bounds.
Per-row source links, hashes, and byte ranges make the claimed upper bounds cheap
to check. The more conservative bound column prevents untraced archive metadata
from being mistaken for a local proof.

Pending decisions: consenting maintainer, review capacity, original code/text license,
credit policy, canonical public home, publication, and any eventual hub consent.
The manifest intentionally fails the schema's nonempty-maintainer rule. The LICENSE
notice grants no license for original pilot material. A future maintainer should
review the verifier and frontier most carefully; review capacity will set the pace.

Picker smoke-test seed: `3dea6ad0da2a3d63247b45f5a4d24b12`; drawn task `verify-independently`, row `(14,5,3)`. This draw is not a reservation. The payload below is local only; no posting destination is authorized.

```discover
{
  "v": 0,
  "kind": "handoff",
  "task": "verify-independently",
  "scope": "Independent audit of five covering-design records; seeded picker example draws (14,5,3).",
  "base": "2f320f8d1193bf4ae238b2fae3a9221fe1ae6228",
  "posted_at": "2026-10-20T04:56:54.834271Z",
  "evidence_level": "local-only",
  "priority_revision": 1,
  "request": {
    "question": "Can a separate reviewer reproduce the five records and independently check the verifier, starting with C(14,5,3)?",
    "first_step": "python3 -m covering.records check_row --v 14 --k 5 --t 3",
    "success_test": "All five witnesses and negative controls agree with a separately authored checker; record actual commit and hashes. No independent-review label until a separate reviewer completes it.",
    "track": "independent-verification",
    "est_minutes": 60
  },
  "seed": "3dea6ad0da2a3d63247b45f5a4d24b12"
}
```
