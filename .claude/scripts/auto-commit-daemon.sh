#!/bin/bash
# Auto-commit daemon: every 5 minutes, commit changes and push pending commits.
# Usage:
#   auto-commit-daemon.sh          Run continuously.
#   auto-commit-daemon.sh --once   Commit and push once.
#   auto-commit-daemon.sh --stop   Stop the daemon, then commit and push once.
#   auto-commit-daemon.sh --approve  Approve an oversized change set once.

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
PID_FILE="$REPO_DIR/.claude/.auto-commit-daemon.pid"
REVIEW_FILE="$REPO_DIR/.claude/.auto-commit-review-required"
INTERVAL_SECONDS="${AUTO_COMMIT_INTERVAL_SECONDS:-300}"
MAX_CHANGED_FILES="${AUTO_COMMIT_MAX_FILES:-20}"
MAX_CHANGED_LINES="${AUTO_COMMIT_MAX_LINES:-2000}"
MAX_NEW_FILE_BYTES="${AUTO_COMMIT_MAX_NEW_FILE_BYTES:-20971520}"

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

notify_review_required() {
  changed_files="$1"
  if command -v osascript >/dev/null 2>&1; then
    osascript -e "display notification \"检测到 ${changed_files} 个变更文件，自动提交已暂停，请先确认。\" with title \"Digital Brain 等待提交确认\"" >/dev/null 2>&1 || true
  fi
}

review_required() {
  changed_files="$(git status --porcelain | wc -l | tr -d ' ')"
  changed_lines="$(git diff --numstat HEAD -- . | awk '$1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ { total += $1 + $2 } END { print total + 0 }')"
  large_file=""
  large_file_bytes=0

  while IFS= read -r -d '' candidate; do
    [ -f "$candidate" ] || continue
    candidate_bytes="$(wc -c < "$candidate" | tr -d ' ')"
    if [ "$candidate_bytes" -gt "$large_file_bytes" ]; then
      large_file="$candidate"
      large_file_bytes="$candidate_bytes"
    fi
  done < <(
    git ls-files --others --exclude-standard -z
    git diff --cached --name-only --diff-filter=A -z
  )

  review_reason=""
  if [ "$changed_files" -gt "$MAX_CHANGED_FILES" ]; then
    review_reason="变更文件数 ${changed_files} 超过阈值 ${MAX_CHANGED_FILES}"
  fi
  if [ "$changed_lines" -gt "$MAX_CHANGED_LINES" ]; then
    [ -n "$review_reason" ] && review_reason="$review_reason；"
    review_reason="${review_reason}增删行数 ${changed_lines} 超过阈值 ${MAX_CHANGED_LINES}"
  fi
  if [ "$large_file_bytes" -gt "$MAX_NEW_FILE_BYTES" ]; then
    [ -n "$review_reason" ] && review_reason="$review_reason；"
    review_reason="${review_reason}新文件 ${large_file} 大小为 ${large_file_bytes} 字节，超过阈值 ${MAX_NEW_FILE_BYTES}"
  fi

  if [ -z "$review_reason" ]; then
    rm -f "$REVIEW_FILE"
    return 1
  fi

  change_signature="$(git status --porcelain=v1 -z | shasum | awk '{print $1}')"
  previous_signature="$(sed -n 's/^signature=//p' "$REVIEW_FILE" 2>/dev/null)"
  if [ "$change_signature" != "$previous_signature" ]; then
    {
      printf 'signature=%s\n' "$change_signature"
      printf 'created_at=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
      printf 'reason=%s\n' "$review_reason"
      printf 'changed_files=%s\n' "$changed_files"
      printf 'changed_lines=%s\n' "$changed_lines"
      printf 'largest_new_file=%s\n' "$large_file"
      printf 'largest_new_file_bytes=%s\n' "$large_file_bytes"
      printf '\n变更清单：\n'
      git status --short
    } > "$REVIEW_FILE"
    notify_review_required "$changed_files"
  fi

  log "REVIEW REQUIRED: $review_reason. Automatic commit paused."
  return 0
}

commit_and_push() {
  approve_oversized="${1:-0}"
  cd "$REPO_DIR" || return 1

  if [ -n "$(git status --porcelain)" ]; then
    if [ "$approve_oversized" != "1" ] && review_required; then
      :
    else
      rm -f "$REVIEW_FILE"
      if [ "$approve_oversized" = "1" ]; then
        log "Oversized change set approved; creating automatic commit."
      else
        log "Changes detected; creating automatic commit."
      fi
      if ! git add -A; then
        log "ERROR: git add failed."
        return 1
      fi
      if ! git commit -m "Auto-commit (idle)"; then
        log "ERROR: git commit failed."
        return 1
      fi
    fi
  else
    rm -f "$REVIEW_FILE"
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
  --approve)
    commit_and_push 1
    exit $?
    ;;
  "")
    ;;
  *)
    printf 'Usage: %s [--once|--stop|--approve]\n' "$0" >&2
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
