#!/usr/bin/env bash
# Adopts skills into CDF from common install locations.
#
# Primary workflow (preferred):
#   npx skills add <url> --skill <name> --yes --copy
#   # Installs directly to skills/ — no adopt needed.
#
# This script handles two cleanup scenarios:
#   1. Skills installed globally to ~/.claude/skills/ (via -g flag or manual copy)
#   2. Duplicate copies left in .claude/skills/ after --copy install
#
# Usage: ./scripts/adopt-skills.sh

set -euo pipefail

CDF_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$CDF_DIR/skills"

adopted=0
cleaned=0

# 1. Adopt from ~/.claude/skills/ (global installs)
GLOBAL_DIR="$HOME/.claude/skills"
if [ -d "$GLOBAL_DIR" ]; then
  for skill_dir in "$GLOBAL_DIR"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    [[ "$skill_name" == .* ]] && continue

    if [ -d "$SKILLS_DIR/$skill_name" ]; then
      echo "skip: $skill_name (already in CDF)"
    else
      mv "$skill_dir" "$SKILLS_DIR/"
      echo "adopted: $skill_name (from ~/.claude/skills/)"
      adopted=$((adopted + 1))
    fi
  done
fi

# 2. Clean duplicates from .claude/skills/ (left by --copy installs)
LOCAL_CLONE="$CDF_DIR/.claude/skills"
if [ -d "$LOCAL_CLONE" ]; then
  for skill_dir in "$LOCAL_CLONE"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    [[ "$skill_name" == .* ]] && continue

    if [ -d "$SKILLS_DIR/$skill_name" ]; then
      rm -rf "$skill_dir"
      echo "cleaned: $skill_name (duplicate in .claude/skills/)"
      cleaned=$((cleaned + 1))
    fi
  done
fi

# 3. Clean .agents/ cache if present
if [ -d "$CDF_DIR/.agents" ]; then
  rm -rf "$CDF_DIR/.agents"
  echo "cleaned: .agents/ cache"
fi

if [ "$adopted" -eq 0 ] && [ "$cleaned" -eq 0 ]; then
  echo "Nothing to adopt or clean up."
else
  [ "$adopted" -gt 0 ] && echo "Adopted $adopted skill(s)."
  [ "$cleaned" -gt 0 ] && echo "Cleaned $cleaned duplicate(s)."
  echo "Run 'python3 scripts/health-check.py' to verify."
fi
