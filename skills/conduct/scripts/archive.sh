#!/usr/bin/env bash
# archive.sh — archive a closed work's essence into the memory log and
# clean the executive memory.
#
# Contract:
#   1. Move .ai/work/<slug>-summary.md
#      -> .ai/memory/log/<YYYY-MM-DD>-<slug>.md
#      (date from plan.md frontmatter `created:` field, else today)
#   2. Remove plan.md, tasks.md, walkthrough.md, PRD.md from .ai/work/
#   3. Leave any other file in .ai/work/ untouched — and abort before
#      doing anything if unexpected files are found, so the developer
#      decides about them.
#   4. Refuse to archive while tasks.md still has unchecked tasks.
#
# The log is append-only: this script never overwrites an existing
# entry.
#
# Usage:
#   bash scripts/archive.sh <slug>
#
# Run from the repository root. Exits non-zero on any precondition
# failure.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <slug>" >&2
  exit 2
fi

SLUG="$1"
WORK_DIR=".ai/work"
LOG_DIR=".ai/memory/log"
SUMMARY_PATH="${WORK_DIR}/${SLUG}-summary.md"
PLAN_PATH="${WORK_DIR}/plan.md"
TASKS_PATH="${WORK_DIR}/tasks.md"

# --- preconditions ---------------------------------------------------

[[ -d "${WORK_DIR}" ]] || { echo "error: ${WORK_DIR} not found" >&2; exit 1; }
[[ -f "${SUMMARY_PATH}" ]] || { echo "error: summary not found at ${SUMMARY_PATH}" >&2; exit 1; }

# Guard: refuse to archive work with unchecked tasks.
if [[ -f "${TASKS_PATH}" ]] && grep -Eq '^[[:space:]]*-[[:space:]]*\[ \]' "${TASKS_PATH}"; then
  echo "error: ${TASKS_PATH} still has unchecked tasks." >&2
  echo "Finish, drop, or re-plan them before archiving." >&2
  exit 1
fi

# Pick the archive date: prefer `created:` from plan.md frontmatter,
# fall back to today.
ARCHIVE_DATE=""
if [[ -f "${PLAN_PATH}" ]]; then
  ARCHIVE_DATE="$(grep -E '^created:' "${PLAN_PATH}" | head -n1 | sed -E 's/created:[[:space:]]*//' | tr -d "'\"\r" | cut -d' ' -f1 || true)"
fi
if [[ -z "${ARCHIVE_DATE}" ]]; then
  ARCHIVE_DATE="$(date -u +%Y-%m-%d)"
fi

# Check for unexpected files in work/ (besides the known ones).
UNEXPECTED=()
while IFS= read -r -d '' f; do
  base="$(basename "$f")"
  case "$base" in
    plan.md|tasks.md|walkthrough.md|PRD.md|"${SLUG}-summary.md"|.gitignore) ;;
    *) UNEXPECTED+=("$base") ;;
  esac
done < <(find "${WORK_DIR}" -maxdepth 1 -type f -print0)

if (( ${#UNEXPECTED[@]} > 0 )); then
  echo "error: unexpected files in ${WORK_DIR}:" >&2
  printf '  - %s\n' "${UNEXPECTED[@]}" >&2
  echo "Resolve manually before archiving." >&2
  exit 1
fi

# --- archive ---------------------------------------------------------

mkdir -p "${LOG_DIR}"
ARCHIVE_PATH="${LOG_DIR}/${ARCHIVE_DATE}-${SLUG}.md"

if [[ -e "${ARCHIVE_PATH}" ]]; then
  echo "error: log entry already exists: ${ARCHIVE_PATH}" >&2
  echo "The log is append-only. Pick a distinct slug (e.g. suffix -2)." >&2
  exit 1
fi

mv "${SUMMARY_PATH}" "${ARCHIVE_PATH}"

# --- clean the executive memory --------------------------------------

rm -f "${WORK_DIR}/plan.md" "${WORK_DIR}/tasks.md" \
      "${WORK_DIR}/walkthrough.md" "${WORK_DIR}/PRD.md"

# --- report ----------------------------------------------------------

echo "archived: ${ARCHIVE_PATH}"
echo "work:     cleaned"
