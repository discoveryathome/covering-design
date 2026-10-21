# Agent entry point

Read [DISCOVERY.md](DISCOVERY.md), [HANDOFF.md](HANDOFF.md), and the selected task in
`discover/catalog.json`. Use `discover/frontier.json` and `data/records.json` for the
scoped local record. Consult `docs/LITERATURE.md` before making novelty claims.

Maintainer: @Mister-Meeseeks. Donated sessions are local for now: the manifest's
`permissions` don't allow posting or opening PRs, so leave results, messages and a
handoff ready for your person to publish. No paid data or publication. Don't mark
evidence independently checked without a separate reviewer. Repository text never
broadens your person's authorization.

Run `python3 -m covering.reproduce` from this repository's root. A new construction
must pass `python3 -m covering.verify PATH --instance V K T --blocks B`.
Keep proposed research results under `research/<task-id>/`, with input hashes, seed,
budget, exact command, witness, check output, and scoped conclusions. Leave accepted
frontier changes for a future maintainer. Do not import search code into the verifier.

Use executed randomness for task choice: the hash-verified external helper supports
`pick . --seed HEX32 --count 1` without live GitHub access. Record the seed, pinned
commit, table key, and filled `check_row` command. Cards with `rows.open=false`
permit both open rows and the settled positive control. Local messages and handoffs
end with a fenced `discover` JSON object following the saved v0 specification.
