"""Merge per-run velocity logs and report sample diversity."""

import argparse
import csv
import glob
import os
from collections import Counter
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
    parser.add_argument("-minimum-samples-per-format", type=int, default=200)
    args = parser.parse_args()

    samples = read_rows(os.path.join(args.input_dir, "velocity-f*-run*-samples.csv"))
    neighbors = read_rows(os.path.join(args.input_dir, "velocity-f*-run*-neighbors.csv"))
    write_rows(args.output_prefix + "-samples.csv", samples)
    write_rows(args.output_prefix + "-neighbors.csv", neighbors)

    unique_fitness = {row["fitness"] for row in samples if row.get("fitness")}
    sample_counts = Counter(row["genetic_format"] for row in samples)
    feasible_neighbors = sum(row.get("status") == "feasible" for row in neighbors)
    print(f"Saved {len(samples)} samples ({len(unique_fitness)} unique fitness values)")
    print("Samples by representation: " + ", ".join(f"f{key}={sample_counts.get(key, 0)}" for key in ("0", "1", "4", "H")))
    print(f"Evaluated {len(neighbors)} mutants ({feasible_neighbors} feasible)")
    insufficient_formats = {
        genetic_format: count
        for genetic_format, count in (("0", sample_counts.get("0", 0)), ("1", sample_counts.get("1", 0)), ("4", sample_counts.get("4", 0)), ("H", sample_counts.get("H", 0)))
        if count < args.minimum_samples_per_format
    }
    if insufficient_formats:
        details = ", ".join(f"f{genetic_format}={count}" for genetic_format, count in insufficient_formats.items())
        raise SystemExit(
            f"Not enough samples per representation ({details}); need at least "
            f"{args.minimum_samples_per_format} each. Increase RUNS or sampling iterations."
        )
    if len(unique_fitness) < args.minimum_samples:
        raise SystemExit(
            f"Only {len(unique_fitness)} unique fitness values; increase RUNS or MAX_ITERATIONS "
            f"to reach {args.minimum_samples}."
        )


if __name__ == "__main__":
    main()