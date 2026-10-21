# Agent entry point

Read [DISCOVERY.md](DISCOVERY.md), [HANDOFF.md](HANDOFF.md), and the selected task in
`discover/catalog.json`. Use `discover/frontier.json` and `data/records.json` for the
scoped local record. Consult `docs/LITERATURE.md` before making novelty claims.

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

Use executed randomness for task choice: the Discovery@Home helper supports
`pick . --seed HEX32 --count 1` without live GitHub access. Get it from
https://discoveryathome.org/cli/latest.json (the file name and SHA-256 to check), or
use the `discover` plugin. Record the seed, pinned
commit, table key, and filled `check_row` command. Cards with `rows.open=false`
permit both open rows and the settled positive control. Messages and handoffs
end with a fenced `discover` JSON object following the v0 specification.
