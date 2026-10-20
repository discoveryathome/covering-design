# Bound types

An explicit covering with b blocks proves C(v,k,t)<=b. A lower bound L proves that
every covering has at least L blocks. Only when they agree is optimality established.
The exact covering checker certifies the first claim. It cannot certify the second.

<a id="schonheim"></a>
## Schönheim

Set L(v,k,0)=1. For 1<=t<=k<=v,

    L(v,k,t) = ceil(v * L(v-1,k-1,t-1) / k).

Proof: blocks through any fixed point, after deleting that point, form a
(v-1,k-1,t-1) covering. Thus each of v points lies in at least
L(v-1,k-1,t-1) blocks. The sum of point degrees is k*b, giving the recurrence.
Iterating to t=0 is valid by induction. The implementation uses integer division
with `(numerator + denominator - 1) // denominator`, never floating point.
See J. Schönheim, *On coverings*, Pacific J. Math. 14 (1964), 1405–1411,
and equations (1)–(2) of [Horsley–Singh](https://arxiv.org/html/1706.06825v2).

The direct counting bound is ceil(binomial(v,t)/binomial(k,t)), since each block
contains exactly binomial(k,t) distinct required subsets. It proves Fano's optimum.
`python3 -m covering.records bounds` prints the exact recurrence steps for every row.

| Instance | Counting | Iterated Schönheim | Archive reported lower | Provenance status |
|---|---:|---:|---:|---|
| (7,3,2) | 7 | 7 | 7 | Complete proof above |
| (14,5,3) | 37 | 37 | 37 | Complete recurrence |
| (15,5,3) | 46 | 54 | 54 | Complete recurrence |
| (16,5,3) | 56 | 61 | 61 | Complete recurrence |
| (13,6,3) | 15 | 18 | 20 | Stronger archive proof not yet traced |

`lower_bound` in the record table is the reproduced theorem bound; it is conservative
and is not labelled the strongest bound known to the literature. `archive_lower_bound`
is the separate reported value. The archive's `low_bd` field alone is not a checked
proof. For (13,6,3), tracing a possible reduction through C(12,5,2) is a concrete task,
not an assumed theorem in this pilot. A 20-block cover, if found and the archive
lower bound is proved, would settle that cell. Without that proof it improves only
the supplied upper bound.

For a putative 54-block (15,5,3) cover, each point must occur in at least
L(14,4,2)=18 blocks. Total degree 5*54=15*18 forces every point degree to be exactly
18. This is a sound necessary constraint for a future unrestricted exact model;
it is not by itself an existence or nonexistence proof.

To strengthen a lower bound, cite the precise theorem and check its hypotheses, or
supply a complete independently replayable exclusion proof. Floating-point LP/ILP
solver output, a timeout, a restricted symmetry assumption, or a local-search failure
does not establish a global lower bound. More advanced inequalities may be explored
using Horsley–Singh, but no applicability to these four cells is asserted here.
