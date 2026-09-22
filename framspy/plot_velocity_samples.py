"""Plot collected velocity samples and their mutant neighborhoods."""

import argparse
import csv
import math
import os
from collections import defaultdict
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import numpy as np


FORMATS = ["0", "1", "4", "H"]
LABELS = {"0": "f0", "1": "f1", "4": "f4", "H": "fH"}


def read_rows(filename: str) -> List[Dict[str, str]]:
    with open(filename, newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def write_rows(filename: str, rows: Iterable[Dict[str, object]], fields: List[str]) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def plot_individual_runs(samples: List[Dict[str, str]], filename: str) -> None:
    figure, axis = plt.subplots(figsize=(11, 6))
    for genetic_format in FORMATS:
        format_rows = [row for row in samples if row["genetic_format"] == genetic_format]
        runs = defaultdict(list)
        for row in format_rows:
            runs[row["run"]].append((int(row["sample_index"]), float(row["fitness"])))
        for run, values in sorted(runs.items()):
            values.sort()
            axis.plot([item[0] for item in values], [item[1] for item in values], alpha=0.22, color=f"C{FORMATS.index(genetic_format)}")
        axis.plot([], [], color=f"C{FORMATS.index(genetic_format)}", label=LABELS[genetic_format])
    axis.set(title="Velocity samples in independent optimization runs", xlabel="Sample index", ylabel="Velocity")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(filename, dpi=160)
    plt.close(figure)


def plot_aggregated_runs(samples: List[Dict[str, str]], filename: str) -> None:
    figure, axis = plt.subplots(figsize=(11, 6))
    for genetic_format in FORMATS:
        by_index = defaultdict(list)
        for row in samples:
            if row["genetic_format"] == genetic_format:
                by_index[int(row["sample_index"])].append(float(row["fitness"]))
        indices = sorted(by_index)
        means = np.array([np.mean(by_index[index]) for index in indices])
        deviations = np.array([np.std(by_index[index]) for index in indices])
        color = f"C{FORMATS.index(genetic_format)}"
        axis.plot(indices, means, color=color, label=LABELS[genetic_format])
        axis.fill_between(indices, means - deviations, means + deviations, color=color, alpha=0.16)
    axis.set(title="Mean velocity samples with standard deviation", xlabel="Sample index", ylabel="Velocity")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(filename, dpi=160)
    plt.close(figure)


def plot_boxplots(samples: List[Dict[str, str]], filename: str) -> None:
    terminal = defaultdict(dict)
    for row in samples:
        key = (row["genetic_format"], row["run"])
        index = int(row["sample_index"])
        if not terminal[key] or index > terminal[key]["sample_index"]:
            terminal[key] = {"sample_index": index, "fitness": float(row["fitness"])}
    values = [[item["fitness"] for key, item in terminal.items() if key[0] == genetic_format] for genetic_format in FORMATS]
    figure, axis = plt.subplots(figsize=(9, 6))
    axis.boxplot(values)
    axis.set_xticklabels([LABELS[genetic_format] for genetic_format in FORMATS])
    axis.set(title="Terminal sample velocity by representation", xlabel="Representation", ylabel="Velocity")
    axis.set_ylim(bottom=0)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(filename, dpi=160)
    plt.close(figure)


def plot_neighborhoods(neighbors: List[Dict[str, str]], best_fitness: float, output_prefix: str) -> None:
    for genetic_format in FORMATS:
        rows = [row for row in neighbors if row["genetic_format"] == genetic_format and row["status"] == "feasible"]
        figure, axis = plt.subplots(figsize=(7, 7))
        axis.scatter([float(row["parent_fitness"]) for row in rows], [float(row["fitness"]) for row in rows], s=10, alpha=0.35)
        axis.plot([0, best_fitness], [0, best_fitness], color="black", linestyle="--", linewidth=1, label="y=x")
        axis.set(xlim=(0, best_fitness), ylim=(0, best_fitness), title=f"{LABELS[genetic_format]} mutant neighborhoods", xlabel="Parent velocity", ylabel="Mutant velocity")
        axis.grid(alpha=0.25)
        axis.legend()
        figure.tight_layout()
        figure.savefig(f"{output_prefix}_neighborhood_{LABELS[genetic_format]}.png", dpi=160)
        plt.close(figure)


def calculate_statistics(neighbors: List[Dict[str, str]]) -> List[Dict[str, object]]:
    statistics = []
    for genetic_format in FORMATS:
        rows = [row for row in neighbors if row["genetic_format"] == genetic_format]
        feasible = [row for row in rows if row["status"] == "feasible"]
        better = [row for row in feasible if float(row["fitness"]) > float(row["parent_fitness"])]
        statistics.append({
            "genetic_format": LABELS[genetic_format],
            "total_mutants": len(rows),
            "feasible_mutants": len(feasible),
            "better_mutants": len(better),
            "better_fraction": len(better) / len(feasible) if feasible else 0.0,
        })
    return statistics


def write_conclusions(filename: str, statistics: List[Dict[str, object]], best_fitness: float) -> None:
    with open(filename, "w", encoding="utf-8") as output:
        output.write("# Velocity landscape conclusions\n\n")
        output.write(f"The common plot scale is 0 to {best_fitness:.12g}, the best sampled velocity across all representations.\n\n")
        output.write("The neighborhood scatter plots show how mutant fitness is distributed around collected parents. Points above the y=x line improve on their parent; points below it are worse. The better-mutant fractions are:\n\n")
        for row in statistics:
            output.write(f"- {row['genetic_format']}: {row['better_fraction']:.2%} ({row['better_mutants']}/{row['feasible_mutants']} feasible mutants)\n")
        output.write("\nA representation with a larger fraction above y=x offers more improving one-mutation directions near the sampled solutions. A concentration below the line indicates local resistance or that the climb has reached high-quality local optima. Wider vertical spread indicates a more rugged or heterogeneous local landscape. These conclusions describe the sampled neighborhoods, not the complete genotype spaces.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-samples", required=True)
    parser.add_argument("-neighbors", required=True)
    parser.add_argument("-output-prefix", default="velocity_samples/velocity")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.output_prefix)), exist_ok=True)
    samples = read_rows(args.samples)
    neighbors = read_rows(args.neighbors)
    if not samples or not neighbors:
        raise RuntimeError("Both samples and neighbors files must contain data")
    best_fitness = max(float(row["fitness"]) for row in samples if math.isfinite(float(row["fitness"])))
    if best_fitness <= 0:
        raise RuntimeError("The required 0-to-best plot scale needs a positive sampled fitness")
    plot_individual_runs(samples, args.output_prefix + "_individual_runs.png")
    plot_aggregated_runs(samples, args.output_prefix + "_aggregated_runs.png")
    plot_boxplots(samples, args.output_prefix + "_boxplots.png")
    plot_neighborhoods(neighbors, best_fitness, args.output_prefix)
    statistics = calculate_statistics(neighbors)
    fields = ["genetic_format", "total_mutants", "feasible_mutants", "better_mutants", "better_fraction"]
    write_rows(args.output_prefix + "_neighborhood_statistics.csv", statistics, fields)
    write_conclusions(args.output_prefix + "_conclusions.md", statistics, best_fitness)
    print(f"Saved standard plots, neighborhood plots, statistics, and conclusions with prefix {args.output_prefix}")


if __name__ == "__main__":
    main()