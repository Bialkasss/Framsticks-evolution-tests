#!/usr/bin/env bash
set -euo pipefail

# --- Audio notification setup ---
play_success() {
    # 2 beeps on success
    powershell.exe -NoProfile -Command "1..2 | ForEach-Object { [Console]::Beep(1000, 600); Start-Sleep -Milliseconds 150 }" >/dev/null 2>&1 || true
}

play_error() {
    # 3 beeps on error
    powershell.exe -NoProfile -Command "1..3 | ForEach-Object { [Console]::Beep(1000, 600); Start-Sleep -Milliseconds 150 }" >/dev/null 2>&1 || true
}

cleanup_and_notify() {
    local exit_code=$?
    if [ "$exit_code" -eq 0 ]; then
        echo "Script finished successfully!"
        play_success
    else
        echo "Script failed or aborted with exit code $exit_code!"
        play_error
    fi
}

trap cleanup_and_notify EXIT
# --------------------------------

# Override these values by exporting environment variables before running the script.
GENETIC_FORMAT=1
POP_SIZE=50
GENERATIONS=1000
STAGNATION=25
PROBABILITY_VALUES=(5)
RUNS=10
TOTAL_WORKERS=12
BASE_SEED=106


if (( ${#PROBABILITY_VALUES[@]} == 0 )); then
    echo "At least one probability value is required." >&2
    exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PYTHON_COMMAND="${PYTHON_COMMAND:-python}"
EVOLUTION_SCRIPT="$SCRIPT_DIR/FramsticksEvolution.py"

if [[ ! -f "$EVOLUTION_SCRIPT" ]]; then
    echo "Evolution script not found: $EVOLUTION_SCRIPT" >&2
    exit 1
fi

# Git Bash may invoke the Windows Python executable, so pass a Windows path
# to the native Framsticks library.
if command -v cygpath >/dev/null 2>&1; then
    LIBRARY_PATH="$(cygpath -w "$LIBRARY_PATH")"
fi

cd "$SCRIPT_DIR"

run_experiment() {
    local probability="$1"
    local run_number="$2"
    local simulation="eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim;my-own-probab-${probability}.sim"
    local hall_of_fame="HoF-vel-probab-${probability}-${run_number}.gen"
    local output_prefix="results-vel-probab-${probability}-${run_number}"
    local dynamic_schedule_args=()
    if [[ "$probability" == "5" ]]; then
        dynamic_schedule_args=(-dynamic_mutation_schedule)
    fi

    echo "========== STARTING PROBABILITY ${probability}, RUN ${run_number} =========="
    "$PYTHON_COMMAND" "$EVOLUTION_SCRIPT" \
        -path "$LIBRARY_PATH" \
        -sim "$simulation" \
        -opt velocity \
        -max_numparts 15 \
        -max_numjoints 30 \
        -max_numneurons 20 \
        -max_numconnections 30 \
        -genformat "$GENETIC_FORMAT" \
        -pxov 0 \
        -popsize "$POP_SIZE" \
        -generations "$GENERATIONS" \
        -stagnation "$STAGNATION" \
        -runs 1 \
        -workers 1 \
        -hof_size 1 \
        -hof_savefile "$hall_of_fame" \
        -output_prefix "$output_prefix" \
        -seed "$((BASE_SEED + run_number - 1))" \
        "${dynamic_schedule_args[@]}"
}

job_probabilities=()
job_runs=()
for probability in "${PROBABILITY_VALUES[@]}"; do
    for run_number in $(seq 1 "$RUNS"); do
        job_probabilities+=("$probability")
        job_runs+=("$run_number")
    done
done

next_job=0
active_jobs=0
total_jobs=${#job_probabilities[@]}

while (( next_job < total_jobs || active_jobs > 0 )); do
    while ((
        active_jobs < TOTAL_WORKERS &&
        next_job < total_jobs
    )); do
        run_experiment "${job_probabilities[$next_job]}" "${job_runs[$next_job]}" &
        active_jobs=$((active_jobs + 1))
        next_job=$((next_job + 1))
    done

    if (( active_jobs > 0 )); then
        # Start the next individual run as soon as any active run finishes.
        wait -n
        active_jobs=$((active_jobs - 1))
    fi
done

echo 'All velocity probability experiments completed.'
