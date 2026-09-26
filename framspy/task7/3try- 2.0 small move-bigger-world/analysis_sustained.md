# Task 7 F1 sustained-swimming analysis

## Dataset

The analysis uses `task7-f1-sustained_generations.csv` and `task7-f1-sustained_runs.csv`. These archived runs used 10 independent f1 runs with population size 50, a maximum of 200 generations, and a stagnation limit of 20 generations. Subsequent runs use the revised sustained-motion fitness and a 50-generation stagnation limit.

The reported `mutation_intensity` column is 0.0 because it records the f9-specific `GenMan.f9_mut` parameter. It is not the f1 mutation rate. The actual Python evolutionary settings were `pmut=0.9` and `pxov=0.2`.

## Run-level results

| Run | Best generation | Best fitness | First positive fitness | Improvements | Completed generations |
|---:|---:|---:|---:|---:|---:|
| 0 | 39 | 1.7549 | 9 | 27 | 59 |
| 1 | 80 | 0.2478 | 52 | 32 | 100 |
| 2 | 42 | 1.6796 | 10 | 32 | 62 |
| 3 | 94 | 1.8452 | 38 | 41 | 114 |
| 4 | 90 | 1.9967 | 22 | 43 | 110 |
| 5 | 34 | 2.1905 | 16 | 25 | 54 |
| 6 | 60 | 0.1485 | 18 | 40 | 80 |
| 7 | 91 | 0.4927 | 5 | 57 | 111 |
| 8 | 97 | 2.1242 | 18 | 58 | 117 |
| 9 | 13 | 0.2240 | 5 | 18 | 33 |

Summary statistics:

- Mean best fitness: `1.2704`
- Median best fitness: `1.7173`
- Standard deviation: `0.8270`
- Minimum: `0.1485`
- Maximum: `2.1905`
- Six of ten runs exceeded fitness `1.0`
- Two of ten runs exceeded fitness `2.0`
- Mean completed generations: `84`
- Completed-generation range: `33` to `117`

## Stagnation

Every run stopped exactly 20 generations after its last Hall-of-Fame improvement. This shows that the stopping criterion was active in all runs; none reached the 200-generation hard limit.

The earliest apparent convergence occurred in run 9, which stopped at generation 33 after reaching its best value at generation 13. Run 8 explored longest and found its best at generation 97, then stopped at generation 117. The stopping rule therefore saves time, but it also means that weak runs such as runs 1, 6, and 9 are not given further opportunities after their search plateaus.

The generation traces show a long low-fitness phase followed by occasional jumps. In the first run, fitness remained near zero for roughly the first 15 generations, then increased sharply around generations 16-23. This is consistent with the need to discover a viable combination of body structure, muscle, and oscillator before useful swimming appears.

## Genotype observations

All ten final genotypes contain a `Sin` oscillator. Several also contain `Delay`, `Water`, `G`, or `Gpart` sensors and bending/rotating muscles. This indicates that evolution discovered the importance of periodic control, but oscillator presence alone was not sufficient:

- Runs 0, 2, 3, 4, 5, and 8 produced relatively strong results.
- Runs 1, 6, 7, and 9 remained weak despite containing periodic or delayed neurons.
- The remaining difference is morphology, muscle placement, connection weights, and coordination between body segments.

The best sustained result is run 5 with fitness `2.1905`. Its genotype contains a `Sin` controller, several muscles, sensory inputs, and a longer multi-part body. It is the first individual to inspect manually, followed by runs 8, 4, 3, 0, and 2.

## Comparison with earlier runs

The archived endpoint-style batches reached values as high as approximately `8.47`. Those values must not be compared directly with the sustained scores because the earlier objective rewarded final displacement and could reward a single large movement followed by stopping or hitting a boundary.

The sustained objective produces lower scores by design. It evaluates the latter half of the recording and rewards positive movement across repeated performance windows. The lower maximum is therefore evidence that the objective became stricter, not necessarily that evolution became worse.

## Conclusions

The experiment converged quickly under the 20-generation stagnation rule, but results were highly variable. Six of ten runs found meaningful sustained movement, while four converged to weak local optima. The landscape is rugged: useful behavior appears suddenly after compatible morphology and neural control evolve, and many genotypes with oscillators still fail to coordinate movement.

The next useful comparison is to repeat the same 10 seeds with a larger population, for example `popsize=100`, while keeping the same world, performance period, and fitness function. This tests whether weak runs are caused by insufficient diversity rather than a flawed objective.
