#!/usr/bin/env python3
"""Check an answer's evidence labels against what the conversation actually did.

Every `read (...)`, `observed (...)` and `executed (...)` label in the answer is
compared with the transcript of the conversation that wrote it:

  read      the URL was opened with read_url_content, or the path with view_file,
            the call succeeded, and the quoted text appears in what that source
            returned (not merely somewhere else in the conversation)
  observed  the path or URL was opened, and the call succeeded
  executed  the command shown is the command a successful run_command ran

Each tool call is paired with its own result step, so a failed fetch or a denied
command does not count. URLs must match exactly once case, a trailing slash, the
fragment, http/https and a leading www. are set aside; a label citing a parent of
a page that was opened is a warning, and one citing a page deeper than anything
opened fails. Paths may be Windows, file:///, POSIX (/home/x) or ~/ paths, and
match exactly or as a suffix on a path-segment boundary.

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
# Balanced parentheses stay inside a URL (Wikipedia and Commons titles use them).
URL = re.compile(r"https?://(?:[^\s\"'`<>()\[\]{}]|\([^\s\"'`<>()]*\))+")
WINPATH = re.compile(r"(?:\b[A-Za-z]:[\\/]|\bfile://)[^\s\"'`,;()<>|*]+", re.I)
# POSIX absolute and ~/ paths. The look-behind keeps out fractions (1/102), "and/or",
# and the path part of a URL or of a Windows path.
POSIX = re.compile(r"(?<![\w/\\:.~\-])(?:~[\\/]|/(?=[\w.~\-]))[^\s\"'`,;()<>|*]*")
SCRIPT_PATH = re.compile(r"[^\s\"'`=]*[\\/]([\w.-]+\.(?:py|js|mjs|ts|sh|ps1|rb|go))\b", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{12,})[\"”]")
SAVED_TO = re.compile(r"has been saved to:\s*(\S+)")
NOT_RESULTS = {"PLANNER_RESPONSE", "USER_INPUT", "SYSTEM_MESSAGE", "EPHEMERAL_MESSAGE",
               "ERROR_MESSAGE", "CHECKPOINT"}


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def find_transcript(a):
    if a.transcript:
        if not os.path.isfile(a.transcript):
            fail("transcript not found: %s" % a.transcript)
        return a.transcript
    pattern = "*/.system_generated/logs/transcript_full.jsonl"
    found = [p for r in ROOTS for p in glob.glob(os.path.join(r, pattern))]
    if a.conversation:
        found = [p for p in found if a.conversation in p]
    if not found:
        fail("no transcript found")
    return max(found, key=os.path.getmtime)


def label_spans(text):
    """Yield (tier, inside) for each label, matching parentheses so nested ones survive. A
    parenthesis inside a quoted line, as in "export async function logout(", is not counted,
    unless the label's quote marks never pair up; then every parenthesis counts."""
    for m in LABEL.finditer(text):
        for skip_quoted in (True, False):
            depth, i, quoted = 1, m.end(), False
            while i < len(text) and depth:
                ch = text[i]
                if skip_quoted and ch in ("\"”" if quoted else "\"“”"):
                    quoted = not quoted
                elif not quoted:
                    depth += {"(": 1, ")": -1}.get(ch, 0)
                i += 1
            if not depth:
                break
        yield m.group(1), text[m.end():i - 1]


def find_urls(text):
    return [u.rstrip(".,;:!?*") for u in URL.findall(text)]


def norm_url(u):
    """Comparison key: no scheme, no leading www., no fragment, no trailing slash, lower case."""
    u = unquote(u.strip()).rstrip(".,;:!?*").split("#")[0].lower()
    u = re.sub(r"^[a-z][a-z0-9+.-]*://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = re.sub(r"^([^/?#]+):(?:80|443)(?=[/?]|$)", r"\1", u)  # default ports
    return u.rstrip("/?")


def url_below(child, parent):
    """True when child is a page under parent, on a path-segment boundary."""
    return child != parent and (child.startswith(parent + "/") or child.startswith(parent + "?"))


def norm_path(p):
    p = unquote(p.strip())
    if p.lower().startswith("file://"):
        p = p[7:]
        if re.match(r"/[A-Za-z]:", p):
            p = p[1:]
    p = p.replace("\\", "/")
    if p.startswith("~/"):
        p = os.path.expanduser("~").replace("\\", "/").rstrip("/") + p[1:]
    p = re.sub(r"(?<!^)/{2,}", "/", p)
    p = re.sub(r"(?:#L\d+.*|:\d+(?::\d+)?)$", "", p)  # line references such as x.py:12 or x.md#L4
    return p.rstrip("/.:").lower()


def find_paths(text):
    """Local paths in a label, with URLs already removed from the text."""
    found = []

    def keep(m):
        found.append(m.group(0))
        return " "
    text = WINPATH.sub(keep, text)
    for m in POSIX.finditer(text):
        p = m.group(0).rstrip(".,:;!?")
        segs = [s for s in re.split(r"[\\/]", p) if s]
        if not segs or p.startswith("~"):
            if segs[1:]:
                found.append(p)
            continue
        if all(re.fullmatch(r"[\d.]+", s) for s in segs):
            continue
        if len(segs) >= 2 or "." in segs[-1].strip("."):
            found.append(p)
    return found


def path_matches(label_path, opened):
    if opened == label_path:
        return True
    if label_path.startswith("/") and re.sub(r"^[a-z]:", "", opened) == label_path:
        return True  # Antigravity drops the drive letter when it compares Windows paths
    absolute = label_path.startswith("/") or re.match(r"[a-z]:/", label_path)
    return not absolute and opened.endswith("/" + label_path)


def squash(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or ""))
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t).strip().lower()


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def split_commands(cmd):
    """Split a shell line on unquoted ;, && and ||, and on newlines unless the command
    holds a heredoc, whose body lines are not commands of their own."""
    heredoc = re.search(r"<<-?\s*['\"]?\w+", cmd or "") is not None
    parts, cur, quote, i = [], [], None, 0
    while i < len(cmd):
        ch = cmd[i]
        if quote:
            if ch == quote:
                quote = None
            cur.append(ch)
        elif ch in "\"'":
            quote = ch
            cur.append(ch)
        elif (ch == ";" or (ch == "\n" and not heredoc)) or cmd[i:i + 2] in ("&&", "||"):
            parts.append("".join(cur))
            cur = []
            i += 1 if ch in ";\n" else 2
            continue
        else:
            cur.append(ch)
        i += 1
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def canon_command(c):
    """Script paths reduced to base names, quote marks removed, runs of whitespace made one
    space. Case is kept: `ls -R` and `ls -r` are different commands."""
    c = (c or "").replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    c = SCRIPT_PATH.sub(r"\1", c)
    c = re.sub(r"[\"'`]", "", c)
    c = re.sub(r"\s+", " ", c).strip()
    # spaces beside punctuation carry no meaning (1 + 1, f(a, b)); spaces between words do
    return re.sub(r"\s*([^\w\s])\s*", r"\1", c)


def clean_row(r):
    """A transcript row with the fields this script reads coerced to the expected types."""
    r = dict(r)
    calls = r.get("tool_calls")
    if isinstance(calls, dict):
        calls = [calls]
    r["tool_calls"] = [c if isinstance(c.get("args"), dict) else dict(c, args={})
                       for c in (calls if isinstance(calls, list) else []) if isinstance(c, dict)]
    if not isinstance(r.get("content"), str):
        r["content"] = "" if r.get("content") is None else json.dumps(r.get("content"))
    return r


class Transcript(object):
    """Tool calls paired with their results, grouped by what they opened or ran."""

    def __init__(self, path):
        try:
            with open(path, encoding="utf-8-sig") as f:
                rows = [json.loads(l) for l in f if l.strip()]
        except (OSError, ValueError) as e:
            fail("cannot read transcript %s: %s" % (path, e))
        rows = [clean_row(r) for r in rows if isinstance(r, dict)]
        steps = os.path.join(os.path.dirname(os.path.dirname(path)), "steps")
        by_index = {r.get("step_index"): r for r in rows if isinstance(r.get("step_index"), int)}
        self.urls = {}       # url key -> list of (ok, text, error)
        self.paths = {}      # path key -> list of (ok, text, error)
        self.commands = []   # (ok, raw command)
        search, corpus, saved = [], [], []

        def step_files(res):
            i = res.get("step_index") if res else None
            if not isinstance(i, int):
                return ""
            return "\n".join(read_text(os.path.join(steps, str(i), n)) for n in ("content.md", "output.txt"))

        for pos, r in enumerate(rows):
            calls = r.get("tool_calls") or []
            for j, (call, res) in enumerate(zip(calls, self._results(rows, pos, by_index, len(calls)))):
                name, args = call.get("name"), call.get("args") or {}
                ok = res is not None and res.get("status") != "ERROR"
                text = ((res or {}).get("content") or "") + "\n" + step_files(res)
                error = ""
                if res is None:
                    error = "the call returned no result"
                elif not ok:
                    error = (res.get("error") or res.get("content") or "").strip()
                    error = re.sub(r"^.*?Encountered error in step execution:\s*", "", error, flags=re.S)
                    error = error.splitlines()[0][:120] if error else "the step returned an error"
                if name == "read_url_content":
                    key = norm_url(args.get("Url") or args.get("url") or "")
                    self.urls.setdefault(key, []).append((ok, text, error))
                    m = SAVED_TO.search((res or {}).get("content") or "")
                    if ok and m and norm_path(m.group(1)).startswith(norm_path(steps) + "/"):
                        saved.append((key, norm_path(m.group(1))))
                elif name == "view_file":
                    text = re.sub(r"(?m)^\d+: ", "", text)  # view_file numbers every line
                    key = norm_path(args.get("AbsolutePath") or "")
                    self.paths.setdefault(key, []).append((ok, text, error))
                elif name == "run_command":
                    self.commands.append((ok, args.get("CommandLine") or ""))
                elif name == "search_web":
                    search.append(text)
                corpus.append(text)
            content = r.get("content") or ""
            if r.get("type") == "PLANNER_RESPONSE":
                continue  # the answer itself is not evidence
            if "search for" in content[:400] or "returned the following summary" in content[:600]:
                search.append(content)
            corpus.append(content)
        for p in glob.glob(os.path.join(steps, "*", "content.md")) + glob.glob(os.path.join(steps, "*", "output.txt")):
            corpus.append(read_text(p))
        # A fetched page saved to disk is the same source as its URL, whichever the label cites.
        for key, spath in saved:
            page = "\n".join(t for ok, t, _ in self.urls[key] if ok)
            views = "\n".join(t for ok, t, _ in self.paths.get(spath, []) if ok)
            self.urls[key].append((True, views, ""))
            self.paths.setdefault(spath, []).append((True, page, ""))
        self.searched = unquote(squash(" ".join(search)))
        self.corpus_grams = shingles(" ".join(corpus))

    @staticmethod
    def _results(rows, pos, by_index, n):
        """The result step of each of the n calls made at rows[pos], or None: the next n
        steps that are results, skipping system and user steps, up to the next response."""
        found = []
        for r in rows[pos + 1:]:
            if r.get("type") == "PLANNER_RESPONSE" or len(found) == n:
                break
            if r.get("type") not in NOT_RESULTS:
                found.append(r)
        return found + [None] * (n - len(found))

    def opened_urls(self):
        return {k for k, v in self.urls.items() if any(ok for ok, _, _ in v)}

    def url_text(self, key):
        return "\n".join(t for ok, t, _ in self.urls.get(key, []) if ok)

    def in_search(self, key):
        return re.search(re.escape(key) + r"(?:/|\?|#|[\s\"'<>)\],]|$)", self.searched) is not None


CJK = "\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff"
TOKEN = re.compile(r"[%s]|[^\W_%s]+" % (CJK, CJK))


def words(text):
    text = re.sub(r"(?<![\d.])\d{1,2}\.\s", " ", text or "")  # list numbering such as "7. "
    return TOKEN.findall(squash(text))


def shingles(text, n=4):
    w = words(text)
    return {" ".join(w[i:i + n]) for i in range(max(len(w) - n + 1, 0))}


def tokens(text):
    return set(re.findall(r"[a-z_][a-z0-9_]{2,}|\d+(?:\.\d+)?", text.lower()))


def check_locators(t, inside, notes):
    """Return (ok, texts of the cited sources that were opened, names of those sources)."""
    ok, texts, cited = True, [], []
    urls = find_urls(inside)
    paths = find_paths(URL.sub(" ", inside))
    if not urls and not paths:
        notes.append("NO LOCATOR: the label names no URL or path")
        return False, texts, cited
    opened = t.opened_urls()
    for raw in urls:
        u = norm_url(raw)
        if u in opened:
            texts.append(t.url_text(u))
            cited.append(raw)
            continue
        below = sorted(x for x in opened if url_below(x, u))
        above = sorted(x for x in opened if url_below(u, x))
        if u in t.urls:
            ok = False
            errors = [e for good, _, e in t.urls[u] if not good]
            notes.append("FETCH FAILED: %s (%s)" % (raw, errors[0] if errors else "the fetch returned an error"))
        elif below:
            if ok is True:
                ok = None
            texts.extend(t.url_text(x) for x in below)
            cited.extend(below)
            notes.append("PARENT PAGE: %s itself was not opened, only the page(s) under it: %s"
                         % (raw, ", ".join(below[:3])))
        elif above:
            ok = False
            notes.append("NOT OPENED: %s (only the page above it was opened: %s)" % (raw, above[0]))
        elif t.in_search(u):
            ok = False
            notes.append("SEARCH-ONLY: %s appears only in a search summary" % raw)
        else:
            ok = False
            notes.append("NOT OPENED: %s" % raw)
    for raw in paths:
        p = norm_path(raw)
        hits = [k for k in t.paths if path_matches(p, k)]
        good = [t_ for k in hits for g, t_, _ in t.paths[k] if g]
        if any(g for k in hits for g, _, _ in t.paths[k]):
            texts.extend(good)
            cited.append(raw)
        elif hits:
            ok = False
            errors = [e for k in hits for g, _, e in t.paths[k] if not g]
            notes.append("FETCH FAILED: %s (%s)" % (raw, errors[0] if errors else "view_file returned an error"))
        else:
            ok = False
            notes.append("NOT OPENED: %s" % raw)
    return ok, texts, cited


def check_quotes(t, inside, ok, texts, cited, notes):
    source_grams = shingles("\n".join(texts))
    for q in QUOTE.findall(inside):
        # Compare runs of four words, so changed punctuation, quote marks or list
        # numbering do not count as fabrication, and an ellipsis can join passages.
        grams = shingles(q)
        if not grams:
            short = " ".join(words(q))
            if short and short not in " ".join(words("\n".join(texts))):
                ok = False
                notes.append("QUOTE NOT FOUND in the cited source: \"%s\"" % q[:70])
            continue
        share = len(grams & source_grams) / len(grams)
        if share >= 0.9:
            continue
        if share >= 0.6:
            if ok is True:
                ok = None
            notes.append("QUOTE REFORMATTED or partly paraphrased (%.0f%% of it matches): \"%s\""
                         % (share * 100, q[:70]))
            continue
        ok = False
        elsewhere = len(grams & t.corpus_grams) / len(grams)
        if elsewhere >= 0.6 and cited:
            notes.append("QUOTE NOT IN CITED SOURCE: %.0f%% of it is elsewhere in the conversation but only "
                         "%.0f%% is in %s: \"%s\"" % (elsewhere * 100, share * 100, ", ".join(cited), q[:70]))
        elif elsewhere >= 0.6:
            notes.append("QUOTE NOT IN CITED SOURCE: %.0f%% of it is elsewhere in the conversation, but no "
                         "source the label cites was opened: \"%s\"" % (elsewhere * 100, q[:70]))
        else:
            notes.append("QUOTE NOT FOUND in anything fetched (%.0f%% of it matches): \"%s\""
                         % (elsewhere * 100, q[:70]))
    return ok


def check_command(t, inside, notes):
    # The label may be `command -> output`, and the command may itself contain an arrow,
    # so every prefix that ends before an arrow is a candidate for the command shown.
    cuts = [m.start() for m in re.finditer(r"\s*(?:->|=>|→)", inside)]
    shown = [inside[:c].strip().strip("`") for c in cuts] + [inside.strip().strip("`")]
    cmd = shown[0]
    wants = {canon_command(s) for s in shown if s}

    def parts(c):
        return [canon_command(s) for s in [c] + split_commands(c)]

    def same(c):
        return bool(wants & set(parts(c)))
    if any(same(c) for ok, c in t.commands if ok):
        return True
    if any({w.lower() for w in wants} & {p.lower() for p in parts(c)} for ok, c in t.commands if ok):
        notes.append("PARAPHRASED: the command shown differs from what ran only in letter case; "
                     "show the command exactly as it ran")
        return None
    if any(same(c) for ok, c in t.commands if not ok):
        notes.append("NOT RUN: the run_command for %r returned an error (denied or blocked), so it did not run"
                     % cmd[:70])
        return False
    wanted = tokens(cmd)
    ran = [c for ok, c in t.commands if ok]
    best = max((len(wanted & tokens(c)) / len(wanted) for c in ran), default=0.0) if wanted else 0.0
    if best >= 0.5:
        notes.append("PARAPHRASED: the command shown differs from what ran (%.0f%% of its tokens "
                     "match); show the command that ran, or run the one shown" % (best * 100))
        return None
    notes.append("NOT RUN: no run_command resembles %r" % cmd[:70])
    return False


def check(answer, transcript):
    t = transcript if isinstance(transcript, Transcript) else Transcript(transcript)
    results = []
    for tier, inside in label_spans(answer):
        notes = []
        if tier in ("read", "observed"):
            ok, texts, cited = check_locators(t, inside, notes)
            if tier == "read":
                ok = check_quotes(t, inside, ok, texts, cited, notes)
        else:
            ok = check_command(t, inside, notes)
        results.append((ok, tier, inside, notes))
    return results


def utf8_stdout():
    """Label text may hold any character; a redirected Windows stdout would refuse it."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass  # not a TextIOWrapper (or Python without reconfigure): leave it as it is


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description="Check evidence labels against a transcript")
    ap.add_argument("answer", help="file holding the answer text, or - for stdin")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--transcript")
    g.add_argument("--conversation")
    g.add_argument("--latest", action="store_true")
    a = ap.parse_args()
    try:
        if a.answer == "-":
            text = sys.stdin.buffer.read().decode("utf-8-sig")
        else:
            with open(a.answer, encoding="utf-8-sig") as f:
                text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        fail("cannot read answer (it must be UTF-8 text): %s" % e)
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
