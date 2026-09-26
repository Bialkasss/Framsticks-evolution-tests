#!/usr/bin/env bash
set -euo pipefail

play_success() {
    powershell.exe -NoProfile -Command "1..2 | ForEach-Object { [Console]::Beep(1000, 600); Start-Sleep -Milliseconds 150 }" >/dev/null 2>&1 || true
}

play_error() {
    powershell.exe -NoProfile -Command "1..3 | ForEach-Object { [Console]::Beep(1000, 600); Start-Sleep -Milliseconds 150 }" >/dev/null 2>&1 || true
}

cleanup_and_notify() {
    local exit_code=$?
    if [ "$exit_code" -eq 0 ]; then
        echo "Combined Task 7 F4 experiment finished successfully!"
        play_success
    else
        echo "Combined Task 7 F4 experiment failed or was aborted with exit code $exit_code!"
        play_error
    fi
}

trap cleanup_and_notify EXIT

# Override these values by exporting environment variables before running the script.
GENETIC_FORMAT="${GENETIC_FORMAT:-4}"
POP_SIZE="${POP_SIZE:-50}"
GENERATIONS="${GENERATIONS:-200}"
STAGNATION="${STAGNATION:-50}"
RUNS="${RUNS:-10}"
TOTAL_WORKERS="${TOTAL_WORKERS:-4}"
BASE_SEED="${BASE_SEED:-107}"
MUTATION_PROBABILITY="${MUTATION_PROBABILITY:-0.9}"
CROSSOVER_PROBABILITY="${CROSSOVER_PROBABILITY:-0.2}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
PYTHON_COMMAND="${PYTHON_COMMAND:-python}"
EVOLUTION_SCRIPT="$SCRIPT_DIR/../FramsticksEvolution.py"
SIMULATION_DIR="$SCRIPT_DIR"
HALL_OF_FAME="${HALL_OF_FAME:-task7-final-f4-hof.gen}"
OUTPUT_PREFIX="${OUTPUT_PREFIX:-task7-final-f4}"

if [[ ! -f "$EVOLUTION_SCRIPT" ]]; then
    echo "Evolution script not found: $EVOLUTION_SCRIPT" >&2
    exit 1
fi

if command -v cygpath >/dev/null 2>&1; then
    LIBRARY_PATH="$(cygpath -w "$LIBRARY_PATH")"
    SIMULATION_DIR="$(cygpath -w "$SIMULATION_DIR")"
fi

SIMULATION="${SIMULATION_DIR}\\eval-allcriteria-mini.sim;${SIMULATION_DIR}\\swimming-water.sim;${SIMULATION_DIR}\\recording-body-coords.sim"

cd "$SCRIPT_DIR"

echo "========== STARTING ${RUNS} COMBINED TASK 7 F4 RUNS =========="
"$PYTHON_COMMAND" "$EVOLUTION_SCRIPT" \
    -path "$LIBRARY_PATH" \
    -sim "$SIMULATION" \
    -opt velocity \
    -max_numparts 15 \
    -max_numjoints 30 \
    -max_numneurons 20 \
    -max_numconnections 30 \
    -genformat "$GENETIC_FORMAT" \
    -pxov "$CROSSOVER_PROBABILITY" \
    -pmut "$MUTATION_PROBABILITY" \
    -popsize "$POP_SIZE" \
    -generations "$GENERATIONS" \
    -stagnation "$STAGNATION" \
    -runs "$RUNS" \
    -workers "$TOTAL_WORKERS" \
    -hof_size 1 \
    -hof_savefile "$HALL_OF_FAME" \
    -output_prefix "$OUTPUT_PREFIX" \
    -seed "$BASE_SEED"

echo "All combined Task 7 F4 runs completed."
