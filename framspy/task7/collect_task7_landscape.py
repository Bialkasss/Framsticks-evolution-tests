#!/usr/bin/env python3
"""Collect local mutant neighborhoods for the final F1 and F4 task7 runs."""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from FramsticksLib import FramsticksLib

FITNESS_VALUE_INFEASIBLE_SOLUTION = -999999.0
DATASETS = {
    "Final F1": ("5th-try-it-swimmmsss", "task7-f1-compromise"),
    "Final F4": ("6th try-F4", "task7-f4-compromise"),
}


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def evaluate_swimming_fitness(frams_lib, genotype: str):
    result = frams_lib.evaluate([genotype])
    try:
        data = result[0]["evaluations"][""]
        recording = np.asarray(data["data->bodyrecording"], dtype=float)
    except (IndexError, KeyError, TypeError, ValueError):
        return None
    if len(recording) < 4:
        return None
    displacement = np.diff(recording, axis=0)
    midpoint = max(1, len(displacement) // 2)
    early_speed = max(0.0, float(np.mean(displacement[:midpoint, 0])))
    late_speed = max(0.0, float(np.mean(displacement[midpoint:, 0])))
    forward_progress = float(displacement[:, 0].sum())
    path_length = float(np.linalg.norm(displacement, axis=1).sum())
    straightness = max(0.0, forward_progress) / max(path_length, 1e-9)
    consistency = float(np.mean(displacement[:, 0] > 0.0))
    lateral_drift = float(np.mean(np.abs(displacement[:, 1])))
    vertical_drift = float(np.mean(np.abs(displacement[:, 2])))
    fitness = (
        (0.25 * early_speed + 0.75 * late_speed)
        * (0.5 + 0.5 * consistency)
        * (0.75 + 0.25 * straightness)
        - 0.05 * lateral_drift
        - 0.02 * vertical_drift
    )
    return float(fitness) if math.isfinite(fitness) else None


def select_parents(rows, count: int):
    candidates = []
    seen = set()
    for row in rows:
        genotype = row.get("hof_genotype", "")
        if not genotype or genotype in seen:
            continue
        seen.add(genotype)
        candidates.append({"genotype": genotype, "fitness": float(row["hof_velocity"])})
    candidates.sort(key=lambda row: row["fitness"])
    if len(candidates) <= count:
        selected = candidates
    else:
        indexes = [round(index * (len(candidates) - 1) / (count - 1)) for index in range(count)]
        selected = [candidates[index] for index in indexes]
    for index, parent in enumerate(selected):
        if index == 0:
            parent["rank_group"] = "worst"
        elif index == len(selected) - 1:
            parent["rank_group"] = "best"
        else:
            parent["rank_group"] = "middle"
        parent["parent_id"] = index + 1
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-path", required=True, help="Path to the Framsticks distribution directory")
    parser.add_argument("-neighbors", type=int, default=20)
    parser.add_argument("-parents-per-representation", type=int, default=5)
    parser.add_argument("-seed", type=int, default=7025)
    parser.add_argument("-output-dir", type=Path, default=SCRIPT_DIR / "analysis_outputs_readable" / "landscape")
    args = parser.parse_args()
    if args.neighbors < 1 or args.parents_per_representation < 2:
        parser.error("neighbors must be positive and parents-per-representation must be at least 2")

    random.seed(args.seed)
    FramsticksLib.DETERMINISTIC = False
    FramsticksLib.GENOTYPE_INVALID_OFFSPRING_SUBSTITUTE_ORIGINAL = False
    simulation_dir = SCRIPT_DIR
    simulation = ";".join(str(simulation_dir / name) for name in (
        "eval-allcriteria-mini.sim",
        "swimming-water.sim",
        "recording-body-coords.sim",
    ))
    frams_lib = FramsticksLib(str(Path(args.path).resolve()), None, simulation)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    neighborhood_rows = []
    parent_rows = []
    for representation, (folder, prefix) in DATASETS.items():
        source = SCRIPT_DIR / folder / f"{prefix}_runs.csv"
        parents = select_parents(read_rows(source), args.parents_per_representation)
        for parent in parents:
            evaluated_parent = evaluate_swimming_fitness(frams_lib, parent["genotype"])
            parent_fitness = evaluated_parent if evaluated_parent is not None else parent["fitness"]
            parent_rows.append({
                "representation": representation,
                "parent_id": parent["parent_id"],
                "rank_group": parent["rank_group"],
                "parent_fitness": parent_fitness,
                "genotype": parent["genotype"],
            })
            mutants = []
            attempts = 0
            while len(mutants) < args.neighbors and attempts < args.neighbors * 100:
                attempts += 1
                mutant = frams_lib.mutate([parent["genotype"]])[0]
                if mutant == frams_lib.GENOTYPE_INVALID or mutant in mutants:
                    continue
                mutants.append(mutant)
            evaluations = [evaluate_swimming_fitness(frams_lib, mutant) for mutant in mutants]
            for mutant_index, (mutant, mutant_fitness) in enumerate(zip(mutants, evaluations), start=1):
                neighborhood_rows.append({
                    "representation": representation,
                    "parent_id": parent["parent_id"],
                    "rank_group": parent["rank_group"],
                    "mutant_id": mutant_index,
                    "parent_fitness": parent_fitness,
                    "mutant_fitness": "" if mutant_fitness is None else mutant_fitness,
                    "delta_fitness": "" if mutant_fitness is None else mutant_fitness - parent_fitness,
                    "status": "infeasible" if mutant_fitness is None else "feasible",
                    "genotype": mutant,
                })

    with (output_dir / "task7_landscape_neighborhoods.csv").open("w", newline="", encoding="utf-8") as target:
        fields = list(neighborhood_rows[0])
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(neighborhood_rows)
    with (output_dir / "task7_landscape_parents.csv").open("w", newline="", encoding="utf-8") as target:
        fields = list(parent_rows[0])
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(parent_rows)
    print(f"Saved {len(parent_rows)} parents and {len(neighborhood_rows)} mutants to {output_dir}")


if __name__ == "__main__":
    main()
