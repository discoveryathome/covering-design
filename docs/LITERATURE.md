# Literature and source audit

Accessed for this pilot on 2026-10-20 UTC. A dated archive, a construction witness,
and a lower-bound proof are different evidence. Search terms included the exact
selected C(v,k,t) cells, Schönheim bounds, covering-design greedy algorithms,
simulated annealing, and recent covering-design bounds.

## Repository sources and dates

1. Daniel M. Gordon, [La Jolla Combinatorics Repository](https://dmgordon.org/ljcr/)
   and [Covering Designs](https://dmgordon.org/covering-designs/). These pages explain
   that stored coverings give upper bounds. The database was frozen in March 2026;
   the former servers retired in August. Gordon links the archive and a successor.
2. Gordon, [*La Jolla Coverings Repository*, v1.2](https://doi.org/10.5281/zenodo.19735294),
   24 April 2026. `coverdata.json` holds size, `low_bd`, and historical improvements;
   `covers.json` contains block lists. We checked the metadata file against Zenodo's
   MD5 and independently verified each selected construction. Only bounded portions
   of the 4.2 GB block file were fetched. Selected metadata, unchanged block arrays,
   envelope witnesses, exact byte ranges, and attribution are included locally.
3. [dmgordo/LJCR](https://github.com/dmgordo/LJCR/tree/459bcaf247bd8d34610d946b0465864f7d4dfa37/coverings),
   pinned GitHub commit dated 19 December 2022. The five selected upper/lower entries
   agree with v1.2; see `data/ljcr-github-selected.json`. GitHub's old metadata are
   therefore corroboration for these cells, not a source of post-2022 improvements.
4. Giovanni Acerbi, [Covering Repository](https://coveringrepository.com/).
   Its ordinary (v,k,t) records are a separate section from generalized (v,k,t,m)
   records. For comparison use **m=t**. Its homepage says it imported Gordon's
   historical data and tracks subsequent improvements. The latest-improvements
   page was readable, but filtered k=5,t=3,m=3 and k=6,t=3,m=3 pages were unavailable
   (tool errors/HTTP 403), so selected current cells were **not confirmed**.
   Do not infer that an absent item in the latest-changes page is unchanged.

The archive descriptions differ at the v=100 boundary (v<100 versus v<=100).
This discrepancy does not affect any selected cell; no full-range claim relies on it.

## Construction methods

5. Daniel M. Gordon, Oren Patashnik, Greg Kuperberg, *New constructions for covering
   designs*, Journal of Combinatorial Designs **3** (1995), 269–284,
   [DOI 10.1002/jcd.3180030404](https://doi.org/10.1002/jcd.3180030404),
   [author preprint](https://arxiv.org/html/math/9502238).
   Sections II and VI.5 support greedy and local-improvement experiments;
   induced and combination constructions provide additional directions.
   The baseline implements maximum uncovered gain with seeded tie breaking and
   redundancy deletion. It is **not** a verbatim reproduction of the paper's
   particular pseudorandom ordering or random generator.
6. Kari J. Nurmela and Patric R. J. Östergård, *Upper bounds for covering designs by
   simulated annealing*, Congressus Numerantium **96** (1993), 93–111.
   Bibliographic details and method discussion were checked in the
   [author preprint's references and VI.5](https://arxiv.org/html/math/9502238).
   Their related report *Constructing Covering Designs by Simulated Annealing*,
   Helsinki University of Technology, Series B Technical Report 10 (1993), is
   catalogued by [Aalto's library](https://www.finna.fi/Record/aalto.991624164406526).
   Original report full text was not obtained here; no third-party annealing code
   was executed or copied. Simulated annealing is a literature-backed next task.
7. Gordon, Kuperberg, Patashnik, Spencer,
   [*Asymptotically optimal covering designs*](https://arxiv.org/abs/math/9511224).
   This concerns fixed k,t as v tends to infinity. It does not resolve the small
   independent cells in this pilot and is not a certificate for their optima.

## Lower bounds and known pitfalls

8. J. Schönheim, *On coverings*, Pacific Journal of Mathematics **14** (1964),
   1405–1411. The recurrence and original citation are reproduced in the primary
   author papers [Gordon et al., Theorem 1](https://arxiv.org/html/math/9502238) and
   [Horsley–Singh, equations (1)–(2)](https://arxiv.org/html/1706.06825v2).
   We used those accessible statements and supplied a complete counting proof in
   `LOWER_BOUNDS.md`; a guessed publisher URL was discarded after it led to an
   unrelated paper. No proof claim relies on that failed URL.
9. Daniel Horsley and Rakhi Singh,
   [*New lower bounds for t-coverings*, arXiv:1706.06825v2](https://arxiv.org/html/1706.06825v2),
   revised 4 October 2017. Incidence-matrix methods and small-parameter discussions
   are relevant lower-bound leads. Hypotheses must be checked per cell; no blanket
   transfer of design inequalities to arbitrary coverings is permitted.
10. Gordon, [errata for *New Constructions for Covering Designs*](https://dmgordon.org/errata/).
    Historical unconstructed entries include claimed sizes 14 for (14,7,3) and 30
    for (30,15,4); erroneous optimality marks also occurred. The page calls the paper
    “1996”, whereas publisher metadata give 1995. This dating discrepancy is retained,
    not silently resolved. The pilot relies on checked archive witnesses, not on
    old table entries or stars.

## Selected record evidence

| Cell | Archive upper | Reported lower | Most recent relevant attribution in metadata |
|---|---:|---:|---|
| (7,3,2) | 7 | 7 | Standard Fano construction; archive JCD entry |
| (14,5,3) | 43 | 37 | Nurmela/Östergård simulated annealing |
| (15,5,3) | 55 | 54 | Carmine Iorio, 2020-01-15 |
| (16,5,3) | 65 | 61 | Rade Belic, 1997-08-06 |
| (13,6,3) | 21 | 20 | Random Greedy Covering, 1997-01-31 |

Exact original histories are retained in `data/ljcr-selected.json`. Histories need
not be assumed sorted in the entire archive. These are source attributions, not
new results of this pilot. The stronger 20 lower bound needs a proof citation;
current successor status remains an open obligation for every research cell.

A search also found a [Proof Factory ledger about C(15,5,3)](https://proofs.charliekrug.com/problems/covering-c1553/).
It reports extensive restricted searches and maintains 54..55. This is a **lead only**:
its underlying code, proofs, and claimed exclusions were not audited here, so none
is treated as established or used to mark any branch settled. Before repeating
local trade shells, inspect those artifacts and their exact scope. No external
agent ledger can substitute for a complete unrestricted nonexistence proof.
