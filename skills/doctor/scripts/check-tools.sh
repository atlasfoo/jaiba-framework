#!/usr/bin/env bash
#
# JAIBA doctor — local toolchain probe (maintenance check).
#
# The diagnostic toolchain probe. Where scaffold used to probe once at
# install time, doctor RE-probes during a health check and widens the net: it derives
# the required CLI tools from installed skills, from subagent
# definitions, AND from hook command lines, tracks WHICH of them needs
# each tool (provenance), checks every tool against this machine, and
# rewrites `.atl/tool-layout.md`. Warn-and-record by design — a missing
# tool is reported, never fatal (AGENTS.md §6 keeps surfacing it).
#
# Refreshing tool-layout.md is the ONLY write doctor performs; the file
# is machine state, gitignored, not project memory.
#
# Usage:
#   check-tools.sh <installed-skills-dir>[:<installed-skills-dir>...] [<project-root>]
#
#   <installed-skills-dir>  where JAIBA skills are installed (e.g.
#                           .claude/skills, .agents/skills, or a global
#                           dir like ~/.claude/skills). Pass several,
#                           separated by ':', if the project's skillset
#                           is split across project-local and global
#                           locations (per jaiba-scaffold step 4). Each
#                           directory's parent is treated as an agent
#                           folder, so subagents (agents/*.md) and hook
#                           configs (settings*.json) next to each are
#                           scanned too.
#   <project-root>          defaults to the current directory.
#
# Exit code is always 0 (the missing count is reported in the output
# file and on stdout, not via exit status).

set -uo pipefail

SKILLS_DIRS_RAW="${1:?usage: check-tools.sh <installed-skills-dir>[:<installed-skills-dir>...] [project-root]}"
ROOT="${2:-$PWD}"
OUT="$ROOT/.atl/tool-layout.md"
IFS=':' read -r -a SKILLS_DIRS <<< "$SKILLS_DIRS_RAW"

# Detect host shell flavor to distinguish git bash from WSL in Windows
SHELL_FLAVOR="native"
if [ -n "${MSYSTEM:-}" ]; then
  case "$MSYSTEM" in
    MINGW*|MSYS*) SHELL_FLAVOR="git-bash" ;;
  esac
elif [ -f /proc/version ] && grep -qE "microsoft|WSL" /proc/version 2>/dev/null; then
  SHELL_FLAVOR="wsl"
elif [ -n "${WSL_DISTRO_NAME:-}" ]; then
  SHELL_FLAVOR="wsl"
fi

# Each skills dir's parent is an agent folder (subagents/hooks live
# alongside it). De-duplicate in case two skill dirs share a parent.
declare -A SEEN_AGENT_DIR
AGENT_DIRS=()
for d in "${SKILLS_DIRS[@]}"; do
  ad="$(dirname "$d")"
  if [ -z "${SEEN_AGENT_DIR[$ad]:-}" ]; then
    SEEN_AGENT_DIR[$ad]=1
    AGENT_DIRS+=("$ad")
  fi
done

# Framework baseline — tools the JAIBA skills assume regardless of any
# one declaration. Same set scaffold uses, so the two probes agree.
BASELINE="git bash rg curl"

# tool -> "source1, source2, ..."  (provenance: who needs the tool)
declare -A NEEDS

# source -> "tool1 tool2 ..." (inverse map)
declare -A DECLARED_TOOLS
declare -a SOURCES=()
declare -A SEEN_SOURCE

note() {  # note <tool> <source-label>
  local t="$1" src="$2"
  [ -z "$t" ] && return 0

  # Update inverse map
  if [ -z "${DECLARED_TOOLS[$src]:-}" ]; then
    DECLARED_TOOLS[$src]="$t"
  elif [[ " ${DECLARED_TOOLS[$src]} " != *" $t "* ]]; then
    DECLARED_TOOLS[$src]+=" $t"
  fi

  if [ -z "${SEEN_SOURCE[$src]:-}" ]; then
    SEEN_SOURCE[$src]=1
    SOURCES+=("$src")
  fi

  # Update flat tool needs map
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
for SKILLS_DIR in "${SKILLS_DIRS[@]}"; do
  [ -d "$SKILLS_DIR" ] || continue
  while IFS= read -r -d '' f; do
    label="skill:$(basename "$(dirname "$f")")"
    while IFS= read -r t; do note "$t" "$label"; done < <(requires_of "$f")
  done < <(find "$SKILLS_DIR" -name SKILL.md -print0 2>/dev/null)
done

# 2. Subagents: <agent>/agents/*.md with a `requires:` block, for every
#    agent folder in play (project-local and/or global).
for AGENT_DIR in "${AGENT_DIRS[@]}"; do
  if [ -d "$AGENT_DIR/agents" ]; then
    while IFS= read -r -d '' f; do
      label="subagent:$(basename "$f" .md)"
      while IFS= read -r t; do note "$t" "$label"; done < <(requires_of "$f")
    done < <(find "$AGENT_DIR/agents" -name '*.md' -print0 2>/dev/null)
  fi
done

# 3. Hooks: leading executable of every hook command in settings*.json,
#    for every agent folder in play.
#    Best-effort and jq-gated — hooks can run arbitrary shell, so we only
#    claim the command's first token (the program it invokes).
if command -v jq >/dev/null 2>&1; then
  for AGENT_DIR in "${AGENT_DIRS[@]}"; do
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
  done
fi

# 4. Baseline, always.
for t in $BASELINE; do note "$t" "framework-baseline"; done

# A declared dependency name may differ from the command that probes it.
probe_cmd() { case "$1" in python) echo python3 ;; *) echo "$1" ;; esac; }

missing=0
total=0
rows=""
declare -A TOOL_PRESENT
for t in $(printf '%s\n' "${!NEEDS[@]}" | sort); do
  total=$((total + 1))
  cmd="$(probe_cmd "$t")"
  if path="$(command -v "$cmd" 2>/dev/null)"; then
    TOOL_PRESENT[$t]=1
    state="✅ present"
    if [ "$t" = "bash" ]; then
      state="✅ present ($SHELL_FLAVOR)"
    fi
    rows+="| \`$t\` | $state | \`$path\` | ${NEEDS[$t]} |"$'\n'
  else
    TOOL_PRESENT[$t]=0
    rows+="| \`$t\` | ❌ **missing** | — | ${NEEDS[$t]} |"$'\n'
    missing=$((missing + 1))
  fi
done

# Build the health rollup row per source
rollup_rows=""
for src in $(printf '%s\n' "${SOURCES[@]}" | sort -u); do
  src_tools="${DECLARED_TOOLS[$src]:-}"
  [ -z "$src_tools" ] && continue

  src_missing=""
  for t in $src_tools; do
    if [ "${TOOL_PRESENT[$t]:-0}" -eq 0 ]; then
      if [ -z "$src_missing" ]; then
        src_missing="\`$t\`"
      else
        src_missing+=", \`$t\`"
      fi
    fi
  done

  formatted_tools=""
  for t in $src_tools; do
    if [ -z "$formatted_tools" ]; then
      formatted_tools="\`$t\`"
    else
      formatted_tools+=", \`$t\`"
    fi
  done

  if [ -z "$src_missing" ]; then
    verdict="✅ satisfied"
  else
    verdict="❌ broken — missing: $src_missing"
  fi

  rollup_rows+="| $src | $formatted_tools | $verdict |"$'\n'
done

mkdir -p "$ROOT/.atl"
{
  echo "# Toolchain Layout"
  echo
  echo "> Local CLI toolchain re-probed by \`jaiba-doctor\` inside \`.atl/\`. **Gitignored** —"
  echo "> this records what is installed on *this machine*, not a project"
  echo "> fact. Regenerate by re-running \`jaiba-doctor\` (or the scaffold"
  echo "> tool check)."
  echo
  echo "- **Probed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- **Shell host:** $SHELL_FLAVOR"
  echo "- **Skills scanned:** $(printf '\`%s\` ' "${SKILLS_DIRS[@]}")"
  echo "- **Agent folder(s):** $(printf '\`%s\` ' "${AGENT_DIRS[@]}")"
  echo "- **Missing:** $missing of $total"
  echo
  echo "## Probed Tools"
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
  echo
  echo "## Skill-Specific Health Rollup"
  echo
  echo "| Source | Required Tools | Health Verdict |"
  echo "|---|---|---|"
  printf '%s' "$rollup_rows"
} > "$OUT"

echo "wrote $OUT — $missing missing of $total"
exit 0
