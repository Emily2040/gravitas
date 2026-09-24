#!/usr/bin/env bash
# Install Gravitas as an Antigravity plugin. Language: en (default), zh-CN, ja or ko.
#   bash scripts/install.sh [en|zh-CN|ja|ko]
#   bash scripts/install.sh --uninstall
set -euo pipefail
cd "$(dirname "$0")/.."
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || { echo "Python 3.8 or later is required"; exit 1; }
exec "$PY" scripts/install.py "$@"
