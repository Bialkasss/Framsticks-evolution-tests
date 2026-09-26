#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_PATH="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
PYTHON_COMMAND="${PYTHON_COMMAND:-python}"
OUTPUT_DIR="$SCRIPT_DIR/analysis_outputs_readable/landscape"

if command -v cygpath >/dev/null 2>&1; then
    LIBRARY_PATH="$(cygpath -w "$LIBRARY_PATH")"
fi

cd "$SCRIPT_DIR"
"$PYTHON_COMMAND" collect_task7_landscape.py \
    -path "$LIBRARY_PATH" \
    -neighbors "${NEIGHBORS:-20}" \
    -parents-per-representation "${PARENTS_PER_REPRESENTATION:-5}" \
    -output-dir "$OUTPUT_DIR"
"$PYTHON_COMMAND" plot_task7_landscape.py