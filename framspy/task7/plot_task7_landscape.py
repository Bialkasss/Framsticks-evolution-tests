#!/usr/bin/env python3
"""Plot task7 local mutant neighborhoods in the style of the Task 4 landscape plots."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DIR = SCRIPT_DIR / "analysis_outputs_readable" / "landscape"
REPRESENTATIONS = ("Final F1", "Final F4")
COLORS = {"Final F1": "#2878b5", "Final F4": "#d95f02"}
GROUP_COLORS = {"best": "#2ca25f", "middle": "#756bb1", "worst": "#de2d26"}


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def save(figure, path):
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def feasible(rows):
    return [row for row in rows if row["status"] == "feasible"]


def plot_neighborhoods(rows, output):
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharex=True, sharey=True)
    upper = max(float(row["parent_fitness"]) for row in rows if row["status"] == "feasible")
    upper *= 1.08
    for axis, representation in zip(axes, REPRESENTATIONS):
        current = feasible([row for row in rows if row["representation"] == representation])
        axis.scatter(
            [float(row["parent_fitness"]) for row in current],
            [float(row["mutant_fitness"]) for row in current],
            s=22,
            alpha=0.45,
            color=COLORS[representation],
            label="feasible mutants",
        )
        axis.plot([0, upper], [0, upper], "k--", linewidth=1, label="mutant = parent")
        axis.set_title(representation)
        axis.set_xlabel("Parent fitness")
        axis.set_ylabel("Mutant fitness")
        axis.set_xlim(0, upper)
        axis.set_ylim(0, upper)
        axis.grid(alpha=0.25)
        axis.legend(fontsize="small")
    figure.suptitle("Local mutant neighborhoods\nPoints above the diagonal improve on the parent")
    save(figure, output)


def plot_delta(rows, output):
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
    for axis, representation in zip(axes, REPRESENTATIONS):
        current = feasible([row for row in rows if row["representation"] == representation])
        groups = defaultdict(list)
        for row in current:
            groups[row["rank_group"]].append(float(row["delta_fitness"]))
        values = [groups[group] for group in ("worst", "middle", "best")]
        boxes = axis.boxplot(values, tick_labels=["Worst parent", "Middle parents", "Best parent"], patch_artist=True, showmeans=True)
        for patch, group in zip(boxes["boxes"], ("worst", "middle", "best")):
            patch.set_facecolor(GROUP_COLORS[group])
            patch.set_alpha(0.65)
        axis.axhline(0, color="black", linestyle="--", linewidth=1)
        axis.set_title(representation)
        axis.set_xlabel("Parent quality group")
        axis.grid(axis="y", alpha=0.25)
        axis.tick_params(axis="x", labelrotation=18)
    axes[0].set_ylabel("Delta fitness of mutant compared to parent")
    figure.suptitle("Local fitness changes after one mutation")
    save(figure, output)


def plot_improvement_rates(rows, output):
    labels = []
    rates = []
    errors = []
    for representation in REPRESENTATIONS:
        current = feasible([row for row in rows if row["representation"] == representation])
        by_parent = defaultdict(list)
        for row in current:
            by_parent[row["parent_id"]].append(float(row["delta_fitness"]))
        parent_rates = [np.mean(np.array(values) > 0) for values in by_parent.values()]
        labels.append(representation)
        rates.append(float(np.mean(parent_rates)))
        errors.append(float(np.std(parent_rates)))
    figure, axis = plt.subplots(figsize=(7, 5))
    bars = axis.bar(labels, rates, yerr=errors, color=[COLORS[label] for label in labels], alpha=0.75, capsize=5)
    axis.set_ylim(0, 1)
    axis.set_ylabel("Fraction of improving mutants")
    axis.set_title("Local improvement probability")
    axis.grid(axis="y", alpha=0.25)
    for bar, rate in zip(bars, rates):
        axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03, f"{rate:.1%}", ha="center")
    save(figure, output)


def write_conclusions(rows, output):
    with output.open("w", encoding="ascii") as target:
        target.write("# Task 7 local fitness landscape\n\n")
        target.write("Each point is a one-mutation neighbor of a selected final-run parent. Points above the diagonal in the neighborhood plot improve fitness; points below it reduce fitness. The sampled landscape is local and depends on the Framsticks mutation operator.\n\n")
        for representation in REPRESENTATIONS:
            current = feasible([row for row in rows if row["representation"] == representation])
            deltas = np.array([float(row["delta_fitness"]) for row in current])
            rate = np.mean(deltas > 0)
            target.write(f"- {representation}: {len(current)} feasible neighbors, mean delta {deltas.mean():.4f}, improving fraction {rate:.2%}.\n")
        target.write("\nA broad vertical spread indicates a rugged neighborhood. Many points below the diagonal indicate that high-fitness parents are surrounded mostly by harmful mutations. Points above the diagonal around lower-fitness parents indicate room for local improvement. These results describe sampled neighborhoods, not the complete genotype landscape.\n")


def main():
    input_dir = DEFAULT_DIR
    rows = read_rows(input_dir / "task7_landscape_neighborhoods.csv")
    plot_neighborhoods(rows, input_dir / "task7_landscape_neighborhoods.png")
    plot_delta(rows, input_dir / "task7_landscape_delta_boxplots.png")
    plot_improvement_rates(rows, input_dir / "task7_landscape_improvement_rates.png")
    write_conclusions(rows, input_dir / "task7_landscape_conclusions.md")
    print(f"Saved landscape plots and conclusions to {input_dir}")


if __name__ == "__main__":
    main()
