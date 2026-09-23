# EAS4 task 1 landscape conclusions

The common neighborhood plot scale is 0 to 2.22368774308, the best sampled vertpos across all representations.

The separate neighborhood plots show mutant fitness around collected parents. Points above the y=x line improve on their parent; points below it are worse. Negative mutant fitness values were treated as infeasible and omitted.

The improving-mutant fractions are:

- f0: 12.64% (490/3876 feasible mutants)
- f1: 11.62% (426/3665 feasible mutants)
- f4: 14.67% (518/3531 feasible mutants)
- f9: 3.69% (133/3606 feasible mutants)


## Conclusions from the plots

The landscape is rugged and non-convex, at least around the collected samples. The neighborhood plots do not form a narrow smooth band around the y=x line. Instead, each parent can have mutants with very different fitness values, including many mutants close to zero. Therefore, a small genotype mutation can either preserve fitness, improve it, make only a moderate decrease, or produce an infeasible solution. The broad vertical spread is evidence of uneven local neighborhoods rather than a smooth fitness surface.

The y=x line also shows that most feasible mutations are not improvements. The improving fractions are 12.64% for f0, 11.62% for f1, 14.67% for f4, and only 3.69% for f9. This means that all four representations generally require selection among many worsening or neutral mutations, but f4 has the largest number of locally improving directions in the sampled region. The f9 neighborhood is the most restrictive: its points are concentrated around parent fitness values below 1.0 and its mutants are usually below their parents.

The sample histograms and aggregated runs show clear differences in the reachable fitness range. f4 has the widest distribution and the highest upper tail, reaching about 2.22, and its mean fitness continues increasing to about 1.60. It therefore appears to provide the best access to high-quality solutions, although its evolutionary runs are slower and more variable according to the time boxplot. f1 reaches about 1.36 on average and has a broad distribution with both low and high samples. f0 reaches about 1.22 and has a somewhat narrower distribution than f1, with a visible group around intermediate fitness values. f9 improves quickly at the beginning, but then levels off near 0.75 and has a concentrated sample distribution around 0.7-0.85.

The terminal-fitness boxplot supports the same ranking: f4 has the highest median and largest spread, followed by f1 and f0, while f9 is clearly lower and more tightly clustered. The time boxplot shows the opposite practical trade-off: f9 is the fastest and most stable, f0 and f1 are intermediate, and f4 is the slowest with the greatest variability. Thus, f9 may be computationally cheap but has poor optimization potential in these experiments, whereas f4 costs more time but exposes a larger and more promising part of the landscape.

These conclusions apply to the neighborhoods of the solutions collected by the evolutionary climbs and to the mutation operator used to generate the neighbors. They are not claims about every solution in the full combinatorial search space. The sampling process deliberately over-represents paths visited during optimization, especially intermediate and good solutions.
