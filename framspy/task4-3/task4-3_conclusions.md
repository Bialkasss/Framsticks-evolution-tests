# EAS4 task 3 random-walk conclusions

## Motivation and data collection

Task 3 probes local landscape memory and mutation behavior. Twenty genotype-distinct feasible solutions per representation were selected across the observed fitness range: five best, five high, five medium, and five worst. Each selected solution is the starting point of one sequential 30-step random walk. At every step, the current genotype was mutated and evaluated; invalid genotypes and infeasible fitness values were discarded and mutation was retried until a feasible mutant was obtained. The recreated data therefore contains 80 walks with 31 valid recorded points each, including the starting point.

## What to look for in the diagrams

Each line is one trajectory. The first point is the starting fitness, and the horizontal axis is mutation distance in the sequence, not an independent sample number. Line color identifies the starting-quality group. A trajectory that quickly forgets its initial fitness and joins the same region as other trajectories suggests weak local memory or a broad, mixing mutation operator. Trajectories that remain near their starting level suggest stronger local retention and smoother or more constrained neighborhoods.

## Summary of observed walks

| Representation | Initial mean range | Final mean range | Mean net change range | Infeasible points |
|---|---:|---:|---:|---:|
| f0 | 0.030-1.571 | 0.011-0.383 | -1.353-0.047 | 0 |
| f1 | 0.002-1.931 | 0.000-0.271 | -1.734-0.107 | 0 |
| f4 | 0.010-2.224 | 0.019-0.939 | -1.816-0.167 | 0 |
| f9 | 0.298-0.946 | 0.069-0.393 | -0.827--0.148 | 0 |


## Conclusions

The trajectories show that one mutation can cause a large fitness change, but the effect depends strongly on the starting representation and fitness level. The lines are generally jagged rather than smooth, which is consistent with a rugged combinatorial landscape and with mutation operators that make structural changes rather than small numerical movements.

The best-starting trajectories often fall rapidly after the first few mutations. This is expected in a maximization landscape: a high-fitness solution is surrounded by many solutions that are worse, so random mutation usually leaves the favorable basin. In contrast, the worst-starting trajectories can rise initially because low-fitness solutions have more room for improvement, although they can also fluctuate or become trapped at low values.

The walks also show landscape memory. If trajectories from different starting groups converge toward a similar fitness band, repeated mutation is gradually forgetting the starting solution. If high-start and low-start trajectories remain separated, the landscape has stronger local retention or disconnected regions under the mutation operator. The plots should therefore be interpreted as the combined effect of landscape topology and the particular Framsticks mutation operator.

Across representations, f4 explores the widest fitness range and can retain high values for several steps, but it also shows large downward excursions. f9 is concentrated in a much lower fitness band and its trajectories tend to remain near that band, indicating a more constrained representation or mutation neighborhood. f0 and f1 are intermediate: they show substantial fluctuations and partial convergence across starting groups. The difference between representations is therefore not only their best reachable fitness, but also how quickly random mutation destroys or preserves fitness information.

These walks do not measure optimization performance directly. They measure how fitness changes when selection is removed and mutation is applied repeatedly. The conclusions are local and conditional on the selected starting solutions, the 30-step horizon, the retry rule for invalid mutants, and the mutation operator. Since the recreated files retain only successful evaluations, comparisons describe the valid-mutant sequence rather than the raw frequency of invalid mutation attempts.
