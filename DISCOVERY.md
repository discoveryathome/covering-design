# Research question and evidence

**Follow-up evidence (20 October 2026):**
[`research/frontier-sprint/README.md`](research/frontier-sprint/README.md) supplies
the current-record audit, focused stronger-search experiments and launch assessment.
The successor's public ordinary count export is now accessible through the web
reader. All three earlier large archive improvements have already been surpassed.
Catalogue revision 2 supersedes the attack priorities and weights below. Original
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

The user supplied the objective and LOCAL scope explicitly. The operational
interpretation and evidence standard are recorded in `docs/BRIEF.md`; no additional
interview was needed to invent or approve governance choices.

# Frontier and sources

See the five rows in `data/records.json`, table in README, and `docs/LITERATURE.md`.
Every row points to a concrete witness and SHA-256. Values 43,55,65,21 are verified
archive constructions, not proven optima. The Fano plane has seven blocks covering
all 21 pairs and meets the proved lower bound, hence C(7,3,2)=7.

The 2022 GitHub metadata and April 2026 Zenodo v1.2 agree on these selected counts.
LJCR was frozen in March 2026; the archive's existence is not evidence that its cells
remain current. The successor audit remains open because filtered pages were
inaccessible. Imported LJCR metadata report a stronger lower bound 20 for (13,6,3);
the table's bound is 18 until the stronger proof is traced and checked.

# Bottleneck

All block pools here have only 1,716–4,368 candidates, and verifying a witness is
cheap. Getting from generic greedy covers to the strong archive incumbents is the
search bottleneck. The baseline is deliberately modest. Coverage gaps do not imply
that an improved construction exists. Another bottleneck is tracing stronger bounds
and checking current records before investing compute.

The search track has weight 35, lower-bound tracing 25, archive/current-record audits
20, and independent verification 20. Each track has one concrete card and a working
positive control in `discover/catalog.json`. Retain small budgets until a method
beats or matches an archive incumbent. Symmetry and deletion-repair are plausible
experiments, not claims that these particular instances are easy.

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

# Review, credit, and local operation

Maintainer: @Mister-Meeseeks (from 2026-10-21); review capacity `surge`. Original
material is MIT-licensed; credit is in `discover.json`. See `docs/GOVERNANCE.md`.
Preserve source authorship and contributors' witness/algorithm provenance. No
co-authorship or acceptance is promised. LJCR excerpts keep their existing CC BY 4.0
license and attribution; that is separate from a license for this pilot's code.

A future acceptance procedure should check the exact instance, value, witness hash,
full coverage, incumbent comparison, and source/novelty audit; a separate reviewer
should rerun the verifier and audit lower-bound arguments. Do not label a result
maintainer-reviewed or independently-checked now. Record proposed checks in
`discover/verifications/`, identified by commit and scope. No automated acceptance
or public coordination channel is configured.

The verifier and frontier deserve the most careful review; future review capacity,
not donated compute, will determine the project's pace.
