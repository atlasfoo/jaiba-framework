#!/usr/bin/env bash
# Filesystem-only closure helper, not a surface resolver. The caller must
# resolve ownership and establish serialized writers before either mode.
# prepare freezes evidence IN the visible summary; archive verifies the log
# before selective cleanup. No hidden receipt store or memory mirror.
# Usage: archive.sh {prepare|archive} "<slug>" "<project-id>" "<context-id>"
# Requires JAIBA_ARCHIVE_FILESYSTEM=1 JAIBA_ARCHIVE_SERIALIZED=1 (attestations,
# not locks). See references/summarize-mode.md before invoking.
set -euo pipefail
fail() { printf 'error: %s\n' "$*" >&2; exit 1; }
[[ $# == 4 ]] || fail "usage: $0 {prepare|archive} <slug> <project-id> <context-id>"
MODE=$1 SLUG=$2 PROJECT=$3 CONTEXT=$4
[[ $MODE == prepare || $MODE == archive ]] || fail 'unknown mode'
[[ $SLUG =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || fail 'use a safe slug (letters, digits, dot, underscore, hyphen; start with a letter or digit)'
# Identity is opaque data, never a path component or a value to normalize.
# Receipt fields are line-delimited; preserve all other bytes, including spaces.
for value in "$PROJECT" "$CONTEXT"; do
  [[ -n $value && $value != *$'\n'* && $value != *$'\r'* ]] || fail 'project/context IDs must be nonempty single-line values without CR or LF'
done
[[ ${JAIBA_ARCHIVE_FILESYSTEM:-} == 1 && ${JAIBA_ARCHIVE_SERIALIZED:-} == 1 ]] ||
  fail 'explicit filesystem binding and serialized-writer attestations required'
(( BASH_VERSINFO[0] >= 4 )) || fail 'Bash 4 or later required'
for tool in git grep sed tail cat cmp date mkdir rm; do
  command -v "$tool" >/dev/null || fail "required tool unavailable: $tool"
done
WORK=.ai/work LOG=.ai/memory/log SUMMARY=.ai/work/$SLUG-summary.md
FILES=(plan.md tasks.md walkthrough.md PRD.md .gitignore)
shopt -s nullglob dotglob

# All traversed components are local, real directories, never symlinks.
check_roots() {
  local path
  for path in .ai "$WORK" .ai/memory; do
    [[ -d $path && ! -L $path && -r $path && -x $path ]] || fail "not a readable real directory: $path"
  done
  local bundle=0 legacy=0
  for path in .ai/memory/index.md .ai/memory/constitution.md; do
    if [[ -e $path || -L $path ]]; then
      [[ -f $path && ! -L $path ]] || fail "invalid layout marker: $path"
      if [[ $path == */index.md ]]; then bundle=1; else legacy=1; fi
    fi
  done
  (( bundle + legacy == 1 )) || fail 'missing or ambiguous filesystem brain'
  if [[ -e $LOG || -L $LOG ]]; then
    [[ -d $LOG && ! -L $LOG && -r $LOG && -x $LOG ]] || fail "not a readable real directory: $LOG"
  fi
}
inventory() {
  check_roots
  local path base
  for path in "$WORK"/*; do
    base=${path##*/}
    case "$base" in
      plan.md|tasks.md|walkthrough.md|PRD.md|.gitignore|"$SLUG-summary.md") ;;
      *) fail "unexpected work object: $path" ;;
    esac
    [[ -f $path && ! -L $path ]] || fail "not a regular work file: $path"
    [[ -r $path ]] || fail "unreadable work file: $path"
  done
}
# Git's blob fingerprint covers every byte, including serialized metadata and
# links, with no filters/normalization. It does not fingerprint OS attributes.
hash() { git hash-object --stdin; }
revision() {
  if [[ -e $WORK/$1 ]]; then hash < "$WORK/$1"; else printf 'absent\n'; fi
}
valid_hash() { [[ $1 =~ ^([0-9a-f]{40}|[0-9a-f]{64})$ ]]; }
inventory
ROOT=$(pwd -P)
SCOPE=$(printf '%s\n' filesystem "$ROOT" "$PROJECT" "$CONTEXT" | hash)
ARCHIVE=''
report_failure() {
  local status=$? path
  if (( status != 0 )); then
    printf 'closure incomplete; log candidate: %s; retained work objects:\n' "${ARCHIVE:-not appended}" >&2
    for path in "$WORK"/*; do printf '  %q\n' "$path" >&2; done
    printf 'Reconcile exact log/work state; do not choose a fresh close ID for retry.\n' >&2
  fi
}
trap report_failure EXIT

check_tasks() {
  if [[ -f $WORK/tasks.md ]]; then
    local status=0
    grep -Eq '^[[:space:]]*-[[:space:]]*\[ \]' "$WORK/tasks.md" || status=$?
    [[ $status == 1 ]] || fail 'unchecked tasks or failed task read'
  fi
}
emit_receipt() {
  printf '<!-- jaiba-close-v1\ncontract jaiba-memory-surface 1.0.0\nbinding filesystem\nproject %s\ncontext %s\nscope %s\nclose %s\nbody %s\n' "$PROJECT" "$CONTEXT" "$SCOPE" "$CLOSE" "$BODY"
  local i
  for i in "${!FILES[@]}"; do printf '%s %s\n' "${FILES[i]}" "${REVISIONS[i]}"; done
  printf '%s\n' '-->'
}

if [[ $MODE == prepare ]]; then
  [[ -f $SUMMARY ]] || fail "summary missing: $SUMMARY"
  [[ -f $WORK/plan.md ]] || fail 'plan required for initial closure'
  check_tasks
  status=0
  grep -q '^<!-- jaiba-close-v1' "$SUMMARY" || status=$?
  [[ $status == 1 ]] || fail 'existing/reserved receipt marker; reconcile instead of preparing again'
  # Preserve the existing date convention, but only a valid ISO-shaped date
  # may enter a path. The frozen close ID, not today's date, governs retries.
  CREATED=$(sed -n "s/^created:[[:space:]]*['\"]*\([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\).*/\1/p" "$WORK/plan.md")
  if [[ -z $CREATED ]]; then CREATED=$(date -u +%Y-%m-%d); fi
  [[ $CREATED =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || fail 'ambiguous plan creation date'
  CLOSE=$CREATED-$SLUG ARCHIVE=$LOG/$CREATED-$SLUG.md
  [[ ! -e $ARCHIVE && ! -L $ARCHIVE ]] || fail 'close ID already exists; reconcile existing log'
  REVISIONS=()
  for name in "${FILES[@]}"; do REVISIONS+=("$(revision "$name")"); done
  BODY=$({ cat "$SUMMARY"; printf '\n'; } | hash)
  { printf '\n'; emit_receipt; } >> "$SUMMARY"
  printf 'prepared: %s\nclose: %s\nscope: %s\nPresent the full summary, then obtain explicit confirmation before archive.\n' "$SUMMARY" "$CLOSE" "$SCOPE"
  exit 0
fi

# A deleted draft on retry is recoverable from the unique immutable log.
# Never derive a new date from a partially deleted plan or the current clock.
if [[ -f $SUMMARY ]]; then SOURCE=$SUMMARY; else
  candidates=("$LOG"/????-??-??-"$SLUG".md)
  (( ${#candidates[@]} == 1 )) || fail 'missing summary and no unique closing log; supply original evidence'
  SOURCE=${candidates[0]}
fi
[[ -f $SOURCE && ! -L $SOURCE && -r $SOURCE ]] || fail 'invalid receipt source'
RECEIPT_TEXT=$(tail -n 14 "$SOURCE")
mapfile -t RECEIPT <<< "$RECEIPT_TEXT"
(( ${#RECEIPT[@]} == 14 )) || fail 'incomplete closure receipt'
[[ ${RECEIPT[0]} == '<!-- jaiba-close-v1' && ${RECEIPT[1]} == 'contract jaiba-memory-surface 1.0.0' && ${RECEIPT[2]} == 'binding filesystem' && ${RECEIPT[13]} == '-->' ]] || fail 'invalid receipt contract/binding'
[[ ${RECEIPT[3]} == "project $PROJECT" && ${RECEIPT[4]} == "context $CONTEXT" && ${RECEIPT[5]} == "scope $SCOPE" ]] || fail 'different filesystem/project/context'
CLOSE=${RECEIPT[6]#close }
[[ ${RECEIPT[6]} == "close $CLOSE" && $CLOSE =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}- && ${CLOSE:11} == "$SLUG" ]] || fail 'invalid close ID'
BODY=${RECEIPT[7]#body }
valid_hash "$BODY" || fail 'invalid summary fingerprint'
REVISIONS=()
for i in "${!FILES[@]}"; do
  entry=${RECEIPT[i+8]}
  rev=${entry#"${FILES[i]} "}
  [[ $entry == "${FILES[i]} $rev" ]] || fail 'invalid inventory receipt'
  [[ $rev == absent ]] || valid_hash "$rev" || fail 'invalid revision'
  REVISIONS+=("$rev")
done
verify_payload() {
  local path=$1 actual actual_receipt expected_receipt
  [[ -f $path && ! -L $path && -r $path ]] || fail "invalid closing payload: $path"
  actual=$(sed '/^<!-- jaiba-close-v1$/,$d' "$path" | hash)
  [[ $actual == "$BODY" ]] || fail "closing payload changed: $path"
  # The sentinel retains final newlines, and command status retains read
  # errors (process substitution would hide tail's failure from cmp).
  actual_receipt=$(tail -n 14 "$path" && printf '.')
  expected_receipt=$(emit_receipt; printf '.')
  [[ $actual_receipt == "$expected_receipt" ]] || fail "closing receipt changed: $path"
}
verify_payload "$SOURCE"
ARCHIVE=$LOG/$CLOSE.md
[[ $SOURCE == "$SUMMARY" || $SOURCE == "$ARCHIVE" ]] || fail 'log locator and close ID disagree'
EXISTING=0
if [[ -e $ARCHIVE || -L $ARCHIVE ]]; then
  verify_payload "$ARCHIVE"
  cmp -s "$SOURCE" "$ARCHIVE" || fail 'same close ID with different complete payload'
  EXISTING=1
fi
check_inventory() {
  local i current expected
  inventory
  if [[ -e $SUMMARY ]]; then verify_payload "$SUMMARY"; fi
  for i in "${!FILES[@]}"; do
    current=$(revision "${FILES[i]}") expected=${REVISIONS[i]}
    # Only previously verified cleanup may explain absent executive files.
    if [[ $current == absent && $EXISTING == 1 && ${FILES[i]} != .gitignore ]]; then continue; fi
    [[ $current == "$expected" ]] || fail "inventory conflict: ${FILES[i]}"
  done
}
check_inventory
check_tasks
if (( EXISTING == 0 )); then
  mkdir -p "$LOG"
  check_roots
  # No overwrite, including dangling symlinks. Interrupted copies stay visible
  # as conflicts, never authority for deleting work.
  (set -o noclobber; cat "$SOURCE" > "$ARCHIVE") || fail 'append failed; work retained'
fi
verify_payload "$ARCHIVE"
cmp -s "$SOURCE" "$ARCHIVE" || fail 'full log readback differs from prepared payload'
LOG_REV=$(hash < "$ARCHIVE")
printf 'verified log: %s\nrevision: %s\nclose: %s\nscope: %s\n' "$ARCHIVE" "$LOG_REV" "$CLOSE" "$SCOPE"
EXISTING=1
check_inventory
# No CAS claim: the caller's serialized discipline must remain in force.
# Recheck complete inventory and log before each deletion; stop on any error.
for name in plan.md tasks.md walkthrough.md PRD.md "$SLUG-summary.md"; do
  check_inventory
  verify_payload "$ARCHIVE"
  [[ $(hash < "$ARCHIVE") == "$LOG_REV" ]] || fail 'log revision changed'
  if [[ -e $WORK/$name ]]; then
    if [[ $name == "$SLUG-summary.md" ]]; then
      cmp -s "$SUMMARY" "$ARCHIVE" || fail 'summary changed before deletion'
    fi
    rm -- "$WORK/$name" || fail "partial cleanup: could not remove $name"
    [[ ! -e $WORK/$name && ! -L $WORK/$name ]] || fail "deletion not verified: $name"
    printf 'cleared: %s/%s\n' "$WORK" "$name"
  fi
done
check_inventory
verify_payload "$ARCHIVE"
[[ $(hash < "$ARCHIVE") == "$LOG_REV" ]] || fail 'log revision changed at completion'
printf 'archived: %s\nwork: cleared verified inventory; .gitignore retained if present\n' "$ARCHIVE"
