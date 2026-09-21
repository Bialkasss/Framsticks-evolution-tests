import argparse
import csv
import re
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


def read_csv(filename):
    with open(filename, newline='') as source:
        return list(csv.DictReader(source))


def filter_first_runs(rows, run_count):
    selected_runs = {str(run_id) for run_id in range(run_count)}
    return [row for row in rows if row['run'] in selected_runs]


def genetic_format_from_prefix(prefix):
    match = re.search(r'(?:^|[-_])(f\d+)(?:[-_]|$)', prefix)
    return match.group(1) if match else prefix


def group_generation_rows(rows, criterion):
    groups = defaultdict(list)
    value_name = 'best_' + criterion
    for row in rows:
        key = row['genetic_format']
        groups[key].append((int(row['run']), int(row['generation']), float(row[value_name])))
    return groups


def plot_individual_runs(rows, criterion, output, y_min):
    groups = group_generation_rows(rows, criterion)
    format_values = sorted(groups)
    colors = {genetic_format: plt.get_cmap('viridis')(index / max(1, len(format_values) - 1)) for index, genetic_format in enumerate(format_values)}
    figure, axis = plt.subplots(figsize=(10, 6))
    for genetic_format, values in sorted(groups.items()):
        runs = defaultdict(list)
        for run, generation, quality in values:
            runs[run].append((generation, quality))
        for run, run_values in sorted(runs.items()):
            run_values.sort()
            axis.plot(
                [item[0] for item in run_values],
                [item[1] for item in run_values],
                color=colors[genetic_format],
                label=genetic_format if run == min(runs) else None,
                alpha=0.75,
            )
    axis.set(title='Best individual in each evolutionary run by genetic format', xlabel='Generation', ylabel='Fitness')
    axis.set_ylim(bottom=y_min)
    axis.legend()
    axis.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def plot_aggregated_runs(rows, criterion, deviation_divisor, output, y_min):
    groups = group_generation_rows(rows, criterion)
    format_values = sorted(groups)
    colors = {genetic_format: plt.get_cmap('viridis')(index / max(1, len(format_values) - 1)) for index, genetic_format in enumerate(format_values)}
    figure, axis = plt.subplots(figsize=(10, 6))
    for genetic_format, values in sorted(groups.items()):
        by_generation = defaultdict(list)
        for _, generation, quality in values:
            by_generation[generation].append(quality)
        generations = sorted(by_generation)
        means = np.array([np.mean(by_generation[generation]) for generation in generations])
        deviations = np.array([np.std(by_generation[generation]) for generation in generations]) / deviation_divisor
        axis.plot(generations, means, color=colors[genetic_format], label=genetic_format)
        axis.fill_between(generations, means - deviations, means + deviations, color=colors[genetic_format], alpha=0.18)
    axis.set(title='Mean best fitness by genetic format with standard deviation', xlabel='Generation', ylabel='Fitness')
    axis.set_ylim(bottom=y_min)
    axis.legend()
    axis.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def plot_boxplots(rows, criterion, output):
    groups = defaultdict(lambda: {'quality': [], 'duration': []})
    for row in rows:
        genetic_format = row['genetic_format']
        groups[genetic_format]['quality'].append(float(row['hof_' + criterion]))
        groups[genetic_format]['duration'].append(float(row['duration_seconds']))
    labels = sorted(groups)
    quality_values = [groups[genetic_format]['quality'] for genetic_format in labels]
    duration_values = [groups[genetic_format]['duration'] for genetic_format in labels]

    figure, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].boxplot(quality_values, labels=labels)
    axes[0].set(title='Hall of Fame quality', xlabel='Genetic format', ylabel='Fitness')
    axes[1].boxplot(duration_values, labels=labels)
    axes[1].set(title='Evolution duration', xlabel='Genetic format', ylabel='seconds')
    for axis in axes:
        axis.grid(axis='y', alpha=0.25)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description='Plot FramsticksEvolution CSV results.')
    parser.add_argument('-prefix', nargs='+', default=['evolution_results'], help='One or more CSV prefixes used by FramsticksEvolution.py.')
    parser.add_argument('-criterion', required=True, help='Fitness criterion to plot, for example vertpos.')
    parser.add_argument('-deviation_divisor', type=float, default=1.0, help='Divide standard deviation by this value for readability.')
    parser.add_argument('-output_prefix', default='plots', help='Prefix for generated PNG files.')
    parser.add_argument('-runs_to_plot', type=int, default=5, help='Number of runs to plot from each input prefix, starting with run 0.')
    parser.add_argument('-plot_type', choices=['individual', 'aggregated', 'boxplots', 'all'], default='individual', help='Plot type to generate.')
    parser.add_argument('-y_min', type=float, default=0.4, help='Lower bound of the fitness axis.')
    args = parser.parse_args()
    if args.deviation_divisor <= 0:
        raise ValueError('-deviation_divisor must be positive')
    if args.runs_to_plot <= 0:
        raise ValueError('-runs_to_plot must be positive')
    if args.y_min is None:
        raise ValueError('-y_min must be a number')

    results = {
        prefix: (
            [dict(row, genetic_format=genetic_format_from_prefix(prefix)) for row in filter_first_runs(read_csv(prefix + '_generations.csv'), args.runs_to_plot)],
            [dict(row, genetic_format=genetic_format_from_prefix(prefix)) for row in filter_first_runs(read_csv(prefix + '_runs.csv'), args.runs_to_plot)],
        )
        for prefix in args.prefix
    }
    generation_rows = [row for prefix in args.prefix for row in results[prefix][0]]
    run_rows = [row for prefix in args.prefix for row in results[prefix][1]]
    if args.plot_type in ('individual', 'all'):
        plot_individual_runs(generation_rows, args.criterion, args.output_prefix + '_individual_runs.png', args.y_min)
    if args.plot_type in ('aggregated', 'all'):
        plot_aggregated_runs(generation_rows, args.criterion, args.deviation_divisor, args.output_prefix + '_aggregated_runs.png', args.y_min)
    if args.plot_type in ('boxplots', 'all'):
        plot_boxplots(run_rows, args.criterion, args.output_prefix + '_boxplots.png')
    print('Saved plots with prefix %s' % args.output_prefix)


if __name__ == '__main__':
    main()
