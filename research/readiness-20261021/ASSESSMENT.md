# Readiness assessment — covering-design — 21 October 2026

Recommendation: **Second anchor, with a deliberately limited search pool**.

Two strong proposals were available, but historical metadata remained the default frontier. The launch documentation changes also broke the frozen sprint manifest. Six other shortlisted cells lack witnesses matching their published counts.

## Completed changes

- Added an active frontier exposing the known 272- and 678-block proposals as working upper bounds, preserving their unaccepted evidence status.
- Added an active catalogue with separate search tasks for the two ready cells and six explicit retrieval tasks for gated cells; original catalogue and evidence bindings are untouched.
- Preserved hash-verified original documents and added an isolated historical replay, so launch documentation can evolve without weakening the original integrity checks.

## Validation

Original five-row verifier/tests passed; full sprint replay checked 88 witnesses and bound the recorded 9,931 finite-neighborhood decisions (not a fresh exhaustive rerun of all neighborhoods); direct coverage checks passed for both proposals; 120 picker draws and schema validation passed.

All 11 active task cards' first-step commands passed; repeated identical commands were cached within the check.
Executed outputs are in [checks/](checks/). This is coordinator review and replay,
not an independent cold contributor study or external scientific signoff. No new
research-success rate is inferred. Current workflow: [CONTRIBUTOR_WORKFLOW.md](../../CONTRIBUTOR_WORKFLOW.md).

## Next scientific handoff

A separate scientific reviewer must inspect both witnesses, attribution and a fresh source/propagation audit. Resolve the six current-witness retrieval tasks before broadening search traffic.

Acceptance test: Independent witness and novelty decisions scoped to the actual sources; current-count witness, provenance and parent recipe for each additional cell before activation.

```sh
python3 tools/replay_frontier_sprint.py
python3 research/frontier-sprint/tools/check_row.py --v 48 --k 9 --t 3 --proposal --direct
python3 research/frontier-sprint/tools/check_row.py --v 90 --k 12 --t 3 --proposal --direct
```

## Integration state

Base: `ace467620cec621405b6caf3fa3eab457f21d44f`. Remote main at fetch: `ce0d4a1b12470cefe4ba80fefa2079db483a4e0a`.
This work builds on the newer local launch/coordination branch. The existing
[launch PR #1](https://github.com/discoveryathome/covering-design/pull/1) was still open when
checked, and its Handoffs thread had no comments. Local launch decisions are not
proof that remote main or the public launcher has adopted them. No remote write,
merge, announcement, scientific acceptance or observation submission occurred.
