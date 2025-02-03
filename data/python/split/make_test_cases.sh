#!/bin/bash

# Ensure the test_cases directory exists
mkdir -p test_cases

# Input file
INPUT_FILE="test"

# Check if file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: File '$INPUT_FILE' not found."
    exit 1
fi

# Read the file in chunks
line_counts=(10 10 10 10 10 10 10 10 10 10 20 20 20 20 20 20 20 20 20 20 50 50 50 50 50 50 50 50 50 50)
chunk_index=1
start_line=1

total_lines=$(wc -l < "$INPUT_FILE")

for lines in "${line_counts[@]}"; do
    end_line=$((start_line + lines - 1))
    sed -n "${start_line},${end_line}p" "$INPUT_FILE" > "test_cases/test_case_${chunk_index}_${lines}lines.txt"
    start_line=$((end_line + 1))
    ((chunk_index++))
    if [[ $start_line -gt $total_lines ]]; then
        exit 0
    fi
done

# Handle remaining lines in chunks of 100
while [[ $start_line -le $total_lines ]]; do
    end_line=$((start_line + 100 - 1))
    sed -n "${start_line},${end_line}p" "$INPUT_FILE" > "test_cases/test_case_${chunk_index}_100lines.txt"
    start_line=$((end_line + 1))
    ((chunk_index++))
done

echo "Chunks have been written to the 'test_cases' directory."