#!/bin/bash
# Scans all git repos under "C:/Repositories for Git/" and prints recent commits.
# Searches up to 3 levels deep to find repos in subdirectories.
# Usage: bash scan-repos.sh YYYY-MM-DD [HH:MM]

SINCE_DATE="$1"
SINCE_TIME="${2:-06:00}"
BASE="C:/Repositories for Git"

# Find all .git directories up to 3 levels deep, then log from their parent
find "$BASE" -maxdepth 3 -name .git -type d 2>/dev/null | while read gitdir; do
  repo="${gitdir%/.git}"
  name="${repo#$BASE/}"
  echo "=== $name ==="
  git -C "$repo" log --since="$SINCE_DATE $SINCE_TIME" --format="%h %s" --all 2>/dev/null
done
