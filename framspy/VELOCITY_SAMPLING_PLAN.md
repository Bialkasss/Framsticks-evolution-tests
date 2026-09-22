# Velocity Sampling Plan

## Goal

Build a dataset for velocity optimization with neural networks in four genetic
representations: f0, f1, f4, and fH. Every saved sample has its genotype and
velocity, and every sample is the parent of a separately logged neighborhood of
at least 20 evaluated mutants.

## Decisions and reasons

- Use `eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim` in that
  order. The first file supplies the standard evaluation fields, the second
  removes evaluation noise, and the third makes velocity measurement use the
  longest rectilinear sampling period.
- Start each independent climb from `getSimplest(format)`. This gives the same
  poor starting point within a representation and makes the climbs comparable.
- Use greedy, mutation-only hill climbing. For every parent, generate 20
  distinct mutants, evaluate the complete batch, and accept only the best strict
  improvement. This records the fitness climb and naturally preserves local
  optima as final samples.
- Run 50 independent climbs for each representation. The expected output is
  well above 200 samples, while `merge_velocity_samples.py` checks the actual
  number of unique fitness values and fails when it is below 200.
- Randomize Framsticks mutation state per process. `deterministic.sim` makes
  evaluations repeatable; `FramsticksLib.DETERMINISTIC` must remain false so
  independent climbs do not follow the same mutation sequence.
- Reject invalid mutation results, duplicate mutants, missing evaluations, and
  `FITNESS_VALUE_INFEASIBLE_SOLUTION` (`-999999.0`). Rejected mutants remain in
  the neighborhood CSV with their status for auditability.
- Run independent climbs in parallel, with a bounded worker count. Each worker
  owns one Framsticks process, avoiding shared native-library state.

## Run

From `framspy/` in Git Bash, collect only the representations assigned to that
laptop:

```bash
FORMAT_LIST="0 1" RUNS=50 OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

The other laptop can run the complementary formats:

```bash
FORMAT_LIST="4 H" RUNS=50 OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

The launcher is modular. `MODE=collect` is the default and only runs the
selected climbs; it does not merge or plot partial results. After copying the
per-run files from both laptops into the same `task4-neighbourhood` directory,
run the final analysis once:

```bash
MODE=analyze OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

If the laptops use separate output directories, copy the files from one into
the other's `task4-neighbourhood` directory before analysis. Since the format
subsets do not overlap, the files do not overwrite each other:

```bash
cp task4-neighbourhood_laptop2/velocity-f*-run*-samples.csv task4-neighbourhood/
cp task4-neighbourhood_laptop2/velocity-f*-run*-neighbors.csv task4-neighbourhood/
cp task4-neighbourhood_laptop2/velocity-f*-run*-samples.gen task4-neighbourhood/
```

Defaults are 50 runs per format, 20 neighbors per sample, 100 maximum climb
iterations, 10 stagnation iterations, and 12 parallel workers. Override them,
for example:

```bash
RUNS=60 TOTAL_WORKERS=8 OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

## Outputs

For every format and run, the launcher writes:

- `velocity-f*-run*-samples.csv`: accepted samples with parent genotype,
  genotype, iteration, and fitness.
- `velocity-f*-run*-neighbors.csv`: at least 20 mutants for every saved sample,
  including explicit parent fitness and feasible or infeasible status.
- `velocity-f*-run*-samples.gen`: Framsticks genotype records containing the
  saved genotypes and velocity values.

The final merged files are `velocity-all-samples.csv` and
`velocity-all-neighbors.csv` in the output directory. The merge step reports
the number of unique fitness values and stops with an error if it is below 200.

The launcher then creates:

- `velocity-all_individual_runs.png`, `velocity-all_aggregated_runs.png`, and
  `velocity-all_boxplots.png`: the three standard optimization views.
- `velocity-all_neighborhood_f0.png`, `velocity-all_neighborhood_f1.png`,
  `velocity-all_neighborhood_f4.png`, and `velocity-all_neighborhood_fH.png`:
  parent-versus-mutant scatter plots with a common 0-to-global-best scale and a
  `y=x` line.
- `velocity-all_neighborhood_statistics.csv`: feasible counts and the fraction
  of mutants better than their parent for each representation.
- `velocity-all_conclusions.md`: an automatically generated interpretation
  template grounded in those measured fractions and plots.

## Interpretation

The sample CSV contains the initial poor genotype, every strict best-so-far
improvement, and the terminal local optimum of each climb. Fitness values are
not expected to be uniformly spaced: the independent runs and four
representations provide variation, while the merged report should be inspected
for large gaps before selecting parents for downstream analysis.