#!/usr/bin/env bash
# cleanup.sh — archive a plan summary and empty .ai/session/.
#
# Contract:
#   1. Move .ai/session/<slug>-summary.md
#      -> .ai/memory/archive/plans/<YYYY-MM-DD>-<slug>.md
#      (date from plan.md frontmatter `created:` field, else today)
#   2. Remove plan.md, tasks.md, walkthrough.md from .ai/session/
#   3. Leave any other file in .ai/session/ untouched (and abort if found
#      with a non-empty list, so the developer can decide).
#
# Usage:
#   bash scripts/cleanup.sh <slug>
#
# Run from the repository root. Exits non-zero on any precondition failure.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <slug>" >&2
  exit 2
fi

SLUG="$1"
SESSION_DIR=".ai/session"
ARCHIVE_DIR=".ai/memory/archive/plans"
SUMMARY_PATH="${SESSION_DIR}/${SLUG}-summary.md"
PLAN_PATH="${SESSION_DIR}/plan.md"

# --- preconditions ---------------------------------------------------

[[ -d "${SESSION_DIR}" ]] || { echo "error: ${SESSION_DIR} not found" >&2; exit 1; }
[[ -f "${SUMMARY_PATH}" ]] || { echo "error: summary not found at ${SUMMARY_PATH}" >&2; exit 1; }

# Pick the archive date: prefer `created:` from plan.md frontmatter,
# fall back to today.
ARCHIVE_DATE=""
if [[ -f "${PLAN_PATH}" ]]; then
  ARCHIVE_DATE="$(grep -E '^created:' "${PLAN_PATH}" | head -n1 | sed -E 's/created:[[:space:]]*//' | tr -d '"' || true)"
fi
if [[ -z "${ARCHIVE_DATE}" ]]; then
  ARCHIVE_DATE="$(date -u +%Y-%m-%d)"
fi

# Check for unexpected files in session (besides the four known ones).
UNEXPECTED=()
while IFS= read -r -d '' f; do
  base="$(basename "$f")"
  case "$base" in
    plan.md|tasks.md|walkthrough.md|"${SLUG}-summary.md") ;;
    *) UNEXPECTED+=("$base") ;;
  esac
done < <(find "${SESSION_DIR}" -maxdepth 1 -type f -print0)

if (( ${#UNEXPECTED[@]} > 0 )); then
  echo "error: unexpected files in ${SESSION_DIR}:" >&2
  printf '  - %s\n' "${UNEXPECTED[@]}" >&2
  echo "Resolve manually before running cleanup." >&2
  exit 1
fi

# --- archive ---------------------------------------------------------

mkdir -p "${ARCHIVE_DIR}"
ARCHIVE_PATH="${ARCHIVE_DIR}/${ARCHIVE_DATE}-${SLUG}.md"

if [[ -e "${ARCHIVE_PATH}" ]]; then
  echo "error: archive target already exists: ${ARCHIVE_PATH}" >&2
  echo "Refusing to overwrite. Rename or remove before retrying." >&2
  exit 1
fi

mv "${SUMMARY_PATH}" "${ARCHIVE_PATH}"

# --- empty session ---------------------------------------------------

rm -f "${SESSION_DIR}/plan.md" "${SESSION_DIR}/tasks.md" "${SESSION_DIR}/walkthrough.md"

# --- report ----------------------------------------------------------

echo "archived: ${ARCHIVE_PATH}"
echo "session:  emptied"
