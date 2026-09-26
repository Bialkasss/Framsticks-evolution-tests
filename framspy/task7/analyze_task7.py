from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "analysis_outputs_readable"

DATASETS = [
    ("1st-try", "task7-f1-combined", "1. F1 endpoint", "f1"),
    ("2nd-try-big-one-move", "task7-f1-combined", "2. F1 endpoint + oscillators", "f1"),
    ("3try- 2.0 small move-bigger-world", "task7-f1-sustained", "3. F1 sustained", "f1"),
    ("4th-swimmer-lower-penalties", "task7-f1-sustained", "4. F1 lower drift penalties", "f1"),
    ("5th-try-it-swimmmsss", "task7-f1-compromise", "Final F1", "f1"),
    ("6th try-F4", "task7-f4-compromise", "Final F4", "f4"),
]

FITNESS_NOTES = {
    "1. F1 endpoint": "Endpoint fitness; different from later runs",
    "2. F1 endpoint + oscillators": "Endpoint fitness; different from later runs",
    "3. F1 sustained": "Sustained performance-window fitness",
    "4. F1 lower drift penalties": "Sustained fitness with softer drift penalties",
    "Final F1": "Weighted early/late sustained fitness",
    "Final F4": "Weighted early/late sustained fitness",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as source:
        return list(csv.DictReader(source))


def grouped(rows: list[dict[str, str]]) -> dict[int, list[dict[str, str]]]:
    result: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(int(row["run"]), []).append(row)
    for run_rows in result.values():
        run_rows.sort(key=lambda row: int(row["generation"]))
    return result


def summarize(run_rows: dict[int, list[dict[str, str]]]) -> list[dict[str, object]]:
    summaries = []
    for run, rows in sorted(run_rows.items()):
        values = [float(row["best_velocity"]) for row in rows]
        best = max(values)
        best_index = values.index(best)
        best_generation = int(rows[best_index]["generation"])
        improvements = sum(
            values[index] > max(values[:index]) + 1e-12
            for index in range(1, len(values))
        )
        summaries.append(
            {
                "run": run,
                "best_fitness": best,
                "best_generation": best_generation,
                "completed_generations": int(rows[-1]["generation"]),
                "duration_seconds": float(rows[-1].get("duration_seconds", 0) or 0),
                "first_positive_generation": next(
                    (int(row["generation"]) for row in rows if float(row["best_velocity"]) > 1e-6),
                    "",
                ),
                "improvements": improvements,
                "trailing_generations": int(rows[-1]["generation"]) - best_generation,
            }
        )
    return summaries


def mean_curve(run_rows: dict[int, list[dict[str, str]]]):
    values_by_generation: dict[int, list[float]] = {}
    for rows in run_rows.values():
        for row in rows:
            values_by_generation.setdefault(int(row["generation"]), []).append(float(row["best_velocity"]))
    generations = np.array(sorted(values_by_generation))
    means = np.array([np.mean(values_by_generation[g]) for g in generations])
    deviations = np.array([np.std(values_by_generation[g]) for g in generations])
    return generations, means, deviations


def save_summary(summary_rows: list[dict[str, object]]) -> None:
    fields = [field for field in summary_rows[0] if field != "approach"]
    with (OUTPUT / "task7_all_runs_summary.csv").open("w", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=["approach"] + fields)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    grouped_rows: dict[str, list[dict[str, object]]] = {}
    for row in summary_rows:
        grouped_rows.setdefault(str(row["approach"]), []).append(row)
    with (OUTPUT / "task7_report_summary.md").open("w", encoding="ascii") as target:
        target.write("# Task 7 run summary\n\n")
        target.write("| Approach | Mean | Median | Stddev | Min | Max | Runs > 1 | Mean completed generations |\n")
        target.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for approach, rows in grouped_rows.items():
            scores = np.array([float(row["best_fitness"]) for row in rows])
            completed = np.array([int(row["completed_generations"]) for row in rows])
            target.write(
                f"| {approach} | {scores.mean():.4f} | {np.median(scores):.4f} | "
                f"{scores.std():.4f} | {scores.min():.4f} | {scores.max():.4f} | "
                f"{int((scores > 1).sum())} | {completed.mean():.1f} |\n"
            )
        target.write("\nThe per-run rows below show best-generation timing and stagnation behavior.\n\n")
        target.write("| Approach | Run | Best generation | Best fitness | Completed generations | Improvements | Trailing generations |\n")
        target.write("|---|---:|---:|---:|---:|---:|---:|\n")
        for row in summary_rows:
            target.write(
                f"| {row['approach']} | {row['run']} | {row['best_generation']} | "
                f"{float(row['best_fitness']):.4f} | {row['completed_generations']} | "
                f"{row['improvements']} | {row['trailing_generations']} |\n"
            )


def plot_approach(label, run_rows, slug):
    generations, means, deviations = mean_curve(run_rows)
    figure, axis = plt.subplots(figsize=(12, 6.5))
    colors = plt.get_cmap("tab10")
    for run, rows in sorted(run_rows.items()):
        axis.plot(
            [int(row["generation"]) for row in rows],
            [float(row["best_velocity"]) for row in rows],
            color=colors(run % 10),
            alpha=0.72,
            linewidth=1.2,
            label=f"Run {run + 1}",
        )
    axis.plot(generations, means, color="black", linewidth=2, label="mean best fitness")
    axis.fill_between(generations, means - deviations, means + deviations, color="black", alpha=0.12, label="mean +/- 1 stddev")
    axis.set_title(f"{label}: best fitness by generation\n{FITNESS_NOTES[label]}")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Fitness")
    axis.grid(alpha=0.25)
    axis.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    figure.tight_layout(rect=[0, 0, 0.84, 1])
    figure.savefig(OUTPUT / f"{slug}_convergence.png", dpi=160)
    plt.close(figure)

    scores = [max(float(row["best_velocity"]) for row in rows) for rows in run_rows.values()]
    figure, axis = plt.subplots(figsize=(7, 5))
    axis.boxplot(scores, tick_labels=[label], showmeans=True)
    axis.set_ylabel("Best fitness")
    axis.set_title(f"{label}: best-fitness distribution\n{FITNESS_NOTES[label]}")
    axis.tick_params(axis="x", labelrotation=15)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT / f"{slug}_boxplot.png", dpi=160)
    plt.close(figure)


def plot_all_approaches(dataset_data):
    figure, axis = plt.subplots(figsize=(12, 7))
    for label, run_rows, _slug, _representation in dataset_data:
        generations, means, deviations = mean_curve(run_rows)
        axis.plot(generations, means, linewidth=2, label=label)
        axis.fill_between(generations, means - deviations, means + deviations, alpha=0.08)
    axis.set_title("Task 7: mean convergence across all approaches")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Best fitness")
    axis.grid(alpha=0.25)
    axis.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    figure.text(0.01, 0.01, "Runs 1-2 use endpoint fitness; runs 3-6 use sustained/windowed fitness.", fontsize=9)
    figure.tight_layout(rect=[0, 0.04, 0.82, 1])
    figure.savefig(OUTPUT / "task7_all_approaches_convergence.png", dpi=160)
    plt.close(figure)


def plot_f1_f4(dataset_data):
    selected = [item for item in dataset_data if item[0] in {"Final F1", "Final F4"}]
    figure, axis = plt.subplots(figsize=(10, 6))
    for label, run_rows, _slug, _representation in selected:
        generations, means, deviations = mean_curve(run_rows)
        axis.plot(generations, means, linewidth=2, label=label)
        axis.fill_between(generations, means - deviations, means + deviations, alpha=0.12)
    axis.set_title("Final F1 versus Final F4\nSame environment and weighted sustained fitness")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Best fitness")
    axis.grid(alpha=0.25)
    axis.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
    figure.tight_layout(rect=[0, 0, 0.82, 1])
    figure.savefig(OUTPUT / "task7_f1_vs_f4_convergence.png", dpi=160)
    plt.close(figure)

    scores = []
    labels = []
    for label, run_rows, _slug, _representation in selected:
        labels.append(label)
        scores.append([max(float(row["best_velocity"]) for row in rows) for rows in run_rows.values()])
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.boxplot(scores, tick_labels=labels, showmeans=True)
    axis.set_ylabel("Best fitness")
    axis.set_title("Final F1 versus Final F4: best-fitness distributions")
    axis.tick_params(axis="x", labelrotation=15)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT / "task7_f1_vs_f4_boxplot.png", dpi=160)
    plt.close(figure)


def plot_best_runs(dataset_data, summaries):
    figure, axis = plt.subplots(figsize=(12, 7))
    for label, run_rows, _slug, _representation in dataset_data:
        rows = [row for row in summaries if row["approach"] == label]
        best_summary = max(rows, key=lambda row: float(row["best_fitness"]))
        best_run_rows = run_rows[int(best_summary["run"])]
        axis.plot(
            [int(row["generation"]) for row in best_run_rows],
            [float(row["best_velocity"]) for row in best_run_rows],
            linewidth=2,
            label=f"{label} (run {best_summary['run']})",
        )
    axis.set_title("Task 7: best run from each approach")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Best fitness")
    axis.grid(alpha=0.25)
    axis.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    figure.tight_layout(rect=[0, 0, 0.82, 1])
    figure.savefig(OUTPUT / "task7_best_run_each_approach.png", dpi=160)
    plt.close(figure)


def main():
    OUTPUT.mkdir(exist_ok=True)
    dataset_data = []
    all_summary_rows = []
    for folder, prefix, label, representation in DATASETS:
        directory = ROOT / folder
        run_rows = grouped(read_csv(directory / f"{prefix}_generations.csv"))
        summaries = summarize(run_rows)
        for summary in summaries:
            summary["approach"] = label
            summary["representation"] = representation
            all_summary_rows.append(summary)
        slug = label.lower().replace(" ", "_").replace(".", "").replace("+", "plus")
        dataset_data.append((label, run_rows, slug, representation))
        plot_approach(label, run_rows, slug)
    save_summary(all_summary_rows)
    plot_all_approaches(dataset_data)
    plot_f1_f4(dataset_data)
    plot_best_runs(dataset_data, all_summary_rows)
    print(f"Generated outputs in {OUTPUT}")


if __name__ == "__main__":
    main()
