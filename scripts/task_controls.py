"""Run the four catalogue first_step positive controls from the repository root."""
import json
import subprocess
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'discover/catalog.json').read_text())
for track in catalog['tracks']:
    for card in track['tasks']:
        command=card['first_step']['command'][:]
        if command[0]=='python3': command[0]=sys.executable
        print(f"CARD {card['id']}\nEXPECT {card['first_step']['expected']}",flush=True)
        subprocess.run(command,cwd=root,check=True)
print('PASS: all 4 task first_step controls',flush=True)
