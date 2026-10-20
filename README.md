# Covering designs: Discovery@Home local pilot

The [initial tractability sweep](research/initial-sweep/REPORT.md) now reports the
empirical launch assessment. Read it before advertising easy construction wins.

Find small families of k-element blocks on {1,...,v} that cover every t-element
subset. Each (v,k,t) is an independent minimization record. A witness proves an
**upper bound**, not optimality. Only the Fano control is proved optimal here.

This is a **LOCAL proposal**. No maintainer has agreed, no license for original
project material has been chosen, and no publication or hub consent exists.
See [governance status](docs/GOVERNANCE.md). No remote repository is configured.

Python **3.10+**, standard library only; no install, network, solver, or GPU needed:

```sh
python3 -m covering.reproduce
python3 -m covering.records check_row --v 14 --k 5 --t 3
python3 -m covering.verify witnesses/fano.json --instance 7 3 2 --blocks 7
python3 -m covering.baseline --seed 20261020 --restarts 8 --output-dir scratch/baseline
```

The replay checks five record witnesses, five baseline witnesses, eight tests,
and exact Fano optimality by matching its seven blocks to a lower bound of seven.
All six deliberately invalid fixtures must be rejected. The verifier is independent
of search scoring and masks; independent *review by another contributor* is pending.

| Instance | Proved lower bound reproduced here | LJCR reported lower bound | Verified LJCR construction | Seeded greedy baseline | First search target |
|---|---:|---:|---:|---:|---:|
| C(7,3,2) | 7 | 7 | 7 | 7 | Settled control |
| C(14,5,3) | 37 | 37 | 43 | 51 | 42 |
| C(15,5,3) | 54 | 54 | 55 | 64 | 54 |
| C(16,5,3) | 61 | 61 | 65 | 77 | 64 |
| C(13,6,3) | 18 | 20 | 21 | 24 | 20 |

Archive counts are from [Gordon's frozen LJCR v1.2](https://doi.org/10.5281/zenodo.19735294),
with attribution histories and block witnesses included. They are **archive best-known
constructions**, not an assertion of today's world records. [Acerbi's successor](https://coveringrepository.com/)
tracks later changes; selected filtered pages were inaccessible in this session.
The bound 20 needs a source-proof audit; the record table deliberately uses the
weaker bound 18 with a complete derivation. [Literature](docs/LITERATURE.md) and
[lower bounds](docs/LOWER_BOUNDS.md) explain these distinctions.

Start at [AGENTS.md](AGENTS.md), then [DISCOVERY.md](DISCOVERY.md). Four concrete tasks
are in [the catalogue](discover/catalog.json); priorities and proposed attacks are
in [HANDOFF.md](HANDOFF.md). The authoritative local evidence is the
[frontier](discover/frontier.json) and [per-instance record table](data/records.json).
The greedy run found **no improvement** over the archive.

The start playbook, specification, and schemas fetched for this run are saved under
`docs/protocol/`. The verified helper lives outside this repository at
`../session-covering-design/discover.pyz`. To inspect protocol validation:

```sh
python3 ../session-covering-design/discover.pyz validate .
```

Expected: one intentional schema failure, `maintainers` needs at least one item.
The empty array truthfully records that nobody has accepted the role. Do not fill
it with a fictional person to make validation pass. `LICENSE` is a pending-decision
notice, not a granted open-source license. Other missing online conventions are
intentional in LOCAL mode. See `results/protocol-validation.txt`.
