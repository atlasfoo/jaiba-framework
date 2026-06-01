#!/usr/bin/env bash
# archive.sh — archive a delivered spec into long-term memory and remove
# the active spec folder.
#
# Contract:
#   1. Move the drafted archive doc
#      .ai/specs/<slug>/archive.md
#      -> .ai/memory/archive/specs/<YYYY-MM-DD>-<slug>.md
#      (date = today, the archival date — NOT the PRD creation date)
#   2. Remove the .ai/specs/<slug>/ folder entirely.
#
# Preconditions (abort non-zero if any fails):
#   - .ai/specs/<slug>/ exists.
#   - .ai/specs/<slug>/archive.md exists (the reviewed draft).
#   - every story in user-stories.md is checked (no "- [ ]" / "[ ]"
#     unchecked markers) — a guard against archiving an open spec.
#
# Usage:
#   bash scripts/archive.sh <spec-slug>
#
# Run from the repository root. Exits non-zero on any precondition failure.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <spec-slug>" >&2
  exit 2
fi

SLUG="$1"
SPEC_DIR=".ai/specs/${SLUG}"
ARCHIVE_DIR=".ai/memory/archive/specs"
DRAFT_PATH="${SPEC_DIR}/archive.md"
STORIES_PATH="${SPEC_DIR}/user-stories.md"

# --- preconditions ---------------------------------------------------

[[ -d "${SPEC_DIR}" ]]   || { echo "error: spec folder not found at ${SPEC_DIR}" >&2; exit 1; }
[[ -f "${DRAFT_PATH}" ]] || { echo "error: archive draft not found at ${DRAFT_PATH} (draft it before archiving)" >&2; exit 1; }

# Guard: refuse to archive a spec with open stories. Stories carry a
# status marker `[ ]` (open) / `[x]` (closed), either backtick-wrapped
# (`[ ]`) or as a markdown checkbox (- [ ]).
if [[ -f "${STORIES_PATH}" ]]; then
  if grep -Eq '^[[:space:]]*`?\[ \]' "${STORIES_PATH}" \
     || grep -Eq '^[[:space:]]*-[[:space:]]*\[ \]' "${STORIES_PATH}"; then
    echo "error: ${STORIES_PATH} still has unchecked stories." >&2
    echo "Finish, drop, or split them before archiving." >&2
    exit 1
  fi
fi

# --- archive ---------------------------------------------------------

ARCHIVE_DATE="$(date -u +%Y-%m-%d)"
mkdir -p "${ARCHIVE_DIR}"
ARCHIVE_PATH="${ARCHIVE_DIR}/${ARCHIVE_DATE}-${SLUG}.md"

if [[ -e "${ARCHIVE_PATH}" ]]; then
  echo "error: archive target already exists: ${ARCHIVE_PATH}" >&2
  echo "Refusing to overwrite. Rename or remove before retrying." >&2
  exit 1
fi

mv "${DRAFT_PATH}" "${ARCHIVE_PATH}"

# --- remove the active spec folder -----------------------------------

rm -rf "${SPEC_DIR}"

# --- report ----------------------------------------------------------

echo "archived: ${ARCHIVE_PATH}"
echo "spec:     ${SPEC_DIR} removed"
