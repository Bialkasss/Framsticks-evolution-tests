"""Plot EAS4 task 3 sequential mutation random walks."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPRESENTATIONS = ("f0", "f1", "f4", "f9")
RANK_GROUPS = ("best", "high", "medium", "worst")
GROUP_LABELS = {"best": "Best 5", "high": "High 5", "medium": "Medium 5", "worst": "Worst 5"}
GROUP_COLORS = {
    "best": "lightgreen",
    "high": "darkblue",
    "medium": "orange",
    "worst": "red",
}


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def validate_walks(all_walks):
    expected_steps = set(range(31))
    for representation, walks in all_walks.items():
        if len(walks) != 20:
            raise ValueError(f"Expected 20 walks for {representation}, found {len(walks)}")
        for walk_id, walk in walks.items():
            steps = {int(row["step"]) for row in walk}
            if steps != expected_steps or len(walk) != 31:
                raise ValueError(f"Walk {walk_id} in {representation} does not contain steps 0 through 30")
            if any(float(row["fitness"]) < 0 for row in walk):
                raise ValueError(f"Walk {walk_id} in {representation} contains an infeasible fitness")


def assign_quality_groups(all_walks):
    for walks in all_walks.values():
        ordered_walks = sorted(walks.values(), key=lambda walk: float(walk[0]["fitness"]), reverse=True)
        for index, walk in enumerate(ordered_walks):
            group = RANK_GROUPS[min(index // 5, len(RANK_GROUPS) - 1)]
            for row in walk:
                row["rank_group"] = group


def save(figure, path):
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def group_walks(rows):
    walks = defaultdict(list)
    for row in rows:
        walks[row["walk_id"]].append(row)
    return {
        walk_id: sorted(values, key=lambda row: int(row["step"]))
        for walk_id, values in walks.items()
    }


def plot_representation(walks, representation, output):
    figure, axis = plt.subplots(figsize=(10, 6))
    for walk in walks.values():
        group = walk[0]["rank_group"]
        axis.plot(
            [int(row["step"]) for row in walk],
            [float(row["fitness"]) for row in walk],
            color=GROUP_COLORS[group],
            alpha=0.65,
        )
    for group in RANK_GROUPS:
        axis.plot([], [], color=GROUP_COLORS[group], label=GROUP_LABELS[group])
    axis.set(
        title=f"Random fitness walks: {representation}",
        xlabel="Mutation step",
        ylabel="Vertpos",
        xlim=(0, 30),
    )
    axis.grid(alpha=0.25)
    axis.legend(title="Initial solution quality")
    save(figure, output)


def plot_combined(all_walks, output):
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=False)
    for axis, representation in zip(axes.flat, REPRESENTATIONS):
        walks = all_walks[representation]
        for walk in walks.values():
            group = walk[0]["rank_group"]
            axis.plot(
                [int(row["step"]) for row in walk],
                [float(row["fitness"]) for row in walk],
                color=GROUP_COLORS[group],
                alpha=0.65,
            )
        for group in RANK_GROUPS:
            axis.plot([], [], color=GROUP_COLORS[group], label=GROUP_LABELS[group])
        axis.set(title=f"Random fitness walks: {representation}", xlabel="Mutation step", ylabel="Vertpos", xlim=(0, 30))
        axis.grid(alpha=0.25)
        axis.legend(fontsize="small")
    figure.suptitle("Random walks in the fitness landscape")
    save(figure, output)


def calculate_statistics(all_walks):
    statistics = []
    for representation in REPRESENTATIONS:
        for walk_id, walk in all_walks[representation].items():
            values = np.array([float(row["fitness"]) for row in walk])
            changes = np.diff(values)
            statistics.append({
                "representation": representation,
                "walk_id": walk_id,
                "rank_group": walk[0]["rank_group"],
                "initial_fitness": values[0],
                "final_fitness": values[-1],
                "net_change": values[-1] - values[0],
                "mean_fitness": np.mean(values),
                "mean_step_change": np.mean(changes),
                "step_change_std": np.std(changes),
                "minimum_fitness": np.min(values),
                "maximum_fitness": np.max(values),
                "steps_above_start": int(np.sum(values[1:] > values[0])),
                "infeasible_points": int(np.sum(values < 0)),
            })
    return statistics


def write_statistics(path, statistics):
    fields = list(statistics[0])
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        writer.writerows(statistics)


def write_group_summary(path, statistics):
    fields = ["representation", "rank_group", "walks", "mean_initial_fitness", "mean_final_fitness", "mean_net_change", "mean_fitness", "mean_step_change", "mean_step_change_std", "mean_steps_above_start"]
    rows = []
    for representation in REPRESENTATIONS:
        for rank_group in RANK_GROUPS:
            group = [row for row in statistics if row["representation"] == representation and row["rank_group"] == rank_group]
            rows.append({
                "representation": representation,
                "rank_group": rank_group,
                "walks": len(group),
                "mean_initial_fitness": np.mean([row["initial_fitness"] for row in group]),
                "mean_final_fitness": np.mean([row["final_fitness"] for row in group]),
                "mean_net_change": np.mean([row["net_change"] for row in group]),
                "mean_fitness": np.mean([row["mean_fitness"] for row in group]),
                "mean_step_change": np.mean([row["mean_step_change"] for row in group]),
                "mean_step_change_std": np.mean([row["step_change_std"] for row in group]),
                "mean_steps_above_start": np.mean([row["steps_above_start"] for row in group]),
            })
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_conclusions(path, statistics):
    with path.open("w", encoding="utf-8") as destination:
        destination.write("# EAS4 task 3 random-walk conclusions\n\n")
        destination.write("## Motivation and data collection\n\n")
        destination.write("Task 3 probes local landscape memory and mutation behavior. Twenty genotype-distinct feasible solutions per representation were selected across the observed fitness range: five best, five high, five medium, and five worst. Each selected solution is the starting point of one sequential 30-step random walk. At every step, the current genotype was mutated and evaluated; invalid genotypes and infeasible fitness values were discarded and mutation was retried until a feasible mutant was obtained. The recreated data therefore contains 80 walks with 31 valid recorded points each, including the starting point.\n\n")
        destination.write("## What to look for in the diagrams\n\n")
        destination.write("Each line is one trajectory. The first point is the starting fitness, and the horizontal axis is mutation distance in the sequence, not an independent sample number. Line color identifies the starting-quality group. A trajectory that quickly forgets its initial fitness and joins the same region as other trajectories suggests weak local memory or a broad, mixing mutation operator. Trajectories that remain near their starting level suggest stronger local retention and smoother or more constrained neighborhoods.\n\n")
        destination.write("## Summary of observed walks\n\n")
        destination.write("| Representation | Initial mean range | Final mean range | Mean net change range | Infeasible points |\n|---|---:|---:|---:|---:|\n")
        for representation in REPRESENTATIONS:
            group = [row for row in statistics if row["representation"] == representation]
            initial = [row["initial_fitness"] for row in group]
            final = [row["final_fitness"] for row in group]
            change = [row["net_change"] for row in group]
            invalid = sum(row["infeasible_points"] for row in group)
            destination.write(f"| {representation} | {min(initial):.3f}-{max(initial):.3f} | {min(final):.3f}-{max(final):.3f} | {min(change):.3f}-{max(change):.3f} | {invalid} |\n")
        destination.write("""

## Conclusions

The trajectories show that one mutation can cause a large fitness change, but the effect depends strongly on the starting representation and fitness level. The lines are generally jagged rather than smooth, which is consistent with a rugged combinatorial landscape and with mutation operators that make structural changes rather than small numerical movements.

The best-starting trajectories often fall rapidly after the first few mutations. This is expected in a maximization landscape: a high-fitness solution is surrounded by many solutions that are worse, so random mutation usually leaves the favorable basin. In contrast, the worst-starting trajectories can rise initially because low-fitness solutions have more room for improvement, although they can also fluctuate or become trapped at low values.

The walks also show landscape memory. If trajectories from different starting groups converge toward a similar fitness band, repeated mutation is gradually forgetting the starting solution. If high-start and low-start trajectories remain separated, the landscape has stronger local retention or disconnected regions under the mutation operator. The plots should therefore be interpreted as the combined effect of landscape topology and the particular Framsticks mutation operator.

Across representations, f4 explores the widest fitness range and can retain high values for several steps, but it also shows large downward excursions. f9 is concentrated in a much lower fitness band and its trajectories tend to remain near that band, indicating a more constrained representation or mutation neighborhood. f0 and f1 are intermediate: they show substantial fluctuations and partial convergence across starting groups. The difference between representations is therefore not only their best reachable fitness, but also how quickly random mutation destroys or preserves fitness information.

These walks do not measure optimization performance directly. They measure how fitness changes when selection is removed and mutation is applied repeatedly. The conclusions are local and conditional on the selected starting solutions, the 30-step horizon, the retry rule for invalid mutants, and the mutation operator. Since the recreated files retain only successful evaluations, comparisons describe the valid-mutant sequence rather than the raw frequency of invalid mutation attempts.
""")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    script_directory = Path(__file__).resolve().parent
    parser.add_argument("--input-file", type=Path, default=script_directory / "task4-3-recreate" / "task4-3_recreated_random_walks_all.csv")
    parser.add_argument("--output-directory", type=Path, default=script_directory / "task4-3")
    args = parser.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    input_file = args.input_file.resolve()
    output_directory = args.output_directory.resolve()
    all_walks = {
        representation: group_walks([
            row for row in read_rows(input_file)
            if row["category"] == representation
        ])
        for representation in REPRESENTATIONS
    }
    assign_quality_groups(all_walks)
    validate_walks(all_walks)
    prefix = output_directory / "task4-3"
    plot_combined(all_walks, prefix.with_name(prefix.name + "_random_walks.png"))
    for representation in REPRESENTATIONS:
        plot_representation(all_walks[representation], representation, prefix.with_name(prefix.name + f"_random_walks_{representation}.png"))
    statistics = calculate_statistics(all_walks)
    write_statistics(prefix.with_name(prefix.name + "_walk_statistics.csv"), statistics)
    write_group_summary(prefix.with_name(prefix.name + "_group_summary.csv"), statistics)
    write_conclusions(prefix.with_name(prefix.name + "_conclusions.md"), statistics)
    print(f"Saved task 4-3 random-walk plots and analysis to {output_directory}")


if __name__ == "__main__":
    main()
