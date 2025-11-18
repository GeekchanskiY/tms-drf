source ./env/bin/activate 

ruff format

git add $(ruff format --diff --quiet | grep -E '^--- ' | awk '{print $2}')