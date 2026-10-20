# Local handoff

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

The local handoff payload is appended after the evidence commit is created. It is
for local use only; no posting destination has been authorized.
