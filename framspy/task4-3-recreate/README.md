# Recreate EAS4 task 3 random walks

This collector recreates task 3 for `vertpos` using the EAS4 task-1 samples as starting solutions.

For each representation (`f0`, `f1`, `f4`, `f9`), it selects 20 genotype-distinct feasible samples spread from low to high fitness. Each selected genotype starts a sequential 30-step random walk. At every step, the current genotype is mutated and evaluated. Invalid genotypes or infeasible fitness values are discarded and mutation is repeated until a feasible result is obtained. Only successful points are written to CSV.

Run from the `framspy` directory:

```powershell
python task4-3-recreate\collect_task4_3_random_walks.py `
  -path "C:\MAGISTER\SEM1\BIO_ALGS\Framsticks" `
  -output-dir task4-3-recreate
```

The default source is `Biologically-inspiredAlgorithmsAndModels/EAS4/EAS4_task1_landscape_samples.csv`. Override it with `-samples` when needed. The output contains one CSV per representation, one merged CSV, and a sample-selection manifest. Every walk must contain 31 rows: the starting sample plus 30 successful mutations.
