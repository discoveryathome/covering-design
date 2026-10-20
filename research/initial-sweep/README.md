# Initial tractability sweep

Read REPORT.md for the result and launch recommendation. This is a LOCAL research
package, not an accepted change to the pilot frontier. Original maintainer,
licensing, and publication decisions remain pending.

The experiment manifest records the seed, scope, fixed greedy/repair budgets, base
commit, and archive metadata hash. Inputs, exact witnesses, per-trial JSON Lines,
source credits, and verification transcripts are included. No downloaded covering
program was executed; the search and checkers were written locally.

From the repository root, verify stored evidence without rerunning search:

```sh
python3 research/initial-sweep/tools/check_package.py all
python3 research/initial-sweep/tools/check_package.py check_row --v 92 --k 7 --t 4
```

The package also provides an independent C++ matrix checker for faster audits of
large witnesses. Compile source locally; no binary is committed:

```sh
mkdir -p scratch/sweep
clang++ -O3 -std=c++17 research/initial-sweep/tools/verify_matrix.cpp -o scratch/sweep/verify-matrix
python3 research/initial-sweep/tools/check_native.py research/initial-sweep/witnesses/combined-92-7-4.json --checker scratch/sweep/verify-matrix --matrix scratch/sweep/92-7-4.txt --instance 92 7 4 --blocks 131122
```

For a fast full audit after compiling the native checker, run:

```sh
python3 research/initial-sweep/tools/check_package.py all --native-checker scratch/sweep/verify-matrix --matrix-dir scratch/sweep/matrices
```

The pure-Python checker uses exact colex ranks and one byte per required subset,
with a cap of 30 million subsets. Large-row checks can take a few minutes.
It has no search-code imports. Native and Python implementations were checked on
all 1,024 (5,3,2) families; the existing direct-containment verifier and six negative
fixtures are separate controls. This is algorithmic checking by one author, not a
claim that a second contributor has independently reviewed the package.

Construction audits can be replayed offline:

```sh
python3 research/initial-sweep/tools/closure.py research/initial-sweep/data/archive-counts.json --output scratch/sweep/closure.json
python3 research/initial-sweep/tools/audit_additional_rules.py research/initial-sweep/data/archive-counts.json --output scratch/sweep/additional.json
```

`proposed-frontier.json` is a scoped Discovery record-table proposal, with a
per-instance `check_row` command and witnesses. It is deliberately separate from
`discover/frontier.json`. A verified improvement over a frozen archive is not
necessarily a current public record; current-cell confirmation remains outstanding.

Search requires a C++17 compiler. The saved engine and driver run sequential cells
with fixed seeds. They never need network access. The driver refuses to overwrite
saved experiment result files. Use a separate experiment copy for a new run and
retain the original result package. The command vectors in each result identify
all numeric arguments, source seed files, and output witnesses; paths reflect the
original local workspace and should be adjusted to the new checkout.

Live archive acquisition used bounded, cached byte ranges from the cited public
Zenodo file, with capped retries for transient read timeouts. Rechecking included
witnesses requires no network or archive download. Current successor filtered pages
were inaccessible; no access controls were bypassed, and nothing was published.
