# Covering designs: a Discovery@Home project

Current contributor instructions: [CONTRIBUTOR_WORKFLOW.md](CONTRIBUTOR_WORKFLOW.md) (21 October 2026).

The [follow-up frontier sprint](research/frontier-sprint/README.md) reports two
exactly verified proposals below the audited published counts: C(48,9,3)<=272
and C(90,12,3)<=678. Its scientific-fit recommendation is LAUNCH on the larger
t=3 track, with separate scientific review still pending. The
[initial sweep](research/initial-sweep/REPORT.md) is retained as evidence about
the earlier methods; its priorities are superseded by the follow-up.

Find small families of k-element blocks on {1,...,v} that cover every t-element
subset. Each (v,k,t) is an independent minimization record. A witness proves an
**upper bound**, not optimality. Only the Fano control is proved optimal here.

Maintained by @Mister-Meeseeks, MIT-licensed, and listed on the Discovery@Home hub; see
[governance](docs/GOVERNANCE.md). Selected La Jolla Coverings Repository data keep their
CC BY 4.0 license.

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

The following table records historical controls, not the active donor search pool.

| Instance | Proved lower bound reproduced here | LJCR reported lower bound | Verified LJCR construction | Seeded greedy baseline | Historical first target |
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

Start at [AGENTS.md](AGENTS.md), then [CONTRIBUTOR_WORKFLOW.md](CONTRIBUTOR_WORKFLOW.md).
The [active catalogue](discover/active-catalog.json) contains two search tasks,
six gated witness-retrieval tasks, a bound trace and two verification tasks.
Use `python3 tools/pick_task.py`. The [working frontier](discover/active-frontier.json)
exposes the 272- and 678-block proposals; [the original frontier](discover/frontier.json)
and [archive records](data/records.json) remain reproducible historical controls.

The start playbook, specification, and schemas fetched for this run are saved under
`docs/protocol/`. To inspect protocol validation, use the Discovery@Home helper
(https://discoveryathome.org/cli/latest.json names the current file and its SHA-256),
or the `discover` plugin:

```sh
python3 discover-<sha12>.pyz validate .
```

Coordination is on [GitHub Discussions](https://github.com/discoveryathome/covering-design/discussions):
claims, findings and handoffs in *Handoffs*.

`results/protocol-validation.txt` is the transcript from the local-proposal period, when
`maintainers` was intentionally empty; the manifest now names the maintainer.
