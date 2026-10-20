# Author verification receipt

All checks ran in a macOS OS sandbox denying network and writes outside the
session workspace (with /dev/null allowed). The existing tool environment itself
was not configured as a donated-session sandbox; no donor preset was installed.
No third-party covering program, notebook, or build script was executed.

Evidence: `results/reproduce.txt`, `fresh-clone-reproduce.txt`, `task-controls.txt`,
`negative-cli.txt`, and `baseline-determinism.txt`. Full reproduction from a fresh
local Git clone passed. Eight tests include exhaustive (5,3,2) subfamilies and
mutations of the row's instance, value, hash, and lower bound. All six negative
construction fixtures exited 1 at the CLI. Five baseline witness byte comparisons
passed after rerunning the same seed and restart count.

The fetched hash-verified Discovery helper screened the project without findings.
Its validator recognized five record cells (four open) and reported exactly one
required-file/schema issue: the intentionally empty maintainer list. Licence and
intake readiness must not be inferred merely from a LICENSE file's existence.
Online coordination is absent by design. Source hashes and original contributor
histories are retained in the data and frontier files.

The seeded helper picker also ran locally, returned a concrete row and check_row
command, and made no reservation. This does not constitute research work on that
card. No author-check result has been labelled independent review or acceptance.

```discover
{
  "v": 0,
  "kind": "finding",
  "scope": "Bootstrap evidence: 5 record witnesses, 5 baseline witnesses, Fano optimum, 8 tests, 4 task controls; no record improvement.",
  "base": "2f320f8d1193bf4ae238b2fae3a9221fe1ae6228",
  "posted_at": "2026-10-20T04:56:54.834271Z",
  "evidence_level": "local-only"
}
```
