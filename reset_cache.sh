# Permission command: chmod +x reset_cache.sh
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "cmps.db" -exec rm {} \; -quit