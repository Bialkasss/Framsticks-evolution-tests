import argparse
import csv
import os
import sys

import matplotlib.pyplot as plt

import frams
from FramsticksLib import FramsticksLib


SEED_GENOTYPES = [
    "X",
    "X(X)",
    "RXX(X,CXXX)",
    "XrrX[G][-1:80][|,-1:0.9]X[|,-2:-21]",
    "(rrX(lX(llX[T:1],),lXMMMMX[|1:2,-1:-3]rrX[T:-0.407](LlX,,LlX),))",
    "bDdgX(X[@0:1.524][|1:-2.379], rrLC(rX[|T:2.114], rrrLX[|T:2.114], rrrLX[|T:3.939], rLMX[|T:2.936, -1:-0.812], rLMXFX[@1:-1.040][0:-1.331][|G:1.849][T:-2.607], rLMXFcCX[@1:2.227][0:-1.331][|G:1.849], rLMXFcCX[@0:-2.675, -1:-483.403, 1:-822.175][|G:2.389], X))",
    "X(X, RRMMX[@G:.5](X[@G:.5], X))",
    "FFX[G:-5.141,in:0]MMX[|-1:8.097,in:0.8,fo:0.04]X[|-1:1.768,fo:1]RRX(X, X)",
    "RRLLLLFFFFX[*][Sin][N,-1:-14.52,-2:3.977,in:0.907657]lllffffX[|,-1:52.083,p:1,r:0.886]RRFFFFXllllF(llllFFFF(llllX,llllFFFFX))"
]


def parse_periods(value):
    periods = [int(item) for item in value.split(",")]
    if not periods or any(period < 1 for period in periods):
        raise argparse.ArgumentTypeError("periods must be positive integers")
    return periods


def make_genotypes(frams_lib, target_count):
    genotypes = list(SEED_GENOTYPES)
    mutation_parents = [genotype for genotype in genotypes if genotype != "X"]
    max_attempts = max(100, target_count * 50)
    attempts = 0
    while len(genotypes) < target_count and attempts < max_attempts:
        parent = mutation_parents[attempts % len(mutation_parents)]
        mutant = frams_lib.mutate([parent])[0]
        if mutant != frams_lib.GENOTYPE_INVALID and mutant not in genotypes:
            genotypes.append(mutant)
            mutation_parents.append(mutant)
        attempts += 1
    if len(genotypes) < target_count:
        raise RuntimeError(
            f"Could generate only {len(genotypes)} distinct genotypes after {attempts} mutation attempts"
        )
    return genotypes[:target_count]


def evaluate_landscapes(frams_lib, genotypes, periods):
    rows = []
    for period in periods:
        frams.Populations[0].perfperiod = period
        evaluations = frams_lib.evaluate(genotypes)
        for index, (genotype, evaluation) in enumerate(zip(genotypes, evaluations)):
            values = evaluation.get("evaluations", {}).get("", {})
            rows.append({
                "genotype_index": index,
                "genotype": genotype,
                "perfperiod": period,
                "lifespan": values.get("lifespan"),
                "distance": values.get("distance"),
                "velocity": values.get("velocity"),
            })
    return rows


def save_csv(rows, filename):
    fieldnames = ["genotype_index", "genotype", "perfperiod", "lifespan", "distance", "velocity"]
    with open(filename, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_plot(rows, filename, periods):
    values_by_period = {
        period: [row["velocity"] for row in rows if row["perfperiod"] == period]
        for period in periods
    }
    figure, axis = plt.subplots(figsize=(12, 6))
    positions = range(len(next(iter(values_by_period.values()))))
    for period in periods:
        axis.plot(positions, values_by_period[period], marker=".", linewidth=1, label=f"perfperiod={period}")
    axis.set_xlabel("Genotype index")
    axis.set_ylabel("Velocity")
    axis.set_title("Velocity landscapes for different performance sampling periods")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(filename, dpi=160)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description="Compare Framsticks velocity landscapes for several perfperiod values.")
    parser.add_argument("-path", default="..", help="Path to the Framsticks distribution.")
    parser.add_argument("-count", type=int, default=40, help="Number of distinct genotypes to evaluate.")
    parser.add_argument("-periods", type=parse_periods, default=[1, 20, 100, 500, 2000, 10000])
    parser.add_argument("-output_prefix", default="perfperiod_landscapes")
    args = parser.parse_args()

    if args.count < len(SEED_GENOTYPES):
        parser.error(f"count must be at least {len(SEED_GENOTYPES)}")

    FramsticksLib.DETERMINISTIC = True
    frams_lib = FramsticksLib(args.path, None, "eval-allcriteria.sim")
    genotypes = make_genotypes(frams_lib, args.count)
    rows = evaluate_landscapes(frams_lib, genotypes, args.periods)

    csv_filename = args.output_prefix + ".csv"
    plot_filename = args.output_prefix + ".png"
    save_csv(rows, csv_filename)
    save_plot(rows, plot_filename, args.periods)

    lifespans = {row["lifespan"] for row in rows}
    print(f"Evaluated {len(genotypes)} genotypes at periods {args.periods}")
    print(f"Lifespan values observed: {sorted(lifespans)}")
    print(f"Saved {os.path.abspath(csv_filename)}")
    print(f"Saved {os.path.abspath(plot_filename)}")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()