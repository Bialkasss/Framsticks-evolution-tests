"""Plot EAS4 task 2 crossover results in the Framsticks style."""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPRESENTATIONS = ("f0", "f1", "f4", "f9")
COLORS = dict(zip(REPRESENTATIONS, plt.get_cmap("viridis")(np.linspace(0.1, 0.9, len(REPRESENTATIONS)))))


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def save(figure, path):
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def feasible_rows(rows):
    return [row for row in rows if float(row["offspring_fitness"]) >= 0]


def plot_parent_best(rows_by_representation, output):
    best_fitness = max(float(row["parent_best_fitness"]) for rows in rows_by_representation.values() for row in rows if float(row["offspring_fitness"]) >= 0)
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    for axis, representation in zip(axes.flat, REPRESENTATIONS):
        rows = feasible_rows(rows_by_representation[representation])
        axis.scatter(
            [float(row["parent_best_fitness"]) for row in rows],
            [float(row["offspring_fitness"]) for row in rows],
            s=10,
            alpha=0.35,
            color=COLORS[representation],
        )
        axis.plot([0, best_fitness], [0, best_fitness], "--", color="black", linewidth=1)
        axis.set(
            title=f"{representation}: offspring vs best parent",
            xlabel="Best parent vertpos",
            ylabel="Offspring vertpos",
            xlim=(0, best_fitness),
            ylim=(0, best_fitness),
        )
        axis.grid(alpha=0.25)
    figure.suptitle("Crossover fitness relative to the better parent")
    save(figure, output)


def plot_parent_mean(rows_by_representation, output):
    best_fitness = max(float(row["parent_mean_fitness"]) for rows in rows_by_representation.values() for row in rows if float(row["offspring_fitness"]) >= 0)
    best_fitness = max(best_fitness, max(float(row["offspring_fitness"]) for rows in rows_by_representation.values() for row in rows if float(row["offspring_fitness"]) >= 0))
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    for axis, representation in zip(axes.flat, REPRESENTATIONS):
        rows = feasible_rows(rows_by_representation[representation])
        axis.scatter(
            [float(row["parent_mean_fitness"]) for row in rows],
            [float(row["offspring_fitness"]) for row in rows],
            s=10,
            alpha=0.35,
            color=COLORS[representation],
        )
        axis.plot([0, best_fitness], [0, best_fitness], "--", color="black", linewidth=1)
        axis.set(
            title=f"{representation}: offspring vs mean parent",
            xlabel="Mean parent vertpos",
            ylabel="Offspring vertpos",
            xlim=(0, best_fitness),
            ylim=(0, best_fitness),
        )
        axis.grid(alpha=0.25)
    figure.suptitle("Crossover fitness relative to the mean parent")
    save(figure, output)


def plot_improvement_rates(statistics, output):
    labels = [row["representation"] for row in statistics]
    figure, axis = plt.subplots(figsize=(10, 6))
    positions = np.arange(len(labels))
    width = 0.36
    axis.bar(positions - width / 2, [row["best_parent_rate"] for row in statistics], width, label="Better than best parent")
    axis.bar(positions + width / 2, [row["mean_parent_rate"] for row in statistics], width, label="Better than mean parent")
    axis.set_xticks(positions, labels)
    axis.set_ylim(0, 1)
    axis.set(xlabel="Representation", ylabel="Fraction of feasible offspring", title="Crossover improvement rates")
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    save(figure, output)


def calculate_statistics(rows_by_representation):
    statistics = []
    for representation in REPRESENTATIONS:
        rows = rows_by_representation[representation]
        feasible = feasible_rows(rows)
        better_best = [row for row in feasible if float(row["offspring_fitness"]) > float(row["parent_best_fitness"])]
        better_mean = [row for row in feasible if float(row["offspring_fitness"]) > float(row["parent_mean_fitness"])]
        mean_gain_best = np.mean([float(row["offspring_fitness"]) - float(row["parent_best_fitness"]) for row in feasible])
        mean_gain_mean = np.mean([float(row["offspring_fitness"]) - float(row["parent_mean_fitness"]) for row in feasible])
        statistics.append({
            "representation": representation,
            "total_crossovers": len(rows),
            "feasible_offspring": len(feasible),
            "infeasible_offspring": len(rows) - len(feasible),
            "better_than_best_parent": len(better_best),
            "best_parent_rate": len(better_best) / len(feasible) if feasible else 0.0,
            "better_than_mean_parent": len(better_mean),
            "mean_parent_rate": len(better_mean) / len(feasible) if feasible else 0.0,
            "mean_gain_vs_best_parent": mean_gain_best,
            "mean_gain_vs_mean_parent": mean_gain_mean,
        })
    return statistics


def write_statistics(path, statistics):
    fields = list(statistics[0])
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        writer.writerows(statistics)


def write_conclusions(path, statistics):
    with path.open("w", encoding="utf-8") as destination:
        destination.write("# EAS4 task 2 crossover conclusions\n\n")
        destination.write("## Motivation and data collection\n\n")
        destination.write("Task 2 tests whether crossover combines two selected task-1 solutions into an offspring with useful fitness. For every representation, pairs of sampled parents were crossed, the offspring was evaluated, and invalid offspring were excluded from fitness comparisons. The two reference quantities are the better parent and the mean of the two parents. The parent order is irrelevant because the comparisons use `max(parent1, parent2)` and `(parent1 + parent2) / 2`.\n\n")
        destination.write("## Statistics\n\n")
        destination.write("The main statistic is the best-parent improvement rate:\n\n")
        destination.write("`C_best = number of feasible offspring better than both parents / number of feasible offspring`.\n\n")
        destination.write("A complementary statistic is the mean-parent improvement rate:\n\n")
        destination.write("`C_mean = number of feasible offspring better than the mean parent / number of feasible offspring`.\n\n")
        destination.write("| Representation | Attempts | Feasible | Infeasible | Better than best | Better than mean | Mean gain vs best | Mean gain vs mean |\n|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in statistics:
            destination.write(f"| {row['representation']} | {row['total_crossovers']} | {row['feasible_offspring']} | {row['infeasible_offspring']} | {row['best_parent_rate']:.2%} | {row['mean_parent_rate']:.2%} | {row['mean_gain_vs_best_parent']:.4f} | {row['mean_gain_vs_mean_parent']:.4f} |\n")
        destination.write("""

## What the diagrams show

In both scatter plots, the dashed diagonal is `offspring fitness = reference parent fitness`. Points above the line represent beneficial crossover outcomes; points below it are worse than the reference. The best-parent plot is the stricter test: an offspring above the line is better than both inputs. The mean-parent plot asks whether crossover at least beats the average quality of the two inputs.

The clouds are mostly below the best-parent diagonal, so crossover rarely discovers a child better than the stronger parent. This indicates that crossover is not a reliable local-improvement operator in these data. The mean-parent plot has more points above its diagonal, showing that crossover can often preserve or combine useful material from one good parent while rescuing a weaker parent, even when it does not exceed the best parent.

The representation differences are visible in both the location and spread of the clouds. f4 operates over the highest absolute fitness range and produces the strongest offspring values, but many offspring still fall well below the best parent. f1 has a broad cloud and a comparatively high rate of offspring better than the mean parent. f0 has fewer successful recombinations and a lower improvement rate. f9 has the highest relative improvement rates, especially against the mean parent, but its entire fitness range is much lower; its apparent crossover success should therefore not be confused with reaching the best solutions overall.

The infeasible counts also matter. A representation can have a reasonable conditional improvement rate among feasible offspring while still producing many invalid structures. Consequently, crossover quality should be reported with both the improvement rate and the feasible-offspring rate. These conclusions describe the selected samples and this crossover operator, not all possible parent pairs in the full genotype space.
""")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    script_directory = Path(__file__).resolve().parent
    parser.add_argument("--input-directory", type=Path, default=script_directory / ".." / ".." / "Biologically-inspiredAlgorithmsAndModels" / "EAS4")
    parser.add_argument("--output-directory", type=Path, default=script_directory / "task4-2")
    args = parser.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    input_directory = args.input_directory.resolve()
    output_directory = args.output_directory.resolve()
    rows_by_representation = {
        representation: read_rows(input_directory / f"EAS4_task2_crossovers_{representation}.csv")
        for representation in REPRESENTATIONS
    }
    prefix = output_directory / "task4-2"
    statistics = calculate_statistics(rows_by_representation)
    plot_parent_best(rows_by_representation, prefix.with_name(prefix.name + "_parent_best_vs_offspring.png"))
    plot_parent_mean(rows_by_representation, prefix.with_name(prefix.name + "_parent_mean_vs_offspring.png"))
    plot_improvement_rates(statistics, prefix.with_name(prefix.name + "_improvement_rates.png"))
    write_statistics(prefix.with_name(prefix.name + "_crossover_statistics.csv"), statistics)
    write_conclusions(prefix.with_name(prefix.name + "_conclusions.md"), statistics)
    print(f"Saved task 4-2 crossover plots and analysis to {output_directory}")


if __name__ == "__main__":
    main()
