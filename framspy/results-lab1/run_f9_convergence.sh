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

# Run this many mutation settings simultaneously.
MUTATIONS_IN_PARALLEL=2
# Each mutation setting gets this many worker processes.
WORKERS_PER_MUTATION=6
RUNS_PER_MUTATION=10
GENERATIONS=1000
STAGNATION=50
SEED=12345
MUTATION_VALUES=(0 005 010 020 030 040 050)

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/.." && pwd)"

# Git Bash may invoke the Windows Python executable, so pass a Windows path
# to the native Framsticks library.
if command -v cygpath >/dev/null 2>&1; then
    LIBRARY_PATH="$(cygpath -w "$LIBRARY_PATH")"
fi

cd "$SCRIPT_DIR"

run_mutation() {
    local mutation="$1"
    local simulation="eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;f9-mut-${mutation}.sim"
    local output_prefix="results-f9-${mutation}"
    local hall_of_fame="HoF-f9-${mutation}-{run}.gen"

    echo "========== STARTING MUTATION ${mutation} (${RUNS_PER_MUTATION} runs, ${WORKERS_PER_MUTATION} workers) =========="
    python FramsticksEvolution.py \
        -path "$LIBRARY_PATH" \
        -sim "$simulation" \
        -opt vertpos \
        -max_numparts 30 \
        -max_numgenochars 50 \
        -initialgenotype '/*9*/BLU' \
        -popsize 50 \
        -generations "$GENERATIONS" \
        -stagnation "$STAGNATION" \
        -runs "$RUNS_PER_MUTATION" \
        -workers "$WORKERS_PER_MUTATION" \
        -seed "$SEED" \
        -hof_size 1 \
        -hof_savefile "$hall_of_fame" \
        -output_prefix "$output_prefix"
}

active_mutations=0
for mutation in "${MUTATION_VALUES[@]}"; do
    run_mutation "$mutation" &
    active_mutations=$((active_mutations + 1))
    if (( active_mutations >= MUTATIONS_IN_PARALLEL )); then
        wait
        active_mutations=0
    fi
done
wait

echo 'All mutation settings completed.'
