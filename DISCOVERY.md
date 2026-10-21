# Research question and evidence

Current contributor instructions: [CONTRIBUTOR_WORKFLOW.md](CONTRIBUTOR_WORKFLOW.md) (21 October 2026).

**Follow-up evidence (20 October 2026):**
[`research/frontier-sprint/README.md`](research/frontier-sprint/README.md) supplies
the current-record audit, focused stronger-search experiments and launch assessment.
The successor's public ordinary count export is now accessible through the web
reader. All three earlier large archive improvements have already been surpassed.
Active catalogue revision 3 supersedes the attack priorities and weights below. Original
accepted rows, exact verifier and historical results remain unchanged.

The follow-up found author-checked proposals C(48,9,3)<=272 and C(90,12,3)<=678,
below the audited published 273 and 679. Its scientific-fit recommendation is
LAUNCH for the larger t=3 track. The proposals require separate review; this does
not open donor intake, approve publication, or change the accepted frontier.

Minimize |B| for B a family of distinct k-subsets of {1,...,v} with every t-subset
contained in at least one block, 1 <= t <= k <= v, multiplicity requirement one.
The optimum is C(v,k,t). Repeated blocks can always be removed, so restricting
witnesses to simple families loses no optimal construction. No comparison or
aggregate score across distinct triples has mathematical meaning here.

Progress, in order: (1) an exactly verified smaller witness for a dated, audited
cell; (2) a rigorous stronger lower bound with proof; (3) a source-backed correction
or independent replication. Search speed and a smaller heuristic defect alone
are not record improvements. Verification profile: exact certificate. Lower-bound
arguments require their own proof review; this pilot provides no formal proof kernel.

The user supplied the objective and (originally) LOCAL scope explicitly. The operational
interpretation and evidence standard are recorded in `docs/BRIEF.md`; no additional
interview was needed to invent or approve governance choices.

# Frontier and sources

`discover/active-frontier.json` exposes the known (48,9,3) 272-block and
(90,12,3) 678-block proposals for new work, with reproduced lower bounds 224 and
548. The public ordinary-count export viewed on 21 October lists 273 and 679.
These comparisons need separate literature/propagation review before novelty
acceptance. The original five rows in `data/records.json` remain historical
archive controls. Only C(7,3,2)=7 is settled there.

# Bottleneck

The current bottlenecks are source authority, independent scientific review,
obtaining current-count witnesses for six shortlisted cells, and testing new
registered work units against strong inherited starts. Existing local proposals
are known even before acceptance. An archive warm start worse than the live count
is not a ready ordinary search task.

The active catalogue weights are search 35, lower-bound tracing 20,
construction/source audit 20 and independent verification 25. It has two concrete
search cells, six retrieval cards, one bound trace and two verification cards.
Consult the existing experiment ledger before registering disjoint deletion
clusters; UNKNOWN and restricted neighborhood exclusions are not global bounds.

# Settled and excluded claims

C(7,3,2)=7 is settled by the supplied witness and counting. Do not attack it.
Historical purported C(14,7,3)<=14 and C(30,15,4)<=30 are listed as unsupported in
Gordon's errata; don't inherit either as a construction. A historical optimality mark
on a 47-block (14,5,3) cover was erroneous. The errata distinguish an incorrect bound
from an unconstructed one; the pilot does not supply the outside proof for (14,7,3).

A failed greedy restart, restricted local neighborhood, cyclic search, or timed-out
solver establishes nothing about the unrestricted minimum. Restricted-family
exclusions must say exactly which family they exclude. Asymptotic existence results
for fixed k,t and v tending to infinity do not determine these small cells.

# Review, credit, and coordination

Maintainer: @Mister-Meeseeks (from 2026-10-21); review capacity `surge`. Original
material is MIT-licensed; credit is in `discover.json`. See `docs/GOVERNANCE.md`.
Preserve source authorship and contributors' witness/algorithm provenance. No
co-authorship or acceptance is promised. LJCR excerpts keep their existing CC BY 4.0
license and attribution; that is separate from a license for this pilot's code.

A future acceptance procedure should check the exact instance, value, witness hash,
full coverage, incumbent comparison, and source/novelty audit; a separate reviewer
should rerun the verifier and audit lower-bound arguments. Do not label a result
maintainer-reviewed or independently-checked now. Record proposed checks in
`discover/verifications/`, identified by commit and scope. There's no automated
acceptance. Coordination is on GitHub Discussions (since 2026-10-21): claims,
findings and handoffs in [Handoffs](https://github.com/discoveryathome/covering-design/discussions/3), proposals in [Proposals](https://github.com/discoveryathome/covering-design/discussions/4),
retrospectives in [Feedback](https://github.com/discoveryathome/covering-design/discussions/5).

The verifier and frontier deserve the most careful review; future review capacity,
not donated compute, will determine the project's pace.
