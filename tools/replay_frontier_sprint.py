"""Replay the frozen sprint with its original documentation in an isolated copy.

The original manifest and replay remain untouched. Current contributor documents
can evolve without invalidating the evidence package or concealing hash failures.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "research/frontier-sprint/artifacts.sha256.json").read_text())
    bindings = json.loads((ROOT / "research/readiness-20261021/historical-bindings.json").read_text())
    with tempfile.TemporaryDirectory(prefix="covering-sprint-") as temporary:
        snapshot = Path(temporary) / "repo"
        shutil.copytree(ROOT, snapshot, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache"))
        for name, source in bindings.items():
            data = (ROOT / source).read_bytes()
            if hashlib.sha256(data).hexdigest() != manifest[name]:
                raise ValueError("historical snapshot hash mismatch: " + name)
            (snapshot / name).write_bytes(data)
        subprocess.run([sys.executable, "research/frontier-sprint/tools/replay.py"], cwd=snapshot, check=True)


if __name__ == "__main__":
    main()
