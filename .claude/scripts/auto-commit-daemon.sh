#!/bin/bash
# Auto-commit daemon: every 5 minutes, commit changes and push pending commits.
# Usage:
#   auto-commit-daemon.sh          Run continuously.
#   auto-commit-daemon.sh --once   Commit and push once.
#   auto-commit-daemon.sh --stop   Stop the daemon, then commit and push once.

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
PID_FILE="$REPO_DIR/.claude/.auto-commit-daemon.pid"
INTERVAL_SECONDS="${AUTO_COMMIT_INTERVAL_SECONDS:-300}"

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

commit_and_push() {
  cd "$REPO_DIR" || return 1

  if [ -n "$(git status --porcelain)" ]; then
    log "Changes detected; creating automatic commit."
    if ! git add -A; then
      log "ERROR: git add failed."
      return 1
    fi
    if ! git commit -m "Auto-commit (idle)"; then
      log "ERROR: git commit failed."
      return 1
    fi
  fi

  if ! git rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
    log "ERROR: current branch has no upstream; push skipped."
    return 1
  fi

  ahead_count="$(git rev-list --count '@{upstream}..HEAD' 2>/dev/null)" || {
    log "ERROR: could not determine pending commits."
    return 1
  }

  if [ "$ahead_count" -gt 0 ]; then
    log "Pushing $ahead_count pending commit(s)."
    if git push; then
      log "Push completed."
    else
      log "ERROR: push failed; it will be retried on the next run."
      return 1
    fi
  fi
}

stop_daemon() {
  if [ ! -f "$PID_FILE" ]; then
    return 0
  fi

  daemon_pid="$(cat "$PID_FILE" 2>/dev/null)"
  if [ -n "$daemon_pid" ] && kill -0 "$daemon_pid" 2>/dev/null; then
    daemon_command="$(ps -p "$daemon_pid" -o command= 2>/dev/null)"
    case "$daemon_command" in
      *auto-commit-daemon.sh*)
        kill "$daemon_pid" 2>/dev/null || true
        log "Stopped daemon process $daemon_pid."
        ;;
      *)
        log "WARNING: stale PID file did not point to this daemon."
        ;;
    esac
  fi
  rm -f "$PID_FILE"
}

case "${1:-}" in
  --once)
    commit_and_push
    exit $?
    ;;
  --stop)
    stop_daemon
    commit_and_push
    exit $?
    ;;
  "")
    ;;
  *)
    printf 'Usage: %s [--once|--stop]\n' "$0" >&2
    exit 2
    ;;
esac

if [ -f "$PID_FILE" ]; then
  existing_pid="$(cat "$PID_FILE" 2>/dev/null)"
  if [ -n "$existing_pid" ] && kill -0 "$existing_pid" 2>/dev/null; then
    existing_command="$(ps -p "$existing_pid" -o command= 2>/dev/null)"
    case "$existing_command" in
      *auto-commit-daemon.sh*)
        log "Daemon already running as process $existing_pid."
        exit 0
        ;;
    esac
  fi
  rm -f "$PID_FILE"
fi

echo $$ > "$PID_FILE"
cleanup() {
  if [ "$(cat "$PID_FILE" 2>/dev/null)" = "$$" ]; then
    rm -f "$PID_FILE"
  fi
}
trap cleanup EXIT INT TERM

log "Daemon started as process $$; interval is ${INTERVAL_SECONDS}s."
while true; do
  sleep "$INTERVAL_SECONDS" || exit 0
  commit_and_push || true
done
