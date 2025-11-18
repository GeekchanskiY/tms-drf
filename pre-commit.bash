#!/bin/bash
source ./env/bin/activate

changed_files=$(ruff format --diff --quiet | grep -E '^--- ' | awk '{print $2}')

ruff format

if [ -n "$changed_files" ]; then
    git add $changed_files
fi
