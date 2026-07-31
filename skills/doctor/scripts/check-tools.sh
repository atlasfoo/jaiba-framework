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

# mcp tool (prefix stripped) -> "source1, source2, ..."  (provenance).
# MCP servers aren't CLI tools on PATH — `command -v` can't verify them,
# so `requires: [mcp:foo]` entries are indexed here instead of NEEDS.
# A later diagnostic (doctor #3) verifies MCP reachability.
declare -A MCP_NEEDS

# source -> "tool1 tool2 ..." (inverse map)
declare -A DECLARED_TOOLS
declare -a SOURCES=()
declare -A SEEN_SOURCE

# Agent-layer bookkeeping. SOURCES mixes skills, subagents, hooks and the
# framework baseline into one list for the health rollup; the Agent Layers
# section needs them separated, plus the on-disk path of each SKILL.md so
# its frontmatter can be re-read for origin classification without
# re-walking the filesystem.
declare -a SKILL_LABELS=()
declare -a SUBAGENT_LABELS=()
declare -A SKILL_FILE

# Hooks unverified flag: set to 1 if jq is missing and hooks can't be scanned
HOOKS_UNVERIFIED=0  # consumed by report rendering

register_source() {  # register_source <source-label>
  local src="$1"
  if [ -z "${SEEN_SOURCE[$src]:-}" ]; then
    SEEN_SOURCE[$src]=1
    SOURCES+=("$src")
  fi
}

note() {  # note <tool> <source-label>
  local t="$1" src="$2"
  [ -z "$t" ] && return 0

  # Update inverse map. Store the original token (prefix included) so a
  # source's rollup entry can later distinguish `mcp:context7` from a
  # plain CLI tool by checking the prefix on each space-separated token.
  if [ -z "${DECLARED_TOOLS[$src]:-}" ]; then
    DECLARED_TOOLS[$src]="$t"
  elif [[ " ${DECLARED_TOOLS[$src]} " != *" $t "* ]]; then
    DECLARED_TOOLS[$src]+=" $t"
  fi

  register_source "$src"

  # mcp:* entries are indexed, not probed: `command -v` can't resolve an
  # MCP server, so route them into MCP_NEEDS (prefix stripped) instead
  # of the flat NEEDS map that feeds the CLI probe loop below.
  if [[ "$t" == mcp:* ]]; then
    local mt="${t#mcp:}"
    [ -z "$mt" ] && return 0
    if [ -z "${MCP_NEEDS[$mt]:-}" ]; then
      MCP_NEEDS[$mt]="$src"
    elif [[ ",${MCP_NEEDS[$mt]}," != *",$src,"* ]]; then
      MCP_NEEDS[$mt]="${MCP_NEEDS[$mt]}, $src"
    fi
    return 0
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

# Pull every item out of a SKILL.md's `tags:` YAML list. Same block shape
# as `requires_of`; a missing block simply yields nothing.
tags_of() {
  awk '
    /^tags:[[:space:]]*$/ { inblk=1; next }
    inblk && /^[[:space:]]*-[[:space:]]+/ {
      sub(/^[[:space:]]*-[[:space:]]+/, ""); sub(/[[:space:]]+$/, ""); print; next
    }
    inblk && /^[^[:space:]]/ { inblk=0 }
  ' "$1"
}

# framework vs external, decided by the `jaiba` tag alone. No tags block
# (or one without `jaiba`) means the skill is installed alongside JAIBA
# but not integrated with it — an external skill, reported as such.
origin_of() {  # origin_of <SKILL.md path>
  local tag
  while IFS= read -r tag; do
    if [ "$tag" = "jaiba" ]; then
      printf 'framework\n'
      return 0
    fi
  done < <(tags_of "$1")
  printf 'external\n'
}

# Render a source's requires tokens as a comma-separated backticked list,
# or the explicit "none declared" when the source declared nothing.
format_requires() {  # format_requires <source-label>
  local out="" t
  for t in ${DECLARED_TOOLS[$1]:-}; do
    if [ -z "$out" ]; then out="\`$t\`"; else out+=", \`$t\`"; fi
  done
  if [ -z "$out" ]; then printf 'none declared\n'; else printf '%s\n' "$out"; fi
}

# 1. Skills: <skills-dir>/**/SKILL.md  ->  labelled by skill folder name.
for SKILLS_DIR in "${SKILLS_DIRS[@]}"; do
  [ -d "$SKILLS_DIR" ] || continue
  while IFS= read -r -d '' f; do
    label="skill:$(basename "$(dirname "$f")")"
    register_source "$label"
    # First location wins when the same skill name exists in two dirs:
    # its requires merge into one source anyway, so one row is correct.
    if [ -z "${SKILL_FILE[$label]:-}" ]; then
      SKILL_FILE[$label]="$f"
      SKILL_LABELS+=("$label")
    fi
    while IFS= read -r t; do note "$t" "$label"; done < <(requires_of "$f")
  done < <(find -L "$SKILLS_DIR" -name SKILL.md -print0 2>/dev/null)
done

# 2. Subagents: <agent>/agents/*.md with a `requires:` block, for every
#    agent folder in play (project-local and/or global).
for AGENT_DIR in "${AGENT_DIRS[@]}"; do
  if [ -d "$AGENT_DIR/agents" ]; then
    while IFS= read -r -d '' f; do
      label="subagent:$(basename "$f" .md)"
      if [ -z "${SEEN_SOURCE[$label]:-}" ]; then
        SUBAGENT_LABELS+=("$label")
      fi
      register_source "$label"
      while IFS= read -r t; do note "$t" "$label"; done < <(requires_of "$f")
    done < <(find -L "$AGENT_DIR/agents" -name '*.md' -print0 2>/dev/null)
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
else
  HOOKS_UNVERIFIED=1
fi

# 4. Baseline, always.
for t in $BASELINE; do note "$t" "framework-baseline"; done

# A declared dependency name may differ from the command that probes it.
probe_cmd() { case "$1" in python) echo python3 ;; *) echo "$1" ;; esac; }

missing=0
total=0
rows=""
declare -A TOOL_PRESENT
readarray -t sorted_tools < <(printf '%s\n' "${!NEEDS[@]}" | sort)
for t in "${sorted_tools[@]}"; do
  [ -z "$t" ] && continue
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

# MCP dependencies get their own rows in the same table, appended after the
# CLI rows. They are deliberately kept out of `missing`/`total` (those stay
# CLI-only) and out of TOOL_PRESENT: an MCP server can't be resolved with
# `command -v`, so nothing here may let a downstream reader conclude the
# dependency is either satisfied or installable-missing. Verifying it is
# doctor diagnostic 3's job.
unverified=0
mcp_rows=""
# `${#MCP_NEEDS[@]}` alone would trip `set -u`: an associative array that was
# declared but never assigned still counts as unbound, and no skill/subagent
# declaring an `mcp:` entry is the common case. Probe for existence first.
if [ -n "${MCP_NEEDS[*]+set}" ] && [ "${#MCP_NEEDS[@]}" -gt 0 ]; then
  readarray -t sorted_mcp < <(printf '%s\n' "${!MCP_NEEDS[@]}" | sort)
  for mt in "${sorted_mcp[@]}"; do
    [ -z "$mt" ] && continue
    unverified=$((unverified + 1))
    mcp_rows+="| \`mcp:$mt\` | ❔ [UNVERIFIED] (MCP — verify via doctor diagnostic 3) | — | ${MCP_NEEDS[$mt]} |"$'\n'
  done
fi

# Build the health rollup row per source
rollup_rows=""
readarray -t sorted_sources < <(printf '%s\n' "${SOURCES[@]}" | sort -u)
for src in "${sorted_sources[@]}"; do
  [ -z "$src" ] && continue
  src_tools="${DECLARED_TOOLS[$src]:-}"
  [ -z "$src_tools" ] && continue

  src_missing=""
  src_mcp=""
  for t in $src_tools; do
    if [[ "$t" == mcp:* ]]; then
      # MCP entries can't be resolved via TOOL_PRESENT (command -v can't
      # check them) — route into a separate unverified bucket instead of
      # letting the ${TOOL_PRESENT[$t]:-0} fallback default them to missing.
      if [ -z "$src_mcp" ]; then
        src_mcp="\`$t\`"
      else
        src_mcp+=", \`$t\`"
      fi
    elif [ "${TOOL_PRESENT[$t]:-0}" -eq 0 ]; then
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

  if [ -n "$src_missing" ]; then
    verdict="❌ broken — missing: $src_missing"
    if [ -n "$src_mcp" ]; then
      verdict+="; unverified: $src_mcp"
    fi
  elif [ -n "$src_mcp" ]; then
    verdict="❔ unverified — MCP: $src_mcp (verify via doctor diagnostic 3)"
  else
    verdict="✅ satisfied"
  fi

  rollup_rows+="| $src | $formatted_tools | $verdict |"$'\n'
done

# The hooks scan only runs when jq is available (see the `command -v jq`
# branch above); when it's missing, note()/register_source("hook") never
# ran, so the main loop above never produces a `hook` row at all — the
# gap is invisible. Append one explicitly so the rollup never silently
# omits what it couldn't check.
if [ "$HOOKS_UNVERIFIED" -eq 1 ] && [ -z "${SEEN_SOURCE[hook]:-}" ]; then
  rollup_rows+="| hook | — | ❔ unverified — jq missing, hooks not scanned |"$'\n'
fi

# Build the Agent Layers rows: one per skill (with origin), one per
# subagent, plus a single line summarising what the hook scan produced.
skill_rows=""
if [ "${#SKILL_LABELS[@]}" -gt 0 ]; then
  while IFS= read -r label; do
    [ -z "$label" ] && continue
    skill_rows+="| \`${label#skill:}\` | $(origin_of "${SKILL_FILE[$label]}") | $(format_requires "$label") |"$'\n'
  done < <(printf '%s\n' "${SKILL_LABELS[@]}" | sort -u)
fi

subagent_rows=""
if [ "${#SUBAGENT_LABELS[@]}" -gt 0 ]; then
  while IFS= read -r label; do
    [ -z "$label" ] && continue
    subagent_rows+="| \`${label#subagent:}\` | $(format_requires "$label") |"$'\n'
  done < <(printf '%s\n' "${SUBAGENT_LABELS[@]}" | sort -u)
fi

# Hook needs are only knowable when jq was available to parse settings*.json.
# Without it the scan never ran, so report that rather than a count of zero.
if [ "$HOOKS_UNVERIFIED" -eq 1 ]; then
  hooks_line="⚠️ Not scanned — \`jq\` is missing, so hook commands in \`settings*.json\` could not be parsed. Hook-derived tool needs are unknown."
else
  hook_tools="${DECLARED_TOOLS[hook]:-}"
  hook_count=0
  for t in $hook_tools; do hook_count=$((hook_count + 1)); done
  if [ "$hook_count" -eq 0 ]; then
    hooks_line="Scanned — no tool needs derived from hook commands."
  else
    hooks_line="Scanned — $hook_count tool need(s) derived from hook commands: $(format_requires hook)."
  fi
fi

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
  echo "- **Unverified (MCP):** $unverified"
  echo
  echo "## Probed Tools"
  echo
  echo "| Tool | State | Path | Needed by |"
  echo "|---|---|---|---|"
  printf '%s' "$rows"
  printf '%s' "$mcp_rows"
  if [ "$unverified" -gt 0 ]; then
    echo
    echo "> ❔ $unverified MCP dependency/dependencies can't be probed from the"
    echo "> shell — \`command -v\` only resolves CLI tools on PATH. They are"
    echo "> neither counted as present nor as missing here; doctor diagnostic 3"
    echo "> verifies MCP server reachability."
  fi
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
  echo
  echo "## Agent Layers"
  echo
  echo "> What this machine actually has installed, layer by layer. **Origin**"
  echo "> is read from each skill's \`tags:\` block — \`framework\` when the"
  echo "> \`jaiba\` tag is present, \`external\` otherwise (an external skill"
  echo "> may work fine; it just isn't part of the framework's own surface)."
  echo
  echo "### Skills"
  echo
  if [ -n "$skill_rows" ]; then
    echo "| Skill | Origin | Requires |"
    echo "|---|---|---|"
    printf '%s' "$skill_rows"
  else
    echo "_No skills found under the scanned skills dir(s)._"
  fi
  echo
  echo "### Subagents"
  echo
  if [ -n "$subagent_rows" ]; then
    echo "| Subagent | Requires |"
    echo "|---|---|"
    printf '%s' "$subagent_rows"
  else
    echo "_No subagents found under the scanned agent folder(s)._"
  fi
  echo
  echo "### Hooks"
  echo
  echo "$hooks_line"
} > "$OUT"

echo "wrote $OUT — $missing missing of $total"
exit 0
