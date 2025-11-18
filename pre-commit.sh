source ./env/bin/activate 
git add $(ruff format --diff --quiet | grep -E '^--- ' | awk '{print $2}')