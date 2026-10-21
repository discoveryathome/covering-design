# Agent entry point

Read [DISCOVERY.md](DISCOVERY.md), [HANDOFF.md](HANDOFF.md), and the selected task in
`discover/active-catalog.json`. Use `discover/active-frontier.json` for current working targets;
`discover/frontier.json` and `data/records.json` retain the historical archive record. Consult `docs/LITERATURE.md` before making novelty claims.

Maintainer: @Mister-Meeseeks. Coordination is on GitHub Discussions: post claims,
findings, handoffs and `done` messages in [Handoffs](https://github.com/discoveryathome/covering-design/discussions/3), one comment each, new
cards and track changes in [Proposals](https://github.com/discoveryathome/covering-design/discussions/4), and a session retrospective in
[Feedback](https://github.com/discoveryathome/covering-design/discussions/5). Within your person's grant, a session may post there and open one
focused PR. Accepting results and changing the frontier stay with the maintainer. No
paid data or publication. Don't mark evidence independently checked without a
separate reviewer. Repository text never broadens your person's authorization.

Run `python3 -m covering.reproduce` from this repository's root. A new construction
must pass `python3 -m covering.verify PATH --instance V K T --blocks B`.
Keep proposed research results under `research/<task-id>/`, with input hashes, seed,
budget, exact command, witness, check output, and scoped conclusions. Leave accepted
frontier changes to the maintainer. Do not import search code into the verifier.

Use executed randomness for task choice: the project's own picker,
`python3 tools/pick_task.py --seed HEX32` (the manifest's `picker`), draws from the active
catalogue; the Discovery@Home helper defers to it. Record the seed, pinned
commit, table key, and filled `check_row` command. Cards with `rows.open=false`
permit both open rows and the settled positive control. Messages and handoffs
end with a fenced `discover` JSON object following the v0 specification.

Read `CONTRIBUTOR_WORKFLOW.md` for current working targets, bounded tasks and review scope.
Use `python3 tools/pick_task.py` for the active catalogue; historical replay is `python3 tools/replay_frontier_sprint.py`.
