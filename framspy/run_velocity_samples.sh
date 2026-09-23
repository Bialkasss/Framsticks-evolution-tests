#!/usr/bin/env bash
set -euo pipefail

# Modes:
#   MODE=collect  run only the selected representations (default)
#   MODE=analyze merge existing per-run files and create all plots
MODE="${MODE:-collect}"
FORMAT_LIST="${FORMAT_LIST:-0 1 4 H}"
read -r -a FORMATS <<< "$FORMAT_LIST"
TARGET_SAMPLES="${TARGET_SAMPLES:-200}"
SAMPLES_PER_RUN="${SAMPLES_PER_RUN:-4}"
PLOT_SAMPLES_PER_FORMAT="${PLOT_SAMPLES_PER_FORMAT:-200}"
TOTAL_WORKERS="${TOTAL_WORKERS:-12}"
BASE_SEED="${BASE_SEED:-106}"
NEIGHBORS="${NEIGHBORS:-20}"
MAX_ITERATIONS="${MAX_ITERATIONS:-1000}"
STAGNATION="${STAGNATION:-20}"
NEUTRAL_STEPS="${NEUTRAL_STEPS:-1000}"
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
shopt -s nullglob
mkdir -p "$OUTPUT_DIR"
if command -v cygpath >/dev/null 2>&1; then
    OUTPUT_DIR="$(cygpath -m "$(cd -- "$OUTPUT_DIR" && pwd)")"
else
    OUTPUT_DIR="$(cd -- "$OUTPUT_DIR" && pwd)"
fi

if [[ "$MODE" == "analyze" ]]; then
    mkdir -p "$OUTPUT_DIR"
    "$PYTHON_COMMAND" "$MERGER" -input-dir "$OUTPUT_DIR" -output-prefix "$OUTPUT_DIR/velocity-all"
    "$PYTHON_COMMAND" "$PLOTTER" \
        -samples "$OUTPUT_DIR/velocity-all-samples.csv" \
        -neighbors "$OUTPUT_DIR/velocity-all-neighbors.csv" \
        -output-prefix "$OUTPUT_DIR/velocity-all" \
        -samples-per-format "$PLOT_SAMPLES_PER_FORMAT"
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
        -stagnation "$STAGNATION" \
        -neutral-steps "$NEUTRAL_STEPS" \
        -samples-per-run "$SAMPLES_PER_RUN"
}

count_samples() {
    local genetic_format="$1"
    local markers=("$OUTPUT_DIR"/velocity-f"$genetic_format"-run*-complete)
    local total=0
    for marker in "${markers[@]}"; do
        local samples_file="${marker%-complete}-samples.csv"
        if [[ -f "$samples_file" ]]; then
            local count
            count=$(awk 'FNR > 1 { count++ } END { print count + 0 }' "$samples_file")
            total=$((total + count))
        fi
    done
    echo "$total"
}

for genetic_format in "${FORMATS[@]}"; do
    completed_samples=$(count_samples "$genetic_format")
    active_jobs=0
    next_run=1
    while (( completed_samples < TARGET_SAMPLES )); do
        while (( active_jobs < TOTAL_WORKERS && completed_samples + active_jobs * SAMPLES_PER_RUN < TARGET_SAMPLES )); do
            while [[ -f "$OUTPUT_DIR/velocity-f${genetic_format}-run${next_run}-complete" ]]; do
                next_run=$((next_run + 1))
            done
            run_experiment "$genetic_format" "$next_run" &
            active_jobs=$((active_jobs + 1))
            next_run=$((next_run + 1))
        done
        if (( active_jobs > 0 )); then
            wait -n
            active_jobs=$((active_jobs - 1))
            completed_samples=$(count_samples "$genetic_format")
        fi
    done
    echo "Collected ${completed_samples} samples for f${genetic_format}."
done

echo "Collected at least ${TARGET_SAMPLES} samples for formats: ${FORMATS[*]}"
echo "Run MODE=analyze later after all per-run files have been combined."