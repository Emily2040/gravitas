#!/usr/bin/env bash
# Install the skill into Antigravity's global skills directory.
# Workspace .agents/ directories are never scanned, so global is the only option.
set -euo pipefail
NAME="$(grep -m1 '^name:' skill/SKILL.md | sed 's/^name:[[:space:]]*//')"
DEST="$HOME/.gemini/config/skills/$NAME"
mkdir -p "$DEST"
cp -r skill/. "$DEST/"
echo "installed to $DEST"
python scripts/check_skills.py
