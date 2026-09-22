#!/usr/bin/env bash
set -euo pipefail

# Modes:
#   MODE=collect  run only the selected representations (default)
#   MODE=analyze merge existing per-run files and create all plots
MODE="${MODE:-collect}"
FORMAT_LIST="${FORMAT_LIST:-0 1 4 H}"
read -r -a FORMATS <<< "$FORMAT_LIST"
RUNS="${RUNS:-50}"
TOTAL_WORKERS="${TOTAL_WORKERS:-12}"
BASE_SEED="${BASE_SEED:-106}"
NEIGHBORS="${NEIGHBORS:-20}"
MAX_ITERATIONS="${MAX_ITERATIONS:-100}"
STAGNATION="${STAGNATION:-10}"
OUTPUT_DIR="${OUTPUT_DIR:-task4-neighbourhood}"
PYTHON_COMMAND="${PYTHON_COMMAND:-python}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/.." && pwd)"
COLLECTOR="$SCRIPT_DIR/collect_velocity_samples.py"
MERGER="$SCRIPT_DIR/merge_velocity_samples.py"
PLOTTER="$SCRIPT_DIR/plot_velocity_samples.py"

if [[ "$MODE" != "collect" && "$MODE" != "analyze" ]]; then
    echo "MODE must be collect or analyze, got: $MODE" >&2
    exit 1
fi

for genetic_format in "${FORMATS[@]}"; do
    case "$genetic_format" in
        0|1|4|H) ;;
        *) echo "Invalid format '$genetic_format'; use 0, 1, 4, or H." >&2; exit 1 ;;
    esac
done

if command -v cygpath >/dev/null 2>&1; then
    LIBRARY_PATH="$(cygpath -w "$LIBRARY_PATH")"
fi

cd "$SCRIPT_DIR"

if [[ "$MODE" == "analyze" ]]; then
    mkdir -p "$OUTPUT_DIR"
    "$PYTHON_COMMAND" "$MERGER" -input-dir "$OUTPUT_DIR" -output-prefix "$OUTPUT_DIR/velocity-all"
    "$PYTHON_COMMAND" "$PLOTTER" \
        -samples "$OUTPUT_DIR/velocity-all-samples.csv" \
        -neighbors "$OUTPUT_DIR/velocity-all-neighbors.csv" \
        -output-prefix "$OUTPUT_DIR/velocity-all"
    echo "Velocity analysis completed for files in $OUTPUT_DIR."
    exit 0
fi

mkdir -p "$OUTPUT_DIR"

run_experiment() {
    local genetic_format="$1"
    local run_number="$2"
    echo "========== STARTING f${genetic_format}, RUN ${run_number} =========="
    "$PYTHON_COMMAND" "$COLLECTOR" \
        -path "$LIBRARY_PATH" \
        -genetic-format "$genetic_format" \
        -run "$run_number" \
        -seed "$((BASE_SEED + run_number))" \
        -output-dir "$OUTPUT_DIR" \
        -neighbors "$NEIGHBORS" \
        -max-iterations "$MAX_ITERATIONS" \
        -stagnation "$STAGNATION"
}

job_formats=()
job_runs=()
for genetic_format in "${FORMATS[@]}"; do
    for run_number in $(seq 1 "$RUNS"); do
        job_formats+=("$genetic_format")
        job_runs+=("$run_number")
    done
done

next_job=0
active_jobs=0
total_jobs=${#job_formats[@]}
while (( next_job < total_jobs || active_jobs > 0 )); do
    while (( active_jobs < TOTAL_WORKERS && next_job < total_jobs )); do
        run_experiment "${job_formats[$next_job]}" "${job_runs[$next_job]}" &
        active_jobs=$((active_jobs + 1))
        next_job=$((next_job + 1))
    done
    if (( active_jobs > 0 )); then
        wait -n
        active_jobs=$((active_jobs - 1))
    fi
done

echo "Selected velocity sample climbs completed for formats: ${FORMATS[*]}"
echo "Run MODE=analyze later after all per-run files have been combined."