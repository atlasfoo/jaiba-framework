#!/usr/bin/env bash
#
# JAIBA doctor — local toolchain probe (maintenance re-check).
#
# The diagnostic sibling of scaffold's check-tools.sh. Where scaffold
# probes once at install time from the installed skills' `requires:`,
# doctor RE-probes during a health check and widens the net: it derives
# the required CLI tools from installed skills, from subagent
# definitions, AND from hook command lines, tracks WHICH of them needs
# each tool (provenance), checks every tool against this machine, and
# rewrites `.ai/tools-state.md`. Warn-and-record by design — a missing
# tool is reported, never fatal (AGENTS.md §6 keeps surfacing it).
#
# Refreshing tools-state.md is the ONLY write doctor performs; the file
# is machine state, gitignored, not project memory.
#
# Usage:
#   check-tools.sh <installed-skills-dir> [<project-root>]
#
#   <installed-skills-dir>  where the JAIBA skills are installed
#                           (e.g. .claude/skills or .agents/skills).
#                           Its parent is treated as the agent folder,
#                           so subagents (agents/*.md) and hook configs
#                           (settings*.json) next to it are scanned too.
#   <project-root>          defaults to the current directory.
#
# Exit code is always 0 (the missing count is reported in the output
# file and on stdout, not via exit status).

set -uo pipefail

SKILLS_DIR="${1:?usage: check-tools.sh <installed-skills-dir> [project-root]}"
ROOT="${2:-$PWD}"
OUT="$ROOT/.ai/tools-state.md"
AGENT_DIR="$(dirname "$SKILLS_DIR")"

# Framework baseline — tools the JAIBA skills assume regardless of any
# one declaration. Same set scaffold uses, so the two probes agree.
BASELINE="git bash rg curl"

# tool -> "source1, source2, ..."  (provenance: who needs the tool)
declare -A NEEDS

note() {  # note <tool> <source-label>
  local t="$1" src="$2"
  [ -z "$t" ] && return 0
  if [ -z "${NEEDS[$t]:-}" ]; then
    NEEDS[$t]="$src"
  elif [[ ",${NEEDS[$t]}," != *",$src,"* ]]; then
    NEEDS[$t]="${NEEDS[$t]}, $src"
  fi
}

# Pull every item out of a markdown file's `requires:` YAML list.
# Works for SKILL.md and for subagent definition files alike.
requires_of() {
  awk '
    /^requires:[[:space:]]*$/ { inblk=1; next }
    inblk && /^[[:space:]]*-[[:space:]]+/ {
      sub(/^[[:space:]]*-[[:space:]]+/, ""); sub(/[[:space:]]+$/, ""); print; next
    }
    inblk && /^[^[:space:]]/ { inblk=0 }
  ' "$1"
}

# 1. Skills: <skills-dir>/**/SKILL.md  ->  labelled by skill folder name.
if [ -d "$SKILLS_DIR" ]; then
  while IFS= read -r -d '' f; do
    label="skill:$(basename "$(dirname "$f")")"
    while IFS= read -r t; do note "$t" "$label"; done < <(requires_of "$f")
  done < <(find "$SKILLS_DIR" -name SKILL.md -print0 2>/dev/null)
fi

# 2. Subagents: <agent>/agents/*.md with a `requires:` block.
if [ -d "$AGENT_DIR/agents" ]; then
  while IFS= read -r -d '' f; do
    label="subagent:$(basename "$f" .md)"
    while IFS= read -r t; do note "$t" "$label"; done < <(requires_of "$f")
  done < <(find "$AGENT_DIR/agents" -name '*.md' -print0 2>/dev/null)
fi

# 3. Hooks: leading executable of every hook command in settings*.json.
#    Best-effort and jq-gated — hooks can run arbitrary shell, so we only
#    claim the command's first token (the program it invokes).
if command -v jq >/dev/null 2>&1; then
  for cfg in "$AGENT_DIR"/settings.json "$AGENT_DIR"/settings.local.json; do
    [ -f "$cfg" ] || continue
    while IFS= read -r cmd; do
      [ -z "$cmd" ] && continue
      exe="$(printf '%s\n' "$cmd" | awk '{print $1}')"
      exe="$(basename "$exe")"
      # Skip empties and bare shell wrappers (`bash -c "…"`): the wrapper
      # isn't the dependency, and bash is already in the baseline.
      case "$exe" in ""|sh|bash|zsh|env) continue ;; esac
      note "$exe" "hook"
    done < <(jq -r '.hooks // {} | .. | .command? // empty' "$cfg" 2>/dev/null)
  done
fi

# 4. Baseline, always.
for t in $BASELINE; do note "$t" "framework-baseline"; done

# A declared dependency name may differ from the command that probes it.
probe_cmd() { case "$1" in python) echo python3 ;; *) echo "$1" ;; esac; }

missing=0
total=0
rows=""
for t in $(printf '%s\n' "${!NEEDS[@]}" | sort); do
  total=$((total + 1))
  cmd="$(probe_cmd "$t")"
  if path="$(command -v "$cmd" 2>/dev/null)"; then
    rows+="| \`$t\` | ✅ present | \`$path\` | ${NEEDS[$t]} |"$'\n'
  else
    rows+="| \`$t\` | ❌ **missing** | — | ${NEEDS[$t]} |"$'\n'
    missing=$((missing + 1))
  fi
done

mkdir -p "$ROOT/.ai"
{
  echo "# Toolchain State"
  echo
  echo "> Local CLI toolchain re-probed by \`jaiba-doctor\`. **Gitignored** —"
  echo "> this records what is installed on *this machine*, not a project"
  echo "> fact. Regenerate by re-running \`jaiba-doctor\` (or the scaffold"
  echo "> tool check)."
  echo
  echo "- **Probed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- **Skills scanned:** \`$SKILLS_DIR\`"
  echo "- **Agent folder:** \`$AGENT_DIR\`"
  echo "- **Missing:** $missing of $total"
  echo
  echo "| Tool | State | Path | Needed by |"
  echo "|---|---|---|---|"
  printf '%s' "$rows"
  if [ "$missing" -gt 0 ]; then
    echo
    echo "> ⚠️ $missing tool(s) missing. The skills/subagents/hooks that"
    echo "> depend on them will fail mid-run — AGENTS.md §6 warns about this"
    echo "> each session until resolved."
  fi
} > "$OUT"

echo "wrote $OUT — $missing missing of $total"
exit 0
