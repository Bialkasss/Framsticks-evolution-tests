# Task 7: Swimming Framstick

## Starting individual

The f1 starting individual is `X`, the simplest valid f1 genotype returned by `GenMan.getSimplest("1")`. It is one body Part with no joints and no neurons. The evolutionary algorithm mutates this seed to discover additional body Parts, muscles, neurons, and connections.

## Objective

Maximize forward center-of-gravity displacement along +x while minimizing sideways and vertical movement. The custom score is calculated in `FramsticksEvolution.py` from `data->bodyrecording`.

## Simulation files

Load these files in this order:

```text
eval-allcriteria-mini.sim;swimming-water.sim;recording-body-coords.sim
```

The environment is a flat bounded world with side length `200`. The water surface is at `z=8.0`, and the starting height is `z=6.0`, so the initial creature is submerged with two world units of water above it. Performance is sampled every `100` simulation steps, and the recorder stores one center-of-gravity coordinate per performance update.

The water preset enables `G`, `Water`, `Sin`, and `Delay` neurons. `G` and `Water` provide feedback, while `Sin` and `Delay` provide the periodic control needed for sustained swimming. Existing Hall-of-Fame genotypes must be reevaluated after this change; enabling a neuron class only affects future mutations.

For manual GUI inspection, use [manual-water.sim](manual-water.sim) instead of the evaluation sequence. It uses `expdef:standard`, so manually killing or restarting a creature does not enter the `standard-eval` bookkeeping path. Use the evaluation sequence only for evolutionary measurements. Keep the same water level, starting height, world size, and performance period when comparing GUI behavior with evolutionary results.

The final weighted fitness scores mean forward displacement across the full measured period, weighting the first half by `0.25` and the second half by `0.75`. Consistency and straightness are mild bonuses, while lateral and vertical drift receive small penalties. This rewards early movement but still prioritizes continued swimming.

## F1 run

From this directory, run:

```powershell
python ..\FramsticksEvolution.py -path ..\.. -sim "eval-allcriteria-mini.sim;swimming-water.sim;recording-body-coords.sim" -opt velocity -genformat 1 -popsize 50 -generations 200 -stagnation 50 -runs 1 -workers 1 -hof_savefile task7-f1-hof.gen -output_prefix task7-f1
```

Outputs are `task7-f1_generations.csv`, `task7-f1_runs.csv`, and `task7-f1-hof.gen`.

## Parallel independent runs

Use `run_f1_parallel.cmd` to run four independent evolutionary runs concurrently:

```powershell
python ..\FramsticksEvolution.py -path ..\.. -sim "eval-allcriteria-mini.sim;swimming-water.sim;recording-body-coords.sim" -opt velocity -genformat 1 -popsize 50 -generations 200 -stagnation 50 -runs 4 -workers 4 -hof_savefile task7-f1-hof.gen -output_prefix task7-f1-parallel
```

This is parallel over independent random seeds. It does not make one evolutionary run four times faster. Increase `-workers` only up to the number of physical CPU cores and available memory. For the required 10 repetitions, use `-runs 10 -workers 4`.

## Bash batch runner

For the reproducible multi-run workflow, use [run_f1.sh](run_f1.sh) from Git Bash:

```bash
bash run_f1.sh
```

It runs 10 independent seeded experiments, with up to 12 jobs active at once. Each run gets its own `task7-f1-runN_generations.csv`, `task7-f1-runN_runs.csv`, and `task7-f1-hof-runN.gen` files. Values can be overridden without editing the script, for example:

```bash
RUNS=10 TOTAL_WORKERS=8 BASE_SEED=107 bash run_f1.sh
```

For the combined-output version, matching `run_f1.cmd`, use:

```bash
bash run_f1_combined.sh
```

This invokes the Python runner once with `-runs 10 -workers 4`. The final F1 run writes one combined result CSV and one Hall-of-Fame file per run.

## F4 comparison

Run the equivalent developmental-encoding experiment with:

```bash
bash run_f4_combined.sh
```

It keeps the same population, environment, performance period, fitness, seeds, and stopping rule as the final F1 experiment. Only the genetic representation changes to f4. Outputs use the `task7-final-f4` prefix.

## Fitness landscape plots

To probe the local landscape around the final F1 and F4 solutions, run:

```bash
bash run_task7_landscape.sh
```

The collector selects five final-run parents per representation, spanning low, middle, and high fitness, then evaluates 20 one-mutation neighbors for each parent. The plots show parent fitness versus mutant fitness, delta-fitness distributions, and the fraction of improving mutations. These are local samples of the landscape, in the style of Task 4; they do not enumerate the complete genotype space.
