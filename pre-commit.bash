#!/bin/bash
source ./env/bin/activate

changed_files=$(ruff format --diff --quiet | grep -E '^--- ' | awk '{print $2}')

ruff format

if [ -n "$changed_files" ]; then
    git add $changed_files
fi

changed_files=$(ruff check --select I --output-format=json | jq -r '.[].filename' | sort -u)

ruff check --select I --fix

if [ -n "$changed_files" ]; then
    git add $changed_files
fi