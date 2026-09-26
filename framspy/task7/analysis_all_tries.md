# Task 7: analysis of all six approaches

## Experimental goal

The goal was to evolve a Framstick that swims forward through a large submerged world for the whole evaluation. The desired behavior is sustained forward motion with limited lateral and vertical drift, without resting on the bottom or leaving the water.

The initial position and orientation were fixed. This made the problem easier but introduces overfitting: a controller may work only from the selected starting pose. The body could use `G`, `Water`, `Sin`, and `Delay` neurons. `G` and `Water` provide feedback; `Sin` and `Delay` provide periodic control. The organism does not directly sense global fitness or target position.

The final environment was a flat world of side length `200`, with water at `z=8` and initial height `creath=6`. Performance was sampled every `100` simulation steps. The main simulation sequence was:

```text
eval-allcriteria-mini.sim;swimming-water.sim;recording-body-coords.sim
```

The recorder stored center-of-gravity coordinates at performance updates. The final weighted fitness used the entire measured period, weighting the first half by `0.25` and the second half by `0.75`, with mild consistency and straightness bonuses and small lateral/vertical penalties.

## Six tested approaches

### 1. F1 endpoint fitness

Directory: `1st-try`

The first approach used f1 and rewarded final forward displacement. The world was smaller and the objective was based mainly on the endpoint. This produced the largest numerical scores, up to `8.4689`, but the objective could be exploited by one strong movement followed by stopping or hitting a boundary.

Summary: mean `3.1260`, median `0.9225`, standard deviation `3.5794`. Five of ten runs exceeded `1.0`.

### 2. F1 endpoint fitness with oscillators

Directory: `2nd-try-big-one-move`

This kept the endpoint-oriented objective but enabled or encouraged `Sin` and `Delay` neurons. Periodic control became available, but the fitness loophole remained.

Summary: mean `2.1621`, median `0.0038`, standard deviation `3.3432`. Three of ten runs exceeded `1.0`. The high mean is caused by a few very successful endpoint movements, while most runs remained near zero.

### 3. F1 sustained fitness

Directory: `3try- 2.0 small move-bigger-world`

The world was enlarged and deepened, and performance was sampled using `perfperiod=100`. Fitness was calculated from sustained motion in the latter half of the recording. This reduced the one-movement loophole.

Summary: mean `1.2704`, median `1.7173`, standard deviation `0.8270`. Six of ten runs exceeded `1.0`. The best result was `2.1905`.

### 4. F1 with lower drift penalties

Directory: `4th-swimmer-lower-penalties`

The lateral penalty was reduced from `0.25` to `0.05`, and the vertical penalty from `0.10` to `0.02`. The stagnation limit was increased from `20` to `50` generations. This allowed more imperfect but larger swimming motions and gave evolution longer to refine them.

Summary: mean `1.4703`, median `1.7453`, standard deviation `0.5774`. Eight of ten runs exceeded `1.0`. Several runs reached the 200-generation limit, showing that the larger stagnation threshold allowed continued search.

### 5. Final F1 fitness

Directory: `5th-try-it-swimmmsss`

This approach used the final weighted objective:

```text
weighted_speed = 0.25 * early_speed + 0.75 * late_speed
```

It rewarded early movement but emphasized continued swimming. It used the lower drift penalties and a stagnation limit of `50`.

Summary: mean `1.6230`, median `1.7495`, standard deviation `0.3157`. All ten runs exceeded `1.0`. The best result was `1.9373`. This is the most consistent F1 approach: its standard deviation is much smaller than the endpoint variants.

### 6. Final F4 fitness

Directory: `6th try-F4`

This used the same environment, fitness, population, seeds, workers, and stopping rule as approach 5, but changed the genetic representation to f4. F4 uses developmental instructions and can express repeated structures compactly.

Summary: mean `0.6786`, median `0.4138`, standard deviation `0.6806`. Three of ten runs exceeded `1.0`. The best single run reached `1.9509`, close to the best F1 run, but the result was much less reliable across runs.

## F1 versus F4

The controlled comparison is approaches 5 and 6, named Final F1 and Final F4 in the plots. F1 performed better on average:

- F1 mean best fitness: `1.6230`
- F4 mean best fitness: `0.6786`
- F1 median: `1.7495`
- F4 median: `0.4138`
- F1 standard deviation: `0.3157`
- F4 standard deviation: `0.6806`
- F1 runs above `1.0`: `10/10`
- F4 runs above `1.0`: `3/10`

F4 was capable of producing one strong solution, but it was less reliable with this population size, mutation configuration, and 200-generation budget. The result does not prove that f4 is intrinsically worse; it shows that f4 was less effective under the tested configuration.

## Stagnation and convergence

The first three approaches used a stagnation limit of `20`. The fourth, fifth, and sixth approaches used `50`.

The 50-generation limit allowed more continued search. In approach 5, most runs completed between generations `104` and `196`, and all runs achieved fitness above `1.0`. In approach 6, several runs reached 200 generations without converging to strong solutions, indicating that extra time alone did not solve the f4 search difficulty.

The endpoint approaches had high variance: some runs found a large displacement while others stayed near the stationary baseline. The sustained and weighted objectives reduced this variance, especially for F1.

## Fitness landscape

The landscape is rugged and deceptive. Near the initial genotype, most mutations produce no useful translation. Useful behavior appears when morphology, muscle placement, oscillators, and neural connections happen to cooperate.

Important local optima include:

- stationary or nearly stationary individuals;
- one-time impulses;
- bodies that oscillate but do not translate;
- individuals that move laterally or vertically instead of forward;
- individuals that reach a boundary and stop.

The endpoint fitness made the boundary and one-impulse optima attractive. Performance-window sampling and the weighted early/late objective reduced this problem by rewarding movement that continues later in life.

## Required plots

Generated plots are in `analysis_outputs`:

- one convergence plot per approach;
- one boxplot per approach;
- `task7_all_approaches_convergence.png`;
- `task7_f1_vs_f4_convergence.png`;
- `task7_f1_vs_f4_boxplot.png`;
- `task7_best_run_each_approach.png`.

The machine-readable summary is `task7_all_runs_summary.csv`, and the compact table is `task7_report_summary.md`.

## Qualitative conclusions

The evolved F1 genotypes commonly contain `Sin`, `Delay`, `G`, `Water`, and bending or rotating muscles. The presence of an oscillator is not sufficient by itself: the morphology and muscle placement must convert oscillation into translation.

The fifth approach produced the most consistent F1 results. The sixth approach showed that f4 can produce a competitive individual, but many f4 runs remained weak. The best individuals should be demonstrated in the GUI and, ideally, in a video showing both body movement and neural activity.

One limitation remains: the current recorder stores only center-of-gravity coordinates. Therefore, the fitness does not strictly detect whether an individual Part crosses above the water surface. A future variant can record the maximum Part height and add an explicit surface-violation penalty.
