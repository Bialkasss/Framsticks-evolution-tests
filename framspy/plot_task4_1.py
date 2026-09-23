"""Plot EAS4 task 1 CSV results using the Framsticks sampling style."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPRESENTATIONS = ("f0", "f1", "f4", "f9")
LABELS = {representation: representation for representation in REPRESENTATIONS}
COLORS = dict(zip(REPRESENTATIONS, plt.get_cmap("viridis")(np.linspace(0.1, 0.9, len(REPRESENTATIONS)))))


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def save(figure, path):
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def sample_rows_with_index(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["category"], row["run_id"])].append(row)
    result = []
    for (representation, run_id), values in grouped.items():
        for sample_index, row in enumerate(sorted(values, key=lambda item: int(item["generation"]))):
            result.append((representation, run_id, sample_index, float(row["fitness"])))
    return result


def plot_individual_runs(samples, output):
    figure, axis = plt.subplots(figsize=(11, 6))
    for representation in REPRESENTATIONS:
        color = COLORS[representation]
        runs = defaultdict(list)
        for current_representation, run_id, index, fitness in samples:
            if current_representation == representation:
                runs[run_id].append((index, fitness))
        for values in runs.values():
            values.sort()
            axis.plot([item[0] for item in values], [item[1] for item in values], alpha=0.22, color=color)
        axis.plot([], [], color=color, label=LABELS[representation])
    axis.set(title="Vertpos samples in independent optimization runs", xlabel="Sample index", ylabel="Vertpos")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.25)
    axis.legend()
    save(figure, output)


def plot_aggregated_runs(samples, output):
    figure, axis = plt.subplots(figsize=(11, 6))
    for representation in REPRESENTATIONS:
        by_index = defaultdict(list)
        for current_representation, _, index, fitness in samples:
            if current_representation == representation:
                by_index[index].append(fitness)
        indices = sorted(by_index)
        means = np.array([np.mean(by_index[index]) for index in indices])
        deviations = np.array([np.std(by_index[index]) for index in indices])
        color = COLORS[representation]
        axis.plot(indices, means, color=color, label=LABELS[representation])
        axis.fill_between(indices, means - deviations, means + deviations, color=color, alpha=0.16)
    axis.set(title="Mean vertpos samples with standard deviation", xlabel="Sample index", ylabel="Vertpos")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.25)
    axis.legend()
    save(figure, output)


def plot_boxplots(summary_rows, output):
    values = [[float(row["best_fitness"]) for row in summary_rows if row["mutation_intensity"] == representation] for representation in REPRESENTATIONS]
    durations = [[float(row["elapsed_time_seconds"]) for row in summary_rows if row["mutation_intensity"] == representation] for representation in REPRESENTATIONS]
    figure, axes = plt.subplots(1, 2, figsize=(12, 6))
    labels = [LABELS[representation] for representation in REPRESENTATIONS]
    fitness_boxes = axes[0].boxplot(values, tick_labels=labels, patch_artist=True)
    for patch, representation in zip(fitness_boxes["boxes"], REPRESENTATIONS):
        patch.set_facecolor(COLORS[representation])
        patch.set_alpha(0.65)
    axes[0].set(title="Terminal sample vertpos", xlabel="Representation", ylabel="Vertpos")
    axes[0].set_ylim(bottom=0)
    duration_boxes = axes[1].boxplot(durations, tick_labels=labels, patch_artist=True)
    for patch, representation in zip(duration_boxes["boxes"], REPRESENTATIONS):
        patch.set_facecolor(COLORS[representation])
        patch.set_alpha(0.65)
    axes[1].set(title="Evolution time", xlabel="Representation", ylabel="Time [seconds]")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    save(figure, output)


def plot_histograms(samples, output):
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    all_values = [fitness for representation, _, _, fitness in samples if fitness >= 0]
    best_fitness = max(all_values)
    for axis, representation in zip(axes.flat, REPRESENTATIONS):
        values = [fitness for current_representation, _, _, fitness in samples if current_representation == representation and fitness >= 0]
        axis.hist(values, bins=25, color=COLORS[representation], alpha=0.8)
        axis.set(title=f"Saved sample fitness: {LABELS[representation]}", xlabel="Vertpos", ylabel="Count", xlim=(0, best_fitness))
        axis.grid(alpha=0.25)
    figure.suptitle("Fitness distribution of collected samples")
    save(figure, output)


def plot_neighborhoods(neighbor_rows, best_fitness, output_prefix):
    for representation in REPRESENTATIONS:
        rows = [row for row in neighbor_rows if row["category"] == representation and float(row["mutant_fitness"]) >= 0]
        figure, axis = plt.subplots(figsize=(7, 7))
        axis.scatter(
            [float(row["parent_fitness"]) for row in rows],
            [float(row["mutant_fitness"]) for row in rows],
            s=10,
            alpha=0.35,
            color=COLORS[representation],
        )
        axis.plot([0, best_fitness], [0, best_fitness], color="black", linestyle="--", linewidth=1, label="y=x")
        axis.set(
            xlim=(0, best_fitness),
            ylim=(0, best_fitness),
            title=f"{LABELS[representation]} mutant neighborhoods",
            xlabel="Parent vertpos",
            ylabel="Mutant vertpos",
        )
        axis.grid(alpha=0.25)
        axis.legend()
        save(figure, output_prefix.parent / f"{output_prefix.name}_neighborhood_{LABELS[representation]}.png")


def plot_combined_neighborhoods(neighbor_rows, best_fitness, output):
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    for axis, representation in zip(axes.flat, REPRESENTATIONS):
        rows = [row for row in neighbor_rows if row["category"] == representation and float(row["mutant_fitness"]) >= 0]
        axis.scatter(
            [float(row["parent_fitness"]) for row in rows],
            [float(row["mutant_fitness"]) for row in rows],
            s=10,
            alpha=0.35,
            color=COLORS[representation],
        )
        axis.plot([0, best_fitness], [0, best_fitness], color="black", linestyle="--", linewidth=1)
        axis.set(title=f"{LABELS[representation]} mutant neighborhoods", xlabel="Parent vertpos", ylabel="Mutant vertpos")
        axis.grid(alpha=0.25)
    for axis in axes.flat:
        axis.set_xlim(0, best_fitness)
        axis.set_ylim(0, best_fitness)
    figure.suptitle("Mutant fitness neighborhoods")
    save(figure, output)


def calculate_statistics(neighbor_rows):
    statistics = []
    for representation in REPRESENTATIONS:
        rows = [row for row in neighbor_rows if row["category"] == representation]
        feasible = [row for row in rows if float(row["mutant_fitness"]) >= 0]
        better = [row for row in feasible if float(row["mutant_fitness"]) > float(row["parent_fitness"])]
        statistics.append({
            "representation": representation,
            "total_neighbors": len(rows),
            "feasible_neighbors": len(feasible),
            "improving_neighbors": len(better),
            "fraction_improving": len(better) / len(feasible) if feasible else 0.0,
        })
    return statistics


def write_statistics(path, statistics):
    fields = ["representation", "total_neighbors", "feasible_neighbors", "improving_neighbors", "fraction_improving"]
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        writer.writerows(statistics)


def write_conclusions(path, statistics, best_fitness):
    with path.open("w", encoding="utf-8") as destination:
        destination.write("# EAS4 task 1 landscape conclusions\n\n")
        destination.write(f"The common neighborhood plot scale is 0 to {best_fitness:.12g}, the best sampled vertpos across all representations.\n\n")
        destination.write("The separate neighborhood plots show mutant fitness around collected parents. Points above the y=x line improve on their parent; points below it are worse. Negative mutant fitness values were treated as infeasible and omitted.\n\n")
        destination.write("The improving-mutant fractions are:\n\n")
        for row in statistics:
            destination.write(f"- {row['representation']}: {row['fraction_improving']:.2%} ({row['improving_neighbors']}/{row['feasible_neighbors']} feasible mutants)\n")
        destination.write("\nThe dispersed clouds and many low-fitness neighbors indicate a rugged, non-convex local landscape. f4 has the highest observed fitness and the greatest fraction of improving neighbors in these samples, while f9 has the lowest fitness range and fewest improving neighbors. These conclusions describe the sampled neighborhoods, not the complete combinatorial search space.\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    script_directory = Path(__file__).resolve().parent
    parser.add_argument("--input-directory", type=Path, default=script_directory / ".." / ".." / "Biologically-inspiredAlgorithmsAndModels" / "EAS4")
    parser.add_argument("--output-directory", type=Path, default=script_directory / "task4-1")
    args = parser.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)

    input_directory = args.input_directory.resolve()
    output_directory = args.output_directory.resolve()
    samples = read_rows(input_directory / "EAS4_task1_landscape_samples.csv")
    summary = read_rows(input_directory / "EAS4_task1_landscape_summary.csv")
    neighbors = read_rows(input_directory / "EAS4_task1B_landscape_neighbors.csv")
    sample_values = sample_rows_with_index(samples)
    best_fitness = max(float(row["best_fitness"]) for row in summary)
    prefix = output_directory / "task4-1"

    plot_individual_runs(sample_values, prefix.with_name(prefix.name + "_individual_runs.png"))
    plot_aggregated_runs(sample_values, prefix.with_name(prefix.name + "_aggregated_runs.png"))
    plot_boxplots(summary, prefix.with_name(prefix.name + "_boxplots.png"))
    plot_histograms(sample_values, prefix.with_name(prefix.name + "_fitness_histograms.png"))
    plot_neighborhoods(neighbors, best_fitness, prefix)
    plot_combined_neighborhoods(neighbors, best_fitness, prefix.with_name(prefix.name + "_neighborhoods.png"))
    statistics = calculate_statistics(neighbors)
    write_statistics(prefix.with_name(prefix.name + "_neighborhood_statistics.csv"), statistics)
    write_conclusions(prefix.with_name(prefix.name + "_conclusions.md"), statistics, best_fitness)
    print(f"Saved Framsticks-style task 4-1 plots to {output_directory}")


if __name__ == "__main__":
    main()
