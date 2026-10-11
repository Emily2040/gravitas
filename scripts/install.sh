#!/usr/bin/env bash
# Install Gravitas as an Antigravity plugin. Language: en (default), zh-CN, ja or ko.
# The Second Opinion is off by default: --review adds it, --no-review leaves it out. Every argument is passed to install.py unchanged.
#   bash scripts/install.sh [en|zh-CN|ja|ko] [--review|--no-review]
#   bash scripts/install.sh --uninstall
set -euo pipefail
cd "$(dirname "$0")/.."
# The first interpreter that actually runs: on Windows, python3 can be the Microsoft Store stub.
PY=""
for c in python3 python py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
    PY="$c"
    break
  fi
done
[ -n "$PY" ] || { echo "Python 3.8 or later is required"; exit 1; }
# Bash terminals read UTF-8, so a home folder with a non-ASCII name prints as it is.
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"
exec "$PY" scripts/install.py "$@"
