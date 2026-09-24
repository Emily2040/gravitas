#!/usr/bin/env python3
"""Check an answer's evidence labels against what the conversation actually did.

Every `read (...)`, `observed (...)` and `executed (...)` label in the answer is
compared with the transcript of the conversation that wrote it:

  read      the URL was opened with read_url_content, or the path with view_file,
            and the quoted text appears in what was fetched
  observed  the artifact path was opened with view_file
  executed  the command appears in a run_command call

A URL that appears only inside a search_web summary is reported as SEARCH-ONLY:
the page itself was never opened. Standard library only, Python 3.8 or later.

    python provenance_check.py ANSWER.md --latest
    python provenance_check.py ANSWER.md --conversation <id>
    python provenance_check.py ANSWER.md --transcript <path to transcript_full.jsonl>

Exit status: 0 when every label holds, 1 when any does not, 2 on bad input.
"""
import argparse
import glob
import html
import json
import os
import re
import sys
from urllib.parse import unquote

ROOTS = [os.path.join(os.path.expanduser("~"), ".gemini", d, "brain")
         for d in ("antigravity-cli", "antigravity", "antigravity-ide")]
LABEL = re.compile(r"\b(observed|executed|read)`?\*{0,2}\s*\(")
URL = re.compile(r"https?://[^\s\"'`)<>,]+")
PATH = re.compile(r"(?:\b[A-Za-z]:[\\/]|file:///)[^\s\"'`,;)]+")
SCRIPT = re.compile(r"[\w.-]+\.(?:py|js|mjs|ts|sh|ps1|rb|go)\b")
QUOTE = re.compile(r"[\"“]([^\"”]{12,})[\"”]")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def find_transcript(a):
    if a.transcript:
        return a.transcript
    pattern = "*/.system_generated/logs/transcript_full.jsonl"
    found = [p for r in ROOTS for p in glob.glob(os.path.join(r, pattern))]
    if a.conversation:
        found = [p for p in found if a.conversation in p]
    if not found:
        fail("no transcript found")
    return max(found, key=os.path.getmtime)


def label_spans(text):
    """Yield (tier, inside) for each label, matching parentheses so nested ones survive."""
    for m in LABEL.finditer(text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            i += 1
        yield m.group(1), text[m.end():i - 1]


def norm_url(u):
    return unquote(u).rstrip("/.").split("#")[0].lower()


def norm_path(p):
    p = unquote(p.replace("file:///", ""))
    return p.replace("\\", "/").rstrip("/.").lower()


def squash(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or ""))
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t).strip().lower()


def load(transcript):
    rows = [json.loads(l) for l in open(transcript, encoding="utf-8") if l.strip()]
    urls, paths, commands, search_text, fetched = set(), set(), [], [], []
    for r in rows:
        for c in r.get("tool_calls") or []:
            args = c.get("args") or {}
            name = c.get("name")
            if name == "read_url_content":
                urls.add(norm_url(args.get("Url") or args.get("url") or ""))
            elif name == "view_file":
                paths.add(norm_path(args.get("AbsolutePath") or ""))
            elif name == "run_command":
                commands.append(squash(args.get("CommandLine") or ""))
        content = r.get("content") or ""
        if r.get("type") == "PLANNER_RESPONSE":
            continue
        if "search for" in content[:400] or "returned the following summary" in content[:600]:
            search_text.append(content)
        fetched.append(content)
    steps = os.path.join(os.path.dirname(os.path.dirname(transcript)), "steps")
    for p in glob.glob(os.path.join(steps, "*", "content.md")):
        fetched.append(open(p, encoding="utf-8", errors="replace").read())
    return urls, paths, commands, squash(" ".join(search_text)), squash(" ".join(fetched))


def shingles(text, n=4):
    text = re.sub(r"(?<![\d.])\d{1,2}\.\s", " ", text or "")  # list numbering such as "7. "
    w = re.findall(r"[a-z0-9]+", squash(text))
    return {" ".join(w[i:i + n]) for i in range(max(len(w) - n + 1, 0))}


def tokens(text):
    return set(re.findall(r"[a-z_][a-z0-9_]{2,}|\d+(?:\.\d+)?", text.lower()))


def check(answer, transcript):
    urls, paths, commands, searched, fetched = load(transcript)
    fetched_grams = shingles(fetched)
    results = []
    for tier, inside in label_spans(answer):
        ok, notes = True, []
        found_urls = [norm_url(u) for u in URL.findall(inside)]
        found_paths = [norm_path(p) for p in PATH.findall(URL.sub(" ", inside))]
        if tier in ("read", "observed"):
            if not found_urls and not found_paths:
                ok = False
                notes.append("NO LOCATOR: the label names no URL or path")
            for u in found_urls:
                if u in urls or any(u.startswith(x) or x.startswith(u) for x in urls if x):
                    continue
                ok = False
                notes.append(("SEARCH-ONLY: %s appears only in a search summary" if u in searched
                              else "NOT OPENED: %s") % u)
            for p in found_paths:
                if p not in paths and not any(p.endswith(x) or x.endswith(p) for x in paths if x):
                    ok = False
                    notes.append("NOT OPENED: %s" % p)
            if tier == "read":
                for q in QUOTE.findall(inside):
                    # Compare runs of four words, so changed punctuation, quote marks or list
                    # numbering do not count as fabrication, and an ellipsis can join passages.
                    grams = shingles(q)
                    if not grams:
                        continue
                    share = len(grams & fetched_grams) / len(grams)
                    if share < 0.6:
                        ok = False
                        notes.append("QUOTE NOT FOUND in anything fetched (%.0f%% of it matches): \"%s\""
                                     % (share * 100, q[:70]))
                    elif share < 0.9 and ok:
                        ok = None
                        notes.append("QUOTE REFORMATTED or partly paraphrased (%.0f%% of it matches): \"%s\""
                                     % (share * 100, q[:70]))
        elif tier == "executed":
            cmd = re.split(r"\s*(?:->|=>|→)\s*", inside, maxsplit=1)[0].strip().strip("`")
            flat = re.sub(r"\s+", "", cmd.lower())
            scripts = [s.lower() for s in SCRIPT.findall(cmd)]
            if scripts and all(any(s in c for c in commands) for s in scripts):
                pass
            elif flat and any(flat in re.sub(r"\s+", "", c) for c in commands):
                pass
            else:
                want = tokens(cmd)
                best = max((len(want & tokens(c)) / len(want) for c in commands), default=0.0) if want else 0.0
                if best >= 0.5:
                    ok = None
                    notes.append("PARAPHRASED: the command shown differs from what ran (%.0f%% of its tokens "
                                 "match); show the command that ran, or run the one shown" % (best * 100))
                else:
                    ok = False
                    notes.append("NOT RUN: no run_command resembles %r" % cmd[:70])
        results.append((ok, tier, inside, notes))
    return results


def main():
    ap = argparse.ArgumentParser(description="Check evidence labels against a transcript")
    ap.add_argument("answer", help="file holding the answer text, or - for stdin")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--transcript")
    g.add_argument("--conversation")
    g.add_argument("--latest", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.answer == "-" else open(a.answer, encoding="utf-8").read()
    transcript = find_transcript(a)
    results = check(text, transcript)
    bad = [r for r in results if r[0] is False]
    warn = [r for r in results if r[0] is None]
    print("transcript: %s" % transcript)
    print("labels checked: %d, holding: %d, warnings: %d, failing: %d"
          % (len(results), len(results) - len(bad) - len(warn), len(warn), len(bad)))
    for ok, tier, inside, notes in results:
        if ok is not True:
            print("\n%s  %s (%s)" % ("FAIL" if ok is False else "WARN", tier, inside[:110].replace("\n", " ")))
            for n in notes:
                print("      " + n)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
