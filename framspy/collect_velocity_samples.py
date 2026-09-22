"""Collect velocity samples and mutant neighborhoods for one independent climb."""

import argparse
import csv
import math
import os
import random
import sys
from typing import Dict, List, Optional, Tuple

from FramsticksLib import FramsticksLib


FITNESS_VALUE_INFEASIBLE_SOLUTION = -999999.0
SIMULATION_FILES = "eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim"


def evaluate_velocity(frams_lib: FramsticksLib, genotype: str) -> Optional[float]:
    """Return velocity, or None when Framsticks cannot evaluate the genotype."""
    result = frams_lib.evaluate([genotype])
    try:
        value = result[0]["evaluations"][""]["velocity"]
        value = float(value)
    except (IndexError, KeyError, TypeError, ValueError):
        return None
    if value == FITNESS_VALUE_INFEASIBLE_SOLUTION:
        return None
    return value


def make_mutant_batch(frams_lib: FramsticksLib, parent: str, count: int) -> Tuple[List[str], int]:
    """Create distinct, non-invalid mutants, returning mutants and attempts."""
    mutants = []
    seen = {parent}
    attempts = 0
    max_attempts = max(100, count * 100)
    while len(mutants) < count and attempts < max_attempts:
        attempts += 1
        mutant = frams_lib.mutate([parent])[0]
        if mutant == frams_lib.GENOTYPE_INVALID or mutant in seen:
            continue
        seen.add(mutant)
        mutants.append(mutant)
    return mutants, attempts


def write_gen_file(filename: str, samples: List[Dict[str, object]]) -> None:
    from framsfiles import writer as framswriter

    with open(filename, "w", encoding="utf-8") as output:
        for sample in samples:
            output.write(framswriter.from_collection({
                "_classname": "org",
                "genotype": sample["genotype"],
                "velocity": sample["fitness"],
                "format": sample["genetic_format"],
                "run": sample["run"],
                "sample_index": sample["sample_index"],
            }))
            output.write("\n")


def collect_neighborhoods(frams_lib: FramsticksLib, samples: List[Dict[str, object]], count: int) -> List[Dict[str, object]]:
    neighborhoods = []
    for sample in samples:
        parent = str(sample["genotype"])
        parent_fitness = float(sample["fitness"])
        mutants, attempts = make_mutant_batch(frams_lib, parent, count)
        if len(mutants) < count:
            raise RuntimeError(
                f"Could generate only {len(mutants)} distinct mutants for sample "
                f"{sample['sample_index']} after {attempts} attempts"
            )
        evaluations = frams_lib.evaluate(mutants)
        for mutant, evaluation in zip(mutants, evaluations):
            fitness = FITNESS_VALUE_INFEASIBLE_SOLUTION
            try:
                fitness = float(evaluation["evaluations"][""]["velocity"])
            except (KeyError, TypeError, ValueError):
                pass
            feasible = fitness != FITNESS_VALUE_INFEASIBLE_SOLUTION
            neighborhoods.append({
                "run": sample["run"],
                "genetic_format": sample["genetic_format"],
                "sample_index": sample["sample_index"],
                "parent_genotype": parent,
                "parent_fitness": parent_fitness,
                "genotype": mutant,
                "fitness": fitness,
                "status": "feasible" if feasible else "infeasible",
                "mutation_attempts": attempts,
            })
    return neighborhoods


def run(args: argparse.Namespace) -> Tuple[int, int]:
    random.seed(args.seed)
    # deterministic.sim fixes evaluation noise; Framsticks' mutation RNG must
    # remain randomized so independent climbs explore different paths.
    FramsticksLib.DETERMINISTIC = False
    FramsticksLib.GENOTYPE_INVALID_OFFSPRING_SUBSTITUTE_ORIGINAL = False
    frams_lib = FramsticksLib(args.path, args.lib, SIMULATION_FILES)

    parent = frams_lib.getSimplest(args.genetic_format)
    parent_fitness = evaluate_velocity(frams_lib, parent)
    if parent_fitness is None:
        raise RuntimeError("The simplest genotype could not be evaluated")

    samples: List[Dict[str, object]] = []

    def save_sample(genotype: str, fitness: float, iteration: int) -> None:
        samples.append({
            "run": args.run,
            "genetic_format": args.genetic_format,
            "iteration": iteration,
            "sample_index": len(samples),
            "genotype": genotype,
            "fitness": fitness,
            "parent_genotype": "" if not samples else samples[-1]["genotype"],
        })

    save_sample(parent, parent_fitness, 0)
    stagnant = 0
    iteration = 0
    while iteration < args.max_iterations and stagnant < args.stagnation:
        iteration += 1
        mutants, attempts = make_mutant_batch(frams_lib, parent, args.neighbors)
        if not mutants:
            stagnant += 1
            continue
        evaluations = frams_lib.evaluate(mutants)
        best_genotype = None
        best_fitness = None
        for mutant, evaluation in zip(mutants, evaluations):
            fitness = None
            try:
                fitness = float(evaluation["evaluations"][""]["velocity"])
            except (KeyError, TypeError, ValueError):
                pass
            feasible = fitness is not None and math.isfinite(fitness) and fitness != FITNESS_VALUE_INFEASIBLE_SOLUTION
            if feasible and (best_fitness is None or fitness > best_fitness):
                best_genotype, best_fitness = mutant, fitness

        if best_fitness is not None and best_fitness > parent_fitness:
            parent, parent_fitness = best_genotype, best_fitness
            save_sample(parent, parent_fitness, iteration)
            stagnant = 0
        else:
            stagnant += 1

    neighborhoods = collect_neighborhoods(frams_lib, samples, args.neighbors)
    os.makedirs(args.output_dir, exist_ok=True)
    prefix = os.path.join(args.output_dir, f"velocity-f{args.genetic_format}-run{args.run}")
    sample_fields = ["run", "genetic_format", "iteration", "sample_index", "genotype", "fitness", "parent_genotype"]
    neighborhood_fields = ["run", "genetic_format", "sample_index", "parent_genotype", "parent_fitness", "genotype", "fitness", "status", "mutation_attempts"]
    for filename, fields, rows in ((prefix + "-samples.csv", sample_fields, samples), (prefix + "-neighbors.csv", neighborhood_fields, neighborhoods)):
        with open(filename, "w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    write_gen_file(prefix + "-samples.gen", samples)
    print(f"f{args.genetic_format} run {args.run}: {len(samples)} samples, {len(neighborhoods)} mutants")
    return len(samples), len(neighborhoods)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-path", required=True, help="Path to the Framsticks distribution.")
    parser.add_argument("-lib", default=None)
    parser.add_argument("-genetic-format", choices=["0", "1", "4", "H"], required=True)
    parser.add_argument("-run", type=int, required=True)
    parser.add_argument("-seed", type=int, required=True)
    parser.add_argument("-output-dir", default="velocity_samples")
    parser.add_argument("-neighbors", type=int, default=20)
    parser.add_argument("-max-iterations", type=int, default=100)
    parser.add_argument("-stagnation", type=int, default=10)
    args = parser.parse_args()
    if args.neighbors < 20:
        parser.error("-neighbors must be at least 20")
    run(args)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()