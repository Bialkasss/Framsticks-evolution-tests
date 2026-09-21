import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def read_csv(filename):
    with open(filename, newline='') as source:
        return list(csv.DictReader(source))


def filter_first_runs(rows, run_count):
    selected_runs = {str(run_id) for run_id in range(run_count)}
    return [row for row in rows if row['run'] in selected_runs]


def label_from_prefix(prefix):
    label = Path(prefix).name
    if label.startswith('results-'):
        label = label[len('results-'):]
    return label.replace('-', ' ')


def group_generation_rows(rows, criterion):
    groups = defaultdict(list)
    value_name = 'best_' + criterion
    for row in rows:
        key = row['label']
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
    axis.set(title='(Penalty) Best individual in each evolutionary run by genetic format', xlabel='Generation', ylabel='Fitness')
    if y_min is not None:
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
    axis.set(title='(Penalty) Mean best fitness by genetic format with standard deviation', xlabel='Generation', ylabel='Fitness')
    if y_min is not None:
        axis.set_ylim(bottom=y_min)
    axis.legend()
    axis.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def plot_boxplots(rows, criterion, output):
    groups = defaultdict(lambda: {'quality': [], 'duration': []})
    for row in rows:
        genetic_format = row['label']
        groups[genetic_format]['quality'].append(float(row['hof_' + criterion]))
        groups[genetic_format]['duration'].append(float(row['duration_seconds']))
    labels = sorted(groups)
    quality_values = [groups[genetic_format]['quality'] for genetic_format in labels]
    duration_values = [groups[genetic_format]['duration'] for genetic_format in labels]

    figure, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].boxplot(quality_values, labels=labels)
    axes[0].set(title='(Penalty) Hall of Fame quality', xlabel='Genetic format', ylabel='Fitness')
    axes[1].boxplot(duration_values, labels=labels)
    axes[1].set(title='(Penalty) Evolution duration', xlabel='Genetic format', ylabel='seconds')
    for axis in axes:
        axis.grid(axis='y', alpha=0.25)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description='Plot FramsticksEvolution CSV results.')
    parser.add_argument('-prefix', nargs='+', help='One or more CSV prefixes used by FramsticksEvolution.py. If omitted, matching files are discovered automatically.')
    parser.add_argument('-directory', default='.', help='Directory to search when -prefix is omitted. Default: current directory.')
    parser.add_argument('-criterion', required=True, help='Fitness criterion to plot, for example vertpos.')
    parser.add_argument('-deviation_divisor', type=float, default=1.0, help='Divide standard deviation by this value for readability.')
    parser.add_argument('-output_prefix', default='plots', help='Prefix for generated PNG files.')
    parser.add_argument('-runs_to_plot', type=int, default=5, help='Number of runs to plot from each input prefix, starting with run 0.')
    parser.add_argument('-plot_type', choices=['individual', 'aggregated', 'boxplots', 'all'], default='individual', help='Plot type to generate.')
    parser.add_argument('-y_min', type=float, default=None, help='Optional lower bound of the fitness axis. By default, matplotlib chooses it.')
    args = parser.parse_args()
    if args.deviation_divisor <= 0:
        raise ValueError('-deviation_divisor must be positive')
    if args.runs_to_plot <= 0:
        raise ValueError('-runs_to_plot must be positive')
    if args.y_min is None:
        raise ValueError('-y_min must be a number')

    if args.prefix:
        prefixes = args.prefix
    else:
        directory = Path(args.directory)
        prefixes = sorted(
            str(path.with_name(path.name[:-len('_generations.csv')] ))
            for path in directory.glob('*_generations.csv')
            if path.with_name(path.name[:-len('_generations.csv')] + '_runs.csv').is_file()
        )
    if not prefixes:
        raise FileNotFoundError('No matching *_generations.csv and *_runs.csv pairs found.')

    generation_rows = []
    run_rows = []
    for prefix in prefixes:
        generations = read_csv(prefix + '_generations.csv')
        runs = read_csv(prefix + '_runs.csv')
        generation_columns = generations[0].keys() if generations else ()
        run_columns = runs[0].keys() if runs else ()
        if 'best_' + args.criterion not in generation_columns or 'hof_' + args.criterion not in run_columns:
            continue
        label = label_from_prefix(prefix)
        generation_rows.extend(dict(row, label=label) for row in filter_first_runs(generations, args.runs_to_plot))
        run_rows.extend(dict(row, label=label) for row in filter_first_runs(runs, args.runs_to_plot))
    if not generation_rows or not run_rows:
        raise ValueError('No result files contain the requested criterion: ' + args.criterion)
    if args.plot_type in ('individual', 'all'):
        plot_individual_runs(generation_rows, args.criterion, args.output_prefix + '_individual_runs.png', args.y_min)
    if args.plot_type in ('aggregated', 'all'):
        plot_aggregated_runs(generation_rows, args.criterion, args.deviation_divisor, args.output_prefix + '_aggregated_runs.png', args.y_min)
    if args.plot_type in ('boxplots', 'all'):
        plot_boxplots(run_rows, args.criterion, args.output_prefix + '_boxplots.png')
    print('Saved plots with prefix %s' % args.output_prefix)


if __name__ == '__main__':
    main()
