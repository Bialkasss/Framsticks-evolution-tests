"""Merge per-run velocity logs and report sample diversity."""

import argparse
import csv
import glob
import os
from typing import Dict, List


def read_rows(pattern: str) -> List[Dict[str, str]]:
    rows = []
    for filename in sorted(glob.glob(pattern)):
        with open(filename, newline="", encoding="utf-8") as source:
            rows.extend(csv.DictReader(source))
    return rows


def write_rows(filename: str, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError("No rows found")
    with open(filename, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-input-dir", default="velocity_samples")
    parser.add_argument("-output-prefix", default="velocity_samples/velocity-all")
    parser.add_argument("-minimum-samples", type=int, default=200)
    args = parser.parse_args()

    samples = read_rows(os.path.join(args.input_dir, "velocity-f*-run*-samples.csv"))
    neighbors = read_rows(os.path.join(args.input_dir, "velocity-f*-run*-neighbors.csv"))
    write_rows(args.output_prefix + "-samples.csv", samples)
    write_rows(args.output_prefix + "-neighbors.csv", neighbors)

    unique_fitness = {row["fitness"] for row in samples if row.get("fitness")}
    feasible_neighbors = sum(row.get("status") == "feasible" for row in neighbors)
    print(f"Saved {len(samples)} samples ({len(unique_fitness)} unique fitness values)")
    print(f"Evaluated {len(neighbors)} mutants ({feasible_neighbors} feasible)")
    if len(unique_fitness) < args.minimum_samples:
        raise SystemExit(
            f"Only {len(unique_fitness)} unique fitness values; increase RUNS or MAX_ITERATIONS "
            f"to reach {args.minimum_samples}."
        )


if __name__ == "__main__":
    main()