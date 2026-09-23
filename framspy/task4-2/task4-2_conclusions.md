# EAS4 task 2 crossover conclusions

## Motivation and data collection

Task 2 tests whether crossover combines two selected task-1 solutions into an offspring with useful fitness. For every representation, pairs of sampled parents were crossed, the offspring was evaluated, and invalid offspring were excluded from fitness comparisons. The two reference quantities are the better parent and the mean of the two parents. The parent order is irrelevant because the comparisons use `max(parent1, parent2)` and `(parent1 + parent2) / 2`.

## Statistics

The main statistic is the best-parent improvement rate:

`C_best = number of feasible offspring better than both parents / number of feasible offspring`.

A complementary statistic is the mean-parent improvement rate:

`C_mean = number of feasible offspring better than the mean parent / number of feasible offspring`.

| Representation | Attempts | Feasible | Infeasible | Better than best | Better than mean | Mean gain vs best | Mean gain vs mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| f0 | 1000 | 953 | 47 | 0.63% | 5.14% | -0.7496 | -0.5368 |
| f1 | 1000 | 831 | 169 | 1.44% | 11.91% | -0.8171 | -0.5723 |
| f4 | 1000 | 749 | 251 | 1.20% | 8.28% | -0.9810 | -0.6589 |
| f9 | 1000 | 796 | 204 | 2.76% | 16.46% | -0.3369 | -0.2679 |


## What the diagrams show

In both scatter plots, the dashed diagonal is `offspring fitness = reference parent fitness`. Points above the line represent beneficial crossover outcomes; points below it are worse than the reference. The best-parent plot is the stricter test: an offspring above the line is better than both inputs. The mean-parent plot asks whether crossover at least beats the average quality of the two inputs.

The clouds are mostly below the best-parent diagonal, so crossover rarely discovers a child better than the stronger parent. This indicates that crossover is not a reliable local-improvement operator in these data. The mean-parent plot has more points above its diagonal, showing that crossover can often preserve or combine useful material from one good parent while rescuing a weaker parent, even when it does not exceed the best parent.

The representation differences are visible in both the location and spread of the clouds. f4 operates over the highest absolute fitness range and produces the strongest offspring values, but many offspring still fall well below the best parent. f1 has a broad cloud and a comparatively high rate of offspring better than the mean parent. f0 has fewer successful recombinations and a lower improvement rate. f9 has the highest relative improvement rates, especially against the mean parent, but its entire fitness range is much lower; its apparent crossover success should therefore not be confused with reaching the best solutions overall.

The infeasible counts also matter. A representation can have a reasonable conditional improvement rate among feasible offspring while still producing many invalid structures. Consequently, crossover quality should be reported with both the improvement rate and the feasible-offspring rate. These conclusions describe the selected samples and this crossover operator, not all possible parent pairs in the full genotype space.
