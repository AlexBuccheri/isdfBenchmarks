""" Command line script to submit all jobs in subdirectories of root

To run:
source programs/isdfBenchmarks/.venv/bin/activate
python ~/programs/isdfBenchmarks/scripts/submit.py

Specify ROOT
"""
import os
import subprocess
import re
import sys

ROOT = "/home/bucchera/exchange_calcs/kmeans_plus_plus"
DRY = False

JOBID_RE = re.compile(r"Submitted batch job (\d+)")


def main():
    root = os.path.abspath(ROOT)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    job_dirs = sorted(d for d, _, files in os.walk(root) if "slurm.sh" in files)
    if not job_dirs:
        print(f"No 'slurm.sh' found under {root}")
        return 1

    print(f"Found {len(job_dirs)} dirs with slurm.sh in\n {ROOT}\n")

    submitted, errors = [], 0

    for i, d in enumerate(job_dirs, 1):
        rel = os.path.relpath(d, root)
        label = d if rel.startswith("..") else rel

        if DRY:
            print(f"[{i}/{len(job_dirs)}] [DRY] {label}: sbatch slurm.sh")
            continue

        proc = subprocess.run(["sbatch", "slurm.sh"], cwd=d, capture_output=True, text=True)
        out, err = proc.stdout.strip(), proc.stderr.strip()
        m = JOBID_RE.search(out)
        ok = (proc.returncode == 0) and (m is not None)
        status = "OK" if ok else "ERROR"

        print(f"[{i}/{len(job_dirs)}] {label}: {status}")
        if out:
            print("  stdout:", out)
        if err:
            print("  stderr:", err)
        if ok:
            submitted.append((d, m.group(1)))
        else:
            errors += 1

    print("\n=== Summary ===")
    print(f"Total: {len(job_dirs)} | Submitted: {len(submitted)} | Errors: {errors}")
    if submitted:
        print("\nJobIDs:")
        for d, jid in submitted:
            print(f"  {jid}  <-  {d}")

    return 0 if errors == 0 or DRY else 2


if __name__ == "__main__":
    sys.exit(main())
