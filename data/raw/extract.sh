#!/bin/bash

# Configurable variable
RAW_FILE_NAME="raw"
TRAIN_FILE_NAME="train"
VALIDATION_FILE_NAME="validation"
TEST_FILE_NAME="test"

languages=("python:.py" "c++:.cpp .cc") # Simple array to store languages and extensions
curr_project="./DeepSpeech-master"
chosen_languages=("python" "c++") # Specify languages to process

# Consolidate files for each chosen language
for lang_entry in "${languages[@]}"; do
    lang="${lang_entry%%:*}"        # Extract language
    extensions="${lang_entry#*:}"   # Extract extensions

    # Skip languages not chosen
    if [[ ! " ${chosen_languages[@]} " =~ " ${lang} " ]]; then
        continue
    fi

    echo "Processing language: $lang"
    lang_dir="../$lang"
    mkdir -p "$lang_dir"

    consolidated_file="$lang_dir/$RAW_FILE_NAME"
    >"$consolidated_file" # Create or empty the file

    # Find and process files with the specified extensions
    for ext in $extensions; do
        find "$curr_project" -type f -name "*$ext" -exec cat {} >>"$consolidated_file" \;
    done

    echo "Consolidated files for $lang into $consolidated_file"
done

# Split the consolidated training file into train, validation, and test datasets
for lang_entry in "${languages[@]}"; do
    lang="${lang_entry%%:*}"

    # Skip languages not chosen
    if [[ ! " ${chosen_languages[@]} " =~ " ${lang} " ]]; then
        continue
    fi

    lang_dir="../$lang"
    consolidated_file="$lang_dir/$RAW_FILE_NAME"

    if [[ -f "$consolidated_file" ]]; then
        total_lines=$(wc -l <"$consolidated_file")
        train_lines=$((total_lines * 80 / 100))
        validation_lines=$((total_lines * 10 / 100))
        test_lines=$((total_lines - train_lines - validation_lines))

        split_dir="$lang_dir/split"
        mkdir -p "$split_dir"

        head -n "$train_lines" "$consolidated_file" >"$split_dir/$TRAIN_FILE_NAME"
        tail -n +"$((train_lines + 1))" "$consolidated_file" | head -n "$validation_lines" >"$split_dir/$VALIDATION_FILE_NAME"
        tail -n "$test_lines" "$consolidated_file" >"$split_dir/$TEST_FILE_NAME"

        echo "Split $consolidated_file into $TRAIN_FILE_NAME, $VALIDATION_FILE_NAME, and $TEST_FILE_NAME in $split_dir"
    else
        echo "No consolidated file found for $lang. Skipping split."
    fi
done
