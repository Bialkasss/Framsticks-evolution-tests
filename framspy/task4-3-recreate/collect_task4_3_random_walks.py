"""Recreate valid EAS4 task 3 sequential mutation walks for vertpos."""

import argparse
import csv
import math
import random
import sys
from pathlib import Path

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
FRAMSPY_DIRECTORY = SCRIPT_DIRECTORY.parent
sys.path.insert(0, str(FRAMSPY_DIRECTORY))

from FramsticksLib import FramsticksLib


REPRESENTATIONS = ("0", "1", "4", "9")
GROUPS = ("best", "high", "medium", "worst")
SIMULATION_FILES = "eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;only-body.sim"
FITNESS_VALUE_INFEASIBLE_SOLUTION = -999999.0


def read_samples(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def fitness_is_feasible(value):
    return math.isfinite(value) and value != FITNESS_VALUE_INFEASIBLE_SOLUTION and value >= 0


def evaluate_vertpos(frams_lib, genotype):
    result = frams_lib.evaluate([genotype])
    try:
        value = float(result[0]["evaluations"][""]["vertpos"])
    except (IndexError, KeyError, TypeError, ValueError):
        return None
    return value if fitness_is_feasible(value) else None


def select_samples(rows, target):
    """Select genotype-distinct feasible samples spread from low to high fitness."""
    candidates = []
    seen = set()
    for row in rows:
        try:
            fitness = float(row["fitness"])
        except (KeyError, TypeError, ValueError):
            continue
        genotype = row.get("genotype", "")
        if not genotype or not fitness_is_feasible(fitness) or genotype in seen:
            continue
        seen.add(genotype)
        candidates.append({
            "source_run_id": row["run_id"],
            "source_generation": row["generation"],
            "fitness": fitness,
            "genotype": genotype,
        })
    candidates.sort(key=lambda row: row["fitness"])
    if len(candidates) < target:
        raise RuntimeError(f"Need {target} distinct feasible samples, found only {len(candidates)}")
    indexes = [0] if target == 1 else [round(index * (len(candidates) - 1) / (target - 1)) for index in range(target)]
    selected = [candidates[index] for index in indexes]
    for index, sample in enumerate(selected):
        sample["sample_id"] = index + 1
        sample["rank_group"] = GROUPS[min(index // 5, len(GROUPS) - 1)]
    return selected


def collect_walk(frams_lib, sample, representation, walk_id, steps, max_attempts):
    initial_fitness = sample["fitness"]
    evaluated_initial = evaluate_vertpos(frams_lib, sample["genotype"])
    if evaluated_initial is None:
        raise RuntimeError(
            f"Selected sample {sample['sample_id']} for f{representation} became infeasible when re-evaluated"
        )

    rows = [{
        "category": f"f{representation}",
        "walk_id": walk_id,
        "sample_id": sample["sample_id"],
        "rank_group": sample["rank_group"],
        "step": 0,
        "fitness": evaluated_initial,
        "genotype": sample["genotype"],
        "mutation_attempts": 0,
    }]
    current_genotype = sample["genotype"]
    for step in range(1, steps + 1):
        attempts = 0
        while True:
            attempts += 1
            if attempts > max_attempts:
                raise RuntimeError(
                    f"Could not obtain a feasible f{representation} mutation for sample "
                    f"{sample['sample_id']} at step {step} after {max_attempts} attempts"
                )
            mutant = frams_lib.mutate([current_genotype])[0]
            if mutant == frams_lib.GENOTYPE_INVALID:
                continue
            mutant_fitness = evaluate_vertpos(frams_lib, mutant)
            if mutant_fitness is None:
                continue
            rows.append({
                "category": f"f{representation}",
                "walk_id": walk_id,
                "sample_id": sample["sample_id"],
                "rank_group": sample["rank_group"],
                "step": step,
                "fitness": mutant_fitness,
                "genotype": mutant,
                "mutation_attempts": attempts,
            })
            current_genotype = mutant
            break
    if len(rows) != steps + 1:
        raise AssertionError("A random walk must contain the original sample plus every successful step")
    return rows


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-path", required=True, help="Path to the Framsticks distribution directory")
    parser.add_argument("-samples", type=Path, default=FRAMSPY_DIRECTORY.parent.parent / "Biologically-inspiredAlgorithmsAndModels" / "EAS4" / "EAS4_task1_landscape_samples.csv")
    parser.add_argument("-output-dir", type=Path, default=SCRIPT_DIRECTORY)
    parser.add_argument("-walks-per-representation", type=int, default=20)
    parser.add_argument("-steps", type=int, default=30)
    parser.add_argument("-seed", type=int, default=4303)
    parser.add_argument("-max-attempts", type=int, default=10000)
    parser.add_argument("-lib", default=None)
    args = parser.parse_args()
    if args.walks_per_representation < 1 or args.steps < 1 or args.max_attempts < 1:
        parser.error("walks-per-representation, steps, and max-attempts must be positive")

    random.seed(args.seed)
    FramsticksLib.DETERMINISTIC = False
    FramsticksLib.GENOTYPE_INVALID_OFFSPRING_SUBSTITUTE_ORIGINAL = False
    frams_lib = FramsticksLib(str(Path(args.path).resolve()), args.lib, SIMULATION_FILES)
    source_rows = read_samples(args.samples.resolve())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fields = ["category", "walk_id", "sample_id", "rank_group", "step", "fitness", "genotype", "mutation_attempts"]
    all_rows = []
    manifest_rows = []

    for representation in REPRESENTATIONS:
        representation_rows = [row for row in source_rows if row["category"] == f"f{representation}"]
        selected = select_samples(representation_rows, args.walks_per_representation)
        walk_rows = []
        for sample in selected:
            walk_id = f"{representation}-{sample['sample_id']}"
            walk_rows.extend(collect_walk(frams_lib, sample, representation, walk_id, args.steps, args.max_attempts))
            manifest_rows.append({
                "category": f"f{representation}",
                "walk_id": walk_id,
                "sample_id": sample["sample_id"],
                "rank_group": sample["rank_group"],
                "source_run_id": sample["source_run_id"],
                "source_generation": sample["source_generation"],
                "source_fitness": sample["fitness"],
                "recorded_initial_fitness": walk_rows[-(args.steps + 1)]["fitness"],
            })
        write_csv(args.output_dir / f"task4-3_recreated_random_walks_f{representation}.csv", walk_rows, fields)
        all_rows.extend(walk_rows)
        print(f"f{representation}: saved {len(selected)} walks and {len(walk_rows)} valid points")

    write_csv(args.output_dir / "task4-3_recreated_random_walks_all.csv", all_rows, fields)
    write_csv(args.output_dir / "task4-3_recreated_sample_manifest.csv", manifest_rows, list(manifest_rows[0]))
    print(f"Saved {len(all_rows)} valid random-walk points to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
