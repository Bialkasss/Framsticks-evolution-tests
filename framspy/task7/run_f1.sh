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
        echo "Task 7 F1 experiment finished successfully!"
        play_success
    else
        echo "Task 7 F1 experiment failed or was aborted with exit code $exit_code!"
        play_error
    fi
}

trap cleanup_and_notify EXIT

# Override these values by exporting environment variables before running the script.
GENETIC_FORMAT="${GENETIC_FORMAT:-1}"
POP_SIZE="${POP_SIZE:-50}"
GENERATIONS="${GENERATIONS:-200}"
STAGNATION="${STAGNATION:-50}"
RUNS="${RUNS:-10}"
TOTAL_WORKERS="${TOTAL_WORKERS:-12}"
BASE_SEED="${BASE_SEED:-107}"
MUTATION_PROBABILITY="${MUTATION_PROBABILITY:-0.9}"
CROSSOVER_PROBABILITY="${CROSSOVER_PROBABILITY:-0.2}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
PYTHON_COMMAND="${PYTHON_COMMAND:-python}"
EVOLUTION_SCRIPT="$SCRIPT_DIR/../FramsticksEvolution.py"
SIMULATION_DIR="$SCRIPT_DIR"

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

run_experiment() {
    local run_number="$1"
    local hall_of_fame="task7-f1-hof-run${run_number}.gen"
    local output_prefix="task7-f1-run${run_number}"

    echo "========== STARTING TASK 7 F1 RUN ${run_number}/${RUNS} =========="
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
        -runs 1 \
        -workers 1 \
        -hof_size 1 \
        -hof_savefile "$hall_of_fame" \
        -output_prefix "$output_prefix" \
        -seed "$((BASE_SEED + run_number - 1))"
}

next_run=1
active_jobs=0

while (( next_run <= RUNS || active_jobs > 0 )); do
    while (( active_jobs < TOTAL_WORKERS && next_run <= RUNS )); do
        run_experiment "$next_run" &
        active_jobs=$((active_jobs + 1))
        next_run=$((next_run + 1))
    done

    if (( active_jobs > 0 )); then
        wait -n
        active_jobs=$((active_jobs - 1))
    fi
done

echo "All ${RUNS} Task 7 F1 runs completed."
