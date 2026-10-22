#!/bin/sh
# Gravitas update check for Antigravity on macOS and Linux (SessionStart hook; runs in the plugin folder).
#
# At most once a day it asks GitHub for the latest Gravitas release: one request to
# api.github.com, carrying only a User-Agent with this plugin's version. The answer is
# cached in ~/.gemini/gravitas/update-check.json. When a newer release is out, it prints
# a system message that has the agent say so once, with the step to update; otherwise it
# prints {}. Any failure prints {} and exits 0, so a session never waits on this.
#
# Turn it off: create the file ~/.gemini/gravitas/update-check-off, or set the
# environment variable GRAVITAS_UPDATE_CHECK=off.
none='{}'
dir="$HOME/.gemini/gravitas"
file="$dir/update-check.json"
api='https://api.github.com/repos/Emily2040/gravitas/releases/latest'
page_default='https://github.com/Emily2040/gravitas/releases/latest'

if [ "$GRAVITAS_UPDATE_CHECK" = off ] || [ -e "$dir/update-check-off" ]; then printf '%s\n' "$none"; exit 0; fi

# the first "key": "value" pair in a JSON text, with key $1
field() { tr -d '\n\r' | sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\{0,1\}\([^\",}]*\)\"\{0,1\}.*/\1/p" | head -n 1; }
# 0 (true) when version $1 is later than version $2, both x.y.z
newer() {
  awk -v a="$1" -v b="$2" 'BEGIN { split(a, x, "."); split(b, y, ".")
    for (i = 1; i <= 3; i++) { if (x[i] + 0 > y[i] + 0) exit 0; if (x[i] + 0 < y[i] + 0) exit 1 } exit 1 }'
}
is_version() { printf '%s' "$1" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; }

current=$(field version < plugin.json 2>/dev/null)
is_version "$current" || { printf '%s\n' "$none"; exit 0; }
now=$(date +%s)
checked=''; latest=''; url=''
if [ -f "$file" ]; then
  checked=$(field checkedAt < "$file"); latest=$(field latest < "$file"); url=$(field url < "$file")
fi
case "$checked" in ''|*[!0-9]*) checked='' ;; esac
if [ -z "$checked" ] || [ "$now" -lt "$checked" ] || [ $((now - checked)) -ge 86400 ]; then
  body=$(curl -fsS -m 4 -H 'Accept: application/vnd.github+json' -H "User-Agent: gravitas-antigravity/$current" "$api" 2>/dev/null)
  if [ -n "$body" ]; then
    tag=$(printf '%s' "$body" | field tag_name | sed 's/^v//')
    if is_version "$tag"; then
      latest=$tag
      url=$(printf '%s' "$body" | field html_url)
      case "$url" in https://github.com/*) ;; *) url=$page_default ;; esac
    fi
  fi
  mkdir -p "$dir" 2>/dev/null && printf '{"checkedAt":%s,"latest":"%s","url":"%s"}\n' "$now" "$latest" "$url" > "$file" 2>/dev/null
fi
if ! is_version "$latest" || ! newer "$latest" "$current"; then printf '%s\n' "$none"; exit 0; fi
[ -n "$url" ] || url=$page_default
text="Gravitas update: version $latest is out; this computer has $current ($url). In your first reply in this conversation, after everything else, add one short line in the user's language saying so, with how to update: download Gravitas.zip from that page, unzip it, and double-click Install Gravitas (Mac).command on a Mac or run Install Gravitas (Linux).sh on Linux. Say it once: not in later replies, and not if one of your replies above already said it. Do not change or shorten the answer for it, and do not run the update yourself."
printf '{"injectSteps":[{"systemMessage":{"systemMessage":"%s"}}]}\n' "$text"
exit 0
