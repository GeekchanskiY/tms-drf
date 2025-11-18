#!/bin/bash
source ./env/bin/activate

# Collect files Ruff would change into a variable
changed_files=$(ruff format --diff --quiet | grep -E '^--- ' | awk '{print $2}')

# Run Ruff formatting
ruff format

# Stage only those files
if [ -n "$changed_files" ]; then
    git add $changed_files
    echo "Staged files changed by Ruff:"
    echo "$changed_files"
else
    echo "No files were changed by Ruff."
fi
