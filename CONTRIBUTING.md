# Local research packages

No contribution intake is open. For an authorized local experiment, create
`research/<task-id>/` and include a short report, instance triple, baseline commit,
input/witness SHA-256 values, code changes, seed, command, budget, and checker output.
A valid construction must use integer labels 1..v and contain only distinct k-blocks.
The following checks must all pass before proposing a record change:

```sh
python3 -m covering.verify research/TASK/witness.json --instance V K T --blocks B
python3 -m covering.reproduce
```

Replace V K T B with the actual claim. A smaller B must beat the **audited current
incumbent**, not merely this pilot's weak greedy baseline. Keep old provenance and
the selected lower bound. Recheck successor sources before claiming novelty.
Lower-bound packages need a complete written proof, theorem hypotheses, or an
independently replayable exhaustive proof certificate for the unrestricted model.
Search failure is not a lower-bound certificate.

Prepare local findings and handoffs as prose ending with a v0 `discover` JSON block;
use the actual base commit, UTC timestamp, and `evidence_level: local-only`.
No maintainer, license, credit, publication, or acceptance commitment is implied.
