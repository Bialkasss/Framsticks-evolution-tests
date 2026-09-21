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

# Run this many genetic formats simultaneously.
FORMATS_IN_PARALLEL=2
# Each genetic format gets this many worker processes.
WORKERS_PER_FORMAT=6
RUNS_PER_FORMAT=6
GENERATIONS=1000
STAGNATION=25
SEED=12345
GENETIC_FORMATS=(0 1 4 9)

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PYTHON_COMMAND="${PYTHON_COMMAND:-python}"
EVOLUTION_SCRIPT="$SCRIPT_DIR/FramsticksEvolution_numparts.py"

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

run_format() {
    local genetic_format="$1"
    local simulation="eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;only-body.sim;uneven-ground.sim"
    local output_prefix="results-numparts-f${genetic_format}"
    local hall_of_fame="HoF-numparts-f${genetic_format}-{run}.gen"

    echo "========== STARTING FORMAT ${genetic_format} (${RUNS_PER_FORMAT} runs, ${WORKERS_PER_FORMAT} workers) =========="
    "$PYTHON_COMMAND" "$EVOLUTION_SCRIPT" \
        -path "$LIBRARY_PATH" \
        -sim "$simulation" \
        -opt vertpos \
        -max_numparts 30 \
        -max_numgenochars 50 \
        -genformat "$genetic_format" \
        -popsize 50 \
        -generations "$GENERATIONS" \
        -stagnation "$STAGNATION" \
        -runs "$RUNS_PER_FORMAT" \
        -workers "$WORKERS_PER_FORMAT" \
        -seed "$SEED" \
        -hof_size 1 \
        -hof_savefile "$hall_of_fame" \
        -output_prefix "$output_prefix"
}

active_formats=0
for genetic_format in "${GENETIC_FORMATS[@]}"; do
    run_format "$genetic_format" &
    active_formats=$((active_formats + 1))
    if (( active_formats >= FORMATS_IN_PARALLEL )); then
        wait
        active_formats=0
    fi
done
wait

echo 'All genetic format experiments completed.'
