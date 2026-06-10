#!/usr/bin/env bash
#
# JAIBA scaffold — local toolchain probe.
#
# Derives the set of CLI tools the installed JAIBA skills need from each
# skill's `requires:` frontmatter, unions it with a small framework
# baseline, checks every tool against the local machine, and writes the
# result to `.ai/tools-state.md`. Warn-and-continue by design: a missing
# tool never aborts the scaffold — it is recorded so AGENTS.md §6 can
# surface it every session.
#
# Usage:
#   check-tools.sh <installed-skills-dir> [<project-root>]
#
#   <installed-skills-dir>  where scaffold installed the JAIBA skills
#                           (e.g. .claude/skills or .agents/skills).
#   <project-root>          defaults to the current directory.
#
# Exit code is always 0 (the count of missing tools is reported in the
# output file and on stdout, not via exit status).

set -uo pipefail

SKILLS_DIR="${1:?usage: check-tools.sh <installed-skills-dir> [project-root]}"
ROOT="${2:-$PWD}"
OUT="$ROOT/.ai/tools-state.md"

# Framework baseline — tools the JAIBA skills assume regardless of any
# one skill's declaration. `bash` runs the bundled *.sh scripts, `git`
# is the source of truth for every workflow, and `rg`/`curl` are the
# search/fetch tools the skills reach for. Everything else is derived,
# so the probe only flags tools the project's skills actually need.
BASELINE="git bash rg curl"

# Pull every item out of each SKILL.md `requires:` YAML list.
derive_requires() {
  [ -d "$SKILLS_DIR" ] || return 0
  find "$SKILLS_DIR" -name SKILL.md -print0 2>/dev/null \
  | while IFS= read -r -d '' f; do
      awk '
        /^requires:[[:space:]]*$/ { inblk=1; next }
        inblk && /^[[:space:]]*-[[:space:]]+/ {
          sub(/^[[:space:]]*-[[:space:]]+/, "")
          sub(/[[:space:]]+$/, "")
          print
          next
        }
        inblk && /^[^[:space:]]/ { inblk=0 }
      ' "$f"
    done
}

# A declared dependency name may differ from the command that probes it.
probe_cmd() {
  case "$1" in
    python) echo "python3" ;;
    *)      echo "$1" ;;
  esac
}

tools="$( { printf '%s\n' $BASELINE; derive_requires; } | grep -v '^[[:space:]]*$' | sort -u )"

missing=0
rows=""
for t in $tools; do
  cmd="$(probe_cmd "$t")"
  if path="$(command -v "$cmd" 2>/dev/null)"; then
    rows+="| \`$t\` | ✅ present | \`$path\` |"$'\n'
  else
    rows+="| \`$t\` | ❌ **missing** | — |"$'\n'
    missing=$((missing + 1))
  fi
done

mkdir -p "$ROOT/.ai"
{
  echo "# Toolchain State"
  echo
  echo "> Local CLI toolchain probed by \`jaiba-scaffold\`. **Gitignored** —"
  echo "> this records what is installed on *this machine*, not a project"
  echo "> fact. Regenerate by re-running the scaffold tool check."
  echo
  echo "- **Probed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- **Skills scanned:** \`$SKILLS_DIR\`"
  echo "- **Missing:** $missing"
  echo
  echo "| Tool | State | Path |"
  echo "|---|---|---|"
  printf '%s' "$rows"
  if [ "$missing" -gt 0 ]; then
    echo
    echo "> ⚠️ $missing tool(s) missing. Skills that depend on them will fail"
    echo "> mid-run — AGENTS.md §6 warns about this each session until resolved."
  fi
} > "$OUT"

echo "wrote $OUT — $missing missing of $(printf '%s\n' $tools | grep -c .)"
exit 0
