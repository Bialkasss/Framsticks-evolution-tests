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
  improvement as the next parent. Archive the best feasible candidate from
  stalled iterations as an internal path point without changing the greedy
  parent trajectory.
- Target 200 exported samples per representation rather than a fixed number of
  runs. Each climb keeps its full candidate path internally, then exports four
  fitness-quantile checkpoints by default: the initial solution, two middle
  fitness checkpoints, and the best path candidate. The launcher starts more
  runs as needed until the selected representation reaches 200 saved samples.
- `merge_velocity_samples.py` checks the actual count separately for f0, f1,
  f4, and fH and fails if any representation is below 200. Invalid mutants
  remain in the neighborhood CSV with their status for auditability.
- Run independent climbs in parallel, with a bounded worker count. Each worker
  owns one Framsticks process, avoiding shared native-library state.

## Run

From `framspy/` in Git Bash, collect only the representations assigned to that
laptop:

```bash
FORMAT_LIST="0 1" OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

The other laptop can run the complementary formats:

```bash
FORMAT_LIST="4 H" OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

The launcher is modular. `MODE=collect` is the default and only runs the
selected climbs; it does not merge or plot partial results. After copying the
per-run files from both laptops into the same `task4-neighbourhood` directory,
run the final analysis once:

```bash
MODE=analyze OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

Analysis uses the first 200 samples per representation by default for every
plot, neighborhood statistic, and conclusion. The raw merged CSV files still
contain all collected samples. To change the plotting subset:

```bash
MODE=analyze PLOT_SAMPLES_PER_FORMAT=200 OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

If the laptops use separate output directories, copy the files from one into
the other's `task4-neighbourhood` directory before analysis. Since the format
subsets do not overlap, the files do not overwrite each other:

```bash
cp task4-neighbourhood_laptop2/velocity-f*-run*-samples.csv task4-neighbourhood/
cp task4-neighbourhood_laptop2/velocity-f*-run*-neighbors.csv task4-neighbourhood/
cp task4-neighbourhood_laptop2/velocity-f*-run*-samples.gen task4-neighbourhood/
```

Defaults are 200 target samples per format, four saved checkpoints per run, 20
neighbors per sample, 1000 maximum climb iterations, 20 stagnation iterations,
1000 neutral-bootstrap steps, and 12 parallel workers. Override them, for
example:
for example:

```bash
TARGET_SAMPLES=200 SAMPLES_PER_RUN=4 TOTAL_WORKERS=8 OUTPUT_DIR=task4-neighbourhood ./run_velocity_samples.sh
```

The neutral bootstrap is important for f1, f4, and fH: their simplest
genotypes can have zero velocity, while valid mutations must first cross a
neutral plateau before movement appears. It accepts feasible equal-fitness
mutants temporarily, but the exported checkpoints still remain limited to the
configured samples per run.

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

The internal path contains the initial poor genotype, every strict best-so-far
improvement, and distinct best candidates from stalled iterations. The exported
sample CSV keeps fitness-quantile checkpoints from that path, including the
initial and best candidates, rather than every path step. The merged report
should be inspected for remaining duplicate values or large fitness gaps.