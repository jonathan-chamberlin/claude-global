#!/bin/bash
# Scans all git repos under "C:/Repositories for Git/" and prints recent commits.
# Usage: bash scan-repos.sh YYYY-MM-DD [HH:MM]

SINCE_DATE="$1"
SINCE_TIME="${2:-06:00}"

for dir in "C:/Repositories for Git"/*/; do
  if [ -d "$dir/.git" ]; then
    echo "=== $(basename "$dir") ==="
    git -C "$dir" log --since="$SINCE_DATE $SINCE_TIME" --format="%h %s" --all 2>/dev/null
  fi
done
