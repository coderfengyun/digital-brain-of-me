#!/bin/bash
# Auto-commit daemon: every 5 minutes, commit and push if there are changes.
# Launched by SessionStart hook, killed by Stop hook via PID file.

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
PID_FILE="$REPO_DIR/.claude/.auto-commit-daemon.pid"

# Write PID for cleanup
echo $$ > "$PID_FILE"

while true; do
  sleep 300
  cd "$REPO_DIR" || exit 1
  if [ -n "$(git status --porcelain)" ]; then
    git add -A && git commit -m "Auto-commit (idle)" && git push
  fi
done
