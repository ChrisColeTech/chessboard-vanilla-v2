#!/bin/bash
# ID Setter Runner Script
SCRIPT_DIR="$(dirname "$0")"
PROJECT_ROOT="$SCRIPT_DIR/../../.."
cd "$PROJECT_ROOT"
python3 "$SCRIPT_DIR/main.py" "$@" > id_setter_output.txt 2>&1