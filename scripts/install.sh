#!/usr/bin/env bash
# Install the skill into Antigravity's global skills directory.
# Workspace .agents/ directories are never scanned, so global is the only option.
#
#   bash scripts/install.sh            # English (default)
#   bash scripts/install.sh zh-CN      # 简体中文
#   bash scripts/install.sh ja         # 日本語
#   bash scripts/install.sh ko         # 한국어
#
# Only one language can be installed at a time, because every version uses the
# same skill name. Re-run with a different language to switch.
set -euo pipefail

LANG_CODE="${1:-en}"
case "$LANG_CODE" in
  en)          SRC="skill" ;;
  zh|zh-CN)    SRC="locales/zh-CN" ;;
  ja)          SRC="locales/ja" ;;
  ko)          SRC="locales/ko" ;;
  *) echo "unknown language: $LANG_CODE (use en, zh-CN, ja or ko)"; exit 2 ;;
esac

[ -f "$SRC/SKILL.md" ] || { echo "missing $SRC/SKILL.md"; exit 1; }

NAME="$(grep -m1 '^name:' "$SRC/SKILL.md" | sed 's/^name:[[:space:]]*//')"
DEST="$HOME/.gemini/config/skills/$NAME"

rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"

echo "installed $LANG_CODE to $DEST"
python scripts/check_skills.py
echo "Restart Antigravity to pick up the change."
