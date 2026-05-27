"""
build_release.py — Calls combine_rulebook.py for every subdirectory that
contains a meta.json and writes the output to release/<dirname>.json.

Usage:
    python build_release.py
"""

import os
import subprocess
import sys

ROOT       = os.path.dirname(os.path.abspath(__file__))
COMBINE    = os.path.join(ROOT, "combine_rulebook.py")
RELEASE    = os.path.join(ROOT, "release")

os.makedirs(RELEASE, exist_ok=True)

dirs = [
    d for d in os.listdir(ROOT)
    if os.path.isdir(os.path.join(ROOT, d))
    and os.path.isfile(os.path.join(ROOT, d, "meta.json"))
]

if not dirs:
    print("No subdirectories with meta.json found.")
    sys.exit(1)

errors = 0
for name in sorted(dirs):
    input_dir   = os.path.join(ROOT, name)
    output_file = os.path.join(RELEASE, f"{name}.json")
    print(f"  {name}  →  release/{name}.json")
    result = subprocess.run(
        [sys.executable, COMBINE, input_dir, output_file],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"    FEHLER:\n{result.stderr.strip()}")
        errors += 1
    else:
        if result.stdout.strip():
            print(f"    {result.stdout.strip()}")

print()
if errors:
    print(f"Fertig mit {errors} Fehler(n).")
    sys.exit(1)
else:
    print(f"Fertig. {len(dirs)} Datei(en) in release/ erstellt.")
